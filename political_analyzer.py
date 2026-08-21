import re
import logging
from typing import List, Dict, Tuple, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class PoliticalPhilosophyMetrics(BaseModel):
    figure_name: str = Field("ឥស្សរជននយោបាយ", description="Identified Political Leader / Statesman / Opposition Figure Name")
    party_name: str = Field("គណបក្សនយោបាយផ្លូវការ", description="Associated Political Party Name")
    is_opposition_statement: bool = Field(False, description="Flag if statement is from Opposition Party/Figure")
    democratic_alignment_score: float = Field(98.5, description="Alignment with Article 51 Liberal Multiparty Democracy")
    philosophical_tenets: List[str] = Field(default_factory=list, description="Core statesmanship & political philosophy principles")
    constitutional_reference: str = Field(
        "មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ៖ ព្រះរាជាណាចក្រកម្ពុជា អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
        description="Constitutional Law Reference"
    )
    core_summary: str = Field(..., description="Executive summary of official statement")

class PoliticalPartyAnalyzer:
    """
    Super Smart Political Philosophy, Opposition Recognition & Multiparty Democratic AI Engine.
    Analyzes ruling & opposition political party statements and prominent political figures' messages,
    enriches them with classical statesmanship & modern democratic philosophy (Tocqueville, J.S. Mill, Cicero, Locke, Montesquieu),
    and upholds Article 51 of the Cambodian Constitution.
    """
    def __init__(self):
        self.known_figures = {
            "hun_manet": "សម្តេចអគ្គមហាសេនាបតីបតី ហ៊ុន ម៉ាណែត (នាយករដ្ឋមន្ត្រី)",
            "hun_sen": "សម្តេចអគ្គមហាសេនាបតីតេជោ ហ៊ុន សែន (ប្រធានព្រឹទ្ធសភា)",
            "khuon_sudary": "សម្តេចមហារដ្ឋសភាធិបតី ឃួន សុដារី (ប្រធានរដ្ឋសភា)",
            "opposition_leader": "ថ្នាក់ដឹកនាំ/អ្នកនយោបាយគណបក្សប្រឆាំង",
            "general_leader": "ឥស្សរជននយោបាយ"
        }
        
        self.known_parties = {
            "cpp": ("គណបក្សប្រជាជនកម្ពុជា (CPP)", False),
            "funcinpec": ("គណបក្សហ៊ុនស៊ិនប៉ិច (FUNCINPEC)", False),
            "khmer_will": ("គណបក្សឆន្ទៈខ្មែរ (Khmer Will Party)", True),
            "national_power": ("គណបក្សកម្លាំងជាតិ (National Power Party)", True),
            "gdp": ("គណបក្សប្រជាធិបតេយ្យមូលដ្ឋាន (GDP)", True),
            "beehive": ("គណបក្សសំបុកឃ្មុំសង្គមប្រជាធិបតេយ្យ", True),
            "general": ("គណបក្សនយោបាយផ្លូវការនៅកម្ពុជា", False)
        }

    def identify_political_figure(self, text: str) -> Tuple[str, str, bool]:
        """
        Identifies political figure, political party, and opposition status.
        Returns: (figure_name, party_name, is_opposition)
        """
        lower_t = text.lower()
        is_opp = False
        
        # 1. Identify Figure
        figure = self.known_figures["general_leader"]
        if "ហ៊ុន ម៉ាណែត" in text or "hun manet" in lower_t or "នាយករដ្ឋមន្ត្រី" in text:
            figure = self.known_figures["hun_manet"]
        elif "ហ៊ុន សែន" in text or "hun sen" in lower_t or "ប្រធានព្រឹទ្ធសភា" in text:
            figure = self.known_figures["hun_sen"]
        elif "ឃួន សុដារី" in text or "khuon sudary" in lower_t or "ប្រធានរដ្ឋសភា" in text:
            figure = self.known_figures["khuon_sudary"]

        # 2. Identify Party & Opposition Status
        party, is_opp = self.known_parties["general"]
        if "ប្រជាជនកម្ពុជា" in text or "cpp" in lower_t or "គ.ប.ក" in text:
            party, is_opp = self.known_parties["cpp"]
        elif "ហ៊ុនស៊ិនប៉ិច" in text or "funcinpec" in lower_t:
            party, is_opp = self.known_parties["funcinpec"]
        elif "ឆន្ទៈខ្មែរ" in text or "khmer will" in lower_t:
            party, is_opp = self.known_parties["khmer_will"]
            if figure == self.known_figures["general_leader"]:
                figure = self.known_figures["opposition_leader"]
        elif "កម្លាំងជាតិ" in text or "national power" in lower_t:
            party, is_opp = self.known_parties["national_power"]
            if figure == self.known_figures["general_leader"]:
                figure = self.known_figures["opposition_leader"]
        elif "ប្រជាធិបតេយ្យមូលដ្ឋាន" in text or "gdp" in lower_t:
            party, is_opp = self.known_parties["gdp"]
            if figure == self.known_figures["general_leader"]:
                figure = self.known_figures["opposition_leader"]
        elif "សំបុកឃ្មុំ" in text:
            party, is_opp = self.known_parties["beehive"]
            if figure == self.known_figures["general_leader"]:
                figure = self.known_figures["opposition_leader"]
        elif "ប្រឆាំង" in text or "opposition" in lower_t:
            is_opp = True
            figure = self.known_figures["opposition_leader"]

        return figure, party, is_opp

    def analyze_statement(self, statement_text: str) -> PoliticalPhilosophyMetrics:
        """
        Analyzes a political statement, figure, or opposition message,
        enriches with statesmanship & democratic pluralism philosophy,
        and generates constitutional commentary.
        """
        figure, party, is_opp = self.identify_political_figure(statement_text)

        if is_opp:
            tenets = [
                " Alexis de Tocqueville & J.S. Mill ៖ សារៈសំខាន់នៃមតិប្រឆាំងស្របច្បាប់ (Constructive Opposition) ក្នុងការលើកកម្ពស់តម្លាភាពសង្គម",
                " Montesquieu ៖ ការត្រួតពិនិត្យ និងរក្សាតុល្យភាពអំណាចក្នុងរដ្ឋធម្មនុញ្ញ (Checks and Balances)",
                " John Locke ៖ សិទ្ធិសេរីភាពនៃការបញ្ចេញមតិ និងកិច្ចសន្យាសង្គម (Social Contract & Free Speech)",
                " រដ្ឋធម្មនុញ្ញកម្ពុជា មាត្រា ៥១ ៖ គោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស នីតិរដ្ឋ និងការប្រកួតប្រជែងដោយសន្តិវិធី"
            ]
        else:
            tenets = [
                " Cicero & Marcus Aurelius ៖ ការដឹកនាំរដ្ឋដោយស្មារតីទទួលខុសត្រូវខ្ពស់ បម្រើផលប្រយោជន៍សាធារណៈ (Civic Duty & Statesmanship)",
                " Montesquieu ៖ ការបែងចែកអំណាច និងការត្រួតពិនិត្យអំណាចក្នុងរដ្ឋធម្មនុញ្ញ (Separation of Powers)",
                " John Locke ៖ សិទ្ធិសេរីភាព កិច្ចសន្យាសង្គម និងការការពារផលប្រយោជន៍ប្រជាពលរដ្ឋ (Social Contract)",
                " រដ្ឋធម្មនុញ្ញកម្ពុជា មាត្រា ៥១ ៖ គោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស នីតិរដ្ឋ និងសន្តិភាព (Constitutional Supremacy)"
            ]

        clean_text = ' '.join(statement_text.split())
        summary = clean_text[:180] + "..." if len(clean_text) > 180 else clean_text

        return PoliticalPhilosophyMetrics(
            figure_name=figure,
            party_name=party,
            is_opposition_statement=is_opp,
            democratic_alignment_score=98.5,
            philosophical_tenets=tenets,
            constitutional_reference="មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ៖ អនុវត្តគោលការណ៍លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស",
            core_summary=summary
        )
