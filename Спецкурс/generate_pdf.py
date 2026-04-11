"""
Генератор PDF — Спецкурс по проектированию ЖБ и каменных конструкций.
Формирует два PDF: ответы к зачёту и ответы к курсовому проекту.
Компактная вёрстка: вопросы идут подряд без разрыва страницы.
"""

import os
import re
from fpdf import FPDF

# --- Пути ---
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(
    os.path.dirname(BASE),
    "Безопасность стройплощадки", "dejavu-fonts-ttf-2.37", "ttf"
)
ANSWERS_DIR = os.path.join(BASE, "Ответы")


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

    def __init__(self, header_text="Спецкурс — ответы"):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=12)
        self.set_margins(10, 10, 10)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))
        self._header_text = header_text

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 6)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 4, self._header_text, align="L")
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
                  "Источники: УМП «Спецкурс» (НИУ МГСУ, 2021); СП 63; СП 20; СП 22; СП 15",
                  align="C")

    def add_title_page(self, title, subtitle, total_q, sources):
        self.add_page()
        self.ln(45)
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 0, 210, 8, style="F")

        self.set_font("DS", "B", 22)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(0, 14, "СПЕЦКУРС", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 11)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 8, "по проектированию ЖБ и каменных конструкций",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

        self.set_font("DS", "B", 16)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.2)
        cx = self.w / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(6)

        self.set_font("DS", "B", 36)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 18, str(total_q), align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 12)
        self.set_text_color(*self.GRAY_TEXT)
        self.cell(0, 8, subtitle, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

        self.set_font("DS", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Составлено на основе:", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 8)
        for s in sources:
            self.cell(0, 5, f"  • {s}", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 289, 210, 8, style="F")

    def add_section_header(self, title):
        """Section divider (Раздел)."""
        if self.get_y() > 260:
            self.add_page()
        self.ln(3)
        y0 = self.get_y()
        self.set_fill_color(*self.BLUE_MED)
        self.rect(self.l_margin, y0, self.w - self.l_margin - self.r_margin, 7, style="F")
        self.set_xy(self.l_margin + 2, y0 + 0.5)
        self.set_font("DS", "B", 9)
        self.set_text_color(*self.WHITE)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 4, 3, title, align="L")
        self.set_y(y0 + 8)
        self.set_text_color(*self.GRAY_TEXT)

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
        self.cell(12, block_h - 1, f"{number}", align="C")

        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.3)
        self.line(self.l_margin + 14, y_start + 2, self.l_margin + 14, y_start + block_h - 2)

        self.set_xy(self.l_margin + 16, y_start + 1)
        self.set_font("DS", "B", 7.5)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 18, 3.5, title, align="L")
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
        self.set_font("DS", "", 7.5)
        self.set_text_color(*self.GRAY_TEXT)
        self.set_x(self.l_margin)
        w = self.w - self.l_margin - self.r_margin
        try:
            self.multi_cell(w, 3.6, text)
        except Exception:
            self.cell(w, 3.6, text[:120] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_formula(self, text):
        self.set_fill_color(*self.BLUE_LIGHT)
        self.set_font("DS", "B", 7.5)
        self.set_text_color(*self.BLUE_DARK)
        x0 = self.l_margin + 3
        self.set_x(x0)
        w_avail = self.w - self.l_margin - self.r_margin - 6
        try:
            self.multi_cell(w_avail, 3.6, text, fill=True)
        except Exception:
            self.cell(w_avail, 3.6, text[:100] + "...", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)

    def add_bullet(self, text, level=0):
        self.set_font("DS", "", 7.5)
        self.set_text_color(*self.GRAY_TEXT)
        indent = self.l_margin + 2 + level * 3
        marker = "›" if level == 0 else "-"
        self.set_x(indent)
        self.cell(3, 3.6, marker)
        w_avail = self.w - indent - self.r_margin - 3
        if w_avail < 20:
            w_avail = self.w - self.l_margin - self.r_margin - 8
            self.set_x(self.l_margin + 6)
        try:
            self.multi_cell(w_avail, 3.6, text)
        except Exception:
            self.cell(w_avail, 3.6, text[:100] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_table_row(self, cells, header=False):
        if self.get_y() > 275:
            self.add_page()
        n = len(cells)
        w = (self.w - self.l_margin - self.r_margin) / n
        h = 4
        if header:
            self.set_font("DS", "B", 6.5)
            self.set_fill_color(*self.BLUE_LIGHT)
        else:
            self.set_font("DS", "", 6.5)
            self.set_fill_color(248, 248, 248)
        y0 = self.get_y()
        for i, c in enumerate(cells):
            self.set_xy(self.l_margin + i * w, y0)
            self.cell(w, h, str(c)[:30], border=1, fill=True, align="C")
        self.set_y(y0 + h)


def parse_speckurs_md(filepath):
    """Generic parser for speckurs markdown files.
    Returns list of dicts: {num, title, sections: [{heading, items: [(type, text)]}]}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    questions = []
    current_q = None
    current_section = None
    section_counter = 0
    q_counter = 0

    for line in content.split("\n"):
        ls = line.strip()

        # Detect section headers like "## РАЗДЕЛ X." or "## РАЗДЕЛ"
        if ls.startswith("## РАЗДЕЛ"):
            if current_q:
                if current_section:
                    current_q["sections"].append(current_section)
                questions.append(current_q)
                current_q = None
                current_section = None
            section_counter += 1
            # Store as special section marker
            questions.append({"type": "section", "title": ls.replace("## ", "")})
            continue

        # Detect question headers like "### 1.1." or "## 1."
        q_match = re.match(r"^###?\s+([\d.]+)\s*(.*)", ls)
        if q_match:
            if current_q:
                if current_section:
                    current_q["sections"].append(current_section)
                questions.append(current_q)
            q_counter += 1
            num_str = q_match.group(1).rstrip(".")
            title = q_match.group(2).strip()
            current_q = {"type": "question", "num": num_str, "title": title, "sections": []}
            current_section = None
            continue

        if current_q is None:
            continue

        if ls in ("", "---") or ls.startswith("*Источники"):
            continue
        if ls.startswith("# Ответы"):
            continue

        if current_section is None:
            current_section = {"heading": "", "items": []}

        # Formulas (indented with spaces)
        if line.startswith("    ") and ls and not ls.startswith("-"):
            current_section["items"].append(("formula", ls))
        elif ls.startswith("**") and ls.endswith("**") and len(ls) > 10 and ":" not in ls:
            current_section["items"].append(("formula", ls.strip("*").strip()))
        elif ls.startswith("- **") or ls.startswith("- "):
            text = ls[2:].replace("**", "")
            current_section["items"].append(("bullet", text))
        elif len(ls) > 2 and ls[0].isdigit() and ls[1] in ".)" and ls[2] == " ":
            text = ls.replace("**", "")
            current_section["items"].append(("bullet", text))
        elif ls.startswith("|") and "|" in ls[1:]:
            # Table row
            cells = [c.strip() for c in ls.split("|") if c.strip() and c.strip() != "---"]
            if cells and not all(set(c) <= {'-', ':', ' '} for c in cells):
                current_section["items"].append(("table", cells))
        else:
            text = ls.replace("**", "")
            if text:
                current_section["items"].append(("text", text))

    if current_q:
        if current_section:
            current_q["sections"].append(current_section)
        questions.append(current_q)

    return questions


def build_zachet_pdf():
    """Build PDF for zachet (exam)."""
    pdf = ExamPDF(header_text="Спецкурс — ответы к зачёту")

    # Collect all items
    items = []
    for fname in ["zachet_answers_1.md", "zachet_answers_2.md", "zachet_answers_3.md"]:
        fpath = os.path.join(ANSWERS_DIR, fname)
        if os.path.exists(fpath):
            items.extend(parse_speckurs_md(fpath))

    total_q = sum(1 for i in items if i.get("type") == "question")

    sources = [
        "УМП «Спецкурс по проектированию ЖБ и каменных конструкций» (НИУ МГСУ, 2021)",
        "СП 63.13330.2018 «Бетонные и железобетонные конструкции»",
        "СП 20.13330.2016 «Нагрузки и воздействия»",
        "СП 22.13330.2016 «Основания зданий и сооружений»",
        "СП 15.13330.2020 «Каменные и армокаменные конструкции»",
    ]
    pdf.add_title_page("Ответы к зачёту", f"вопросов с подробными ответами", total_q, sources)

    # Оглавление
    pdf.add_page()
    pdf.set_font("DS", "B", 12)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 8, "СОДЕРЖАНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    for item in items:
        if item.get("type") == "section":
            pdf.set_font("DS", "B", 7)
            pdf.set_text_color(*pdf.ACCENT)
            pdf.cell(0, 5, item["title"][:100], new_x="LMARGIN", new_y="NEXT")
        elif item.get("type") == "question":
            pdf.set_font("DS", "B", 6.5)
            pdf.set_text_color(*pdf.BLUE_MED)
            pdf.cell(10, 4, f"{item['num']}.")
            pdf.set_font("DS", "", 6.5)
            pdf.set_text_color(*pdf.GRAY_TEXT)
            pdf.cell(0, 4, item["title"][:100], new_x="LMARGIN", new_y="NEXT")

    # Questions
    for item in items:
        if item.get("type") == "section":
            pdf.add_section_header(item["title"])
        elif item.get("type") == "question":
            pdf.add_question_header(item["num"], item["title"])
            for section in item["sections"]:
                if section["heading"]:
                    pdf.add_subheading(section["heading"])
                for item_type, item_text in section["items"]:
                    if item_type == "formula":
                        pdf.add_formula(item_text)
                    elif item_type == "bullet":
                        pdf.add_bullet(item_text)
                    elif item_type == "table":
                        pdf.add_table_row(item_text, header=False)
                    elif item_type == "text":
                        pdf.add_body_text(item_text)

    output = os.path.join(ANSWERS_DIR, "Спецкурс_зачёт_ответы.pdf")
    pdf.output(output)
    print(f"[OK] Zachet PDF: {output}")
    print(f"     Pages: {pdf.page_no()}, questions: {total_q}")


def build_kursovoy_pdf():
    """Build PDF for course project."""
    pdf = ExamPDF(header_text="Спецкурс — ответы к курсовому проекту")

    fpath = os.path.join(ANSWERS_DIR, "kursovoy_answers.md")
    items = parse_speckurs_md(fpath)

    total_q = sum(1 for i in items if i.get("type") == "question")

    sources = [
        "УМП «Спецкурс по проектированию ЖБ и каменных конструкций» (НИУ МГСУ, 2021)",
        "СП 63.13330.2018 «Бетонные и железобетонные конструкции»",
        "СП 22.13330.2016 «Основания зданий и сооружений»",
    ]
    pdf.add_title_page("Ответы к курсовому проекту",
                       "вопросов с подробными ответами", total_q, sources)

    # Оглавление
    pdf.add_page()
    pdf.set_font("DS", "B", 12)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 8, "СОДЕРЖАНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    for item in items:
        if item.get("type") == "question":
            pdf.set_font("DS", "B", 7)
            pdf.set_text_color(*pdf.BLUE_MED)
            pdf.cell(8, 4.5, f"{item['num']}.")
            pdf.set_font("DS", "", 7)
            pdf.set_text_color(*pdf.GRAY_TEXT)
            pdf.cell(0, 4.5, item["title"][:100], new_x="LMARGIN", new_y="NEXT")

    # Questions
    for item in items:
        if item.get("type") == "question":
            pdf.add_question_header(item["num"], item["title"])
            for section in item["sections"]:
                if section["heading"]:
                    pdf.add_subheading(section["heading"])
                for item_type, item_text in section["items"]:
                    if item_type == "formula":
                        pdf.add_formula(item_text)
                    elif item_type == "bullet":
                        pdf.add_bullet(item_text)
                    elif item_type == "table":
                        pdf.add_table_row(item_text, header=False)
                    elif item_type == "text":
                        pdf.add_body_text(item_text)

    output = os.path.join(ANSWERS_DIR, "Спецкурс_курсовой_ответы.pdf")
    pdf.output(output)
    print(f"[OK] Kursovoy PDF: {output}")
    print(f"     Pages: {pdf.page_no()}, questions: {total_q}")


if __name__ == "__main__":
    build_zachet_pdf()
    build_kursovoy_pdf()
    print("\nDone! Both PDFs created.")
