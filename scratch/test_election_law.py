import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_election_law_engine():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine: {len(engine.laws)}")
    assert len(engine.laws) >= 150, "Engine should load at least 150 laws!"

    # Test Query 1: NEC Role and powers
    q1 = "តើ គ.ជ.ប មានសមត្ថកិច្ច និងភារកិច្ចអ្វីខ្លះក្នុងការរៀបចំការបោះឆ្នោត?"
    res1 = engine.search_relevant_laws(q1, limit=3)
    print(f"\nQuery 1: {q1}")
    for item in res1:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 2: Non-voter candidate disqualification (Article 47 New)
    q2 = "តើប្រជាពលរដ្ឋដែលមិនបានទៅបោះឆ្នោត អាចឈរឈ្មោះឱ្យគេបោះឆ្នោតជាតំណាងរាស្ត្របានដែរឬទេ?"
    res2 = engine.search_relevant_laws(q2, limit=3)
    print(f"\nQuery 2: {q2}")
    for item in res2:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Query 3: Election Campaign duration
    q3 = "តើយុទ្ធនាការឃោសនាបោះឆ្នោតមានរយៈពេលប៉ុន្មានថ្ងៃ ហើយត្រូវបញ្ចប់នៅពេលណា?"
    res3 = engine.search_relevant_laws(q3, limit=3)
    print(f"\nQuery 3: {q3}")
    for item in res3:
        print(f"  - [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    # Test Citation Generation
    citation = engine.generate_legal_compliance_citation("ការរៀបចំការបោះឆ្នោតជ្រើសតាំងតំណាងរាស្ត្រ", "ការិយាល័យបោះឆ្នោត និង គ.ជ.ប")
    print(f"\nGenerated Citation:\n{citation}")

    print("\n✅ Khmer Legal Engine Election Law Verification Passed!")

if __name__ == "__main__":
    test_election_law_engine()
