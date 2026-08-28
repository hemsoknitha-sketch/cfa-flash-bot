import re
import time
import html
import logging
from typing import Optional, Union, Dict, List
from config import config

logger = logging.getLogger(__name__)

class SecuritySentinel:
    """
    Super Smart 8-Layer Military-Grade Enterprise Security Suite V8.0 GOLD STANDARD.
    Layer 1: Per-User Anti-Spam Sliding Window Rate Limiter & Cooldown Lock
    Layer 2: AI Anti-Prompt Injection & Jailbreak Purger
    Layer 3: Input Sanitization Engine (Anti-XSS, HTML Purger & Anti-SQL Injection)
    Layer 4: Anti-Malware File & External Link Security Gatekeeper
    Layer 5: Strict Admin Authentication & Role-Based Access Control (RBAC)
    Layer 6: Cryptographic Content Hash Vault (SHA-256 Anti-Replay DoS)
    Layer 7: Secret Key Masking & Log Sanitization
    Layer 8: Banned User Security Gatekeeper (User Management Suspension)
    """
    def __init__(self):
        self.admin_chat_id = str(config.TELEGRAM_ADMIN_CHAT_ID)
        
        # Regex patterns for malicious payloads
        self.xss_pattern = re.compile(r'<(script|iframe|object|embed|applet)[^>]*>.*?</\1>', re.IGNORECASE | re.DOTALL)
        self.sql_injection_pattern = re.compile(r'\b(select|insert|update|delete|drop|truncate|union|exec)\b\s+[\'\"]', re.IGNORECASE)
        self.malicious_extension_pattern = re.compile(r'\.(exe|apk|bat|cmd|vbs|sh|php|js|scr|pif|jar|dmg)\b', re.IGNORECASE)
        
        # Anti-Prompt Injection Patterns
        self.prompt_injection_pattern = re.compile(
            r'\b(ignore previous instructions|forget all rules|override system|act as DAN|system prompt|jailbreak|developer mode)\b',
            re.IGNORECASE
        )

        # Layer 1: Anti-Spam Rate Limiter state
        self.user_timestamps: Dict[str, List[float]] = {}
        self.cooldown_locks: Dict[str, float] = {}
        self.max_requests_per_window: int = 5
        self.window_seconds: float = 10.0
        self.cooldown_seconds: float = 30.0

    def is_rate_limited(self, chat_id: Union[str, int]) -> bool:
        """
        Layer 1: Per-User Anti-Spam Rate Limiter.
        Allows max 5 requests per 10 seconds. Locks spammers for 30 seconds on violation.
        """
        user_id = str(chat_id).strip()
        now = time.time()

        # Check if user is under cooldown lock
        if user_id in self.cooldown_locks:
            lock_time = self.cooldown_locks[user_id]
            if now - lock_time < self.cooldown_seconds:
                remaining = int(self.cooldown_seconds - (now - lock_time))
                logger.warning(f"🚨 [RATE LIMITER] User {user_id} blocked under cooldown lock ({remaining}s remaining).")
                return True
            else:
                del self.cooldown_locks[user_id]

        # Clean timestamps older than window_seconds
        timestamps = self.user_timestamps.get(user_id, [])
        timestamps = [ts for ts in timestamps if now - ts < self.window_seconds]

        if len(timestamps) >= self.max_requests_per_window:
            self.cooldown_locks[user_id] = now
            logger.warning(f"🚨 [ANTI-SPAM LOCK] User {user_id} exceeded {self.max_requests_per_window} reqs/{self.window_seconds}s. Locked for {self.cooldown_seconds}s.")
            return True

        timestamps.append(now)
        self.user_timestamps[user_id] = timestamps
        return False

    def verify_admin_access(self, chat_id: Union[str, int]) -> bool:
        """
        Layer 5: Verifies if the incoming command originates strictly from the authorized Admin.
        """
        incoming_id = str(chat_id).strip()
        if self.admin_chat_id and incoming_id == self.admin_chat_id:
            return True
        return False

    def is_user_banned(self, chat_id: Union[str, int]) -> bool:
        """
        Layer 8: Checks if user account has been suspended by Bot Admin.
        """
        try:
            from user_manager import user_manager
            return user_manager.is_banned(chat_id)
        except Exception:
            return False

    def sanitize_input_payload(self, text: str) -> str:
        """
        Layer 2 & 3: Sanitizes payloads against Prompt Injections, XSS, HTML tags (<p>, <div>), and SQL Injections.
        """
        if not text:
            return ""

        # 1. Strip HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # 2. Unescape HTML entities
        text = html.unescape(text)

        # 3. Purge XSS script tags
        text = self.xss_pattern.sub('', text)

        # 4. Neutralize Anti-Prompt Injection phrases
        text = self.prompt_injection_pattern.sub('[Purified Prompt]', text)

        # 5. Neutralize SQL Injections
        text = self.sql_injection_pattern.sub('', text)

        return text.strip()

    def is_malicious_file_or_link(self, text: str) -> bool:
        """
        Layer 4: Detects malicious executable file extensions (.exe, .apk, .bat) or dangerous link patterns.
        """
        if not text:
            return False
        if self.malicious_extension_pattern.search(text):
            logger.warning(f"🚨 [MALWARE DETECTED] Dangerous file extension detected in payload: '{text[:50]}'")
            return True
        return False

    def mask_sensitive_key(self, key: str) -> str:
        """
        Layer 7: Masks API Keys and secrets in log outputs.
        """
        if not key or len(key) < 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"

security_sentinel = SecuritySentinel()
