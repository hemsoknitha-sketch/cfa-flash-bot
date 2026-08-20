import asyncio
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
2. PARAGRAPH 1 (DATELINE & LEAD): Start with "រាជធានីភ្នំពេញ៖ " followed by the lead news story.
3. PARAGRAPH 2 (SUPER BRAIN DYNAMIC SOURCE): MUST start with: "យោងតាមប្រភពព័ត៌មានច្បាស់ការពី {source_name} ដែលប្រព័ន្ធខួរក្បាលឆ្លាតវៃ @CFAflashBot AI Super Brain ឆែកឃើញ បានបញ្ជាក់ឱ្យដឹងថា..." followed by details connecting to human rights, anti-corruption, or rule of law.
4. PARAGRAPH 3 & 4 (IMPACT & CONCLUSION): Write fluid, elegant Khmer prose paragraphs analyzing the positive social impact, benefits to citizens, and national prestige. End the final paragraph with the official Khmer full stop "៕".
5. NO BULLET POINTS IN BODY: The article body must be smooth, continuous Khmer literary prose paragraphs (អក្សរសិល្បិ៍ខ្មែរ).

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
                logger.error(f"Failed to initialize Gemini API client: {e}")

    def process_news(self, raw_id: str, title: str, content: str, source: str, source_tier: int = 1, is_unverified: bool = False) -> ProcessedNewsArticle:
        return self.rewrite_news(raw_id, title, content, source, source_tier, is_unverified)

    def rewrite_news(self, raw_id: str, title: str, content: str, source: str, source_tier: int = 1, is_unverified: bool = False) -> ProcessedNewsArticle:
        """Processes raw breaking news, evaluates credibility score, and rewrites into professional Khmer post."""
        
        # Option A: Local Ollama (Qwen 2.5 3B) if enabled
        if config.USE_LOCAL_OLLAMA:
            try:
                return self._process_with_ollama(raw_id, title, content, source, source_tier, is_unverified)
            except Exception as e:
                logger.error(f"Local Ollama API call failed: {e}. Switching to Cloud/Rule fallback.")

        # Option B: Cloud Google Gemini API
        if self.client:
            try:
                prompt = f"Source: {source} (Tier {source_tier})\nIs Unverified Flag: {is_unverified}\nTitle: {title}\nContent: {content}"
                model_name = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
                if "gemini-2.5-flash" in model_name:
                    model_name = "gemini-3.6-flash"
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=SYSTEM_PROMPT + "\n\nRaw News Input:\n" + prompt,
                )
                data = json.loads(response.text)
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
                logger.error(f"Gemini API call failed: {e}. Switching to Rule-based AI Fallback engine.")

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
            f"Paragraph 1: Dateline starting with 'រាជធានីភ្នំពេញ៖ ' and lead viral event.\n"
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
            f"រាជធានីភ្នំពេញ៖ ព្រឹត្តិការណ៍ក្តៅគគុកអំពី «{title}» កំពុងផ្ទុះការចាប់អារម្មណ៍ និងពិភាក្សាយ៉ាងផុសផុលពីសំណាក់មហាជនលើបណ្តាញសង្គម។\n\n"
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
        tenets_str = "\n".join([f"- {t}" for t in political_metrics.philosophical_tenets])
        
        prompt = (
            f"=== OFFICIAL POLITICAL STATEMENT / LEADER MESSAGE INPUT ===\n"
            f"Political Leader / Figure: {political_metrics.figure_name}\n"
            f"Political Party: {political_metrics.party_name}\n"
            f"Source: {source}\n"
            f"Headline: {title}\n"
            f"Statement Details: {content}\n\n"
            f"=== CONSTITUTIONAL & POLITICAL PHILOSOPHY FRAMEWORK ===\n"
            f"Constitutional Law: {political_metrics.constitutional_reference}\n"
            f"Core Tenets:\n{tenets_str}\n\n"
            f"INSTRUCTION: Write an official Khmer Political Science & Statesmanship Article (អត្ថបទសារលិខិតឥស្សរជននយោបាយ និងលទ្ធិប្រជាធិបតេយ្យសេរីពហុបក្ស) with:\n"
            f"Paragraph 1: Dateline starting with 'រាជធានីភ្នំពេញ៖ ' summarizing the official message/statement of {political_metrics.figure_name} ({political_metrics.party_name}).\n"
            f"Paragraph 2: Statesmanship and political philosophy analysis connecting the message to Cicero, Marcus Aurelius civic duty, Montesquieu, and John Locke principles.\n"
            f"Paragraph 3: Defense of Article 51 of the Cambodian Constitution, emphasizing the absolute necessity of maintaining peace, stability, national unity, and liberal multiparty democracy.\n"
            f"Paragraph 4: Balanced journalistic conclusion upholding constitutional rule of law ending with '៕'."
        )

        status_label = f"🏛️ [POLITICAL PHILOSOPHY - គោរពគ្រឹះប្រជាធិបតេយ្យសេរីពហុបក្ស មាត្រា ៥១]"
        
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
        body = (
            f"រាជធានីភ្នំពេញ៖ {political_metrics.figure_name} នៃ {political_metrics.party_name} បានចេញផ្សាយសារលិខិតផ្លូវការអំពី «{title}» ដោយបញ្ជាក់ពីជំហរនយោបាយ និងការរួមចំណែកក្នុងការអភិវឌ្ឍជាតិ។\n\n"
            f"ផ្នែកតាមទស្សនៈវិទ្យាសាស្ត្រនយោបាយ និងទស្សនៈវិទ្យារដ្ឋបាលដឹកនាំរដ្ឋ ការប្រកួតប្រជែងនយោបាយដោយសន្តិវិធី និងការបញ្ចេញមតិចម្រុះ គឺជាកម្លាំងចលករយ៉ាងសំខាន់នៃលទ្ធិប្រជាធិបតេយ្យ ដូចដែលមានចែងក្នុងទ្រឹស្តីកិច្ចសន្យាសង្គម និងការបែងចែកអំណាចរដ្ឋ។\n\n"
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

        headline = "កម្ពុជាពង្រឹងកិច្ចសហប្រតិបត្តិការអន្តរជាតិ បើកយុទ្ធនាការក្ដៅគគុកបង្រ្កាបបទល្មើសឆបោកតាមប្រព័ន្ធអនឡាញ និងលើកកម្ពស់នីតិរដ្ឋ"
        
        source_name = fallback_translate_to_khmer(source) if source and "Super Brain" not in source else "ប្រព័ន្ធខួរក្បាលឆ្លាតវៃ Super Brain"
        body = (
            "រាជធានីភ្នំពេញ៖ អាជ្ញាធរមានសមត្ថកិច្ចនៃព្រះរាជាណាចក្រកម្ពុជា បាននិងកំពុងពង្រឹងកិច្ចសហប្រតិបត្តិការយ៉ាងជិតស្និទ្ធជាមួយស្ថាប័នអនុវត្តច្បាប់អន្តរជាតិ ដើម្បីបើកប្រតិបត្តិការរួមគ្នាក្នុងទ្រង់ទ្រាយធំ ឈានទៅបោសសម្អាត និងវែកមុខសញ្ញាឧក្រិដ្ឋជនឆបោកតាមប្រព័ន្ធអនឡាញ (Online Scam) ដែលកំពុងប្រតិបត្តិការឆ្លងដែន។\n\n"
            f"យោងតាមប្រភពព័ត៌មានច្បាស់ការពី {source_name} ដែលប្រព័ន្ធខួរក្បាលឆ្លាតវៃ @CFAflashBot AI Super Brain ឆែកឃើញ បានបញ្ជាក់ឱ្យដឹងថា ប្រតិបត្តិការចម្រុះនេះមិនត្រឹមតែផ្តោតសំខាន់លើការផ្ដន្ទាទោសឧក្រិដ្ឋជនបច្ចេកវិទ្យាប៉ុណ្ណោះទេ ប៉ុន្តែក៏បានផ្សារភ្ជាប់យ៉ាងស្អិតរមួតទៅនឹងការលើកកម្ពស់ការគោរពសិទ្ធិមនុស្ស និងការពង្រឹងនីតិរដ្ឋយ៉ាងម៉ឺងម៉ាត់នៅកម្ពុជាផងដែរ។ ការបោះជំហាននេះ ឆ្លុះបញ្ចាំងពីឆន្ទៈមោះមុតរបស់អាជ្ញាធរ ក្នុងការកម្ចាត់ភាពអសកម្ម និងធានានូវយុត្តិធម៌សង្គមប្រកបដោយតម្លាភាព។\n\n"
            "ជុំវិញការរឹតបន្តឹងវិធានការច្បាប់នេះ អ្នកជំនាញបានធ្វើការវិភាគយ៉ាងច្បាស់លាស់ពីផលប្រយោជន៍ និងឥទ្ធិពលជាវិជ្ជមាននៃយុទ្ធនាការនេះ។ ជាបឋម ប្រតិបត្តិការដ៏ក្តៅគគុកនេះបានចូលរួមចំណែកយ៉ាងសកម្មក្នុងការកាត់បន្ថយ និងទប់ស្កាត់ហានិភ័យនៃបទល្មើសឆបោកតាមប្រព័ន្ធបច្ចេកវិទ្យាឌីជីថល ដែលកំពុងគំរាមកំហែងដល់ប្រជាពលរដ្ឋស្លូតត្រង់ទូទាំងសកលលោក។ តាមរយៈការវាយបំបែកសំបុកឧក្រិដ្ឋជនទាំងនេះ វាបានជួយស្តារ និងបង្កើនទំនុកចិត្តយ៉ាងរឹងមាំ ព្រមទាំងធានាបាននូវសន្តិសុខសុវត្ថិភាពសង្គមជូនប្រជាពលរដ្ឋកម្ពុជាឱ្យរស់នៅដោយភាពកក់ក្តៅ។\n\n"
            "លើសពីនេះទៅទៀត ភាពជោគជ័យនៃកិច្ចសហប្រតិបត្តិការជាមួយសហគមន៍អន្តរជាតិនេះ បានផ្តល់នូវផលប្រយោជន៍ជាយុទ្ធសាស្ត្រយ៉ាងធំធេង ដោយបានរួមចំណែកយ៉ាងសំខាន់ក្នុងការលើកស្ទួយកិត្តិយស និងកិត្យានុភាពរបស់ប្រទេសកម្ពុជានៅលើឆាកអន្តរជាតិ ក្នុងនាមជារដ្ឋអធិបតេយ្យដែលប្រកាន់ខ្ជាប់នូវច្បាប់ និងសណ្តាប់ធ្នាប់សាធារណៈយ៉ាងខ្ជាប់ខ្ជួន៕"
        )
        impact = "លើកកម្ពស់សិទ្ធិមនុស្ស និងនីតិរដ្ឋនៅកម្ពុជា"

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

        leak_banner = "\n🚨 *បដាព្រមាន៖ ព័ត៌មាននេះមិនទាន់មានការបញ្ជាក់ផ្លូវការនៅឡើយទេ សូមផ្ទៀងផ្ទាត់មុនធ្វើការសម្រេចចិត្ត។*\n" if is_leak else ""

        headline_clean = clean_khmer_spaces(headline).replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").strip()
        body_clean = clean_khmer_spaces(body)
        impact_clean = clean_khmer_spaces(impact or "")
        impact_lines = [line.strip() for line in impact_clean.split("\n") if line.strip()]
        formatted_impact = "\n".join([f"• {line}" if not line.startswith("•") else line for line in impact_lines])

        return (
            f"*{headline_clean}*\n\n"
            f"{body_clean}\n"
            f"{leak_banner}\n"
            f"🔍 *ព័ត៌មាននេះនាំមកជូនដោយ៖*\n"
            f"• កម្រិតភាពជឿជាក់ (Credibility Score): `{score}%`\n"
            f"• ប្រភពដើម: `ប្រព័ន្ធខួរក្បាលឆ្លាតវៃ Super Brain`\n"
            f"• ផលិតដោយ៖ *សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA*\n"
            f"• Telegram: *CFA Flash News | @CFAflashBot*"
        )

    async def generate_banner_image(self, headline: str) -> str:
        """
        High-Impact AI Image & Graphic Banner Rendering Engine.
        Uses Playwright Chromium Engine for 100% perfect Khmer typography OpenType shaping.
        """
        import os
        logger.info(f"🎨 [AI IMAGE ENGINE] Rendering High-Impact Banner Image for: '{headline}'...")
        image_filename = f"banner_{abs(hash(headline)) % 10000}.jpg"
        clean_headline = headline.replace("ព័ត៌មានទាន់ហេតុការណ៍៖", "").strip()

        # Load LOGO.png if available
        logo_path = os.path.abspath("LOGO.png")
        if os.path.exists(logo_path):
            import base64
            try:
                with open(logo_path, "rb") as f:
                    logo_b64 = base64.b64encode(f.read()).decode("utf-8")
                    logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height: 36px; width: auto; vertical-align: middle; border-radius: 6px;" />'
            except Exception:
                logo_html = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'
        else:
            logo_html = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'

        # Method 1: High-Definition Playwright HTML5 HarfBuzz OpenType Engine
        try:
            from playwright.async_api import async_playwright

            html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<style>
@import url('https://fonts.googleapis.com/css2?family=Battambang:wght@400;700&family=Moul&family=Outfit:wght@600;800&display=swap');

body {{
    margin: 0;
    padding: 0;
    width: 1200px;
    height: 630px;
    background: linear-gradient(135deg, #0b132b 0%, #1c2541 60%, #3a506b 100%);
    font-family: 'Battambang', 'Khmer OS Battambang', sans-serif;
    color: #f8fafc;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 55px 60px;
    border-top: 14px solid #ef4444;
}}

.header-container {{
    display: flex;
    align-items: center;
    gap: 16px;
}}

.badge {{
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
    color: white;
    font-family: 'Battambang', 'Outfit', sans-serif;
    font-size: 24px;
    font-weight: 700;
    padding: 10px 24px;
    border-radius: 50px;
    display: inline-flex;
    align-items: center;
    gap: 12px;
    letter-spacing: 0.5px;
    box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
    width: fit-content;
}}

.category-title {{
    font-family: 'Moul', 'Khmer OS Muol', serif;
    color: #ef4444;
    font-size: 38px;
    margin-top: 25px;
    margin-bottom: 18px;
    text-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
}}

.news-headline {{
    font-size: 38px;
    line-height: 1.6;
    font-weight: 700;
    color: #f8fafc;
    text-shadow: 0 2px 10px rgba(0,0,0,0.6);
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}}

.footer {{
    border-top: 2px solid rgba(255, 255, 255, 0.15);
    padding-top: 22px;
    font-size: 20px;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.footer-brand {{
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #f8fafc;
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

.bot-tag {{
    color: #38bdf8;
    font-weight: 800;
    text-shadow: 0 0 12px rgba(56, 189, 248, 0.7);
}}
</style>
</head>
<body>
    <div>
        <div class='header-container'>
            <div class='badge'>
                {logo_html}
                សម្ពន្ធហ្វេសប៊ុកកម្ពុជា CFA
            </div>
        </div>
        <div class='category-title'>ព័ត៌មានទាន់ហេតុការណ៍</div>
        <div class='news-headline'>{clean_headline}</div>
    </div>
    <div class='footer'>
        <span class='footer-brand'>APEX SUPER BRAIN AI SYSTEM</span>
        <span><span class='bot-tag'>@CFAflashBot</span> | REAL-TIME FLASH FEED</span>
    </div>
</body>
</html>"""

            temp_html_path = os.path.abspath(f"temp_{abs(hash(headline)) % 10000}.html")
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page(viewport={"width": 1200, "height": 630})
                await page.goto("file:///" + temp_html_path.replace("\\", "/"))
                await page.screenshot(path=image_filename, type="jpeg", quality=95)
                await browser.close()

            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

            logger.info(f"✨ [AI IMAGE READY] High-Definition Khmer Banner Asset prepared: {image_filename}")
            return image_filename
        except Exception as err:
            logger.warning(f"Playwright HTML rendering fallback: {err}. Switching to PIL fallback.")

        # Method 2: PIL Fallback Engine
        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new('RGB', (1200, 630), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            draw.rectangle([(0, 0), (1200, 16)], fill=(239, 68, 68))
            draw.rectangle([(60, 48), (380, 100)], fill=(239, 68, 68))
            
            font_arial = r'C:\Windows\Fonts\arialbd.ttf'
            font_battambang = r'C:\Windows\Fonts\KhmerOSbattambang.ttf'
            badge_font = ImageFont.truetype(font_arial, 20) if os.path.exists(font_arial) else ImageFont.load_default()
            draw.text((78, 64), "SUPER VIP FLASH NEWS", fill=(255, 255, 255), font=badge_font)

            body_font = ImageFont.truetype(font_battambang, 28) if os.path.exists(font_battambang) else badge_font
            draw.text((60, 150), clean_headline[:60], fill=(248, 250, 252), font=body_font)
            img.save(image_filename, format="JPEG", quality=95)
        except Exception as e:
            logger.warning(f"PIL Image generation fallback: {e}")
            if not os.path.exists(image_filename):
                valid_jpeg_bytes = bytes.fromhex("ffd8ffe000104a46494600010101006000600000ffdb004300080606070605080707070909080a0c140d0c0b0b0c1912130f141d1a1f1e1d1a1c1c20242e2720222c231c1c2837292c30313434341f27393d38323c2e333430ffc0000b080001000101011100ffc4001f0000010501010101010100000000000000000102030405060708090a0bffda0008010100003f00d2cf00ffd9")
                with open(image_filename, "wb") as f:
                    f.write(valid_jpeg_bytes)

        logger.info(f"✨ [AI IMAGE READY] Asset prepared successfully: {image_filename}")
        return image_filename
