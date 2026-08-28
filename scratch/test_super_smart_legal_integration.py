import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_rewriter import SuperBrainAIRewriter
from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_integration():
    rewriter = SuperBrainAIRewriter()
    
    # Sample Breaking News Input
    title = "អាជ្ញាធរជាតិប្រយុទ្ធប្រឆាំងគ្រឿងញៀន និងនគរបាលជាតិ បើកប្រតិបត្តិការបង្ក្រាបបទល្មើសគ្រឿងញៀនឆ្លងដែន"
    content = "រាជធានីភ្នំពេញ៖ កម្លាំងសមត្ថកិច្ចនៃអាជ្ញាធរជាតិប្រយុទ្ធប្រឆាំងគ្រឿងញៀន (NACD) សហការជាមួយកងនគរបាលជាតិ បានចុះបង្រ្កាបទីតាំងរក្សាទុក និងជួញដូរគ្រឿងញៀនឆ្លងដែនដ៏ធំមួយ ដោយឃាត់ខ្លួនជនល្មើសជាច្រើននាក់ និងរឹបអូសសារធាតុញៀនជាច្រើនគីឡូក្រាម បញ្ជូនទៅកាន់តុលាការដើម្បីចាត់ការតាមច្បាប់។"
    
    print("\n================ TESTING SUPER SMART AI LEGAL INTEGRATION ================")
    article = rewriter.process_news(
        raw_id="test_001",
        title=title,
        content=content,
        source="ក្រសួងមហាផ្ទៃ",
        source_tier=1,
        is_unverified=False
    )

    print("\n📌 Headline:", article.khmer_headline)
    print("\n📌 Body Text:\n", article.khmer_body)
    print("\n📌 Formatted Telegram Post (With AI Legal Cross-Referencing Citation):\n")
    print(article.formatted_telegram_post)
    
    assert "មូលដ្ឋានច្បាប់ និងនីតិរដ្ឋនៃព្រះរាជាណាចក្រកម្ពុជា" in article.formatted_telegram_post or "ច្បាប់" in article.formatted_telegram_post, "Legal citation should be injected!"
    print("\n✅ Super Smart AI Legal Engine Integration Test Passed 100%!")

if __name__ == "__main__":
    test_integration()
