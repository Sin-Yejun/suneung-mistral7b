import cv2
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
import easyocr
import math
from collections import defaultdict
import re
import os

# 경로 설정
file_path = 'downloads/png/'
output_path = 'downloads/answer/'
file_list = os.listdir(file_path)

for file_name  in file_list:
    # file_name = '고1_2020년_9월.png'
    full_path = file_path+file_name
    img_path = Path(full_path)

    if f'{file_name[:-4]}.txt' in os.listdir(output_path):
        continue
    print(file_name)
    # (1) 이미지 열기 → PIL → 대비 강화 + 확대
    pil = Image.open(img_path).convert('RGB')
    pil = ImageEnhance.Contrast(pil).enhance(2.0)  # 대비 증가
    pil = pil.resize((pil.width * 2, pil.height * 2), Image.LANCZOS)  # 확대

    # (2) NumPy 변환 → 그레이스케일
    img = np.array(pil)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # (3) 블러 + 이진화 (노이즈 제거 + 명암 강조)
    blur = cv2.medianBlur(gray, 3)
    _, binarized = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # ✅ (3-1) 동그라미 제거를 위한 원형 검출 (Hough Circle Transform)
    circles = cv2.HoughCircles(
        blur,                   # 입력 이미지
        cv2.HOUGH_GRADIENT,     # 검출 방법
        dp=1.2,                 # 해상도 비율
        minDist=30,             # 원 사이 최소 거리
        param1=50, param2=30,   # Canny + 원 검출 민감도
        
        # minRadius=25, maxRadius=30  # 원 반지름 범위 (조정 필요)
        #minRadius=17, maxRadius=23  # 원 반지름 범위 (조정 필요)
        minRadius=12, maxRadius=16  # 원 반지름 범위 (조정 필요)
    )

    reader = easyocr.Reader(['ko'])
    # print("📌 동그라미 OCR 결과:")
    # (5) 원 영역에서 OCR
    results = []
    answer = []
    debug_img = img.copy()
    if circles is not None:
        circles = np.uint16(np.around(circles[0]))


        # 행 간 거리 허용 오차 (픽셀)
        ROW_TOL = 30

        # 1. y값 기준으로 비슷한 값끼리 행 그룹핑
        rows = defaultdict(list)
        for c in circles:
            c_y = int(c[1])
            inserted = False
            for key_y in rows:
                if abs(c_y - int(key_y)) < ROW_TOL:
                    rows[key_y].append(c)
                    inserted = True
                    break
            if not inserted:
                rows[c[1]].append(c)

        # 2. 각 행을 x좌표 오름차순으로 정렬하고, 전체를 y 오름차순으로 flatten
        sorted_circles = []
        for key_y in sorted(rows.keys()):
            sorted_row = sorted(rows[key_y], key=lambda c: int(c[0]))
            sorted_circles.extend(sorted_row)


        debug_img = img.copy()
        for i, circle in enumerate(sorted_circles):
            cx, cy, r = circle
            r = r - 2  # 약간 여유 두기

            # ROI 좌표 계산
            x1, y1 = max(cx - r, 0), max(cy - r, 0)
            x2, y2 = min(cx + r, binarized.shape[1]), min(cy + r, binarized.shape[0])
            roi = binarized[y1:y2, x1:x2]
            h, w = roi.shape

            # [2] 원형 마스크 생성 (조금 작게 잡기)
            mask = np.zeros_like(roi, dtype=np.uint8)
            cv2.circle(mask, (w//2, h//2), r - 3, 255, -1)  # 반지름 살짝 줄임

            # [3] 외부 흰색 배경 이미지
            white_bg = np.full_like(roi, 255)

            # [4] 원 내부는 roi, 바깥은 흰색 배경
            masked = cv2.bitwise_or(
                cv2.bitwise_and(roi, mask),
                cv2.bitwise_and(white_bg, cv2.bitwise_not(mask))
            )

            # OCR (이미지 확대하면 더 정확해짐)
            masked_resized = cv2.resize(masked, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)

            # cv2.imwrite(f"debug/roi_{i+1}.png", roi)
            # cv2.imwrite(f"debug/mask_{i+1}.png", mask)
            # cv2.imwrite(f"debug/masked_{i+1}.png", masked)
            # cv2.imwrite(f"debug/masked_resized_{i+1}.png", masked_resized)

            ocr_result = reader.readtext(masked_resized, detail=0)
            raw_text = ocr_result[0] if ocr_result else ''

            # ✅ 정수 숫자만 추출 (예: '4', '5.' → 5)
            match = re.search(r'\d+', raw_text)
            number = int(match.group()) if match else None
            if number and number > 5 or number == 0:
                number = None
            answer.append(number)

            #print(f"{i+1}번 → 원본: {raw_text}, 정제 숫자: {number}")


    if len(answer) >= 40:
        print(file_name, len(answer))
        print(answer)
        with open(f"{output_path+file_name[:-4]}.txt", "w", encoding="utf-8") as f:
            f.write("answer = " + str(answer) + "\n")

'''
   
            # 원 & 중심점 표시
            cv2.circle(debug_img, (cx, cy), r, (0, 255, 0), 2)
            cv2.circle(debug_img, (cx, cy), 2, (0, 0, 255), 3)

            # ✅ 번호 표시 (정렬된 순서 기준)
            cv2.putText(debug_img, f"{i+1}", (cx - r, cy - r), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)
        print(file_name)
        cv2.imwrite("debug_circles_sorted.png", debug_img)
        break
'''    