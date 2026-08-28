import sys
import os
import asyncio
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_legal_engine_loading_and_search():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine: {len(engine.laws)}")
    assert len(engine.laws) >= 51, "Engine should load at least 51 laws!"

    # Test query 1: Registration of political parties
    q1 = "តើគណបក្សនយោបាយត្រូវសុំចុះបញ្ជីនៅក្រសួងណា ហើយត្រូវការស្នាមមេដៃប៉ុន្មាន?"
    res1 = engine.search_relevant_laws(q1, limit=3)
    print(f"\nQuery 1: {q1}")
    for item in res1:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test query 2: Dissolution by Supreme Court
    q2 = "តើតុលាការកំពូលមានសមត្ថកិច្ចរំលាយគណបក្សនយោបាយតាមមាត្រាណា?"
    res2 = engine.search_relevant_laws(q2, limit=3)
    print(f"\nQuery 2: {q2}")
    for item in res2:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Citation Generation
    citation = engine.generate_legal_compliance_citation("សកម្មភាពគណបក្សនយោបាយ", "ការចុះបញ្ជីនៅក្រសួងមហាផ្ទៃ និងការគោរពអធិបតេយ្យជាតិ")
    print(f"\nGenerated Citation:\n{citation}")

    print("\n✅ Khmer Legal Engine Verification Passed!")

if __name__ == "__main__":
    test_legal_engine_loading_and_search()
