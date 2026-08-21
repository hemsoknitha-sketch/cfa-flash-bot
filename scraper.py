import time
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import feedparser
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RawNewsItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    source: str
    url: Optional[str] = None
    timestamp: float = Field(default_factory=time.time)
    source_tier: int = 1  # 1: Tier 1 (Reuters/Bloomberg), 2: Reputable media, 3: Social/Unverified
    is_unverified: bool = False

class IngestionEngine:
    def __init__(self, rss_urls: Optional[List[str]] = None):
        from national_ingestion_registry import get_all_national_feeds
        self.national_feeds = get_all_national_feeds()
        self.rss_urls = rss_urls or [f["url"] for f in self.national_feeds]

    def _fetch_single_feed(self, feed_info: dict) -> List[RawNewsItem]:
        from security_sentinel import security_sentinel
        url = feed_info["url"]
        source_name = feed_info["name"]
        tier = feed_info.get("tier", 1)
        items = []
        try:
            logger.info(f"⚡ Scanning Feed [{source_name}]: {url}")
            feed = feedparser.parse(url, request_headers={"User-Agent": "CFA-Flash-Bot/4.2"})
            for entry in feed.entries[:5]:
                raw_title = entry.get("title", "No Title")
                raw_content = entry.get("summary", entry.get("title", ""))
                clean_title = security_sentinel.sanitize_input_payload(raw_title)
                clean_content = security_sentinel.sanitize_input_payload(raw_content)
                items.append(RawNewsItem(
                    title=clean_title,
                    content=clean_content,
                    source=source_name,
                    url=entry.get("link", ""),
                    source_tier=tier,
                    is_unverified=False
                ))
        except Exception as e:
            logger.error(f"Error fetching RSS [{source_name}] {url}: {e}")
        return items

    async def fetch_from_facebook_pages_async(self) -> List[RawNewsItem]:
        """
        Meta Graph API Facebook Page Ingestion Engine.
        Scans official configured Facebook Pages via Meta Graph API v19.0.
        """
        import aiohttp
        from security_sentinel import security_sentinel
        page_id = config.FB_PAGE_ID
        token = config.FB_PAGE_ACCESS_TOKEN
        items = []

        if not token or token == "MOCK_FB_PAGE_ACCESS_TOKEN" or page_id == "MOCK_FB_PAGE_ID":
            return items

        url = f"https://graph.facebook.com/v19.0/{page_id}/posts?fields=id,message,created_time,permalink_url,full_picture&limit=5&access_token={token}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5.0)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        for post in data.get("data", []):
                            msg = post.get("message", "").strip()
                            if not msg:
                                continue
                            clean_msg = security_sentinel.sanitize_input_payload(msg)
                            first_line = clean_msg.split("\n")[0].strip()
                            title = first_line[:100] if len(first_line) > 10 else clean_msg[:80]
                            items.append(RawNewsItem(
                                title=title,
                                content=clean_msg,
                                source="Facebook Page ផ្លូវការ",
                                url=post.get("permalink_url", f"https://facebook.com/{post.get('id')}"),
                                source_tier=1,
                                is_unverified=False
                            ))
                        logger.info(f"📘 [FB PAGE INGESTION] Ingested {len(items)} live posts from Facebook Page ID: {page_id}")
                    else:
                        err_json = await resp.json()
                        logger.warning(f"FB Page Graph API Notice: {err_json.get('error', {}).get('message')}")
        except Exception as e:
            logger.error(f"FB Page Ingestion Error: {e}")
        return items

    async def fetch_from_rss_async(self) -> List[RawNewsItem]:
        """Fetch all national feeds & Facebook Pages concurrently in parallel (<3s total)."""
        import asyncio
        start_t = time.time()
        tasks = []
        for feed_info in self.national_feeds:
            # Wrap each feed fetch in asyncio.to_thread with 5.0s timeout
            task = asyncio.wait_for(asyncio.to_thread(self._fetch_single_feed, feed_info), timeout=5.0)
            tasks.append(task)
        
        fb_task = asyncio.create_task(self.fetch_from_facebook_pages_async())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        fb_items = await fb_task

        news_items = []
        for res in results:
            if isinstance(res, list):
                news_items.extend(res)
            elif isinstance(res, Exception):
                pass
        
        if fb_items:
            news_items.extend(fb_items)
        
        elapsed = time.time() - start_t
        logger.info(f"⚡ [PARALLEL ASYNC INGESTION] Scanned {len(self.national_feeds)} Feeds + FB Pages in {elapsed:.2f}s! Retrieved {len(news_items)} items.")
        return news_items

    def fetch_from_rss(self) -> List[RawNewsItem]:
        """Synchronous wrapper for backwards compatibility."""
        import asyncio
        try:
            return asyncio.run(self.fetch_from_rss_async())
        except Exception:
            news_items = []
            for feed_info in self.national_feeds:
                news_items.extend(self._fetch_single_feed(feed_info))
            return news_items

    def generate_mock_breaking_news(self) -> List[RawNewsItem]:
        """Generate Cambodia-specific breaking news items."""
        return [
            RawNewsItem(
                title="Cambodia Strengthens International Joint Operations to Crackdown Online Scams and Enforce Rule of Law",
                content="Cambodian law enforcement agencies in partnership with international police forces launch a major operation suppressing online scam networks, safeguarding human rights, social justice, and national security.",
                source="Phnom Penh National News Terminal",
                source_tier=1,
                is_unverified=False
            ),
            RawNewsItem(
                title="Cambodia Foreign Ministry Reaffirms Multi-Party Democracy and International Law Principles",
                content="The Ministry of Foreign Affairs of Cambodia issues an official diplomatic statement affirming commitment to liberal multi-party democracy, rule of law, and peaceful international cooperation.",
                source="Cambodian Foreign Desk",
                source_tier=1,
                is_unverified=False
            )
        ]
