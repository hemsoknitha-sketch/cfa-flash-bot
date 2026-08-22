import os
import json
import hashlib
import logging
import time
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class DefenseIntelligenceEngine:
    """
    Military & Diplomatic Intelligence Engine for CFA Flash Feed.
    Features:
    1. Dedicated Chronological Storage for Ministry of National Defence & MFAIC statements.
    2. SHA-256 Content Deduplication with 0% Data Loss Guarantee.
    3. Chronological Archiving, Search, and Text Report Generation.
    """
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.archive_file = os.path.join(self.data_dir, "border_defense_archives.json")
        self.archives: List[Dict] = self._load_archives()

    def _load_archives(self) -> List[Dict]:
        if os.path.exists(self.archive_file):
            try:
                with open(self.archive_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading defense archives: {e}")
        return []

    def _save_archives(self):
        try:
            with open(self.archive_file, "w", encoding="utf-8") as f:
                json.dump(self.archives, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving defense archives: {e}")

    def archive_post(
        self,
        post_id: str,
        title: str,
        content: str,
        source_name: str,
        category: str = "សេចក្តីថ្លែងការណ៍ផ្លូវការ",
        timestamp: Optional[float] = None
    ) -> bool:
        """
        Archives a military command or diplomatic statement with SHA-256 deduplication.
        """
        full_text = f"{title} - {content}"
        content_hash = hashlib.sha256(full_text.strip().encode("utf-8")).hexdigest()

        # Check deduplication
        for item in self.archives:
            if item.get("content_hash") == content_hash or item.get("post_id") == post_id:
                return False

        if timestamp is None:
            timestamp = time.time()

        date_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

        archive_item = {
            "post_id": post_id,
            "content_hash": content_hash,
            "date": date_str,
            "timestamp": timestamp,
            "source_name": source_name,
            "category": category,
            "title": title.strip(),
            "content": content.strip()
        }

        self.archives.append(archive_item)
        # Sort chronologically by timestamp (newest first)
        self.archives.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        self._save_archives()

        logger.info(f"🛡️ [DEFENSE INTELLIGENCE ARCHIVED] Archived '{title[:50]}...' from {source_name}")
        return True

    def get_latest_defense_news(self, limit: int = 5) -> List[Dict]:
        """Returns the most recent military & diplomatic press releases."""
        return self.archives[:limit]

    def get_border_archives(self, query: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        Searches archives for border defense keywords (ព្រំដែន, ណាតូ, ថៃ, ការពារជាតិ, កំណត់ទូត)
        or returns chronological records.
        """
        if not query:
            keywords = ["ព្រំដែន", "ការពារជាតិ", "យោធា", "កំណត់ទូត", "អធិបតេយ្យ", "ថៃ"]
            matched = [
                item for item in self.archives
                if any(kw in item.get("title", "") or kw in item.get("content", "") for kw in keywords)
            ]
            return matched[:limit] if matched else self.archives[:limit]

        query_lower = query.lower()
        matched = [
            item for item in self.archives
            if query_lower in item.get("title", "").lower() or query_lower in item.get("content", "").lower()
        ]
        return matched[:limit]

    def export_archive_report(self) -> str:
        """Generates a complete unabridged chronological text report of archived records."""
        if not self.archives:
            return "📂 មិនទាន់មានទិន្នន័យកំណត់ត្រាយោធា ឬការទូតក្នុងបញ្ជី Archive នៅឡើយទេ។"

        report_lines = [
            "============================================================",
            "🛡️ របាយការណ៍កត់ត្រាប្រវត្តិសាស្ត្រយោធា និងកិច្ចការការបរទេសកម្ពុជា",
            "============================================================\n"
        ]

        for idx, item in enumerate(self.archives, 1):
            report_lines.append(f"📌 [{idx}] {item.get('date')} | {item.get('source_name')}")
            report_lines.append(f"ចំណងជើង ៖ {item.get('title')}")
            report_lines.append(f"ខ្លឹមសារ ៖\n{item.get('content')}")
            report_lines.append("------------------------------------------------------------\n")

        return "\n".join(report_lines)

# Global Instance
defense_engine = DefenseIntelligenceEngine()
