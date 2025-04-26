import os
import re
import json

def extract_all_question_sets_fixed(text):
    """
    텍스트 내 여러 [1~3], [4~7] 같은 묶음을 모두 찾아
    각각 id, paragraph, problems 형태로 추출하되,
    실제 문제 번호(start~end)에 맞춰 각 묶음별 문제를 정확히 추출한다.
    """
    answers = [
        3, 4, 5, 4, 5, 3, 2, 1, 2, 3,
        1, 5, 3, 1, 2, 2, 3, 2, 4, 1,
        4, 4, 5, 2, 2, 1, 1, 4, 3, 5,
        4, 3, 5, 2, 2, 4, 3, 4, 5, 4,
        3, 1, 1, 5, 2
    ]

    scores = [
        2, 2, 3, 2, 2,    # 1 ~ 5
        2, 2, 3, 2, 2,    # 6 ~ 10
        2, 2, 3, 2, 2,    # 11 ~ 15
        3, 2, 2, 2, 2,    # 16 ~ 20
        3, 2, 2, 2, 3,    # 21 ~ 25
        2, 2, 2, 2, 2,    # 26 ~ 30
        3, 2, 2, 3, 2,    # 31 ~ 35
        2, 2, 2, 2, 3,     # 36 ~ 40
        2, 2, 2, 2, 3     # 41 ~ 45 (추가)
    ]



    # 전처리
    cleaned_text = re.sub(r'\s+', ' ', text)
    cleaned_text = re.sub(r'\[\d+점\]', '', cleaned_text)
    cleaned_text = re.sub(r'\(cid:\d+\)', '', cleaned_text)

    # ID 블록 모두 찾기
    id_block_pattern = r'(\[\d+\s*(~|～)\s*\d+\][^.\n]*\.)'
    id_blocks = list(re.finditer(id_block_pattern, cleaned_text))

    results = []

    for idx, match in enumerate(id_blocks):
        id_full = match.group(1)
        id_val = re.search(r'\[(\d+)\s*(?:~|～)\s*(\d+)\]', id_full)
        if not id_val:
            continue

        start_num = int(id_val.group(1))
        end_num = int(id_val.group(2))
        id_str = f"{start_num}～{end_num}"

        start = match.end()
        end = id_blocks[idx + 1].start() if idx + 1 < len(id_blocks) else len(cleaned_text)
        section_text = cleaned_text[start:end]

        # 문제 시작 전까지를 paragraph로
        para_to_q_start = re.search(rf'{start_num}\.', section_text)
        if not para_to_q_start:
            print(f"[{id_str}] 문제 시작점 찾기 실패")
            continue

        paragraph = section_text[:para_to_q_start.start()].strip()
        remaining_text = section_text[para_to_q_start.start():]

        # 문제 블록 추출 (start_num부터 end_num까지)
        question_blocks = []
        for i in range(start_num, end_num + 1):
            if i < end_num:
                pattern = rf"{i}\.\s*(.*?)(?={i+1}\.\s*|\[\d+\s*(?:~|～)\s*\d+\])"
            else:
                pattern = rf"{i}\.\s*(.*)"
            match = re.search(pattern, remaining_text)
            if match:
                question_blocks.append((i, match.group(1).strip()))
            else:
                print(f"[{id_str}] {i}번 문제를 찾지 못했습니다.")

        problems = []
        for number, block in question_blocks:
            question_match = re.match(r"(.*?\?)", block)
            if not question_match:
                print(f"{id_str} - {number}번 질문에서 물음표 없음")
                continue

            question_text = question_match.group(1).strip()
            rest = block[question_match.end():].strip()

            choice_marker = re.search(r'①', rest)
            if choice_marker:
                question_plus = rest[:choice_marker.start()].strip() or None
                choices_text = rest[choice_marker.start():]
            else:
                print(f"{id_str} - {number}번 보기 추출 실패")
                continue

            next_id_or_q = re.search(r'(?= \[\d+\s*(~|～)\s*\d+\])', choices_text)
            if next_id_or_q:
                choices_text = choices_text[:next_id_or_q.start()].strip()

            choice_pattern = r"①\s(.*?)②\s(.*?)③\s(.*?)④\s(.*?)⑤\s(.*)"
            choice_match = re.search(choice_pattern, choices_text)
            if not choice_match:
                print(f"{id_str} - {number}번 보기 추출 실패")
                continue

            choices = [choice_match.group(i).strip() for i in range(1, 6)]

            if question_plus:
                problems.append({
                    "question": question_text,
                    "question_plus": question_plus,
                    "choices": choices,
                    "answer": answers[number-1],
                    "score": scores[number-1],
                })
            else:
                problems.append({
                    "question": question_text,
                    "choices": choices,
                    "answer": answers[number-1],
                    "score": scores[number-1],
                })

        results.append({
            "id": id_str,
            "paragraph": paragraph,
            "type": 0,
            "problems": problems
        })

    return results



def save_to_json(txt_path, json_path, max_q=45):
    with open(txt_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    structured = extract_all_question_sets_fixed(raw_text)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {json_path}")


input_file_list = os.listdir("data/processed/txt")
output_file_list = [f.replace(".txt", ".json") for f in input_file_list]
# 경로 설정
INPUT_DATA_DIR = "data/processed/txt"
PROCESSED_DATA_DIR = "data/processed/json"
OUTPUT_FILES = os.listdir(PROCESSED_DATA_DIR)
for i in range(len(input_file_list)):
    if output_file_list[i] in OUTPUT_FILES:
        #print(f"{output_file_list[i]}있음")
        continue
    INPUT_TXT = os.path.join(INPUT_DATA_DIR, input_file_list[i])
    OUTPUT_JSON = os.path.join(PROCESSED_DATA_DIR, output_file_list[i])
    save_to_json(INPUT_TXT, OUTPUT_JSON, max_q=45)

print("TXT -> JSON 변환 완료")