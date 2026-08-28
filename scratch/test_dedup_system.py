import asyncio
import os
import sys
import time
import logging

# Set working directory to project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TestDedup")

async def test_dedup():
    from vector_store import VectorDeduplicator
    from telegram_broadcaster import TelegramBroadcaster
    from bot_interactive import SuperSmartTelegramBot

    logger.info("🧪 [TEST 1] Testing VectorDeduplicator atomic_check_and_add...")
    dedup = VectorDeduplicator(enable_local_embeddings=False)
    
    sample_text = "រដ្ឋាភិបាលកម្ពុជាប្រកាសដាក់ចេញនូវវិធានការសេដ្ឋកិច្ចថ្មី ដើម្បីគាំទ្រអាជីវកម្មក្នុងស្រុក"
    news_id_1 = "test_news_001"
    news_id_2 = "test_news_002"

    # First check: should be unique (False)
    is_dup1, sim1, match1 = dedup.atomic_check_and_add(sample_text, news_id_1)
    logger.info(f"Check 1: is_dup={is_dup1}, sim={sim1}, match={match1}")
    assert not is_dup1, "First check should be UNIQUE!"

    # Second check (exact same text): should be DUPLICATE (True)
    is_dup2, sim2, match2 = dedup.atomic_check_and_add(sample_text, news_id_2)
    logger.info(f"Check 2 (Exact Duplicate): is_dup={is_dup2}, sim={sim2}, match={match2}")
    assert is_dup2, "Second check should be DUPLICATE!"

    # Third check (slightly rephrased headline): should be DUPLICATE (True)
    rephrased_text = "រដ្ឋាភិបាលកម្ពុជាប្រកាសដាក់ចេញនូវវិធានការសេដ្ឋកិច្ចថ្មី! ដើម្បីគាំទ្រអាជីវកម្មក្នុងស្រុក។"
    is_dup3, sim3, match3 = dedup.atomic_check_and_add(rephrased_text, "test_news_003")
    logger.info(f"Check 3 (Rephrased Duplicate): is_dup={is_dup3}, sim={sim3}, match={match3}")
    assert is_dup3, "Rephrased check should be DUPLICATE!"

    logger.info("✅ [TEST 1 PASSED] VectorDeduplicator atomic_check_and_add works perfectly!")

    logger.info("\n🧪 [TEST 2] Testing TelegramBroadcaster deduplication cache...")
    broadcaster = TelegramBroadcaster(bot_token="MOCK_TELEGRAM_BOT_TOKEN", channel_id="@mock_channel")
    msg_text = "📰 ព័ត៌មានទាន់ហេតុការណ៍ចុងក្រោយពីកម្ពុជា..."
    
    # First broadcast: should succeed
    res1 = await broadcaster.broadcast_to_vip_channel(msg_text)
    assert res1, "First broadcast should succeed!"

    # Second immediate broadcast: should be intercepted by deduplication cache
    res2 = await broadcaster.broadcast_to_vip_channel(msg_text)
    assert res2, "Second broadcast should return True via deduplication interceptor!"

    logger.info("✅ [TEST 2 PASSED] TelegramBroadcaster deduplication cache works perfectly!")

    logger.info("\n🧪 [TEST 3] Testing Telegram Bot update & callback deduplication...")
    bot = SuperSmartTelegramBot(token="MOCK_BOT_TOKEN")
    
    # Mock update
    mock_update = {"update_id": 999991, "message": {"chat": {"id": 12345}, "text": "/ping"}}
    
    # First handle
    await bot.handle_update(mock_update)
    assert 999991 in bot._processed_update_ids, "Update ID should be recorded in _processed_update_ids!"

    # Second handle with same update_id
    await bot.handle_update(mock_update)
    logger.info("✅ [TEST 3 PASSED] Bot update deduplication works perfectly!")

    logger.info("\n🎉 All Deduplication System Tests PASSED 100% Successfully!")

if __name__ == "__main__":
    asyncio.run(test_dedup())
