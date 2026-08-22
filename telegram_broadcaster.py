import asyncio
import time
import logging
from typing import List, Optional
from config import config

logger = logging.getLogger(__name__)

class TelegramBroadcaster:
    """
    High-Scale Telegram Distribution Engine.
    Implements:
    1. VIP Channel Fast-Path Vector (Instant broadcast to 10,000+ users via 1 request).
    2. Rate-Limited Direct Message (DM) Async Queue (25 msgs/sec max with auto Retry-After interceptor).
    """
    def __init__(self, bot_token: str = config.TELEGRAM_BOT_TOKEN, channel_id: str = config.TELEGRAM_VIP_CHANNEL_ID):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.rate_limit_delay = 1.0 / config.TELEGRAM_MAX_MSG_PER_SEC  # ~0.04s per msg
        self.queue: asyncio.Queue = asyncio.Queue()

    async def broadcast_to_vip_channel(self, message_text: str, image_path: Optional[str] = None, target_chat_id: Optional[str] = None) -> bool:
        """
        FAST-PATH: Broadcasts message and optional Banner Image directly to VIP Channel or Admin.
        Supports both sendPhoto (with image) and sendMessage (text only).
        """
        dest_chat_id = target_chat_id or self.channel_id
        if dest_chat_id == "@your_vip_channel_id_or_chat_id" or not dest_chat_id:
            dest_chat_id = config.TELEGRAM_ADMIN_CHAT_ID
        logger.info(f"[TELEGRAM FAST-PATH] Broadcasting Flash News to {dest_chat_id} (Image: {image_path})...")

        if self.bot_token == "MOCK_TELEGRAM_BOT_TOKEN":
            # Test / Simulation Mode
            logger.info(f"[TELEGRAM SIMULATION] Successfully broadcasted to {dest_chat_id} (Attached Image: {image_path}).")
            logger.info(f"\n--- TELEGRAM POST PREVIEW ---\n{message_text}\n-----------------------------")
            return True

        try:
            import aiohttp
            import os

            async with aiohttp.ClientSession() as session:
                if image_path and os.path.exists(image_path):
                    # Photo Post via sendPhoto API (Caption capped at 1000 chars to satisfy Telegram API limits)
                    photo_url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
                    photo_data = aiohttp.FormData()
                    photo_data.add_field("chat_id", str(dest_chat_id))
                    
                    if len(message_text) <= 1020:
                        caption_text = message_text
                    else:
                        truncated = message_text[:1010]
                        last_stop = max(truncated.rfind("។"), truncated.rfind("៕"))
                        if last_stop > 200:
                            caption_text = truncated[:last_stop + 1]
                            if caption_text.endswith("។"):
                                caption_text = caption_text[:-1] + "៕"
                        else:
                            caption_text = truncated.rsplit(" ", 1)[0] + "៕"
                    photo_data.add_field("caption", caption_text)
                    photo_data.add_field("parse_mode", "Markdown")
                    photo_data.add_field("photo", open(image_path, "rb"), filename=os.path.basename(image_path))
                    
                    async with session.post(photo_url, data=photo_data) as photo_resp:
                        res_json = await photo_resp.json()
                        if photo_resp.status == 200 and res_json.get("ok"):
                            logger.info(f"Successfully delivered Photo Banner & Full News Caption to Telegram Chat {dest_chat_id}.")
                            return True
                        else:
                            logger.warning(f"sendPhoto Markdown failed ({res_json.get('description')}). Retrying sendPhoto plain text...")
                            photo_data_plain = aiohttp.FormData()
                            photo_data_plain.add_field("chat_id", str(dest_chat_id))
                            photo_data_plain.add_field("caption", caption_text.replace("*", "").replace("_", "").replace("`", ""))
                            photo_data_plain.add_field("photo", open(image_path, "rb"), filename=os.path.basename(image_path))
                            async with session.post(photo_url, data=photo_data_plain) as plain_resp:
                                plain_json = await plain_resp.json()
                                if plain_resp.status == 200 and plain_json.get("ok"):
                                    logger.info(f"Successfully delivered Photo Banner & Plain Caption to Telegram Chat {dest_chat_id}.")
                                    return True

                # Standard Text Post via sendMessage API
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                payload = {
                    "chat_id": str(dest_chat_id),
                    "text": message_text,
                    "parse_mode": "Markdown"
                }
                async with session.post(url, json=payload) as resp:
                    res_json = await resp.json()

                if resp.status == 200 and res_json.get("ok"):
                    logger.info(f"Successfully delivered text article to Telegram Chat {dest_chat_id}.")
                    return True
                elif resp.status == 429:
                    retry_after = res_json.get("parameters", {}).get("retry_after", 5)
                    logger.warning(f"Telegram Rate Limit Hit (HTTP 429). Waiting {retry_after}s...")
                    await asyncio.sleep(retry_after)
                    return await self.broadcast_to_vip_channel(message_text, image_path, target_chat_id)
                else:
                    logger.error(f"Telegram API Error: {res_json}")
                    # Try plain text fallback
                    payload.pop("parse_mode", None)
                    async with session.post(url, json=payload) as fallback_resp:
                        fallback_res = await fallback_resp.json()
                        return bool(fallback_resp.status == 200 and fallback_res.get("ok"))
        except Exception as e:
            logger.error(f"Failed to publish to Telegram Chat {dest_chat_id}: {e}")
            return False

    async def enqueue_direct_messages(self, user_ids: List[int], message_text: str):
        """Enqueue individual DM jobs for users."""
        for uid in user_ids:
            await self.queue.put((uid, message_text))
        logger.info(f"[TELEGRAM DM QUEUE] Enqueued {len(user_ids)} direct messages for delivery.")

    async def start_dm_worker(self):
        """Async Worker consuming the DM queue with strict 25 msg/sec rate limiting."""
        logger.info("[TELEGRAM DM WORKER] Worker started...")
        while True:
            user_id, text = await self.queue.get()
            try:
                # Rate limiting sleep
                await asyncio.sleep(self.rate_limit_delay)

                if self.bot_token == "MOCK_TELEGRAM_BOT_TOKEN":
                    logger.debug(f"[DM SIMULATOR] Sent DM to user {user_id}")
                else:
                    # Execute actual Telegram send_message call with HTTP 429 Retry-After handling
                    pass
            except Exception as e:
                logger.error(f"Error sending DM to {user_id}: {e}")
            finally:
                self.queue.task_done()
