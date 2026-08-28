import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from ai_rewriter import SuperBrainAIRewriter
from khmer_auditor import khmer_auditor

rewriter = SuperBrainAIRewriter()
query = "តើអ្វីជាអត្ថប្រយោជន៍នៃការគោរពរដ្ឋធម្មនុញ្ញ មាត្រា ៥១ (ថ្មី)?"

ans = rewriter.answer_freeform_question(query)
clean_ans = khmer_auditor.sanitize_khmer_spelling_and_punctuation(ans)

print("=== FREE-FORM AI ASSISTANT TEST ===")
print("QUERY:", query)
print("ANSWER:\n", clean_ans)
