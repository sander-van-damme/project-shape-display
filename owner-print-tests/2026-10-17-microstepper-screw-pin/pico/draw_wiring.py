"""Render electrical diagram only; never touches mechanical drawings/CAD."""
from pathlib import Path
from html import escape
parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1380" viewBox="0 0 1500 1380">
<title>E-301 Pico W en TMC2208: 9V motorvoeding, 3,3V logica en voedingsuitval-reset</title>
<desc>Netnamen verbinden de vier panelen. TMC aansluitingen zijn logische namen, geen ongeverifieerde headerposities.</desc>
<style>text{font-family:DejaVu Sans,sans-serif;fill:#182836;font-size:18px} .title{font-size:30px;font-weight:bold}.head{font-size:23px;font-weight:bold}.small{font-size:15px}.wire{fill:none;stroke-width:3;stroke-linejoin:round} .box{fill:#fff;stroke:#9cabb7;stroke-width:2}</style>
<rect width="1500" height="1380" fill="#edf2f6"/>
</svg>'''.replace('</svg>', '')]
C = {'gnd':'#25313c', 'vm':'#b82a31', 'logic':'#176ab0', 'sig':'#8447a0','reset':'#1a8065'}

def text(x,y,s,kind='',color=None):
    parts.append(f'<text x="{x}" y="{y}" class="{kind}"'+ (f' style="fill:{color}"' if color else '') +f'>{escape(s)}</text>')

def box(x,y,w,h,fill='#fff',radius=12):
    parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="#9cabb7" stroke-width="2"/>')

def wire(points,color='sig'):
    parts.append('<polyline class="wire" stroke="'+C[color]+'" points="'+' '.join(f'{x},{y}' for x,y in points)+'"/>')

def node(x,y,color='sig'):
    parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{C[color]}"/>')

def label(x,y,s,color='logic'):
    text(x,y,s,'',C[color])

text(30,44,'E-301  |  Pico W → TMC2208 → bestaande motor','title')
text(30,76,'UART-only via VACTUAL • 9 V PD voor motor • computer-USB voor Pico')
box(25,98,1450,66,'#fff1d0')
text(42,124,'VÓÓR INSCHAKELEN: bevestig exact PCB, R110-shunts, UART-brug, motorparen en PD-DIP-tabel.','head')
text(42,150,'De TMC- en PD-blokken tonen aansluitnamen, GEEN fysieke pinvolgorde. Lees handleiding.md en wiring.md.','small')
# Logic panel
box(25,184,1450,478)
text(45,219,'1  Logica en motor — gebruik alleen bevestigde modulelabels','head')
box(50,243,292,370,'#e2f2eb')
text(72,276,'Pico W (RP2040)','head')
text(72,301,'USB → computer; USB boven','small')
rows=[(495,'GP4 TX / pin 6',''),(550,'GP5 RX / pin 7','')]
for y,name,dest in rows:
    text(65,y-8,name)
    if dest:
        wire([(342,y),(775,y)])
box(775,243,330,370,'#fff4e5')
text(795,276,'TMC2208 V1.2','head')
text(795,301,'Logisch blok; controleer jouw PCB','small')
for y,_,dest in rows:
    if dest:text(793,y+6,dest)
text(793,556,'PDN_UART')
text(793,341,'STEP / DIR / EN: LOS')
text(793,366,'Geen draden of weerstanden','small')
text(65,341,'GP2, GP3, GP6: ongebruikt','small')
text(65,370,'Snelheid en richting: UART','small')
# uart 1k and RX node
wire([(342,495),(425,495)])
box(425,481,100,28,'#fff',0);text(444,502,'1 kΩ','small')
wire([(525,495),(690,495),(690,550),(775,550)])
wire([(342,550),(690,550)]);node(690,550)
text(410,579,'TX via 1k; RX direct op dezelfde node','small')
# motor
box(1190,308,250,252,'#e9e7f2')
text(1210,343,'Motor Ø8 × 8,2','head')
text(1210,370,'Spanningsloos meten!','small')
for y,s in [(408,'Spoel A ~40Ω'),(496,'Spoel B ~40Ω')]:
    text(1210,y,s)
    wire([(1105,y-15),(1190,y-15)])
    wire([(1105,y+12),(1190,y+12)])
text(1000,393,'OA1','small');text(1000,420,'OA2','small')
text(1000,481,'OB1','small');text(1000,508,'OB2','small')
text(1190,593,'Andere labels: zie PCB-schema.','small')
text(47,643,'Pico 3V3(OUT), pin 36 → VIO;  GND pin 38 → alle GND.  MS1, MS2 en bevestigd CLK_IN → GND.','')
# power panel
box(25,682,1450,248)
text(45,716,'2  Motorvoeding — motor nooit rechtstreeks op PD aansluiten','head')
box(45,742,280,100,'#efe6fc')
text(65,773,'PD-trigger: kies 9 V','head')
text(65,800,'DIP-code: eerst bord verifiëren','small')
text(65,824,'OUT+ meten vóór aansluiten','small')
wire([(325,775),(365,775)],'vm')
box(365,753,170,44);text(379,782,'F1 250 mA snel')
wire([(535,775),(575,775)],'vm')
box(575,753,150,44);text(589,782,'S1 AAN/UIT')
wire([(725,775),(765,775)],'vm')
box(765,753,170,44);text(779,782,'SS14  → |')
wire([(935,775),(1415,775)],'vm')
label(1010,758,'VM → driver VM/VMOT','vm')
text(779,818,'band naar VM','small')
wire([(45,880),(1415,880)],'gnd')
label(46,909,'PD OUT− → GND = Pico GND = driver GND = supervisor GND','gnd')
# capacitors explicit symbolic box
for x,t in [(1090,'100µF / 25V'),(1290,'100nF / 25V')]:
    wire([(x,775),(x,802)],'vm');node(x,775,'vm')
    wire([(x,853),(x,880)],'gnd');node(x,880,'gnd')
    box(x-72,802,145,51);text(x-65,832,t,'small')
text(1010,865,'Elco: + VM / − GND; vlak bij driver','small')
# supervisor
box(25,950,945,365)
text(45,986,'3  Bestaande VM-bewaking: Pico-reset, daarna UART-stop','head')
box(475,1010,320,250,'#e0f2f1')
text(492,1040,'TPS3808G01DBVR','head')
text(492,1064,'SOT23-6 / DBV; adapter controleren','small')
label(44,1039,'VM (na diode)','vm')
wire([(45,1055),(185,1055)],'vm');box(185,1037,128,36);text(196,1062,'162kΩ 1%')
wire([(313,1055),(365,1055),(365,1110),(475,1110)],'vm');node(365,1110,'vm')
text(493,1116,'5  SENSE')
wire([(365,1110),(365,1140)],'vm');box(300,1140,130,36);text(310,1165,'10kΩ 1%')
wire([(365,1176),(365,1220)],'gnd');label(325,1245,'GND','gnd')
text(493,1155,'6  VDD → 3V3')
text(493,1188,'2  GND → GND')
text(493,1222,'4  CT: open (20 ms)')
text(45,1100,'Nominale drempel 6,97 V','small')
text(45,1131,'MR pin 3 → 10kΩ → 3V3','small')
text(45,1287,'VDD-GND: 100nF bij IC. RESET_N pin 1 → 10kΩ → 3V3; J1 → Pico RUN pin 30.','small')
wire([(795,1100),(935,1100)],'reset')
text(808,1088,'1 RESET_N','small',C['reset'])
text(810,1132,'J1 → RUN pin 30','small',C['reset'])
text(45,1346,'J1 alleen los voor installatie met VM UIT; vóór motorgebruik verplicht terugplaatsen.','small')
# legend panel
box(990,950,485,365)
text(1010,986,'4  Logicarail en controles','head')
text(1010,1022,'Pico pin 36  3V3(OUT)','',C['logic'])
text(1010,1055,'→ VIO + 100nF naar GND','',C['logic'])
text(1010,1088,'→ supervisor VDD + pull-ups','',C['logic'])
text(1010,1121,'Pico pin 38  GND: alle minpolen','',C['gnd'])
text(1010,1164,'Vref: 0,80 V t.o.v. GND; UART verplicht.')
text(1010,1197,'R110 + CS5 + VSENSE1: berekend','small')
text(1010,1220,'77mA piek / 55mA RMS per fase.','small')
text(1010,1256,'PD+ NOOIT op Pico, VIO of USB.','small',C['vm'])
text(1010,1286,'OFF = TOFF 0, dan VACTUAL 0.','small')
text(1010,1310,'Zwevende EN niet softwarematig overruled.','small')
parts.append('</svg>')
Path(__file__).with_name('wiring.svg').write_text('\n'.join(parts))
