#!/usr/bin/env python3
"""Export the reviewed text package to a portable PDF; does not fabricate evidence.

Requires reportlab. Run from any directory with --output path/to/report.pdf.
The repository Markdown and calculation sources remain authoritative.
"""
import argparse
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
STYLES = getSampleStyleSheet()
STYLES.add(ParagraphStyle('BodyEngineering', fontName='Helvetica', fontSize=9,
                         leading=12.3, spaceAfter=6, alignment=TA_LEFT))
STYLES.add(ParagraphStyle('CellEngineering', fontName='Helvetica', fontSize=7.4,
                         leading=9.5, spaceAfter=0))
STYLES.add(ParagraphStyle('MonoEngineering', fontName='Courier', fontSize=7,
                         leading=9, spaceAfter=6))
STYLES['Title'].fontSize = 23
STYLES['Title'].leading = 28
STYLES['Heading1'].fontSize = 17
STYLES['Heading1'].leading = 21
STYLES['Heading2'].fontSize = 12
STYLES['Heading2'].leading = 15


def inline(text):
    # Core Helvetica lacks some Unicode engineering glyphs. Preserve their
    # unambiguous text equivalents in the PDF; source retains original symbols.
    for old, new in [('→', ' -> '), ('²', '^2'), ('³', '^3'), ('×', ' x '),
                     ('−', '-'), ('≤', '<='), ('≥', '>='), ('θ', 'theta'),
                     ('√', 'sqrt'), ('≈', '~'), ('°', ' deg'), ('Ø', 'diameter '),
                     ('↔', ' <-> '), ('✅', ''), ('✗', 'FAIL')]:
        text = text.replace(old, new)
    text = html.escape(text)
    # Preserve readable source names rather than creating broken relative PDF URLs.
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m:
        ('<link href="'+m[2]+'" color="#175b85">'+m[1]+'</link>')
        if m[2].startswith('https://') else m[1]+' ('+m[2]+')', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', text)
    return text


def paragraph(text, style='BodyEngineering'):
    return Paragraph(inline(text), STYLES[style])


def parse(path):
    source = path.read_text()
    source = re.sub(r'^---\n.*?\n---\n', '', source, count=1, flags=re.S)
    lines = source.splitlines(); flow = []; i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1; continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append([paragraph(c, 'CellEngineering') for c in cells])
                i += 1
            columns = len(rows[0])
            weights = [1.0]*columns
            if columns == 3: weights = [1.1, 1.0, 1.7]
            if columns == 4: weights = [1.1, 1.5, 1.6, .9]
            if columns >= 5: weights[0] = 1.7
            widths = [174*mm*w/sum(weights) for w in weights]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e0eaf0')),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), .3, colors.HexColor('#aebac2')),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
            flow += [table, Spacer(1, 7)]
            continue
        if line.startswith('```'):
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                flow.append(paragraph(lines[i], 'MonoEngineering')); i += 1
            i += 1; continue
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            depth = min(len(heading[1]), 3)
            flow.append(paragraph(heading[2], 'Heading'+str(depth)))
            i += 1; continue
        text = line
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|\d+\. |[-*] )', lines[i].strip()):
            text += ' '+lines[i].strip(); i += 1
        if re.match(r'^[-*] ', text): text = '• '+text[2:]
        flow.append(paragraph(text))
    return flow


def footer(canvas, document):
    canvas.saveState(); canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#536572'))
    canvas.drawString(18*mm, 12*mm, 'Shape Display / DES-008 / 15 October 2026 / No physical validation claimed')
    canvas.drawRightString(192*mm, 12*mm, str(document.page))
    canvas.restoreState()


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--append-pdf', type=Path, action='append', default=[],
                        help='Append native figure/drawing pages without rasterizing them; requires PyMuPDF')
    args = parser.parse_args(); args.output.parent.mkdir(parents=True, exist_ok=True)
    docs = [ROOT/(ROOT.name+'.md'), ROOT/'construction.md', ROOT/'timing-evidence.md',
            ROOT/'cost-and-manufacture.md', ROOT/'research.md', ROOT/'verification.md']
    optional = ['resident-integration.md', 'resident-manufacture.md', 'guide-escape.md', 'bank-drive.md', 'review/revised-system.md', 'review/integration-final-review.md', 'review/final-disposition.md']
    docs += [ROOT/name for name in optional if (ROOT/name).exists()]
    story = [paragraph('Shape Display: DES-008', 'Title'),
             paragraph('Positive latches, resident mechanical memory and shared bank lifts', 'Heading1'),
             paragraph('Engineering decision package · 15 October 2026'),
             paragraph('Recommendation: build the small manual support-transfer article. Do not build a full display from this package. The conditional resident mechanism still lacks qualified seating, bank integration, affordability and playable walls; the separate memory print is deferred.'),
             paragraph('Source branch: codex/des008-multiplexed-lift. Baseline: main b23ed12. The source archive contains reproducible calculations, parametric CAD, independent reviews and ready-to-slice test files. No purchase, physical test or merge into main has occurred.'),
             Spacer(1, 10), paragraph('Included documents', 'Heading2')]
    for path in docs: story.append(paragraph(path.name))
    for path in docs:
        story += [PageBreak()] + parse(path)
    document = SimpleDocTemplate(str(args.output), pagesize=(210*mm,297*mm),
        leftMargin=18*mm,rightMargin=18*mm,topMargin=17*mm,bottomMargin=20*mm,
        title='Shape Display DES-008 engineering decision package',author='Shape Display engineering investigation')
    document.build(story,onFirstPage=footer,onLaterPages=footer)
    if args.append_pdf:
        import fitz
        merged = fitz.open(args.output)
        for path in args.append_pdf:
            with fitz.open(path) as figure: merged.insert_pdf(figure)
        temporary = args.output.with_suffix('.assembled.pdf')
        merged.save(temporary); merged.close(); temporary.replace(args.output)
    print(args.output)


if __name__ == '__main__': main()
