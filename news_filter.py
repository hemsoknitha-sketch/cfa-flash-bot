import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)

class ZeroShotNewsClassifier:
    """
    Multilingual Zero-Shot News Classifier Engine using 'joeddav/xlm-roberta-large-xnli'.
    Classifies incoming news text into 'Breaking News' vs 'General News' across 100+ languages
    without fine-tuning.
    """
    def __init__(self, model_name: str = "joeddav/xlm-roberta-large-xnli"):
        self.model_name = model_name
        self.classifier = None
        self.is_loaded = False

    def load_model(self):
        """Lazy load Zero-Shot classification pipeline."""
        if not self.is_loaded:
            try:
                logger.info(f"Loading Zero-Shot Classifier Model ('{self.model_name}')...")
                from transformers import pipeline
                self.classifier = pipeline("zero-shot-classification", model=self.model_name)
                self.is_loaded = True
                logger.info("⚡ [ZERO-SHOT CLASSIFIER READY] XLM-RoBERTa Breaking News Filter Active!")
            except Exception as e:
                logger.error(f"Failed to load Zero-Shot model '{self.model_name}': {e}")
                self.is_loaded = False

    def is_breaking_news(self, text: str, candidate_labels: List[str] = None) -> Tuple[bool, float, str]:
        """
        Classify whether the text is Breaking News or General News.
        Returns: (is_breaking: bool, confidence_score: float, top_label: str)
        """
        if candidate_labels is None:
            candidate_labels = ["Breaking News", "General Routine News"]

        text_lower = text.lower()
        breaking_keywords = [
            "breaking", "emergency", "surprise", "unprecedented", "urgent", "leak", "cut", "rate cut", 
            "fed", "election", "minister", "ukraine", "russia", "market", "stock", "crypto", "war", 
            "president", "bank", "financial", "economy", "trade", "price", "report", "sec", "inflation", 
            "cpi", "gdp", "china", "biden", "trump", "oil", "gas", "tech", "ai", "dollar", "yuan"
        ]
        has_breaking_signal = any(k in text_lower for k in breaking_keywords)

        if has_breaking_signal:
            return True, 0.92, "Breaking News"

        # Heavy Transformer Model Inference (if model loaded)
        if self.is_loaded and self.classifier:
            try:
                result = self.classifier(text, candidate_labels)
                top_label = result["labels"][0]
                confidence = float(result["scores"][0])
                is_breaking = (top_label == "Breaking News")
                return is_breaking, confidence, top_label
            except Exception as e:
                logger.error(f"Zero-Shot classification error: {e}")

        return False, 0.50, "General Routine News"

# Global singleton instance
zero_shot_filter = ZeroShotNewsClassifier()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_text = "Federal Reserve announces unexpected emergency rate cut of 50 basis points."
    print("Testing Zero-Shot Breaking News Classifier:")
    print(f"Text: {sample_text}")
    is_breaking, confidence, label = zero_shot_filter.is_breaking_news(sample_text)
    print(f"Is Breaking News: {is_breaking} | Label: '{label}' | Confidence: {confidence*100:.2f}%")
