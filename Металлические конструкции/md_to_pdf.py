"""
Конвертер Markdown -> PDF через pandoc + xelatex.
Поддерживает LaTeX-формулы, кириллицу и вставку иллюстраций.
"""
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ANSWERS_DIR = os.path.join(BASE, "\u041e\u0442\u0432\u0435\u0442\u044b")
ILL_DIR = os.path.join(ANSWERS_DIR, "illustrations")
OUTPUT_PDF = os.path.join(ANSWERS_DIR, "\u041c\u0435\u0442\u0430\u043b\u043b\u0438\u0447\u0435\u0441\u043a\u0438\u0435_\u043a\u043e\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u0438_\u043e\u0442\u0432\u0435\u0442\u044b.pdf")

# LaTeX header template for pandoc
HEADER = r"""---
title: "Металлические конструкции"
subtitle: "Ответы на экзаменационные вопросы (29 вопросов)"
author: "На основе учебника Кудишина Ю.И. (13-е изд.)"
date: "2026"
lang: ru
documentclass: article
geometry: "margin=2cm"
fontsize: 11pt
mainfont: "DejaVu Sans"
monofont: "DejaVu Sans Mono"
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhead[L]{\small\textit{Металлические конструкции — ответы на экзамен}}
  - \fancyhead[R]{\small\thepage}
  - \fancyfoot[C]{\small\textit{Источники: Кудишин Ю.И.; СП 16.13330.2017; СП 20.13330.2016}}
  - \usepackage{tcolorbox}
  - \usepackage{graphicx}
---

"""


def get_md_files():
    """Возвращает отсортированный список MD-файлов с ответами."""
    files = []
    for fn in sorted(os.listdir(ANSWERS_DIR)):
        if fn.startswith("answers_") and fn.endswith(".md"):
            files.append(os.path.join(ANSWERS_DIR, fn))
    return files


def combine_markdown():
    """Объединяет все MD-файлы в один с YAML-заголовком."""
    combined = HEADER
    for fpath in get_md_files():
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove per-file headers (# Ответы на ...) since we have a title
        lines = content.split("\n")
        filtered = []
        skip_first_heading = True
        for line in lines:
            if skip_first_heading and line.startswith("# "):
                skip_first_heading = False
                continue
            # Remove source lines at the end
            if line.strip().startswith("*\u0418\u0441\u0442\u043e\u0447\u043d\u0438\u043a\u0438"):
                continue
            filtered.append(line)
        combined += "\n".join(filtered) + "\n\n\\newpage\n\n"
    
    out_path = os.path.join(ANSWERS_DIR, "_combined.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(combined)
    return out_path


def build_pdf(md_path):
    """Конвертирует MD -> PDF через pandoc + xelatex."""
    cmd = [
        "pandoc",
        md_path,
        "-o", OUTPUT_PDF,
        "--pdf-engine=xelatex",
        "--toc",
        "--toc-depth=2",
        "--number-sections",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "toccolor=blue",
        "--highlight-style=tango",
    ]
    
    print(f"Running: {' '.join(cmd[:5])}...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ANSWERS_DIR)
    
    if result.returncode == 0:
        size_mb = os.path.getsize(OUTPUT_PDF) / 1024 / 1024
        print(f"PDF created: {OUTPUT_PDF}")
        print(f"Size: {size_mb:.1f} MB")
    else:
        print(f"Error (exit {result.returncode}):")
        print(result.stderr[:2000])
    
    return result.returncode


if __name__ == "__main__":
    print("1. Combining Markdown files...")
    md_path = combine_markdown()
    print(f"   Combined: {md_path}")
    
    print("2. Building PDF via pandoc + xelatex...")
    rc = build_pdf(md_path)
    
    if rc != 0:
        print("\nTrying without --toc (fallback)...")
        # Simpler command in case of TOC issues
        cmd = [
            "pandoc", md_path, "-o", OUTPUT_PDF,
            "--pdf-engine=xelatex",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=ANSWERS_DIR)
        if result.returncode == 0:
            print(f"PDF created (fallback): {OUTPUT_PDF}")
        else:
            print(f"Fallback also failed: {result.stderr[:1000]}")
    
    sys.exit(rc)
