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
    1. Automatic posting to Facebook Page Feed / Photos API.
    2. Automatic Failover Emergency Sentinel: Sends alert to Telegram Admin if Graph API fails.
    """
    def __init__(self, page_id: str = config.FB_PAGE_ID, access_token: str = config.FB_PAGE_ACCESS_TOKEN):
        self.page_id = page_id
        self.access_token = access_token
        self.graph_url = f"https://graph.facebook.com/v19.0/{self.page_id}"

    async def publish_news(self, caption: str, image_path: Optional[str] = None) -> bool:
        """
        Publish post to Facebook Page.
        Supports text post or image post.
        """
        logger.info(f"[FACEBOOK PUBLISHER] Preparing to publish Flash News to Page ID: {self.page_id}...")

        if self.access_token in ("MOCK_FB_PAGE_ACCESS_TOKEN", "your_long_lived_facebook_page_access_token", ""):
            # Test / Simulation Mode
            logger.info("[FACEBOOK SIMULATION] Post successfully published to Facebook Page!")
            if image_path:
                logger.info(f"[FACEBOOK SIMULATION] Attached Banner Image: {image_path}")
            logger.info(f"\n--- FACEBOOK POST PREVIEW ---\n{caption}\n-----------------------------")
            return True

        try:
            async with aiohttp.ClientSession() as session:
                if image_path:
                    # Photo Post API
                    url = f"{self.graph_url}/photos"
                    data = aiohttp.FormData()
                    data.add_field('caption', caption)
                    data.add_field('access_token', self.access_token)
                    data.add_field('source', open(image_path, 'rb'), filename='banner.jpg')
                    async with session.post(url, data=data) as resp:
                        res_json = await resp.json()
                else:
                    # Standard Feed Post API
                    url = f"{self.graph_url}/feed"
                    payload = {
                        "message": caption,
                        "access_token": self.access_token
                    }
                    async with session.post(url, json=payload) as resp:
                        res_json = await resp.json()

                if resp.status == 200 and "id" in res_json:
                    logger.info(f"Successfully published to Facebook Page! Post ID: {res_json.get('id')}")
                    return True
                else:
                    error_msg = f"Graph API Error (HTTP {resp.status}): {res_json.get('error', {}).get('message', res_json)}"
                    logger.error(error_msg)
                    # Trigger Emergency Telegram Admin Alert
                    await self.send_telegram_admin_alert(error_msg, caption)
                    return False

        except Exception as e:
            error_msg = f"Facebook Graph API Connection Exception: {str(e)}"
            logger.error(error_msg)
            # Trigger Emergency Telegram Admin Alert
            await self.send_telegram_admin_alert(error_msg, caption)
            return False

    async def send_telegram_admin_alert(self, error_details: str, failed_payload: str):
        """
        EMERGENCY SENTINEL: Automatically sends alarm message to Telegram Admin
        when Facebook Graph API experiences failure or token deprecation.
        """
        logger.warning(f"🚨 [EMERGENCY SENTINEL TRIGGERED] Sending Telegram Alert to Admin ({config.TELEGRAM_ADMIN_CHAT_ID})...")

        alert_message = (
            f"🚨 *[EMERGENCY SENTINEL ALERT: FACEBOOK API FAILURE]*\n\n"
            f"❌ * Error Details:*\n`{error_details}`\n\n"
            f"📌 *Failed News Post Payload:*\n{failed_payload[:300]}...\n\n"
            f"⚠️ *Action Required:* Please inspect Facebook Page Access Token or Graph API version."
        )

        if config.TELEGRAM_BOT_TOKEN == "MOCK_TELEGRAM_BOT_TOKEN":
            logger.info(f"[TELEGRAM ADMIN SENTINEL SIMULATION] Alert delivered to Admin:\n{alert_message}")
            return

        try:
            url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                "chat_id": config.TELEGRAM_ADMIN_CHAT_ID,
                "text": alert_message,
                "parse_mode": "Markdown"
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        logger.info("Emergency alert delivered to Telegram Admin successfully.")
        except Exception as e:
            logger.error(f"Failed to deliver Emergency Telegram Admin Alert: {e}")
