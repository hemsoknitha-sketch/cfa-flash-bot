import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from facebook_url_extractor import extract_facebook_url_content

async def main():
    url = "https://www.facebook.com/reel/2532972943814116"
    res = await extract_facebook_url_content(url)
    print("=== EXTRACTED RESULT ===")
    print("Title:", res.get("title"))
    print("Content:", res.get("content"))
    print("Source:", res.get("source_name"))

if __name__ == "__main__":
    asyncio.run(main())
