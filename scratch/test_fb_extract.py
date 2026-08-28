import requests
import re

url = "https://www.facebook.com/reel/2532972943814116"

user_agents = [
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
]

for ua in user_agents:
    print(f"\n--- Testing UA: {ua[:40]}... ---")
    try:
        r = requests.get(url, headers={"User-Agent": ua, "Accept-Language": "km-KH,km;q=0.9,en-US;q=0.8"}, timeout=8)
        print("Status Code:", r.status_code)
        
        # Meta og:title / og:description
        titles = re.findall(r'property="og:title"\s+content="([^"]+)"', r.text)
        descs = re.findall(r'property="og:description"\s+content="([^"]+)"', r.text)
        sites = re.findall(r'property="og:site_name"\s+content="([^"]+)"', r.text)
        
        print("OG Titles:", titles)
        print("OG Descs:", descs)
        print("OG Site:", sites)
        
        if not titles and not descs:
            # Fallback regex for title element or script data
            t_tag = re.findall(r'<title[^>]*>(.*?)</title>', r.text)
            print("Title tag:", t_tag)
    except Exception as e:
        print("Error:", e)
