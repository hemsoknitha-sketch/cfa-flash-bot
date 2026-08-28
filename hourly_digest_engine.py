"""
24/7 Hourly Executive Digest Engine V8.0
Ensures continuous 24/7 news reporting on Telegram VIP Channel & Facebook Page.
If no news has been published for >= 60 minutes, automatically aggregates top 3 verified news items
across 79+ national & global feeds into an executive bulletin.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

TRACKER_FILE = os.path.join("data", "last_publish_tracker.json")

class HourlyDigestEngine:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.last_published_time = self._load_last_published_time()

    def _load_last_published_time(self) -> float:
        if os.path.exists(TRACKER_FILE):
            try:
                with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return float(data.get("last_published_time", time.time()))
            except Exception as e:
                logger.warning(f"Failed to load last publish tracker: {e}")
        return time.time()

    def record_publication(self):
        """Call this whenever any Flash News or Digest is published to reset the 60-minute timer."""
        self.last_published_time = time.time()
        try:
            with open(TRACKER_FILE, "w", encoding="utf-8") as f:
                json.dump({"last_published_time": self.last_published_time}, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save last publish tracker: {e}")

    async def check_and_trigger_hourly_digest(self, force: bool = False) -> bool:
        """
        Checks if 60 minutes have elapsed since last publication.
        If true (or force=True), aggregates top 3 verified news items and dispatches the bulletin.
        """
        elapsed = time.time() - self.last_published_time
        if not force and elapsed < 3600:
            logger.info(f"⏳ [HOURLY DIGEST] Timer check: {elapsed/60:.1f} mins elapsed (< 60 mins). No digest needed.")
            return False

        logger.info(f"📰 [HOURLY DIGEST] Triggering 24/7 Hourly Executive Digest (Elapsed: {elapsed/60:.1f} mins)...")
        from defense_intelligence_engine import defense_engine
        from khmer_auditor import khmer_auditor
        from ai_rewriter import SuperBrainAIRewriter
        from telegram_broadcaster import telegram_broadcaster

        rewriter = SuperBrainAIRewriter()
        items = defense_engine.get_latest_defense_news(6)

        valid_items = []
        for it in items:
            h = it.get("title", "")
            b = it.get("content", "")
            src = it.get("source_name", "សារព័ត៌មានផ្លូវការ")
            is_valid, quality_score, clean_h, clean_b, verified_src, _ = khmer_auditor.evaluate_news_quality_score(h, b, src)
            if is_valid:
                valid_items.append((clean_h, clean_b, verified_src))
            if len(valid_items) >= 3:
                break

        if not valid_items:
            logger.warning("⚠️ [HOURLY DIGEST] No valid items available for hourly digest.")
            return False

        dateline_str = khmer_auditor.format_khmer_dateline()

        digest_body = (
            f"📰 *របាយការណ៍សង្ខេបព័ត៌មានជាតិ និងអន្តរជាតិប្រចាំម៉ោង - 24/7 HOURLY EXECUTIVE DIGEST*\n\n"
            f"{dateline_str}\n"
            f"🏛️ *ប្រភពដកស្រង់ ៖ ស្ថាប័នរដ្ឋ និងសារព័ត៌មានផ្លូវការទាំង ៧៩ ស្ថាប័ន*\n\n"
        )

        for idx, (title, body, src) in enumerate(valid_items, 1):
            short_body = body[:250].strip()
            if not short_body.endswith("។") and not short_body.endswith("៕"):
                short_body += "..."
            digest_body += (
                f"*{idx}. {title}*\n"
                f"• ប្រភព ៖ {src}\n"
                f"{short_body}\n\n"
            )

        digest_body += (
            f"🔍 *ព័ត៌មាន 24/7*\n"
            f"• បច្ចេកទេស: *AI APEX Super Brain*\n"
            f"• ផលិតដោយ៖ *សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA*\n"
            f"• Telegram: *CFA Flash Feed | @CFAflashBot*\n"
            f"• ADMIN: *@Sokpheatonsai*"
        )

        # Broadcast via Telegram
        await telegram_broadcaster.broadcast_text_message(digest_body)
        
        # Publish via Facebook Page
        try:
            from facebook_publisher import fb_publisher
            fb_publisher.publish_news_to_facebook(
                headline="របាយការណ៍សង្ខេបព័ត៌មានជាតិ និងអន្តរជាតិប្រចាំម៉ោង 24/7",
                body=digest_body,
                banner_path="",
                source_name="CFA Flash Feed AI Super Brain"
            )
        except Exception as e:
            logger.warning(f"Facebook publish failed for hourly digest: {e}")

        self.record_publication()
        logger.info("✅ [HOURLY DIGEST] Successfully dispatched 24/7 Hourly Executive Digest!")
        return True

# Global Instance
hourly_digest_engine = HourlyDigestEngine()
