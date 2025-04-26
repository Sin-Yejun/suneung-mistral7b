import requests
import re
import json

def format_date(yyyymmdd):
    year = yyyymmdd[:4]
    month = yyyymmdd[4:6]
    return f"_{year}년_{int(month)}월"
def format__(s):
    if s is not None:
        return 'https://wdown.ebsi.co.kr/W61001/01exam'+s
    else:
        return 'None'

URL = "https://www.ebsi.co.kr/ebs/xip/xipc/previousPaperListAjax.ajax"
STARTPAGE = 1
PAGES = 14

c_header = {
    'referer': 'https://www.ebsi.co.kr/ebs/xip/xipc/previousPaperList.ebs?targetCd=D100',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}

data_base = {
    'monthList': '02,03,04,05,06,07,09,10,11,12',
    'sort': 'recent',
    'pageSize': '50',
    'beginYear': '2016',
    'endYear': '2024',
    'subjList': '1'
}
grade_targets = {
    "고1": "D100",
    "고2": "D200",
    "고3": "D300"
}

results = []
seen_dates = set()
count = 0
for grade, targetCd in grade_targets.items():
    for page in range(STARTPAGE, PAGES + 1):
        c_data = data_base.copy()
        c_data['targetCd'] = targetCd
        c_data['currentPage'] = page

        r = requests.post(URL, headers=c_header, data=c_data)
        t_v = r.text

        # 문제지 PDF 경로 추출
        pdfs = re.findall(r"goDownLoadP\('([^']+\.pdf)", t_v)
        solutions = re.findall(r"goDownLoadH\('([^']+\.pdf)", t_v)

        if len(pdfs) > len(solutions):
            new_solutions = []
            sol_map = {s[:13]: s for s in solutions}

            for p in pdfs:
                prefix = p[:13]
                matched = sol_map.get(prefix, None)
                new_solutions.append(matched)

            solutions = new_solutions
        # 해설 이미지 전체 URL 추출
        imgs = re.findall(r"https?://wdown\.ebsi\.co\.kr/.+?\.png", t_v)

        # 문제지-해설지 짝이 맞는 경우만 저장
        for q, s, a in zip(pdfs, solutions, imgs):
            parts = q.split('/')
            date = parts[1] if len(parts) > 1 else "unknown"
            filename = parts[-1]
            type_ = filename.split('_mun_')[0] if '_mun_' in filename else "unknown"
            key = f"{date}_{grade}"
            if key not in seen_dates and 'B' not in type_ :
                results.append({
                    "date": grade+format_date(date),
                    "type": type_,
                    "question_pdf": 'https://wdown.ebsi.co.kr/W61001/01exam'+q,
                    "solution_pdf": 'https://wdown.ebsi.co.kr/W61001/01exam'+s,
                    "answer_img": a
                })
                seen_dates.add(key)
                count += 1
#print(json.dumps(results, indent=2, ensure_ascii=False))
# print(count)
# JSON 출력
with open(f"downloads/ebs_korean.json", 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
