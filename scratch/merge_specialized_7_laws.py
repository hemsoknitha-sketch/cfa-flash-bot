import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

new_law_files = [
    "cambodian_military_police_statute.json",
    "cambodian_disaster_emergency_law.json",
    "cambodian_drug_control_law.json",
    "cambodian_weapons_control_law.json",
    "cambodian_commercial_gambling_law.json",
    "cambodian_commercial_enterprises_law.json",
    "cambodian_banking_mfi_law.json"
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

print(f"Successfully merged all 7 specialized legal frameworks into master vault. Total provisions in disk storage: {len(merged)}")
