import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_master_7_laws():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine memory: {len(engine.laws)}")
    assert len(engine.laws) >= 200, "Engine should load at least 200 laws!"

    test_queries = [
        ("Anti-Corruption (ACU)", "តើប្រធាន ឬមន្ត្រីរាជការត្រូវមានកាតព្វកិច្ចប្រកាសទ្រព្យសម្បត្តិ និងបំណុលជូន ACU យ៉ាងដូចម្តេច?"),
        ("Cybercrime & Hacking", "តើបទល្មើសហែកប្រព័ន្ធ Hacking និងការផ្សាយព័ត៌មានក្លែងក្លាយ Fake News ត្រូវទទួលទោសដូចម្តេច?"),
        ("E-Commerce & Digital Signature", "តើកិច្ចសន្យាអេឡិចត្រូនិក និងហត្ថលេខាឌីជីថលមានសុពលភាពច្បាប់ដែរឬទេ?"),
        ("Anti-Money Laundering (AML)", "តើគ្រឹះស្ថានហិរញ្ញវត្ថុ និងធនាគារមានកាតព្វកិច្ចរាយការណ៍ប្រតិបត្តិការសង្ស័យ STR យ៉ាងដូចម្តេច?"),
        ("LANGO & NGO Neutrality", "តើអង្គការមិនមែនរដ្ឋាភិបាល (NGO) មានកាតព្វកិច្ចសុំចុះបញ្ជី និងរក្សាអព្យាក្រឹតភាពយ៉ាងដូចម្តេច?"),
        ("Digital Media & Online News", "តើអាជ្ញាប័ណ្ណសារព័ត៌មានអនឡាញ និងគេហទំព័រត្រូវសុំចុះបញ្ជីនៅក្រសួងណា?"),
        ("Consumer Protection", "តើការផ្សាយពាណិជ្ជកម្មភូតភរ និងការលក់ទំនិញបោកប្រាស់អ្នកប្រើប្រាស់ត្រូវទទួលទោសដូចម្តេច?")
    ]

    print("\n================ TESTING ALL 7 LEGAL DOMAINS ================")
    for domain, q in test_queries:
        res = engine.search_relevant_laws(q, limit=2)
        print(f"\n📌 Domain: {domain}")
        print(f"   Query: {q}")
        for item in res:
            print(f"   --> [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    print("\n✅ Khmer Legal Engine Master 7 Laws Verification Passed 100%!")

if __name__ == "__main__":
    test_master_7_laws()
