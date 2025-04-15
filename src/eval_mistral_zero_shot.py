import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# 모델 로드
model_id = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, 
    device_map="auto", 
    torch_dtype=torch.float16
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0)

# 평가용 데이터 로드
with open("data/processed/korean2025.json", "r", encoding="utf-8") as f:
    data = json.load(f)

total = 0
correct = 0

for item in data:
    paragraph = item["paragraph"]
    for prob in item["problems"]:
        question = prob["question"]
        question_plus = prob.get("question_plus", "")
        choices = prob["choices"]
        answer = prob["answer"]  # already 1~5

        # 프롬프트 구성
        prompt = f"### 지문\n{paragraph.strip()}\n\n"
        prompt += f"### 질문\n{question.strip()}"
        if question_plus:
            prompt += f"\n{question_plus.strip()}"
        prompt += "\n\n### 선택지\n"
        for i, c in enumerate(choices):
            prompt += f"{i+1}. {c.strip()}\n"
        prompt += "\n### 정답\n"

        # 모델 추론
        output = generator(prompt, max_new_tokens=5, do_sample=False)[0]["generated_text"]
        predicted = output.strip().split("### 정답")[-1].strip().split()[0]

        try:
            predicted_num = int(predicted)
        except ValueError:
            predicted_num = -1  # 예측 실패

        total += 1
        if predicted_num == answer:
            correct += 1

        print(f"[{total}] 정답: {answer}, 예측: {predicted_num}")

print(f"\n✅ 총 {total}문제 중 {correct}개 정답 ({correct/total*100:.2f}%) 정확도")

