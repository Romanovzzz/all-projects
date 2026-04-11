"""
Скрипт для подготовки иллюстраций из учебника Кудишина для вставки в PDF.
Копирует релевантные страницы в папку Ответы/illustrations/
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE, "Пособия и методички", "kudishin_pages")
OUT_DIR = os.path.join(BASE, "Ответы", "illustrations")
os.makedirs(OUT_DIR, exist_ok=True)

# Маппинг: (вопрос, описание рисунка) -> номер файла страницы
# Смещение: файл page_N.jpg = учебник стр. N-3
ILLUSTRATIONS = {
    # Вопрос 2: Каркасы промзданий
    "q02_fig10_1_karkas.jpg": ("page_305.jpg", "Рис. 10.1 — Конструктивная схема каркаса двухпролётного промздания"),
    "q02_fig10_2_schemes.jpg": ("page_310.jpg", "Рис. 10.2 — Конструктивные схемы каркасов (план, разрезы)"),
    "q02_fig10_4_joints.jpg": ("page_311.jpg", "Рис. 10.4 — Сопряжение ригеля с колонной (жёсткое/шарнирное)"),

    # Вопрос 6: Связи по колоннам
    "q06_fig11_5_bracing.jpg": ("page_322.jpg", "Рис. 11.5 — Схемы связей между колоннами (крестовые, портальные)"),

    # Вопрос 10: Фермы
    "q10_fig13_4_trusses.jpg": ("page_374.jpg", "Рис. 13.4 — Схемы ферм покрытий (типы решёток и очертаний)"),
    "q10_fig13_5_standard.jpg": ("page_375.jpg", "Рис. 13.5 — Типовые стропильные и подстропильные фермы"),

    # Вопрос 15-16: Колонны
    "q15_fig14_4_sections.jpg": ("page_399.jpg", "Рис. 14.4 — Типы сечений сплошных колонн"),

    # Вопрос 17: Сквозные колонны
    "q17_fig14_5_lattice.jpg": ("page_400.jpg", "Рис. 14.5 — Типы сечений сквозных колонн"),

    # Вопрос 20: Базы колонн
    "q20_fig14_16_base.jpg": ("page_412.jpg", "Рис. 14.16 — Базы внецентренно сжатых колонн"),

    # Вопрос 21-22: Подкрановые конструкции
    "q21_fig15_2_crane.jpg": ("page_429.jpg", "Рис. 15.2 — Типы сечений подкрановых балок"),

    # Вопрос 24: Листовые конструкции
    "q24_fig22_reservoir.jpg": ("page_551.jpg", "Рис. 22 — Листовые конструкции (резервуары)"),

    # Вопрос 25: Большепролётные
    "q25_fig18_largespan.jpg": ("page_484.jpg", "Рис. 18 — Типы большепролётных конструкций"),
}


def copy_illustrations():
    """Копирует страницы из учебника в папку иллюстраций."""
    count = 0
    for out_name, (src_name, desc) in ILLUSTRATIONS.items():
        src = os.path.join(PAGES_DIR, src_name)
        dst = os.path.join(OUT_DIR, out_name)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  OK {out_name}: {desc}")
            count += 1
        else:
            print(f"  MISS: {src_name}")
    print(f"\nСкопировано {count}/{len(ILLUSTRATIONS)} иллюстраций в {OUT_DIR}")


if __name__ == "__main__":
    copy_illustrations()
