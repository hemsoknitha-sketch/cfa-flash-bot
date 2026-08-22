import os
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class HuggingFacePolymathAI:
    """
    Super Smart Polymath AI Engine powered by fine-tuned model:
    hemsinath/cfa-flash-bot on Hugging Face Inference API.
    Unsloth Prompt Format:
    Below is an instruction that describes a task...
    ### Instruction:
    {prompt_text}
    ### Input:

    ### Response:
    """
    def __init__(
        self,
        model_id: str = "hemsinath/cfa-flash-bot",
        token: Optional[str] = None
    ):
        self.model_id = os.getenv("HF_MODEL_ID", model_id)
        self.token = token or os.getenv("HF_API_TOKEN", "")
        self.urls = [
            f"https://api-inference.huggingface.co/models/{self.model_id}",
            f"https://router.huggingface.co/hf-inference/models/{self.model_id}",
            f"https://router.huggingface.co/models/{self.model_id}"
        ]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def ask_polymath_ai(self, prompt_text: str, max_tokens: int = 512, temperature: float = 0.3) -> str:
        """Queries Hugging Face Fine-Tuned CFA Flash Bot model."""
        formatted_prompt = (
            "Below is an instruction that describes a task...\n"
            "### Instruction:\n"
            f"{prompt_text}\n"
            "### Input:\n\n"
            "### Response:\n"
        )
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False
            }
        }

        for url in self.urls:
            try:
                response = requests.post(url, headers=self.headers, json=payload, timeout=6)
                if response.status_code == 200:
                    res_json = response.json()
                    if isinstance(res_json, list) and len(res_json) > 0:
                        text = res_json[0].get("generated_text", "").strip()
                        if text:
                            return text
                    elif isinstance(res_json, dict) and "generated_text" in res_json:
                        return res_json["generated_text"].strip()
            except Exception as e:
                logger.warning(f"Hugging Face endpoint {url} exception: {e}")

        return f"❌ បញ្ហាការតភ្ជាប់ Hugging Face API (Model: {self.model_id})"

# Global Instance
hf_polymath_ai = HuggingFacePolymathAI()
