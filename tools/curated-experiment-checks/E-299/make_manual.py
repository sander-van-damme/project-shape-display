#!/usr/bin/env python3
"""Build print instructions and a blank one-page physical results sheet."""
from pathlib import Path
import re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];FOLDER=ROOT/'owner-print-tests/2026-10-17-two-cell-supported-selector'
FONT=Path('/usr/share/fonts/truetype/open-sans')
for n,f in [('Body','OpenSans-Regular.ttf'),('Strong','OpenSans-Bold.ttf'),('Ital','OpenSans-Italic.ttf')]:pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Strong',italic='Ital',boldItalic='Strong')
styles=getSampleStyleSheet()
for n in styles.byName:styles[n].fontName='Body'
styles['BodyText'].fontSize=9;styles['BodyText'].leading=13;styles['BodyText'].spaceAfter=6
styles['Heading1'].fontSize=18;styles['Heading1'].leading=22;styles['Heading1'].textColor=colors.HexColor('#16394c')
styles['Heading2'].fontSize=12;styles['Heading2'].leading=16;styles['Heading2'].textColor=colors.HexColor('#16394c');styles['Heading2'].spaceBefore=12
styles['Heading3'].fontSize=10;styles['Heading3'].leading=14
small=ParagraphStyle('Small',parent=styles['BodyText'],fontSize=8,leading=11,spaceAfter=3)
W=178*mm

def inline(t):
 t=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',t);t=html.escape(t);t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t);t=re.sub(r'`([^`]+)`',r'<font name="Body">\1</font>',t)
 return t

def table(rows,width=W,fontsize=8):
 n=len(rows[0]); widths=[width/n]*n
 if n==3:widths=[width*.31,width*.28,width*.41]
 if n==4:widths=[width*.18,width*.22,width*.22,width*.38]
 if n==5:widths=[width*.14,width*.18,width*.21,width*.24,width*.23]
 cells=[[Paragraph(inline(c.strip()),small) for c in row] for row in rows]
 tab=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT')
 tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eff2')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#a6b7bf')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
 return tab

def parse(path):
 lines=path.read_text().splitlines();out=[];i=0
 while i<len(lines):
  l=lines[i].strip()
  if not l:i+=1;continue
  if l.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=lines[i].strip().strip('|').split('|')
    if not all(re.fullmatch(r'[\s:-]+',c) for c in cells):rows.append(cells)
    i+=1
   out.extend([table(rows),Spacer(1,6)]);continue
  if l.startswith('!['):
   target=re.search(r'\]\(([^)]+)\)',l).group(1);imgpath=path.parent/target
   if imgpath.exists():
    from PIL import Image as PImage
    wi,he=PImage.open(imgpath).size;out.append(Image(str(imgpath),width=W,height=W*he/wi));out.append(Spacer(1,6))
   i+=1;continue
  if l.startswith('#'):
   level=min(len(l)-len(l.lstrip('#')),3);out.append(Paragraph(inline(l.lstrip('#').strip()),styles['Heading'+str(level)]));i+=1;continue
  # Consecutive metadata lines remain individual, ordinary prose paragraphs join.
  para=l;i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].lstrip().startswith(('#','|','![')) and not re.match(r'^\d+\. ',lines[i].strip()) and not lines[i].strip().startswith('**'):
   para+=' '+lines[i].strip();i+=1
  out.append(Paragraph(inline(para),styles['BodyText']))
 return out

def footer(canvas,doc):
 canvas.setFont('Body',8);canvas.setFillColor(colors.HexColor('#536d7a'));canvas.drawString(16*mm,11*mm,'E-299 · 17 oktober 2026 · fysieke resultaten nog open');canvas.drawRightString(194*mm,11*mm,str(doc.page))

p=FOLDER/'montage-en-test.pdf';doc=SimpleDocTemplate(str(p),pagesize=(210*mm,297*mm),rightMargin=16*mm,leftMargin=16*mm,topMargin=14*mm,bottomMargin=19*mm,title='E-299 — montage en test',author='Shape Display')
doc.build(parse(FOLDER/'test.md'),onFirstPage=footer,onLaterPages=footer)

# One-page sheet, blank physical observations.
p=FOLDER/'resultatenformulier.pdf';doc=SimpleDocTemplate(str(p),pagesize=(210*mm,297*mm),rightMargin=16*mm,leftMargin=16*mm,topMargin=12*mm,bottomMargin=15*mm,title='E-299 — resultatenformulier')
story=[Paragraph('E-299 — mijn resultaten',styles['Heading1']),Paragraph('Datum: __________   Filamentproduct/type: ____________________<br/>3MF / profielwijzigingen: ______________________________________<br/>Werkelijke printtijd / massa: __________   Montagetijd: __________',small)]
rows=[['Controle','Goed / deels / nee / niet getest; opmerkingen'],['18 objecten compleet; schroeven recht',''],['Steunen los zonder draad-/DD-schade',''],['Beide pin/schroefparen soepel',''],['Montage / diepe sleutelbus bruikbaar',''],['Volle 3-mm slag; geen buigende rail',''],['Grote houders; volledige zetting A/B','']]
t=table(rows);t._argW=[W*.47,W*.53];story.extend([t,Spacer(1,7)])
rows=[['Beginfase / poging','Passief dicht?','Met fasezoeken dicht? / hoek / probleem'],['A: tand-op-tand; 45°; 90°','',''],['B: tand-op-tand; 45°; 90°','',''],['A+B verschillende fases','','']]
story.extend([table(rows),Spacer(1,7),Paragraph('Gedeeld sluiten: pin A vóór/na ____ / ____ mm; B ____ / ____ mm.<br/>Onderrotor/input draaide of nam DD-speling op? __________________',small)])
rows=[['Rij / A / B (0=UIT, 1=AAN)','Werkelijk gekoppeld / ongewenste buurbeweging'],['0/0/0; 0/1/0; 0/0/1; 0/1/1',''],['1/0/0',''],['1/1/0 — A vijf op/neercycli',''],['1/0/1 — B vijf op/neercycli',''],['1/1/1 — beide','']]
story.extend([table(rows),Spacer(1,6),Paragraph('Rij trekt los: ______   Kolom trekt los: ______<br/>Schade/slijtage / lastigste handeling / foto: ____________________<br/>____________________________________________________________',small),Paragraph('Leeg = onbekend. Fasezoeken is geen passieve zelfuitlijning. Stop bij hard blokkeren, verbuigen, schade of openende framevoeg.',small)])
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('PDFs written')
