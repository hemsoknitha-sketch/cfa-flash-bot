import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
ethics_file = os.path.join(data_dir, "cambodian_civil_service_ethics.json")
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

with open(ethics_file, "r", encoding="utf-8") as f:
    ethics_laws = json.load(f)

with open(master_law_file, "r", encoding="utf-8") as f:
    master_laws = json.load(f)

# Filter out existing ethics laws if any to prevent duplicate keys
non_ethics_laws = [
    item for item in master_laws 
    if "សហលក្ខន្តិកៈមន្ត្រីរាជការ" not in item.get("code_name", "")
]

# Merge ethics laws into master vault
new_master_laws = ethics_laws + non_ethics_laws

with open(master_law_file, "w", encoding="utf-8") as f:
    json.dump(new_master_laws, f, ensure_ascii=False, indent=2)

print(f"Merged {len(ethics_laws)} Civil Service Ethics provisions with {len(non_ethics_laws)} other laws. Total in master vault: {len(new_master_laws)}")
