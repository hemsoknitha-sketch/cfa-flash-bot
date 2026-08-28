import sys
import os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
import logging
import json
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

from scraper import IngestionEngine
from vector_store import VectorDeduplicator
from news_filter import zero_shot_filter
from khmer_auditor import khmer_auditor
from config import config

async def test_ingestion_and_pipeline():
    print("\n--- 1. Testing RSS Ingestion ---", flush=True)
    engine = IngestionEngine()
    print(f"Total RSS urls configured: {len(engine.national_feeds)}", flush=True)
    start = time.time()

    items = await engine.fetch_from_rss_async()
    print(f"\nFetched {len(items)} items in parallel in {time.time() - start:.2f}s", flush=True)
    
    if not items:
        print("❌ No items fetched at all!", flush=True)
        return

    dedup = VectorDeduplicator()
    print(f"\nTotal seen hashes in seen_hashes.json: {len(dedup.seen_hashes)}", flush=True)

    valid_count = 0
    dup_count = 0
    quality_reject_count = 0
    breaking_reject_count = 0

    for i, item in enumerate(items):
        full_text = f"{item.title} - {item.content}"
        print(f"\n--- Item {i+1}/{len(items)}: [{item.source}] {item.title[:60]}... ---", flush=True)
        
        # Check breaking news filter
        is_breaking, conf, label = zero_shot_filter.is_breaking_news(full_text)
        if not is_breaking:
            print(f"  ❌ Breaking filter rejected (label={label}, conf={conf})", flush=True)
            breaking_reject_count += 1
            continue
        
        # Check duplicate
        is_dup, sim, matched_id = dedup.is_duplicate(full_text)
        if is_dup:
            print(f"  ❌ Duplicate filter rejected (sim={sim*100:.1f}%, matched_id={matched_id})", flush=True)
            dup_count += 1
            continue

        # Check quality
        is_valid, quality_score, clean_h, clean_b, verified_src, dateline = khmer_auditor.evaluate_news_quality_score(
            headline=item.title[:100],
            body=full_text,
            source_name=item.source,
            url=item.url,
            timestamp=item.timestamp
        )
        if not is_valid:
            print(f"  ❌ Quality Gatekeeper rejected (score={quality_score:.1f}%)", flush=True)
            quality_reject_count += 1
            continue

        print(f"  ✅ Item VALID! Quality Score: {quality_score:.1f}%, Source: {verified_src}", flush=True)
        valid_count += 1

    print("\n================ SUMMARY ================", flush=True)
    print(f"Total items evaluated: {len(items)}", flush=True)
    print(f"Valid candidates to publish: {valid_count}", flush=True)
    print(f"Duplicates (in seen_hashes.json): {dup_count}", flush=True)
    print(f"Quality rejected (<75%): {quality_reject_count}", flush=True)
    print(f"Breaking filter rejected: {breaking_reject_count}", flush=True)

if __name__ == "__main__":
    asyncio.run(test_ingestion_and_pipeline())
