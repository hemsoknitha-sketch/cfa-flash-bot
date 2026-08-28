import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from ai_rewriter import SuperBrainAIRewriter
from khmer_auditor import khmer_auditor

rewriter = SuperBrainAIRewriter()
raw_title = "តើធ្វើបែបណាទើបវិនិយោគិនល្អៗ ចូលប្រទេសខ្មែរ"
raw_content = "ចំនួនមើល 30 ពាន់ · ប្រតិកម្ម 3.1 ពាន់ | តើធ្វើបែបណាទើបវិនិយោគិនល្អៗ ចូលប្រទេសខ្មែរ។ | ពលរដ្ឋសកម្ម"
raw_source = "ប្រភព Facebook ផ្លូវការ"

processed = rewriter._rule_based_fallback(
    raw_id="test-reel-1",
    title=raw_title,
    content=raw_content,
    source=raw_source,
    source_tier=1,
    is_unverified=False
)

is_valid, h, b, s = khmer_auditor.audit_full_news_item(
    headline=processed.khmer_headline,
    body=processed.khmer_body,
    source_name=raw_source
)

print("=== REEL TOPIC EXPANDER TEST ===")
print("HEADLINE:", h)
print("BODY:\n", b)
