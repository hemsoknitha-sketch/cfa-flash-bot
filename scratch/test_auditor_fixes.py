import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from khmer_auditor import khmer_auditor

t1 = "ប្រធានបទ អភិបាលកិច្ច ប្រធានសក្តិ ភាពជឿជាក់ 95.0%"
res1 = khmer_auditor.sanitize_khmer_spelling_and_punctuation(t1)

s1 = "Facebook Page / User Source"
valid, h, b, cleaned_s = khmer_auditor.audit_full_news_item("ចំណងជើង", "ខ្លឹមសារ", source_name=s1)

print("=== TEST AUDITOR FIXES ===")
print("Input 1:", t1)
print("Result 1:", res1)
print("Source Input:", s1)
print("Source Cleaned:", cleaned_s)
