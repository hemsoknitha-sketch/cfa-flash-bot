import asyncio
import time
import json
import logging
from typing import Optional
from pydantic import BaseModel, Field
from config import config

logger = logging.getLogger(__name__)

class ProcessedNewsArticle(BaseModel):
    original_id: str
    credibility_score: float = Field(..., description="0 to 100 confidence score")
    is_unverified_leak: bool = False
    status_label: str = Field(..., description="[VERIFIED FLASH NEWS] or [UNVERIFIED MARKET LEAK]")
    khmer_headline: str = Field(..., description="Official headline in professional Khmer")
    khmer_body: str = Field(..., description="Detailed body text in Khmer journalistic style")
    impact_analysis: str = Field(..., description="Brief impact analysis on market/economy in Khmer")
    formatted_telegram_post: str = Field(..., description="Complete ready-to-publish Telegram Markdown post")

SYSTEM_PROMPT = """
You are the Chief AI Editor for CFA Flash News (Cambodia National & International News Engine).
Your mission is to evaluate incoming news from all global social networks and news feeds, assign a credibility score (0-100%), and write a complete, beautiful, professional Khmer journalistic prose article (អត្ថបទសារព័ត៌មានភាសាខ្មែរផ្លូវការពេញលេញ).

STRICT JOURNALISTIC FORMATTING RULES:
1. HEADLINE: Write a powerful, elegant Khmer headline without prefixing "ព័ត៌មានទាន់ហេតុការណ៍".
2. PARAGRAPH 1 (DYNAMIC GEOGRAPHIC DATELINE & LEAD STORY): Start Paragraph 1 with a dynamic dateline (e.g. 'ខេត្តសៀមរាប៖ ', 'ខេត្តព្រះសីហនុ៖ ', 'រាជធានីភ្នំពេញ៖ ') followed by the main lead story details.
3. PARAGRAPH 2 (PROFESSIONAL JOURNALISTIC ATTRIBUTION & RULE OF LAW): MUST be separated by a double newline (\n\n). Cite official sources cleanly ("យោងតាមប្រភពព័ត៌មានផ្លូវការពី {source_name}...") analyzing leadership transparency, accountability, and rule of law. NEVER insert internal AI terms like "Super Brain System" in prose body!
4. PARAGRAPH 3 (CONSTITUTIONAL & PUBLIC WELFARE CONCLUSION): MUST be separated by a double newline (\n\n). Connect the story to Cambodian Constitution Articles (Article 31, 35, 41, 51, or 52) and citizen benefits, ending cleanly with '៕'.
5. THREE PARAGRAPH CONSTRAINT: Write EXACTLY 3 complete, distinct paragraphs separated by double newlines (\n\n). NEVER collapse paragraphs into a single long block!
6. NO BULLET POINTS IN BODY: The article body must be smooth, continuous Khmer literary prose paragraphs (អក្សរសិល្បិ៍ខ្មែរ).

Respond ONLY in valid JSON matching this schema:
{
  "credibility_score": float,
  "is_unverified_leak": boolean,
  "status_label": "string",
  "khmer_headline": "string",
  "khmer_body": "string",
  "impact_analysis": "string"
}
"""

class SuperBrainAIRewriter:
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        self.client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info("⚡ [SUPER BRAIN AI READY] Gemini 2.5 Flash News Rewriter Active!")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini Client: {e}")

    def extract_geographic_location(self, title: str, content: str) -> str:
        """
        Smart Geographic Location Extractor.
        Scans title and content for Cambodian 25 provinces/cities & major world capitals.
        """
        text = f"{title} {content}".lower()
        
        # 1. Cambodian 25 Provinces & Cities
        cam_locations = [
            ("សៀមរាប", "siem reap", "ខេត្តសៀមរាប៖"),
            ("ព្រះសីហនុ", "sihanouk", "ខេត្តព្រះសីហនុ៖"),
            ("បាត់ដំបង", "battambang", "ខេត្តបាត់ដំបង៖"),
            ("កំពត", "kampot", "ខេត្តកំពត៖"),
            ("កែប", "kep", "ខេត្តកែប៖"),
            ("កោះកុង", "koh kong", "ខេត្តកោះកុង៖"),
            ("កំពង់ចាម", "kampong cham", "ខេត្តកំពង់ចាម៖"),
            ("ស្វាយរៀង", "svay rieng", "ខេត្តស្វាយរៀង៖"),
            ("តាកែវ", "takeo", "ខេត្តតាកែវ៖"),
            ("ក្រចេះ", "kratie", "ខេត្តក្រចេះ៖"),
            ("ស្ទឹងត្រែង", "stung treng", "ខេត្តស្ទឹងត្រែង៖"),
            ("រតនគិរី", "ratanakiri", "ខេត្តរតនគិរី៖"),
            ("មណ្ឌលគិរី", "mondulkiri", "ខេត្តមណ្ឌលគិរី៖"),
            ("ព្រះវិហារ", "preah vihear", "ខេត្តព្រះវិហារ៖"),
            ("បន្ទាយមានជ័យ", "banteay meanchey", "ខេត្តបន្ទាយមានជ័យ៖"),
            ("ឧត្តរមានជ័យ", "oddar meanchey", "ខេត្តឧត្តរមានជ័យ៖"),
            ("ពោធិ៍សាត់", "pursat", "ខេត្តពោធិ៍សាត់៖"),
            ("កំពង់ឆ្នាំង", "kampong chhnang", "ខេត្តកំពង់ឆ្នាំង៖"),
            ("កំពង់ស្ពឺ", "kampong speu", "ខេត្តកំពង់ស្ពឺ៖"),
            ("កំពង់ធំ", "kampong thom", "ខេត្តកំពង់ធំ៖"),
            ("ព្រៃវែង", "prey veng", "ខេត្តព្រៃវែង៖"),
            ("ប៉ោយប៉ែត", "poipet", "ក្រុងប៉ោយប៉ែត៖"),
            ("បាវិត", "bavet", "ក្រុងបាវិត៖"),
            ("ភ្នំពេញ", "phnom penh", "រាជធានីភ្នំពេញ៖"),
        ]
        for name_kh, name_en, dateline in cam_locations:
            if name_kh in text or name_en in text:
                return dateline

        # 2. International Capitals & Cities
        intl_locations = [
            ("ហុងកុង", "hong kong", "ហុងកុង៖"),
            ("វ៉ាស៊ីនតោន", "washington", "ទីក្រុងវ៉ាស៊ីនតោន៖"),
            ("ហ្សឺណែវ", "geneva", "ទីក្រុងហ្សឺណែវ៖"),
            ("បេកាំង", "beijing", "ទីក្រុងបេកាំង៖"),
            ("បាងកក", "bangkok", "ទីក្រុងបាងកក៖"),
            ("ហាណូយ", "hanoi", "ទីក្រុងហាណូយ៖"),
            ("ឡុងដ៍", "london", "ទីក្រុងឡុងដ៍៖"),
            ("ប៉ារីស", "paris", "ទីក្រុងប៉ារីស៖"),
            ("តូក្យូ", "tokyo", "ទីក្រុងតូក្យូ៖"),
            ("សេអ៊ូល", "seoul", "ទីក្រុងសេអ៊ូល៖"),
            ("ម៉ានីល", "manila", "ទីក្រុងម៉ានីល៖"),
            ("ហ្សាការតា", "jakarta", "ទីក្រុងហ្សាការតា៖"),
            ("កូឡាឡាំពួ", "kuala lumpur", "ទីក្រុងកូឡាឡាំពួ៖"),
            ("ស៊ីងហ្គាពូរី", "singapore", "ប្រទេសសឹង្ហបូរី៖"),
            ("ញូវយ៉ក", "new york", "ទីក្រុងញូវយ៉ក៖"),
            ("ម៉ូស្កូ", "moscow", "ទីក្រុងម៉ូស្កូ៖"),
            ("កង់បេរ៉ា", "canberra", "ទីក្រុងកង់បេរ៉ា៖"),
            ("អូស្ត្រាលី", "australia", "ប្រទេសអូស្ត្រាលី៖"),
            ("អាមេរិក", "usa", "សហរដ្ឋអាមេរិក៖"),
            ("ចិន", "china", "ប្រទេសចិន៖"),
            ("ជប៉ុន", "japan", "ប្រទេសជប៉ុន៖"),
            ("បារាំង", "france", "ប្រទេសបារាំង៖"),
            ("វៀតណាម", "vietnam", "ប្រទេសវៀតណាម៖"),
            ("ថៃ", "thailand", "ប្រទេសថៃ៖"),
            ("ឡាវ", "laos", "ប្រទេសឡាវ៖"),
        ]
        for name_kh, name_en, dateline in intl_locations:
            if name_kh in text or name_en in text:
                return dateline

        return "រាជធានីភ្នំពេញ៖"

    def process_news(self, raw_id: str, title: str, content: str, source: str, source_tier: int = 1, is_unverified: bool = False) -> ProcessedNewsArticle:
        return self.rewrite_news(raw_id, title, content, source, source_tier, is_unverified)

    def _clean_and_parse_json(self, raw_text: str) -> dict:
        text = raw_text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
        return json.loads(text)

    def rewrite_news(self, raw_id: str, title: str, content: str, source: str, source_tier: int = 1, is_unverified: bool = False) -> ProcessedNewsArticle:
        """Processes raw breaking news, evaluates credibility score, and rewrites into professional Khmer post."""
        
        # Option A: Local Ollama (Qwen 2.5 3B) if enabled
        if config.USE_LOCAL_OLLAMA:
            try:
                return self._process_with_ollama(raw_id, title, content, source, source_tier, is_unverified)
            except Exception as e:
                logger.error(f"Local Ollama API call failed: {e}. Switching to Cloud/Rule fallback.")

        # Option B: Cloud Google Gemini API with Multi-Key Pool Rotation
        from gemini_key_pool import gemini_key_pool
        client_tuple = gemini_key_pool.get_client()
        if client_tuple:
            client, active_key = client_tuple
            prompt = f"Source: {source} (Tier {source_tier})\nIs Unverified Flag: {is_unverified}\nTitle: {title}\nContent: {content}"
            models_to_try = ["gemini-3.6-flash", "gemini-flash-latest", "gemini-flash-lite-latest"]
            
            for m_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=m_name,
                        contents=SYSTEM_PROMPT + "\n\nRaw News Input:\n" + prompt,
                    )
                    data = self._clean_and_parse_json(response.text)
                    cred_score = float(data.get("credibility_score", 95.0))
                    is_leak = data.get("is_unverified_leak", is_unverified)
                    status_label = data.get("status_label", "⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ")
                    headline = data.get("khmer_headline", title)
                    body = data.get("khmer_body", content)
                    impact = data.get("impact_analysis", "លើកកម្ពស់សិទ្ធិមនុស្ស និងនីតិរដ្ឋនៅកម្ពុជា")

                    formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)

                    return ProcessedNewsArticle(
                        original_id=raw_id,
                        credibility_score=cred_score,
                        is_unverified_leak=is_leak,
                        status_label=status_label,
                        khmer_headline=headline,
                        khmer_body=body,
                        impact_analysis=impact,
                        formatted_telegram_post=formatted_post
                    )
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        gemini_key_pool.mark_key_exhausted(active_key)
                        logger.info(f"ℹ️ Gemini key [{active_key[:6]}...] / model [{m_name}] 429 quota reached. Rotating to next pool key...")
                        new_client_tuple = gemini_key_pool.get_client()
                        if new_client_tuple:
                            client, active_key = new_client_tuple
                        continue
                    else:
                        logger.warning(f"Gemini API model [{m_name}] error: {e}")
                        break

        # Option B.2: Hugging Face Fine-Tuned Model (hemsinath/cfa-flash-bot) Failover
        try:
            from huggingface_engine import hf_polymath_ai
            hf_prompt = f"ចំណងជើង ៖ {title}\nខ្លឹមសារ ៖ {content}\nប្រភព ៖ {source}"
            hf_res = hf_polymath_ai.ask_polymath_ai(f"រៀបចំអត្ថបទសារព័ត៌មានផ្លូវការជាភាសាខ្មែរ ៖\n{hf_prompt}")
            if hf_res and not hf_res.startswith("❌"):
                headline = title
                body = hf_res
                impact = "លើកកម្ពស់សិទ្ធិមនុស្ស នីតិរដ្ឋ និងអធិបតេយ្យភាពជាតិកម្ពុជា"
                formatted_post = self._build_telegram_markdown("⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ", headline, body, impact, 95.0, source, is_unverified)
                return ProcessedNewsArticle(
                    original_id=raw_id,
                    credibility_score=95.0,
                    is_unverified_leak=is_unverified,
                    status_label="⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ",
                    khmer_headline=headline,
                    khmer_body=body,
                    impact_analysis=impact,
                    formatted_telegram_post=formatted_post
                )
        except Exception as e:
            logger.warning(f"Hugging Face rewriter failover skipped: {e}")

        # Option C: Intelligent Rule-Based Fallback Engine
        return self._rule_based_fallback(raw_id, title, content, source, source_tier, is_unverified)

    def rewrite_public_opinion_news(
        self,
        raw_id: str,
        title: str,
        content: str,
        source: str,
        sentiment_metrics
    ) -> ProcessedNewsArticle:
        """
        Public Opinion Journalism Rewriter:
        Rewrites viral hot posts into Khmer Public Opinion Journalism articles incorporating public sentiment % and citizen quotes.
        """
        dateline = self.extract_geographic_location(title, content)
        quotes_str = "\n".join([f"- {q}" for q in sentiment_metrics.representative_quotes]) if sentiment_metrics.representative_quotes else "- មហាជនសម្តែងការគាំទ្រយ៉ាងពេញទំហឹង"
        
        prompt = (
            f"=== HOT VIRAL EVENT PUBLIC OPINION INPUT ===\n"
            f"Source: {source}\n"
            f"Headline Event: {title}\n"
            f"Story Details: {content}\n\n"
            f"=== PUBLIC SENTIMENT METRICS ===\n"
            f"Support (គាំទ្រ): {sentiment_metrics.support_pct}%\n"
            f"Concern (បារម្ភ/រិះគន់): {sentiment_metrics.concern_pct}%\n"
            f"Proposal/Neutral (ស្នើសុំ/អព្យាក្រឹត): {sentiment_metrics.proposal_pct}%\n"
            f"Trending Score: {sentiment_metrics.trending_score}\n\n"
            f"=== REPRESENTATIVE CITIZEN QUOTES ===\n"
            f"{quotes_str}\n\n"
            f"INSTRUCTION: Write an official Khmer Public Opinion Journalistic Article (អត្ថបទសារព័ត៌មានមតិសាធារណៈផ្លូវការ) with:\n"
            f"Paragraph 1: Dateline starting with exact location '{dateline} ' and lead viral event.\n"
            f"Paragraph 2: Public sentiment breakdown (% Support, % Concern) connecting to rule of law and human rights.\n"
            f"Paragraph 3: Representative citizen quotes and public reactions.\n"
            f"Paragraph 4: Balanced journalistic conclusion ending with '៕'."
        )

        status_label = f"🔥 [HOT VIRAL NEWS - មតិមហាជនគាំទ្រ {sentiment_metrics.support_pct}%]"
        
        if self.client:
            try:
                model_name = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
                if "gemini-2.5-flash" in model_name:
                    model_name = "gemini-3.6-flash"
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=SYSTEM_PROMPT + "\n\n" + prompt,
                )
                data = json.loads(response.text)
                cred_score = float(data.get("credibility_score", 96.5))
                headline = data.get("khmer_headline", title)
                body = data.get("khmer_body", content)
                impact = data.get("impact_analysis", f"ការបញ្ចេញមតិរបស់មហាជន គាំទ្រ {sentiment_metrics.support_pct}% លើកកម្ពស់តម្លាភាពសង្គម")

                formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, False)

                return ProcessedNewsArticle(
                    original_id=raw_id,
                    credibility_score=cred_score,
                    is_unverified_leak=False,
                    status_label=status_label,
                    khmer_headline=headline,
                    khmer_body=body,
                    impact_analysis=impact,
                    formatted_telegram_post=formatted_post
                )
            except Exception as e:
                logger.error(f"Gemini Public Opinion Rewrite failed: {e}. Using fallback.")

        # Fallback
        headline = f"មហាជនសម្តែងការចាប់អារម្មណ៍យ៉ាងខ្លាំងលើ ៖ {title}"
        body = (
            f"{dateline} ព្រឹត្តិការណ៍ក្តៅគគុកអំពី «{title}» កំពុងផ្ទុះការចាប់អារម្មណ៍ និងពិភាក្សាយ៉ាងផុសផុលពីសំណាក់មហាជនលើបណ្តាញសង្គម។\n\n"
            f"យោងតាមការបញ្ជាក់ពីប្រព័ន្ធខួរក្បាលឆ្លាតវៃ @CFAflashBot AI Super Brain ដែលបានធ្វើការស្កេនមតិមហាជន បានបង្ហាញឱ្យដឹងថា មហាជនរហូតដល់ {sentiment_metrics.support_pct}% បានសម្តែងការគាំទ្រ និងស្វាគមន៍យ៉ាងពេញទំហឹង  ខណៈ {sentiment_metrics.concern_pct}% សម្តែងការបារម្ភ និងស្នើសុំឱ្យមានការយកចិត្តទុកដាក់បន្ថែម។\n\n"
            f"ចំពោះមតិតំណាងរបស់ប្រជាពលរដ្ឋបានបញ្ជាក់ថា៖ «{sentiment_metrics.representative_quotes[0] if sentiment_metrics.representative_quotes else 'ការរួមចំណែករបស់មហាជន គឺជាកម្លាំងចលករយ៉ាងសំខាន់ក្នុងការលើកកម្ពស់សង្គម'}»។\n\n"
            f"ជាការសន្និដ្ឋាន ការបញ្ចេញមតិយ៉ាងសកម្មរបស់សាធារណជន ឆ្លុះបញ្ចាំងពីការយល់ដឹង និងការចូលរួមយ៉ាងសកម្មក្នុងការលើកកម្ពស់តម្លាភាព និងនីតិរដ្ឋនៅកម្ពុជា៕"
        )
        impact = f"មតិមហាជន គាំទ្រ {sentiment_metrics.support_pct}%, បារម្ភ {sentiment_metrics.concern_pct}%"
        formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, 96.5, source, False)

        return ProcessedNewsArticle(
            original_id=raw_id,
            credibility_score=96.5,
            is_unverified_leak=False,
            status_label=status_label,
            khmer_headline=headline,
            khmer_body=body,
            impact_analysis=impact,
            formatted_telegram_post=formatted_post
        )

    def rewrite_political_philosophy_news(
        self,
        raw_id: str,
        title: str,
        content: str,
        source: str,
        political_metrics
    ) -> ProcessedNewsArticle:
        """
        Political Philosophy Rewriter:
        Rewrites political party statements into formal Khmer political science articles that promote
        Article 51 of the Cambodian Constitution and liberal multiparty democratic principles.
        """
        dateline = self.extract_geographic_location(title, content)
        status_label = f"🏛️ [{'មតិប្រឆាំងស្ថាបនា' if getattr(political_metrics, 'is_opposition_statement', False) else 'POLITICAL PHILOSOPHY'} - គោរពគ្រឹះប្រជាធិបតេយ្យសេរីពហុបក្ស មាត្រា ៥១]"
        tenets_str = "\n".join([f"- {t}" for t in political_metrics.philosophical_tenets])
        
        prompt = (
            f"=== OFFICIAL POLITICAL STATEMENT / LEADER MESSAGE INPUT ===\n"
            f"Political Leader / Figure: {political_metrics.figure_name}\n"
            f"Political Party: {political_metrics.party_name}\n"
            f"Is Opposition Statement: {getattr(political_metrics, 'is_opposition_statement', False)}\n"
            f"Source: {source}\n"
            f"Headline: {title}\n"
            f"Statement Details: {content}\n\n"
            f"=== CONSTITUTIONAL & POLITICAL PHILOSOPHY FRAMEWORK ===\n"
            f"Constitutional Law: {political_metrics.constitutional_reference}\n"
            f"Core Tenets:\n{tenets_str}\n\n"
            f"INSTRUCTION: Write an official Khmer Political Science & Democratic Pluralism Article (អត្ថបទសារលិខិតឥស្សរជននយោបាយ និងលទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស) with:\n"
            f"Paragraph 1: Dateline starting with exact location '{dateline} ' summarizing the official message/statement of {political_metrics.figure_name} ({political_metrics.party_name}).\n"
            f"Paragraph 2: Political philosophy analysis connecting the message to Tocqueville, J.S. Mill constructive opposition, Montesquieu, and John Locke principles.\n"
            f"Paragraph 3: Defense of Article 51 of the Cambodian Constitution, emphasizing the absolute necessity of maintaining peace, stability, national unity, and liberal multiparty democracy.\n"
            f"Paragraph 4: Balanced journalistic conclusion upholding constitutional rule of law ending with '៕'."
        )

        if self.client:
            try:
                model_name = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
                if "gemini-2.5-flash" in model_name:
                    model_name = "gemini-3.6-flash"
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=SYSTEM_PROMPT + "\n\n" + prompt,
                )
                data = json.loads(response.text)
                cred_score = float(data.get("credibility_score", 98.5))
                headline = data.get("khmer_headline", f"សារលិខិតផ្លូវការ ៖ {title}")
                body = data.get("khmer_body", content)
                impact = data.get("impact_analysis", "លើកកម្ពស់លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស និងរដ្ឋធម្មនុញ្ញកម្ពុជា")

                formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, False)

                return ProcessedNewsArticle(
                    original_id=raw_id,
                    credibility_score=cred_score,
                    is_unverified_leak=False,
                    status_label=status_label,
                    khmer_headline=headline,
                    khmer_body=body,
                    impact_analysis=impact,
                    formatted_telegram_post=formatted_post
                )
            except Exception as e:
                logger.error(f"Gemini Political Philosophy Rewrite failed: {e}. Using fallback.")

        # Fallback
        headline = f"សារលិខិតផ្លូវការ ៖ {title}"
        opp_comment = "ផ្នែកតាមទស្សនៈវិទ្យាសាស្ត្រនយោបាយ និងទស្សនៈវិទ្យារដ្ឋបាលដឹកនាំរដ្ឋ ការប្រកួតប្រជែងនយោបាយដោយសន្តិវិធី និងការបញ្ចេញមតិប្រឆាំងស្ថាបនា (Constructive Opposition) គឺជាកម្លាំងចលករយ៉ាងសំខាន់នៃលទ្ធិប្រជាធិបតេយ្យ ដូចដែលមានចែងក្នុងទ្រឹស្តីកិច្ចសន្យាសង្គម និងការបែងចែកអំណាចរដ្ឋ។" if getattr(political_metrics, 'is_opposition_statement', False) else "ផ្នែកតាមទស្សនៈវិទ្យាសាស្ត្រនយោបាយ និងទស្សនៈវិទ្យារដ្ឋបាលដឹកនាំរដ្ឋ ការប្រកួតប្រជែងនយោបាយដោយសន្តិវិធី និងការបញ្ចេញមតិចម្រុះ គឺជាកម្លាំងចលករយ៉ាងសំខាន់នៃលទ្ធិប្រជាធិបតេយ្យ ដូចដែលមានចែងក្នុងទ្រឹស្តីកិច្ចសន្យាសង្គម និងការបែងចែកអំណាចរដ្ឋ។"
        body = (
            f"{dateline} {political_metrics.figure_name} នៃ {political_metrics.party_name} បានចេញផ្សាយសារលិខិតផ្លូវការអំពី «{title}» ដោយបញ្ជាក់ពីជំហរនយោបាយ និងការរួមចំណែកក្នុងការអភិវឌ្ឍជាតិ។\n\n"
            f"{opp_comment}\n\n"
            f"ផ្អែកលើស្មារតីនៃ មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ការគោរព និងរក្សាឱ្យបាននូវគ្រឹះនៃរបបដឹកនាំនយោបាយ «លទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស» គឺជាកាតព្វកិច្ចចម្បងក្នុងការការពារសន្តិភាព ស្ថិរភាពសង្គម និងនីតិរដ្ឋ។\n\n"
            f"ជាការសន្និដ្ឋាន ការប្រកាន់ខ្ជាប់នូវគោលការណ៍ប្រជាធិបតេយ្យសេរីពហុបក្ស ដើរទន្ទឹមគ្នានឹងការគោរពច្បាប់ នឹងនាំមកនូវការអភិវឌ្ឍប្រកបដោយចីរភាពសម្រាប់ជាតិ និងប្រជាជនកម្ពុជាទាំងមូល៕"
        )
        impact = "ការពាររដ្ឋធម្មនុញ្ញ មាត្រា ៥១ និងលទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស"
        formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, 98.5, source, False)

        return ProcessedNewsArticle(
            original_id=raw_id,
            credibility_score=98.5,
            is_unverified_leak=False,
            status_label=status_label,
            khmer_headline=headline,
            khmer_body=body,
            impact_analysis=impact,
            formatted_telegram_post=formatted_post
        )

    def _process_with_ollama(self, raw_id: str, title: str, content: str, source: str, source_tier: int, is_unverified: bool) -> ProcessedNewsArticle:
        import requests
        logger.info(f"🤖 Calling Local Ollama ({config.OLLAMA_MODEL}) at {config.OLLAMA_HOST}...")
        prompt = f"{SYSTEM_PROMPT}\n\nRaw Input:\nSource: {source} (Tier {source_tier})\nTitle: {title}\nContent: {content}"
        
        payload = {
            "model": config.OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        resp = requests.post(f"{config.OLLAMA_HOST}/api/generate", json=payload, timeout=30)
        if resp.status_code == 200:
            res_data = resp.json()
            data = json.loads(res_data.get("response", "{}"))
            cred_score = float(data.get("credibility_score", 95.0))
            is_leak = data.get("is_unverified_leak", is_unverified)
            status_label = data.get("status_label", "⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ")
            headline = data.get("khmer_headline", title)
            body = data.get("khmer_body", content)
            impact = data.get("impact_analysis", "លើកកម្ពស់សិទ្ធិមនុស្ស និងនីតិរដ្ឋនៅកម្ពុជា")

            formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)
            return ProcessedNewsArticle(
                original_id=raw_id,
                credibility_score=cred_score,
                is_unverified_leak=is_leak,
                status_label=status_label,
                khmer_headline=headline,
                khmer_body=body,
                impact_analysis=impact,
                formatted_telegram_post=formatted_post
            )
        else:
            raise Exception(f"Ollama returned HTTP status {resp.status_code}: {resp.text}")

    def _rule_based_fallback(self, raw_id: str, title: str, content: str, source: str, source_tier: int, is_unverified: bool) -> ProcessedNewsArticle:
        from translator import fallback_translate_to_khmer
        cred_score = 95.0 if source_tier == 1 and not is_unverified else 70.0
        is_leak = is_unverified
        status_label = "⚡ VERIFIED FLASH NEWS - ព័ត៌មានទាន់ហេតុការណ៍ច្បាស់ការ" if not is_leak else "⚠️ UNVERIFIED MARKET LEAK - ព័ត៌មានបែកធ្លាយមិនទាន់ផ្លូវការ"

        dateline = self.extract_geographic_location(title, content)
        clean_title = title.replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").replace("ព័ត៌មានទាន់ហេតុការណ៍ ៖", "").replace("ព័ត៌មានទាន់ហេតុការណ៍", "").strip()
        headline = fallback_translate_to_khmer(clean_title) if any(c.isalpha() and ord(c) < 128 for c in clean_title) else clean_title

        is_clean_source_name = source and len(source) < 25 and not any(k in source for k in ["កម្ពុជា", "រដ្ឋ", "ប្រព័ន្ធ", "ព័ត៌មាន"])
        source_name = fallback_translate_to_khmer(source) if is_clean_source_name else "ប្រភពព័ត៌មានផ្លូវការ"

        clean_desc = content.strip() if content else clean_title
        if any(c.isalpha() and ord(c) < 128 for c in clean_desc[:100]):
            clean_desc = fallback_translate_to_khmer(clean_desc)
        
        clean_desc = clean_desc.strip()
        if not clean_desc.endswith("។") and not clean_desc.endswith("»") and not clean_desc.endswith("!"):
            clean_desc += "។"

        if len(clean_desc) > 200:
            clean_desc = clean_desc[:200] + "..."

        p1 = f"{dateline} {clean_desc}"
        p2 = f"យោងតាមប្រភពព័ត៌មានផ្លូវការពី {source_name} បានបញ្ជាក់ឱ្យដឹងថា ព្រឹត្តិការណ៍នេះគឺជាជំហានដ៏សំខាន់ក្នុងការលើកកម្ពស់តម្លាភាព គណនេយ្យភាពសង្គម និងការទប់ស្កាត់រាល់បាតុភាពអសកម្ម។"
        p3 = f"ផ្អែកលើស្មារតីនៃ មាត្រា ៥១ និងមាត្រា ៥២ នៃរដ្ឋធម្មនុញ្ញនៃព្រះរាជាណាចក្រកម្ពុជា ការគោរពច្បាប់ នីតិរដ្ឋ និងប្រជាធិបតេយ្យសេរីពហុបក្ស នឹងនាំមកនូវការអភិវឌ្ឍប្រកបដោយចីរភាព និងសុខសន្តិភាពជានិរន្តរ៍ជូនជាតិ និងប្រជាជនទាំងមូល៕"

        body = f"{p1}\n\n{p2}\n\n{p3}"
        impact = "លើកកម្ពស់សិទ្ធិមនុស្ស មាត្រា ៥១ និងនីតិរដ្ឋនៅកម្ពុជា"

        formatted_post = self._build_telegram_markdown(status_label, headline, body, impact, cred_score, source, is_leak)

        return ProcessedNewsArticle(
            original_id=raw_id,
            credibility_score=cred_score,
            is_unverified_leak=is_leak,
            status_label=status_label,
            khmer_headline=headline,
            khmer_body=body,
            impact_analysis=impact,
            formatted_telegram_post=formatted_post
        )

    def _build_telegram_markdown(self, status: str, headline: str, body: str, impact: str, score: float, source: str, is_leak: bool) -> str:
        from translator import clean_khmer_spaces
        from khmer_auditor import khmer_auditor

        leak_banner = "\n🚨 *បដាព្រមាន៖ ព័ត៌មាននេះមិនទាន់មានការបញ្ជាក់ផ្លូវការនៅឡើយទេ សូមផ្ទៀងផ្ទាត់មុនធ្វើការសម្រេចចិត្ត។*\n" if is_leak else ""

        headline_clean = khmer_auditor.audit_khmer_text(clean_khmer_spaces(headline).replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").strip()).replace("*", "").replace("_", "").strip()
        body_clean = khmer_auditor.audit_khmer_text(clean_khmer_spaces(body)).replace("*", "").replace("_", "").strip()
        
        footer_signature = (
            f"\n\n🔍 *ព័ត៌មាននេះនាំមកជូនដោយ៖*\n"
            f"• បច្ចេកទេស: *ប្រព័ន្ធខួរក្បាលឆ្លាតវៃ APEX Super Brain*\n"
            f"• ផលិតដោយ៖ *សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA*\n"
            f"• Telegram: *CFA Flash Feed | @CFAflashBot*\n"
            f"• ADMIN: *@Sokpheatonsai*"
        )

        # Telegram Photo Caption Limit Safety Guard (1024 chars max)
        max_body_len = 980 - len(headline_clean) - len(leak_banner) - len(footer_signature)
        if len(body_clean) > max_body_len and max_body_len > 100:
            truncated = body_clean[:max_body_len]
            # Smart Sentence-Boundary Truncation: Find last Khmer sentence ending ('។' or '៕')
            last_full_stop = max(truncated.rfind("។"), truncated.rfind("៕"))
            if last_full_stop > 100:
                body_clean = truncated[:last_full_stop + 1]
                if body_clean.endswith("។"):
                    body_clean = body_clean[:-1] + "៕"
            else:
                body_clean = truncated.rsplit(" ", 1)[0] + "៕"

        return f"*{headline_clean}*\n\n{body_clean}{leak_banner}{footer_signature}"

    async def generate_banner_image(self, headline: str, category_title: str = "ព័ត៌មានទាន់ហេតុការណ៍") -> str:
        """
        High-Impact AI Graphic Banner Rendering Engine.
        Delegates to dedicated BannerEngine for 100% synchronized Playwright HTML5 & PIL Fallback branding.
        """
        from banner_engine import banner_engine
        return await banner_engine.generate_banner_image(headline, category_title)
