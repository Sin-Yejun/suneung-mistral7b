import os

input_files = [
    "data/train/train_korean2022.jsonl",
    "data/train/train_korean2023.jsonl",
    "data/train/train_korean2024.jsonl"
]

output_file = "data/train/train_korean_all.jsonl"

with open(output_file, "w", encoding="utf-8") as out_f:
    for fname in input_files:
        with open(fname, "r", encoding="utf-8") as in_f:
            for line in in_f:
                out_f.write(line)

print(f"✅ 총 {len(input_files)}개 파일 병합 완료 → {output_file}")
