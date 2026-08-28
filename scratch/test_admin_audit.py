import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from bot_interactive import SuperSmartTelegramBot

bot = SuperSmartTelegramBot()

user_dummy = {
    "id": 999888777,
    "first_name": "Sok",
    "last_name": "Nitha",
    "username": "soknitha_user"
}

req = "បង្ហាញព័ត៌មានសន្តិសុខសង្គម"
resp = "ផ្អែកលើទិន្នន័យចុងក្រោយ ស្ថានភាពសន្តិសុខសង្គមទូទាំងព្រះរាជាណាចក្រកម្ពុជា រក្សាបាននូវកម្រិតស្ថិរភាព..."

print("=== REAL-TIME ADMIN AUDIT ALERT TEST ===")
print("Generated Alert Payload Check:")
user_id = user_dummy.get("id")
full_name = f"{user_dummy.get('first_name')} {user_dummy.get('last_name')}"
username = f"@{user_dummy.get('username')}"

alert_msg = (
    f"🔔 *🧠 [REAL-TIME AUDIT ៖ USER QUESTION]*\n"
    f"👤 *អ្នកប្រើប្រាស់ ៖* `{full_name}` ({username})\n"
    f"🆔 *Chat ID ៖* `{user_id}`\n\n"
    f"📥 *សំណើ/URL ផ្ញើចូល ៖*\n`{req}`\n\n"
    f"📤 *ចម្លើយ AI Super Brain ៖*\n{resp[:350]}...\n"
)
print(alert_msg)
