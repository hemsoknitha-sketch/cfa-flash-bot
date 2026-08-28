import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
election_law_file = os.path.join(data_dir, "cambodian_election_law.json")
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

with open(election_law_file, "r", encoding="utf-8") as f:
    election_laws = json.load(f)

with open(master_law_file, "r", encoding="utf-8") as f:
    master_laws = json.load(f)

# Filter out existing Election law entries from master_laws if any to prevent duplicates
non_election_laws = [
    item for item in master_laws 
    if "ការបោះឆ្នោត" not in item.get("code_name", "")
]

# Merge election laws into master vault
new_master_laws = election_laws + non_election_laws

with open(master_law_file, "w", encoding="utf-8") as f:
    json.dump(new_master_laws, f, ensure_ascii=False, indent=2)

print(f"Merged {len(election_laws)} Election Law articles with {len(non_election_laws)} other laws. Total in master vault: {len(new_master_laws)}")
