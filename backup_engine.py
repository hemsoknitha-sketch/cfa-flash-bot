import os
import time
import zipfile
import asyncio
import logging
from datetime import datetime, timezone, timedelta
from config import config

logger = logging.getLogger("BackupEngine")

def create_project_zip_backup() -> str:
    """Creates a timestamped ZIP archive of the project codebase and config vault."""
    phnom_penh_tz = timezone(timedelta(hours=7))
    now = datetime.now(phnom_penh_tz)
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    zip_filename = f"cfa_backup_{timestamp}.zip"
    zip_filepath = os.path.abspath(zip_filename)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    logger.info(f"📦 [BACKUP ENGINE] Creating daily ZIP backup archive: {zip_filename}...")

    included_exts = {".py", ".env", ".json", ".md", ".txt", ".yml", ".yaml", ".sql"}
    excluded_dirs = {"venv", "__pycache__", ".git", ".pytest_cache", "scratch"}

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in included_exts or file == ".env":
                    abs_file = os.path.join(root, file)
                    rel_file = os.path.relpath(abs_file, base_dir)
                    zipf.write(abs_file, rel_file)

    logger.info(f"✨ [BACKUP READY] Archive created successfully ({os.path.getsize(zip_filepath) / 1024:.1f} KB).")
    return zip_filepath

async def send_backup_to_admin(zip_filepath: str) -> bool:
    """Sends ZIP backup document to Telegram Admin and immediately cleans it up."""
    admin_id = config.TELEGRAM_ADMIN_CHAT_ID
    bot_token = config.TELEGRAM_BOT_TOKEN
    if not admin_id or admin_id in ("your_admin_chat_id", "123456789") or bot_token == "MOCK_TELEGRAM_BOT_TOKEN":
        logger.warning("Telegram Admin ID or Bot Token not configured for daily backup delivery.")
        return False

    phnom_penh_tz = timezone(timedelta(hours=7))
    now_str = datetime.now(phnom_penh_tz).strftime("%Y-%m-%d %I:%M:%S %p (UTC+7)")

    caption = (
        f"📦 *CFA FLASH NEWS - DAILY SYSTEM BACKUP*\n\n"
        f"📅 *កាលបរិច្ឆេទ:* `{now_str}`\n"
        f"🔒 *សុវត្ថិភាព:* Codebase + .env Vault + DB Config Complete\n"
        f"🧹 *Server Status:* Temp Files Cleared & 100% Secure!\n"
        f"⚡ *មាស៊ីន Cloud:* Active 24/7 365 ($0.00)"
    )

    try:
        import aiohttp
        url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("chat_id", str(admin_id))
            data.add_field("caption", caption)
            data.add_field("parse_mode", "Markdown")
            data.add_field("document", open(zip_filepath, "rb"), filename=os.path.basename(zip_filepath))

            async with session.post(url, data=data) as resp:
                res_json = await resp.json()
                if resp.status == 200 and res_json.get("ok"):
                    logger.info(f"🚀 [BACKUP SENT] Daily ZIP backup delivered to Telegram Admin Chat ID: {admin_id}")
                    return True
                else:
                    logger.error(f"Failed to send backup to Telegram Admin: {res_json}")
                    return False
    except Exception as e:
        logger.error(f"Error sending ZIP backup to Telegram: {e}")
        return False
    finally:
        # 🧹 Immediately delete ZIP file from server after sending to maintain 100% clean disk
        if os.path.exists(zip_filepath):
            try:
                os.remove(zip_filepath)
                logger.info(f"🧹 [AUTO-CLEANUP] Deleted temporary ZIP backup file: '{zip_filepath}'")
            except Exception as e:
                logger.error(f"Failed to delete temp backup ZIP {zip_filepath}: {e}")

async def run_daily_2am_backup_loop():
    """Runs a background loop that triggers a ZIP backup every day at 2:00 AM Phnom Penh time (UTC+7)."""
    phnom_penh_tz = timezone(timedelta(hours=7))
    logger.info("⏰ [DAILY BACKUP SCHEDULER ACTIVE] Scheduled for 2:00 AM Phnom Penh Time (UTC+7) every day.")

    while True:
        try:
            now = datetime.now(phnom_penh_tz)
            # Calculate next 2:00 AM Phnom Penh Time
            target = now.replace(hour=2, minute=0, second=0, microsecond=0)
            if now >= target:
                target += timedelta(days=1)

            seconds_until_target = (target - now).total_seconds()
            logger.info(f"⏳ Next scheduled ZIP backup in {seconds_until_target / 3600:.2f} hours (at {target.strftime('%Y-%m-%d %H:%M:%S UTC+7')}).")

            await asyncio.sleep(seconds_until_target)

            # Trigger daily backup
            zip_path = create_project_zip_backup()
            await send_backup_to_admin(zip_path)

        except Exception as e:
            logger.error(f"Error in daily backup loop: {e}")
            await asyncio.sleep(300)  # Retry in 5 minutes on error
