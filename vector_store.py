import time
import math
import logging
from typing import List, Tuple, Dict
import numpy as np
from config import config

logger = logging.getLogger(__name__)

class VectorDeduplicator:
    """
    Enterprise Vector Deduplication Engine.
    Uses Qdrant Vector Database + BAAI/bge-m3 Flagship 1024-dim Multilingual Embeddings
    with TF-IDF Cosine Fallback.
    """
    def __init__(self, similarity_threshold: float = config.SIMILARITY_THRESHOLD, window_seconds: int = 3600, enable_local_embeddings: bool = False):
        self.similarity_threshold = similarity_threshold
        self.window_seconds = window_seconds
        self.enable_local_embeddings = enable_local_embeddings
        
        self.qdrant_enabled = False
        self.qdrant_client = None
        self.encoder = None
        self.collection_name = "news_vectors"
        self.vector_size = config.QDRANT_VECTOR_SIZE

        # Fast memory store & persistent SHA-256 content hash cache
        import os
        import json
        self.history: List[Dict] = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.cache_file = os.path.join(base_dir, "seen_hashes.json")
        self.seen_hashes: set = self._load_seen_hashes()

        if self.enable_local_embeddings:
            self._init_qdrant()
        else:
            logger.info("⚡ [LIGHTWEIGHT MODE] Vector Deduplication running on SHA-256 + TF-IDF Engine (<5MB RAM).")

    def _load_seen_hashes(self) -> set:
        import os
        import json
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} cached news hashes from seen_hashes.json.")
                    return set(data)
            except Exception as e:
                logger.error(f"Error loading seen_hashes.json: {e}")
        return set()

    def _save_seen_hashes(self):
        import json
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(list(self.seen_hashes), f)
        except Exception as e:
            logger.error(f"Error saving seen_hashes.json: {e}")

    def purge_temp_banner_files(self) -> int:
        """Deletes all temporary banner images and temp HTML files from the project directory."""
        import glob
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        patterns = ["banner_*.jpg", "temp_banner.html", "test_*.jpg", "test_*.png"]
        removed_count = 0
        for pattern in patterns:
            for filepath in glob.glob(os.path.join(base_dir, pattern)):
                try:
                    os.remove(filepath)
                    removed_count += 1
                except Exception as e:
                    logger.error(f"Could not remove temp banner file {filepath}: {e}")
        logger.info(f"🧹 [TEMP BANNERS PURGED] Removed {removed_count} temporary banner files.")
        return removed_count

    def clear_news_cache(self) -> int:
        """Clears all old cached news hashes and history while keeping user/admin settings 100% intact."""
        count = len(self.seen_hashes)
        self.seen_hashes.clear()
        self.history.clear()
        self._save_seen_hashes()
        self.purge_temp_banner_files()
        logger.info(f"🧹 [NEWS DEDUPLICATION CACHE PURGED] Cleared {count} old news hashes & temp banner files.")
        return count

    async def seed_baseline_from_rss_async(self, ingestion_engine) -> int:
        """
        Seeds existing news from active RSS feeds into seen_hashes as baseline.
        This prevents old feed items from being processed as 'new news' on initial boot,
        after a /clearcache command, or after restarting/updating on Google Cloud.
        """
        import hashlib
        try:
            items = await ingestion_engine.fetch_from_rss_async()
            count = 0
            for item in items:
                full_text = f"{item.title} - {item.content}"
                content_hash = hashlib.sha256(full_text.strip().encode('utf-8')).hexdigest()
                if content_hash not in self.seen_hashes:
                    self.seen_hashes.add(content_hash)
                    count += 1
            self._save_seen_hashes()
            logger.info(f"🛡️ [BASELINE SEEDED] Seeded {count} current RSS feed items into seen_hashes.json as baseline.")
            return count
        except Exception as e:
            logger.error(f"Error seeding baseline hashes from RSS: {e}")
            return 0

    def _init_qdrant(self):
        """Initialize Qdrant Vector DB & SentenceTransformer model if explicitly enabled."""
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.models import VectorParams, Distance
            from sentence_transformers import SentenceTransformer

            # Step 1: Try connecting to Qdrant Server at localhost:6333, fallback to :memory:
            try:
                import socket
                logger.info(f"Checking Qdrant Server at {config.QDRANT_HOST}:{config.QDRANT_PORT}...")
                with socket.create_connection((config.QDRANT_HOST, config.QDRANT_PORT), timeout=1.0):
                    pass
                self.qdrant_client = QdrantClient(host=config.QDRANT_HOST, port=config.QDRANT_PORT)
                logger.info(f"✅ Connected to Qdrant Server on {config.QDRANT_HOST}:{config.QDRANT_PORT}")
            except Exception as conn_err:
                logger.info("Local Qdrant Server not detected. Using In-Memory Qdrant Vector Engine.")
                self.qdrant_client = QdrantClient(":memory:")

            # Step 2: Load model
            try:
                logger.info(f"Loading Multilingual Embedding Model ('{config.QDRANT_MODEL}')...")
                self.encoder = SentenceTransformer(config.QDRANT_MODEL)
                self.vector_size = self.encoder.get_sentence_embedding_dimension()
            except Exception as model_err:
                logger.warning(f"Failed to load '{config.QDRANT_MODEL}': {model_err}. Falling back to 'all-MiniLM-L6-v2'.")
                self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
                self.vector_size = self.encoder.get_sentence_embedding_dimension()

            # Step 3: Recreate Collection
            self.qdrant_client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE),
            )
            self.qdrant_enabled = True
            logger.info(f"⚡ [QDRANT VECTOR DB READY] Collection '{self.collection_name}' (dim={self.vector_size}) Active!")
        except Exception as e:
            logger.warning(f"Could not initialize Qdrant/SentenceTransformers: {e}. Falling back to TF-IDF Engine.")
            self.qdrant_enabled = False

    def is_duplicate(self, text: str) -> Tuple[bool, float, str]:
        """
        Check if text is duplicate (similarity >= threshold or exact SHA256 hash match).
        Returns: (is_dup: bool, max_similarity: float, matched_id: str)
        """
        import hashlib
        content_hash = hashlib.sha256(text.strip().encode('utf-8')).hexdigest()
        if content_hash in self.seen_hashes:
            return True, 1.0, f"hash_{content_hash[:8]}"

        if self.qdrant_enabled:
            return self._is_duplicate_qdrant(text)
        return self._is_duplicate_tfidf(text)

    def add_item(self, item_id: str, text: str):
        """Add a processed news item to the vector history and content hash cache."""
        import hashlib
        content_hash = hashlib.sha256(text.strip().encode('utf-8')).hexdigest()
        self.seen_hashes.add(content_hash)
        self._save_seen_hashes()

        if self.qdrant_enabled:
            self._add_item_qdrant(item_id, text)
        else:
            self._add_item_tfidf(item_id, text)

    # --- Qdrant Engine Implementation ---
    def _is_duplicate_qdrant(self, text: str) -> Tuple[bool, float, str]:
        try:
            query_vector = self.encoder.encode(text).tolist()

            # Compatible with qdrant-client >= 1.10.0 (query_points) and older (search)
            if hasattr(self.qdrant_client, "query_points"):
                response = self.qdrant_client.query_points(
                    collection_name=self.collection_name,
                    query=query_vector,
                    limit=1
                )
                search_result = response.points
            elif hasattr(self.qdrant_client, "search"):
                search_result = self.qdrant_client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=1
                )
            else:
                search_result = []

            if search_result:
                top_hit = search_result[0]
                similarity = float(top_hit.score)
                matched_id = str(top_hit.payload.get("id", ""))
                is_dup = similarity >= self.similarity_threshold
                return is_dup, similarity, matched_id
            return False, 0.0, ""
        except Exception as e:
            logger.error(f"Qdrant search error: {e}. Switching to TF-IDF.")
            return self._is_duplicate_tfidf(text)

    def _add_item_qdrant(self, item_id: str, text: str):
        try:
            from qdrant_client.models import PointStruct
            vector = self.encoder.encode(text).tolist()
            point_id = abs(hash(item_id)) % (10**12)
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[
                    PointStruct(
                        id=point_id,
                        vector=vector,
                        payload={"id": item_id, "text": text, "timestamp": time.time()}
                    )
                ]
            )
            logger.info(f"Added news item [{item_id}] to Qdrant Vector Store.")
        except Exception as e:
            logger.error(f"Failed to index point in Qdrant: {e}")

    # --- TF-IDF Engine Fallback Implementation ---
    def _tokenize(self, text: str) -> List[str]:
        words = text.lower().replace(",", " ").replace(".", " ").replace("-", " ").split()
        return [w for w in words if len(w) > 2]

    def _compute_tf_vector(self, text: str) -> Dict[str, float]:
        tokens = self._tokenize(text)
        if not tokens:
            return {}
        counts = {}
        for token in tokens:
            counts[token] = counts.get(token, 0) + 1
        total = len(tokens)
        return {word: count / total for word, count in counts.items()}

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        dot_product = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([val ** 2 for val in vec1.values()])
        sum2 = sum([val ** 2 for val in vec2.values()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        return dot_product / denominator if denominator else 0.0

    def _is_duplicate_tfidf(self, text: str) -> Tuple[bool, float, str]:
        current_time = time.time()
        self.history = [item for item in self.history if (current_time - item['timestamp']) <= self.window_seconds]
        target_vec = self._compute_tf_vector(text)
        if not target_vec:
            return False, 0.0, ""
        max_sim = 0.0
        matched_id = ""
        for item in self.history:
            sim = self._cosine_similarity(target_vec, item['vector'])
            if sim > max_sim:
                max_sim = sim
                matched_id = item['id']
        return max_sim >= self.similarity_threshold, max_sim, matched_id

    def _add_item_tfidf(self, item_id: str, text: str):
        target_vec = self._compute_tf_vector(text)
        self.history.append({
            'id': item_id,
            'text': text,
            'vector': target_vec,
            'timestamp': time.time()
        })
        logger.info(f"Added news item [{item_id}] to TF-IDF Vector Store.")
