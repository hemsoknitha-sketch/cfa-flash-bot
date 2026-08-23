"""
National Institutional Ingestion Registry V5.0 (35+ Premier Desks)
Broadens news scanning coverage across:
1. Cambodian State Ministries & National Institutions (MoINFO, AKP, MoFAIC, MoD, MoI, MoJ, OCM, Assembly, Senate, ACU, NEC, MEF).
2. Provincial Administrations & 25 Capital/Municipal Desks (Phnom Penh, Siem Reap, Sihanoukville, Battambang, Border Desks).
3. Civil Society Organizations, Human Rights, Anti-Corruption & Social Justice (CCHR, LICADHO, ADHOC, TI Cambodia, CHRC).
4. National & International Premier Media Outlets (AKP, Khmer Times, Phnom Penh Post, ThmeyThmey, Fresh News, CamboJA, RFI, VOA, Reuters, NYT).
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
    {
        "name": "Office of the Council of Ministers (ទីស្តីការគណៈរដ្ឋមន្ត្រី)",
        "url": "https://pressocm.gov.kh/feed",
        "category": "Cabinet Office",
        "tier": 1
    },
    {
        "name": "Ministry of Interior Cambodia (ក្រសួងមហាផ្ទៃ)",
        "url": "https://www.interior.gov.kh/feed",
        "category": "Internal Security",
        "tier": 1
    },
    {
        "name": "Ministry of Justice Cambodia (ក្រសួងយុត្តិធម៌)",
        "url": "https://www.moj.gov.kh/feed",
        "category": "Judicial System",
        "tier": 1
    },
    {
        "name": "Ministry of Economy & Finance (ក្រសួងសេដ្ឋកិច្ច និងហិរញ្ញវត្ថុ)",
        "url": "https://www.mef.gov.kh/feed",
        "category": "Economy & Finance",
        "tier": 1
    },
    {
        "name": "Ministry of Environment Cambodia (ក្រសួងបរិស្ថាន)",
        "url": "https://www.moe.gov.kh/feed",
        "category": "Environment",
        "tier": 1
    },
    {
        "name": "National Election Committee NEC (គណៈកម្មាធិការជាតិរៀបចំការបោះឆ្នោត)",
        "url": "https://www.nec.gov.kh/khmer/rss.xml",
        "category": "Democracy & Elections",
        "tier": 1
    },
    {
        "name": "National Assembly of Cambodia (រដ្ឋសភាជាតិ)",
        "url": "https://www.nac.org.kh/feed",
        "category": "Parliament",
        "tier": 1
    }
]

# 2. Provincial Administrations & Regional Municipal Desks
PROVINCIAL_ADMIN_FEEDS = [
    {
        "name": "Phnom Penh Capital Hall (រដ្ឋបាលរាជធានីភ្នំពេញ)",
        "url": "https://phnompenh.gov.kh/feed",
        "category": "Capital Administration",
        "tier": 1
    },
    {
        "name": "Siem Reap Provincial Administration (រដ្ឋបាលខេត្តសៀមរាប)",
        "url": "https://siemreap.gov.kh/feed",
        "category": "Provincial Administration",
        "tier": 1
    },
    {
        "name": "Preah Sihanouk Provincial Administration (រដ្ឋបាលខេត្តព្រះសីហនុ)",
        "url": "https://preahsihanouk.gov.kh/feed",
        "category": "Coastal Regional Hub",
        "tier": 1
    },
    {
        "name": "Battambang Provincial Administration (រដ្ឋបាលខេត្តបាត់ដំបង)",
        "url": "https://battambang.gov.kh/feed",
        "category": "Provincial Administration",
        "tier": 1
    },
    {
        "name": "Kampong Cham Provincial Administration (រដ្ឋបាលខេត្តកំពង់ចាម)",
        "url": "https://kampongcham.gov.kh/feed",
        "category": "Provincial Administration",
        "tier": 1
    },
    {
        "name": "Kandal Provincial Administration (រដ្ឋបាលខេត្តកណ្តាល)",
        "url": "https://kandal.gov.kh/feed",
        "category": "Provincial Administration",
        "tier": 1
    },
    {
        "name": "Svay Rieng Border Desk (រដ្ឋបាលខេត្តស្វាយរៀង - ព្រំដែន)",
        "url": "https://svayrieng.gov.kh/feed",
        "category": "Border Regional Desk",
        "tier": 1
    },
    {
        "name": "Koh Kong Maritime Desk (រដ្ឋបាលខេត្តកោះកុង - ដែនសមុទ្រ)",
        "url": "https://kohkong.gov.kh/feed",
        "category": "Maritime Regional Desk",
        "tier": 1
    },
    {
        "name": "Stung Treng Border Desk (រដ្ឋបាលខេត្តស្ទឹងត្រែង - ព្រំដែន)",
        "url": "https://stungtreng.gov.kh/feed",
        "category": "Border Regional Desk",
        "tier": 1
    },
    {
        "name": "Ratanakiri Highland Border Desk (រដ្ឋបាលខេត្តរតនគិរី)",
        "url": "https://ratanakiri.gov.kh/feed",
        "category": "Border Regional Desk",
        "tier": 1
    }
]

# 3. Civil Society, Human Rights, Anti-Corruption & Social Justice
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
    {
        "name": "ADHOC Human Rights Association (សមាគមអាដហុក)",
        "url": "https://adhoc-cambodia.org/feed/",
        "category": "Human Rights & Justice",
        "tier": 1
    },
    {
        "name": "Cambodia Human Rights Committee CHRC (គណៈកម្មាធិការសិទ្ធិមនុស្សកម្ពុជា)",
        "url": "https://chrc.gov.kh/feed",
        "category": "State Human Rights Desk",
        "tier": 1
    }
]

# 4. Leading Cambodian & Global News Agencies
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
        "name": "Fresh News Asia (សារព័ត៌មាន Fresh News)",
        "url": "https://freshnewsasia.com/index.php/en/news-feed.xml",
        "category": "National Media",
        "tier": 1
    },
    {
        "name": "Koh Santepheap Daily (កោះសន្តិភាព)",
        "url": "https://kohsantepheapdaily.com.kh/feed",
        "category": "National Media & Social Trends",
        "tier": 1
    },
    {
        "name": "Kampuchea Thmey Daily (កម្ពុជាថ្មី)",
        "url": "https://www.kampucheathmey.com/feed/",
        "category": "National Media & Social Trends",
        "tier": 1
    },
    {
        "name": "Popular Magazine News (សារព័ត៌មានប្រជាប្រិយ)",
        "url": "https://www.popular.com.kh/feed/",
        "category": "Social & Cultural Media",
        "tier": 1
    },
    {
        "name": "KPT Plus News (សារព័ត៌មាន ខេភីធី ផ្លាស់)",
        "url": "https://kpt-plus.com/feed/",
        "category": "National Media & Breaking News",
        "tier": 1
    },
    {
        "name": "CamboJA News (សមាគមអ្នកសារព័ត៌មានកម្ពុជា)",
        "url": "https://cambojanews.com/feed/",
        "category": "Journalism & Human Rights",
        "tier": 1
    },
    {
        "name": "DAP News (ដើមអំពិល)",
        "url": "https://dap-news.com/feed/",
        "category": "National Media",
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
    all_feeds.extend(PROVINCIAL_ADMIN_FEEDS)
    all_feeds.extend(HUMAN_RIGHTS_JUSTICE_FEEDS)
    all_feeds.extend(MAINSTREAM_NEWS_FEEDS)
    logger.info(f"🌐 [NATIONAL REGISTRY V5.0] Loaded {len(all_feeds)} Institutional Feeds across Cambodia & Global Desks.")
    return all_feeds
