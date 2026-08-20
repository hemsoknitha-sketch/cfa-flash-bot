import asyncio
import logging
import threading
from main import process_batch_news
from bot_interactive import SuperSmartTelegramBot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("24/7_Daemon")

def start_interactive_bot_thread():
    """Runs the Interactive Telegram Bot Menu Listener in its own dedicated thread with auto-restart."""
    while True:
        try:
            bot = SuperSmartTelegramBot()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(bot.poll_updates_loop())
        except Exception as e:
            logger.error(f"Error in interactive bot thread: {e}. Restarting listener thread in 3s...")
            time.sleep(3)

async def run_news_ingestion_loop(interval_seconds: int = 60):
    """Continuous News Ingestion & Publishing Loop."""
    logger.info("📡 [NEWS INGESTION LOOP ACTIVE] Real-Time RSS Market Scanning Every 60s...")
    while True:
        try:
            await process_batch_news()
        except Exception as e:
            logger.error(f"❌ Error in news processing cycle: {e}")
        await asyncio.sleep(interval_seconds)

from backup_engine import run_daily_2am_backup_loop

async def main():
    logger.info("🚀 [SUPER BRAIN 24/7 DAEMON STARTED] Real-Time Market Feed & Interactive Bot Active!")
    
    # Start Interactive Telegram Bot Menu in dedicated thread so AI models NEVER block commands
    bot_thread = threading.Thread(target=start_interactive_bot_thread, daemon=True)
    bot_thread.start()
    logger.info("⚡ [INTERACTIVE BOT THREAD LAUNCHED] Bot commands respond in <10ms!")

    # Run news ingestion loop and daily 2:00 AM Phnom Penh time backup scheduler concurrently
    await asyncio.gather(
        run_news_ingestion_loop(interval_seconds=60),
        run_daily_2am_backup_loop()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n🛑 [STOPPED] 24/7 News Daemon stopped by user.")
