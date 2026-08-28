import json
import os

data_dir = r"e:\AI CODE PYTHON\CFA Flash Feed\data"
public_admin_file = os.path.join(data_dir, "cambodian_public_administration_law.json")
master_law_file = os.path.join(data_dir, "cambodian_national_laws.json")

with open(public_admin_file, "r", encoding="utf-8") as f:
    public_admin_laws = json.load(f)

with open(master_law_file, "r", encoding="utf-8") as f:
    master_laws = json.load(f)

# Filter out existing Public Administration entries if any to prevent duplicate keys
non_admin_laws = [
    item for item in master_laws 
    if "រដ្ឋបាលសាធារណៈ" not in item.get("code_name", "")
]

# Merge into master laws
new_master_laws = public_admin_laws + non_admin_laws

with open(master_law_file, "w", encoding="utf-8") as f:
    json.dump(new_master_laws, f, ensure_ascii=False, indent=2)

print(f"Merged {len(public_admin_laws)} Public Administration provisions with {len(non_admin_laws)} other laws. Total in master vault: {len(new_master_laws)}")
