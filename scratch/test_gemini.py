import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from google import genai

print("Testing Gemini Key:", config.GEMINI_API_KEY[:10])
try:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents="Hello, reply with OK"
    )
    print("Gemini Response:", response.text)
except Exception as e:
    print("Gemini Error:", e)
