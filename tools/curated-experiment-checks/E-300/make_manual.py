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
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];FOLDER=ROOT/'owner-print-tests/2026-10-17-cone-friction-selector'
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
 t=t.replace('→',' naar ')
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
 canvas.setFont('Body',8);canvas.setFillColor(colors.HexColor('#536d7a'));canvas.drawString(16*mm,11*mm,'E-300 · 17 oktober 2026 · fysieke resultaten nog open');canvas.drawRightString(194*mm,11*mm,str(doc.page))


# Full reference is supplied separately; this is a fixed two-page quick manual.
def P(t): return Paragraph(inline(t),styles['BodyText'])
imagepath=HERE/'drawings/assembly.png'
story=[Paragraph('E-300 — montage en één fysieke proef',styles['Heading1']),P('Twee pinnen op 5,08 mm; gewone PLA-conussen. Eerst selecteren en sluiten bij stilstaande inputs, pas daarna draaien. Geen fasezoeken. Er zijn nog geen fysieke resultaten.')]
if imagepath.exists(): story.append(Image(str(imagepath),width=W,height=73*mm))
story.append(Paragraph('Print en inleggen',styles['Heading2']))
for t in [
'1. Open cone-friction-selector.3mf als X1 Carbon/0,4-mm/PLA-project. Behoud alle oriëntaties en de vaste plaatsing. Geen automatische oriëntatie/plaatsing. 17 printobjecten leveren 18 mechanische delen; het schroefsteunframe is afval. Slicerraming: 3 u 47 min 48 s / 10,48 g PLA.',
'2. Laat afkoelen. Knip de schroefsteunverbindingen van boven naar beneden aan de staanderkant los; steun de schroef vlak erbij. Knip de voet bij de 1-mm-overgang onder de DD-staart los. Geen draad schuren/uitboren. Stop bij schade of een achtergebleven steunbult.',
'3. Pas beide schroef/pinparen en alle DD-schuifverbindingen buiten het frame. Vang iedere flens tussen de twee hoge selectorbladen: smalle U aan de aszijde, brede U aan de hals. Niet spreiden.',
'4. Leg de achterste framehelft plat, deelvlak omhoog. Leg de twee inputassen onderin; dikke bus omlaag. Mannelijke conussen op de inputs, vlakke top omhoog. Eén gedeelde rij vangt beide flenzen; de centrale paddle gaat naar achteren.',
'5. Monteer elke pin circa 5,25 mm boven het begin van de schroefdraad. Een vrouwelijke cup gaat op de neergaande schroefstaart, opening omlaag; vang haar flens in een kolomselector. Leg de complete paren in: schroefkraag op haar steun en pin in beide geleidingen.',
'6. Sluit met de voorste framehelft; tape alleen de buitenvoegen. A=links en B=rechts vanaf de twee kolomtabs. Sleutel van onderen circa 3 mm in de inputbus. Pinnen circa 4 mm boven het frame; blijf tijdens de proef tussen 2,5 en 5,5 mm.'
]:story.append(P(t))
story.extend([Paragraph('Bediening',styles['Heading2']),P('Kolom UIT: omhoog, houder onder de tab. Kolom AAN: omlaag, houder boven de tab. Houder moet zonder wrikken passen. Rij UIT: actief omlaag trekken. Rij AAN: centraal op de paddle omhoog drukken en die druk vasthouden. Geen rijhouder. De rij mag licht links/rechts kantelen; nooit één uiteinde apart helpen. Tot eerste belast contact is de nominale rij-handbeweging circa 3,52 mm; een vensterrand is geen krachtinstelling.')])
story.append(PageBreak())
story.extend([Paragraph('Sluiten, grip en loskomen',styles['Heading1']),P('Verder nodig: tape, pen/liniaal en een bestaand fijn kniptangetje. Een aanwezige keukenweegschaal/schuifmaat kan meetgegevens opleveren. Stop bij klemmen, zichtbaar buigen, frameopening, beschadiging, buurcontact of te zware druk. Geen motor, boormachine of tang op bewegende delen.')])
for t in [
'1. Zet beide kolommen AAN. Houd de inputs stil. Kies vooraf verschillende outputhoeken, bijvoorbeeld A circa 0° en B 70°. Druk de gedeelde rij centraal omhoog. Beide cups moeten contact maken zonder te draaien of individueel te helpen. Noteer pinhoogten vóór/na en de werkelijke sluitstand.',
'2. Houd dezelfde rijdruk aan en draai A en daarna B elk hoogstens 1/4 omwenteling heen en terug. Beide outputs moeten volgen; theoretische pinverplaatsing is 0,75 mm per kwartslag. Herhaal sluiten met twee andere willekeurige hoekparen. Iedere hulp apart noteren.',
'3. Begin licht, verhoog alleen comfortabel en vergelijk grip van beide pinnen in beide richtingen. Voor herkenbare slip mag je het zichtbare bovenrotorlichaam héél licht met een zacht vingercontact afremmen. Geen draad/contactvlak aanraken of op de pin drukken. Stop zodra slip zichtbaar is. DD-speling of sleutelverlies is geen conusslip. Onveilig/onduidelijk? Slipgrens onbekend laten.',
'4. Controleer lichte rijhelling zonder klemmen. Alleen na nominale grip: eventueel één gemeten dun laagje tape op het statische bovencontactvlak van één kolomhouder, ver van bewegende delen. Zonder wrikken opnieuw monteren en één gezamenlijke gripproef doen. Noteer shimdikte en nieuwe kolompositie; daarna verwijderen.',
'5. Controleer de acht standen hieronder. Stop beide inputs vóór elke wissel; rij terug, kolommen instellen/borgen, rij stilstaand sluiten. Draai beide inputs afzonderlijk. Alleen gekozen pinnen mogen bewegen. Alleen A en alleen B elk drie korte op/neercycli.',
'6. Ontlast torsie. Trek alleen de rij terug en controleer dat de input de output niet meer meeneemt. Sluit opnieuw en test terugtrekken via alleen de kolom. Herhaal na de andere draairichting. Inspecteer uitsparingen, cups, flenzen, draad en sleutelbus. Stop hier.'
]:story.append(P(t))
story.append(table([['Rij / A / B (0=UIT, 1=AAN)','Verwacht gekoppeld'],['0/0/0; 0/1/0; 0/0/1; 0/1/1; 1/0/0','geen'],['1/1/0','A'],['1/0/1','B'],['1/1/1','A en B']]))
story.extend([Spacer(1,7),P('Optioneel druk meten: steun alleen de centrale paddle via een stabiel bestaand blokje op de keukenweegschaal. Houd het frame vrij en druk het langzaam omlaag; frame/inputs mogen schaal of blok niet raken. Trek de onbelaste lezing af: F≈0,00981×extra gram N. Probeer hoogstens circa 50/100/200/300 gram extra (0,5/1/2/3 N); stop eerder bij buigen/klemmen. Noteer laagste druk voor beide pinnen en druk bij slip. Ongeldige krachtweg = onbekende kracht.'),P('Dit is één tweepins-handproef. Een vrije kantelrij vereffent geen willekeurige hoogtefouten van veel koppelingen. Gevoelde druk is geen meting; zonder koppelmeter blijft slipkoppel onbekend. Volledige instructies: test.md. Vul het aparte resultatenformulier in.')])
doc=SimpleDocTemplate(str(FOLDER/'montage-en-test.pdf'),pagesize=(210*mm,297*mm),rightMargin=16*mm,leftMargin=16*mm,topMargin=13*mm,bottomMargin=18*mm,title='E-300 — montage en test',author='Shape Display')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
# Standalone blank results, compact one-page sheet.
story=[Paragraph('E-300 — mijn resultaten',styles['Heading1']),Paragraph('Datum: __________  PLA-product/type: __________________________<br/>3MF / profiel- of oriëntatiewijzigingen: __________________________<br/>Werkelijke tijd/massa: __________  Montage-/opruimtijd: __________',small)]
rows=[['Controle','Goed / deels / nee / onbekend; opmerking'],['Compleet; steunen los zonder draad-/DD-schade',''],['Beide schroefparen soepel; cups gaaf',''],['Montage / sleutel / houders bruikbaar',''],['Uitsparingen recht; vrije slag / kanteling',''],['Beide contacten bij dezelfde centrale druk','']]
story.extend([table(rows),Spacer(1,6)])
story.append(table([['Beginhoeken A/B','Dicht zonder draaien/hulp?','Pin A/B vóór→na; beide heen/terug?'],['','',''],['','',''],['','','']]))
story.extend([Spacer(1,6),Paragraph('Drukmeting / uitgangslezing / resolutie: _________________________<br/>Zonder meting: gevoelde druk __________________________________',small)])
story.append(table([['Extra gram / rijdruk N (of gevoeld)','A op/neer','B op/neer','Slip waar / richting / DD of conus?'],['','','',''],['','','',''],['','','',''],['','','','']]))
story.extend([Spacer(1,6),Paragraph('Laagste druk voor beide: ______  Slipkoppel gemeten? ______ (anders onbekend)<br/>Shim / kolompositie / rijhelling / beide grip: _____________________',small)])
story.append(table([['Rij/A/B','Werkelijk bewogen / ongewenste buurbeweging'],['0/0/0; 0/1/0; 0/0/1; 0/1/1; 1/0/0',''],['1/1/0 — A 3 cycli',''],['1/0/1 — B 3 cycli',''],['1/1/1 — beide','']]))
story.extend([Spacer(1,6),Paragraph('Rij trekt los na beide richtingen? ______  Kolom? ______<br/>Buiging / plakken / mond- of bodemcontact / slijtage: ______________<br/>Lastigste handeling / foto: ___________________________________<br/>Leeg = onbekend. Geen fasezoeken of individuele hulp verbergen.',small)])
doc=SimpleDocTemplate(str(FOLDER/'resultatenformulier.pdf'),pagesize=(210*mm,297*mm),rightMargin=16*mm,leftMargin=16*mm,topMargin=12*mm,bottomMargin=16*mm,title='E-300 — resultatenformulier')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
# Technical argument; all claims retain their analytical/physical evidence level.
doc=SimpleDocTemplate(str(HERE/'ontwerp-en-onderbouwing.pdf'),pagesize=(210*mm,297*mm),rightMargin=16*mm,leftMargin=16*mm,topMargin=14*mm,bottomMargin=18*mm,title='E-300 — ontwerp en onderbouwing')
doc.build(parse(HERE/'design-report.md'),onFirstPage=footer,onLaterPages=footer)
print('PDFs built')
