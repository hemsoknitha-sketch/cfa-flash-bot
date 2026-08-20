import asyncio
import logging
from main import process_batch_news
from bot_interactive import SuperSmartTelegramBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("24/7_Daemon")

async def run_news_ingestion_loop(interval_seconds: int = 60):
    """Continuous News Ingestion & Publishing Loop."""
    logger.info("📡 [NEWS INGESTION LOOP ACTIVE] Real-Time RSS Market Scanning Every 60s...")
    while True:
        try:
            await process_batch_news()
        except Exception as e:
            logger.error(f"❌ Error in news processing cycle: {e}")
        await asyncio.sleep(interval_seconds)

async def main():
    logger.info("🚀 [SUPER BRAIN 24/7 DAEMON STARTED] Real-Time Market Feed & Interactive Bot Active!")
    interactive_bot = SuperSmartTelegramBot()
    
    # Run both 24/7 News Ingestion AND Interactive Telegram Commands Listener concurrently
    await asyncio.gather(
        run_news_ingestion_loop(interval_seconds=60),
        interactive_bot.poll_updates_loop()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n🛑 [STOPPED] 24/7 News Daemon stopped by user.")
