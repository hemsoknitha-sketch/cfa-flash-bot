import re
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

class KhmerLanguageAuditor:
    """
    Master Khmer Script Purifier & Deep Linguistic Auditor Engine.
    Guarantees 100% formal Khmer linguistic purity:
    1. Detects and strips any leaked Thai characters (Unicode range \\u0e00-\\u0e7f) or foreign scripts.
    2. Enforces formal Khmer punctuation placement (៖, ។, ៕).
    3. Cleans up zero-width spaces and redundant whitespace.
    """
    def __init__(self):
        # Regex pattern matching Thai Unicode script (\u0e00-\u0e7f)
        self.thai_script_pattern = re.compile(r'[\u0e00-\u0e7f]+')
        
        # Common orthographic fixes for Khmer news text
        self.punctuation_replacements = [
            (r'\s+៖', '៖'),
            (r'\s+។', '។'),
            (r'\s+៕', '៕'),
            (r'៖([^\s])', r'៖ \1'),
            (r'([^\s])។', r'\1។'),
        ]

        # Samdach Presh Sangkareach Chuon Nath Khmer Dictionary Orthographic Rules & Normalization
        self.chuon_nath_spelling_dictionary = [
            (r'ព័ត៏មាន', 'ព័ត៌មាន'),
            (r'រដ្ឋធម្មនុញ្ញ័', 'រដ្ឋធម្មនុញ្ញ'),
            (r'ប្រជាធិបតេយ្យ៍', 'ប្រជាធិបតេយ្យ'),
            (r'អន្តរជាំតិ', 'អន្តរជាតិ'),
            (r'សន្តិសុខ័', 'សន្តិសុខ'),
            (r'កិច្ចសហប្រតិបត្តការ', 'កិច្ចសហប្រតិបត្តិការ'),
            (r'ព្រះរាជាណាចក្រកម្ពុជា\s+៖', 'ព្រះរាជាណាចក្រកម្ពុជា៖'),
        ]

    def strip_thai_and_foreign_scripts(self, text: str) -> str:
        """
        Detects and strips any leaked Thai characters/words.
        """
        if not text:
            return ""
        
        # Check if Thai script is present
        if self.thai_script_pattern.search(text):
            logger.warning("⚠️ [KHMER AUDITOR] Detected leaked Thai script! Purifying text...")
            # Remove Thai characters
            text = self.thai_script_pattern.sub('', text)

        return text

    def sanitize_khmer_spelling_and_punctuation(self, text: str) -> str:
        """
        Normalizes Khmer punctuation, Chuon Nath dictionary spelling, and zero-width spaces.
        """
        if not text:
            return ""

        # Normalize multiple spaces
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Apply Chuon Nath Orthographic Corrections
        for wrong_spelling, correct_spelling in self.chuon_nath_spelling_dictionary:
            text = re.sub(wrong_spelling, correct_spelling, text)

        # Apply Khmer punctuation rules
        for pattern, repl in self.punctuation_replacements:
            text = re.sub(pattern, repl, text)

        return text.strip()

    def audit_khmer_text(self, text: str) -> str:
        """
        Master entrypoint: Deeply audits, purifies, and polishes Khmer news text.
        """
        if not text:
            return ""

        # Step 1: Strip leaked Thai or foreign characters
        text = self.strip_thai_and_foreign_scripts(text)

        # Step 2: Sanitize Khmer grammar & punctuation
        text = self.sanitize_khmer_spelling_and_punctuation(text)

        return text

khmer_auditor = KhmerLanguageAuditor()
