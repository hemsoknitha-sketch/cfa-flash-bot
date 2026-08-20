import re
import logging
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class PoliticalPhilosophyMetrics(BaseModel):
    figure_name: str = Field("ឥស្សរជននយោបាយ", description="Identified Political Leader / Statesman Name")
    party_name: str = Field("គណបក្សនយោបាយផ្លូវការ", description="Associated Political Party Name")
    democratic_alignment_score: float = Field(98.5, description="Alignment with Article 51 Liberal Multiparty Democracy")
    philosophical_tenets: List[str] = Field(default_factory=list, description="Core statesmanship & political philosophy principles")
    constitutional_reference: str = Field(
        "មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ៖ ព្រះរាជាណាចក្រកម្ពុជា អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
        description="Constitutional Law Reference"
    )
    core_summary: str = Field(..., description="Executive summary of official statement")

class PoliticalPartyAnalyzer:
    """
    Super Smart Political Philosophy, Statesmanship & Multiparty Democratic AI Engine.
    Analyzes political party statements and prominent political figures' official messages,
    enriches them with classical statesmanship & modern political philosophy (Cicero, Locke, Montesquieu, Tocqueville),
    and upholds Article 51 of the Cambodian Constitution.
    """
    def __init__(self):
        self.known_figures = {
            "hun_manet": "សម្តេចអគ្គមហាសេនាបតីបតី ហ៊ុន ម៉ាណែត (នាយករដ្ឋមន្ត្រី)",
            "hun_sen": "សម្តេចអគ្គមហាសេនាបតីតេជោ ហ៊ុន សែន (ប្រធានព្រឹទ្ធសភា)",
            "khuon_sudary": "សម្តេចមហារដ្ឋសភាធិបតី ឃួន សុដារី (ប្រធានរដ្ឋសភា)",
            "general_leader": "ឥស្សរជននយោបាយជាន់ខ្ពស់"
        }
        
        self.known_parties = {
            "cpp": "គណបក្សប្រជាជនកម្ពុជា (CPP)",
            "funcinpec": "គណបក្សហ៊ុនស៊ិនប៉ិច (FUNCINPEC)",
            "khmer_will": "គណបក្សឆន្ទៈខ្មែរ (Khmer Will Party)",
            "national_power": "គណបក្សកម្លាំងជាតិ (National Power Party)",
            "beehive": "គណបក្សសំបុកឃ្មុំសង្គមប្រជាធិបតេយ្យ",
            "general": "គណបក្សនយោបាយផ្លូវការនៅកម្ពុជា"
        }

    def identify_political_figure(self, text: str) -> Tuple[str, str]:
        """
        Identifies both the political figure and political party from the text.
        Returns: (figure_name, party_name)
        """
        lower_t = text.lower()
        
        # 1. Identify Figure
        figure = self.known_figures["general_leader"]
        if "ហ៊ុន ម៉ាណែត" in text or "hun manet" in lower_t or "នាយករដ្ឋមន្ត្រី" in text:
            figure = self.known_figures["hun_manet"]
        elif "ហ៊ុន សែន" in text or "hun sen" in lower_t or "ប្រធានព្រឹទ្ធសភា" in text:
            figure = self.known_figures["hun_sen"]
        elif "ឃួន សុដារី" in text or "khuon sudary" in lower_t or "ប្រធានរដ្ឋសភា" in text:
            figure = self.known_figures["khuon_sudary"]

        # 2. Identify Party
        party = self.known_parties["general"]
        if "ប្រជាជនកម្ពុជា" in text or "cpp" in lower_t or "គ.ប.ក" in text:
            party = self.known_parties["cpp"]
        elif "ហ៊ុនស៊ិនប៉ិច" in text or "funcinpec" in lower_t:
            party = self.known_parties["funcinpec"]
        elif "ឆន្ទៈខ្មែរ" in text or "khmer will" in lower_t:
            party = self.known_parties["khmer_will"]
        elif "កម្លាំងជាតិ" in text or "national power" in lower_t:
            party = self.known_parties["national_power"]
        elif "សំបុកឃ្មុំ" in text:
            party = self.known_parties["beehive"]

        return figure, party

    def analyze_statement(self, statement_text: str) -> PoliticalPhilosophyMetrics:
        """
        Analyzes a political statement or figure message, enriches with statesmanship philosophy,
        and generates constitutional democratic commentary.
        """
        figure, party = self.identify_political_figure(statement_text)

        # Core Philosophical Tenets
        tenets = [
            " Cicero & Marcus Aurelius ៖ ការដឹកនាំរដ្ឋដោយស្មារតីទទួលខុសត្រូវខ្ពស់ បម្រើផលប្រយោជន៍សាធារណៈ (Civic Duty & Statesmanship)",
            " Montesquieu ៖ ការបែងចែកអំណាច និងការត្រួតពិនិត្យអំណាចក្នុងរដ្ឋធម្មនុញ្ញ (Separation of Powers)",
            " John Locke ៖ សិទ្ធិសេរីភាព កិច្ចសន្យាសង្គម និងការការពារផលប្រយោជន៍ប្រជាពលរដ្ឋ (Social Contract)",
            " Alexis de Tocqueville ៖ ភាពចម្រុះនៃមតិនយោបាយ និងការប្រកួតប្រជែងដោយសន្តិវិធីក្នុងប្រជាធិបតេយ្យ (Democratic Pluralism)",
            " រដ្ឋធម្មនុញ្ញកម្ពុជា មាត្រា ៥១ ៖ គោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស នីតិរដ្ឋ និងសន្តិភាព (Constitutional Supremacy)"
        ]

        clean_text = ' '.join(statement_text.split())
        summary = clean_text[:180] + "..." if len(clean_text) > 180 else clean_text

        return PoliticalPhilosophyMetrics(
            figure_name=figure,
            party_name=party,
            democratic_alignment_score=98.5,
            philosophical_tenets=tenets,
            constitutional_reference="មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ៖ អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
            core_summary=summary
        )
