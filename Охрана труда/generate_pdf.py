"""
Генератор PDF — Охрана труда.
Формирует PDF с ответами на 27 вопросов к зачёту.
Компактная верстка: вопросы идут подряд без разрыва страницы.
"""

import os
from fpdf import FPDF

# --- Пути ---
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "dejavu-fonts-ttf-2.37", "ttf")
ANSWERS_DIR = os.path.join(BASE, "Ответы")
OUTPUT = os.path.join(ANSWERS_DIR, "Охрана_труда_ответы.pdf")

TOTAL_QUESTIONS = 27


class ExamPDF(FPDF):
    """PDF с оформлением в стиле предыдущих проектов."""

    BLUE_DARK = (24, 57, 99)
    BLUE_MED = (41, 98, 163)
    BLUE_LIGHT = (220, 235, 252)
    GRAY_TEXT = (50, 50, 50)
    GRAY_LINE = (180, 200, 220)
    ACCENT = (200, 60, 40)
    WHITE = (255, 255, 255)
    GREEN = (34, 120, 60)
    ORANGE = (200, 120, 30)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=12)
        self.set_margins(10, 10, 10)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 6)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 4, "Охрана труда — ответы к зачёту", align="L")
        self.cell(0, 4, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(1)

    def footer(self):
        self.set_y(-10)
        self.set_font("DS", "I", 6)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5,
                  "Источники: БЖД (НИУ МГСУ); лекции «Охрана труда в строительстве»; ФЗ-125; Приказ 776н",
                  align="C")

    def add_title_page(self):
        self.add_page()
        self.ln(50)
        self.set_fill_color(*self.GREEN)
        self.rect(0, 0, 210, 8, style="F")

        self.set_font("DS", "B", 28)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(0, 14, "ОХРАНА ТРУДА", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

        self.set_font("DS", "", 14)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 10, "Ответы на вопросы к зачёту", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.2)
        cx = self.w / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(8)

        self.set_font("DS", "B", 36)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 18, str(TOTAL_QUESTIONS), align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 12)
        self.set_text_color(*self.GRAY_TEXT)
        self.cell(0, 8, "вопросов с подробными ответами", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

        self.set_font("DS", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Составлено на основе:", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 9)
        sources = [
            "Учебник «Безопасность жизнедеятельности» (НИУ МГСУ)",
            "Лекции «Охрана труда в строительстве» (Сугак Е.Б.)",
            "ФЗ от 24.07.1998 № 125-ФЗ (обязательное страхование)",
            "Приказ Минтруда от 29.10.2021 № 776н (СУОТ)",
            "Трудовой кодекс РФ (Раздел X «Охрана труда»)",
        ]
        for s in sources:
            self.cell(0, 6, f"  • {s}", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_fill_color(*self.GREEN)
        self.rect(0, 289, 210, 8, style="F")

    def add_question_header(self, number, title):
        if self.get_y() > 265:
            self.add_page()
        self.ln(2)
        y_start = self.get_y()
        block_h = 10
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(self.l_margin, y_start, self.w - self.l_margin - self.r_margin, block_h, style="F")

        self.set_xy(self.l_margin + 1, y_start + 0.5)
        self.set_font("DS", "B", 14)
        self.set_text_color(*self.WHITE)
        self.cell(12, block_h - 1, f"{number:02d}", align="C")

        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.3)
        self.line(self.l_margin + 14, y_start + 2, self.l_margin + 14, y_start + block_h - 2)

        self.set_xy(self.l_margin + 16, y_start + 1)
        self.set_font("DS", "B", 8.5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 18, 4, title, align="L")
        self.set_y(y_start + block_h + 1)
        self.set_text_color(*self.GRAY_TEXT)

    def add_subheading(self, text):
        if self.get_y() > 272:
            self.add_page()
        self.ln(1)
        self.set_font("DS", "B", 8)
        self.set_text_color(*self.BLUE_MED)
        y0 = self.get_y()
        self.set_fill_color(*self.BLUE_MED)
        self.rect(self.l_margin, y0, 1.5, 4.5, style="F")
        self.set_x(self.l_margin + 3)
        self.cell(0, 4.5, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)

    def add_body_text(self, text):
        self.set_font("DS", "", 8)
        self.set_text_color(*self.GRAY_TEXT)
        self.set_x(self.l_margin)
        if "|" in text and text.count("|") >= 3:
            cells = [c.strip() for c in text.split("|") if c.strip()]
            text = "  •  ".join(cells)
        w = self.w - self.l_margin - self.r_margin
        try:
            self.multi_cell(w, 3.8, text)
        except Exception:
            self.cell(w, 3.8, text[:120] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_formula(self, text):
        self.set_fill_color(*self.BLUE_LIGHT)
        self.set_font("DS", "B", 8)
        self.set_text_color(*self.BLUE_DARK)
        x0 = self.l_margin + 3
        self.set_x(x0)
        w_avail = self.w - self.l_margin - self.r_margin - 6
        try:
            self.multi_cell(w_avail, 4, text, fill=True)
        except Exception:
            self.cell(w_avail, 4, text[:100] + "...", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)

    def add_bullet(self, text, level=0):
        self.set_font("DS", "", 8)
        self.set_text_color(*self.GRAY_TEXT)
        indent = self.l_margin + 2 + level * 3
        marker = "›" if level == 0 else "-"
        self.set_x(indent)
        self.cell(3, 3.8, marker)
        w_avail = self.w - indent - self.r_margin - 3
        if w_avail < 20:
            w_avail = self.w - self.l_margin - self.r_margin - 8
            self.set_x(self.l_margin + 6)
        try:
            self.multi_cell(w_avail, 3.8, text)
        except Exception:
            self.cell(w_avail, 3.8, text[:100] + "...", new_x="LMARGIN", new_y="NEXT")


def parse_markdown_files():
    """Парсит MD-файлы ответов."""
    questions = []
    for fname in sorted(os.listdir(ANSWERS_DIR)):
        if not fname.startswith("answers_") or not fname.endswith(".md"):
            continue
        fpath = os.path.join(ANSWERS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        current_q = None
        current_section = None

        for line in content.split("\n"):
            line_stripped = line.strip()

            if line_stripped.startswith("## Вопрос "):
                if current_q:
                    if current_section:
                        current_q["sections"].append(current_section)
                    questions.append(current_q)
                after_prefix = line_stripped[len("## Вопрос "):]
                dot_pos = after_prefix.find(".")
                if dot_pos == -1:
                    continue
                num_str = after_prefix[:dot_pos].strip()
                title = after_prefix[dot_pos + 1:].strip()
                try:
                    num = int(num_str)
                except ValueError:
                    continue
                current_q = {"num": num, "title": title, "sections": []}
                current_section = None
                continue

            if current_q is None:
                continue

            if line_stripped.startswith("### "):
                if current_section:
                    current_q["sections"].append(current_section)
                current_section = {"heading": line_stripped[4:], "items": []}
                continue

            if line_stripped in ("", "---") or line_stripped.startswith("*Источники"):
                continue
            if line_stripped.startswith("# Ответы"):
                continue
            if line_stripped.startswith("> **"):
                continue

            if current_section is None:
                current_section = {"heading": "", "items": []}

            if line_stripped.startswith("**") and line_stripped.endswith("**") and len(line_stripped) > 10:
                text = line_stripped.strip("*").strip()
                current_section["items"].append(("formula", text))
            elif line_stripped.startswith("- "):
                text = line_stripped[2:].replace("**", "")
                current_section["items"].append(("bullet", text))
            elif len(line_stripped) > 2 and line_stripped[0].isdigit() and line_stripped[1] in ".)" and line_stripped[2] == " ":
                text = line_stripped.replace("**", "")
                current_section["items"].append(("bullet", text))
            else:
                text = line_stripped.replace("**", "")
                if text:
                    current_section["items"].append(("text", text))

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

    # Оглавление
    pdf.add_page()
    pdf.set_font("DS", "B", 12)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 8, "СОДЕРЖАНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for q in questions:
        pdf.set_font("DS", "B", 7)
        pdf.set_text_color(*pdf.BLUE_MED)
        pdf.cell(8, 4.5, f"{q['num']:02d}.")
        pdf.set_font("DS", "", 7)
        pdf.set_text_color(*pdf.GRAY_TEXT)
        title_trunc = q["title"][:95]
        pdf.cell(0, 4.5, title_trunc, new_x="LMARGIN", new_y="NEXT")

    # Вопросы — идут подряд без разрыва страницы
    for q in questions:
        pdf.add_question_header(q["num"], q["title"])

        for section in q["sections"]:
            if section["heading"]:
                pdf.add_subheading(section["heading"])
            for item_type, item_text in section["items"]:
                if item_type == "formula":
                    pdf.add_formula(item_text)
                elif item_type == "bullet":
                    pdf.add_bullet(item_text)
                elif item_type == "text":
                    pdf.add_body_text(item_text)

    pdf.output(OUTPUT)
    print(f"PDF created: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
