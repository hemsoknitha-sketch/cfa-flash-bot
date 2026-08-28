import os
import sys
import time
import psutil
import asyncio

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_process_ram_mb() -> float:
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

async def test_ultra_fast_pipeline():
    print("==================================================================")
    print("⚡ CFA FLASH FEED ULTRA-LIGHTWEIGHT & ULTRA-FAST PIPELINE TEST ⚡")
    print("==================================================================")
    
    start_ram = get_process_ram_mb()
    print(f"📊 Initial Process RAM: {start_ram:.2f} MB")

    # 1. Test Translator & Orthography Engine
    t0 = time.time()
    from translator import nllb_translator, super_smart_khmer_formatter
    formatted_khmer = super_smart_khmer_formatter("សម្តេចធិបតី ហ៊ុន ម៉ាណែត ចូលរួម ប្រជុំ នីតិរដ្ធ នៅ កម្ពុជាា")
    t_khmer = time.time() - t0
    print(f"✅ Chuon Nath Orthography Formatter: {t_khmer*1000:.2f}ms -> '{formatted_khmer}'")

    # 2. Test Zero-Shot Domain Classifier
    t0 = time.time()
    from news_filter import zero_shot_filter
    is_breaking, confidence, label = zero_shot_filter.is_breaking_news("Cambodia signs major trade agreement in Phnom Penh.")
    t_filter = time.time() - t0
    print(f"✅ Zero-Shot Domain Signal Filter: {t_filter*1000:.2f}ms -> Label: '{label}' ({confidence*100:.1f}%)")

    # 3. Test Vector Deduplicator (SHA-256 + TF-IDF)
    t0 = time.time()
    from vector_store import VectorDeduplicator
    dedup = VectorDeduplicator()
    is_dup, sim, match_id = dedup.is_duplicate("Cambodia signs major trade agreement in Phnom Penh.")
    t_dedup = time.time() - t0
    print(f"✅ Vector Deduplication Check: {t_dedup*1000:.2f}ms -> Duplicate: {is_dup} (Similarity: {sim:.2f})")

    # 4. Test Ultra-Fast PIL HD Banner Generator
    t0 = time.time()
    from banner_engine import banner_engine
    headline_sample = "សម្តេចធិបតី ហ៊ុន ម៉ាណែត អញ្ជើញជាអធិបតីក្នុងពិធីបើកមហាសន្និបាតជាតិ"
    banner_file = await banner_engine.generate_banner_image(headline_sample)
    t_banner = time.time() - t0
    print(f"✅ PIL HD Banner Rendering: {t_banner*1000:.2f}ms -> Created: '{banner_file}'")

    if os.path.exists(banner_file):
        size_kb = os.path.getsize(banner_file) / 1024
        print(f"   Asset Verified: Size = {size_kb:.2f} KB")
        os.remove(banner_file)

    end_ram = get_process_ram_mb()
    print("------------------------------------------------------------------")
    print(f"📊 Final RAM Footprint: {end_ram:.2f} MB")
    print(f"⚡ Pipeline Verification Test Completed Successfully!")
    print("==================================================================")

if __name__ == "__main__":
    asyncio.run(test_ultra_fast_pipeline())
