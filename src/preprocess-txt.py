import re
import json
def find_questions(text, max_q=45):
    """
    PDF 추출 텍스트에서 번호 있는 질문(1~max_q)을 줄바꿈 포함해서 감지합니다.
    """
    # 줄바꿈 포함한 모든 공백 제거
    cleaned_text = re.sub(r'\s+', ' ', text)

    question_blocks = []
    for i in range(1, max_q + 1):
        if i < max_q:
            pattern = rf"{i}\.\s(.*?)(?={i+1}\.\s)"
        else:
            pattern = rf"{i}\.\s(.*)"  # 마지막 질문은 끝까지
        match = re.search(pattern, cleaned_text)
        if match:
            question_blocks.append((i, match.group(1).strip()))
        else:
            print(f"{i}번 질문 블록을 찾지 못했습니다.")

    result = []
    for number, block in question_blocks:
        # 질문 본문 (물음표로 끝나는 부분까지만)
        question_match = re.match(r"(.*?\?)", block)
        if not question_match:
            print(f"{number}번 질문에서 물음표 없음")
            continue

        question_text = question_match.group(1).strip()

        # 보기 추출: ①~⑤로 시작, ⑤는 온점으로 끝나는 것만
        choice_pattern = r"①\s(.*?)②\s(.*?)③\s(.*?)④\s(.*?)⑤\s(.*?)(?=\s*\d+\.\s|$)"
        choice_match = re.search(choice_pattern, block)
        if not choice_match:
            print(f"{number}번 보기 추출 실패")
            continue

        choices = [f"{opt}. {choice_match.group(i).strip()}" for i, opt in zip(range(1, 6), ["①", "②", "③", "④", "⑤"])]

        result.append({
            "number": number,
            "question": question_text,
            "choices": choices
        })

    return result

def save_questions__json(txt_path, json_path, max_q=45):
    with open(txt_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    questions = find_questions(raw_text, max_q=max_q)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"질문 JSON 저장 완료: {json_path}")

TXT = "data/processed/korean2024_extracted.txt"
JSON = "data/processed/korean2024_extracted.json"
save_questions__json(TXT, JSON, max_q=45)


