import requests

def summarize_with_qwen(text: str) -> str:
    """Summarize news text using local Ollama Qwen 2.5 3B."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5:3b",
        "prompt": f"សង្ខេបព័ត៌មានខាងក្រោមឲ្យខ្លី និងច្បាស់លាស់ជាភាសាខ្មែរ៖\n\n{text}",
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "គ្មានចម្លើយ")
        else:
            return f"Error: HTTP {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Error: {e} (សូមពិនិត្យមើលថាតើ Ollama ត្រូវបានបើកឬនៅ)"

if __name__ == "__main__":
    sample_text = "ធនាគារកណ្តាលអាមេរិក (Fed) បានប្រកាសកាត់បន្ថយអត្រាការប្រាក់គោលចំនួន ០.៥០% ក្នុងកិច្ចប្រជុំបន្ទាន់មួយ ដើម្បីជួយសម្រួលដល់សាច់ប្រាក់ងាយស្រួលក្នុងទីផ្សារ និងពង្រឹងស្ថិរភាពសេដ្ឋកិច្ច។"
    print("Testing Qwen 2.5 3B News Summarization:\n")
    print(f"Original Text: {sample_text}\n")
    summary = summarize_with_qwen(sample_text)
    print(f"Qwen Summary:\n{summary}")
