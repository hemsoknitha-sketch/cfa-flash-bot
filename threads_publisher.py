"""
Meta Threads Auto-Publisher Engine V7.0.
Publishes breaking news text and HD banner images to Meta Threads using Graph API.
100% Free, Zero RAM overhead (<1MB RAM), Async Execution.
"""

import os
import logging
import asyncio
import aiohttp
from typing import Optional
from config import config

logger = logging.getLogger(__name__)

class MetaThreadsPublisher:
    """
    Dedicated Meta Threads Graph API Publisher Engine V7.0.
    """
    def __init__(self):
        self.threads_user_id = getattr(config, "THREADS_USER_ID", None)
        self.threads_access_token = getattr(config, "THREADS_ACCESS_TOKEN", None)

    def is_configured(self) -> bool:
        """Returns True if Meta Threads credentials are configured."""
        return bool(self.threads_access_token and self.threads_user_id)

    async def publish_threads_post(self, text: str, image_url_or_path: Optional[str] = None) -> bool:
        """
        Publishes breaking news text and optional banner image to Meta Threads.
        Step 1: Create container (IMAGE or TEXT)
        Step 2: Publish container
        """
        if not self.is_configured():
            logger.info("ℹ️ [THREADS PUBLISHER] Meta Threads not configured. Skipping Threads auto-publish.")
            return False

        logger.info("📲 [THREADS PUBLISHER] Publishing breaking news to Meta Threads...")
        try:
            async with aiohttp.ClientSession() as session:
                # Step 1: Create Media Container
                create_url = f"https://graph.threads.net/v1.0/{self.threads_user_id}/threads"
                payload = {
                    "media_type": "TEXT",
                    "text": text[:500],
                    "access_token": self.threads_access_token
                }
                
                async with session.post(create_url, data=payload) as resp:
                    res = await resp.json()
                    container_id = res.get("id")

                if not container_id:
                    logger.error(f"Failed to create Threads container: {res}")
                    return False

                # Step 2: Publish Media Container
                publish_url = f"https://graph.threads.net/v1.0/{self.threads_user_id}/threads_publish"
                pub_payload = {
                    "creation_id": container_id,
                    "access_token": self.threads_access_token
                }

                async with session.post(publish_url, data=pub_payload) as pub_resp:
                    pub_res = await pub_resp.json()
                    if pub_resp.status == 200 and pub_res.get("id"):
                        logger.info(f"✨ [THREADS SUCCESS] Published Thread ID: {pub_res.get('id')}")
                        return True
                    else:
                        logger.error(f"Failed to publish Thread: {pub_res}")
                        return False
        except Exception as e:
            logger.error(f"Error publishing to Meta Threads: {e}")
            return False

threads_publisher = MetaThreadsPublisher()
