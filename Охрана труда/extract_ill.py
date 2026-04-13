import fitz
import os

pdf_path = "Пособия и методички/Методичка_Седов,_Сугак_БОС_высот_и_бп_зд_итог_в_издание.pdf"
doc = fitz.open(pdf_path)

out_dir = "Ответы/illustrations"
os.makedirs(out_dir, exist_ok=True)

image_count = 0
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)
    if images:
        for idx, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_filename = f"page_{page_num+1}_img_{idx+1}.{ext}"
            with open(os.path.join(out_dir, img_filename), "wb") as f:
                f.write(image_bytes)
            image_count += 1
            print(f"Extracted {img_filename} on page {page_num+1}")
            
print(f"Total images extracted: {image_count}")
