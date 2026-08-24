import os
import sys
import time
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

_global_lock_fp = None

def acquire_single_instance_lock():
    """Enforces strict single-instance execution across both Linux (fcntl) and Windows (msvcrt)."""
    global _global_lock_fp
    if _global_lock_fp is not None:
        return _global_lock_fp

    if os.name == 'nt':
        try:
            import msvcrt
            lock_file_path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "cfa_flash_bot_daemon.lock")
            fp = open(lock_file_path, "a+")
            fp.seek(0)
            msvcrt.locking(fp.fileno(), msvcrt.LK_NBLCK, 1)
            fp.truncate(0)
            fp.write(str(os.getpid()))
            fp.flush()
            _global_lock_fp = fp
            logger.info(f"🔒 [SINGLE INSTANCE LOCK ACQUIRED - WINDOWS] PID: {os.getpid()}")
            return _global_lock_fp
        except (IOError, OSError):
            logger.error("🚨 [SINGLE INSTANCE LOCK ERROR] Another instance of CFA Flash Feed is already running on this machine! Terminating duplicate instance to prevent double-posting.")
            sys.exit(0)
    else:
        try:
            import fcntl
            lock_file_path = "/tmp/cfa_flash_bot_daemon.lock"
            fp = open(lock_file_path, "a+")
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            fp.seek(0)
            fp.truncate(0)
            fp.write(str(os.getpid()))
            fp.flush()
            _global_lock_fp = fp
            logger.info(f"🔒 [SINGLE INSTANCE LOCK ACQUIRED - LINUX] PID: {os.getpid()}")
            return _global_lock_fp
        except (ImportError, IOError, OSError) as lock_err:
            logger.error(f"🚨 [SINGLE INSTANCE LOCK ERROR] Another instance of CFA Flash Feed is already running on this server! ({lock_err}). Terminating duplicate instance to prevent double-posting.")
            sys.exit(0)

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
    """Continuous News Ingestion & Publishing Loop with Active Memory Management."""
    import gc
    logger.info("📡 [NEWS INGESTION LOOP ACTIVE] Real-Time RSS Market Scanning Every 60s...")
    while True:
        try:
            await process_batch_news()
            gc.collect()  # Release unused objects back to OS memory
        except Exception as e:
            logger.error(f"❌ Error in news processing cycle: {e}")
        await asyncio.sleep(interval_seconds)

from backup_engine import run_daily_2am_backup_loop

async def main():
    acquire_single_instance_lock()
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
