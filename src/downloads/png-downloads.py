import os
import requests
import json

# ▶ 기존 JSON 파일에서 데이터 로드
with open('downloads/ebs_korean.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

output_dir = "downloads/png/"

for item in results:
    img_url = item["answer_img"]
    filename = item['date']

    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            with open(f"{output_dir+filename}.png", "wb") as f:
                f.write(response.content)
            print(f"🟢 저장 성공: {filename}")
        else:
            print(f"🔴 실패 ({response.status_code}): {filename}")
    except Exception as e:
        print(f"⚠️ 에러 ({filename}): {e}")
