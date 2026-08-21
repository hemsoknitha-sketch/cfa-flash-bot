import time
import uuid
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
import feedparser

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

    def fetch_from_rss(self) -> List[RawNewsItem]:
        """Fetch latest raw news items from configured National & Global feeds."""
        from security_sentinel import security_sentinel
        news_items = []
        for feed_info in self.national_feeds:
            url = feed_info["url"]
            source_name = feed_info["name"]
            tier = feed_info.get("tier", 1)
            try:
                logger.info(f"Scanning Institutional Feed [{source_name}]: {url}")
                feed = feedparser.parse(url, request_headers={"User-Agent": "CFA-Flash-Bot/4.2"})
                for entry in feed.entries[:5]:  # Take latest 5 items per feed
                    raw_title = entry.get("title", "No Title")
                    raw_content = entry.get("summary", entry.get("title", ""))
                    
                    # Layer 2 Input Sanitization (XSS & SQL Injection protection)
                    clean_title = security_sentinel.sanitize_input_payload(raw_title)
                    clean_content = security_sentinel.sanitize_input_payload(raw_content)

                    news_items.append(RawNewsItem(
                        title=clean_title,
                        content=clean_content,
                        source=source_name,
                        url=entry.get("link", ""),
                        source_tier=tier,
                        is_unverified=False
                    ))
            except Exception as e:
                logger.error(f"Error fetching RSS [{source_name}] {url}: {e}")
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
