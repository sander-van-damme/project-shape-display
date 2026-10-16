"""Build a printable copy of the two maintained test instructions (no physical results)."""
from pathlib import Path
import re, html, hashlib, json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
FONTS=Path('/usr/share/fonts/truetype/dejavu')
for suffix,name in [('', 'DejaVu'),('-Bold','DejaVu-Bold'),('-Oblique','DejaVu-Italic')]:
 pdfmetrics.registerFont(TTFont(name,str(FONTS/('DejaVuSans'+suffix+'.ttf'))))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu-Italic',boldItalic='DejaVu-Bold')
styles=getSampleStyleSheet()
for key in styles.byName: styles[key].fontName='DejaVu'
styles['Normal'].fontSize=9;styles['Normal'].leading=13;styles['Normal'].spaceAfter=6
styles['Heading1'].fontSize=17;styles['Heading1'].leading=21
styles['Heading2'].fontSize=12;styles['Heading2'].leading=16
styles.add(ParagraphStyle(name='Cell',fontName='DejaVu',fontSize=7,leading=10,spaceAfter=0))
WIDTH=511
sources=[];story=[]
def text(s):
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',s)
 s=html.escape(s.strip()).replace('`','')
 s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
 return s

def document(p):
 sources.append({'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 lines=p.read_text().splitlines();i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  match=re.match(r'!\[[^\]]*\]\(([^)]+)\)',line)
  if match:
   f=(p.parent/match[1]).resolve();w,h=ImageReader(str(f)).getSize();story.append(Image(str(f),width=WIDTH,height=WIDTH*h/w));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.match(r'^:?-+:?$',c) for c in cells):rows.append(cells)
    i+=1
   n=len(rows[0]);data=[[Paragraph(text(c),styles['Cell']) for c in r] for r in rows]
   table=Table(data,colWidths=[WIDTH/n]*n,repeatRows=1,hAlign='LEFT',minRowHeights=[25]*len(rows))
   table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3eef0')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#a6b8bc')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   story.extend([table,Spacer(1,9)]);continue
  if line.startswith('# '):story.append(Paragraph(text(line[2:]),styles['Heading1']));i+=1;continue
  if line.startswith('## '):story.append(Paragraph(text(line[3:]),styles['Heading2']));i+=1;continue
  para=[line];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||!\[|\d+\.)',lines[i].strip()):para.append(lines[i].strip());i+=1
  story.append(Paragraph(text(' '.join(para)),styles['Normal']))

def foot(canvas,doc):
 canvas.setFont('DejaVu',8);canvas.setFillColor(colors.HexColor('#52666b'))
 canvas.drawString(42,25,'E-298 · 16 oktober 2026 · fysieke resultaten nog onbekend')
 canvas.drawRightString(553,25,str(doc.page))
for k,name in enumerate(['fit','matrix']):
 if k:story.append(PageBreak())
 document(ROOT/f'owner-print-tests/2026-10-16-self-aligning-point-{name}/test.md')
SimpleDocTemplate(str(HERE/'print-and-assembly.pdf'),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=42,title='E-298 — printtests, montage en resultaten',author='Shape Display').build(story,onFirstPage=foot,onLaterPages=foot)
(HERE/'print-and-assembly.sources.json').write_text(json.dumps({'sources':sources},indent=2)+'\n')
print('Built print-and-assembly.pdf')
