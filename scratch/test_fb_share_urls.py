import sys
import os

sys.path.insert(0, os.path.abspath("."))
sys.stdout.reconfigure(encoding='utf-8')

from facebook_url_extractor import fb_url_extractor

test_urls = [
    "https://www.facebook.com/share/p/1B1xyz123/",
    "https://www.facebook.com/share/v/1B1xyz123/",
    "https://www.facebook.com/share/r/1B1xyz123/",
    "https://m.facebook.com/story.php?story_fbid=123456789&id=100000",
    "https://www.facebook.com/permalink.php?story_fbid=123456789&id=100000",
    "https://www.facebook.com/100000/posts/123456789/?comment_id=987654321",
    "https://fb.watch/xyz123456/",
    "https://fb.me/xyz123456/"
]

print("=== UNIVERSAL FACEBOOK URL PATTERN TEST ===")
for url in test_urls:
    is_valid = fb_url_extractor.is_facebook_url(url)
    print(f"URL: {url} | Valid: {is_valid}")
