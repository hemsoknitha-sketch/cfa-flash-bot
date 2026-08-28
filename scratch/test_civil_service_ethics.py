import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_ethics_engine():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine: {len(engine.laws)}")
    assert len(engine.laws) >= 180, "Engine should load at least 180 laws!"

    # Test Query 1: Political neutrality & secrecy
    q1 = "តើមន្ត្រីរាជការស៊ីវិលមានកាតព្វកិច្ចរក្សាអព្យាក្រឹតភាព និងរក្សាការសម្ងាត់ផ្លូវការយ៉ាងដូចម្តេច?"
    res1 = engine.search_relevant_laws(q1, limit=3)
    print(f"\nQuery 1: {q1}")
    for item in res1:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 2: Disciplinary Sanctions Tier 1 & 2
    q2 = "តើទោសវិន័យរដ្ឋបាលថ្នាក់ទី ១ និង ថ្នាក់ទី ២ របស់មន្ត្រីរាជការស៊ីវិលមានអ្វីខ្លះ?"
    res2 = engine.search_relevant_laws(q2, limit=3)
    print(f"\nQuery 2: {q2}")
    for item in res2:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 3: Refusal of Unlawful orders
    q3 = "តើមន្ត្រីរាជការមានសិទ្ធិបដិសេធមិនអនុវត្តបទបញ្ជាខុសច្បាប់របស់ថ្នាក់លើដែរឬទេ?"
    res3 = engine.search_relevant_laws(q3, limit=3)
    print(f"\nQuery 3: {q3}")
    for item in res3:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Citation Generation
    citation = engine.generate_legal_compliance_citation("ក្រមសីលធម៌មន្ត្រីរាជការ", "ការផ្តល់សេវាសាធារណៈដោយអព្យាក្រឹតភាព និងគ្មានការសូកប៉ាន់")
    print(f"\nGenerated Citation:\n{citation}")

    print("\n✅ Khmer Legal Engine Civil Service Ethics Verification Passed!")

if __name__ == "__main__":
    test_ethics_engine()
