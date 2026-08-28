import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from bot_interactive import SuperSmartTelegramBot
from security_sentinel import security_sentinel

bot = SuperSmartTelegramBot()

public_kb = bot._build_inline_keyboard(is_admin=False)
admin_kb = bot._build_inline_keyboard(is_admin=True)

public_buttons_count = sum(len(row) for row in public_kb["inline_keyboard"])
admin_buttons_count = sum(len(row) for row in admin_kb["inline_keyboard"])

print("=== STRICT RBAC ACCESS CONTROL TEST ===")
print("Public User Buttons Count:", public_buttons_count)
print("Admin User Buttons Count:", admin_buttons_count)
print("Admin Chat ID Configured:", security_sentinel.admin_chat_id)
print("Non-Admin Chat ID Check (999999):", security_sentinel.verify_admin_access("999999"))
print("Admin Chat ID Check:", security_sentinel.verify_admin_access(security_sentinel.admin_chat_id))
