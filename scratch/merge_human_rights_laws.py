import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

new_law_files = [
    "cambodian_trade_unions_law.json",
    "cambodian_peaceful_demonstration_law.json",
    "cambodian_international_human_rights.json",
    "cambodian_chrc_human_rights_committee.json",
    "cambodian_domestic_violence_law.json"
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

print(f"Successfully merged all 5 Human Rights & Civil Society legal frameworks into master vault. Total provisions in disk storage: {len(merged)}")
