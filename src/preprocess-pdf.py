import pdfplumber
import os

# 경로 설정
RAW_DATA_DIR = "data/raw/"
PROCESSED_DATA_DIR = "data/processed/"
INPUT_PDF = os.path.join(RAW_DATA_DIR, "korean2024.pdf")
OUTPUT_TXT = os.path.join(PROCESSED_DATA_DIR, "korean2024_extracted.txt")

def extract_text_from_pdf_two_columns(pdf_path, output_path):
    """
    2단 레이아웃 PDF에서 텍스트를 열 단위로 추출해 저장합니다.
    """
    try:
        # 출력 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # PDF 파일 열기
        with pdfplumber.open(pdf_path) as pdf:
            full_text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                # 페이지 크기 확인
                width = page.width
                height = page.height

                # 1, 13, 17페이지      height*0.174
                # 나머지 페이지 height*0.1255
                # 하단 height*0.8992
                # 2단을 나누기 위해 페이지의 왼쪽 절반과 오른쪽 절반으로 영역 설정
                title_page_height = height*0.174
                other_page_height = height*0.1255
                bottom_page_height = height*0.8992
                if page_num in (1, 13, 17):
                    left_column = page.crop((0, title_page_height, width / 2, bottom_page_height))  
                    right_column = page.crop((width / 2, title_page_height, width, bottom_page_height))  
                else:
                    left_column = page.crop((0, other_page_height, width / 2, bottom_page_height)) 
                    right_column = page.crop((width / 2, other_page_height, width, bottom_page_height)) 

                # 각 열에서 텍스트 추출
                left_text = left_column.extract_text()
                right_text = right_column.extract_text()
                
                # 텍스트가 없으면 경고 출력
                if not left_text or not right_text:
                    print(f"페이지 {page_num}: 한쪽 열 텍스트 추출 실패 (이미지 기반일 가능성 있음)")
                
                # 페이지별로 텍스트 결합 (왼쪽 → 오른쪽 순서로)
                full_text += f"--- Page {page_num} ---\n"
                full_text += "Left Column:\n" + (left_text or "No text") + "\n\n"
                full_text += "Right Column:\n" + (right_text or "No text") + "\n\n"
            
            # 텍스트 파일로 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"텍스트 추출 완료: {output_path}")
    
    except FileNotFoundError:
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    # PDF 텍스트 추출 실행
    extract_text_from_pdf_two_columns(INPUT_PDF, OUTPUT_TXT)