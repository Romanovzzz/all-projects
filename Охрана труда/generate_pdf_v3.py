import os
import re
from fpdf import FPDF
from fpdf.fonts import FontFace
from fpdf.enums import Align, TableCellFillMode

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "dejavu-fonts-ttf-2.37", "ttf")
ANSWERS_DIR = os.path.join(BASE, "Ответы")
OUTPUT = os.path.join(ANSWERS_DIR, "Охрана_труда_ответы_ФИНАЛ.pdf")

TOTAL_QUESTIONS = 27

def clean_formula(text):
    t = text.strip()
    t = re.sub(r'\$\$(.+?)\$\$', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\$(.+?)\$', r'\1', t)
    t = t.replace('$', '')
    for _ in range(3): t = re.sub(r'\\text\{([^}]*)\}', r'\1', t)
    for _ in range(3): t = re.sub(r'_\{([^}]*)\}', r'\1', t)
    for _ in range(3): t = re.sub(r'\^\{([^}]*)\}', r'\1', t)
    for _ in range(3): t = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'(\1) / (\2)', t)
    replacements = {
        '\\cdot': '·', '\\times': '×', '\\div': '÷',
        '\\leq': '≤', '\\geq': '≥', '\\neq': '≠',
        '\\approx': '≈', '\\,': ' ', '\\;': ' ',
        '\\quad': '  ', '\\left': '', '\\right': '',
        '\\%': '%',
    }
    for k, v in replacements.items():
        t = t.replace(k, v)
    t = re.sub(r'_([A-Za-zА-Яа-яёЁ0-9])', r'\1', t)
    t = re.sub(r'\^([A-Za-zА-Яа-яёЁ0-9])', r'\1', t)
    t = re.sub(r'\\([a-zA-Z]+)', r'\1', t)
    t = t.replace('{', '').replace('}', '')
    t = t.replace('_', ' ')
    t = re.sub(r' {2,}', ' ', t)
    return t.strip()

def clean_markdown(text):
    t = text
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
    t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', t)
    t = re.sub(r'`(.+?)`', r'\1', t)
    t = t.replace('📖', '[Рис.]')
    t = clean_formula(t)
    return t.strip()

class ExamPDF(FPDF):
    COLOR_DARK = (20, 30, 45)
    COLOR_BLUE = (35, 85, 145)
    COLOR_ACCENT = (210, 50, 40)
    COLOR_GRAY = (60, 60, 60)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=18)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))
        self.set_left_margin(20)
        self.set_right_margin(20)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 8)
        self.set_text_color(*self.COLOR_BLUE)
        self.cell(0, 6, "Охрана труда — экзаменационный конспект", align="L")
        self.cell(0, 6, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(220, 220, 220)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(5)

    def add_title_page(self):
        self.add_page()
        self.ln(60)
        
        self.set_fill_color(*self.COLOR_ACCENT)
        self.rect(self.l_margin, 60, 4, 30, style="F")
        self.set_x(self.l_margin + 8)

        self.set_font("DS", "B", 32)
        self.set_text_color(*self.COLOR_DARK)
        self.multi_cell(0, 14, "ОХРАНА ТРУДА", align="L")
        self.ln(4)
        
        self.set_x(self.l_margin + 8)
        self.set_font("DS", "", 16)
        self.set_text_color(*self.COLOR_GRAY)
        self.multi_cell(0, 8, "Экзаменационные ответы", align="L")
        self.ln(15)

        self.set_font("DS", "B", 24)
        self.set_text_color(*self.COLOR_BLUE)
        self.cell(0, 10, f"{TOTAL_QUESTIONS} ВАЖНЫХ ВОПРОСОВ", align="L", new_x="LMARGIN", new_y="NEXT")
        
        self.ln(50)
        self.set_font("DS", "I", 10)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Составлено на основе учебников НИУ МГСУ, лекций, ТК РФ и ФЗ.", align="L", new_x="LMARGIN", new_y="NEXT")

    def chapter_title(self, num, title):
        if self.get_y() > 240:
            self.add_page()
        self.ln(6)
        self.set_fill_color(*self.COLOR_BLUE)
        self.set_text_color(255, 255, 255)
        self.set_font("DS", "B", 14)
        
        title_cl = clean_markdown(title)
        lines = self.multi_cell(self.w - 40, 8, f"Вопрос {num}. {title_cl}", fill=True, align="L", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        # Reset colors so next elements don't randomly adopt the Blue Fill / White Text
        self.set_text_color(*self.COLOR_GRAY)
        self.set_fill_color(255, 255, 255)

    def section_title(self, title):
        if self.get_y() > 250:
            self.add_page()
        self.ln(4)
        self.set_font("DS", "B", 11)
        self.set_text_color(*self.COLOR_DARK)
        self.multi_cell(0, 6, clean_markdown(title), align="L")
        self.ln(1)

    def body_text(self, text):
        self.set_font("DS", "", 10)
        self.set_text_color(*self.COLOR_GRAY)
        self.multi_cell(0, 5.5, clean_markdown(text), align="L")
        self.ln(1.5)

    def bullet_point(self, text):
        self.set_font("DS", "", 10)
        self.set_text_color(*self.COLOR_GRAY)
        old_l = self.l_margin
        self.set_left_margin(old_l + 6)
        self.set_x(old_l)
        self.cell(6, 5.5, "•", align="C")
        self.multi_cell(0, 5.5, clean_markdown(text), align="L")
        self.set_left_margin(old_l)
        self.ln(1)

    def add_image_placeholder(self, text):
        if self.get_y() > 220:
            self.add_page()
        self.ln(3)
        w = self.w - self.l_margin - self.r_margin
        self.set_fill_color(240, 243, 248)
        self.set_draw_color(*self.COLOR_BLUE)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, w, 25, style="D")
        self.set_xy(self.l_margin, y0 + 10)
        self.set_font("DS", "I", 9)
        self.set_text_color(*self.COLOR_BLUE)
        self.multi_cell(w, 5, "[Место для инфографики: " + clean_markdown(text) + "]", align="C")
        self.set_y(y0 + 28)
        self.ln(2)
        # Reset colors
        self.set_text_color(*self.COLOR_GRAY)
        self.set_fill_color(255, 255, 255)

    def quote_block(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(2)
        old_l = self.l_margin
        w = self.w - old_l - self.r_margin
        self.set_fill_color(245, 235, 235)
        self.set_left_margin(old_l + 4)
        
        self.set_font("DS", "I", 9)
        self.set_text_color(*self.COLOR_DARK)
        
        lines = self.multi_cell(w - 6, 5, clean_markdown(text), dry_run=True, output="LINES")
        block_h = len(lines) * 5 + 4
        y0 = self.get_y()
        self.set_left_margin(old_l)
        
        self.rect(old_l, y0, w, block_h, style="F")
        self.set_fill_color(*self.COLOR_ACCENT)
        self.rect(old_l, y0, 2, block_h, style="F")
        
        self.set_left_margin(old_l + 4)
        self.set_xy(old_l + 4, y0 + 2)
        self.multi_cell(w - 6, 5, clean_markdown(text), align="L")
        
        self.set_left_margin(old_l)
        self.set_y(y0 + block_h + 3)
        # Reset colors
        self.set_text_color(*self.COLOR_GRAY)
        self.set_fill_color(255, 255, 255)

    def formula_block(self, text):
        if self.get_y() > 250:
            self.add_page()
        self.ln(2)
        self.set_font("DS", "B", 11)
        self.set_text_color(*self.COLOR_BLUE)
        old_l = self.l_margin
        self.set_left_margin(old_l + 10)
        self.set_x(old_l + 10)
        self.multi_cell(0, 7, clean_formula(text), align="L")
        self.set_left_margin(old_l)
        self.ln(2)
        # Reset colors
        self.set_text_color(*self.COLOR_GRAY)

    def render_table(self, headers, rows):
        if self.get_y() > 230:
            self.add_page()
        self.ln(3)

        self.set_font("DS", "B", 9)
        self.set_text_color(*self.COLOR_GRAY)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*self.COLOR_DARK)
        
        headings_style = FontFace(emphasis="B", color=self.COLOR_DARK, fill_color=(255, 255, 255))

        with self.table(
            borders_layout="ALL",
            cell_fill_mode=TableCellFillMode.NONE,
            line_height=5.5,
            text_align="LEFT",
            width=self.w - 40,
            first_row_as_headings=True
        ) as table:
            # Header
            row = table.row()
            for h in headers:
                row.cell(clean_markdown(h), style=headings_style)
            
            # Data
            self.set_font("DS", "", 9)
            for r in rows:
                row = table.row()
                for i in range(len(headers)):
                    val = clean_markdown(r[i]) if i < len(r) else ""
                    row.cell(val)

        self.ln(4)

def parse_final_markdown():
    path = os.path.join(ANSWERS_DIR, "Охрана_труда_ФИНАЛ.md")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    questions = []
    current_q = None
    current_section = None
    in_table = False
    table_headers = []
    table_rows = []

    def flush_table():
        nonlocal in_table, table_headers, table_rows
        if in_table and table_headers and current_section is not None:
            current_section["items"].append(("table", (table_headers[:], table_rows[:])))
        in_table = False
        table_headers = []
        table_rows = []

    for line in content.split("\n"):
        ls = line.strip()

        if ls.startswith("|") and all(c in "-|: " for c in ls):
            continue

        if in_table and not ls.startswith("|"):
            flush_table()

        if ls.startswith("## Вопрос "):
            if current_q:
                flush_table()
                if current_section:
                    current_q["sections"].append(current_section)
                questions.append(current_q)
            
            match = re.match(r'## Вопрос (\d+)\.\s*(.*)', ls)
            if match:
                current_q = {"num": int(match.group(1)), "title": match.group(2).strip(), "sections": []}
                current_section = {"heading": "", "items": []}
            continue

        if current_q is None:
            continue

        if ls.startswith("### ") or ls.startswith("#### "):
            flush_table()
            if current_section and current_section["items"]:
                current_q["sections"].append(current_section)
            current_section = {"heading": ls.lstrip("#").strip(), "items": []}
            continue

        if ls in ("", "---"):
            continue

        if current_section is None:
            current_section = {"heading": "", "items": []}

        if ls.startswith("!["):
            match = re.search(r'!\[(.*?)\]', ls)
            if match:
                current_section["items"].append(("image", match.group(1)))
            continue

        if ls.startswith("|") and "|" in ls[1:]:
            cells = [c.strip() for c in ls.split("|")]
            cells = [c for c in cells if c]
            if not in_table:
                in_table = True
                table_headers = cells
                table_rows = []
            else:
                table_rows.append(cells)
            continue

        if "$$" in ls:
            formula = ls.replace("$$", "").strip()
            if formula:
                current_section["items"].append(("formula", formula))
            continue

        if ls.startswith(">"):
            current_section["items"].append(("quote", ls.lstrip("> ").strip()))
            continue

        if re.match(r'^[-*]\s+', ls) or re.match(r'^\d+\.\s+', ls):
            current_section["items"].append(("bullet", re.sub(r'^[-*\d.]+\s+', '', ls).strip()))
            continue

        if ls:
            current_section["items"].append(("text", ls))

    if current_q:
        flush_table()
        if current_section:
            current_q["sections"].append(current_section)
        questions.append(current_q)

    return questions

def generate():
    pdf = ExamPDF()
    pdf.add_title_page()
    questions = parse_final_markdown()
    
    print(f"Обработано вопросов: {len(questions)}")
    
    # 1. Генерируем оглавление после титульного листа
    pdf.add_page()
    pdf.set_font("DS", "B", 18)
    pdf.set_text_color(*pdf.COLOR_DARK)
    pdf.cell(0, 12, "СПИСОК ВОПРОСОВ", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    
    pdf.set_font("DS", "", 10)
    for q in questions:
        title_text = clean_markdown(q["title"])
        pdf.set_font("DS", "B", 10)
        pdf.set_text_color(*pdf.COLOR_BLUE)
        pdf.cell(8, 6, f"{q['num']}.", align="R")
        
        pdf.set_x(pdf.l_margin + 10)
        pdf.set_font("DS", "", 10)
        pdf.set_text_color(*pdf.COLOR_GRAY)
        pdf.multi_cell(0, 6, title_text, align="L")
        pdf.ln(1)
    
    # 2. Выводим ответы (с новой страницы)
    pdf.add_page()
    
    for q in questions:
        pdf.chapter_title(q["num"], q["title"])
        for sec in q["sections"]:
            if sec["heading"]:
                pdf.section_title(sec["heading"])
            for itype, idata in sec["items"]:
                if itype == "text": pdf.body_text(idata)
                elif itype == "bullet": pdf.bullet_point(idata)
                elif itype == "quote": pdf.quote_block(idata)
                elif itype == "formula": pdf.formula_block(idata)
                elif itype == "image": pdf.add_image_placeholder(idata)
                elif itype == "table": pdf.render_table(idata[0], idata[1])

    pdf.output(OUTPUT)
    print(f"PDF успешно создан: {OUTPUT}")

if __name__ == "__main__":
    generate()
