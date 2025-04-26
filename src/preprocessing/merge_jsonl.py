import os

input_files = [
'korean2024_3월', 'korean2024_6월','korean2024_9월', 'korean2023_3월','korean2023_6월', 'korean2023_9월','korean2022_3월', 'korean2022_6월','korean2022_9월'
]
output_file = "data/train/train_korean_all.jsonl"

with open(output_file, "w", encoding="utf-8") as out_f:
    for fname in input_files:
        with open(f"data/train/train_{fname}.jsonl", "r", encoding="utf-8") as in_f:
            for line in in_f:
                out_f.write(line)

print(f"✅ 총 {len(input_files)}개 파일 병합 완료 → {output_file}")
