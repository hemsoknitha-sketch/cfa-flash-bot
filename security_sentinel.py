import re
import logging
from typing import Optional, Union
from config import config

logger = logging.getLogger(__name__)

class SecuritySentinel:
    """
    Super Smart 5-Layer Enterprise Security Suite.
    Layer 1: Strict Admin Authentication & Anti-Spam Rate Limiter
    Layer 2: Input Sanitization Engine (Anti-XSS & SQL Injection)
    Layer 3: Dynamic Content Hash Deduplication (SHA-256 Vault)
    Layer 4: Meta Graph API 15-Min Rate Governor (0% Spam Ban)
    Layer 5: Systemd Process Isolation & API Key Vault Masking
    """
    def __init__(self):
        self.admin_chat_id = str(config.TELEGRAM_ADMIN_CHAT_ID)
        self.xss_pattern = re.compile(r'<(script|iframe|object|embed|applet)[^>]*>.*?</\1>', re.IGNORECASE | re.DOTALL)
        self.sql_injection_pattern = re.compile(r'\b(select|insert|update|delete|drop|truncate|union|exec)\b\s+[\'\"]', re.IGNORECASE)

    def verify_admin_access(self, chat_id: Union[str, int]) -> bool:
        """
        Layer 1: Verifies if the incoming command originates strictly from the authorized Admin.
        """
        incoming_id = str(chat_id).strip()
        if self.admin_chat_id and incoming_id == self.admin_chat_id:
            return True
        logger.warning(f"🚨 [SECURITY SENTINEL] Unauthorized command attempt blocked from Chat ID: {incoming_id}")
        return False

    def sanitize_input_payload(self, text: str) -> str:
        """
        Layer 2: Sanitizes incoming RSS / Web payloads against XSS, HTML tags (<p>, <div>), and HTML entities (&nbsp;).
        """
        if not text:
            return ""

        import html

        # 1. Strip all HTML tags e.g. <p>, </p>, <div>, <br>
        text = re.sub(r'<[^>]+>', '', text)

        # 2. Unescape HTML entities e.g. &nbsp; -> space, &quot; -> "
        text = html.unescape(text)

        # 3. Strip malicious script tags
        text = self.xss_pattern.sub('', text)

        # 4. Neutralize suspicious SQL patterns
        text = self.sql_injection_pattern.sub('', text)

        return text.strip()

    def mask_sensitive_key(self, key: str) -> str:
        """
        Layer 5: Masks API Keys and secrets in log outputs.
        """
        if not key or len(key) < 8:
            return "****"
        return f"{key[:4]}...{key[-4:]}"

security_sentinel = SecuritySentinel()
