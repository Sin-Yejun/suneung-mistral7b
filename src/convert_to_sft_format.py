import json
import os

def convert_korean_json_to_sft_format(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    output = []
    for item in data:
        paragraph = item["paragraph"]
        for prob in item["problems"]:
            question = prob["question"]
            question_plus = prob.get("question_plus", "")
            choices = prob["choices"]
            answer = prob["answer"]

            # 텍스트 형식 구성
            text = f"### 지문\n{paragraph.strip()}\n\n"
            text += f"### 질문\n{question.strip()}"
            if question_plus:
                text += f"\n{question_plus.strip()}"
            text += "\n\n### 선택지\n"
            for i, c in enumerate(choices):
                text += f"{i+1}. {c.strip()}\n"
            text += f"\n### 정답\n{answer}"

            output.append({"text": text.strip()})

    # JSONL로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in output:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ 변환 완료: {len(output)}개 항목 → {output_path}")

# 사용 예시
if __name__ == "__main__":
    input_file = "data/processed/korean2024.json"
    output_file = "data/train/train_korean2024.jsonl"
    convert_korean_json_to_sft_format(input_file, output_file)
