#!/usr/bin/env python3
"""Turn a Markdown file into a clean, branded PDF (and HTML) for selling.

Reusable for every ebook/guide you ship. Converts a practical subset of Markdown
(headings, bold, lists, blockquotes, rules, paragraphs) to styled HTML, then uses
LibreOffice (soffice) to render a PDF.

    python3 md_to_pdf.py input.md [--out-dir DIR] [--title "Cover Title"]

Requires: libreoffice/soffice on PATH (already present in this environment).
No network, no Python deps.
"""
import argparse
import html
import os
import re
import subprocess
import sys

CSS = """
@page { size: A4; margin: 22mm 20mm; }
body { font: 12pt/1.55 Georgia, 'Times New Roman', serif; color: #1a1a1a; }
h1 { font-family: Helvetica, Arial, sans-serif; font-size: 26pt; color: #0b3d91;
     margin: 0 0 6pt; line-height: 1.15; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 17pt; color: #0b3d91;
     margin: 20pt 0 6pt; border-bottom: 1px solid #ccd6f0; padding-bottom: 3pt; }
h3 { font-family: Helvetica, Arial, sans-serif; font-size: 13pt; color: #333;
     margin: 14pt 0 4pt; }
h4 { font-family: Helvetica, Arial, sans-serif; font-size: 12pt; color: #555;
     margin: 12pt 0 4pt; }
p { margin: 0 0 9pt; }
ul, ol { margin: 0 0 9pt 18pt; padding: 0; }
li { margin: 0 0 4pt; }
blockquote { margin: 10pt 0; padding: 8pt 12pt; background: #f1f5ff;
             border-left: 4px solid #4f8cff; color: #243; }
hr { border: none; border-top: 1px solid #ddd; margin: 16pt 0; }
strong { color: #111; }
a { color: #0b3d91; }
"""


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    # markdown links [t](u)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    return text


def md_to_html_body(md):
    out, i = [], 0
    lines = md.split("\n")
    list_type = None  # 'ul' or 'ol'

    def close_list():
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    para = []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para).strip()) + "</p>")
            para.clear()

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush_para(); close_list(); continue
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_para(); close_list()
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); continue
        if re.match(r"^---+\s*$", line):
            flush_para(); close_list(); out.append("<hr/>"); continue
        if line.lstrip().startswith(">"):
            flush_para(); close_list()
            out.append("<blockquote>" +
                       inline(line.lstrip()[1:].strip()) + "</blockquote>")
            continue
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            flush_para()
            if list_type != "ul":
                close_list(); out.append("<ul>"); list_type = "ul"
            out.append("<li>" + inline(m.group(1)) + "</li>"); continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            flush_para()
            if list_type != "ol":
                close_list(); out.append("<ol>"); list_type = "ol"
            out.append("<li>" + inline(m.group(1)) + "</li>"); continue
        para.append(line)
    flush_para(); close_list()
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()

    if not os.path.exists(a.input):
        sys.exit(f"no such file: {a.input}")
    md = open(a.input, encoding="utf-8").read()
    out_dir = a.out_dir or os.path.dirname(os.path.abspath(a.input))
    base = os.path.splitext(os.path.basename(a.input))[0]
    html_path = os.path.join(out_dir, base + ".html")

    title = a.title or base.replace("-", " ").title()
    body = md_to_html_body(md)
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<title>{html.escape(title)}</title><style>{CSS}</style></head>"
           f"<body>{body}</body></html>")
    open(html_path, "w", encoding="utf-8").write(doc)
    print(f"wrote {html_path}")

    soffice = "soffice"
    try:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf",
             "--outdir", out_dir, html_path],
            check=True, capture_output=True, timeout=180)
        pdf_path = os.path.join(out_dir, base + ".pdf")
        if os.path.exists(pdf_path):
            kb = os.path.getsize(pdf_path) / 1024
            print(f"wrote {pdf_path} ({kb:.0f} KB)")
        else:
            print("soffice ran but PDF not found; open the HTML and Print->PDF.")
    except Exception as e:  # noqa: BLE001
        print(f"PDF step skipped ({e}). Open the HTML and use Print -> Save as PDF.")


if __name__ == "__main__":
    main()
