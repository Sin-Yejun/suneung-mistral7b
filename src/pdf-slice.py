from pypdf import PdfReader, PdfWriter

# 원본 PDF 열기
reader = PdfReader("data/raw/korean2025.pdf")

# 새 PDF 생성기
writer = PdfWriter()

for i in range(16):
    writer.add_page(reader.pages[i])

# 잘라낸 PDF 저장
with open("data/raw/korean2025.pdf", "wb") as f:
    writer.write(f)
