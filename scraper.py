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
        """Generate mock news items to simulate real-time breaking news & leaks."""
        return [
            RawNewsItem(
                title="Federal Reserve Announces Emergency 50bps Interest Rate Cut",
                content="The US Federal Reserve has held an unscheduled meeting and decided to cut interest rates by 50 basis points effective immediately, citing financial liquidity stabilization.",
                source="Reuters Terminal",
                source_tier=1,
                is_unverified=False
            ),
            # Duplicate item (same event, different phrasing) to test vector deduplication
            RawNewsItem(
                title="US Fed Cuts Interest Rates by 0.50% in Emergency Announcement",
                content="In a surprise move today, the Federal Reserve reduced benchmark interest rates by 50 basis points to support economic growth.",
                source="Bloomberg Flash",
                source_tier=1,
                is_unverified=False
            ),
            # Market-moving leak item (unverified source) to test Credibility Evaluation
            RawNewsItem(
                title="UNCONFIRMED LEAK: Major Global Tech Giant Preparing $20 Billion AI Crypto Treasury Reserve Acquisition",
                content="Leaked internal memo from anonymous source suggests a trillion-dollar tech giant is planning to allocate $20B into digital asset reserves next week.",
                source="Unverified Telegram Insider Channel",
                source_tier=3,
                is_unverified=True
            )
        ]
