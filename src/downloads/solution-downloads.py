import os
import requests
import json

# ▶ 이건 앞에서 수집된 results 리스트라고 가정
with open('downloads/ebs_korean.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

output_dir = "downloads/solutions/"


for item in results:
    pdf_path = item["solution_pdf"]
    full_url = pdf_path
    filename = item['date']+'_해설'

    try:
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            with open(f"{output_dir+filename}.pdf", "wb") as f:
                f.write(response.content)
            print(f"✅ 다운로드 성공: {filename}")
        else:
            print(f"❌ 실패 ({response.status_code}): {filename}")
    except Exception as e:
        print(f"⚠️ 에러 ({filename}): {e}")
