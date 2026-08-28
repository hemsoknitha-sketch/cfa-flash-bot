"""
Super Smart Telegram Live Telemetry & Engagement Engine V8.0 GOLD STANDARD.
Implements:
1. Interactive 1-Click Reactions (👍 Like, ❤️ Love, 🔥 Fire, 🇰🇭 Pride).
2. Live Real-Time Views & Impression Counter.
3. Live Comment Discussion Threads per news post.
4. Live 1-Click Share & Forward Tracking.
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class TelegramEngagementEngine:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.db_file = os.path.join(self.data_dir, "news_engagement_db.json")
        self.db: Dict[str, Dict] = self._load_db()

    def _load_db(self) -> Dict[str, Dict]:
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            except Exception as e:
                logger.error(f"Error loading engagement DB: {e}")
        return {}

    def _save_db(self):
        try:
            with open(self.db_file, "w", encoding="utf-8") as f:
                json.dump(self.db, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving engagement DB: {e}")

    def get_post_stats(self, post_id: str) -> Dict:
        """Returns stats for a given news post ID."""
        if post_id not in self.db:
            self.db[post_id] = {
                "views": 1,
                "shares": 0,
                "reactions": {"up": {}, "love": {}, "fire": {}, "khmer": {}},
                "comments": []
            }
            self._save_db()
        return self.db[post_id]

    def increment_view(self, post_id: str) -> int:
        stats = self.get_post_stats(post_id)
        stats["views"] = stats.get("views", 0) + 1
        self._save_db()
        return stats["views"]

    def increment_share(self, post_id: str) -> int:
        stats = self.get_post_stats(post_id)
        stats["shares"] = stats.get("shares", 0) + 1
        self._save_db()
        return stats["shares"]

    def toggle_reaction(self, user_id: int, post_id: str, reaction_type: str) -> Dict:
        """Toggles user reaction (up, love, fire, khmer) and returns updated status."""
        stats = self.get_post_stats(post_id)
        reactions = stats.setdefault("reactions", {"up": {}, "love": {}, "fire": {}, "khmer": {}})
        user_str = str(user_id)
        
        target_dict = reactions.setdefault(reaction_type, {})
        toggled_on = False
        
        if user_str in target_dict:
            del target_dict[user_str]
            toggled_on = False
        else:
            target_dict[user_str] = time.strftime("%Y-%m-%d %H:%M:%S")
            toggled_on = True

        self._save_db()
        
        counts = {
            "up": len(reactions.get("up", {})),
            "love": len(reactions.get("love", {})),
            "fire": len(reactions.get("fire", {})),
            "khmer": len(reactions.get("khmer", {}))
        }
        return {"toggled_on": toggled_on, "counts": counts}

    def add_comment(self, user_id: int, user_name: str, post_id: str, comment_text: str) -> Dict:
        """Adds a direct user comment to a news post."""
        stats = self.get_post_stats(post_id)
        comments = stats.setdefault("comments", [])
        comment_entry = {
            "user_id": user_id,
            "user_name": user_name,
            "text": comment_text,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        comments.append(comment_entry)
        self._save_db()
        return {"comment_count": len(comments), "comment": comment_entry}

    def build_engagement_inline_keyboard(self, post_id: str) -> List[List[Dict]]:
        """Builds Telegram Inline Keyboard containing Live Reactions, Views, Shares & Comments."""
        stats = self.get_post_stats(post_id)
        reactions = stats.get("reactions", {})
        up_cnt = len(reactions.get("up", {}))
        love_cnt = len(reactions.get("love", {}))
        fire_cnt = len(reactions.get("fire", {}))
        khmer_cnt = len(reactions.get("khmer", {}))
        
        views_cnt = stats.get("views", 1)
        shares_cnt = stats.get("shares", 0)
        comments_cnt = len(stats.get("comments", []))

        keyboard = [
            [
                {"text": f"👍 {up_cnt}", "callback_data": f"rx_up_{post_id}"},
                {"text": f"❤️ {love_cnt}", "callback_data": f"rx_love_{post_id}"},
                {"text": f"🔥 {fire_cnt}", "callback_data": f"rx_fire_{post_id}"},
                {"text": f"🇰🇭 {khmer_cnt}", "callback_data": f"rx_khmer_{post_id}"}
            ],
            [
                {"text": f"💬 មតិពិភាក្សា ({comments_cnt})", "callback_data": f"cmt_list_{post_id}"},
                {"text": f"📲 ចែករំលែក ({shares_cnt})", "callback_data": f"share_post_{post_id}"},
                {"text": f"👁️ {views_cnt} Views", "callback_data": f"vw_info_{post_id}"}
            ]
        ]
        return keyboard

# Global Instance
engagement_engine = TelegramEngagementEngine()
