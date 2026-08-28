import sys
import os
import asyncio
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TestPipeline")

from main import pipeline_engine, process_news
from scraper import IngestionEngine

async def run_test():
    logger.info("--- TESTING FULL LIVE PIPELINE ---")
    ingestion = IngestionEngine()
    items = await ingestion.fetch_from_rss_async()
    logger.info(f"Total RSS Items Fetched: {len(items)}")
    
    for item in items[:5]:
        full_text = f"{item.title} - {item.content}"
        await process_news(news_text=full_text, news_id=item.id, source_name=item.source, url=item.url, timestamp=item.timestamp)

if __name__ == "__main__":
    asyncio.run(run_test())
