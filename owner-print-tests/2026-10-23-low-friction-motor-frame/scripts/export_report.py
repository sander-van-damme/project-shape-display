#!/usr/bin/env python3
"""Export the diagnosis and bench protocol as portable HTML/PDF deliverables.

Usage: python scripts/export_report.py OUTPUT_DIRECTORY
Requires pandoc and Python weasyprint; does not modify source documents.
"""
from pathlib import Path
import base64
import re
import shutil
import subprocess
import sys

from weasyprint import HTML

PACK = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
CSS = """
@page { size: A4; margin: 15mm 14mm 16mm;
  @bottom-left { content: 'Shape Display · 23 October 2026 · Mechanical diagnostic'; font-size: 8pt; color: #526577; }
  @bottom-right { content: counter(page); font-size: 8pt; color: #526577; }
}
body { font-family: DejaVu Sans, sans-serif; color: #243746; font-size: 9.2pt; line-height: 1.42; max-width: 1100px; margin: auto; }
h1 { font-size: 23pt; line-height: 1.13; margin: 0 0 7mm; color: #164e63; }
h2 { font-size: 14pt; margin: 7mm 0 3mm; break-after: avoid; color: #164e63; }
h3 { font-size: 11pt; break-after: avoid; }
p { margin: 2.2mm 0; orphans: 3; widows: 3; }
table { width: 100%; border-collapse: collapse; margin: 4mm 0; font-size: 8pt; line-height: 1.35; }
th { background: #e7eff2; color: #164e63; text-align: left; }
td, th { border: 0.4pt solid #b7c9d0; padding: 2mm; vertical-align: top; }
tr { break-inside: avoid; }
thead { display: table-header-group; }
li { margin: 2mm 0; }
a { color: #126278; text-decoration: none; }
code { font-family: DejaVu Sans Mono, monospace; font-size: .9em; overflow-wrap: anywhere; }
.diagram { break-before: page; break-after: page; }
.diagram img { width: 100%; }
.appendix { break-before: page; }
@media screen { body { padding: 32px; } .diagram { margin: 32px 0; } }
"""


def fragment(filename):
    text = (PACK / filename).read_text()
    # This is a portable reading edition; authoritative relative links remain
    # in the Markdown sources delivered alongside the reproduction package.
    text = re.sub(r"\[([^\]]+)\]\((?!https?://)[^)]+\)", r"\1", text)
    return subprocess.run(["pandoc", "--from=gfm", "--to=html"],
                          input=text, text=True, capture_output=True, check=True).stdout


def save(name, title, body):
    html = '<!doctype html><html lang="en"><meta charset="utf-8">'
    html += f'<title>{title}</title><style>{CSS}</style><body>{body}</body></html>'
    (OUT / (name + '.html')).write_text(html)
    HTML(string=html, base_url=str(PACK)).write_pdf(OUT / (name + '.pdf'))


svg = (PACK / 'images/contact-map.svg').read_bytes()
embedded = base64.b64encode(svg).decode()
diagram = '<div class="diagram"><h2>Dimensioned contact map</h2>'
diagram += f'<img alt="Low and high pin positions and rotor supports" src="data:image/svg+xml;base64,{embedded}"></div>'
save('mechanical-diagnosis', 'Shape Display — height-dependent friction',
     fragment('diagnosis.md') + diagram)
save('bench-test-and-results', 'Shape Display — existing-parts bench test',
     fragment('test.md') + '<div class="appendix">' + fragment('results.md') + '</div>')
save('bench-card', 'Shape Display — one test before another print', fragment('bench-card.md'))
shutil.copy2(PACK / 'images/contact-map.svg', OUT / 'contact-map.svg')
print('Exported diagnosis, bench test/results and contact map to', OUT)
