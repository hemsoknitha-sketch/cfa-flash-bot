"""
Cambodian Legal Compliance & National Rights Engine
Anchors news items, user queries, and AI analysis directly to current Cambodian National Laws,
Articles of the Constitution, Law on Press Regime, Anti-Corruption Law, and Rule of Law.
"""

import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LAWS_FILE = os.path.join(DATA_DIR, "cambodian_national_laws.json")

class KhmerLegalEngine:
    def __init__(self):
        self.laws: List[Dict[str, Any]] = []
        self._load_laws()

    def _load_laws(self):
        """Loads Cambodian legal articles repository from master file and specialized law files."""
        seen_keys = set()
        laws_list = []

        # List of candidate law files to load from DATA_DIR
        candidate_files = [LAWS_FILE]
        if os.path.exists(DATA_DIR):
            for filename in os.listdir(DATA_DIR):
                if filename.endswith(".json") and filename != "news_engagement_db.json" and filename != "seen_hashes.json":
                    file_path = os.path.join(DATA_DIR, filename)
                    if file_path not in candidate_files:
                        candidate_files.append(file_path)

        for file_path in candidate_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        items = json.load(f)
                        if isinstance(items, list):
                            for item in items:
                                key = (item.get("code_name", ""), item.get("article", ""))
                                if key not in seen_keys:
                                    seen_keys.add(key)
                                    laws_list.append(item)
                except Exception as e:
                    logger.error(f"Error loading Cambodian laws JSON from {file_path}: {e}")

        self.laws = laws_list
        logger.info(f"⚖️ [LEGAL ENGINE] Loaded {len(self.laws)} Cambodian National Legal Provisions.")

    def search_relevant_laws(self, text: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Finds Cambodian legal articles relevant to a given news topic or user question."""
        matched = []
        text_lower = text.lower().strip()
        
        # 1. Exact or keyword match
        for law in self.laws:
            # Check explicit keywords
            kw_match = False
            for kw in law.get("keywords", []):
                if kw.lower() in text_lower:
                    kw_match = True
                    break
            
            if kw_match:
                matched.append(law)
                continue

            # Check title, article, or category
            title = law.get("title", "").lower()
            article = law.get("article", "").lower()
            category = law.get("category", "").lower()
            summary = law.get("summary", "").lower()
            
            if any(term in text_lower for term in [title, article, category]) or any(term in text_lower for term in title.split()):
                matched.append(law)

        # Remove duplicate matched dicts while preserving order
        unique_matched = []
        seen = set()
        for item in matched:
            k = (item.get("code_name"), item.get("article"))
            if k not in seen:
                seen.add(k)
                unique_matched.append(item)

        # Fallback to default provisions if no specific match
        if not unique_matched and self.laws:
            unique_matched = self.laws[:limit]

        return unique_matched[:limit]

    def generate_legal_compliance_citation(self, title: str, content: str) -> str:
        """Generates legal compliance citation footnote for Khmer news articles."""
        relevant = self.search_relevant_laws(f"{title} {content}", limit=2)
        if not relevant:
            return ""

        citation = "\n\n⚖️ *មូលដ្ឋានច្បាប់ និងនីតិរដ្ឋនៃព្រះរាជាណាចក្រកម្ពុជា ៖*\n"
        for item in relevant:
            citation += f"• *{item.get('code_name')} ({item.get('article')}) ៖* {item.get('title')} — «{item.get('summary')}»\n"

        return citation

    async def answer_legal_question(self, question: str) -> str:
        """Answers user legal & constitutional research questions in Khmer."""
        matched_laws = self.search_relevant_laws(question, limit=3)
        laws_context = "\n".join([f"[{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}" for item in matched_laws])

        prompt = (
            "You are the Senior Legal Analyst & Constitutional Scholar for CFA Flash Feed AI Super Brain.\n"
            "Answer the user's research question in authoritative, professional Khmer legal prose.\n"
            "Always anchor your answer to the official Cambodian Constitution, Law on Press, and national statutes.\n\n"
            f"=== CAMBODIAN LEGAL CONTEXT ===\n{laws_context}\n\n"
            f"=== USER LEGAL QUESTION ===\n{question}\n\n"
            "Provide a complete 3-paragraph legal explanation in formal Khmer. End with '៕'."
        )

        # 1. Try Hugging Face Fine-Tuned Model
        try:
            from huggingface_engine import hf_polymath_ai
            hf_res = hf_polymath_ai.ask_polymath_ai(f"វិភាគច្បាប់ជាតិកម្ពុជា ៖ {question}\n\nបរិបទច្បាប់ ៖\n{laws_context}")
            if hf_res and not hf_res.startswith("❌"):
                return f"⚖️ *[ការវិភាគច្បាប់ជាតិកម្ពុជា - AI Legal Engine]*\n\n{hf_res}"
        except Exception as e:
            logger.warning(f"Hugging Face legal AI query failed: {e}")

        # 2. Try Gemini Multi-Key Pool
        try:
            from gemini_key_pool import gemini_key_pool
            client_tuple = gemini_key_pool.get_client()
            if client_tuple:
                client, _ = client_tuple
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                if response and response.text:
                    return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini legal AI query failed: {e}")

        # Rule-based fallback
        law_summary = "\n".join([f"• *{l.get('code_name')} ({l.get('article')})* ៖ {l.get('summary')}" for l in matched_laws])
        return (
            f"⚖️ *ការវិភាគច្បាប់ជាតិកម្ពុជា ៖ «{question}»*\n\n"
            f"រាជធានីភ្នំពេញ៖ យោងតាមក្របខ័ណ្ឌច្បាប់ និងរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ៖\n\n"
            f"{law_summary}\n\n"
            "ផ្អែកលើស្មារតីនៃ មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ការគោរព និងអនុវត្តច្បាប់គឺជាកាតព្វកិច្ចចម្បងក្នុងការការពារសន្តិភាព និងស្ថិរភាពសង្គមជាតិ៕"
        )

# Global Instance
legal_engine = KhmerLegalEngine()
