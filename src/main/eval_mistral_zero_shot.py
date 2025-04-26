import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re

# 모델 로드
model_id = "davidkim205/komt-mistral-7b-v1"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="auto", 
    torch_dtype=torch.float16
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 평가용 데이터 로드
with open("../data/processed/korean2025.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = 0
scores = 0
correct = 0

for item in data:
    paragraph = item["paragraph"]
    for prob in item["problems"]:
        question = prob["question"]
        question_plus = prob.get("question_plus", "")
        choices = prob["choices"]
        score = prob["score"]
        answer = prob["answer"]  # already 1~5

        # 프롬프트 구성
        prompt = f"### Paragraph\n{paragraph.strip()}\n\n"
        prompt += f"### Question\n{question.strip()}"
        if question_plus:
            prompt += f"\n{question_plus.strip()}"
        prompt += "\n\n### Choices\n"
        for i, c in enumerate(choices):
            prompt += f"{i+1}. {c.strip()}\n"
        prompt += "\n### Answer\nAnswer with only the number 1 to 5. No text, no punctuation, just the number:\n"

        # 모델 추론
        output = generator(prompt, max_new_tokens=5, do_sample=False)[0]["generated_text"]
        
        generated_only = output[len(prompt):].strip()

        # 숫자만 추출
        match = re.search(r"\b[1-5]\b", generated_only)
        predicted_num = int(match.group()) if match else -1

        total += 1
        if predicted_num == answer:
            correct += 1
            scores += score

        print(f"[{total}] 정답: {answer}, 예측: {predicted_num}, 원출력: '{generated_only}'")


print(f"\n✅ 총 {total}문제 중 {correct}개 정답\n({correct/total*100:.2f}%) 정확도\n점수 {scores} 점")

# source .venv/bin/activate