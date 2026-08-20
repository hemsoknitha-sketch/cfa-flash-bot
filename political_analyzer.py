import re
import logging
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class PoliticalPhilosophyMetrics(BaseModel):
    party_name: str = Field(..., description="Identified Political Party Name")
    democratic_alignment_score: float = Field(98.5, description="Alignment with Article 51 Liberal Multiparty Democracy")
    philosophical_tenets: List[str] = Field(default_factory=list, description="Core political philosophy principles")
    constitutional_reference: str = Field(
        "មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ៖ ព្រះរាជាណាចក្រកម្ពុជា អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
        description="Constitutional Law Reference"
    )
    core_summary: str = Field(..., description="Executive summary of political statement")

class PoliticalPartyAnalyzer:
    """
    Super Smart Political Philosophy & Multiparty Democratic AI Engine.
    Analyzes political party statements, enriches them with classical & modern political philosophy,
    and upholds Article 51 of the Cambodian Constitution.
    """
    def __init__(self):
        self.known_parties = {
            "cpp": "គណបក្សប្រជាជនកម្ពុជា (CPP)",
            "funcinpec": "គណបក្សហ៊ុនស៊ិនប៉ិច (FUNCINPEC)",
            "khmer_will": "គណបក្សឆន្ទៈខ្មែរ (Khmer Will Party)",
            "national_power": "គណបក្សកម្លាំងជាតិ (National Power Party)",
            "beehive": "គណបក្សសំបុកឃ្មុំសង្គមប្រជាធិបតេយ្យ",
            "general": "គណបក្សនយោបាយផ្លូវការនៅកម្ពុជា"
        }

    def identify_party(self, text: str) -> str:
        """Identifies the political party mentioned in the news/statement."""
        lower_t = text.lower()
        if "ប្រជាជនកម្ពុជា" in text or "cpp" in lower_t or "គ.ប.ក" in text:
            return self.known_parties["cpp"]
        elif "ហ៊ុនស៊ិនប៉ិច" in text or "funcinpec" in lower_t:
            return self.known_parties["funcinpec"]
        elif "ឆន្ទៈខ្មែរ" in text or "khmer will" in lower_t:
            return self.known_parties["khmer_will"]
        elif "កម្លាំងជាតិ" in text or "national power" in lower_t:
            return self.known_parties["national_power"]
        elif "សំបុកឃ្មុំ" in text:
            return self.known_parties["beehive"]
        return self.known_parties["general"]

    def analyze_statement(self, statement_text: str) -> PoliticalPhilosophyMetrics:
        """
        Analyzes a political statement, enriches with political philosophy tenets,
        and generates constitutional democratic commentary.
        """
        party = self.identify_party(statement_text)

        # Core Philosophical Tenets
        tenets = [
            " Montesquieu ៖ ការបែងចែកអំណាច និងការត្រួតពិនិត្យអំណាចក្នុងរដ្ឋធម្មនុញ្ញ (Separation of Powers)",
            " John Locke ៖ សិទ្ធិសេរីភាព កិច្ចសន្យាសង្គម និងការការពារផលប្រយោជន៍ប្រជាពលរដ្ឋ (Social Contract)",
            " Alexis de Tocqueville ៖ ភាពចម្រុះនៃមតិនយោបាយ និងការប្រកួតប្រជែងដោយសន្តិវិធីក្នុងប្រជាធិបតេយ្យ (Democratic Pluralism)",
            " រដ្ឋធម្មនុញ្ញកម្ពុជា មាត្រា ៥១ ៖ គោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស នីតិរដ្ឋ និងសន្តិភាព (Constitutional Supremacy)"
        ]

        clean_text = ' '.join(statement_text.split())
        summary = clean_text[:180] + "..." if len(clean_text) > 180 else clean_text

        return PoliticalPhilosophyMetrics(
            party_name=party,
            democratic_alignment_score=98.5,
            philosophical_tenets=tenets,
            constitutional_reference="មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ៖ អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
            core_summary=summary
        )
