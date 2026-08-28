import os
import re
import json
import urllib.request
from bs4 import BeautifulSoup

def fetch_and_process_constitution():
    url = "https://km.wikipedia.org/wiki/%E1%9E%9A%E1%9E%8A%E1%9F%92%E1%9E%8B%E1%9E%92%E1%9E%98%E1%9F%92%E1%9E%98%E1%9E%93%E1%9E%BB%E1%9E%89%E1%9F%92%E1%9E%89%E1%9E%93%E1%9F%83%E1%9E%96%E1%9F%92%E1%9E%9A%E1%9F%87%E1%9E%9A%E1%9E%B6%E1%9E%87%E1%9E%B6%E1%9E%8E%E1%9E%B6%E1%9E%85%E1%9E%80%E1%9F%92%E1%9E%9A%E1%9E%80%E1%9E%98%E1%9F%92%E1%9E%96%E1%9E%BB%E1%9E%87%E1%9E%B6"
    print("Fetching Cambodian Constitution from official Wikipedia URL...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    html_bytes = urllib.request.urlopen(req).read()
    html_content = html_bytes.decode("utf-8")

    soup = BeautifulSoup(html_content, "html.parser")
    content_div = soup.find("div", {"id": "mw-content-text"})
    
    if not content_div:
        print("Error: Could not locate mw-content-text div.")
        return

    # Extract all elements
    elements = content_div.find_all(["h1", "h2", "h3", "h4", "h5", "p", "div", "li"])

    current_chapter = "បុព្វកថា (Preamble)"
    current_article_no = None
    current_article_text = []

    articles = []

    def commit_article(chap, art_no, text_lines):
        if not art_no or not text_lines:
            return
        full_text = " ".join([t.strip() for t in text_lines if t.strip()])
        # Clean edit links [កែប្រែ]
        full_text = re.sub(r'\[\s*កែប្រែ\s*\]', '', full_text).strip()
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        
        # Derive title/summary
        parts = full_text.split("៖", 1)
        if len(parts) > 1 and len(parts[0]) < 80:
            art_title = parts[0].strip()
            summary_text = parts[1].strip()
        else:
            art_title = f"{art_no} នៃរដ្ឋធម្មនុញ្ញ"
            summary_text = full_text

        # Extract keywords
        kw = [art_no, "រដ្ឋធម្មនុញ្ញ", "ព្រះរាជាណាចក្រកម្ពុជា", "ច្បាប់កំពូល"]
        if "អធិបតេយ្យ" in full_text: kw.append("អធិបតេយ្យភាព")
        if "ប្រជាធិបតេយ្យ" in full_text: kw.append("ប្រជាធិបតេយ្យ")
        if "ព្រះមហាក្សត្រ" in full_text: kw.append("ព្រះមហាក្សត្រ")
        if "សិទ្ធិ" in full_text: kw.append("សិទ្ធិមនុស្ស")
        if "តុលាការ" in full_text: kw.append("អំណាចតុលាការ")
        if "រដ្ឋសភា" in full_text: kw.append("រដ្ឋសភា")
        if "ព្រឹទ្ធសភា" in full_text: kw.append("ព្រឹទ្ធសភា")
        if "រាជរដ្ឋាភិបាល" in full_text: kw.append("រាជរដ្ឋាភិបាល")
        if "ក្រុមប្រឹក្សារដ្ឋធម្មនុញ្ញ" in full_text: kw.append("ក្រុមប្រឹក្សារដ្ឋធម្មនុញ្ញ")

        articles.append({
            "code_name": "រដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា",
            "chapter": chap,
            "article": art_no,
            "category": chap,
            "title": art_title,
            "summary": summary_text,
            "full_text": full_text,
            "keywords": kw
        })

    for el in elements:
        txt = el.get_text().strip()
        if not txt:
            continue
        
        # Check chapter header
        if re.search(r'ជំពូក\s*ទី?\s*[\d\u17e0-\u17e9IXVLCDM]+', txt, re.IGNORECASE):
            # Save previous article
            if current_article_no:
                commit_article(current_chapter, current_article_no, current_article_text)
                current_article_no = None
                current_article_text = []
            clean_chap = re.sub(r'\[\s*កែប្រែ\s*\]', '', txt).strip()
            current_chapter = clean_chap
            continue

        # Check article header e.g. "មាត្រា ១", "មាត្រា ៥១ (ថ្មី)"
        art_match = re.search(r'^(មាត្រា\s*[\d\u17e0-\u17e9]+(?:\s*\([^\)]+\))?)', txt)
        if art_match:
            # Save previous article
            if current_article_no:
                commit_article(current_chapter, current_article_no, current_article_text)
                current_article_text = []
            
            current_article_no = art_match.group(1).strip()
            current_article_text.append(txt)
        elif current_article_no:
            current_article_text.append(txt)

    # Save final article
    if current_article_no:
        commit_article(current_chapter, current_article_no, current_article_text)

    print(f"Successfully processed {len(articles)} Articles of the Cambodian Constitution!")

    # Output paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    constitution_json_path = os.path.join(data_dir, "cambodian_constitution.json")
    with open(constitution_json_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Saved complete Cambodian Constitution JSON to: {constitution_json_path}")

    # Also update/merge with cambodian_national_laws.json
    laws_json_path = os.path.join(data_dir, "cambodian_national_laws.json")
    existing_laws = []
    if os.path.exists(laws_json_path):
        try:
            with open(laws_json_path, "r", encoding="utf-8") as f:
                existing_laws = json.load(f)
        except Exception as e:
            print(f"Notice reading existing laws: {e}")

    # Keep non-constitution laws from existing laws, and append all constitutional articles
    non_const_laws = [l for l in existing_laws if l.get("code_name") != "រដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា"]
    merged_laws = articles + non_const_laws

    with open(laws_json_path, "w", encoding="utf-8") as f:
        json.dump(merged_laws, f, ensure_ascii=False, indent=2)

    print(f"Successfully updated master {laws_json_path} with {len(merged_laws)} total legal provisions!")

if __name__ == "__main__":
    fetch_and_process_constitution()
