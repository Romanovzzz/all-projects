"""Скриншоты обновлённого PDF v3 для проверки новых иллюстраций."""
import os
import fitz

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE, "\u041e\u0442\u0432\u0435\u0442\u044b", "\u041c\u0435\u0442\u0430\u043b\u043b\u0438\u0447\u0435\u0441\u043a\u0438\u0435_\u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438_\u043e\u0442\u0432\u0435\u0442\u044b.pdf")
OUT_DIR = r"C:\Users\jason\.gemini\antigravity\brain\9978874e-33a5-4e71-ac17-6bc4f29a3a44"

doc = fitz.open(PDF_PATH)
print(f"Total pages: {len(doc)}")

# Preview key new pages: q7 bracing, q14 lengths, q29 suspended
for pg_num in [0, 1, 11, 22, 38, 60, 63]:
    if pg_num < len(doc):
        page = doc.load_page(pg_num)
        pix = page.get_pixmap(dpi=150)
        path = os.path.join(OUT_DIR, f"pdf_v3_page{pg_num+1}.png")
        pix.save(path)
        print(f"Saved: page {pg_num+1}")
doc.close()
