import os
from dotenv import load_dotenv

# Load environment variables from .env file relative to config.py location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path)

class Config:
    # Telegram settings
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "MOCK_TELEGRAM_BOT_TOKEN")
    TELEGRAM_VIP_CHANNEL_ID: str = os.getenv("TELEGRAM_VIP_CHANNEL_ID", "859271875")
    TELEGRAM_ADMIN_CHAT_ID: str = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "859271875")
    TELEGRAM_MAX_MSG_PER_SEC: int = int(os.getenv("TELEGRAM_MAX_MSG_PER_SEC", "25"))

    # Facebook settings
    FB_PAGE_ID: str = os.getenv("FB_PAGE_ID", "MOCK_FB_PAGE_ID")
    FB_PAGE_ACCESS_TOKEN: str = os.getenv("FB_PAGE_ACCESS_TOKEN", "MOCK_FB_PAGE_ACCESS_TOKEN")

    # Gemini AI settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_API_KEYS_RAW: str = os.getenv("GEMINI_API_KEYS", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    def get_gemini_api_keys(self) -> list:
        """Returns list of Gemini API keys for Multi-Key Pool Round-Robin rotation."""
        keys = []
        if self.GEMINI_API_KEYS_RAW:
            keys.extend([k.strip() for k in self.GEMINI_API_KEYS_RAW.replace("\n", ",").split(",") if k.strip()])
        if self.GEMINI_API_KEY and self.GEMINI_API_KEY not in keys:
            keys.append(self.GEMINI_API_KEY.strip())
        return keys

    # Local Ollama LLM settings (Qwen 2.5 3B)
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    USE_LOCAL_OLLAMA: bool = os.getenv("USE_LOCAL_OLLAMA", "False").lower() in ("true", "1", "t")

    # Hugging Face Fine-Tuned Model settings (hemsinath/cfa-flash-bot)
    HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")
    HF_MODEL_ID: str = os.getenv("HF_MODEL_ID", "hemsinath/cfa-flash-bot")

    # Vector similarity deduplication settings (BAAI/bge-m3 1024-dim or all-MiniLM-L6-v2 384-dim)
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_MODEL: str = os.getenv("QDRANT_MODEL", "all-MiniLM-L6-v2")
    QDRANT_VECTOR_SIZE: int = int(os.getenv("QDRANT_VECTOR_SIZE", "384"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.80"))
    DEDUP_WINDOW_HOURS: int = 1  # 1 hour window for duplicate checking

    # AI Credibility score thresholds
    CREDIBILITY_HIGH_THRESHOLD: float = 85.0
    CREDIBILITY_LEAK_THRESHOLD: float = 65.0

config = Config()
