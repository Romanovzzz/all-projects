"""
Генератор PDF v2 — Спецкурс по проектированию ЖБ и каменных конструкций.
С иллюстрациями из УМП, профессиональным оформлением формул, таблицами.
Формат и стиль — по образцу generate_pdf.py из «Металлических конструкций».
"""

import os
import re
from fpdf import FPDF

# --- Пути ---
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(
    os.path.dirname(BASE),  # all-projects
    "Металлические конструкции", "dejavu-fonts-ttf-2.37", "ttf"
)
ANSWERS_DIR = os.path.join(BASE, "Ответы")
ILL_DIR = os.path.join(ANSWERS_DIR, "illustrations")
OUTPUT = os.path.join(ANSWERS_DIR, "Спецкурс_ответы_v2.pdf")

# --- Маппинг: номер вопроса -> [(файл_иллюстрации, подпись)] ---
QUESTION_IMAGES = {
    "K1": [
        ("k01_fig1_1_winkler.jpg", "Рис. 1.1 — Схематичное изображение модели Винклера — Фусса (УМП, стр. 9)"),
    ],
    "K2": [
        ("k01_fig1_2_pasternak.jpg", "Рис. 1.2 — Модель с двумя коэффициентами постели C1 и C2 (УМП, стр. 9)"),
    ],
    "K4": [
        ("k04_fig1_6_reinforcement.jpg", "Рис. 1.6 — Армирование фундаментной плиты: верхнее и нижнее (УМП, стр. 26)"),
    ],
    "K7": [
        ("k07_fig1_7_punching.jpg", "Рис. 1.7 — Расчёт на продавливание: расчётный контур и пирамида (УМП, стр. 29)"),
        ("k07_fig1_8_punching_plan.jpg", "Рис. 1.8 — Контур продавливания в плане (УМП, стр. 30)"),
    ],
    "K9": [
        ("k09_fig1_9_anchorage.jpg", "Рис. 1.9-1.10 — Анкеровка и нахлёстка арматуры (УМП, стр. 38)"),
    ],
    "K11": [
        ("k11_fig1_11_shear_reinf.jpg", "Зона установки поперечной арматуры при продавливании (УМП, стр. 31)"),
    ],
    "K15": [
        ("z_fig2_1_punching_schemes.jpg", "Рис. 2.1 — Схемы продавливания для центральной, краевой и угловой колонн (УМП, стр. 41)"),
        ("z_fig2_2_critical_section.jpg", "Рис. 2.2 — Расчётное сечение продавливания (УМП, стр. 42)"),
    ],
    "1.3": [
        ("z_fig2_3_contours.jpg", "Рис. 2.3 — Расчётные контуры продавливания у края и угла плиты (УМП, стр. 43)"),
    ],
    "1.12": [
        ("k01_fig1_1_winkler.jpg", "Рис. 1.1 — Модель Винклера (клавишная модель) (УМП, стр. 9)"),
        ("k01_fig1_2_pasternak.jpg", "Рис. 1.2 — Модель Пастернака (двухкоэффициентная) (УМП, стр. 9)"),
    ],
    "6.4": [
        ("z_fig4_1_frp_bend.jpg", "Рис. 4.1 — Усиление изгибаемого ЖБ элемента композитом (УМП, стр. 82)"),
    ],
    "6.5": [
        ("z_fig6_3_masonry_frp.jpg", "Рис. 6.3 — Усиление каменных конструкций обоймой из композитных материалов (УМП, стр. 129)"),
    ],
    "6.7": [
        ("z_fig4_2_frp_shear.jpg", "Рис. 4.2 — Усиление наклонного сечения U-образными лентами (УМП, стр. 90)"),
        ("z_fig4_3_frp_column.jpg", "Рис. 4.3 — Усиление сжатого элемента обмоткой из FRP (УМП, стр. 95)"),
    ],
    "5.2": [
        ("z_fig6_1_hanging_wall.jpg", "Рис. 6.1 — Висячие стены каменной кладки (УМП, стр. 120)"),
        ("z_fig6_2_arches.jpg", "Рис. 6.2 — Расчётные схемы висячих стен (УМП, стр. 124)"),
    ],
}


class SpetskursPDF(FPDF):
    """PDF с профессиональным оформлением для спецкурса."""

    BLUE_DARK = (24, 57, 99)
    BLUE_MED = (41, 98, 163)
    BLUE_LIGHT = (220, 235, 252)
    GRAY_TEXT = (50, 50, 50)
    GRAY_LINE = (180, 200, 220)
    ACCENT = (180, 50, 30)
    WHITE = (255, 255, 255)
    GREEN = (34, 120, 60)
    FORMULA_BG = (245, 248, 255)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=22)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))
        self.add_font("DSr", "", os.path.join(FONT_DIR, "DejaVuSerif.ttf"))
        self.add_font("DSr", "B", os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf"))
        self.add_font("DSr", "I", os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf"))
        self.add_font("DSr", "BI", os.path.join(FONT_DIR, "DejaVuSerif-BoldItalic.ttf"))
        self.add_font("DM", "", os.path.join(FONT_DIR, "DejaVuSansMono.ttf"))
        self.add_font("DM", "B", os.path.join(FONT_DIR, "DejaVuSansMono-Bold.ttf"))

    def header(self):
        if self.page_no() <= 2:
            return
        self.set_font("DS", "I", 7)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 5, "Спецкурс по проектированию ЖБ и каменных конструкций", align="L")
        self.cell(0, 5, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(3)

    def footer(self):
        self.set_y(-14)
        self.set_font("DS", "I", 6)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6,
                  "Источники: УМП (НИУ МГСУ, 2021); СП 63; СП 22; СП 20; СП 15; ГОСТ 27751",
                  align="C")

    def add_title_page(self):
        self.add_page()
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 0, 210, 8, style="F")
        self.ln(45)
        self.set_font("DS", "B", 24)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(0, 13, "СПЕЦКУРС", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "B", 16)
        self.cell(0, 10, "ПО ПРОЕКТИРОВАНИЮ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, "ЖЕЛЕЗОБЕТОННЫХ И КАМЕННЫХ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 10, "КОНСТРУКЦИЙ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)
        self.set_font("DS", "", 12)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 8, "Ответы на вопросы к курсовому проекту и зачёту", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.2)
        cx = self.w / 2
        self.line(cx - 45, self.get_y(), cx + 45, self.get_y())
        self.ln(8)
        self.set_font("DS", "B", 32)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 16, "67", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 11)
        self.set_text_color(*self.GRAY_TEXT)
        self.cell(0, 7, "вопросов с подробными ответами", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)
        self.set_font("DS", "B", 9)
        self.set_text_color(*self.GREEN)
        self.cell(0, 7, "С иллюстрациями из учебного пособия", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(12)
        self.set_font("DS", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, "Составлено на основе:", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 8)
        for s in [
            "УМП «Спецкурс» (НИУ МГСУ, 2021)",
            "СП 63.13330.2018; СП 22.13330.2016; СП 20.13330.2016",
            "СП 15.13330.2020; СП 28.13330.2017; ГОСТ 27751-2014",
        ]:
            self.cell(0, 5, f"  {s}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 289, 210, 8, style="F")

    def add_part_header(self, title):
        self.add_page()
        self.ln(30)
        self.set_font("DS", "B", 18)
        self.set_text_color(*self.BLUE_DARK)
        self.multi_cell(0, 10, title, align="C")
        self.ln(2)
        self.set_draw_color(*self.ACCENT)
        self.set_line_width(0.8)
        cx = self.w / 2
        self.line(cx - 50, self.get_y(), cx + 50, self.get_y())
        self.ln(8)

    def add_section_header(self, title):
        self.add_page()
        self.ln(4)
        y0 = self.get_y()
        self.set_fill_color(230, 237, 248)
        self.set_draw_color(*self.BLUE_MED)
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, y0, w, 12, style="FD")
        self.set_xy(self.l_margin + 4, y0 + 2)
        self.set_font("DS", "B", 10)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(w - 8, 8, title[:80], align="C")
        self.set_y(y0 + 16)
        self.set_text_color(*self.GRAY_TEXT)

    def add_question_header(self, qid, title):
        if self.get_y() > 240:
            self.add_page()
        self.ln(4)
        y_start = self.get_y()
        block_h = 14
        w = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(self.l_margin, y_start, w, block_h, style="F")
        self.set_xy(self.l_margin + 2, y_start + 1)
        self.set_font("DS", "B", 16)
        self.set_text_color(*self.WHITE)
        self.cell(18, block_h - 2, qid, align="C")
        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.4)
        self.line(self.l_margin + 22, y_start + 3, self.l_margin + 22, y_start + block_h - 3)
        self.set_xy(self.l_margin + 26, y_start + 1)
        self.set_font("DS", "B", 9)
        self.multi_cell(w - 30, 5.5, title[:100], align="L")
        self.set_y(y_start + block_h + 3)
        self.set_text_color(*self.GRAY_TEXT)

    def add_subheading(self, text):
        if self.get_y() > 260:
            self.add_page()
        self.ln(3)
        self.set_font("DS", "B", 9.5)
        self.set_text_color(*self.BLUE_MED)
        y0 = self.get_y()
        self.set_fill_color(*self.BLUE_MED)
        self.rect(self.l_margin, y0, 2.5, 5.5, style="F")
        self.set_x(self.l_margin + 5)
        self.cell(0, 5.5, text[:90], new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)

    def add_body_text(self, text):
        self.set_font("DSr", "", 9)
        self.set_text_color(*self.GRAY_TEXT)
        w = self.w - self.l_margin - self.r_margin
        try:
            self.multi_cell(w, 5, text)
        except Exception:
            self.cell(w, 5, text[:150] + "...", new_x="LMARGIN", new_y="NEXT")
        self.ln(0.5)

    def add_formula(self, text):
        self.ln(1.5)
        self.set_fill_color(*self.FORMULA_BG)
        self.set_draw_color(*self.BLUE_LIGHT)
        self.set_font("DM", "B", 9)
        self.set_text_color(*self.BLUE_DARK)
        x0 = self.l_margin + 4
        w_avail = self.w - self.l_margin - self.r_margin - 8
        y0 = self.get_y()
        h = 8
        self.rect(x0 - 2, y0, w_avail + 4, h, style="FD")
        self.set_xy(x0, y0 + 1)
        try:
            self.cell(w_avail, 5.5, text.strip(), new_x="LMARGIN", new_y="NEXT")
        except Exception:
            pass
        self.set_y(y0 + h + 1)
        self.set_text_color(*self.GRAY_TEXT)

    def add_bullet(self, text, level=0):
        self.set_font("DSr", "", 9)
        self.set_text_color(*self.GRAY_TEXT)
        indent = self.l_margin + 3 + level * 5
        self.set_x(indent)
        self.set_font("DS", "", 8)
        self.cell(4, 5, "-")
        self.set_font("DSr", "", 9)
        w_avail = self.w - indent - self.r_margin - 5
        if w_avail < 30:
            w_avail = self.w - self.l_margin - self.r_margin - 12
            self.set_x(self.l_margin + 9)
        try:
            self.multi_cell(w_avail, 5, text)
        except Exception:
            self.cell(w_avail, 5, text[:120] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_table(self, headers, rows, col_widths=None):
        if self.get_y() > 250:
            self.add_page()
        self.ln(2)
        w_total = self.w - self.l_margin - self.r_margin
        n_cols = len(headers)
        if col_widths is None:
            col_widths = [w_total / n_cols] * n_cols
        self.set_fill_color(*self.BLUE_DARK)
        self.set_text_color(*self.WHITE)
        self.set_font("DS", "B", 7.5)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h[:25], border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(*self.GRAY_TEXT)
        self.set_font("DSr", "", 7.5)
        fill = False
        for row in rows:
            if self.get_y() > 270:
                self.add_page()
            if fill:
                self.set_fill_color(245, 248, 253)
            else:
                self.set_fill_color(255, 255, 255)
            for i, cell_val in enumerate(row):
                w = col_widths[min(i, len(col_widths)-1)]
                self.cell(w, 6, str(cell_val)[:30], border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(2)

    def add_illustration(self, img_path, caption):
        if not os.path.exists(img_path):
            return
        self.add_page()
        self.set_fill_color(230, 245, 235)
        self.set_draw_color(*self.GREEN)
        y0 = self.get_y()
        w = self.w - self.l_margin - self.r_margin
        self.rect(self.l_margin, y0, w, 8, style="FD")
        self.set_font("DS", "BI", 8)
        self.set_text_color(*self.GREEN)
        self.set_xy(self.l_margin + 3, y0 + 1)
        self.cell(0, 6, "ИЛЛЮСТРАЦИЯ ИЗ УЧЕБНОГО ПОСОБИЯ")
        self.set_y(y0 + 10)
        img_w = w - 6
        try:
            self.image(img_path, x=self.l_margin + 3, y=self.get_y(), w=img_w)
        except Exception as e:
            self.set_font("DS", "I", 9)
            self.set_text_color(200, 0, 0)
            self.cell(0, 6, f"[Ошибка: {e}]", new_x="LMARGIN", new_y="NEXT")
            return
        self.ln(2)
        self.set_font("DS", "I", 7.5)
        self.set_text_color(100, 100, 100)
        self.set_x(self.l_margin)
        self.multi_cell(w, 4.5, caption, align="C")


def parse_md_content():
    """Парсит MD-файл ответов v2."""
    md_path = os.path.join(ANSWERS_DIR, "spetskurs_all_answers_v2.md")
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    parts = []
    current_q = None
    current_sub = None
    in_code_block = False

    for line in content.split("\n"):
        ls = line.strip()

        # Кодовые блоки — пропускаем (заменяются иллюстрациями)
        if ls.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if not ls or ls.startswith("**Источники:**") or ls.startswith("*Дата составления"):
            continue

        # Части
        if ls.startswith("# ЧАСТЬ "):
            if current_q:
                if current_sub:
                    current_q["subs"].append(current_sub)
                parts.append(current_q)
                current_q = None
                current_sub = None
            title = ls.lstrip("# ").strip()
            parts.append({"type": "part", "title": title})
            continue

        # Пропуск основного заголовка
        if ls.startswith("# СПЕЦКУРС") or ls.startswith("## Полный сборник"):
            continue

        # Разделы
        if ls.startswith("## РАЗДЕЛ "):
            if current_q:
                if current_sub:
                    current_q["subs"].append(current_sub)
                parts.append(current_q)
                current_q = None
                current_sub = None
            title = ls.lstrip("## ").strip()
            parts.append({"type": "section", "title": title})
            continue

        # Вопросы курсового
        m_k = re.match(r'^##\s+К(\d+)\.\s+(.+)', ls)
        if m_k:
            if current_q:
                if current_sub:
                    current_q["subs"].append(current_sub)
                parts.append(current_q)
            current_q = {"type": "question", "id": f"К{m_k.group(1)}", "title": m_k.group(2), "subs": []}
            current_sub = None
            continue

        # Вопросы зачёта
        m_z = re.match(r'^###\s+(\d+\.\d+)\.\s+(.+)', ls)
        if m_z:
            if current_q:
                if current_sub:
                    current_q["subs"].append(current_sub)
                parts.append(current_q)
            current_q = {"type": "question", "id": m_z.group(1), "title": m_z.group(2), "subs": []}
            current_sub = None
            continue

        if current_q is None:
            continue

        # Подзаголовки
        if ls.startswith("### "):
            if current_sub:
                current_q["subs"].append(current_sub)
            current_sub = {"heading": ls[4:].strip(), "items": []}
            continue

        if current_sub is None:
            current_sub = {"heading": "", "items": []}

        if ls == "---":
            continue

        # Формулы (с отступом 4+ пробел)
        if line.startswith("    ") and len(ls) > 3 and not ls.startswith("- "):
            current_sub["items"].append(("formula", ls))
            continue

        # Строки таблиц
        if "|" in ls and ls.count("|") >= 3:
            if ls.replace("|", "").replace("-", "").replace(" ", "") == "":
                continue  # разделитель таблицы
            cells = [c.strip() for c in ls.split("|") if c.strip()]
            if cells:
                current_sub["items"].append(("table_row", cells))
            continue

        # Буллеты
        if ls.startswith("- ") or ls.startswith("* "):
            text = ls[2:].replace("**", "").strip()
            current_sub["items"].append(("bullet", text))
            continue

        m_num = re.match(r'^(\d+)\.\s+(.+)', ls)
        if m_num and int(m_num.group(1)) <= 20:
            text = m_num.group(0).replace("**", "").strip()
            current_sub["items"].append(("bullet", text))
            continue

        # Обычный текст
        text = ls.replace("**", "").strip()
        if text:
            current_sub["items"].append(("text", text))

    if current_q:
        if current_sub:
            current_q["subs"].append(current_sub)
        parts.append(current_q)

    return parts


def build_pdf():
    pdf = SpetskursPDF()
    pdf.add_title_page()

    parts = parse_md_content()
    q_count = sum(1 for p in parts if p["type"] == "question")
    print(f"Parsed {len(parts)} elements, {q_count} questions")

    # Оглавление
    pdf.add_page()
    pdf.set_font("DS", "B", 14)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 10, "СОДЕРЖАНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for p in parts:
        if p["type"] == "part":
            pdf.ln(2)
            pdf.set_font("DS", "B", 10)
            pdf.set_text_color(*pdf.BLUE_DARK)
            pdf.cell(0, 6, p["title"][:85], new_x="LMARGIN", new_y="NEXT")
        elif p["type"] == "section":
            pdf.set_font("DS", "B", 8)
            pdf.set_text_color(*pdf.BLUE_MED)
            pdf.cell(0, 5, f"  {p['title'][:80]}", new_x="LMARGIN", new_y="NEXT")
        elif p["type"] == "question":
            pdf.set_font("DS", "", 7.5)
            pdf.set_text_color(*pdf.GRAY_TEXT)
            pdf.cell(14, 4.5, f"  {p['id']}.")
            pdf.cell(0, 4.5, p["title"][:85], new_x="LMARGIN", new_y="NEXT")
            if pdf.get_y() > 275:
                pdf.add_page()

    # Основное содержание
    for p in parts:
        if p["type"] == "part":
            pdf.add_part_header(p["title"])
            continue
        if p["type"] == "section":
            pdf.add_section_header(p["title"])
            continue
        if p["type"] == "question":
            pdf.add_page()
            pdf.add_question_header(p["id"], p["title"])

            table_headers = None
            table_rows = []

            for sub in p["subs"]:
                if table_rows and sub["heading"]:
                    if table_headers:
                        cw = (pdf.w - pdf.l_margin - pdf.r_margin) / len(table_headers)
                        pdf.add_table(table_headers, table_rows, [cw] * len(table_headers))
                    table_headers = None
                    table_rows = []

                if sub["heading"]:
                    pdf.add_subheading(sub["heading"])

                for item_type, item_data in sub["items"]:
                    # Завершить таблицу при смене типа
                    if item_type != "table_row" and table_rows:
                        if table_headers:
                            cw = (pdf.w - pdf.l_margin - pdf.r_margin) / len(table_headers)
                            pdf.add_table(table_headers, table_rows, [cw] * len(table_headers))
                        table_headers = None
                        table_rows = []

                    if item_type == "formula":
                        pdf.add_formula(item_data)
                    elif item_type == "bullet":
                        pdf.add_bullet(item_data)
                    elif item_type == "text":
                        pdf.add_body_text(item_data)
                    elif item_type == "table_row":
                        if table_headers is None:
                            table_headers = item_data
                        else:
                            table_rows.append(item_data)

            # Завершающая таблица
            if table_rows and table_headers:
                cw = (pdf.w - pdf.l_margin - pdf.r_margin) / len(table_headers)
                pdf.add_table(table_headers, table_rows, [cw] * len(table_headers))

            # Иллюстрации
            q_key = p["id"].replace("\u041a", "K")  # К -> K
            if q_key in QUESTION_IMAGES:
                for img_file, caption in QUESTION_IMAGES[q_key]:
                    img_path = os.path.join(ILL_DIR, img_file)
                    pdf.add_illustration(img_path, caption)

    pdf.output(OUTPUT)
    print(f"\n{'='*50}")
    print(f"PDF: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")
    n_img = sum(len(v) for v in QUESTION_IMAGES.values())
    print(f"Illustrations: {n_img}")


if __name__ == "__main__":
    build_pdf()
