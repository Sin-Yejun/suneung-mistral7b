import re

# 1. 텍스트 파일 읽기
with open("data/processed/txt/해설/해설 2024_3월.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# 2. 각 줄마다 정규식으로 앞부분 제거
processed_lines = []
for line in lines:
    cleaned_line = re.sub(r"^\d+\.\s*\[출제의도\]\s*", "", line).strip()
    processed_lines.append(cleaned_line)

# 3. 다시 텍스트 파일로 저장
with open("data/processed/txt/해설/해설 2024_3월.txt", "w", encoding="utf-8") as f:
    for line in processed_lines:
        f.write(line + '\n')
