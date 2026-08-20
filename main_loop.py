import asyncio
import logging
from main import process_batch_news, pipeline_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("24/7_Daemon")

async def run_247_daemon(interval_seconds: int = 60):
    """
    Super Brain AI 24/7 365 Continuous News Ingestion & Broadcasting Loop.
    Scans live RSS feeds every 60 seconds indefinitely.
    """
    logger.info("🚀 [SUPER BRAIN 24/7 DAEMON STARTED] Real-Time Market Feed Active!")
    logger.info(f"🔄 Polling interval: Every {interval_seconds} seconds...\n")
    
    while True:
        try:
            await process_batch_news()
        except Exception as e:
            logger.error(f"❌ Error in 24/7 news processing cycle: {e}")
            
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    try:
        asyncio.run(run_247_daemon(interval_seconds=60))
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n🛑 [STOPPED] 24/7 News Daemon stopped by user.")
