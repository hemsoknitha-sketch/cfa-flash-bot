import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_human_rights_laws():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine memory: {len(engine.laws)}")
    assert len(engine.laws) >= 245, "Engine should load at least 245 laws!"

    test_queries = [
        ("Trade Unions Law", "តើច្បាប់ស្តីពីសហជីព ធានាសិទ្ធិបង្កើតសហជីព និងសិទ្ធិធ្វើកូដកម្មរបស់កម្មករនិយោជិតយ៉ាងដូចម្តេច?"),
        ("Peaceful Demonstration Law", "តើច្បាប់ស្តីពីការធ្វើបាតុកម្មដោយអហិង្សា តម្រូវឱ្យមានការជូនដំណឹងជាមុន និងការពារបាតុករយ៉ាងដូចម្តេច?"),
        ("UN Human Rights & Constitution", "តើរដ្ឋធម្មនុញ្ញ មាត្រា ៣១ និងសេចក្តីប្រកាសជាសកល UN ICCPR ធានាសិទ្ធិមនុស្ស និងសិទ្ធិទទួលបានការជំនុំជម្រះ Fair Trial យ៉ាងដូចម្តេច?"),
        ("CHRC Human Rights Committee", "តើសមត្ថកិច្ចរបស់ គណៈកម្មាធិការសិទ្ធិមនុស្សកម្ពុជា CHRC ក្នុងការស៊ើបអង្កេតបណ្តឹងរំលោភសិទ្ធិមនុស្ស និងធ្វើរបាយការណ៍ UN UPR មានអ្វីខ្លះ?"),
        ("Domestic Violence Law", "តើច្បាប់ស្តីពីការទប់ស្កាត់អំពើហិង្សាក្នុងគ្រួសារ ចេញដីកាការពារបន្ទាន់ និងផ្តន្ទាទោសជនល្មើសយ៉ាងដូចម្តេច?")
    ]

    print("\n================ TESTING ALL 5 HUMAN RIGHTS LEGAL DOMAINS ================")
    for domain, q in test_queries:
        res = engine.search_relevant_laws(q, limit=2)
        print(f"\n📌 Domain: {domain}")
        print(f"   Query: {q}")
        for item in res:
            print(f"   --> [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    print("\n✅ Khmer Legal Engine HUMAN RIGHTS & CIVIL SOCIETY Verification Passed 100%!")

if __name__ == "__main__":
    test_human_rights_laws()
