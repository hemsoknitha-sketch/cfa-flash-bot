import os
import sys
import asyncio
import logging

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TestBannerCartoon")

from banner_engine import banner_engine

async def main():
    logger.info("--- TESTING AI DIGITAL CARTOON DRAWING BANNER GENERATOR ---")
    headline = "កម្ពុជាបន្តបញ្ជូនកងទ័ពមួកខៀវ ២០០នាក់ ទៅបំពេញបេសកកម្មរក្សាសន្តិភាពអង្គការសហប្រជាជាតិ"
    visual_prompt = "Cambodian UN peacekeeper soldiers wearing blue helmets marching heroically in Africa, digital cartoon drawing editorial art style"
    
    banner_file = await banner_engine.generate_banner_image(
        headline=headline,
        category_title="ព័ត៌មានយោធា & សន្តិភាព",
        badge_label="🟢 VERIFIED 95% — ព័ត៌មានផ្លូវការ",
        badge_color="green",
        visual_prompt=visual_prompt
    )
    
    logger.info(f"✅ Banner generated successfully: {banner_file} (Size: {os.path.getsize(banner_file)} bytes)")
    print(f"SUCCESS: Generated cartoon banner '{banner_file}'!")

if __name__ == "__main__":
    asyncio.run(main())
