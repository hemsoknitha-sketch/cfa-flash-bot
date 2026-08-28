import os
import json
import re

def build_full_extended_cambodian_laws():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    criminal_code_file = os.path.join(data_dir, "cambodian_criminal_code.json")
    land_labor_file = os.path.join(data_dir, "cambodian_land_labor_laws.json")
    laws_file = os.path.join(data_dir, "cambodian_national_laws.json")

    # 1. ក្រមព្រហ្មទណ្ឌ (Cambodian Criminal Code / Penal Code 2009)
    criminal_code_articles = [
        {
            "code_name": "ក្រមព្រហ្មទណ្ឌ នៃព្រះរាជាណាចក្រកម្ពុជា (២០០៩)",
            "book": "មាតិកា ៖ បទល្មើសប្រឆាំងនឹងបុគ្គល និងសន្តិសុខ",
            "article": "មាត្រា ៣០៥",
            "category": "Public Defamation & Individual Reputation",
            "title": "បទបរិហារកេរ្តិ៍ជាសាធារណៈ",
            "summary": "គ្រប់ការអះអាង ឬការទម្លាក់កំហុសដោយអព្ភន្តរៈ ដែលនាំឱ្យប៉ះពាល់ដល់កិត្តិយស ឬកេរ្តិ៍ឈ្មោះនៃបុគ្គល ឬស្ថាប័ន តាមរយៈសារព័ត៌មាន បណ្តាញសង្គម ឬទីសាធារណៈ គឺជាបទបរិហារកេរ្តិ៍ជាសាធារណៈ។",
            "full_text": "គ្រប់ការអះអាង ឬការទម្លាក់កំហុសដោយអព្ភន្តរៈ ដែលនាំឱ្យប៉ះពាល់ដល់កិត្តិយស ឬកេរ្តិ៍ឈ្មោះនៃបុគ្គល ឬស្ថាប័ន តាមរយៈសារព័ត៌មាន បណ្តាញសង្គម ឬទីសាធារណៈ គឺជាបទបរិហារកេរ្តិ៍ជាសាធារណៈ។",
            "keywords": ["មាត្រា ៣០៥", "ក្រមព្រហ្មទណ្ឌ", "បរិហារកេរ្តិ៍", "កិត្តិយស", "កេរ្តិ៍ឈ្មោះ"]
        },
        {
            "code_name": "ក្រមព្រហ្មទណ្ឌ នៃព្រះរាជាណាចក្រកម្ពុជា (២០០៩)",
            "book": "មាតិកា ៖ បទល្មើសប្រឆាំងនឹងសន្តិសុខសាធារណៈ",
            "article": "មាត្រា ៤៩៥",
            "category": "Incitement & Public Order",
            "title": "បទញុះញង់ឱ្យប្រព្រឹត្តបទល្មើសជាអាទិ៍ ឬបង្កភាពវឹកវរធ្ងន់ធ្ងរដល់សន្តិសុខសង្គម",
            "summary": "ការញុះញង់ផ្ទាល់ដោយពាក្យសម្តី សារលិខិត រូបភាព ឬប្រព័ន្ធផ្សព្វផ្សាយ ដើម្បីឱ្យប្រព្រឹត្តបទល្មើស ឬបង្កភាពវឹកវរធ្ងន់ធ្ងរដល់សន្តិសុខសង្គម ត្រូវផ្តន្ទាទោសដាក់ពន្ធនាគារពី ៦ ខែ ដល់ ២ ឆ្នាំ។",
            "full_text": "ការញុះញង់ផ្ទាល់ដោយពាក្យសម្តី សារលិខិត រូបភាព ឬប្រព័ន្ធផ្សព្វផ្សាយ ដើម្បីឱ្យប្រព្រឹត្តបទល្មើស ឬបង្កភាពវឹកវរធ្ងន់ធ្ងរដល់សន្តិសុខសង្គម ត្រូវផ្តន្ទាទោសដាក់ពន្ធនាគារពី ៦ ខែ ដល់ ២ ឆ្នាំ។",
            "keywords": ["មាត្រា ៤៩៥", "ការញុះញង់", "សន្តិសុខសង្គម", "ភាពវឹកវរ", "ពន្ធនាគារ"]
        },
        {
            "code_name": "ក្រមព្រហ្មទណ្ឌ នៃព្រះរាជាណាចក្រកម្ពុជា (២០០៩)",
            "book": "មាតិកា ៖ បទល្មើសបច្ចេកវិទ្យា និងព័ត៌មានវិទ្យា",
            "article": "មាត្រា ៤២៧",
            "category": "Cybercrime & Data Tampering",
            "title": "បទល្មើសលួចចូលប្រព័ន្ធទិន្នន័យ និងកែប្រែទិន្នន័យដោយខុសច្បាប់ (Cybercrime)",
            "summary": "អំពើលួចចូលទៅក្នុងប្រព័ន្ធដំណើរការទិន្នន័យដោយខុសច្បាប់ ឬការលុប បន្ថែម ឬកែប្រែទិន្នន័យប្រព័ន្ធព័ត៌មានវិទ្យា ត្រូវទទួលទោសព្រហ្មទណ្ឌ។",
            "full_text": "អំពើលួចចូលទៅក្នុងប្រព័ន្ធដំណើរការទិន្នន័យដោយខុសច្បាប់ ឬការលុប បន្ថែម ឬកែប្រែទិន្នន័យប្រព័ន្ធព័ត៌មានវិទ្យា ត្រូវទទួលទោសព្រហ្មទណ្ឌ។",
            "keywords": ["មាត្រា ៤២៧", "បទល្មើសបច្ចេកវិទ្យា", "Cybercrime", "លួចទិន្នន័យ", "Hacking"]
        }
    ]

    # 2. ច្បាប់ស្តីពីដីធ្លី (Land Law 2001)
    land_law_articles = [
        {
            "code_name": "ច្បាប់ស្តីពីដីធ្លី (២០០១)",
            "article": "មាត្រា ៥",
            "category": "Land Ownership & State Public Property",
            "title": "កិច្ចការពារកម្មសិទ្ធិដីធ្លី និងដីសាធារណៈរបស់រដ្ឋ",
            "summary": "គ្មានបុគ្គលណាម្នាក់អាចត្រូវបានដកហូតកម្មសិទ្ធិដីធ្លីរបស់ខ្លួនបានឡើយ លើកលែងតែក្នុងករណីប្រយោជន៍សាធារណៈដែលកំណត់ដោយច្បាប់ និងតម្រូវឱ្យមានការសងសំណងជាមុនដោយសមរម្យ និងយុត្តិធម៌។",
            "full_text": "គ្មានបុគ្គលណាម្នាក់អាចត្រូវបានដកហូតកម្មសិទ្ធិដីធ្លីរបស់ខ្លួនបានឡើយ លើកលែងតែក្នុងករណីប្រយោជន៍សាធារណៈដែលកំណត់ដោយច្បាប់ និងតម្រូវឱ្យមានការសងសំណងជាមុនដោយសមរម្យ និងយុត្តិធម៌។",
            "keywords": ["មាត្រា ៥", "ច្បាប់ដីធ្លី", "កម្មសិទ្ធិដីធ្លី", "សំណងជាមុន", "ប្រយោជន៍សាធារណៈ"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីដីធ្លី (២០០១)",
            "article": "មាត្រា ១៦",
            "category": "State Public Land Inalienability",
            "title": "ភាពមិនអាចលក់ ឬទន្ទ្រានកាន់កាប់ដីសាធារណៈរបស់រដ្ឋ",
            "summary": "ដីសាធារណៈរបស់រដ្ឋ (ដូចជា ព្រៃឈើ ទន្លេ ផ្លូវថ្នល់ ឧទ្យានជាតិ) មិនអាចធ្វើជាកម្មសិទ្ធិឯកជន លក់ដូរ ឬទន្ទ្រានកាន់កាប់បានឡើយ។",
            "full_text": "ដីសាធារណៈរបស់រដ្ឋ (ដូចជា ព្រៃឈើ ទន្លេ ផ្លូវថ្នល់ ឧទ្យានជាតិ) មិនអាចធ្វើជាកម្មសិទ្ធិឯកជន លក់ដូរ ឬទន្ទ្រានកាន់កាប់បានឡើយ។",
            "keywords": ["មាត្រា ១៦", "ដីសាធារណៈរបស់រដ្ឋ", "ទន្ទ្រានដី", "ព្រៃឈើ", "ទន្លេ"]
        }
    ]

    # 3. ច្បាប់ស្តីពីការងារ (Labor Law 1997)
    labor_law_articles = [
        {
            "code_name": "ច្បាប់ស្តីពីការងារ (១៩៩៧)",
            "article": "មាត្រា ១២",
            "category": "Labor Rights & Non-Discrimination",
            "title": "ការហាមឃាត់ការរើសអើងក្នុងការងារ និងប្រាក់ឈ្នួលស្មើគ្នា",
            "summary": "គ្មាននិយោជកណាម្នាក់អាចធ្វើការរើសអើងកម្មករនិយោជិត ដោយសារភេទ អាយុ ពូជសាសន៍ សាសនា ឬគណបក្សនយោបាយឡើយ។ ការងារស្មើគ្នា ត្រូវទទួលបានប្រាក់ឈ្នួលស្មើគ្នា។",
            "full_text": "គ្មាននិយោជកណាម្នាក់អាចធ្វើការរើសអើងកម្មករនិយោជិត ដោយសារភេទ អាយុ ពូជសាសន៍ សាសនា ឬគណបក្សនយោបាយឡើយ។ ការងារស្មើគ្នា ត្រូវទទួលបានប្រាក់ឈ្នួលស្មើគ្នា។",
            "keywords": ["មាត្រា ១២", "ច្បាប់ការងារ", "រើសអើង", "ប្រាក់ឈ្នួល", "កម្មករនិយោជិត"]
        },
        {
            "code_name": "ច្បាប់ស្តីពីការងារ (១៩៩៧)",
            "article": "មាត្រា ៣១៨",
            "category": "Labor Disputes & Strikes",
            "title": "សិទ្ធិធ្វើកូដកម្ម និងការដោះស្រាយវិវាទការងារ",
            "summary": "សិទ្ធិធ្វើកូដកម្ម គឺជាសិទ្ធិស្របច្បាប់របស់កម្មករនិយោជិត ក្នុងការការពារផលប្រយោជន៍សេដ្ឋកិច្ច និងសង្គម បន្ទាប់ពីនីតិវិធីសះជាត្រូវបានរៀបចំរួចរាល់។",
            "full_text": "សិទ្ធិធ្វើកូដកម្ម គឺជាសិទ្ធិស្របច្បាប់របស់កម្មករនិយោជិត ក្នុងការការពារផលប្រយោជន៍សេដ្ឋកិច្ច និងសង្គម បន្ទាប់ពីនីតិវិធីសះជាត្រូវបានរៀបចំរួចរាល់។",
            "keywords": ["មាត្រា ៣១៨", "កូដកម្ម", "វិវាទការងារ", "រោងចក្រ", "កម្មករ"]
        }
    ]

    # 4. ច្បាប់ស្តីពីពាណិជ្ជកម្មតាមប្រព័ន្ធអេឡិចត្រូនិក (E-Commerce Law 2019)
    ecommerce_law_articles = [
        {
            "code_name": "ច្បាប់ស្តីពីពាណិជ្ជកម្មតាមប្រព័ន្ធអេឡិចត្រូនិក (២០១៩)",
            "article": "មាត្រា ១៣",
            "category": "E-Commerce & Digital Signature Legal Validity",
            "title": "សុពលភាពផ្លូវច្បាប់នៃសារអេឡិចត្រូនិក និងហត្ថលេខាឌីជីថល",
            "summary": "សារអេឡិចត្រូនិក និងហត្ថលេខាឌីជីថល មានតម្លៃ និងសុពលភាពផ្លូវច្បាប់ស្មើនឹងឯកសារក្រដាស និងហត្ថលេខាលើក្រដាស។",
            "full_text": "សារអេឡិចត្រូនិក និងហត្ថលេខាឌីជីថល មានតម្លៃ និងសុពលភាពផ្លូវច្បាប់ស្មើនឹងឯកសារក្រដាស និងហត្ថលេខាលើក្រដាស។",
            "keywords": ["មាត្រា ១៣", "ពាណិជ្ជកម្មតាមអេឡិចត្រូនិក", "ហត្ថលេខាឌីជីថល", "សុពលភាពច្បាប់"]
        }
    ]

    # Save to files
    with open(criminal_code_file, "w", encoding="utf-8") as f:
        json.dump(criminal_code_articles, f, ensure_ascii=False, indent=2)

    with open(land_labor_file, "w", encoding="utf-8") as f:
        json.dump(land_law_articles + labor_law_articles + ecommerce_law_articles, f, ensure_ascii=False, indent=2)

    # Merge into master cambodian_national_laws.json
    all_new = criminal_code_articles + land_law_articles + labor_law_articles + ecommerce_law_articles
    
    existing = []
    if os.path.exists(laws_file):
        try:
            with open(laws_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except Exception as e:
            print(f"Notice reading existing laws: {e}")

    # Deduplicate based on code_name + article
    existing_keys = {f"{l.get('code_name')}_{l.get('article')}" for l in existing}
    added_count = 0
    for item in all_new:
        key = f"{item.get('code_name')}_{item.get('article')}"
        if key not in existing_keys:
            existing.append(item)
            existing_keys.add(key)
            added_count += 1

    with open(laws_file, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print(f"✅ Added {added_count} new statutes. Total provisions in {laws_file}: {len(existing)}")

if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    build_full_extended_cambodian_laws()
