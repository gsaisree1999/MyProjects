#!/usr/bin/env python3
"""Build Sai's Artifact 4 PDF from standalone HTML content."""
from fpdf import FPDF
import re, html

SRC = "artifact-4-standalone.html"
OUT = "artifact-4.pdf"

with open(SRC, encoding="utf-8") as f:
    raw = f.read()

raw = re.sub(r"<style.*?</style>", " ", raw, flags=re.S)
raw = re.sub(r"<script.*?</script>", " ", raw, flags=re.S)

def strip(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

m = re.search(r'<div class="section" id="artifact4">(.*?)<!-- PROJECTS', raw, flags=re.S)
body = m.group(1) if m else raw

chunks = []
for mm in re.finditer(r"<(h1|h2|h3|p|li)[^>]*>(.*?)</\1>", body, flags=re.S):
    tag = mm.group(1)
    txt = strip(mm.group(2))
    if txt:
        chunks.append((tag, txt))

NAVY = (15, 35, 75)
ACCENT = (37, 99, 235)
GREY = (90, 90, 90)

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(8)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 5, "Artifact 4 - Navigating Data Challenges in ML  |  Sai Sri Gottapu", 0, 0, "C")
        self.ln(6)
        self.set_draw_color(230, 230, 240)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GREY)
        self.cell(0, 5, f"Page {self.page_no()}  |  Indiana Wesleyan University - ML Fundamentals - 2026", 0, 0, "C")

pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.set_margins(18, 16, 18)
pdf.add_page()

def clean(s):
    s = (s.replace("’", "'").replace("“", '"').replace("”", '"')
          .replace("–", "-").replace("—", "-").replace("·", "-")
          .replace("•", "-").replace("→", "->").replace("“", '"').replace("”", '"'))
    s = s.encode("latin-1", "ignore").decode("latin-1")
    return s

pdf.set_fill_color(*NAVY)
pdf.rect(0, 0, pdf.w, 46, "F")
pdf.set_xy(18, 12)
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 9, "Artifact 4", 0, 1)
pdf.set_x(18)
pdf.set_font("Helvetica", "B", 14)
pdf.cell(0, 7, "Navigating Data Challenges in Machine Learning", 0, 1)
pdf.set_x(18)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(200, 210, 230)
pdf.cell(0, 6, "Professional Portfolio - Sai Sri Gottapu", 0, 1)
pdf.set_text_color(0, 0, 0)
pdf.ln(14)

def emit(tag, txt):
    txt = clean(txt)
    pdf.set_x(pdf.l_margin)
    W = pdf.w - pdf.l_margin - pdf.r_margin
    try:
        if tag == "h1":
            pdf.set_font("Helvetica", "B", 16); pdf.set_text_color(*NAVY); pdf.ln(2)
            pdf.multi_cell(W, 8, txt); pdf.set_text_color(0,0,0)
        elif tag == "h2":
            pdf.ln(2); pdf.set_font("Helvetica", "B", 12.5); pdf.set_text_color(*ACCENT)
            pdf.multi_cell(W, 7, txt); pdf.set_text_color(0,0,0)
        elif tag == "h3":
            pdf.set_font("Helvetica", "B", 11); pdf.set_text_color(*NAVY)
            pdf.multi_cell(W, 6, txt); pdf.set_text_color(0,0,0)
        elif tag == "li":
            pdf.set_font("Helvetica", "", 10.5); pdf.set_text_color(20,20,20)
            pdf.multi_cell(W, 5.4, "- " + txt); pdf.ln(0.5)
        else:
            pdf.set_font("Helvetica", "", 10.5); pdf.set_text_color(20,20,20)
            pdf.multi_cell(W, 5.4, txt); pdf.ln(1.5)
    except Exception as e:
        print("FAIL CHUNK:", repr(txt[:120])); raise

for tag, txt in chunks:
    emit(tag, txt)

pdf.output(OUT)
print("WROTE", OUT)
