import asyncio
import logging
import time
from scraper import IngestionEngine, RawNewsItem
from vector_store import VectorDeduplicator
from ai_rewriter import SuperBrainAIRewriter
from telegram_broadcaster import TelegramBroadcaster
from facebook_publisher import FacebookPublisher
from news_filter import zero_shot_filter
from translator import nllb_translator
from config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("MasterOrchestrator")

class FlashNewsSuperBrainPipeline:
    def __init__(self):
        self.ingestion = IngestionEngine()
        self.dedup_store = VectorDeduplicator()
        self.ai_rewriter = SuperBrainAIRewriter()
        self.broadcaster = TelegramBroadcaster()
        self.fb_publisher = FacebookPublisher()

# Global pipeline instance
pipeline_engine = FlashNewsSuperBrainPipeline()

async def process_news(news_text: str, news_id: str):
    """
    Unified 5-Step Async Production Pipeline:
    1. ត្រង Breaking News (XLM-RoBERTa Zero-Shot NLP)
    2. រក្សាទិន្នន័យវ៉ិចទ័រ (BAAI/bge-m3 1024-dim Qdrant Vector Store)
    3. សង្ខេប (Qwen 2.5 3B / Gemini AI)
    4. បកប្រែខ្មែរ (Meta NLLB-200 Neural Translator)
    5. ផ្ញើទៅ Telegram VIP Channel & Facebook Page
    """
    logger.info(f"\n============================================================")
    logger.info(f"⚡ [PROCESSING NEWS ID: {news_id}] Starting 5-Step Pipeline...")
    logger.info(f"============================================================")

    # 1. ត្រង Breaking News (XLM-RoBERTa Zero-Shot Filter)
    is_breaking, confidence, filter_label = zero_shot_filter.is_breaking_news(news_text)
    logger.info(f"Step 1: Zero-Shot Filter -> Label: '{filter_label}' | Confidence: {confidence*100:.1f}%")
    if not is_breaking:
        logger.info(f"⏩ [SKIPPED] News is classified as Routine/General News.")
        return

    # 2. រក្សាទិន្នន័យ និង ត្រួតពិនិត្យវ៉ិចទ័រជាន់គ្នា (BAAI/bge-m3 Qdrant Deduplication)
    is_dup, similarity, matched_id = pipeline_engine.dedup_store.is_duplicate(news_text)
    if is_dup:
        logger.warning(f"⚠️ [SKIPPED DUPLICATE] News is {similarity*100:.1f}% similar to previous item [{matched_id}].")
        return

    logger.info(f"Step 2: Qdrant Vector Check -> Unique News Verified (Similarity: {similarity*100:.1f}% < 80%).")

    # 3. សង្ខេបអត្ថបទ (Local Qwen 2.5 3B / Gemini AI) & 4. បកប្រែខ្មែរ (Meta NLLB-200)
    processed_article = pipeline_engine.ai_rewriter.process_news(
        raw_id=news_id,
        title=news_text[:100],
        content=news_text,
        source="Super Brain System",
        source_tier=1,
        is_unverified=False
    )
    logger.info(f"Step 3 & 4: AI Rewriting & Khmer Translation Completed -> Score: {processed_article.credibility_score}%")

    # 5. រៀបចំរូបភាព Banner & ផ្ញើទៅ Telegram (VIP Channel + Admin Chat) & Facebook Page
    image_path = await pipeline_engine.ai_rewriter.generate_banner_image(processed_article.khmer_headline)
    
    try:
        # ផ្ញើទៅ Telegram VIP Channel ជាមួយរូបភាព Banner (១ លើកគត់)
        tg_success = await pipeline_engine.broadcaster.broadcast_to_vip_channel(
            message_text=processed_article.formatted_telegram_post,
            image_path=image_path
        )

        # ផ្ញើទៅ Telegram Admin Chat ID តែក្នុងករណី Admin Chat ID ផ្សេងពី VIP Channel ID ប៉ុណ្ណោះ (ការពារស្ទួន)
        if config.TELEGRAM_ADMIN_CHAT_ID and config.TELEGRAM_ADMIN_CHAT_ID not in ("your_admin_chat_id", "123456789") and str(config.TELEGRAM_ADMIN_CHAT_ID) != str(config.TELEGRAM_VIP_CHANNEL_ID):
            await pipeline_engine.broadcaster.broadcast_to_vip_channel(
                message_text=processed_article.formatted_telegram_post,
                image_path=image_path,
                target_chat_id=config.TELEGRAM_ADMIN_CHAT_ID
            )

        # ផ្ញើទៅ Facebook Page ជាមួយរូបភាព Banner
        fb_success = await pipeline_engine.fb_publisher.publish_news(
            caption=processed_article.formatted_telegram_post,
            image_path=image_path
        )

        if tg_success or fb_success:
            # Index in Qdrant Vector DB
            pipeline_engine.dedup_store.add_item(news_id, news_text)
            logger.info(f"🚀 [STEP 5 COMPLETED: PUBLISHED TO TELEGRAM & FACEBOOK] Item ID: {news_id}\n")
    finally:
        # 🧹 AUTO-CLEANUP: Delete temp banner image immediately after publishing to preserve 100% disk space
        import os
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
                logger.info(f"🧹 [AUTO-CLEANUP] Deleted temporary banner image: '{image_path}' to keep disk 100% clean!")
            except Exception as e:
                logger.error(f"Failed to delete temp image {image_path}: {e}")

async def process_public_opinion_news(news_text: str, comments: list, news_id: str, source: str = "Social Media Hot Post"):
    """
    Super Smart Social Listening & Public Sentiment News Pipeline:
    1. Analyzes public comment stream (Engagement Velocity, Sentiment %, Representative Quotes).
    2. Rewrites into Khmer Public Opinion Journalism Article via Gemini 3.6 Flash.
    3. Renders Playwright HD Banner Image.
    4. Broadcasts to Telegram VIP Channel & Facebook Page.
    """
    logger.info(f"\n============================================================")
    logger.info(f"🔥 [PROCESSING PUBLIC SENTIMENT NEWS ID: {news_id}] Starting Public Opinion Pipeline...")
    logger.info(f"============================================================")

    # 1. Analyze Public Sentiment & Comments
    from sentiment_analyzer import PublicSentimentEngine
    sentiment_engine = PublicSentimentEngine()
    sentiment_metrics = sentiment_engine.analyze_comment_stream(comments)

    logger.info(f"Step 1: Sentiment Analysis -> Support: {sentiment_metrics.support_pct}% | Concern: {sentiment_metrics.concern_pct}% | Trending Score: {sentiment_metrics.trending_score}")

    # 2. Public Opinion Journalistic Rewriting
    processed_article = pipeline_engine.ai_rewriter.rewrite_public_opinion_news(
        raw_id=news_id,
        title=news_text[:100],
        content=news_text,
        source=source,
        sentiment_metrics=sentiment_metrics
    )

    # 3. Banner Image Rendering
    image_path = await pipeline_engine.ai_rewriter.generate_banner_image(processed_article.khmer_headline)

    try:
        # 4. Broadcast to Telegram VIP & Admin (១ លើកគត់)
        tg_success = await pipeline_engine.broadcaster.broadcast_to_vip_channel(
            message_text=processed_article.formatted_telegram_post,
            image_path=image_path
        )
        if config.TELEGRAM_ADMIN_CHAT_ID and config.TELEGRAM_ADMIN_CHAT_ID not in ("your_admin_chat_id", "123456789") and str(config.TELEGRAM_ADMIN_CHAT_ID) != str(config.TELEGRAM_VIP_CHANNEL_ID):
            await pipeline_engine.broadcaster.broadcast_to_vip_channel(
                message_text=processed_article.formatted_telegram_post,
                image_path=image_path,
                target_chat_id=config.TELEGRAM_ADMIN_CHAT_ID
            )

        # 5. Publish to Facebook Page
        fb_success = await pipeline_engine.fb_publisher.publish_news(
            caption=processed_article.formatted_telegram_post,
            image_path=image_path
        )

        if tg_success or fb_success:
            pipeline_engine.dedup_store.add_item(news_id, news_text)
            logger.info(f"🚀 [PUBLIC OPINION NEWS PUBLISHED TO TELEGRAM & FACEBOOK] Item ID: {news_id}\n")
    finally:
        import os
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass

async def process_political_news(news_text: str, news_id: str, source: str = "Official Political Party Statement"):
    """
    Super Smart Political Science & Philosophy News Pipeline:
    1. Identifies political party & extracts Article 51 Constitution & Philosophy tenets.
    2. Rewrites into Khmer Political Science Article via Gemini 3.6 Flash.
    3. Renders Playwright HD Banner Image.
    4. Broadcasts to Telegram VIP Channel & Facebook Page.
    """
    logger.info(f"\n============================================================")
    logger.info(f"🏛️ [PROCESSING POLITICAL NEWS ID: {news_id}] Starting Political Philosophy Pipeline...")
    logger.info(f"============================================================")

    # 1. Analyze Political Statement & Philosophy
    from political_analyzer import PoliticalPartyAnalyzer
    political_engine = PoliticalPartyAnalyzer()
    political_metrics = political_engine.analyze_statement(news_text)

    logger.info(f"Step 1: Political Analysis -> Party: {political_metrics.party_name} | Constitutional Alignment: {political_metrics.democratic_alignment_score}%")

    # 2. Political Science Rewriting
    processed_article = pipeline_engine.ai_rewriter.rewrite_political_philosophy_news(
        raw_id=news_id,
        title=news_text[:100],
        content=news_text,
        source=source,
        political_metrics=political_metrics
    )

    # 3. Banner Image Rendering
    image_path = await pipeline_engine.ai_rewriter.generate_banner_image(processed_article.khmer_headline)

    try:
        # 4. Broadcast to Telegram VIP & Admin (១ លើកគត់)
        tg_success = await pipeline_engine.broadcaster.broadcast_to_vip_channel(
            message_text=processed_article.formatted_telegram_post,
            image_path=image_path
        )
        if config.TELEGRAM_ADMIN_CHAT_ID and config.TELEGRAM_ADMIN_CHAT_ID not in ("your_admin_chat_id", "123456789") and str(config.TELEGRAM_ADMIN_CHAT_ID) != str(config.TELEGRAM_VIP_CHANNEL_ID):
            await pipeline_engine.broadcaster.broadcast_to_vip_channel(
                message_text=processed_article.formatted_telegram_post,
                image_path=image_path,
                target_chat_id=config.TELEGRAM_ADMIN_CHAT_ID
            )

        # 5. Publish to Facebook Page
        fb_success = await pipeline_engine.fb_publisher.publish_news(
            caption=processed_article.formatted_telegram_post,
            image_path=image_path
        )

        if tg_success or fb_success:
            pipeline_engine.dedup_store.add_item(news_id, news_text)
            logger.info(f"🚀 [POLITICAL PHILOSOPHY NEWS PUBLISHED TO TELEGRAM & FACEBOOK] Item ID: {news_id}\n")
    finally:
        import os
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception:
                pass

async def process_batch_news():
    """Fetch and process incoming news items from RSS feeds in batch."""
    logger.info("📡 [RSS INGESTION] Scanning live news feeds...")
    news_items = await pipeline_engine.ingestion.fetch_from_rss_async()
    if not news_items:
        logger.info("No new live RSS news items found in this 60s cycle. Waiting for next scan...")
        return

    logger.info(f"Retrieved {len(news_items)} live news items to process.")
    for item in news_items:
        full_text = f"{item.title} - {item.content}"
        await process_news(news_text=full_text, news_id=item.id)
        await asyncio.sleep(3)  # Pacing delay to prevent Gemini 429 Rate Limits

async def main():
    logger.info("⚡ [STARTING SUPER BRAIN AI SYSTEM] Initializing 24/7 Dual-Thread Orchestrator...")
    
    # 1. Spawn Interactive Telegram Bot Listener in Background Thread
    try:
        from bot_interactive import SuperSmartTelegramBot
        bot_listener = SuperSmartTelegramBot()
        asyncio.create_task(bot_listener.poll_updates_loop())
        logger.info("⚡ [TELEGRAM BOT LISTENER READY] Responding to /start, /status, /backup, /ping <10ms!")
    except Exception as e:
        logger.error(f"Failed to start Interactive Telegram Bot listener: {e}")

    # 2. Continuous 24/7 RSS Ingestion Loop
    while True:
        try:
            await process_batch_news()
        except Exception as e:
            logger.error(f"Error in 24/7 news cycle: {e}")
        
        logger.info("⏳ [CYCLE COMPLETED] Waiting 60s for next 24/7 National News Scan...")
        await asyncio.sleep(60)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n🛑 [STOPPED] Super Brain AI News Engine stopped by user.")
