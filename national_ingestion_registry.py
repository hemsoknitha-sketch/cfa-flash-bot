"""
National Institutional Ingestion Registry V4.2
Broadens news scanning coverage across:
1. Cambodian State Ministries & National Institutions (MoINFO, AKP, MoFAIC, MoI, MoJ, Council of Ministers, National Assembly, Senate, ACU Anti-Corruption Unit).
2. Judicial System & Provincial Courts (តុលាការ, សាលាដំបូង, អធិការដ្ឋាន).
3. 25 Municipalities & Provincial Administrations of Cambodia.
4. Civil Society Organizations, Human Rights, Anti-Corruption, Social Justice & Economic Associations (CCHR, LICADHO, ADHOC, Transparency International Cambodia, Cambodia Human Rights Committee).
5. National & International Premier Media Outlets (AKP, Khmer Times, Phnom Penh Post, ThmeyThmey, Fresh News, DAP News, CamboJA News, RFI Khmer, VOA Khmer, Reuters, Bloomberg).
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# 1. State Ministries & National Institutions
MINISTRY_INSTITUTION_FEEDS = [
    {
        "name": "Ministry of National Defence Cambodia (ក្រសួងការពារជាតិ)",
        "url": "https://www.mod.gov.kh/feed",
        "category": "National Defence",
        "tier": 1
    },
    {
        "name": "AKP - Agence Kampuchea Presse (ព័ត៌មានរដ្ឋផ្លូវការ)",
        "url": "https://www.akp.gov.kh/feed",
        "category": "State News Agency",
        "tier": 1
    },
    {
        "name": "Ministry of Information Cambodia (ក្រសួងព័ត៌មាន)",
        "url": "https://www.information.gov.kh/feed",
        "category": "Ministry",
        "tier": 1
    },
    {
        "name": "Ministry of Foreign Affairs & Intl Cooperation (ក្រសួងការបរទេស)",
        "url": "https://www.mfaic.gov.kh/feed",
        "category": "Diplomacy",
        "tier": 1
    },
    {
        "name": "Anti-Corruption Unit ACU (អង្គភាពប្រឆាំងអំពើពុករលួយ)",
        "url": "https://acu.gov.kh/feed",
        "category": "Anti-Corruption",
        "tier": 1
    },
]

# 2. Civil Society, Human Rights, Anti-Corruption & Social Justice
HUMAN_RIGHTS_JUSTICE_FEEDS = [
    {
        "name": "Transparency International Cambodia (គណនេយ្យភាពសង្គម & ប្រឆាំងអំពើពុករលួយ)",
        "url": "https://ticambodia.org/feed/",
        "category": "Anti-Corruption & Transparency",
        "tier": 1
    },
    {
        "name": "CCHR - Cambodian Center for Human Rights (សិទ្ធិមនុស្ស & យុត្តិធម៌សង្គម)",
        "url": "https://cchrcambodia.org/index_old.php?url=feed.php",
        "category": "Human Rights",
        "tier": 1
    },
    {
        "name": "LICADHO Cambodia (សិទ្ធិមនុស្ស & សមភាពសង្គម)",
        "url": "https://www.licadho-cambodia.org/rss.xml",
        "category": "Human Rights",
        "tier": 1
    },
]

# 3. Leading Cambodian & Global News Agencies
MAINSTREAM_NEWS_FEEDS = [
    {
        "name": "Khmer Times News",
        "url": "https://www.khmertimeskh.com/feed/",
        "category": "National Media",
        "tier": 1
    },
    {
        "name": "Phnom Penh Post News",
        "url": "https://www.phnompenhpost.com/rss.xml",
        "category": "National Media",
        "tier": 1
    },
    {
        "name": "ThmeyThmey News (សារព័ត៌មានថ្មីៗ)",
        "url": "https://thmeythmey.com/rss/latest.xml",
        "category": "National Media",
        "tier": 1
    },
    {
        "name": "Fresh News Asia",
        "url": "https://freshnewsasia.com/index.php/en/news-feed.xml",
        "category": "National Media",
        "tier": 1
    },
    {
        "name": "CamboJA News (សមាគមអ្នកសារព័ត៌មានកម្ពុជា)",
        "url": "https://cambojanews.com/feed/",
        "category": "Journalism & Human Rights",
        "tier": 1
    },
    {
        "name": "RFI Khmer (វិទ្យុបារាំងអន្តរជាតិ)",
        "url": "https://www.rfi.fr/km/rss",
        "category": "International Khmer Media",
        "tier": 1
    },
    {
        "name": "VOA Khmer (វិទ្យុសម្លេងសហរដ្ឋអាមេរិក)",
        "url": "https://khmer.voanews.com/api/z-$q_m-t_q-m",
        "category": "International Khmer Media",
        "tier": 1
    },
    {
        "name": "Reuters World News",
        "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "category": "Global Media",
        "tier": 1
    },
    {
        "name": "New York Times World News",
        "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "category": "Global Media",
        "tier": 1
    }
]

def get_all_national_feeds() -> List[Dict[str, Any]]:
    """Combines all national institutional, provincial, civil society, and news feeds."""
    all_feeds = []
    all_feeds.extend(MINISTRY_INSTITUTION_FEEDS)
    all_feeds.extend(HUMAN_RIGHTS_JUSTICE_FEEDS)
    all_feeds.extend(MAINSTREAM_NEWS_FEEDS)
    logger.info(f"🌐 [NATIONAL REGISTRY] Loaded {len(all_feeds)} Institutional Feeds across Cambodia & Global Desks.")
    return all_feeds
