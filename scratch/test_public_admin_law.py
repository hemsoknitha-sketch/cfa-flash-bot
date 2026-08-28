import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_public_admin_engine():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine: {len(engine.laws)}")
    assert len(engine.laws) >= 170, "Engine should load at least 170 laws!"

    # Test Query 1: Village Chief duties
    q1 = "តើមេភូមិ និង អនុប្រធានភូមិ មានតួនាទី និងភារកិច្ចអ្វីខ្លះក្នុងការរក្សាសន្តិសុខ?"
    res1 = engine.search_relevant_laws(q1, limit=3)
    print(f"\nQuery 1: {q1}")
    for item in res1:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 2: Commune Chief vs Clerk roles
    q2 = "តើមេឃុំ និង ស្មៀនឃុំ មានតួនាទីខុសគ្នាយ៉ាងដូចម្តេចក្នុងការធ្វើសំបុត្រកំណើត និងអត្រានុកូលដ្ឋាន?"
    res2 = engine.search_relevant_laws(q2, limit=3)
    print(f"\nQuery 2: {q2}")
    for item in res2:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 3: Provincial Governor vs Line Departments
    q3 = "តើអភិបាលខេត្ត និង មន្ទីរជំនាញជុំវិញខេត្ត មានសមត្ថកិច្ចដឹកនាំ និងសម្របសម្រួលយ៉ាងដូចម្តេច?"
    res3 = engine.search_relevant_laws(q3, limit=3)
    print(f"\nQuery 3: {q3}")
    for item in res3:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Citation Generation
    citation = engine.generate_legal_compliance_citation("សេវារដ្ឋបាលថ្នាក់មូលដ្ឋាន", "ការផ្តល់សេវារដ្ឋបាលតាមរយៈការិយាល័យច្រកចេញចូលតែមួយ និងមេឃុំ")
    print(f"\nGenerated Citation:\n{citation}")

    print("\n✅ Khmer Legal Engine Public Administration Verification Passed!")

if __name__ == "__main__":
    test_public_admin_engine()
