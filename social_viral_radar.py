"""
Cambodia Facebook Social Debate & Viral Trend Detector V6.0.
Features:
1. Detects hot viral topics, public debates, breaking accidents, scam busts, and social trends across Cambodia.
2. Evaluates Social Viral Index Score (0-100%).
3. Generates Civic Clarity & Fact-Check Summaries to resolve social debate and clarify constitutional rule of law.
"""

import re
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

VIRAL_KEYWORDS = [
    "ផ្ទុះការជជែក", "វែកញ៉ែក", "សមត្ថកិច្ច", "គ្រោះថ្នាក់ចរាចរណ៍",
    "ឆបោកតាមអនឡាញ", "បង្ក្រាប", "ចរាចរណ៍", "សង្គម", "កោតសរសើរ",
    "មតិរិះគន់", "ប្រតិកម្ម", "ប្រជាពលរដ្ឋ", "ស្នងការ", "ស្នងការដ្ឋាន",
    "អន្តរាគមន៍", "ចាត់វិធានការ", "ចាប់ខ្លួន", "អាជ្ញាធរ", "ច្បាប់"
]

class SocialViralRadarEngine:
    """
    Radar Engine for detecting and elevating Cambodian Facebook Viral Trends & Public Debates.
    """
    def __init__(self):
        self.keywords = VIRAL_KEYWORDS

    def analyze_viral_trend(self, title: str, content: str) -> Dict[str, Any]:
        """
        Analyzes title and content to calculate Social Viral Score (0-100%) and detect hot trends.
        """
        combined_text = f"{title} {content}".lower()
        matched_words = [w for w in self.keywords if w in combined_text]
        
        match_count = len(matched_words)
        viral_score = min(100, match_count * 20 + (30 if "ផ្ទុះ" in combined_text or "វែកញ៉ែក" in combined_text else 10))

        is_viral = viral_score >= 50 or match_count >= 2

        topic_label = "ព័ត៌មានទូទៅ"
        if any(w in combined_text for w in ["ចរាចរណ៍", "គ្រោះថ្នាក់"]):
            topic_label = "សុវត្ថិភាពចរាចរណ៍ & សង្គម"
        elif any(w in combined_text for w in ["ឆបោក", "បង្ក្រាប", "សមត្ថកិច្ច", "ស្នងការ"]):
            topic_label = "សន្តិសុខសង្គម & ការបង្ក្រាបបទល្មើស"
        elif any(w in combined_text for w in ["ផ្ទុះ", "វែកញ៉ែក", "រិះគន់", "ប្រតិកម្ម"]):
            topic_label = "ប្រធានបទក្តៅ ផ្ទុះការជជែកក្នុងសង្គម"

        return {
            "is_viral": is_viral,
            "viral_score": viral_score,
            "matched_keywords": matched_words,
            "topic_label": topic_label
        }

viral_radar = SocialViralRadarEngine()
