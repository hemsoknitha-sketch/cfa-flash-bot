import aiohttp
import asyncio
import logging
from typing import Optional
from config import config

logger = logging.getLogger(__name__)

class FacebookPublisher:
    """
    Facebook Graph API Publisher.
    Features:
    1. Automatic posting to Facebook Page Feed / Photos API with In-Memory Photo Buffer.
    2. Strict 30-min Meta Pacing Governor for 100% Meta Code 368 Anti-Spam Compliance.
    3. Zero Telegram Duplicate Messages (Silent Logging on FB Errors).
    """
    def __init__(self, page_id: str = config.FB_PAGE_ID, access_token: str = config.FB_PAGE_ACCESS_TOKEN):
        self.page_id = page_id
        self.access_token = access_token
        self.graph_url = f"https://graph.facebook.com/v19.0/{self.page_id}"
        self.last_post_time = 0   # Rate Governor timestamp (Min 30 mins = 1800s between posts)
        self.min_post_interval = 1800  # 30 mins safety interval for 100% Meta Policy Compliance

    async def publish_news(self, caption: str, image_path: Optional[str] = None) -> bool:
        """
        Non-blocking Facebook Page Publisher.
        Reads image bytes upfront before main.py deletes the file, then paces post via 30-min Governor.
        """
        import os
        image_bytes = None
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            except Exception as e:
                logger.warning(f"Could not read image file bytes for Facebook: {e}")

        asyncio.create_task(self._publish_with_pacing(caption, image_bytes))
        return True

    async def _publish_with_pacing(self, caption: str, image_bytes: Optional[bytes] = None):
        import time
        logger.info(f"[FACEBOOK PUBLISHER] Preparing to publish Flash News to Page ID: {self.page_id}...")

        if self.access_token in ("MOCK_FB_PAGE_ACCESS_TOKEN", "your_long_lived_facebook_page_access_token", ""):
            logger.info("[FACEBOOK SIMULATION] Post successfully published to Facebook Page!")
            if image_bytes:
                logger.info(f"[FACEBOOK SIMULATION] Attached Banner Image ({len(image_bytes)} bytes)")
            logger.info(f"\n--- FACEBOOK POST PREVIEW ---\n{caption}\n-----------------------------")
            return

        now = time.time()
        time_since_last = now - self.last_post_time
        if self.last_post_time > 0 and time_since_last < self.min_post_interval:
            wait_needed = int(self.min_post_interval - time_since_last)
            logger.info(f"🛡️ [FACEBOOK RATE GOVERNOR] Pacing Facebook post ({wait_needed}s remaining in 30-min safety window) for 100% Meta Policy Compliance.")
            await asyncio.sleep(wait_needed)

        try:
            async with aiohttp.ClientSession() as session:
                if image_bytes:
                    url = f"{self.graph_url}/photos"
                    data = aiohttp.FormData()
                    data.add_field('caption', caption)
                    data.add_field('access_token', self.access_token)
                    data.add_field('source', image_bytes, filename='banner.jpg', content_type='image/jpeg')
                    async with session.post(url, data=data) as resp:
                        res_json = await resp.json()
                else:
                    url = f"{self.graph_url}/feed"
                    payload = {
                        "message": caption,
                        "access_token": self.access_token
                    }
                    async with session.post(url, json=payload) as resp:
                        res_json = await resp.json()

                if resp.status == 200 and "id" in res_json:
                    self.last_post_time = time.time()
                    logger.info(f"✨ [FACEBOOK SUCCESS] Post published to Facebook Page! Post ID: {res_json.get('id')}")
                else:
                    error_obj = res_json.get("error", {})
                    error_msg = f"Graph API Error (HTTP {resp.status}): {error_obj.get('message', res_json)}"
                    logger.error(f"⚠️ [FACEBOOK PUBLISH NOTICE] {error_msg}")
                    # Update governor timestamp on rate limit so we don't spam Meta
                    self.last_post_time = time.time()
        except Exception as e:
            logger.error(f"⚠️ [FACEBOOK EXCEPTION] {e}")
