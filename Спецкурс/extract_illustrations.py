"""
Скрипт извлечения иллюстраций из PDF учебного пособия (УМП Спецкурс).
Извлекает страницы с рисунками как высококачественные изображения.
"""
import os
import fitz  # PyMuPDF

BASE = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(BASE, "Пособия и методички", "УМП_Спецкурс.pdf")
ILL_DIR = os.path.join(BASE, "Ответы", "illustrations")
os.makedirs(ILL_DIR, exist_ok=True)

# Маппинг: имя файла -> номер страницы PDF (1-indexed)
# Определяется по оглавлению УМП:
# Гл.1 стр.7-40, Гл.2 стр.41-64, Гл.3 стр.65-78, Гл.4 стр.79-101
# Гл.5 стр.102-119, Гл.6 стр.120-139

PAGES_TO_EXTRACT = {
    # Глава 1: Фундаментная плита
    "k01_fig1_1_winkler.jpg": 9,        # Рис. 1.1 Модель Винклера
    "k01_fig1_2_pasternak.jpg": 9,       # Рис. 1.2 Модель с двумя коэфф. постели
    "k02_fig1_3_section.jpg": 13,        # Рис. 1.3 Разрез по зданию
    "k02_fig1_4_plan.jpg": 14,           # Рис. 1.4 План типового этажа
    "k04_fig1_6_reinforcement.jpg": 26,  # Рис. 1.6 Армирование плиты
    "k07_fig1_7_punching.jpg": 29,       # Рис. 1.7 Пирамида продавливания
    "k07_fig1_8_punching_plan.jpg": 30,  # Рис. 1.8 Контур продавливания (план)
    "k09_fig1_9_anchorage.jpg": 38,      # Рис. 1.9-1.10 Анкеровка
    "k11_fig1_11_shear_reinf.jpg": 31,   # Поперечное армирование
    
    # Глава 2: Продавливание
    "z_fig2_1_punching_schemes.jpg": 41,  # Рис. 2.1 Схемы продавливания
    "z_fig2_2_critical_section.jpg": 42,  # Рис. 2.2 Расчётное сечение
    "z_fig2_3_contours.jpg": 43,          # Рис. 2.3 Контуры у края/угла
    "z_fig2_5_with_reinf.jpg": 48,        # Рис. 2.5 С поперечной арматурой
    
    # Глава 3: Внецентренное сжатие
    "z_fig3_1_eccentric.jpg": 65,         # Рис. 3.1 Схемы внецентр. сжатия
    "z_fig3_2_diagrams.jpg": 70,          # Рис. 3.2 Диаграмма σ-ε
    
    # Глава 4: Усиление композитами
    "z_fig4_1_frp_bend.jpg": 82,          # Рис. 4.1 Усиление изгиб. элемента
    "z_fig4_2_frp_shear.jpg": 90,         # Рис. 4.2 Усиление наклонного сечения
    "z_fig4_3_frp_column.jpg": 95,        # Рис. 4.3 Усиление сжатого элемента
    
    # Глава 5: Фибробетон
    "z_fig5_1_sfb_diagram.jpg": 102,      # Рис. 5.1 Диаграмма СФБ
    "z_fig5_2_sfb_slab.jpg": 105,         # Наращивание сжатой зоны
    "z_fig5_3_sfb_column.jpg": 109,       # Обойма
    
    # Глава 6: Каменные
    "z_fig6_1_hanging_wall.jpg": 120,     # Висячие стены
    "z_fig6_2_arches.jpg": 124,           # Расчёт висячих стен
    "z_fig6_3_masonry_frp.jpg": 129,      # Усиление каменных конструкций
}

def extract_pages():
    if not os.path.exists(PDF_PATH):
        print(f"PDF not found: {PDF_PATH}")
        return
    
    doc = fitz.open(PDF_PATH)
    total = doc.page_count
    print(f"PDF has {total} pages")
    
    extracted = 0
    for img_name, page_num in PAGES_TO_EXTRACT.items():
        if page_num < 1 or page_num > total:
            print(f"  SKIP {img_name}: page {page_num} out of range")
            continue
        
        page = doc[page_num - 1]  # 0-indexed
        # Высокое разрешение для качественных иллюстраций
        mat = fitz.Matrix(3.0, 3.0)  # 3x zoom = ~216 DPI
        pix = page.get_pixmap(matrix=mat)
        
        out_path = os.path.join(ILL_DIR, img_name)
        pix.save(out_path)
        size_kb = os.path.getsize(out_path) / 1024
        print(f"  OK {img_name} (page {page_num}, {size_kb:.0f} KB)")
        extracted += 1
    
    doc.close()
    print(f"\nExtracted {extracted}/{len(PAGES_TO_EXTRACT)} illustrations")

if __name__ == "__main__":
    extract_pages()
