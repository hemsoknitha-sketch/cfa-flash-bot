import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import logging

from telegram_broadcaster import TelegramBroadcaster
from facebook_publisher import FacebookPublisher
from config import config

async def test_channels():
    print("--- 1. Testing Telegram Config ---", flush=True)
    print(f"Bot Token: {config.TELEGRAM_BOT_TOKEN[:10]}...")
    print(f"VIP Channel ID: {config.TELEGRAM_VIP_CHANNEL_ID}")
    print(f"Admin Chat ID: {config.TELEGRAM_ADMIN_CHAT_ID}")
    
    broadcaster = TelegramBroadcaster()
    # Test sending ping message to Telegram Admin/Channel
    res_tg = await broadcaster.broadcast_to_vip_channel(
        message_text="🧪 [TEST SYSTEM DIAGNOSTIC] Testing Telegram Bot Connectivity...",
        target_chat_id=config.TELEGRAM_ADMIN_CHAT_ID
    )
    print(f"Telegram Direct Broadcast Result: {res_tg}", flush=True)

    print("\n--- 2. Testing Facebook Graph API ---", flush=True)
    print(f"FB Page ID: {config.FB_PAGE_ID}")
    print(f"FB Token length: {len(config.FB_PAGE_ACCESS_TOKEN)}")
    
    fb = FacebookPublisher()
    # Test executing FB publish directly
    try:
        import aiohttp
        url = f"{fb.graph_url}/feed"
        payload = {
            "message": "🧪 [TEST SYSTEM DIAGNOSTIC] System test connection to Facebook Page.",
            "access_token": fb.access_token
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_json = await resp.json()
                print(f"FB API HTTP Status: {resp.status}", flush=True)
                print(f"FB API Response: {res_json}", flush=True)
    except Exception as e:
        print(f"FB API Error: {e}", flush=True)

if __name__ == "__main__":
    asyncio.run(test_channels())
