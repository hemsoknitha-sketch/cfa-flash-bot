"""
====================================================================================================
🏛️ APEX SUPER BRAIN AI — LOCAL HUGGING FACE MODEL DOWNLOADER & CACHE ENGINE
====================================================================================================
Downloads fine-tuned models (e.g. hemsinath/cfa-flash-bot, hemsinath/apex-super-brain-khmer-news) 
directly from Hugging Face Hub and saves weights, tokenizers, and configs into the local project 
'models/' directory for local offline inference.
"""

import os
import sys
import json
import logging
from typing import Optional

sys.stdout.reconfigure(encoding='utf-8')

# Ensure parent directory is in path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("LocalModelDownloader")

from config import config

MODELS_DIR = os.path.dirname(os.path.abspath(__file__))

def download_model_from_hub(
    model_id: Optional[str] = None,
    token: Optional[str] = None
) -> str:
    from huggingface_hub import snapshot_download, login
    
    target_model_id = model_id or config.HF_MODEL_ID or "hemsinath/cfa-flash-bot"
    hf_token = token or config.HF_API_TOKEN or os.getenv("HF_ACCESS_TOKEN", "")

    # Sanitize folder name from model ID (e.g. 'hemsinath/cfa-flash-bot' -> 'hemsinath_cfa-flash-bot')
    safe_folder_name = target_model_id.replace("/", "_")
    local_path = os.path.join(MODELS_DIR, safe_folder_name)
    
    os.makedirs(local_path, exist_ok=True)
    logger.info(f"📥 [LOCAL MODEL DOWNLOADER] Initializing download for '{target_model_id}' into '{local_path}'...")

    if hf_token:
        try:
            login(token=hf_token, write_permission=False)
            logger.info("🔑 Authorized with Hugging Face token.")
        except Exception as e:
            logger.warning(f"Hugging Face login notice: {e}")

    try:
        downloaded_dir = snapshot_download(
            repo_id=target_model_id,
            local_dir=local_path,
            token=hf_token if hf_token else None,
            resume_download=True
        )
        logger.info(f"✨ [SUCCESS] Model '{target_model_id}' successfully saved to local PC: {downloaded_dir}")

        # Update local manifest
        manifest_path = os.path.join(MODELS_DIR, "model_manifest.json")
        manifest_data = {}
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest_data = json.load(f)
            except Exception:
                manifest_data = {}

        manifest_data[target_model_id] = {
            "local_path": local_path,
            "status": "DOWNLOADED_LOCAL",
            "model_id": target_model_id
        }

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)

        return local_path
    except Exception as e:
        logger.error(f"❌ [DOWNLOAD ERROR] Failed to download model '{target_model_id}': {e}")
        return ""

if __name__ == "__main__":
    download_model_from_hub()
