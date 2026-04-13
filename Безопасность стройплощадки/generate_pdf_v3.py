"""
Генератор PDF v3 — Безопасность на стройплощадке.
Особенности:
- Рендеринг настоящих LaTeX-формул через Matplotlib.
- Вставка иллюстраций (схем) из файлов.
- Крупный, читабельный шрифт (Аналог DejaVu).
"""

import os
import re
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "dejavu-fonts-ttf-2.37", "ttf")
ANSWERS_DIR = os.path.join(BASE, "Ответы")
ILL_DIR = os.path.join(ANSWERS_DIR, "illustrations")
OUTPUT = os.path.join(ANSWERS_DIR, "Безопасность_стройплощадки_ответы_FINAL.pdf")

TOTAL_QUESTIONS = 46

QUESTION_IMAGES = {
    1: [("fig_2_1_strojgenplan.png", "Рис. 2.1 — Стройгенплан")],
    3: [("fig_2_3_ogr_doborn.png", "Рис. 2.3 — Ограждение с козырьком")],
    5: [("fig_2_4_dorogi.png", "Рис. 2.4 — Схемы внутриплощадочных дорог")],
    6: [("fig_2_5_dorozh_polotno.png", "Рис. 2.5 — Дорожное полотно")],
    12: [("fig_2_6_zemlyanye.png", "Рис. 2.6 — Земляные работы")],
    13: [("fig_2_7_ravnoustchiv.png", "Рис. 2.7 — Профиль равноустойчивого откоса")],
    17: [("fig_2_7b_krepl.png", "Рис. 2.7б — Крепление откоса")],
    19: [("fig_2_8_kran.png", "Рис. 2.8 — Зоны крана")],
    20: [("fig_2_9_kran_ust.png", "Рис. 2.9 — Грузовая устойчивость крана")],
    28: [("fig_2_10_ograzhdenie_h.png", "Рис. 2.10 — Защитное ограждение рабочего места")],
    31: [("fig_2_11_vetroekrany.png", "Рис. 2.11 — Ветрозащитные экраны")],
    32: [("fig_2_12_zus.png", "Рис. 2.12 — Защитно-улавливающая сетка")],
    33: [("fig_2_13_podemnik.png", "Рис. 2.13 — Грузопассажирский подъемник")],
    41: [("fig_3_1_pozhar.png", "Рис. 3.1 — Пожар")],
}

def render_latex_to_image(latex_str):
    # Убираем $$ 
    clean_tex = latex_str.replace("$$", "").strip()
    if not clean_tex:
        return None
    
    # Matplotlib mathtext doesn't support \text perfectly without raw string, we'll try standard
    clean_tex = clean_tex.replace("·", r"\cdot ")
    clean_tex = clean_tex.replace("×", r"\times ")
    
    fig = plt.figure(figsize=(8, 1))
    fig.patch.set_alpha(0.0)
    plt.axis('off')
    
    try:
        # Рисуем текст в центре
        plt.text(0.5, 0.5, f"${clean_tex}$", size=24, ha='center', va='center')
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi=300)
        buf.seek(0)
        plt.close(fig)
        return buf
    except Exception as e:
        plt.close(fig)
        print("LaTeX render error:", e)
        return None

class ExamPDF(FPDF):
    BLUE_DARK = (24, 57, 99)
    BLUE_MED = (41, 98, 163)
    BLUE_LIGHT = (230, 240, 252)
    GRAY_TEXT = (40, 40, 40)
    GRAY_LINE = (180, 200, 220)
    ACCENT = (200, 60, 40)
    WHITE = (255, 255, 255)
    GREEN = (34, 120, 60)
    ORANGE = (240, 140, 40)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(15, 15, 15)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 8)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 6, "Безопасность на строительной площадке — ответы к зачёту", align="L")
        self.cell(0, 6, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("DS", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, "НИУ МГСУ | Методичка: Сугак Е.Б., Седов Д.С.", align="C")

    def add_title_page(self):
        self.add_page()
        self.ln(50)
        self.set_fill_color(*self.ORANGE)
        self.rect(0, 0, 210, 8, style="F")

        self.set_font("DS", "B", 24)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(0, 14, "БЕЗОПАСНОСТЬ НА", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 14, "СТРОИТЕЛЬНОЙ ПЛОЩАДКЕ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

        self.set_font("DS", "", 16)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 10, "Подробные ответы на вопросы к зачёту", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.2)
        cx = self.w / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(8)

        self.set_font("DS", "B", 40)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 20, str(TOTAL_QUESTIONS), align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 14)
        self.set_text_color(*self.GRAY_TEXT)
        self.cell(0, 8, "вопросов с формулами и иллюстрациями", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(15)

        self.set_fill_color(*self.ORANGE)
        self.rect(0, 289, 210, 8, style="F")

    def add_question_header(self, number, title):
        if self.get_y() > 250:
            self.add_page()
        self.ln(4)
        y_start = self.get_y()
        block_h = 14
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(self.l_margin, y_start, self.w - self.l_margin - self.r_margin, block_h, style="F")

        self.set_xy(self.l_margin + 2, y_start + 1)
        self.set_font("DS", "B", 18)
        self.set_text_color(*self.WHITE)
        self.cell(16, block_h - 2, f"{number:02d}", align="C")

        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.5)
        self.line(self.l_margin + 20, y_start + 3, self.l_margin + 20, y_start + block_h - 3)

        self.set_xy(self.l_margin + 24, y_start + 1.5)
        self.set_font("DS", "B", 11)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 28, 5.5, title, align="L")
        self.set_y(y_start + block_h + 3)

    def add_subheading(self, text):
        if self.get_y() > 270:
            self.add_page()
        self.ln(3)
        self.set_font("DS", "B", 10)
        self.set_text_color(*self.BLUE_MED)
        y0 = self.get_y()
        self.set_fill_color(*self.BLUE_MED)
        self.rect(self.l_margin, y0, 2, 5, style="F")
        self.set_x(self.l_margin + 4)
        self.cell(0, 5, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def add_body_text(self, text):
        self.set_font("DS", "", 10)
        self.set_text_color(*self.GRAY_TEXT)
        self.set_x(self.l_margin)
        w = self.w - self.l_margin - self.r_margin
        
        # Cleanup ascii box drawings
        if "─" in text or "═" in text or "│" in text:
            # Skip ascii art since we have real images
            return

        try:
            self.multi_cell(w, 5.5, text)
        except Exception:
            self.cell(w, 5.5, text[:120] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_formula(self, text):
        buf = render_latex_to_image(text)
        if buf:
            self.ln(2)
            self.set_fill_color(*self.BLUE_LIGHT)
            self.rect(self.l_margin, self.get_y(), self.w - self.l_margin - self.r_margin, 18, style="F")
            
            # Using PIL to get cropped bbox
            try:
                img_pil = Image.open(buf)
                bg = Image.new(img_pil.mode, img_pil.size, (255,255,255))
                diff = Image.composite(img_pil, bg, img_pil)
                bbox = diff.getbbox()
                if bbox:
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    # Calc mm 
                    w_mm = w * 25.4 / 300
                    h_mm = h * 25.4 / 300
                    self.image(buf, x = self.w/2 - w_mm/2, y = self.get_y() + (18 - h_mm)/2, h = h_mm)
            except Exception as e:
                pass
            self.set_y(self.get_y() + 20)
        else:
            # Fallback
            self.set_font("DS", "B", 11)
            self.set_text_color(*self.BLUE_DARK)
            self.cell(0, 8, text.replace("$$",""), align="C", new_x="LMARGIN", new_y="NEXT")
            self.set_text_color(*self.GRAY_TEXT)

    def add_bullet(self, text):
        self.set_font("DS", "", 10)
        self.set_text_color(*self.GRAY_TEXT)
        indent = self.l_margin + 5
        self.set_x(indent)
        self.cell(4, 5.5, "•")
        w_avail = self.w - indent - self.r_margin - 4
        self.multi_cell(w_avail, 5.5, text)
        
    def add_note(self, text):
        self.ln(2)
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(220, 180, 80)
        y0 = self.get_y()
        self.set_font("DS", "I", 9.5)
        w = self.w - self.l_margin - self.r_margin
        
        # Calc height
        lines = self.multi_cell(w - 6, 5, text.replace(">","").strip(), dry_run=True, output="LINES")
        h = len(lines)*5 + 4
        
        self.rect(self.l_margin, y0, w, h, style="FD")
        self.set_xy(self.l_margin + 3, y0 + 2)
        self.set_text_color(100, 80, 30)
        self.multi_cell(w - 6, 5, text.replace(">","").strip())
        self.set_y(y0 + h + 2)

    def add_illustration(self, img_path, caption):
        if not os.path.exists(img_path):
            return

        # Зелёная плашка с надписью
        self.ln(4)
        if self.get_y() > 200:
            self.add_page()
            
        self.set_fill_color(230, 245, 235)
        self.set_draw_color(*self.GREEN)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, self.w - self.l_margin - self.r_margin, 8, style="FD")
        self.set_font("DS", "BI", 9)
        self.set_text_color(*self.GREEN)
        self.set_xy(self.l_margin + 3, y0 + 1.5)
        self.cell(0, 5, "ИЛЛЮСТРАЦИЯ ИЗ МЕТОДИЧЕСКОГО ПОСОБИЯ")
        self.set_y(y0 + 10)

        # Вычисляем максимальную ширину и высоту
        w_avail = self.w - self.l_margin - self.r_margin
        h_max = self.h - self.get_y() - 25

        try:
            with Image.open(img_path) as im:
                img_w, img_h = im.size
                ratio = img_w / img_h
                r_w = w_avail
                r_h = w_avail / ratio
                if r_h > h_max:
                    r_h = h_max
                    r_w = h_max * ratio
                if r_w > w_avail:
                    r_w = w_avail
                    r_h = w_avail / ratio

                self.image(img_path, x=self.w/2 - r_w/2, y=self.get_y(), w=r_w)
                self.set_y(self.get_y() + r_h + 3)
        except Exception as e:
            return

        # Подпись
        self.set_font("DS", "I", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, caption, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

def parse_markdown_files():
    questions = []
    # Using _v2.md files
    for fname in sorted(os.listdir(ANSWERS_DIR)):
        if not fname.endswith("_v2.md"):
            continue
        fpath = os.path.join(ANSWERS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        current_q = None
        current_section = None

        for line in content.split("\n"):
            ls = line.strip()

            if ls.startswith("## Вопрос "):
                if current_q:
                    if current_section:
                        current_q["sections"].append(current_section)
                    questions.append(current_q)
                title = ls.split(".", 1)[-1].strip()
                num = int(re.search(r'\d+', ls).group())
                current_q = {"num": num, "title": title, "sections": []}
                current_section = None
                continue

            if not current_q: continue

            if ls.startswith("### "):
                if current_section:
                    current_q["sections"].append(current_section)
                current_section = {"heading": ls[4:].strip(), "items": []}
                continue

            if ls in ("", "---") or ls.startswith("# Ответы"):
                continue

            if current_section is None:
                current_section = {"heading": "", "items": []}

            if "$$" in ls:
                current_section["items"].append(("formula", ls))
            # Also catch old formula style or indented blocks if they are math
            elif ls.startswith("    ") and "=" in ls and len(ls.strip()) < 40 and not ls.strip().startswith("┌"):
                current_section["items"].append(("formula", f"$$ {ls.strip()} $$"))
            elif ls.startswith("> "):
                current_section["items"].append(("note", ls))
            elif ls.startswith("- "):
                current_section["items"].append(("bullet", ls[2:].replace("**", "")))
            elif re.match(r'^\d+\.', ls):
                current_section["items"].append(("bullet", ls.replace("**", "")))
            else:
                current_section["items"].append(("text", ls.replace("**", "")))

        if current_q:
            if current_section:
                current_q["sections"].append(current_section)
            questions.append(current_q)

    return questions

def build_pdf():
    pdf = ExamPDF()
    pdf.add_title_page()

    questions = parse_markdown_files()
    print(f"Found {len(questions)} questions")

    # Table of contents
    pdf.add_page()
    pdf.set_font("DS", "B", 16)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 10, "ОГЛАВЛЕНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    for q in questions:
        pdf.set_font("DS", "B", 10)
        pdf.set_text_color(*pdf.BLUE_MED)
        pdf.cell(10, 6, f"{q['num']:02d}.")
        pdf.set_font("DS", "", 10)
        pdf.set_text_color(*pdf.GRAY_TEXT)
        pdf.cell(0, 6, q["title"], new_x="LMARGIN", new_y="NEXT")

    for q in questions:
        pdf.add_question_header(q["num"], q["title"])
        for section in q["sections"]:
            if section["heading"]:
                pdf.add_subheading(section["heading"])
            for item_type, text in section["items"]:
                if item_type == "formula":
                    pdf.add_formula(text)
                elif item_type == "bullet":
                    pdf.add_bullet(text)
                elif item_type == "note":
                    pdf.add_note(text)
                elif item_type == "text":
                    pdf.add_body_text(text)
                    
        # Add illustrations if map exists
        if q["num"] in QUESTION_IMAGES:
            for img_file, caption in QUESTION_IMAGES[q["num"]]:
                pdf.add_illustration(os.path.join(ILL_DIR, img_file), caption)

    pdf.output(OUTPUT)
    print(f"PDF creation COMPLETE: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")

if __name__ == "__main__":
    plt.rc('mathtext', fontset='stix')
    build_pdf()
