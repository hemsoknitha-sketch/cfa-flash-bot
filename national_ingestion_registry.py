"""
National Institutional Ingestion Registry V8.0 (70+ Premier Desks)
Broadens news scanning coverage across:
1. Cambodian State Ministries & National Institutions (MoINFO, AKP, MoFAIC, MoD, MoI, MoJ, OCM, Assembly, Senate, ACU, NEC, MEF, MPWT, MoEYS, MoH, MAFF, MoC, MoT, MLVT, MCS).
2. All 25 Cambodian Provincial Administrations & Border/Coastal Desks.
3. Civil Society Organizations, Human Rights, Anti-Corruption & Social Justice (CCHR, LICADHO, ADHOC, TI Cambodia, CHRC).
4. Leading Cambodian Digital Media & Global News Agencies (BBC, CNN, Al Jazeera, CNA, SCMP, Bangkok Post, VNExpress, AP, Reuters, NYT, DW, France24, Fresh News, ThmeyThmey, Koh Santepheap, Kampuchea Thmey, Sabay).
"""

import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# 1. State Ministries & National Institutions (20 Feeds)
MINISTRY_INSTITUTION_FEEDS = [
    {"name": "Ministry of National Defence Cambodia (ក្រសួងការពារជាតិ)", "url": "https://www.mod.gov.kh/feed", "category": "National Defence", "tier": 1},
    {"name": "AKP - Agence Kampuchea Presse (ព័ត៌មានរដ្ឋផ្លូវការ)", "url": "https://www.akp.gov.kh/feed", "category": "State News Agency", "tier": 1},
    {"name": "Ministry of Information Cambodia (ក្រសួងព័ត៌មាន)", "url": "https://www.information.gov.kh/feed", "category": "Ministry", "tier": 1},
    {"name": "Ministry of Foreign Affairs & Intl Cooperation (ក្រសួងការបរទេស)", "url": "https://www.mfaic.gov.kh/feed", "category": "Diplomacy", "tier": 1},
    {"name": "Anti-Corruption Unit ACU (អង្គភាពប្រឆាំងអំពើពុករលួយ)", "url": "https://acu.gov.kh/feed", "category": "Anti-Corruption", "tier": 1},
    {"name": "Office of the Council of Ministers (ទីស្តីការគណៈរដ្ឋមន្ត្រី)", "url": "https://pressocm.gov.kh/feed", "category": "Cabinet Office", "tier": 1},
    {"name": "Ministry of Interior Cambodia (ក្រសួងមហាផ្ទៃ)", "url": "https://www.interior.gov.kh/feed", "category": "Internal Security", "tier": 1},
    {"name": "Ministry of Justice Cambodia (ក្រសួងយុត្តិធម៌)", "url": "https://www.moj.gov.kh/feed", "category": "Judicial System", "tier": 1},
    {"name": "Ministry of Economy & Finance (ក្រសួងសេដ្ឋកិច្ច និងហិរញ្ញវត្ថុ)", "url": "https://www.mef.gov.kh/feed", "category": "Economy & Finance", "tier": 1},
    {"name": "Ministry of Environment Cambodia (ក្រសួងបរិស្ថាន)", "url": "https://www.moe.gov.kh/feed", "category": "Environment", "tier": 1},
    {"name": "National Election Committee NEC (គណៈកម្មាធិការជាតិរៀបចំការបោះឆ្នោត)", "url": "https://www.nec.gov.kh/khmer/rss.xml", "category": "Democracy & Elections", "tier": 1},
    {"name": "National Assembly of Cambodia (រដ្ឋសភាជាតិ)", "url": "https://www.nac.org.kh/feed", "category": "Parliament", "tier": 1},
    {"name": "Ministry of Public Works and Transport MPWT (ក្រសួងសាធារណការ)", "url": "https://www.mpwt.gov.kh/feed", "category": "Infrastructure", "tier": 1},
    {"name": "Ministry of Education, Youth and Sport MoEYS (ក្រសួងអប់រំ)", "url": "https://moeys.gov.kh/feed", "category": "Education", "tier": 1},
    {"name": "Ministry of Health Cambodia (ក្រសួងសុខាភិបាល)", "url": "https://moh.gov.kh/feed", "category": "Public Health", "tier": 1},
    {"name": "Ministry of Agriculture MAFF (ក្រសួងកសិកម្ម)", "url": "https://maff.gov.kh/feed", "category": "Agriculture", "tier": 1},
    {"name": "Ministry of Commerce MoC (ក្រសួងពាណិជ្ជកម្ម)", "url": "https://moc.gov.kh/feed", "category": "Commerce & Trade", "tier": 1},
    {"name": "Ministry of Tourism MoT (ក្រសួងទេសចរណ៍)", "url": "https://tourismcambodia.org/feed", "category": "Tourism", "tier": 1},
    {"name": "Ministry of Labor MLVT (ក្រសួងការងារ និងបណ្តុះបណ្តាលវិជ្ជាជីវៈ)", "url": "https://mlvt.gov.kh/feed", "category": "Labor & Employment", "tier": 1},
    {"name": "Ministry of Civil Service MCS (ក្រសួងមុខងារសាធារណៈ)", "url": "https://mcs.gov.kh/feed", "category": "Public Service", "tier": 1}
]

# 2. All 25 Cambodian Provincial Administrations (25 Feeds)
PROVINCIAL_ADMIN_FEEDS = [
    {"name": "Phnom Penh Capital Hall (រដ្ឋបាលរាជធានីភ្នំពេញ)", "url": "https://phnompenh.gov.kh/feed", "category": "Capital Administration", "tier": 1},
    {"name": "Siem Reap Provincial Administration (រដ្ឋបាលខេត្តសៀមរាប)", "url": "https://siemreap.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Preah Sihanouk Provincial Administration (រដ្ឋបាលខេត្តព្រះសីហនុ)", "url": "https://preahsihanouk.gov.kh/feed", "category": "Coastal Regional Hub", "tier": 1},
    {"name": "Battambang Provincial Administration (រដ្ឋបាលខេត្តបាត់ដំបង)", "url": "https://battambang.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Kampong Cham Provincial Administration (រដ្ឋបាលខេត្តកំពង់ចាម)", "url": "https://kampongcham.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Kandal Provincial Administration (រដ្ឋបាលខេត្តកណ្តាល)", "url": "https://kandal.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Svay Rieng Border Desk (រដ្ឋបាលខេត្តស្វាយរៀង - ព្រំដែន)", "url": "https://svayrieng.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Koh Kong Maritime Desk (រដ្ឋបាលខេត្តកោះកុង - ដែនសមុទ្រ)", "url": "https://kohkong.gov.kh/feed", "category": "Maritime Regional Desk", "tier": 1},
    {"name": "Stung Treng Border Desk (រដ្ឋបាលខេត្តស្ទឹងត្រែង - ព្រំដែន)", "url": "https://stungtreng.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Ratanakiri Highland Border Desk (រដ្ឋបាលខេត្តរតនគិរី)", "url": "https://ratanakiri.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Kampong Speu Provincial Administration (រដ្ឋបាលខេត្តកំពង់ស្ពឺ)", "url": "https://kampongspeu.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Kampong Chhnang Provincial Administration (រដ្ឋបាលខេត្តកំពង់ឆ្នាំង)", "url": "https://kampongchhnang.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Kampong Thom Provincial Administration (រដ្ឋបាលខេត្តកំពង់ធំ)", "url": "https://kampongthom.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Kampot Coastal Desk (រដ្ឋបាលខេត្តកំពត)", "url": "https://kampot.gov.kh/feed", "category": "Coastal Regional Hub", "tier": 1},
    {"name": "Kep Coastal Desk (រដ្ឋបាលខេត្តកែប)", "url": "https://kep.gov.kh/feed", "category": "Coastal Regional Hub", "tier": 1},
    {"name": "Kratie Riverine Desk (រដ្ឋបាលខេត្តក្រចេះ)", "url": "https://kratie.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Mondulkiri Highland Desk (រដ្ឋបាលខេត្តមណ្ឌលគិរី)", "url": "https://mondulkiri.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Oddar Meanchey Border Desk (រដ្ឋបាលខេត្តឧត្តរមានជ័យ)", "url": "https://oddarmeanchey.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Pailin Border Desk (រដ្ឋបាលខេត្តប៉ៃលិន)", "url": "https://pailin.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Prey Veng Provincial Administration (រដ្ឋបាលខេត្តព្រៃវែង)", "url": "https://preyveng.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Pursat Provincial Administration (រដ្ឋបាលខេត្តពោធិ៍សាត់)", "url": "https://pursat.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Preah Vihear Border Desk (រដ្ឋបាលខេត្តព្រះវិហារ)", "url": "https://preahvihear.gov.kh/feed", "category": "Border Regional Desk", "tier": 1},
    {"name": "Takeo Provincial Administration (រដ្ឋបាលខេត្តតាកែវ)", "url": "https://takeo.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Tboung Khmum Provincial Administration (រដ្ឋបាលខេត្តត្បូងឃ្មុំ)", "url": "https://tboungkhmum.gov.kh/feed", "category": "Provincial Administration", "tier": 1},
    {"name": "Banteay Meanchey Border Desk (រដ្ឋបាលខេត្តបន្ទាយមានជ័យ)", "url": "https://banteaymeanchey.gov.kh/feed", "category": "Border Regional Desk", "tier": 1}
]

# 3. Civil Society, Human Rights, Anti-Corruption & Social Justice (5 Feeds)
HUMAN_RIGHTS_JUSTICE_FEEDS = [
    {"name": "Transparency International Cambodia (គណនេយ្យភាពសង្គម & ប្រឆាំងអំពើពុករលួយ)", "url": "https://ticambodia.org/feed/", "category": "Anti-Corruption & Transparency", "tier": 1},
    {"name": "CCHR - Cambodian Center for Human Rights (សិទ្ធិមនុស្ស & យុត្តិធម៌សង្គម)", "url": "https://cchrcambodia.org/index_old.php?url=feed.php", "category": "Human Rights", "tier": 1},
    {"name": "LICADHO Cambodia (សិទ្ធិមនុស្ស & សមភាពសង្គម)", "url": "https://www.licadho-cambodia.org/rss.xml", "category": "Human Rights", "tier": 1},
    {"name": "ADHOC Human Rights Association (សមាគមអាដហុក)", "url": "https://adhoc-cambodia.org/feed/", "category": "Human Rights & Justice", "tier": 1},
    {"name": "Cambodia Human Rights Committee CHRC (គណៈកម្មាធិការសិទ្ធិមនុស្សកម្ពុជា)", "url": "https://chrc.gov.kh/feed", "category": "State Human Rights Desk", "tier": 1}
]

# 4. Leading Cambodian Digital Media & Global 24/7 News Outlets (25 Feeds)
MAINSTREAM_NEWS_FEEDS = [
    {"name": "Khmer Times News", "url": "https://www.khmertimeskh.com/feed/", "category": "National Media", "tier": 1},
    {"name": "Phnom Penh Post News", "url": "https://www.phnompenhpost.com/rss.xml", "category": "National Media", "tier": 1},
    {"name": "ThmeyThmey News (សារព័ត៌មានថ្មីៗ)", "url": "https://thmeythmey.com/rss/latest.xml", "category": "National Media", "tier": 1},
    {"name": "Fresh News Asia (សារព័ត៌មាន Fresh News 24/7)", "url": "https://freshnewsasia.com/index.php/en/news-feed.xml", "category": "National Media", "tier": 1},
    {"name": "Koh Santepheap Daily (កោះសន្តិភាព 24/7)", "url": "https://kohsantepheapdaily.com.kh/feed", "category": "National Media & Social Trends", "tier": 1},
    {"name": "Kampuchea Thmey Daily (កម្ពុជាថ្មី)", "url": "https://www.kampucheathmey.com/feed/", "category": "National Media & Social Trends", "tier": 1},
    {"name": "Popular Magazine News (សារព័ត៌មានប្រជាប្រិយ)", "url": "https://www.popular.com.kh/feed/", "category": "Social & Cultural Media", "tier": 1},
    {"name": "KPT Plus News (សារព័ត៌មាន ខេភីធី ផ្លាស់)", "url": "https://kpt-plus.com/feed/", "category": "National Media & Breaking News", "tier": 1},
    {"name": "CamboJA News (សមាគមអ្នកសារព័ត៌មានកម្ពុជា)", "url": "https://cambojanews.com/feed/", "category": "Journalism & Human Rights", "tier": 1},
    {"name": "DAP News (ដើមអំពិល)", "url": "https://dap-news.com/feed/", "category": "National Media", "tier": 1},
    {"name": "RFI Khmer (វិទ្យុបារាំងអន្តរជាតិ)", "url": "https://www.rfi.fr/km/rss", "category": "International Khmer Media", "tier": 1},
    {"name": "VOA Khmer (វិទ្យុសម្លេងសហរដ្ឋអាមេរិក)", "url": "https://khmer.voanews.com/api/z-$q_m-t_q-m", "category": "International Khmer Media", "tier": 1},
    
    # Premier Global 24/7 News Agencies
    {"name": "BBC World News 24/7", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "category": "Global Media", "tier": 1},
    {"name": "CNN International World News 24/7", "url": "http://rss.cnn.com/rss/edition_world.rss", "category": "Global Media", "tier": 1},
    {"name": "Al Jazeera English News 24/7", "url": "https://www.aljazeera.com/xml/rss/all.xml", "category": "Global Media", "tier": 1},
    {"name": "Channel NewsAsia CNA 24/7", "url": "https://www.channelnewsasia.com/api/v1/rss-outbound/rssnews/cna-asia.xml", "category": "ASEAN & Global Media", "tier": 1},
    {"name": "South China Morning Post SCMP 24/7", "url": "https://www.scmp.com/rss/91/feed", "category": "Asia-Pacific Media", "tier": 1},
    {"name": "Bangkok Post Regional News 24/7", "url": "https://www.bangkokpost.com/rss/data/topstories.xml", "category": "Regional ASEAN Desk", "tier": 1},
    {"name": "VNExpress International 24/7", "url": "https://e.vnexpress.net/rss/news.rss", "category": "Regional ASEAN Desk", "tier": 1},
    {"name": "Associated Press AP World News 24/7", "url": "https://feedx.net/rss/apnews.xml", "category": "Global Media", "tier": 1},
    {"name": "Reuters World News 24/7", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml", "category": "Global Media", "tier": 1},
    {"name": "New York Times World News 24/7", "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "category": "Global Media", "tier": 1},
    {"name": "Deutsche Welle DW World 24/7", "url": "https://rss.dw.com/rdf/rss-en-world", "category": "European Global Desk", "tier": 1},
    {"name": "France 24 International News 24/7", "url": "https://www.france24.com/en/rss", "category": "European Global Desk", "tier": 1}
]

# 5. Influential Social Media Journalists & Digital Desks (5 Feeds)
INFLUENTIAL_SOCIAL_JOURNALIST_DESKS = [
    {"name": "Pheng Vannak News (អ្នកសារព័ត៌មានលោក ផែង វណ្ណះ)", "url": "https://www.facebook.com/pvannakblue", "category": "Social Media Journalist & Breaking News", "tier": 1},
    {"name": "News Today Khmer (សារព័ត៌មាន News Today Khmer)", "url": "https://www.facebook.com/newstodaykhmer", "category": "Social Media Digital News", "tier": 1},
    {"name": "VOD Khmer (សារព័ត៌មាន VOD Khmer)", "url": "https://www.facebook.com/VODKhmer", "category": "Social Media Digital News", "tier": 1},
    {"name": "RFA Khmer (វិទ្យុអាស៊ីសេរី)", "url": "https://www.facebook.com/rfacambodia", "category": "Social Media International News", "tier": 1},
    {"name": "Social Media Journalist Desk (អ្នកសារព័ត៌មានសង្គមឌីជីថល)", "url": "https://www.facebook.com/profile.php?id=61568942406243", "category": "Social Media Journalist & Breaking News", "tier": 1}
]

def get_all_national_feeds() -> List[Dict[str, Any]]:
    """Combines all national institutional, provincial, civil society, news, and social journalist desks."""
    all_feeds = []
    all_feeds.extend(MINISTRY_INSTITUTION_FEEDS)
    all_feeds.extend(PROVINCIAL_ADMIN_FEEDS)
    all_feeds.extend(HUMAN_RIGHTS_JUSTICE_FEEDS)
    all_feeds.extend(MAINSTREAM_NEWS_FEEDS)
    all_feeds.extend(INFLUENTIAL_SOCIAL_JOURNALIST_DESKS)
    logger.info(f"🌐 [NATIONAL REGISTRY V8.0] Loaded {len(all_feeds)} Institutional & Global 24/7 Feeds across Cambodia & World Desks.")
    return all_feeds
