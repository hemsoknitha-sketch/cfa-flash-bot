import sys
import os
import asyncio
import aiohttp

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from config import config

async def check_facebook_token():
    page_id = config.FB_PAGE_ID
    access_token = config.FB_PAGE_ACCESS_TOKEN
    
    print("=== FACEBOOK PAGE ACCESS TOKEN DIAGNOSTIC ===")
    print("FB_PAGE_ID:", page_id)
    if not access_token:
        print("❌ ERROR: FB_PAGE_ACCESS_TOKEN is missing or empty in .env!")
        return

    print("FB_PAGE_ACCESS_TOKEN Snippet:", access_token[:15] + "..." + access_token[-10:])
    
    # 1. Test /me endpoint with token
    url = f"https://graph.facebook.com/v19.0/me?fields=id,name,category,link&access_token={access_token}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                status = resp.status
                res_data = await resp.json()
                print(f"Graph API Status Code: {status}")
                if status == 200:
                    print("✅ [TOKEN ACTIVE & VALID 100%]")
                    print(f"📌 Page ID: {res_data.get('id')}")
                    print(f"📌 Page Name: {res_data.get('name')}")
                    print(f"📌 Category: {res_data.get('category')}")
                    print(f"📌 Link: {res_data.get('link')}")
                else:
                    print("❌ [TOKEN INVALID OR EXPIRED]")
                    err = res_data.get("error", {})
                    print(f"Error Message: {err.get('message')}")
                    print(f"Error Type: {err.get('type')}")
                    print(f"Error Code: {err.get('code')}")
                    print(f"Error Subcode: {err.get('error_subcode')}")
        except Exception as e:
            print(f"❌ Network Exception during Facebook Graph API check: {e}")

if __name__ == "__main__":
    asyncio.run(check_facebook_token())
