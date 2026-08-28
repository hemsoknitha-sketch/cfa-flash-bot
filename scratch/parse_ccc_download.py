import subprocess
import re
import sys
import io
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_ccc():
    cmd = [
        'curl', '-s', '-k',
        'https://www.ccc.gov.kh/detail_info_kh.php?_txtID=660',
        '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        '-H', 'Accept-Language: km,en;q=0.9'
    ]
    res_bytes = subprocess.check_output(cmd)
    res_str = res_bytes.decode('utf-8', errors='ignore')
    
    print(f"HTML Length: {len(res_str)}")

    soup = BeautifulSoup(res_str, 'html.parser')
    
    # Check middle paragraph or content area
    print("\n--- ALL LINKS IN HTML ---")
    for a in soup.find_all('a'):
        href = a.get('href', '')
        txt = a.get_text().strip()
        print(f"Text: '{txt}' | Href: '{href}'")

    print("\n--- FORM DETAILS ---")
    for form in soup.find_all('form'):
        print("Form Action:", form.get('action'), "Method:", form.get('method'))
        for inp in form.find_all('input'):
            print("  Input:", inp.get('name'), "=", inp.get('value'))

if __name__ == "__main__":
    parse_ccc()
