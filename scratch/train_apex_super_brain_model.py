"""
====================================================================================================
🏛️ APEX SUPER BRAIN AI — KHMER NEWS LLM FINE-TUNING & HUGGING FACE PUSH SCRIPT
====================================================================================================
Fine-tunes Qwen 2.5 0.5B/1.5B Instruct using QLoRA 4-bit quantization (BitsAndBytes + PEFT) 
for 4-Paragraph Gold Standard Khmer News Rewriting, and pushes trained adapters directly 
to Hugging Face Hub non-interactively.
"""

import os
import sys
import json
import torch
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("FineTuneEngine")

def run_fine_tuning(
    hf_token: str = os.getenv("HF_ACCESS_TOKEN", ""),
    hub_model_id: str = "hemsinath/apex-super-brain-khmer-news",
    dataset_path: str = "data/khmer_news_fine_tuning_dataset.jsonl",
    base_model_name: str = "Qwen/Qwen2.5-0.5B-Instruct"
):
    # 1. Non-Interactive Hugging Face Login
    from huggingface_hub import login
    if hf_token:
        logger.info(f"🔑 [HF LOGIN] Logging in non-interactively to Hugging Face Hub...")
        login(token=hf_token, write_permission=True)
    else:
        logger.warning("⚠️ No HF_ACCESS_TOKEN found in environment. Make sure token is set.")

    # 2. Prepare Sample Khmer Gold Standard Dataset if file missing
    if not os.path.exists(dataset_path):
        os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
        logger.info(f"📝 Creating sample Khmer Gold Standard dataset at {dataset_path}...")
        sample_data = [
            {
                "instruction": "សរសេរអត្ថបទព័ត៌មានឡើងវិញជាភាសាខ្មែរផ្លូវការ ៤ កថាខណ្ឌ ជាមួយ Dynamic Dateline និងវិភាគរដ្ឋធម្មនុញ្ញ មាត្រា ៥១",
                "input": "ប្រភព៖ AKP | ទីតាំង៖ សៀមរាប | ខ្លឹមសាររ៉ូ៖ អាជ្ញាធរជាតិអប្សរាបើកការដ្ឋានជួសជុលប្រាសាទបុរាណ...",
                "output": "ខេត្តសៀមរាប៖ អាជ្ញាធរជាតិអប្សរាបានប្រកាសបើកការដ្ឋានជួសជុល និងអភិរក្សប្រាសាទបុរាណក្នុងតំបន់រមណីយដ្ឋានអង្គរ...\n\nការងារអភិរក្សបេតិកភណ្ឌជាតិនេះ រក្សាបាននូវអត្តសញ្ញាណវប្បធម៌ និងទាក់ទាញទេសចរអន្តរជាតិមកទស្សនាកម្ពុជា...\n\nសកម្មភាពនេះឆ្លុះបញ្ចាំងពីការអនុវត្ត មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ក្នុងការការពារបេតិកភណ្ឌជាតិ និងអភិវឌ្ឍន៍សង្គម...\n\nអាជ្ញាធររំពឹងថាគម្រោងនេះនឹងបញ្ចប់ដោយជោគជ័យនាពេលឆាប់ៗខាងមុខនេះ៕"
            },
            {
                "instruction": "សរសេរអត្ថបទព័ត៌មានឡើងវិញជាភាសាខ្មែរផ្លូវការ ៤ កថាខណ្ឌ ជាមួយ Dynamic Dateline និងវិភាគរដ្ឋធម្មនុញ្ញ មាត្រា ៥១",
                "input": "ប្រភព៖ ក្រសួងការពារជាតិ | ទីតាំង៖ ភ្នំពេញ | ខ្លឹមសាររ៉ូ៖ កម្ពុជាបញ្ជូនកងទ័ពមួកខៀវទៅបំពេញបេសកកម្ម...",
                "output": "រាជធានីភ្នំពេញ៖ ក្រសួងការពារជាតិកម្ពុជាបានរៀបចំពិធីបញ្ជូនកងទ័ពមួកខៀវកម្ពុជាទៅបំពេញបេសកកម្មរក្សាសន្តិភាព...\n\nបេសកកម្មអន្តរជាតិនេះស្តែងឱ្យឃើញពីការចូលរួមចំណែកយ៉ាងសកម្មរបស់កម្ពុជាក្នុងក្របខ័ណ្ឌអង្គការសហប្រជាជាតិ...\n\nការបំពេញភារកិច្ចនេះស្របតាមស្មារតី មាត្រា ៥១ នៃរដ្ឋធម្មនុញ្ញ ក្នុងការលើកកម្ពស់សន្តិភាព និងកិច្ចសហប្រតិបត្តិការ...\n\nថ្នាក់ដឹកនាំបានជូនពរកងទ័ពទាំងអស់ឱ្យទទួលបានជោគជ័យក្នុងការបំពេញភារកិច្ចការពារសន្តិភាពពិភពលោក៕"
            }
        ]
        with open(dataset_path, "w", encoding="utf-8") as f:
            for item in sample_data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # 3. Load Quantization Config & Model
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import LoraConfig, get_peft_model
    from datasets import load_dataset
    from trl import SFTTrainer, SFTConfig

    logger.info(f"🤖 Loading Base Model: {base_model_name} with 4-bit NF4 Quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    )

    tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    device_map = "auto" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        quantization_config=bnb_config if torch.cuda.is_available() else None,
        device_map=device_map,
        trust_remote_code=True,
    )

    # 4. LoRA PEFT Config
    lora_config = LoraConfig(
        r=8,
        lora_alpha=32,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.1,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    logger.info("✨ LoRA Adapter configured successfully!")

    # 5. Load Dataset
    dataset = load_dataset("json", data_files=dataset_path)

    def formatting_prompts_func(example):
        output_texts = []
        for inst, inp, out in zip(example['instruction'], example['input'], example['output']):
            text = f"<|im_start|>system\n{inst}<|im_end|>\n<|im_start|>user\n{inp}<|im_end|>\n<|im_start|>assistant\n{out}<|im_end|>"
            output_texts.append(text)
        return output_texts

    # 6. SFT Training Config
    sft_config = SFTConfig(
        output_dir="./results_apex_super_brain",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        optim="paged_adamw_8bit" if torch.cuda.is_available() else "adamw_torch",
        save_steps=50,
        logging_steps=5,
        learning_rate=2e-4,
        fp16=torch.cuda.is_available(),
        push_to_hub=bool(hf_token),
        hub_model_id=hub_model_id,
        report_to="none",
        dataset_text_field="text"
    )

    trainer = SFTTrainer(
        model=model,
        args=sft_config,
        train_dataset=dataset["train"],
        formatting_func=formatting_prompts_func,
        tokenizer=tokenizer,
    )

    logger.info("🚀 Starting Model Fine-Tuning Training...")
    trainer.train()

    # 7. Push to Hugging Face Hub
    if hf_token:
        logger.info(f"📤 Pushing Fine-Tuned Model Adapters to Hugging Face Hub ({hub_model_id})...")
        trainer.push_to_hub()
        tokenizer.push_to_hub(hub_model_id)
        logger.info(f"✅ SUCCESS! Model published to https://huggingface.co/{hub_model_id}")

if __name__ == "__main__":
    run_fine_tuning()
