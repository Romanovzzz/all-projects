"""
Генератор PDF v2 — с иллюстрациями из учебника Кудишина.
Вставляет сканированные страницы учебника после соответствующих вопросов.
"""

import os
from fpdf import FPDF

# --- Пути ---
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "dejavu-fonts-ttf-2.37", "ttf")
ANSWERS_DIR = os.path.join(BASE, "Ответы")
ILL_DIR = os.path.join(ANSWERS_DIR, "illustrations")
OUTPUT = os.path.join(ANSWERS_DIR, "Металлические_конструкции_ответы.pdf")

# --- Маппинг: номер вопроса -> [(файл_иллюстрации, подпись)] ---
QUESTION_IMAGES = {
    2: [
        ("q02_fig10_1_karkas.jpg", "\u0420\u0438\u0441. 10.1 \u2014 \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u0438\u0432\u043d\u0430\u044f \u0441\u0445\u0435\u043c\u0430 \u043a\u0430\u0440\u043a\u0430\u0441\u0430 (\u0441\u0442\u0440. 302, \u041a\u0443\u0434\u0438\u0448\u0438\u043d)"),
        ("q02_fig10_2_schemes.jpg", "\u0420\u0438\u0441. 10.2 \u2014 \u041a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u0441\u0445\u0435\u043c\u044b \u043a\u0430\u0440\u043a\u0430\u0441\u043e\u0432 (\u0441\u0442\u0440. 307)"),
        ("q02_fig10_4_joints.jpg", "\u0420\u0438\u0441. 10.4 \u2014 \u0412\u0438\u0434\u044b \u0441\u043e\u043f\u0440\u044f\u0436\u0435\u043d\u0438\u0439 \u0440\u0438\u0433\u0435\u043b\u044f \u0441 \u043a\u043e\u043b\u043e\u043d\u043d\u043e\u0439 (\u0441\u0442\u0440. 308)"),
    ],
    3: [
        ("q03_fig_snow_wind.jpg", "\u0421\u0445\u0435\u043c\u0430 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u0438\u044f \u043f\u043e\u043f\u0435\u0440\u0435\u0447\u043d\u043e\u0439 \u0440\u0430\u043c\u044b (\u0441\u0442\u0440. 313)"),
    ],
    4: [
        ("q04_fig11_1_crane_loads.jpg", "\u0420\u0438\u0441. 11.1 \u2014 \u041b\u0438\u043d\u0438\u0438 \u0432\u043b\u0438\u044f\u043d\u0438\u044f \u043e\u043f\u043e\u0440\u043d\u044b\u0445 \u0440\u0435\u0430\u043a\u0446\u0438\u0439 (\u0441\u0442\u0440. 313)"),
    ],
    5: [
        ("q05_fig11_2_influence.jpg", "\u0420\u0438\u0441. 11.2 \u2014 \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u043a\u0440\u0430\u043d\u043e\u0432\u044b\u0445 \u043d\u0430\u0433\u0440\u0443\u0437\u043e\u043a (\u0441\u0442\u0440. 314)"),
    ],
    6: [
        ("q06_fig11_5_bracing.jpg", "\u0420\u0438\u0441. 11.5 \u2014 \u0421\u0445\u0435\u043c\u044b \u0441\u0432\u044f\u0437\u0435\u0439 \u043c\u0435\u0436\u0434\u0443 \u043a\u043e\u043b\u043e\u043d\u043d\u0430\u043c\u0438 (\u0441\u0442\u0440. 319)"),
    ],
    7: [
        ("q07_fig11_6_roof_bracing.jpg", "\u0420\u0438\u0441. 11.6\u201311.8 \u2014 \u0421\u0432\u044f\u0437\u0438 \u043f\u043e \u0432\u0435\u0440\u0445\u043d\u0435\u043c\u0443 \u043f\u043e\u044f\u0441\u0443 \u0444\u0435\u0440\u043c (\u0441\u0442\u0440. 323)"),
    ],
    8: [
        ("q08_fig11_9_spatial.jpg", "\u0420\u0438\u0441. 11.9 \u2014 \u041f\u0440\u043e\u0441\u0442\u0440\u0430\u043d\u0441\u0442\u0432\u0435\u043d\u043d\u0430\u044f \u0440\u0430\u0431\u043e\u0442\u0430 \u043a\u0430\u0440\u043a\u0430\u0441\u0430 (\u0441\u0442\u0440. 327)"),
    ],
    9: [
        ("q09_fig_rsu_table.jpg", "\u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0420\u0421\u0423 \u0438 \u0441\u0445\u0435\u043c\u044b \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u0438\u0439 (\u0441\u0442\u0440. 317)"),
    ],
    10: [
        ("q10_fig13_4_trusses.jpg", "\u0420\u0438\u0441. 13.4 \u2014 \u0421\u0445\u0435\u043c\u044b \u0444\u0435\u0440\u043c \u043f\u043e\u043a\u0440\u044b\u0442\u0438\u0439 (\u0441\u0442\u0440. 371)"),
        ("q10_fig13_5_standard.jpg", "\u0420\u0438\u0441. 13.5 \u2014 \u0422\u0438\u043f\u043e\u0432\u044b\u0435 \u0441\u0442\u0440\u043e\u043f\u0438\u043b\u044c\u043d\u044b\u0435 \u0444\u0435\u0440\u043c\u044b (\u0441\u0442\u0440. 372)"),
    ],
    11: [
        ("q11_fig13_5_loads.jpg", "\u0420\u0438\u0441. 13.5 \u2014 \u0421\u0445\u0435\u043c\u044b \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d\u0438\u044f \u0444\u0435\u0440\u043c (\u0441\u0442\u0440. 373)"),
    ],
    12: [
        ("q12_fig13_3_methods.jpg", "\u0420\u0438\u0441. 13.3 \u2014 \u041c\u0435\u0442\u043e\u0434 \u0432\u044b\u0440\u0435\u0437\u0430\u043d\u0438\u044f \u0443\u0437\u043b\u043e\u0432 \u0438 \u0441\u0435\u0447\u0435\u043d\u0438\u0439 (\u0441\u0442\u0440. 376)"),
    ],
    13: [
        ("q13_fig13_6_sections.jpg", "\u0420\u0438\u0441. 13.6 \u2014 \u0422\u0438\u043f\u044b \u0441\u0435\u0447\u0435\u043d\u0438\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u043e\u0432 \u0444\u0435\u0440\u043c (\u0441\u0442\u0440. 380)"),
    ],
    14: [
        ("q14_fig14_3_lengths.jpg", "\u0420\u0438\u0441. 14.3 \u2014 \u0421\u0445\u0435\u043c\u0430 \u0440\u0430\u0441\u0447\u0451\u0442\u043d\u044b\u0445 \u0434\u043b\u0438\u043d \u0441\u0442\u0443\u043f\u0435\u043d\u0447\u0430\u0442\u044b\u0445 \u043a\u043e\u043b\u043e\u043d\u043d (\u0441\u0442\u0440. 393)"),
    ],
    15: [
        ("q15_fig14_4_sections.jpg", "\u0420\u0438\u0441. 14.4 \u2014 \u0422\u0438\u043f\u044b \u0441\u0435\u0447\u0435\u043d\u0438\u0439 \u0441\u043f\u043b\u043e\u0448\u043d\u044b\u0445 \u043a\u043e\u043b\u043e\u043d\u043d (\u0441\u0442\u0440. 396)"),
    ],
    16: [
        ("q16_fig14_4_calc.jpg", "\u0420\u0438\u0441. 14.4 \u2014 \u041f\u043e\u0434\u0431\u043e\u0440 \u0441\u0435\u0447\u0435\u043d\u0438\u044f \u043a\u043e\u043b\u043e\u043d\u043d\u044b (\u0441\u0442\u0440. 396)"),
    ],
    17: [
        ("q17_fig14_5_lattice.jpg", "\u0420\u0438\u0441. 14.5 \u2014 \u0422\u0438\u043f\u044b \u0441\u0435\u0447\u0435\u043d\u0438\u0439 \u0441\u043a\u0432\u043e\u0437\u043d\u044b\u0445 \u043a\u043e\u043b\u043e\u043d\u043d (\u0441\u0442\u0440. 397)"),
    ],
    18: [
        ("q18_fig14_8_lattice.jpg", "\u0420\u0438\u0441. 14.8 \u2014 \u041f\u043b\u0430\u043d\u043a\u0438 \u0438 \u0440\u0430\u0441\u043a\u043e\u0441\u043d\u0430\u044f \u0440\u0435\u0448\u0451\u0442\u043a\u0430 (\u0441\u0442\u0440. 403)"),
    ],
    19: [
        ("q19_fig14_12_joint.jpg", "\u0420\u0438\u0441. 14.12\u201314.13 \u2014 \u0421\u0442\u044b\u043a \u0432\u0435\u0440\u0445\u043d\u0435\u0439 \u0438 \u043d\u0438\u0436\u043d\u0435\u0439 \u0447\u0430\u0441\u0442\u0435\u0439 (\u0441\u0442\u0440. 405)"),
    ],
    20: [
        ("q20_fig14_16_base.jpg", "\u0420\u0438\u0441. 14.16 \u2014 \u0411\u0430\u0437\u044b \u0432\u043d\u0435\u0446\u0435\u043d\u0442\u0440\u0435\u043d\u043d\u043e \u0441\u0436\u0430\u0442\u044b\u0445 \u043a\u043e\u043b\u043e\u043d\u043d (\u0441\u0442\u0440. 409)"),
    ],
    21: [
        ("q21_fig15_2_crane.jpg", "\u0420\u0438\u0441. 15.2 \u2014 \u0422\u0438\u043f\u044b \u043f\u043e\u0434\u043a\u0440\u0430\u043d\u043e\u0432\u044b\u0445 \u0431\u0430\u043b\u043e\u043a (\u0441\u0442\u0440. 426)"),
    ],
    22: [
        ("q22_fig15_8_moment.jpg", "\u0420\u0438\u0441. 15.8 \u2014 \u041e\u043f\u0440\u0435\u0434\u0435\u043b\u0435\u043d\u0438\u0435 M_max (\u0441\u0442\u0440. 430)"),
    ],
    23: [
        ("q23_fig15_10_strength.jpg", "\u0420\u0438\u0441. 15.10 \u2014 \u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u0440\u043e\u0447\u043d\u043e\u0441\u0442\u0438 \u043f\u043e\u0434\u043a\u0440\u0430\u043d\u043e\u0432\u043e\u0439 \u0431\u0430\u043b\u043a\u0438 (\u0441\u0442\u0440. 434)"),
    ],
    24: [
        ("q24_fig22_reservoir.jpg", "\u0420\u0438\u0441. 22 \u2014 \u041b\u0438\u0441\u0442\u043e\u0432\u044b\u0435 \u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438 (\u0441\u0442\u0440. 548)"),
    ],
    25: [
        ("q25_fig18_largespan.jpg", "\u0420\u0438\u0441. 18 \u2014 \u0411\u043e\u043b\u044c\u0448\u0435\u043f\u0440\u043e\u043b\u0451\u0442\u043d\u044b\u0435 \u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438 (\u0441\u0442\u0440. 481)"),
    ],
    26: [
        ("q26_fig18_2_supports.jpg", "\u0420\u0438\u0441. 18.2\u201318.5 \u2014 \u041e\u043f\u043e\u0440\u043d\u044b\u0435 \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u0444\u0435\u0440\u043c (\u0441\u0442\u0440. 484)"),
    ],
    28: [
        ("q28_fig18_8_frames.jpg", "\u0420\u0438\u0441. 18.8\u201318.12 \u2014 \u0422\u0438\u043f\u044b \u0440\u0430\u043c \u0438 \u043a\u0430\u0440\u043d\u0438\u0437\u043d\u044b\u0439 \u0443\u0437\u0435\u043b (\u0441\u0442\u0440. 500)"),
    ],
    29: [
        ("q29_fig20_1_suspended.jpg", "\u0420\u0438\u0441. 20.1 \u2014 \u0422\u0438\u043f\u044b \u0432\u0438\u0441\u044f\u0447\u0438\u0445 \u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0439 (\u0441\u0442\u0440. 530)"),
        ("q29_fig20_3_double.jpg", "\u0420\u0438\u0441. 20.3 \u2014 \u0414\u0432\u0443\u0445\u043f\u043e\u044f\u0441\u043d\u044b\u0435 \u0432\u0438\u0441\u044f\u0447\u0438\u0435 \u0441\u0438\u0441\u0442\u0435\u043c\u044b (\u0441\u0442\u0440. 535)"),
    ],
}

# Текстовые ссылки для вопросов без картинок (1 и 27 не имеют иллюстраций)
TEXT_REFS = {
    1: "\u0421\u043c. \u0443\u0447\u0435\u0431\u043d\u0438\u043a \u041a\u0443\u0434\u0438\u0448\u0438\u043d\u0430, \u0433\u043b. 10, \u043f. 10.1 (\u0441\u0442\u0440. 302-304)",
    27: "\u0421\u043c. \u041a\u0443\u0434\u0438\u0448\u0438\u043d, \u043f. 18.3-18.4 (\u0441\u0442\u0440. 490-500)",
}


class ExamPDF(FPDF):
    """PDF с красивым оформлением и иллюстрациями."""

    BLUE_DARK = (24, 57, 99)
    BLUE_MED = (41, 98, 163)
    BLUE_LIGHT = (220, 235, 252)
    GRAY_TEXT = (50, 50, 50)
    GRAY_LINE = (180, 200, 220)
    ACCENT = (200, 60, 40)
    WHITE = (255, 255, 255)
    GREEN = (34, 120, 60)

    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=20)
        self.add_font("DS", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DS", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DS", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))
        self.add_font("DS", "BI", os.path.join(FONT_DIR, "DejaVuSans-BoldOblique.ttf"))

    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 8)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 6, "Металлические конструкции — ответы на экзам. вопросы", align="L")
        self.cell(0, 6, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DS", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, "Источники: Кудишин Ю.И. (13-е изд.); СП 16.13330.2017; СП 20.13330.2016",
                  align="C")

    def add_title_page(self):
        self.add_page()
        self.ln(50)
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 0, 210, 8, style="F")

        self.set_font("DS", "B", 26)
        self.set_text_color(*self.BLUE_DARK)
        self.cell(0, 14, "МЕТАЛЛИЧЕСКИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 14, "КОНСТРУКЦИИ", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

        self.set_font("DS", "", 14)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 10, "Ответы на экзаменационные вопросы", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

        self.set_draw_color(*self.ACCENT)
        self.set_line_width(1.2)
        cx = self.w / 2
        self.line(cx - 40, self.get_y(), cx + 40, self.get_y())
        self.ln(8)

        self.set_font("DS", "B", 36)
        self.set_text_color(*self.ACCENT)
        self.cell(0, 18, "29", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 12)
        self.set_text_color(*self.GRAY_TEXT)
        self.cell(0, 8, "вопросов с подробными ответами", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(8)

        self.set_font("DS", "B", 10)
        self.set_text_color(*self.GREEN)
        self.cell(0, 8, "С иллюстрациями из учебника Кудишина", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(10)

        self.set_font("DS", "I", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "Составлено на основе:", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("DS", "", 9)
        sources = [
            "Учебник Кудишина Ю.И., 13-е издание",
            "СП 16.13330.2017 (Стальные конструкции)",
            "СП 20.13330.2016 (Нагрузки и воздействия)",
        ]
        for s in sources:
            self.cell(0, 6, f"  * {s}", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_fill_color(*self.BLUE_DARK)
        self.rect(0, 289, 210, 8, style="F")

    def add_question_header(self, number, title):
        if self.get_y() > 240:
            self.add_page()
        self.ln(4)
        y_start = self.get_y()
        block_h = 16
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(self.l_margin, y_start, self.w - self.l_margin - self.r_margin, block_h, style="F")

        self.set_xy(self.l_margin + 2, y_start + 1)
        self.set_font("DS", "B", 20)
        self.set_text_color(*self.WHITE)
        self.cell(16, block_h - 2, f"{number:02d}", align="C")

        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.5)
        self.line(self.l_margin + 20, y_start + 3, self.l_margin + 20, y_start + block_h - 3)

        self.set_xy(self.l_margin + 24, y_start + 1.5)
        self.set_font("DS", "B", 10)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 28, 6, title, align="L")
        self.set_y(y_start + block_h + 4)
        self.set_text_color(*self.GRAY_TEXT)

    def add_subheading(self, text):
        if self.get_y() > 260:
            self.add_page()
        self.ln(3)
        self.set_font("DS", "B", 10)
        self.set_text_color(*self.BLUE_MED)
        y0 = self.get_y()
        self.set_fill_color(*self.BLUE_MED)
        self.rect(self.l_margin, y0, 2, 6, style="F")
        self.set_x(self.l_margin + 5)
        self.cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)

    def add_body_text(self, text):
        self.set_font("DS", "", 9)
        self.set_text_color(*self.GRAY_TEXT)
        self.set_x(self.l_margin)
        if "|" in text and text.count("|") >= 3:
            cells = [c.strip() for c in text.split("|") if c.strip()]
            text = "  *  ".join(cells)
        w = self.w - self.l_margin - self.r_margin
        try:
            self.multi_cell(w, 5, text)
        except Exception:
            self.cell(w, 5, text[:120] + "...", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def add_formula(self, text):
        self.ln(1)
        self.set_fill_color(*self.BLUE_LIGHT)
        self.set_font("DS", "B", 9)
        self.set_text_color(*self.BLUE_DARK)
        x0 = self.l_margin + 4
        self.set_x(x0)
        w_avail = self.w - self.l_margin - self.r_margin - 8
        try:
            self.multi_cell(w_avail, 6, text, fill=True)
        except Exception:
            self.cell(w_avail, 6, text[:100] + "...", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)

    def add_bullet(self, text, level=0):
        self.set_font("DS", "", 9)
        self.set_text_color(*self.GRAY_TEXT)
        indent = self.l_margin + 3 + level * 4
        marker = ">" if level == 0 else "-"
        self.set_x(indent)
        self.cell(4, 5, marker)
        w_avail = self.w - indent - self.r_margin - 4
        if w_avail < 20:
            w_avail = self.w - self.l_margin - self.r_margin - 10
            self.set_x(self.l_margin + 8)
        try:
            self.multi_cell(w_avail, 5, text)
        except Exception:
            self.cell(w_avail, 5, text[:100] + "...", new_x="LMARGIN", new_y="NEXT")

    def add_illustration(self, img_path, caption):
        """Вставляет иллюстрацию из учебника с подписью."""
        if not os.path.exists(img_path):
            return

        self.add_page()

        # Зелёная плашка с надписью
        self.set_fill_color(230, 245, 235)
        self.set_draw_color(*self.GREEN)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, self.w - self.l_margin - self.r_margin, 8, style="FD")
        self.set_font("DS", "BI", 9)
        self.set_text_color(*self.GREEN)
        self.set_xy(self.l_margin + 3, y0 + 1)
        self.cell(0, 6, "ИЛЛЮСТРАЦИЯ ИЗ УЧЕБНИКА")
        self.set_y(y0 + 10)

        # Изображение — масштабируем по ширине
        img_w = self.w - self.l_margin - self.r_margin - 4
        try:
            self.image(img_path, x=self.l_margin + 2, y=self.get_y(), w=img_w)
        except Exception as e:
            self.set_font("DS", "I", 9)
            self.set_text_color(200, 0, 0)
            self.cell(0, 6, f"[Err image: {e}]", new_x="LMARGIN", new_y="NEXT")
            return

        # Подпись
        self.ln(2)
        self.set_font("DS", "I", 8)
        self.set_text_color(100, 100, 100)
        self.set_x(self.l_margin)
        self.multi_cell(self.w - self.l_margin - self.r_margin, 5, caption, align="C")

    def add_text_reference(self, text):
        """Добавляет текстовую ссылку на источник."""
        self.ln(3)
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(200, 170, 80)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, self.w - self.l_margin - self.r_margin, 10, style="FD")
        self.set_font("DS", "BI", 8)
        self.set_text_color(150, 110, 30)
        self.set_xy(self.l_margin + 3, y0 + 1)
        self.cell(self.w - self.l_margin - self.r_margin - 6, 4, "Иллюстрации:")
        self.set_xy(self.l_margin + 3, y0 + 5)
        self.set_font("DS", "I", 8)
        self.set_text_color(100, 80, 30)
        self.cell(self.w - self.l_margin - self.r_margin - 6, 4, text)
        self.set_y(y0 + 12)
        self.set_text_color(*self.GRAY_TEXT)


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

            if line_stripped.startswith("## \u0412\u043e\u043f\u0440\u043e\u0441 "):
                if current_q:
                    if current_section:
                        current_q["sections"].append(current_section)
                    questions.append(current_q)
                # Parse: "## Вопрос 1. Title..."
                after_prefix = line_stripped[len("## \u0412\u043e\u043f\u0440\u043e\u0441 "):]
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

            if line_stripped in ("", "---") or line_stripped.startswith("*Istochniki") or line_stripped.startswith("*\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438"):
                continue
            if line_stripped.startswith("# \u041e\u0442\u0432\u0435\u0442\u044b"):
                continue
            # Skip illustration reference lines from MD source
            if line_stripped.startswith("> **") or line_stripped.startswith("> **["):
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
    pdf.set_font("DS", "B", 16)
    pdf.set_text_color(*pdf.BLUE_DARK)
    pdf.cell(0, 12, "СОДЕРЖАНИЕ", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    for q in questions:
        pdf.set_font("DS", "B", 10)
        pdf.set_text_color(*pdf.BLUE_MED)
        pdf.cell(10, 7, f"{q['num']:02d}.")
        pdf.set_font("DS", "", 10)
        pdf.set_text_color(*pdf.GRAY_TEXT)
        pdf.cell(0, 7, q["title"][:90], new_x="LMARGIN", new_y="NEXT")

    # Вопросы
    for q in questions:
        pdf.add_page()
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

        # Текстовая ссылка на источник (для ВСЕХ вопросов)
        if q["num"] in TEXT_REFS:
            pdf.add_text_reference(TEXT_REFS[q["num"]])

        # Иллюстрации из учебника (для определённых вопросов)
        if q["num"] in QUESTION_IMAGES:
            for img_file, caption in QUESTION_IMAGES[q["num"]]:
                img_path = os.path.join(ILL_DIR, img_file)
                pdf.add_illustration(img_path, caption)

    pdf.output(OUTPUT)
    print(f"PDF created: {OUTPUT}")
    print(f"Pages: {pdf.page_no()}")

    # Подсчёт иллюстраций
    n_images = sum(len(v) for v in QUESTION_IMAGES.values())
    n_refs = len(TEXT_REFS)
    print(f"Illustrations inserted: {n_images}")
    print(f"Text references added: {n_refs}")


if __name__ == "__main__":
    build_pdf()
