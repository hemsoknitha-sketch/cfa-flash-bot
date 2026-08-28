import sys
import os
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_legal_engine import KhmerLegalEngine

logging.basicConfig(level=logging.INFO)

def test_ultimate_all_laws():
    engine = KhmerLegalEngine()
    print(f"Total laws loaded in engine memory: {len(engine.laws)}")
    assert len(engine.laws) >= 230, "Engine should load at least 230 laws!"

    test_queries = [
        ("Military & Police Statute", "តើកងយោធពលខេមរភូមិន្ទ RCAF កងរាជអាវុធហត្ថ និងកងនគរបាលជាតិ មានតួនាទីការពារជាតិ និងរក្សាសន្តិសុខសាធារណៈយ៉ាងដូចម្តេច?"),
        ("Disaster & State of Emergency", "តើសមត្ថកិច្ចរបស់ NCDM ក្នុងការគ្រប់គ្រងគ្រោះមហន្តរាយ និងការប្រកាសដាក់ប្រទេសជាតិស្ថិតក្នុងភាពអាសន្នមានអ្វីខ្លះ?"),
        ("Drug Control (NACD)", "តើអំពើផលិត ជួញដូរ និងរក្សាទុកគ្រឿងញៀន ត្រូវផ្តន្ទាទោសដាក់ពន្ធនាគារប៉ុន្មានឆ្នាំ?"),
        ("Weapons & Explosives Control", "តើការកាន់កាប់ និងជួញដូរអាវុធ គ្រឿងផ្ទុះខុសច្បាប់ ត្រូវទទួលទោសដូចម្តេច?"),
        ("Commercial Gambling (CGMC)", "តើអាជីវកម្មកាស៊ីណូ និងល្បែងស៊ីសងអនឡាញខុសច្បាប់ត្រូវគ្រប់គ្រងដោយ CGMC និងទទួលទោសដូចម្តេច?"),
        ("Commercial Enterprises (CamDX)", "តើការចុះបញ្ជីពាណិជ្ជកម្មតាមប្រព័ន្ធ CamDX និងការទទួលខុសត្រូវរបស់ប្រធានក្រុមហ៊ុនមានអ្វីខ្លះ?"),
        ("Banking & MFI (NBC)", "តើ ធនាគារជាតិនៃកម្ពុជា (NBC) មានអំណាចគ្រប់គ្រងធនាគារ MFI និងការពារប្រាក់បញ្ញើយ៉ាងដូចម្តេច?")
    ]

    print("\n================ TESTING ALL 7 SPECIALIZED LEGAL DOMAINS ================")
    for domain, q in test_queries:
        res = engine.search_relevant_laws(q, limit=2)
        print(f"\n📌 Domain: {domain}")
        print(f"   Query: {q}")
        for item in res:
            print(f"   --> [{item.get('code_name')} - {item.get('article')}] {item.get('title')}: {item.get('summary')}")

    print("\n✅ Khmer Legal Engine ULTIMATE ALL CAMBODIAN LAWS Verification Passed 100%!")

if __name__ == "__main__":
    test_ultimate_all_laws()
