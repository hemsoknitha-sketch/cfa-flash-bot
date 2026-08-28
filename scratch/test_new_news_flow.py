import sys
import os
import asyncio
import logging
import time

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TestNewNewsFlow")

from main import process_news, pipeline_engine

async def run_test():
    logger.info("--- TESTING BRAND NEW UNSEEN NEWS ITEM PIPELINE ---")
    
    unique_time_id = str(int(time.time()))
    fresh_title = f"ក្រសួងព័ត៌មាន បើកយុទ្ធនាការបច្ចេកវិទ្យាឌីជីថលថ្មី ឆ្នាំ២០២៦ {unique_time_id}"
    fresh_content = f"រាជធានីភ្នំពេញ៖ នៅថ្ងៃទី២៤ ខែសីហា ឆ្នាំ២០២៦ ក្រសួងព័ត៌មាន នៃព្រះរាជាណាចក្រកម្ពុជា បានប្រកាសដាក់ឱ្យអនុវត្តជាផ្លូវការនូវប្រព័ន្ធបច្ចេកវិទ្យាព័ត៌មានឌីជីថលជំនាន់ថ្មី ដើម្បីពង្រឹងប្រសិទ្ធភាពនៃការផ្សព្វផ្សាយព័ត៌មានពិត និងទប់ស្កាត់ព័ត៌មានមិនពិតទូទាំងប្រទេស។ ឯកឧត្តម រដ្ឋមន្ត្រី បានសង្កត់ធ្ងន់ពីសារៈសំខាន់នៃការប្រកាន់ខ្ជាប់នូវក្រមសីលធម៌សារព័ត៌មាន ស្របតាមមាត្រា ៣១ និងមាត្រា ៤១ នៃរដ្ឋធម្មនុញ្ញ នៃព្រះរាជាណាចក្រកម្ពុជា ក្នុងការការពារសិទ្ធិ និងផលប្រយោជន៍ស្របច្បាប់របស់ប្រជាពលរដ្ឋគ្រប់រូប {unique_time_id}៕"

    full_text = f"{fresh_title} - {fresh_content}"
    news_id = f"test_fresh_{unique_time_id}"

    await process_news(
        news_text=full_text,
        news_id=news_id,
        source_name="ក្រសួងព័ត៌មានកម្ពុជា",
        url="https://www.information.gov.kh/news/fresh_test",
        timestamp=time.time()
    )

if __name__ == "__main__":
    asyncio.run(run_test())
