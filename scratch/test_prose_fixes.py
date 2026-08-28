import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from khmer_auditor import khmer_auditor
from bot_interactive import SuperSmartTelegramBot

text_with_empty_brackets = """ខេត្តបន្ទាយមានជ័យ៖ ក្រុមអ្នកសម្របសម្រួល (CLG) នៃព្រះរាជាណាចក្រកម្ពុជា បានសម្របសម្រួលជូនក្រុមអ្នកសង្កេតការណ៍អាស៊ានប្រចាំកម្ពុជា (AOT-KH) (-) ដឹកនាំដោយប្រធានបេសកកម្មមកពីសាធារណរដ្ឋហ្វីលីពីន ចុះសង្កេតការណ៍... () គណៈកម្មការចម្រុះខណ្ឌសីមាព្រំដែនគោក () កម្ពុជា-ថៃ... ក្នុងការកសាងតំបន់ព្រំដែនសន្តិភាព មិត្តភាព កិច្ចសហប្រតិបត្តិការ និងការអភិវឌ្ឍប្រកបដោយចីរភាពសម្រាប់ប្រជាជាតិទាំងមូល៕៕"""

_, clean = khmer_auditor.audit_prose_structure("test", text_with_empty_brackets)

print("--- AUDITED OUTPUT ---")
print(clean)
print("----------------------")

assert "(-)" not in clean, "Should strip (-)"
assert "()" not in clean, "Should strip ()"
assert clean.endswith(" ៕"), f"Should end cleanly with single ' ៕', got '{clean[-10:]}'"
assert "៕៕" not in clean and "៕។" not in clean, "Should not contain double closing signs"

print("✅ ALL TESTS PASSED SUCCESSFULLY!")
