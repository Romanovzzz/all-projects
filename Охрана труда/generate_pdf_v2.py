"""
Генератор PDF — Охрана труда (v3).
Основан на проверенном генераторе Металлических конструкций.
Поддержка: формулы, таблицы, заметки, ссылки. Без ASCII-арта.
"""

import os
import re
from fpdf import FPDF

# --- Пути ---
BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE, "dejavu-fonts-ttf-2.37", "ttf")
ANSWERS_DIR = os.path.join(BASE, "Ответы")
OUTPUT = os.path.join(ANSWERS_DIR, "Охрана_труда_ответы_v2.pdf")

TOTAL_QUESTIONS = 27


def clean_formula(text):
    """Превращает LaTeX-запись в читабельный текст для PDF.
    Порядок обработки критичен: \text → _{} → LaTeX-символы → \frac → cleanup
    """
    t = text.strip()

    # 1. Убираем $$...$$ и $...$, сохраняя содержимое
    t = re.sub(r'\$\$(.+?)\$\$', r'\1', t, flags=re.DOTALL)
    t = re.sub(r'\$(.+?)\$', r'\1', t)
    t = t.replace('$', '')

    # 2. \text{общ} → общ (ПЕРВЫМ, чтобы убрать вложенные {})
    for _ in range(3):
        t = re.sub(r'\\text\{([^}]*)\}', r'\1', t)

    # 3. Подстрочные _{...} и надстрочные ^{...} (ДО \frac!)
    for _ in range(3):
        t = re.sub(r'_\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\^\{([^}]*)\}', r'\1', t)

    # 4. \frac{A}{B} → (A) / (B) — теперь внутри нет вложенных {}
    for _ in range(3):
        t = re.sub(r'\\frac\{([^}]*)\}\{([^}]*)\}', r'(\1) / (\2)', t)

    # 5. LaTeX-команды → Unicode
    replacements = {
        '\\cdot': '·', '\\times': '×', '\\div': '÷',
        '\\leq': '≤', '\\geq': '≥', '\\neq': '≠',
        '\\approx': '≈', '\\,': ' ', '\\;': ' ',
        '\\quad': '  ', '\\left': '', '\\right': '',
    }
    for latex_cmd, replacement in replacements.items():
        t = t.replace(latex_cmd, replacement)

    # 6. Одиночные _X или ^X → X
    t = re.sub(r'_([A-Za-zА-Яа-яёЁ0-9])', r'\1', t)
    t = re.sub(r'\^([A-Za-zА-Яа-яёЁ0-9])', r'\1', t)

    # 7. Оставшиеся \команды → убираем \
    t = re.sub(r'\\([a-zA-Z]+)', r'\1', t)

    # 8. Фигурные скобки
    t = t.replace('{', '').replace('}', '')

    # 9. Оставшиеся _ → пробел
    t = t.replace('_', ' ')

    # 10. Множественные пробелы
    t = re.sub(r' {2,}', ' ', t)

    return t.strip()


def clean_markdown(text):
    """Убирает Markdown-разметку для текстового рендера."""
    t = text
    # Bold **...**
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
    # Italic *...*
    t = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', t)
    # Code `...`
    t = re.sub(r'`(.+?)`', r'\1', t)
    # Применяем очистку формул ко всему тексту
    t = clean_formula(t)
    return t.strip()


class ExamPDF(FPDF):
    """PDF — стиль идентичен Металлическим конструкциям."""

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

    # --- Колонтитулы (как в МК) ---
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DS", "I", 8)
        self.set_text_color(*self.BLUE_MED)
        self.cell(0, 6, "Охрана труда — ответы к зачёту", align="L")
        self.cell(0, 6, f"стр. {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DS", "I", 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8,
                  "НОМ «БЖД» (НИУ МГСУ) | Лекции Сугака Е.Б. | ТК РФ | ФЗ-125 | Приказ 776н",
                  align="C")

    # --- Титульная страница (как в МК) ---
    def add_title_page(self):
        self.add_page()
        self.ln(50)
        self.set_fill_color(*self.GREEN)
        self.rect(0, 0, 210, 8, style="F")

        self.set_font("DS", "B", 26)
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
            "НОМ «Безопасность жизнедеятельности» (НИУ МГСУ)",
            "Лекции «Охрана труда в строительстве» (Сугак Е.Б.)",
            "Трудовой кодекс РФ (Раздел X «Охрана труда»)",
            "ФЗ от 24.07.1998 № 125-ФЗ; ФЗ от 28.12.2013 № 426-ФЗ",
            "Приказ Минтруда от 29.10.2021 № 776н (СУОТ)",
        ]
        for s in sources:
            self.cell(0, 6, f"  * {s}", align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_fill_color(*self.GREEN)
        self.rect(0, 289, 210, 8, style="F")

    # --- Заголовок вопроса (как в МК: крупный номер + плашка) ---
    def add_question_header(self, number, title):
        if self.get_y() > 240:
            self.add_page()
        self.ln(4)
        y_start = self.get_y()
        block_h = 16
        w_full = self.w - self.l_margin - self.r_margin
        self.set_fill_color(*self.BLUE_DARK)
        self.rect(self.l_margin, y_start, w_full, block_h, style="F")

        # Номер
        self.set_xy(self.l_margin + 2, y_start + 1)
        self.set_font("DS", "B", 20)
        self.set_text_color(*self.WHITE)
        self.cell(16, block_h - 2, f"{number:02d}", align="C")

        # Разделительная линия
        self.set_draw_color(255, 255, 255)
        self.set_line_width(0.5)
        self.line(self.l_margin + 20, y_start + 3,
                  self.l_margin + 20, y_start + block_h - 3)

        # Название вопроса
        self.set_xy(self.l_margin + 24, y_start + 1.5)
        self.set_font("DS", "B", 10)
        self.multi_cell(w_full - 28, 6, clean_markdown(title), align="L")
        self.set_y(y_start + block_h + 4)
        self.set_text_color(*self.GRAY_TEXT)

    # --- Подзаголовок (синяя полоска слева, как в МК) ---
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
        self.cell(0, 6, clean_markdown(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)

    # --- Основной текст (как в МК: 9pt, 5mm line height) ---
    def add_body_text(self, text):
        self.set_font("DS", "", 9)
        self.set_text_color(*self.GRAY_TEXT)
        w = self.w - self.l_margin - self.r_margin
        clean = clean_markdown(text)
        if clean:
            try:
                self.multi_cell(w, 5, clean)
            except Exception:
                self.cell(w, 5, clean[:120] + "...", new_x="LMARGIN", new_y="NEXT")
            self.ln(1)

    # --- Формула (как в МК: голубой фон, жирный, отступ) ---
    def add_formula_block(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.ln(1)
        self.set_fill_color(*self.BLUE_LIGHT)
        self.set_font("DS", "B", 9)
        self.set_text_color(*self.BLUE_DARK)
        x0 = self.l_margin + 4
        self.set_x(x0)
        w_avail = self.w - self.l_margin - self.r_margin - 8
        clean = clean_formula(text)
        try:
            self.multi_cell(w_avail, 6, clean, fill=True)
        except Exception:
            self.cell(w_avail, 6, clean[:100] + "...", fill=True,
                      new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)

    # --- Маркированный список (как в МК: >, indent, 5mm) ---
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
        clean = clean_markdown(text)
        try:
            self.multi_cell(w_avail, 5, clean)
        except Exception:
            self.cell(w_avail, 5, clean[:100] + "...", new_x="LMARGIN", new_y="NEXT")

    # --- Таблица (многострочные ячейки, без обрезки) ---
    def add_table(self, headers, rows):
        if self.get_y() > 240:
            self.add_page()
        self.ln(2)

        n_cols = len(headers)
        w_full = self.w - self.l_margin - self.r_margin

        # Подготовим чистый текст
        clean_headers = [clean_markdown(h) for h in headers]
        clean_rows = []
        for row in rows:
            cr = []
            for ci in range(n_cols):
                cr.append(clean_markdown(row[ci]) if ci < len(row) else "")
            clean_rows.append(cr)

        # Вычисляем пропорции колонок по длине содержимого
        max_lens = []
        for i in range(n_cols):
            col_max = len(clean_headers[i])
            for cr in clean_rows:
                col_max = max(col_max, len(cr[i]))
            max_lens.append(max(col_max, 4))

        total = sum(max_lens)
        col_widths = [max(w_full * (ml / total), 15) for ml in max_lens]
        # Нормализуем чтобы сумма = w_full
        s = sum(col_widths)
        col_widths = [cw * w_full / s for cw in col_widths]

        line_h = 4  # высота одной строки текста в ячейке
        font_size = 7

        # --- Заголовок таблицы ---
        self.set_fill_color(*self.BLUE_DARK)
        self.set_text_color(*self.WHITE)
        self.set_font("DS", "B", font_size)

        # Вычислить высоту заголовка
        header_h = self._calc_row_height(clean_headers, col_widths, line_h, font_size, "B")
        y_row = self.get_y()
        for ci in range(n_cols):
            x = self.l_margin + sum(col_widths[:ci])
            self.rect(x, y_row, col_widths[ci], header_h, style="F")
            self.set_xy(x + 1, y_row + 0.5)
            self.set_font("DS", "B", font_size)
            self.set_text_color(*self.WHITE)
            self.multi_cell(col_widths[ci] - 2, line_h, clean_headers[ci], align="C")
        self.set_y(y_row + header_h)

        # --- Строки ---
        alt_bg = (240, 245, 252)
        white_bg = (255, 255, 255)

        for ri, cr in enumerate(clean_rows):
            self.set_font("DS", "", font_size)
            row_h = self._calc_row_height(cr, col_widths, line_h, font_size, "")

            # Новая страница при необходимости
            if self.get_y() + row_h > self.h - self.b_margin - 5:
                self.add_page()

            bg = alt_bg if ri % 2 == 0 else white_bg
            self.set_fill_color(*bg)
            y_row = self.get_y()

            for ci in range(n_cols):
                x = self.l_margin + sum(col_widths[:ci])
                # Фон ячейки
                self.rect(x, y_row, col_widths[ci], row_h, style="F")
                # Текст ячейки
                self.set_xy(x + 1, y_row + 0.5)
                self.set_font("DS", "", font_size)
                self.set_text_color(*self.GRAY_TEXT)
                self.multi_cell(col_widths[ci] - 2, line_h, cr[ci], align="L")

            self.set_y(y_row + row_h)

        # Тонкая линия под таблицей
        self.set_draw_color(*self.GRAY_LINE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y(), self.l_margin + w_full, self.get_y())
        self.ln(2)

    def _calc_row_height(self, cells, col_widths, line_h, font_size, style):
        """Рассчитывает высоту строки по самой длинной ячейке."""
        max_h = line_h + 1  # минимум одна строка
        self.set_font("DS", style, font_size)
        for ci, text in enumerate(cells):
            cw = col_widths[ci] - 2  # отступ слева и справа
            if cw < 5:
                cw = 5
            # Считаем сколько строк займёт текст
            lines = self.multi_cell(cw, line_h, text, dry_run=True, output="LINES")
            n_lines = len(lines) if lines else 1
            cell_h = n_lines * line_h + 1
            max_h = max(max_h, cell_h)
        return max_h

    # --- Заметка (жёлтый фон, как text_reference в МК) ---
    def add_note_block(self, text):
        if self.get_y() > 265:
            self.add_page()
        self.ln(2)
        self.set_fill_color(255, 248, 230)
        self.set_draw_color(200, 170, 80)
        clean = clean_markdown(text)
        w_full = self.w - self.l_margin - self.r_margin
        y0 = self.get_y()

        # Оценим высоту текста
        self.set_font("DS", "I", 8)
        lines = max(1, len(clean) // 80 + 1)
        block_h = max(8, lines * 5 + 2)

        self.rect(self.l_margin, y0, w_full, block_h, style="FD")
        self.set_text_color(100, 80, 30)
        self.set_xy(self.l_margin + 3, y0 + 1)
        self.multi_cell(w_full - 6, 5, clean)
        self.set_y(y0 + block_h + 2)
        self.set_text_color(*self.GRAY_TEXT)

    # --- Ссылки на источники ---
    def add_reference(self, text):
        self.ln(2)
        self.set_font("DS", "I", 7.5)
        self.set_text_color(100, 120, 150)
        clean = clean_markdown(text)
        w = self.w - self.l_margin - self.r_margin
        self.multi_cell(w, 4.5, clean)
        self.set_text_color(*self.GRAY_TEXT)
        self.ln(1)


# =============================================
# ПАРСЕР MARKDOWN v2
# =============================================
def parse_v2_markdown_files():
    """Парсит _v2.md файлы в структурированные данные."""
    questions = []

    for fname in sorted(os.listdir(ANSWERS_DIR)):
        if not fname.endswith("_v2.md"):
            continue
        fpath = os.path.join(ANSWERS_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

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

            # Пропускаем разделитель таблицы |---|---|
            if ls.startswith("|") and all(
                c in "-|: " for c in ls
            ):
                continue

            # Конец таблицы
            if in_table and not ls.startswith("|"):
                flush_table()

            # --- Заголовок вопроса ---
            if ls.startswith("## Вопрос "):
                if current_q:
                    flush_table()
                    if current_section:
                        current_q["sections"].append(current_section)
                    questions.append(current_q)
                after = ls[len("## Вопрос "):]
                dot = after.find(".")
                if dot == -1:
                    continue
                num_str = after[:dot].strip()
                title = after[dot + 1:].strip()
                try:
                    num = int(num_str)
                except ValueError:
                    continue
                current_q = {"num": num, "title": title, "sections": []}
                current_section = None
                continue

            if current_q is None:
                continue

            # --- Подзаголовок ---
            if ls.startswith("### ") or ls.startswith("#### "):
                flush_table()
                if current_section:
                    current_q["sections"].append(current_section)
                heading = ls.lstrip("#").strip()
                current_section = {"heading": heading, "items": []}
                continue

            # Пропуск мусора
            if ls in ("", "---") or ls.startswith("# Ответы") or ls.startswith("*Источники"):
                continue

            if current_section is None:
                current_section = {"heading": "", "items": []}

            # --- Таблица ---
            if ls.startswith("|") and "|" in ls[1:]:
                cells = [c.strip() for c in ls.split("|")]
                cells = [c for c in cells if c]  # убрать пустые от ведущего |
                if not in_table:
                    in_table = True
                    table_headers = cells
                    table_rows = []
                else:
                    table_rows.append(cells)
                continue

            # --- Формула $$ ... $$ ---
            if "$$" in ls:
                formula = ls.replace("$$", "").strip()
                if formula:
                    current_section["items"].append(("formula", formula))
                continue

            # --- Заметка  > 📖 ... или  > **Важно** ---
            if ls.startswith(">"):
                text = ls.lstrip("> ").strip()
                # Убираем эмодзи 📖
                text = text.replace("📖", "[Рис.]")
                current_section["items"].append(("note", text))
                continue

            # --- Ссылки на источники ---
            if ls.startswith("**Ссылки"):
                text = re.sub(r'^\*\*Ссылки\*\*\s*:?\s*', '', ls).strip()
                current_section["items"].append(("ref", text))
                continue

            # --- Маркированный список ---
            if ls.startswith("- ") or ls.startswith("* "):
                text = ls[2:].strip()
                current_section["items"].append(("bullet", text))
                continue

            # --- Нумерованный список ---
            m = re.match(r'^(\d+)\.\s+(.*)', ls)
            if m:
                text = f"{m.group(1)}. {m.group(2).strip()}"
                current_section["items"].append(("bullet", text))
                continue

            # --- Обычный текст ---
            if ls:
                current_section["items"].append(("text", ls))

        # Последний вопрос
        if current_q:
            flush_table()
            if current_section:
                current_q["sections"].append(current_section)
            questions.append(current_q)

    return questions


# =============================================
# СБОРКА PDF
# =============================================
def build_pdf():
    pdf = ExamPDF()
    pdf.add_title_page()

    questions = parse_v2_markdown_files()
    print(f"Найдено вопросов: {len(questions)}")

    # --- Оглавление (как в МК: шрифт 10pt) ---
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
        pdf.cell(0, 7, clean_markdown(q["title"])[:90], new_x="LMARGIN", new_y="NEXT")

    # --- Вопросы (компактно, без разрыва страницы на каждый) ---
    for q in questions:
        pdf.add_question_header(q["num"], q["title"])

        for section in q["sections"]:
            if section["heading"]:
                pdf.add_subheading(section["heading"])

            for item_type, item_data in section["items"]:
                if item_type == "formula":
                    pdf.add_formula_block(item_data)
                elif item_type == "bullet":
                    pdf.add_bullet(item_data)
                elif item_type == "text":
                    pdf.add_body_text(item_data)
                elif item_type == "table":
                    headers, rows = item_data
                    pdf.add_table(headers, rows)
                elif item_type == "note":
                    pdf.add_note_block(item_data)
                elif item_type == "ref":
                    pdf.add_reference(item_data)

    pdf.output(OUTPUT)
    print(f"PDF создан: {OUTPUT}")
    print(f"Страниц: {pdf.page_no()}")


if __name__ == "__main__":
    build_pdf()
