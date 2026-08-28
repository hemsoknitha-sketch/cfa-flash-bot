import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
party_law_file = os.path.join(data_dir, "cambodian_political_party_law.json")
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

with open(party_law_file, "r", encoding="utf-8") as f:
    party_laws = json.load(f)

with open(master_law_file, "r", encoding="utf-8") as f:
    master_laws = json.load(f)

# Filter out old Political Party law entries from master_laws
non_party_laws = [
    item for item in master_laws 
    if "គណបក្សនយោបាយ" not in item.get("code_name", "")
]

# Merge new complete party laws with non_party_laws
new_master_laws = party_laws + non_party_laws

with open(master_law_file, "w", encoding="utf-8") as f:
    json.dump(new_master_laws, f, ensure_ascii=False, indent=2)

print(f"Merged {len(party_laws)} Political Party Law articles with {len(non_party_laws)} other laws. Total in master vault: {len(new_master_laws)}")
