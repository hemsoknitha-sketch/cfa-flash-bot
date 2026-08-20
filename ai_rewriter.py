import asyncio
import json
import logging
from typing import Optional
from pydantic import BaseModel, Field
from config import config

logger = logging.getLogger(__name__)

class ProcessedNewsArticle(BaseModel):
    original_id: str
    credibility_score: float = Field(..., description="0 to 100 confidence score")
    is_unverified_leak: bool = False
    status_label: str = Field(..., description="[VERIFIED FLASH NEWS] or [UNVERIFIED MARKET LEAK]")
    khmer_headline: str = Field(..., description="Official headline in professional Khmer")
    khmer_body: str = Field(..., description="Detailed body text in Khmer journalistic style")
    impact_analysis: str = Field(..., description="Brief impact analysis on market/economy in Khmer")
    formatted_telegram_post: str = Field(..., description="Complete ready-to-publish Telegram Markdown post")

SYSTEM_PROMPT = """
You are the Chief AI Editor for Super VIP Flash News.
Your mission is to evaluate incoming breaking news, assign a credibility score (0-100%), and rewrite it into high-impact, professional Khmer journalism.

CRITICAL RULES FOR LEAKS & UNVERIFIED NEWS:
1. Evaluate source authority and cross-verification evidence.
2. If source tier is 3 or text indicates unconfirmed rumors, credibility_score MUST be between 50-75% and set is_unverified_leak = true.
3. If credibility_score >= 85%, status_label = "[VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ]".
4. If credibility_score is 65-84%, status_label = "[UNVERIFIED MARKET LEAK - ព័ត៌មានបែកធ្លាយមិនទាន់ផ្លូវការ ⚠️]".
5. Write strictly in official Khmer journalistic tone.
6. Provide a concise bullet point impact analysis (ផលប៉ះពាល់).

Respond ONLY in valid JSON matching this schema:
{
  "credibility_score": float,
  "is_unverified_leak": boolean,
  "status_label": "string",
  "khmer_headline": "string",
  "khmer_body": "string",
  "impact_analysis": "string"
}
"""

class SuperBrainAIRewriter:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.client = None
        if self.api_key and self.api_key.strip() not in ("your_gemini_api_key_here", "MOCK_GEMINI_API_KEY", ""):
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("Gemini AI Client initialized successfully.")
            except Exception as e:
                logger.warning(f"Could not initialize Google GenAI SDK: {e}. Falling back to Rule-based AI Engine.")

    def process_news(self, raw_id: str, title: str, content: str, source: str, source_tier: int, is_unverified: bool) -> ProcessedNewsArticle:
        """Process raw news using Gemini API, Ollama (Qwen 2.5 3B), or Rule-based Engine."""

        # Option A: Local Ollama (Qwen 2.5 3B) if enabled
        if config.USE_LOCAL_OLLAMA:
            try:
                return self._process_with_ollama(raw_id, title, content, source, source_tier, is_unverified)
            except Exception as e:
                logger.error(f"Local Ollama API call failed: {e}. Switching to Cloud/Rule fallback.")

        # Option B: Cloud Google Gemini API
        if self.client:
            try:
                prompt = f"Source: {source} (Tier {source_tier})\nIs Unverified Flag: {is_unverified}\nTitle: {title}\nContent: {content}"
                response = self.client.models.generate_content(
                    model=config.GEMINI_MODEL,
                    contents=SYSTEM_PROMPT + "\n\nRaw News Input:\n" + prompt,
                )
                data = json.loads(response.text)
                cred_score = float(data.get("credibility_score", 70.0))
                is_leak = data.get("is_unverified_leak", is_unverified)
                status_label = data.get("status_label", "[FLASH NEWS]")
                headline = data.get("khmer_headline", title)
                body = data.get("khmer_body", content)
                impact = data.get("impact_analysis", "គ្មានការវិភាគ")

                formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)

                return ProcessedNewsArticle(
                    original_id=raw_id,
                    credibility_score=cred_score,
                    is_unverified_leak=is_leak,
                    status_label=status_label,
                    khmer_headline=headline,
                    khmer_body=body,
                    impact_analysis=impact,
                    formatted_telegram_post=formatted_post
                )
            except Exception as e:
                logger.error(f"Gemini API call failed: {e}. Switching to Rule-based AI Fallback engine.")

        # Option C: Intelligent Rule-Based Fallback Engine
        return self._rule_based_fallback(raw_id, title, content, source, source_tier, is_unverified)

    def _process_with_ollama(self, raw_id: str, title: str, content: str, source: str, source_tier: int, is_unverified: bool) -> ProcessedNewsArticle:
        """Process raw news using local Ollama (Qwen 2.5 3B)."""
        import requests
        logger.info(f"🤖 Calling Local Ollama ({config.OLLAMA_MODEL}) at {config.OLLAMA_HOST}...")
        prompt = f"{SYSTEM_PROMPT}\n\nRaw Input:\nSource: {source} (Tier {source_tier})\nTitle: {title}\nContent: {content}"
        
        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        resp = requests.post(f"{config.OLLAMA_HOST}/api/generate", json=payload, timeout=30)
        if resp.status_code == 200:
            res_data = resp.json()
            data = json.loads(res_data.get("response", "{}"))
            cred_score = float(data.get("credibility_score", 70.0))
            is_leak = data.get("is_unverified_leak", is_unverified)
            status_label = data.get("status_label", "[FLASH NEWS]")
            headline = data.get("khmer_headline", title)
            body = data.get("khmer_body", content)
            impact = data.get("impact_analysis", "គ្មានការវិភាគ")

            formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)
            return ProcessedNewsArticle(
                original_id=raw_id,
                credibility_score=cred_score,
                is_unverified_leak=is_leak,
                status_label=status_label,
                khmer_headline=headline,
                khmer_body=body,
                impact_analysis=impact,
                formatted_telegram_post=formatted_post
            )
        else:
            raise Exception(f"Ollama returned HTTP status {resp.status_code}: {resp.text}")

    def _rule_based_fallback(self, raw_id: str, title: str, content: str, source: str, source_tier: int, is_unverified: bool) -> ProcessedNewsArticle:
        """Deterministic AI processing fallback for offline/test environments."""
        if source_tier == 1 and not is_unverified:
            cred_score = 92.0
            is_leak = False
            status_label = "⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ"
        else:
            cred_score = 70.0
            is_leak = True
            status_label = "⚠️ UNVERIFIED MARKET LEAK - ព័ត៌មានបែកធ្លាយមិនទាន់ផ្លូវការ"

        # Translation & journalistic formatting engine (Meta NLLB-200 Neural Khmer Translation)
        from translator import nllb_translator, fallback_translate_to_khmer, super_smart_khmer_formatter

        translated_title = nllb_translator.translate_to_khmer(title)
        translated_body = nllb_translator.translate_to_khmer(content)

        if not translated_title.startswith("ព័ត៌មានទាន់ហេតុការណ៍"):
            headline = f"ព័ត៌មានទាន់ហេតុការណ៍៖ {translated_title}"
        else:
            headline = translated_title

        khmer_source = fallback_translate_to_khmer(source) if source and "Super Brain" not in source else "ប្រព័ន្ធខួរក្បាលឆ្លាតវៃ Super Brain"
        body = f"តាមប្រភពព័ត៌មានពី {khmer_source} ៖ {translated_body}"

        impact = (
            "វិភាគច្បាស់លាស់ពីផលប្រយោជន៍នៃព័ត៌មាននេះ៖ ផ្តល់សញ្ញាទីផ្សារសំខាន់សម្រាប់អ្នកវិនិយោគ\n"
            "វិភាគច្បាស់លាស់ពីផលប៉ះពាល់នៃព័ត៌មាននេះ៖ អាចបង្កឱ្យមានការប្រែប្រួលតម្លៃជាបណ្តោះអាសន្នលើទីផ្សារ"
        )

        formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)

        return ProcessedNewsArticle(
            original_id=raw_id,
            credibility_score=cred_score,
            is_unverified_leak=is_leak,
            status_label=status_label,
            khmer_headline=headline,
            khmer_body=body,
            impact_analysis=impact,
            formatted_telegram_post=formatted_post
        )

    def _build_telegram_markdown(self, status: str, headline: str, body: str, impact: str, score: float, source: str, is_leak: bool) -> str:
        from translator import clean_khmer_spaces

        leak_banner = "\n🚨 *បដាព្រមាន៖ ព័ត៌មាននេះមិនទាន់មានការបញ្ជាក់ផ្លូវការនៅឡើយទេ សូមផ្ទៀងផ្ទាត់មុនធ្វើការសម្រេចចិត្តវិនិយោគ។*\n" if is_leak else ""

        headline_clean = clean_khmer_spaces(headline)
        body_clean = clean_khmer_spaces(body)
        impact_clean = clean_khmer_spaces(impact)

        impact_lines = [line.strip() for line in impact_clean.split("\n") if line.strip()]
        formatted_impact = "\n".join([f"• {line}" if not line.startswith("•") else line for line in impact_lines])

        return (
            f"{status}\n\n"
            f"🎯 *{headline_clean}*\n\n"
            f"📝 *ខ្លឹមសារព័ត៌មាន៖*\n{body_clean}\n"
            f"{leak_banner}\n"
            f"📊 *ការវិភាគ៖*\n{formatted_impact}\n\n"
            f"🔍 *ព័ត៌មាននេះនាំមកជូនដោយ៖*\n"
            f"• កម្រិតភាពជឿជាក់ (Credibility Score): `{score}%`\n"
            f"• ប្រភពដើម: `{source}`\n"
            f"• ផលិតដោយ៖ *សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA*\n"
            f"• Telegram: *CFA Flash News | @CFAflashBot*"
        )

    async def generate_banner_image(self, headline: str) -> str:
        """
        High-Impact AI Image & Graphic Banner Rendering Engine.
        Uses Playwright Chromium Engine for 100% perfect Khmer typography OpenType shaping.
        """
        import os
        logger.info(f"🎨 [AI IMAGE ENGINE] Rendering High-Impact Banner Image for: '{headline}'...")
        image_filename = f"banner_{abs(hash(headline)) % 10000}.jpg"
        clean_headline = headline.replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").strip()

        # Method 1: High-Definition Playwright HTML5 HarfBuzz OpenType Engine
        try:
            from playwright.async_api import async_playwright

            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<style>
@import url('https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&family=Moul&family=Outfit:wght@600;800&display=swap');

body {{
    margin: 0;
    padding: 0;
    width: 1200px;
    height: 630px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    font-family: 'Battambang', 'Khmer OS Battambang', sans-serif;
    color: #f8fafc;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 60px;
    border-top: 16px solid #ef4444;
}}

.badge {{
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
    color: white;
    font-family: 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 800;
    padding: 12px 28px;
    border-radius: 50px;
    display: inline-block;
    letter-spacing: 1.5px;
    box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
    width: fit-content;
}}

.category-title {{
    font-family: 'Moul', 'Khmer OS Muol', serif;
    color: #ef4444;
    font-size: 38px;
    margin-top: 30px;
    margin-bottom: 20px;
}}

.news-headline {{
    font-size: 38px;
    line-height: 1.6;
    font-weight: 700;
    color: #f8fafc;
    text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}

.footer {{
    border-top: 2px solid #334155;
    padding-top: 25px;
    font-size: 20px;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.footer-brand {{
    font-weight: 700;
    color: #cbd5e1;
}}
</style>
</head>
<body>
    <div>
        <div class='badge'>⚡ SUPER VIP FLASH NEWS</div>
        <div class='category-title'>ព័ត៌មានទាន់ហេតុការណ៍</div>
        <div class='news-headline'>{clean_headline}</div>
    </div>
    <div class='footer'>
        <span class='footer-brand'>SUPER VIP FLASH NEWS AI SYSTEM</span>
        <span>REAL-TIME FINANCIAL & MARKET FEED</span>
    </div>
</body>
</html>"""

            temp_html_path = os.path.abspath(f"temp_{abs(hash(headline)) % 10000}.html")
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(viewport={"width": 1200, "height": 630})
                await page.goto("file:///" + temp_html_path.replace("\\", "/"))
                await page.screenshot(path=image_filename, type="jpeg", quality=95)
                await browser.close()

            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

            logger.info(f"✨ [AI IMAGE READY] High-Definition Khmer Banner Asset prepared: {image_filename}")
            return image_filename
        except Exception as err:
            logger.warning(f"Playwright HTML rendering fallback: {err}. Switching to PIL fallback.")

        # Method 2: PIL Fallback Engine
        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new('RGB', (1200, 630), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (1200, 16)], fill=(239, 68, 68))
            draw.rectangle([(60, 48), (380, 100)], fill=(239, 68, 68))
            
            font_arial = r'C:\Windows\Fonts\arialbd.ttf'
            font_battambang = r'C:\Windows\Fonts\KhmerOSbattambang.ttf'
            badge_font = ImageFont.truetype(font_arial, 20) if os.path.exists(font_arial) else ImageFont.load_default()
            draw.text((78, 64), "SUPER VIP FLASH NEWS", fill=(255, 255, 255), font=badge_font)

            body_font = ImageFont.truetype(font_battambang, 28) if os.path.exists(font_battambang) else badge_font
            draw.text((60, 150), clean_headline[:60], fill=(248, 250, 252), font=body_font)
            img.save(image_filename, format="JPEG", quality=95)
        except Exception as e:
            logger.warning(f"PIL Image generation fallback: {e}")
            if not os.path.exists(image_filename):
                valid_jpeg_bytes = bytes.fromhex("ffd8ffe000104a46494600010101006000600000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333430ffc0000b080001000101011100ffc4001f0000010501010101010100000000000000000102030405060708090a0bffda0008010100003f00d2cf00ffd9")
                with open(image_filename, "wb") as f:
                    f.write(valid_jpeg_bytes)

        logger.info(f"✨ [AI IMAGE READY] Asset prepared successfully: {image_filename}")
        return image_filename
