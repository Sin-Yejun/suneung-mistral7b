from pypdf import PdfReader, PdfWriter

# 원본 PDF 열기
reader = PdfReader("data/raw/korean2022.pdf")

# 새 PDF 생성기
writer = PdfWriter()

# 0부터 시작하므로 0~19까지가 1~20페이지
for i in range(16):
    writer.add_page(reader.pages[i])

# 잘라낸 PDF 저장
with open("data/raw/korean2022.pdf", "wb") as f:
    writer.write(f)
