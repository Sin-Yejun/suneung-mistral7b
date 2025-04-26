import pdfplumber
import os
import re

def pdf_to_txt(pdf_path, output_path):
    try:        
        # PDF 파일 열기
        
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                # 페이지 크기 확인
                width = page.width
                height = page.height
                if page_num == 1:
                    column = page.crop((0, height*0.2609, width, height*0.9043))
                else:
                    column = page.crop((0, height*0.1043, width, height*0.9043))

                # 각 열에서 텍스트 추출
                column_text = column.extract_text()

                
                # 페이지별로 텍스트 결합 (왼쪽 → 오른쪽 순서로)
                page_text = column_text
                cleaned_text = re.sub(r'\n', '', page_text)
                full_text += cleaned_text

            filtered_text = ""
            pattern = r"정답해설\s*:\s*(.*?)\s*정답"
            matches = re.finditer(pattern, full_text)
            for i, match in enumerate(matches, 1):
                filtered_text += match.group(1).strip()
                filtered_text += '\n'
                if i == 45:
                    break
            
            # 텍스트 파일로 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(filtered_text)
            print(f"텍스트 추출 완료: {output_path}")
    
    except FileNotFoundError:
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    
    input_file_list = os.listdir("data/raw/")
    output_file_list = [f.replace(".pdf", ".txt") for f in input_file_list]
    # 경로 설정
    file_name = "해설 2024_9월"
    INPUT = f"data/raw/{file_name}.pdf"
    OUTPUT = f"data/processed/txt/해설/{file_name}.txt"

    # PDF 텍스트 추출 실행
    pdf_to_txt(INPUT, OUTPUT)
    print("PDF -> TXT 변환 완료")