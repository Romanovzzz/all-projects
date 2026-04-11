import fitz  # pymupdf
import os

files = [
    (r"презентации\Новый документ.pdf", r"презентации\presentations_text.txt"),
    (r"Пособия и методички\SP_16.13330.2017_Stalnye_konstruktsii.pdf", r"Пособия и методички\SP_16_text.txt"),
    (r"Пособия и методички\СП 20.13330.2016.pdf", r"Пособия и методички\SP_20_text.txt"),
    (r"Пособия и методички\Металлические конструкции под редакцией Ю. И. Кудишина dnl12764.pdf", r"Пособия и методички\Kudishin_text.txt"),
]

base = os.path.dirname(os.path.abspath(__file__))

for pdf_path, txt_path in files:
    full_pdf = os.path.join(base, pdf_path)
    full_txt = os.path.join(base, txt_path)
    print(f"Processing: {pdf_path}")
    try:
        doc = fitz.open(full_pdf)
        text = ""
        for i, page in enumerate(doc):
            text += f"\n\n===== PAGE {i+1} =====\n\n"
            text += page.get_text()
        doc.close()
        with open(full_txt, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  -> Saved: {txt_path} ({len(text)} chars)")
    except Exception as e:
        print(f"  -> ERROR: {e}")

print("\nDone!")
