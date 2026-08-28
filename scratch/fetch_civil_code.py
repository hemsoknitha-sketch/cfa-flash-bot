import urllib.request
import ssl
import sys
import io
import re
import json
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fetch_ccc_civil_code():
    url = 'https://www.ccc.gov.kh/detail_info_kh.php?_txtID=660'
    print(f"Fetching Civil Code page from {url}...")
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'km-KH,km;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.ccc.gov.kh/'
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            html_bytes = resp.read()
            html_str = html_bytes.decode('utf-8', errors='ignore')
            print("Fetched page length:", len(html_str))
            
            soup = BeautifulSoup(html_str, 'html.parser')
            print("Page Title:", soup.title.get_text() if soup.title else "No Title")
            
            # Print body text
            print("--- PRINTING MAIN CONTENT CONTAINERS ---")
            for div in soup.find_all(['div', 'td', 'p', 'span']):
                txt = div.get_text().strip()
                if len(txt) > 50 and 'ទំព័រដើម' not in txt:
                    print(f"[{div.name} class={div.get('class')}] -> {txt[:300]}\n")
            return html_str
    except Exception as e:
        print("Fetch Error:", e)
        return None

if __name__ == "__main__":
    fetch_ccc_civil_code()
