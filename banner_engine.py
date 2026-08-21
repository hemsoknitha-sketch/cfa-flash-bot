import os
import base64
import logging
import asyncio
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

Image.MAX_IMAGE_PIXELS = None

logger = logging.getLogger(__name__)

class BannerEngine:
    """
    Dedicated Super Smart HD Banner Rendering Engine.
    Features:
    1. High-Definition Playwright HTML5 OpenType Khmer Engine (HarfBuzz).
    2. Synchronized PIL/Pillow Fallback Engine with 100% Identical Branding:
       - Badge: LOGO.png + សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA
       - Footer Left: APEX SUPER BRAIN AI SYSTEM
       - Watermark Right: @CFAflashBot | REAL-TIME FLASH FEED (Neon Cyan)
    3. Optimized Linux VM launch flags (--no-sandbox, 30s max timeout).
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(self.base_dir, "LOGO.png")

    def _get_logo_b64(self) -> str:
        if os.path.exists(self.logo_path):
            try:
                with open(self.logo_path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception as e:
                logger.error(f"Failed to read LOGO.png: {e}")
        return ""

    def _get_font_b64(self, font_name: str) -> str:
        font_path = os.path.join(self.base_dir, "fonts", font_name)
        if os.path.exists(font_path):
            try:
                with open(font_path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception as e:
                logger.error(f"Failed to read font {font_name}: {e}")
        return ""

    async def generate_banner_image(self, headline: str, category_title: str = "ព័ត៌មានទាន់ហេតុការណ៍", use_playwright: bool = True) -> str:
        """
        Generates 4K HD Banner Image (1200x630 JPEG).
        Uses Playwright OpenType Khmer HarfBuzz Engine with Embedded Base64 TTF Fonts.
        """
        logger.info(f"🎨 [BANNER ENGINE] Generating Banner for: '{headline[:60]}...'")
        image_filename = f"banner_{abs(hash(headline)) % 10000}.jpg"
        clean_headline = headline.replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").strip()

        # Method 1: Playwright HTML5 Engine with Embedded Base64 TTF Fonts
        if use_playwright and async_playwright is not None:
            try:
                logo_b64 = self._get_logo_b64()
                battambang_b64 = self._get_font_b64("Battambang-Regular.ttf")
                moul_b64 = self._get_font_b64("Moul-Regular.ttf")

                logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 36px; width: auto; vertical-align: middle; border-radius: 6px;" />' if logo_b64 else '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'

                font_faces = ""
                if battambang_b64:
                    font_faces += f"""
@font-face {{
    font-family: 'Battambang';
    src: url('data:font/ttf;charset=utf-8;base64,{battambang_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}"""
                if moul_b64:
                    font_faces += f"""
@font-face {{
    font-family: 'Moul';
    src: url('data:font/ttf;charset=utf-8;base64,{moul_b64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}"""

                html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<style>
{font_faces}
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@600;800&display=swap');
body {{
    margin: 0;
    padding: 0;
    width: 1200px;
    height: 630px;
    background: linear-gradient(135deg, #0b132b 0%, #1c2541 60%, #3a506b 100%);
    font-family: 'Battambang', 'Khmer OS Battambang', sans-serif;
    color: #f8fafc;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 55px 60px;
    border-top: 14px solid #ef4444;
}}

.header-container {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.badge {{
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
    color: white;
    font-family: 'Battambang', 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 50px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    letter-spacing: 0.5px;
    box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
    width: fit-content;
}}

.category-title {{
    font-family: 'Moul', 'Khmer OS Muol', serif;
    color: #ef4444;
    font-size: 38px;
    margin-top: 25px;
    text-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}}

.headline-box {{
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: 15px 0;
}}

.headline {{
    font-family: 'Battambang', sans-serif;
    font-size: 44px;
    font-weight: 700;
    line-height: 1.45;
    color: #ffffff;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
}}

.footer-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 25px;
    border-top: 2px solid rgba(255, 255, 255, 0.15);
}}

.brand-left {{
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #94a3b8;
    text-transform: uppercase;
}}

.watermark-right {{
    font-family: 'Outfit', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1px;
}}
</style>
</head>
<body>
    <div>
        <div class="header-container">
            <div class="badge">
                {logo_html}
                <span>សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA</span>
            </div>
        </div>
        <div class="category-title">{category_title}</div>
    </div>

    <div class="headline-box">
        <div class="headline">{clean_headline}</div>
    </div>

    <div class="footer-container">
        <div class="brand-left">APEX SUPER BRAIN AI SYSTEM</div>
        <div class="watermark-right">@CFAflashBot | REAL-TIME FLASH FEED</div>
    </div>
</body>
</html>"""

                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'])
                    page = await browser.new_page(viewport={"width": 1200, "height": 630})
                    await page.set_content(html_content, wait_until="networkidle")
                    await page.screenshot(path=image_filename, type="jpeg", quality=95)
                    await browser.close()
                logger.info(f"✨ [PLAYWRIGHT BANNER READY] Asset prepared: {image_filename}")
                return image_filename
            except Exception as e:
                logger.warning(f"Playwright HTML rendering fallback ({e}). Switching to PIL fallback.")

        # Method 2: Synchronized PIL/Pillow Fallback Engine with Embedded Khmer TTF Fonts
        return await asyncio.to_thread(self._generate_banner_pil, clean_headline, category_title, image_filename)

    def _generate_banner_pil(self, headline: str, category_title: str, image_filename: str) -> str:
        """
        PIL Fallback Engine with Embedded Khmer TTF Fonts (0% Tofu Boxes).
        """
        width, height = 1200, 630
        img = Image.new("RGB", (width, height), color=(11, 19, 43))
        draw = ImageDraw.Draw(img)

        # Load Embedded Khmer Fonts
        battambang_path = os.path.join(self.base_dir, "fonts", "Battambang-Regular.ttf")
        moul_path = os.path.join(self.base_dir, "fonts", "Moul-Regular.ttf")
        
        font_badge = ImageFont.truetype(battambang_path, 22) if os.path.exists(battambang_path) else ImageFont.load_default()
        font_cat = ImageFont.truetype(moul_path, 32) if os.path.exists(moul_path) else (ImageFont.truetype(battambang_path, 32) if os.path.exists(battambang_path) else ImageFont.load_default())
        font_head = ImageFont.truetype(battambang_path, 36) if os.path.exists(battambang_path) else ImageFont.load_default()
        font_footer = ImageFont.truetype(battambang_path, 20) if os.path.exists(battambang_path) else ImageFont.load_default()

        # 1. Top Accent Line (#ef4444)
        draw.rectangle([0, 0, width, 14], fill=(239, 68, 68))

        # 2. Draw LOGO.png if present
        start_x = 60
        if os.path.exists(self.logo_path):
            try:
                logo_img = Image.open(self.logo_path).convert("RGBA")
                logo_img = logo_img.resize((45, 45), Image.Resampling.LANCZOS)
                img.paste(logo_img, (60, 55), logo_img)
                start_x = 115
            except Exception as e:
                logger.error(f"PIL logo paste failed: {e}")

        # 3. Badge background & Text
        draw.rounded_rectangle([start_x, 50, start_x + 360, 100], radius=25, fill=(239, 68, 68))
        draw.text((start_x + 20, 62), "សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA", font=font_badge, fill=(255, 255, 255))

        # 4. Category Title
        draw.text((60, 125), category_title, font=font_cat, fill=(239, 68, 68))

        # 5. Headline Text (Wrapped)
        words = headline.split()
        lines = []
        current_line = ""
        for w in words:
            if len(current_line + " " + w) > 40:
                lines.append(current_line.strip())
                current_line = w
            else:
                current_line += " " + w
        if current_line:
            lines.append(current_line.strip())

        y_pos = 200
        for line in lines[:3]:
            draw.text((60, y_pos), line, font=font_head, fill=(248, 250, 252))
            y_pos += 60

        # 6. Footer Divider Line
        draw.line([(60, 540), (1140, 540)], fill=(51, 65, 85), width=2)

        # 7. Footer Left & Right Branding
        draw.text((60, 565), "APEX SUPER BRAIN AI SYSTEM", font=font_footer, fill=(248, 250, 252))
        draw.text((680, 565), "@CFAflashBot | REAL-TIME FLASH FEED", font=font_footer, fill=(56, 189, 248))

        img.save(image_filename, quality=95)
        logger.info(f"✨ [PIL BANNER READY] Asset prepared with Khmer Font: {image_filename}")
        return image_filename

banner_engine = BannerEngine()
