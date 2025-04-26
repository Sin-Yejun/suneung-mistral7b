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
            solution = prob["solution"]

            # 텍스트 형식 구성
            text = "<|user|>\n"
            text += f"### Paragrap\n{paragraph.strip()}\n\n"
            text += f"### Question\n{question.strip()}"
            if question_plus:
                text += f"\n{question_plus.strip()}"
            text += "\n\n### Choices\n"
            for i, c in enumerate(choices):
                text += f"{i+1}. {c.strip()}\n"
            text += f"<|assistant|>\n\n### Answer\n{answer}\n"
            text += f"### Reason\n{solution}\n"
            output.append({"text": text.strip()})

    # JSONL로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in output:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"✅ 변환 완료: {len(output)}개 항목 → {output_path}")

# 사용 예시
if __name__ == "__main__":
    file_list = ['korean2024_3월', 'korean2024_6월',
                 'korean2024_9월', 'korean2023_3월',
                 'korean2023_6월', 'korean2023_9월',
                 'korean2022_3월', 'korean2022_6월',
                 'korean2022_9월']
    for file in file_list:
        input_file = f"data/processed/json/{file}.json"
        output_file = f"data/train/train_{file}.jsonl"
        convert_korean_json_to_sft_format(input_file, output_file)
