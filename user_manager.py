"""
Super Smart Enterprise User Management Suite V8.0 GOLD STANDARD.
Features:
1. Persistent User Database (data/user_database.json).
2. Auto-Registration & Telemetry Tracking (Chat ID, Username, Full Name, Joined Date, Last Active, Query Count).
3. Role-Based Access Control (Admin, VIP, Moderator, Subscriber).
4. Ban / Unban & Security Suspension Gatekeeper.
5. Admin User Management Dashboard (/users, /user_info, /ban_user, /unban_user, /set_role, /users_stats).
"""

import os
import json
import time
import logging
from typing import Dict, List, Optional, Union, Tuple
from config import config

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USER_DB_FILE = os.path.join(DATA_DIR, "user_database.json")

class UserManager:
    """
    Dedicated Super Smart User Management System for Bot Admin.
    """
    def __init__(self):
        self.admin_chat_id = str(config.TELEGRAM_ADMIN_CHAT_ID).strip()
        self.users: Dict[str, dict] = {}
        self._load_database()

    def _load_database(self):
        """Loads user database from disk."""
        if not os.path.exists(DATA_DIR):
            try:
                os.makedirs(DATA_DIR, exist_ok=True)
            except Exception:
                pass

        if os.path.exists(USER_DB_FILE):
            try:
                with open(USER_DB_FILE, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
                logger.info(f"👥 [USER MANAGER] Loaded {len(self.users)} registered users from database.")
            except Exception as e:
                logger.error(f"Error loading user database: {e}")
                self.users = {}
        else:
            self.users = {}
            # Seed Admin User if configured
            if self.admin_chat_id and self.admin_chat_id != "your_telegram_admin_chat_id_here":
                self.users[self.admin_chat_id] = {
                    "chat_id": self.admin_chat_id,
                    "username": "@Sokpheatonsai",
                    "full_name": "Bot Admin",
                    "role": "admin",
                    "status": "active",
                    "joined_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "last_active": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "total_queries": 0,
                    "ban_reason": "",
                    "notes": "System Administrator"
                }
                self._save_database()

    def _save_database(self):
        """Saves user database atomically to disk."""
        try:
            temp_file = USER_DB_FILE + ".tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
            os.replace(temp_file, USER_DB_FILE)
        except Exception as e:
            logger.error(f"Error saving user database: {e}")

    def register_or_update_user(self, user_info: dict) -> dict:
        """
        Registers a new user or updates active telemetry upon receiving any interaction.
        """
        if not user_info or not isinstance(user_info, dict):
            return {}

        raw_id = user_info.get("id")
        if not raw_id:
            return {}

        chat_id = str(raw_id).strip()
        first_name = user_info.get("first_name", "")
        last_name = user_info.get("last_name", "")
        full_name = f"{first_name} {last_name}".strip() or "Anonymous User"
        raw_username = user_info.get("username", "")
        username = f"@{raw_username}" if raw_username else "No Username"

        now_str = time.strftime("%Y-%m-%d %H:%M:%S")

        is_admin_user = (chat_id == self.admin_chat_id)

        if chat_id not in self.users:
            role = "admin" if is_admin_user else "subscriber"
            self.users[chat_id] = {
                "chat_id": chat_id,
                "username": username,
                "full_name": full_name,
                "role": role,
                "status": "active",
                "joined_at": now_str,
                "last_active": now_str,
                "total_queries": 1,
                "ban_reason": "",
                "notes": ""
            }
            logger.info(f"👥 [NEW USER REGISTERED] Chat ID: {chat_id} | Name: '{full_name}' ({username}) | Role: {role}")
        else:
            u = self.users[chat_id]
            u["full_name"] = full_name
            u["username"] = username
            u["last_active"] = now_str
            u["total_queries"] = u.get("total_queries", 0) + 1
            if is_admin_user:
                u["role"] = "admin"

        self._save_database()
        return self.users[chat_id]

    def is_banned(self, chat_id: Union[str, int]) -> bool:
        """Checks if a user is currently banned from using the bot."""
        cid = str(chat_id).strip()
        u = self.users.get(cid)
        if u and u.get("status") == "banned":
            return True
        return False

    def find_user(self, query: str) -> Optional[dict]:
        """
        Finds user by Chat ID or Username (e.g. '@username' or '12345678').
        """
        q = str(query).strip().lower()
        if not q:
            return None

        # Try exact Chat ID match
        if q in self.users:
            return self.users[q]

        # Try Username match
        q_user = q if q.startswith("@") else f"@{q}"
        for u in self.users.values():
            if u.get("username", "").lower() == q_user:
                return u

        return None

    def ban_user(self, query: str, reason: str = "Violation of Terms") -> Tuple[bool, str]:
        """Bans a user from bot access."""
        u = self.find_user(query)
        if not u:
            return False, f"⚠️ រកមិនឃើញអ្នកប្រើប្រាស់ `{query}` ក្នុងប្រព័ន្ធឡើយ!"

        cid = u["chat_id"]
        if cid == self.admin_chat_id:
            return False, "🔒 មិនអាច Ban អ្នកគ្រប់គ្រងប្រព័ន្ធ (Bot Admin) បានឡើយ!"

        u["status"] = "banned"
        u["ban_reason"] = reason
        self._save_database()
        logger.warning(f"🚨 [USER BANNED] Admin banned Chat ID: {cid} ({u.get('username')}). Reason: {reason}")
        return True, f"🚫 *[USER BANNED SUCCESSFULLY]*\n\n👤 *អ្នកប្រើប្រាស់ ៖* `{u.get('full_name')}` ({u.get('username')})\n🆔 *Chat ID ៖* `{cid}`\n⚠️ *មូលហេតុ ៖* `{reason}`"

    def unban_user(self, query: str) -> Tuple[bool, str]:
        """Unbans a user, restoring bot access."""
        u = self.find_user(query)
        if not u:
            return False, f"⚠️ រកមិនឃើញអ្នកប្រើប្រាស់ `{query}` ក្នុងប្រព័ន្ធឡើយ!"

        cid = u["chat_id"]
        u["status"] = "active"
        u["ban_reason"] = ""
        self._save_database()
        logger.info(f"✅ [USER UNBANNED] Admin unbanned Chat ID: {cid} ({u.get('username')})")
        return True, f"✅ *[USER UNBANNED SUCCESSFULLY]*\n\n👤 *អ្នកប្រើប្រាស់ ៖* `{u.get('full_name')}` ({u.get('username')})\n🆔 *Chat ID ៖* `{cid}`\nSTATUS: `Active`"

    def set_user_role(self, query: str, role: str) -> Tuple[bool, str]:
        """Modifies user role (admin, vip, moderator, subscriber)."""
        valid_roles = ["admin", "vip", "moderator", "subscriber"]
        role = role.lower().strip()
        if role not in valid_roles:
            return False, f"⚠️ Role មិនត្រឹមត្រូវឡើយ! (សូមជ្រើសរើសពី ៖ `admin`, `vip`, `moderator`, `subscriber`)"

        u = self.find_user(query)
        if not u:
            return False, f"⚠️ រកមិនឃើញអ្នកប្រើប្រាស់ `{query}` ក្នុងប្រព័ន្ធឡើយ!"

        cid = u["chat_id"]
        u["role"] = role
        self._save_database()
        logger.info(f"👑 [ROLE UPDATED] Chat ID: {cid} -> Role: {role}")
        return True, f"👑 *[USER ROLE UPDATED]*\n\n👤 *អ្នកប្រើប្រាស់ ៖* `{u.get('full_name')}` ({u.get('username')})\n🆔 *Chat ID ៖* `{cid}`\n✨ *Role ថ្មី ៖* `{role.upper()}`"

    def get_users_list(self, page: int = 1, page_size: int = 8) -> Tuple[str, List[List[dict]]]:
        """Generates formatted users list for Admin view with inline pagination."""
        if not self.users:
            return "👥 *បញ្ជីអ្នកប្រើប្រាស់ទទេ (No Registered Users Yet).*", []

        all_users = list(self.users.values())
        all_users.sort(key=lambda x: x.get("last_active", ""), reverse=True)

        total_users = len(all_users)
        total_pages = max(1, (total_users + page_size - 1) // page_size)
        page = max(1, min(page, total_pages))

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        page_users = all_users[start_idx:end_idx]

        report = f"👥 *បញ្ជីអ្នកប្រើប្រាស់ប្រព័ន្ធ (USER MANAGEMENT DASHBOARD) ៖*\n"
        report += f"📊 *សរុប ៖* `{total_users}` Users | *ទំព័រ ៖* `{page}/{total_pages}`\n\n"

        for idx, u in enumerate(page_users, start_idx + 1):
            role_icon = "👑 ADMIN" if u.get("role") == "admin" else ("🌟 VIP" if u.get("role") == "vip" else ("🛡️ MOD" if u.get("role") == "moderator" else "👤 SUB"))
            status_icon = "🚫 BANNED" if u.get("status") == "banned" else "✅ ACTIVE"
            report += (
                f"*{idx}. {u.get('full_name')}* ({u.get('username')})\n"
                f"  └ 🆔 `{u.get('chat_id')}` | {role_icon} | {status_icon}\n"
                f"  └ 💬 សំណួរ ៖ `{u.get('total_queries', 0)}` | 🕒 ចូលចុងក្រោយ ៖ `{u.get('last_active')}`\n\n"
            )

        report += (
            "----------------------------------\n"
            "💡 *ពាក្យបញ្ជា Admin រៀបចំអ្នកប្រើប្រាស់ ៖*\n"
            "• `/user_info <Chat_ID/Username>` - មើលប្រវត្តិលម្អិត\n"
            "• `/ban_user <Chat_ID/Username> <មូលហេតុ>` - បិទសិទ្ធិប្រើប្រាស់\n"
            "• `/unban_user <Chat_ID/Username>` - ដោះបម្រាម\n"
            "• `/set_role <Chat_ID/Username> <vip/subscriber/admin>` - កំណត់សិទ្ធិ"
        )

        pagination_btns = []
        nav_row = []
        if page > 1:
            nav_row.append({"text": "⬅️ ថយក្រោយ", "callback_data": f"usr_page_{page-1}"})
        if page < total_pages:
            nav_row.append({"text": "បន្ទាប់ ➡️", "callback_data": f"usr_page_{page+1}"})
        if nav_row:
            pagination_btns.append(nav_row)

        return report, pagination_btns

    def get_user_detail_info(self, query: str) -> str:
        """Generates detailed profile report for a specific user."""
        u = self.find_user(query)
        if not u:
            return f"⚠️ រកមិនឃើញអ្នកប្រើប្រាស់ `{query}` ក្នុងប្រព័ន្ធឡើយ!"

        role_str = u.get("role", "subscriber").upper()
        status_str = u.get("status", "active").upper()

        return (
            f"👤 *[ព័ត៌មានលម្អិតអ្នកប្រើប្រាស់ - USER PROFILE]*\n\n"
            f"• *ឈ្មោះពេញ ៖* `{u.get('full_name')}`\n"
            f"• *Username ៖* `{u.get('username')}`\n"
            f"• *Telegram Chat ID ៖* `{u.get('chat_id')}`\n"
            f"• *សិទ្ធិប្រើប្រាស់ (Role) ៖* `{role_str}`\n"
            f"• *ស្ថានភាព (Status) ៖* `{status_str}`\n"
            f"• *កាលបរិច្ឆេទចុះឈ្មោះ ៖* `{u.get('joined_at')}`\n"
            f"• *សកម្មភាពចុងក្រោយ ៖* `{u.get('last_active')}`\n"
            f"• *ចំនួនសំណួរដេញដោលសរុប ៖* `{u.get('total_queries', 0)}` សារ\n"
            f"• *មូលហេតុបម្រាម ៖* `{u.get('ban_reason') or 'គ្មាន'}`\n\n"
            "----------------------------------\n"
            "💡 *សកម្មភាព Admin ៖*\n"
            f"• `/ban_user {u.get('chat_id')} <មូលហេតុ>`\n"
            f"• `/unban_user {u.get('chat_id')}`\n"
            f"• `/set_role {u.get('chat_id')} vip`"
        )

    def get_telemetry_stats(self) -> str:
        """Returns overall User Telemetry Statistics."""
        total = len(self.users)
        banned = sum(1 for u in self.users.values() if u.get("status") == "banned")
        active = total - banned
        vips = sum(1 for u in self.users.values() if u.get("role") == "vip")
        admins = sum(1 for u in self.users.values() if u.get("role") == "admin")
        total_queries = sum(u.get("total_queries", 0) for u in self.users.values())

        return (
            f"📊 *[របាយការណ៍ស្ថិតិអ្នកប្រើប្រាស់ - USER TELEMETRY DASHBOARD]*\n\n"
            f"👥 *អ្នកប្រើប្រាស់សរុប ៖* `{total}` Users\n"
            f"✅ *Active Subscribers ៖* `{active}` Users\n"
            f"🌟 *VIP Subscribers ៖* `{vips}` Users\n"
            f"👑 *Admin System ៖* `{admins}` Users\n"
            f"🚫 *Banned Suspensions ៖* `{banned}` Users\n"
            f"💬 *សំណួរឆ្លើយតបសរុប ៖* `{total_queries}` Messages Served\n\n"
            f"⏱️ *ធ្វើបច្ចុប្បន្នភាព ៖* `{time.strftime('%Y-%m-%d %H:%M:%S')}`"
        )

# Global Instance
user_manager = UserManager()
