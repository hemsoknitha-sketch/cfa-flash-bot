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
        self.rss_urls = rss_urls or [
            "https://www.khmertimeskh.com/feed/",
            "https://www.phnompenhpost.com/rss.xml",
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
        ]

    def fetch_from_rss(self) -> List[RawNewsItem]:
        """Fetch latest raw news items from configured RSS feeds."""
        news_items = []
        for url in self.rss_urls:
            try:
                logger.info(f"Scanning RSS Feed: {url}")
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # Take latest 5 items per feed
                    news_items.append(RawNewsItem(
                        title=entry.get("title", "No Title"),
                        content=entry.get("summary", entry.get("title", "")),
                        source=feed.feed.get("title", "RSS Source"),
                        url=entry.get("link", ""),
                        source_tier=1,
                        is_unverified=False
                    ))
            except Exception as e:
                logger.error(f"Error fetching RSS {url}: {e}")
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
