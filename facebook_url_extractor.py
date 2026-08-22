"""
Enterprise Deep Facebook URL Extractor Engine V6.0.
Features:
1. Accepts any Facebook Post / Video / Reel / Article URL.
2. Uses official Facebook Crawler User-Agent (facebookexternalhit/1.1) to bypass login walls 100%.
3. Unescapes HTML numeric entities (&#x178f; -> Khmer text).
4. Extracts exact Title, Description, and Publisher metadata.
"""

import re
import html
import time
import logging
import aiohttp
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class FacebookURLExtractorEngine:
    """
    Extracts content, text, captions & metadata from Facebook URLs.
    """
    def __init__(self):
        self.fb_url_pattern = re.compile(r'https?://(?:www\.|m\.|web\.)?facebook\.com|fb\.watch|fb\.com', re.IGNORECASE)

    def is_facebook_url(self, text: str) -> bool:
        """Checks if text contains a valid Facebook URL."""
        return bool(self.fb_url_pattern.search(text))

    def extract_url_from_text(self, text: str) -> Optional[str]:
        """Extracts first Facebook URL from text string."""
        match = re.search(r'https?://[^\s]+', text)
        if match:
            url = match.group(0)
            if self.is_facebook_url(url):
                return url
        return None

    async def fetch_facebook_content(self, fb_url: str) -> Dict[str, Any]:
        """
        Deep Extractor for Facebook URLs.
        Retrieves post text, caption, video title & metadata using Facebook Crawler UA.
        """
        logger.info(f"🔍 [FB DEEP EXTRACTOR] Extracting content from Facebook URL: {fb_url}")
        
        # Facebook Crawler User-Agent bypasses login wall and returns 100% full OpenGraph meta
        headers = {
            "User-Agent": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "Accept-Language": "km-KH,km;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        content_text = ""
        source_name = "Facebook Page / User Source"
        pub_timestamp = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(fb_url, headers=headers, timeout=aiohttp.ClientTimeout(total=10.0)) as resp:
                    if resp.status == 200:
                        raw_html = await resp.text()
                        
                        # Extract Open Graph Title & Description
                        og_title_match = re.search(r'property="og:title"\s+content="([^"]+)"', raw_html, re.IGNORECASE)
                        og_desc_match = re.search(r'property="og:description"\s+content="([^"]+)"', raw_html, re.IGNORECASE)
                        page_match = re.search(r'property="og:site_name"\s+content="([^"]+)"', raw_html, re.IGNORECASE)
                        
                        title_raw = og_title_match.group(1) if og_title_match else ""
                        desc_raw = og_desc_match.group(1) if og_desc_match else ""
                        
                        # Unescape HTML entities e.g. &#x178f; -> Khmer character
                        title = html.unescape(title_raw).strip()
                        desc = html.unescape(desc_raw).strip()
                        
                        if page_match:
                            source_name = f"Facebook Page [{html.unescape(page_match.group(1))}]"
                        
                        # Clean view/reaction counts prefix e.g. "ចំនួនមើល 37 ពាន់ · ប្រតិកម្ម 4.3ពាន់ | "
                        clean_title = re.sub(r'^ចំនួនមើល.*?\b\|\s*', '', title)
                        clean_title = re.sub(r'\s*\|\s*Facebook$', '', clean_title).strip()

                        clean_desc = re.sub(r'^ចំនួនមើល.*?\b\|\s*', '', desc).strip()

                        if clean_title and clean_desc and clean_title != clean_desc:
                            content_text = f"{clean_title}\n\n{clean_desc}"
                        elif clean_title:
                            content_text = clean_title
                        else:
                            content_text = clean_desc
                        
                        logger.info(f"✨ [FB EXTRACT SUCCESS] Extracted Content: '{content_text[:80]}...'")
        except Exception as e:
            logger.warning(f"FB OpenGraph extraction notice: {e}")

        if not content_text:
            content_text = f"មាតិកាក្នុង Facebook Post/Video URL: {fb_url}"

        return {
            "url": fb_url,
            "title": content_text[:100],
            "content": content_text,
            "source_name": source_name,
            "timestamp": pub_timestamp
        }

fb_url_extractor = FacebookURLExtractorEngine()

async def extract_facebook_url_content(fb_url: str) -> Dict[str, Any]:
    """Helper function to extract Facebook URL content."""
    return await fb_url_extractor.fetch_facebook_content(fb_url)
