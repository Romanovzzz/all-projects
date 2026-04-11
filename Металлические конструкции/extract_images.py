import fitz
import os

base = os.path.dirname(os.path.abspath(__file__))

# Extract presentation pages as images
pdf_path = os.path.join(base, "презентации", "Новый документ.pdf")
out_dir = os.path.join(base, "презентации", "pages")
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Presentations: {len(doc)} pages")
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=200)
    img_path = os.path.join(out_dir, f"slide_{i+1:03d}.jpg")
    pix.save(img_path)
    if (i+1) % 20 == 0:
        print(f"  Saved {i+1}/{len(doc)} slides")
print(f"  Done: {len(doc)} slides saved")
doc.close()

# Extract Kudishin textbook pages as images
pdf_path2 = os.path.join(base, "Пособия и методички", "Металлические конструкции под редакцией Ю. И. Кудишина dnl12764.pdf")
out_dir2 = os.path.join(base, "Пособия и методички", "kudishin_pages")
os.makedirs(out_dir2, exist_ok=True)

doc2 = fitz.open(pdf_path2)
print(f"\nKudishin textbook: {len(doc2)} pages")
for i, page in enumerate(doc2):
    pix = page.get_pixmap(dpi=150)
    img_path = os.path.join(out_dir2, f"page_{i+1:03d}.jpg")
    pix.save(img_path)
    if (i+1) % 50 == 0:
        print(f"  Saved {i+1}/{len(doc2)} pages")
print(f"  Done: {len(doc2)} pages saved")
doc2.close()
