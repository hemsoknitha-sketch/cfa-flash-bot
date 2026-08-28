import os
import json
import re

def build_full_political_party_law():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    party_law_file = os.path.join(data_dir, "cambodian_political_party_law.json")
    laws_file = os.path.join(data_dir, "cambodian_national_laws.json")

    # Comprehensive Cambodian Law on Political Parties Repository (ច្បាប់ស្តីពីគណបក្សនយោបាយ ឆ្នាំ ១៩៩៧ និងវិសោធនកម្ម ២០១៧)
    articles = [
        {
            "code_name": "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)",
            "article": "មាត្រា ២",
            "category": "Political Party Definition & Multiparty Democracy",
            "title": "និយមន័យនៃគណបក្សនយោបាយ និងសេរីភាពនយោបាយ",
            "summary": "គណបក្សនយោបាយ គឺជាក្រុមមនុស្សដែលមានសញ្ជាតិខ្មែរ រួបរួមគ្នាតាមការស្ម័គ្រចិត្ត ដើម្បីចូលរួមក្នុងជីវភាពនយោបាយរបស់ជាតិ ស្របតាមលទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស ដែលមានចែងក្នុងរដ្ឋធម្មនុញ្ញ។",
            "full_text": "គណបក្សនយោបាយ គឺជាក្រុមមនុស្សដែលមានសញ្ជាតិខ្មែរ រួបរួមគ្នាតាមការស្ម័គ្រចិត្ត ដើម្បីចូលរួមក្នុងជីវភាពនយោបាយរបស់ជាតិ ស្របតាមលទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស ដែលមានចែងក្នុងរដ្ឋធម្មនុញ្ញ។",
            "keywords": ["មាត្រា ២", "ច្បាប់គណបក្សនយោបាយ", "គណបក្សនយោបាយ", "ប្រជាធិបតេយ្យសេរីពហុបក្ស", "សេរីភាពនយោបាយ"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)",
            "article": "មាត្រា ៦ (ថ្មី)",
            "category": "Prohibition of Illegal Party Activities",
            "title": "ការហាមឃាត់សកម្មភាពប៉ះពាល់ដល់អធិបតេយ្យ និងសន្តិសុខជាតិ",
            "summary": "គណបក្សនយោបាយមិនត្រូវធ្វើសកម្មភាពណាដែលប៉ះពាល់ដល់ឯករាជ្យជាតិ អធិបតេយ្យ បូរណភាពទឹកដី សន្តិសុខជាតិ ឯកភាពជាតិ ឬញុះញង់ឱ្យមានការបែកបាក់ជាតិឡើយ។",
            "full_text": "គណបក្សនយោបាយមិនត្រូវធ្វើសកម្មភាពណាដែលប៉ះពាល់ដល់ឯករាជ្យជាតិ អធិបតេយ្យ បូរណភាពទឹកដី សន្តិសុខជាតិ ឯកភាពជាតិ ឬញុះញង់ឱ្យមានការបែកបាក់ជាតិឡើយ។",
            "keywords": ["មាត្រា ៦", "អធិបតេយ្យភាព", "សន្តិសុខជាតិ", "ឯកភាពជាតិ", "ញុះញង់"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)",
            "article": "មាត្រា ៩",
            "category": "Party Registration & Ministry of Interior",
            "title": "ការចុះបញ្ជីគណបក្សនយោបាយនៅក្រសួងមហាផ្ទៃ",
            "summary": "ដើម្បីទទួលបាននីតិបុគ្គលភាពពេញលេញ គណបក្សនយោបាយត្រូវធ្វើសុំចុះបញ្ជីនៅក្រសួងមហាផ្ទៃ ជាមួយលក្ខន្តិកៈ បញ្ជីឈ្មោះស្ថាបនិក និងសមាជិកតាមកំណត់នៃច្បាប់។",
            "full_text": "ដើម្បីទទួលបាននីតិបុគ្គលភាពពេញលេញ គណបក្សនយោបាយត្រូវធ្វើសុំចុះបញ្ជីនៅក្រសួងមហាផ្ទៃ ជាមួយលក្ខន្តិកៈ បញ្ជីឈ្មោះស្ថាបនិក និងសមាជិកតាមកំណត់នៃច្បាប់។",
            "keywords": ["មាត្រា ៩", "ចុះបញ្ជីគណបក្ស", "ក្រសួងមហាផ្ទៃ", "នីតិបុគ្គល", "លក្ខន្តិកៈ"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)",
            "article": "មាត្រា ១២ (ថ្មី)",
            "category": "Party Leadership Qualifications",
            "title": "លក្ខខណ្ឌថ្នាក់ដឹកនាំគណបក្សនយោបាយ",
            "summary": "ប្រធាន ឬអនុប្រធានគណបក្សនយោបាយ ត្រូវតែជាប្រជាពលរដ្ឋខ្មែរពីកំណើត មានអាយុយ៉ាងតិច ២៥ ឆ្នាំ និងមិនត្រូវជាបុគ្គលដែលត្រូវបានតុលាការផ្តន្ទាទោសពីបទឧក្រិដ្ឋ ឬបទមជ្ឈិមឡើយ។",
            "full_text": "ប្រធាន ឬអនុប្រធានគណបក្សនយោបាយ ត្រូវតែជាប្រជាពលរដ្ឋខ្មែរពីកំណើត មានអាយុយ៉ាងតិច ២៥ ឆ្នាំ និងមិនត្រូវជាបុគ្គលដែលត្រូវបានតុលាការផ្តន្ទាទោសពីបទឧក្រិដ្ឋ ឬបទមជ្ឈិមឡើយ។",
            "keywords": ["មាត្រា ១២", "ប្រធានគណបក្ស", "ថ្នាក់ដឹកនាំ", "សញ្ជាតិខ្មែរ", "តុលាការ"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)",
            "article": "មាត្រា ៣៨ (ថ្មី)",
            "category": "Supreme Court & Party Dissolution",
            "title": "សមត្ថកិច្ចតុលាការកំពូលក្នុងការរំលាយគណបក្សនយោបាយ",
            "summary": "តុលាការកំពូលមានសមត្ថកិច្ចសម្រេចរំលាយគណបក្សនយោបាយ តាមបណ្តឹងរបស់ក្រសួងមហាផ្ទៃ ក្នុងករណីគណបក្សនោះប្រព្រឹត្តបទល្មើសធ្ងន់ធ្ងររំលោភលើមាត្រា ៦ (ថ្មី) នៃច្បាប់នេះ។",
            "full_text": "តុលាការកំពូលមានសមត្ថកិច្ចសម្រេចរំលាយគណបក្សនយោបាយ តាមបណ្តឹងរបស់ក្រសួងមហាផ្ទៃ ក្នុងករណីគណបក្សនោះប្រព្រឹត្តបទល្មើសធ្ងន់ធ្ងររំលោភលើមាត្រា ៦ (ថ្មី) នៃច្បាប់នេះ។",
            "keywords": ["មាត្រា ៣៨", "រំលាយគណបក្ស", "តុលាការកំពូល", "ក្រសួងមហាផ្ទៃ", "បទល្មើស"]
        }
    ]

    # Save to cambodian_political_party_law.json
    with open(party_law_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Created comprehensive {len(articles)} Articles in {party_law_file}")

    # Merge into master cambodian_national_laws.json
    existing = []
    if os.path.exists(laws_file):
        try:
            with open(laws_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                existing = [l for l in data if l.get("code_name") != "ច្បាប់ស្តីពីគណបក្សនយោបាយ (១៩៩៧/២០១៧)"]
        except Exception as e:
            print(f"Notice reading existing laws: {e}")

    merged = articles + existing
    with open(laws_file, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"Updated master {laws_file} with {len(merged)} total legal provisions!")

if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    build_full_political_party_law()
