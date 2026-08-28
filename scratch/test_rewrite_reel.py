import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from ai_rewriter import SuperBrainAIRewriter
from khmer_auditor import khmer_auditor

async def main():
    content = "តើ តុលាការ និងក្រសួងយុត្តិធម៌ គឺ ជាស្ថាប័នតែមួយឬខុសគ្នា ? | ពលរដ្ឋសកម្ម"
    rewriter = SuperBrainAIRewriter()
    processed = rewriter.process_news(
        raw_id="test_reel_1",
        title=content[:100],
        content=content,
        source="ពលរដ្ឋសកម្ម (Active Citizen)",
        source_tier=1
    )
    
    clean_h = khmer_auditor.audit_headline_purity(processed.khmer_headline)
    clean_b = khmer_auditor.sanitize_khmer_spelling_and_punctuation(processed.khmer_body)
    
    print("=== REWRITTEN REEL ARTICLE ===")
    print("Headline:", clean_h)
    print("Body:\n", clean_b)

if __name__ == "__main__":
    asyncio.run(main())
