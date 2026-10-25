from pathlib import Path
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[4]
R=ROOT/'tools/curated-experiment-checks/E-304/images';P=ROOT/'owner-print-tests/2026-10-25-reversible-magnet-force/images'
class SVG:
 def __init__(self,w,h,title):
  self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#34495e"/></marker></defs><rect width="100%" height="100%" fill="#fff"/><style>text{{font-family:Arial,sans-serif;fill:#1c2c3c}}.title{{font-size:24px;font-weight:bold}}.sub{{font-size:15px}}.label{{font-size:16px}}.small{{font-size:13px}}</style>'];self.text(28,35,title,'title')
 def text(self,x,y,t,cls='label'):self.s.append(f'<text x="{x}" y="{y}" class="{cls}">{escape(t)}</text>')
 def rect(self,x,y,w,h,c,stroke='#34495e'):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" stroke="{stroke}"/>')
 def line(self,x,y,X,Y,arrow=False,dash=False):self.s.append(f'<path d="M{x} {y}L{X} {Y}" fill="none" stroke="#34495e" stroke-width="1.4"'+(' marker-end="url(#a)"'if arrow else'')+(' stroke-dasharray="5 4"'if dash else'')+'/>')
 def poly(self,pts,c):self.s.append('<polygon points="'+' '.join(f'{x},{y}'for x,y in pts)+f'" fill="{c}" stroke="#34495e"/>')
 def save(self,p):p.write_text('\n'.join(self.s+['</svg>']))
s=SVG(1100,820,'E-304 · selected clutch principle / axial section')
s.text(28,62,'Dimensioned concept, mm · not a fabrication release · terrain support independent of actuator','sub')
x=270;y=lambda z:690-z*12
# frame lands, washers (both sides)
for z,h,inner,outer in [(6,1.7,5.15,7),(10.3,1.7,5.15,7),(17,1.5,1.7,7),(20.6,1.5,1.7,7),(2.5,.3,1.9,7),(32,2,2.4,7),(42,2,2.4,7)]:
 for sign in [-1,1]:s.rect(x+(inner if sign==1 else -outer)*12,y(z+h),(outer-inner)*12,h*12,'#e0e5e9')
for z,h,inner,outer in [(7.7,.3,5.1,6.5),(10,.3,5.1,6.5),(18.5,.5,1.7,3.25),(20.1,.5,1.7,3.25)]:
 for sign in [-1,1]:s.rect(x+(inner if sign==1 else -outer)*12,y(z+h),(outer-inner)*12,h*12,'#8294a3')
s.rect(x-1.6*12,y(38),3.2*12,(38-3.2)*12,'#7fb3d5');s.rect(x-36,y(20),72,12,'#7fb3d5')
# pin: hollow envelope
for sign in [-1,1]:s.rect(x+(1.78 if sign==1 else -2.2)*12,y(46),.42*12,18*12,'#c6d9ee')
# input sectional polygons
for sign in [-1,1]:
 pts=[(5.4,3.8),(5.4,6),(5,6),(5,8),(6.5,8),(6.5,10),(5,10),(5,12),(3,12),(3,5.43),(4,5.43),(5.147,3.8)]
 s.poly([(x+sign*r*12,y(z))for r,z in pts],'#90cfb2')
# carrier profile with DD bore
for sign in [-1,1]:
 pts=[(1.8,1.6),(1.8,3.4),(5,3.4),(5,4),(4,5.428),(1.9,5.428),(1.9,9),(1.7,9),(1.7,2.4),(0,2.4),(0,1.6)]
 s.poly([(x+sign*r*12,y(z))for r,z in pts],'#f5d37b')
s.rect(x-18,y(1.6),36,12,'#e88484');s.rect(x-18,y(.6),36,12,'#6d9dd6');s.text(x-5,y(1.0),'N','small');s.text(x-5,y(0),'S','small')
# coil and bobbin
for sign in [-1,1]:
 s.rect(x+(2.4 if sign==1 else -3.66)*12,y(0),1.26*12,3.6*12,'#d99b52')
 s.rect(x+(2 if sign==1 else -2.4)*12,y(.8),.4*12,4.4*12,'#b8bec3')
 s.rect(x+(2 if sign==1 else -4.2)*12,y(-3.6),2.2*12,.8*12,'#b8bec3')
 s.rect(x+(2.45 if sign==1 else -4.2)*12,y(.8),1.75*12,.8*12,'#b8bec3')
s.line(x,100,x,760,False,True)
labels=[(42,'4.4-mm pin / square guides react torque and lateral load'),(34,'Ø3.2 screw / 3-mm lead (thread envelope only)'),(20,'Resident screw collar + 2 thrust washers → fixed frame'),(17,'Separate screw journal lands; no magnetic terrain support'),(12,'Input journal lands + 2 independent thrust washers'),(9,'Shared spur input: 24T, module 0.5, PD12 / OD13 envelope'),(5.43,'Continuous cone: radii 4–5, α35°, height 1.428'),(3.2,'One sliding double-D carrier; output AF2.7 / nominal Ø3.2'),(1,'Ø3 ×2 N48 magnet, N up; adhesive + retaining film'),(-2,'140-turn stationary air coil / OD7.32, ID4.8, length3.6')]
for z,t in labels:
 yy=y(z);s.line(x+85,yy,440,yy);s.text(455,yy+5,t,'small')
s.text(30,110,'Terrain load → frame','small');s.text(28,470,'Corner frame webs','small');s.text(28,488,'out of section plane','small');s.line(180,150,180,400,True)
s.line(128,y(3),128,y(5),True);s.text(30,635,'Fmag ↑ ON','small')
s.text(28,770,'Housing 14 ×14 envelope · carrier stroke 0.60 · g OFF −1.0 / ON −0.4 relative to winding top','sub')
s.text(28,796,'OFF gravity return is conditional on unloaded free sliding; cut shared drive on loss of selector power.','sub')
s.save(R/'concept-section.svg')
s=SVG(1000,800,'E-304 · exploded functional assembly')
s.text(28,65,'15 cell-associated pieces; supports and retention counted. Concept only.','sub')
rows=[('1','Pin + integral screw/extension (2 pieces)','#7fb3d5','Terrain force → screw collar → frame'),('2','Two frame halves + 4 thrust washers (6)','#c0c8d0','Separate screw and input radial/thrust support'),('3','Shared-drive input gear + conical socket (1)','#90cfb2','Ø13 gear / Ø10 contact outer diameter'),('4','Sliding carrier (1)','#f5d37b','Keyed to output; 0.60-mm movement; no spring'),('5','Axial magnet + retaining film (2)','#e88484','Ø3 ×2; N up; electrically passive'),('6','Bobbin body + top flange + wound coil (3)','#d99b52','Fixed; 140 turns; 2 coil terminals')]
for j,(n,t,c,d)in enumerate(rows):
 yy=95+j*99;s.rect(80,yy,180,57,c);s.text(30,yy+32,n);s.text(300,yy+22,t);s.text(300,yy+47,d,'small')
 if j<5:s.line(170,yy+62,170,yy+91,True,True)
s.text(28,725,'Additional: two bonding operations, winding/terminations, shared fasteners, drive train and electronics.','sub')
s.text(28,753,'Exploded spacing is illustrative. Section drawing and CAD define the nominal envelope.','sub')
s.save(R/'concept-exploded.svg')
s=SVG(1080,790,'E-304 · one reusable force fixture')
s.text(28,65,'Two mechanically independent supports: scale carries magnet; bench carries coil.','sub')
s.rect(70,600,350,60,'#dbeaf5');s.text(95,638,'0.01-g scale + ≥100-g nonmagnetic preload')
s.rect(290,570,60,25,'#7fb3d5');s.rect(310,210,18,360,'#ddc49d');s.text(340,390,'Ø6 wood dowel','small');s.text(340,412,'nominal 80 mm','small')
s.rect(100,180,230,25,'#7fb3d5');s.rect(105,205,20,30,'#7fb3d5');s.rect(105,235,20,15,'#e88484');s.rect(105,250,20,15,'#6d9dd6');s.text(78,238,'N','small')
s.rect(77,248,18,50,'#d99b52');s.rect(135,248,18,50,'#d99b52');s.rect(68,298,110,10,'#b8bec3');s.rect(68,241,110,7,'#b8bec3');s.line(115,215,115,335,False,True)
s.rect(55,308,245,12,'#c6c9cd');s.rect(340,308,265,12,'#c6c9cd');s.line(300,314,340,314,False,True);s.rect(580,320,25,330,'#c6c9cd');s.text(450,350,'Independent bench stand','small')
s.line(100,265,45,265);s.text(28,286,'g','small');s.text(28,350,'z=0 at copper top','small');s.line(55,335,77,248,True)
s.line(147,268,490,140);s.text(495,138,'140 turns, 7 layers ×20 turns','label');s.text(495,162,'0.15-mm enamelled copper / 0.18-mm pitch','small');s.text(495,184,'Winding ID4.8 / OD7.32 / length3.6 mm','small')
s.text(640,270,'1. Print six parts as laid out.','label');s.text(640,300,'2. Wind, glue flange, measure R.','label');s.text(640,330,'3. Invert magnet arm for assembly.','label');s.text(640,360,'4. Bond magnet to Ø3 post; tape.','label');s.text(640,390,'5. Set signed g using a caliper.','label');s.text(640,420,'6. Read force at measured ±I.','label');s.text(640,465,'Optional core: Ø3 ×8 steel,','small');s.text(640,486,'sleeve from below; tip flush z=0.','small');s.text(640,507,'Only use g ≥0.3 mm with core.','small')
s.text(28,700,'Fz = −(scale reading − baseline) ×9.80665 mN/g. Tare at every gap; retain raw readings.','label')
s.text(28,731,'No contact between magnet/post and bore. Move stand, never preload the coil through the scale.','sub')
s.text(28,758,'Bracket points 90° to magnet arm: projected crossing above is clear in depth. No dowel/stand contact.','sub')
s.text(640,560,'Top view: keep supports separate','small');s.rect(770,585,110,12,'#7fb3d5');s.rect(770,585,12,70,'#c6c9cd');s.text(890,598,'dowel','small');s.text(790,650,'bench arm','small');s.text(640,605,'magnet/coil →','small');s.save(P/'assembly.svg')
s=SVG(1080,690,'E-304 · low-voltage bipolar bench wiring')
s.text(28,65,'Use identified Pololu 2130 carrier / one bridge. Verify measured current before mounting magnet.','sub')
s.rect(35,120,180,100,'#dbeaf5');s.text(48,150,'Bench 3–5 V DC');s.text(48,178,'Current limit 0.50 A');s.text(48,204,'Output switch + fuse')
s.rect(400,130,220,190,'#dcefe6');s.text(420,160,'DRV8833 carrier');s.text(420,190,'VIN / GND');s.text(420,230,'AIN1    AIN2');s.text(420,260,'AOUT1  AOUT2');s.text(420,294,'nSLEEP / AISEN')
s.line(215,140,400,140,True);s.text(240,126,'0.75-A fuse','small');s.line(215,205,400,205)
s.rect(250,260,120,60,'#f1e4cb');s.text(260,282,'100 µF /10 V','small');s.text(260,303,'+100 nF','small');s.line(300,260,300,140);s.line(330,260,330,205)
s.rect(790,130,210,80,'#f1e4cb');s.text(808,157,'10 Ω /5 W series');s.text(808,184,'Initial current limiting');s.line(620,245,740,245);s.line(740,245,740,170);s.line(740,170,790,170)
s.rect(790,285,210,75,'#e9c69c');s.text(810,315,'140-turn coil');s.text(810,340,'R ≈2.7 Ω (measure)');s.line(1000,170,1040,170);s.line(1040,170,1040,320);s.line(1040,320,1000,320);s.line(790,320,680,320);s.line(680,320,680,270);s.line(680,270,620,270)
s.rect(35,380,380,100,'#dbeaf5');s.text(50,409,'Pico: GP2 → AIN1; GP3 → AIN2');s.text(50,436,'GP4 → nSLEEP; common GND');s.text(50,462,'10-kΩ input pulldowns; no GPIO coil power','small');s.line(415,395,470,320,True)
s.text(470,400,'IN1 IN2       State','label');s.text(470,426,' 0     0          OFF / coast','label');s.text(470,452,' 1     0          +I','label');s.text(470,478,' 0     1          −I','label')
s.text(28,535,'Bridge paths handle inductive recirculation. No single flyback diode across a reversible coil.','label')
s.text(28,565,'Higher-current stage: documented carrier sense-trace modification +0.43 Ω /1% /1206 AISEN resistor.','small')
s.text(28,590,'Nominal trip ≈0.465 A, verify on load before removing10 Ω. Keep bench limit0.50 A; no default current limit.','small')
s.text(28,620,'Start ≤0.2-s pulses, ≥4.8-s cooling; stop at45°C or+10°C. Turn power off before changing core/wiring.','small')
s.text(28,651,'Unused B inputs low. Supply/interlock must also stop shared rotary drive in any later clutch test.','small')
s.save(P/'wiring.svg')
