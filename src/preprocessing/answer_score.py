import json

# 1. 수정할 파일 경로
file_path = "data/processed/json/korean2022_9월.json"  # 원본 파일 경로
modified_path = "data/processed/json/korean2022_9월.json"  # 수정본 저장 경로

# 2. 정답과 점수 배열
answers = [
    1,4,1,3,1,
    5,5,3,1,2,
    4,2,4,2,5,
    5,1,4,2,3,
    4,1,4,5,5,
    4,3,5,4,3,
    3,4,3,2,4,
    4,3,1,2,2,
    5,2,1,5,2
]
scores = [
    2, 3, 2, 2, 2,    # 1 ~ 5
    2, 2, 3, 2, 2,    # 6 ~ 10
    2, 2, 3, 2, 2,    # 11 ~ 15
    3, 2, 2, 2, 2,    # 16 ~ 20
    3, 2, 3, 2, 2,    # 21 ~ 25
    2, 2, 2, 2, 2,    # 26 ~ 30
    3, 2, 2, 3, 2,    # 31 ~ 35
    2, 2, 2, 2, 3,    # 36 ~ 40
    2, 2, 2, 2, 3     # 41 ~ 45
]



# 3. JSON 파일 불러오기
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 4. answers와 scores를 순서대로 각 문제에 반영
index = 0
for section in data:
    for problem in section["problems"]:
        if index < len(answers):
            problem["answer"] = answers[index]
            problem["score"] = scores[index]
            index += 1

# 5. 수정된 JSON 저장
with open(modified_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 수정 완료! 저장 위치: {modified_path}")
