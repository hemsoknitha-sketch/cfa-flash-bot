"""
Enterprise Multi-Key Gemini API Pool Engine.
Features:
1. Multi-Key Round-Robin & Failover Pool (Supports up to 84+ Free Gemini API Keys).
2. Auto-Rotation on HTTP 429 / RESOURCE_EXHAUSTED.
3. 24-Hour Quota Reset Tracker.
4. Seamless Integration with google-genai Client.
"""

import time
import logging
from typing import List, Optional
from config import config

logger = logging.getLogger(__name__)

class GeminiKeyPoolEngine:
    """
    Round-Robin & Dynamic Failover Pool for Gemini API Keys.
    """
    def __init__(self):
        self.raw_keys = config.get_gemini_api_keys()
        self.active_keys: List[str] = [k for k in self.raw_keys if k and k != "your_gemini_api_key_here"]
        self.exhausted_keys: dict = {}  # {key: timestamp_exhausted}
        self.current_index: int = 0
        
        logger.info(f"🔑 [GEMINI KEY POOL INITIALIZED] Active Key Pool Size: {len(self.active_keys)} Keys.")

    def get_client(self) -> Optional[tuple]:
        """
        Returns (google.genai.Client instance, active_key_string).
        Automatically skips exhausted keys and rotates to next available key.
        """
        if not self.active_keys:
            return None

        now = time.time()
        # Clean up keys exhausted more than 1 hour ago
        for k in list(self.exhausted_keys.keys()):
            if now - self.exhausted_keys[k] > 3600:
                del self.exhausted_keys[k]

        available = [k for k in self.active_keys if k not in self.exhausted_keys]
        if not available:
            logger.warning("⚠️ [GEMINI KEY POOL] All keys temporarily exhausted. Resetting key pool state.")
            self.exhausted_keys.clear()
            available = self.active_keys

        key = available[self.current_index % len(available)]
        self.current_index = (self.current_index + 1) % len(available)

        try:
            from google import genai
            client = genai.Client(api_key=key)
            return client, key
        except Exception as e:
            logger.error(f"Failed to create genai.Client with key [{key[:6]}...]: {e}")
            return None

    def mark_key_exhausted(self, key: str):
        """Marks a key as exhausted (429 Rate Limited) for 1 hour."""
        self.exhausted_keys[key] = time.time()
        logger.warning(f"🚨 [GEMINI KEY POOL] Key [{key[:6]}...] marked EXHAUSTED (429 Rate Limit). Active remaining: {len(self.active_keys) - len(self.exhausted_keys)}")

gemini_key_pool = GeminiKeyPoolEngine()
