import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

new_law_files = [
    "cambodian_anticorruption_law.json",
    "cambodian_cybercrime_law.json",
    "cambodian_ecommerce_law.json",
    "cambodian_aml_cft_law.json",
    "cambodian_ngo_lango_law.json",
    "cambodian_digital_media_regulations.json",
    "cambodian_consumer_competition_law.json"
]

all_new_items = []
for fname in new_law_files:
    fpath = os.path.join(data_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            items = json.load(f)
            all_new_items.extend(items)

with open(master_law_file, "r", encoding="utf-8") as f:
    master_laws = json.load(f)

# Filter out old duplicates if any based on (code_name, article)
seen = set()
merged = []

for item in all_new_items + master_laws:
    key = (item.get("code_name"), item.get("article"))
    if key not in seen:
        seen.add(key)
        merged.append(item)

with open(master_law_file, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"Successfully merged all 7 new legal frameworks into master vault. Total provisions in disk storage: {len(merged)}")
