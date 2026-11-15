from pathlib import Path
from html import escape
P=Path(__file__).resolve().parents[1]/'images/plan.svg'
a=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800" viewBox="0 0 1200 800"><rect width="1200" height="800" fill="white"/><style>text{font-family:Arial,sans-serif;fill:#20333f} .small{font-size:15px}</style>']
def t(x,y,s,n=17):a.append(f'<text x="{x}" y="{y}" font-size="{n}">{escape(s)}</text>')
def xy(x,y):return 70+(x+55)*4,105+(y+75)*4
def rect(x,y,w,h,c,opacity=1):
 X,Y=xy(x,y);a.append(f'<rect x="{X}" y="{Y}" width="{w*4}" height="{h*4}" fill="{c}" fill-opacity="{opacity}" stroke="{c}"/>')
def circle(x,y,r,c):
 X,Y=xy(x,y);a.append(f'<circle cx="{X}" cy="{Y}" r="{r*4}" fill="{c}" stroke="white" stroke-width="1"/>')
t(38,40,'DES-010 — bovenaanzicht en montagevolgorde',28);t(38,70,'Projectie van verschillende hoogten: overlap op papier betekent geen botsing. Geen fysiek werkingsbewijs.',17)
rect(-33,-60,71,81,'#b7c3c9');rect(.08,20,10,9,'#b7c3c9')
for y in [-70,35]:rect(-36,y,78,8,'#738691')
for x in [-28,33]:rect(x-1.5,-72,3,120,'#536572')
rect(-27.46,-57,60,45,'#e8ac53',.85)
rect(-18.61,-56.15,42.3,42.3,'#a7692b',.25)
rect(-48,-9,101,23.08,'#578aa2',.25)
for x in [-42,47]:
 for y in [-5,10.08]:rect(x-6,y-6,12,12,'#578aa2',.55)
for x in [0,5.08]:
 for y in [0,5.08]:circle(x,y,2.3,'#285775')
for x,y in [(0,18),(5.08,25)]:circle(x,y,2.5,'#a6608e')
circle(2.54,-35,5.8,'#c37a2b')
for x in [0,5.08]:circle(x,0,2.8,'#c37a2b')
X,Y=xy(2.54,-35);U,V=xy(0,0);W,Z=xy(5.08,0);a.append(f'<path d="M {X-23} {Y} L {U-11} {V} L {W+11} {Z} L {X+23} {Y}" fill="none" stroke="#845123" stroke-width="2"/>')
t(74,641,'x → ; y ↓ langs rail. Alle geometrie in mm; tekening circa 4 px/mm.',15)
t(74,668,'Oranje = losse motorplaat/riem; blauw = vast raster en voeten.',15)
t(74,693,'Grijs = bank/rail; paars = twee versprongen handjacks.',15)
a.append('<path d="M580 112H1155V713H580Z" fill="#f2f6f8"/>')
for x,y,s,n in [(605,145,'Eén geïntegreerde proef',24),(605,180,'2×2 pinnen op 5,08; buitenmaat 4,50.',18),(605,210,'Twee bankuitgangen bedienen één rij tegelijk.',18),(605,240,'Bank schuift 5,08 naar de tweede rij.',18),(605,290,'Montage in lagen',24),(605,325,'1. Zet voeten en railblokken op 45-mm verhogingen.',17),(605,355,'2. Monteer bank en los bedienbare riemrotoren.',17),(605,385,'3. Schroef de vlak geprinte motorplaat op de bank.',17),(605,415,'4. Motor onder plaat met 2-mm metalen spacers.',17),(605,445,'5. Vast raster: onderstrips, schroeven, keeper.',17),(605,475,'6. Korte guides op z50 en66; pinnen op z40,2.',17),(605,505,'7. Jacks op (0,18) en (5,08,25); veerkracht meten.',17),(605,555,'Verplaatsen',24),(605,590,'Motor uit → beide 2,4 mm park → vrije tips zien',17),(605,620,'→ indexpin uit → 5,08 schuiven → pin terug.',17),(605,665,'Exacte maten/onderdelen: assembly.md.',17)]:t(x,y,s,n)
a.append('</svg>');P.write_text('\n'.join(a))
