# Mistral 7B 모델을 로컬 환경에서 int4 양자화와 LoRA를 활용하여 파인튜닝
# pip install -U transformers datasets peft accelerate bitsandbytes
# source .venv/bin/activate
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset
from trl import SFTTrainer

# 1. 모델 및 토크나이저 로드 (bfloat16 설정)
model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,  # ✅ bfloat16 설정
    device_map="auto"
)

# 2. LoRA 설정 
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 3. 학습용 데이터셋 로드
dataset = load_dataset("json", data_files="../data/train/train_korean_all.jsonl", split="train")

# 4. 학습 설정
training_args = TrainingArguments(
    output_dir="./mistral-korean-lora",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  
    learning_rate=2e-4,
    num_train_epochs=3,
    fp16=False,
    bf16=True,
    logging_steps=10,
    save_strategy="epoch",
    save_total_limit=1,
    report_to="none"
)

# 5. SFTTrainer로 학습 시작
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    tokenizer=tokenizer,
    args=training_args,
    dataset_text_field="text"
)

trainer.train()
