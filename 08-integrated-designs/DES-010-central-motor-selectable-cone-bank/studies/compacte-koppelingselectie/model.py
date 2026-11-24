"""Schaaltekeningen van de kinematische ontwerpstudie. Python 3, standaardbibliotheek."""
from dataclasses import dataclass
from html import escape
from math import cos, sin, pi, radians
from pathlib import Path

OUT = Path(__file__).parent / "figuren"
PITCH, LIFT, CUP, CONE, SHUT = 5.08, 2.4, 29.0, 1.386, 28.36
INK, MUTED = "#16343a", "#4d686e"
COL = {"resident":"#9baeb0","stift":"#218480","vork":"#2fa99b","park":"#d87740",
       "schuif":"#dfaa50","huis":"#c1ccce","select":"#8060a1","hef":"#3979ad",
       "veer":"#6e8d4c","puls":"#ae6681","pool":"#73868e","magneet":"#b94c54"}
NAMES = {"A":"Veer en ontgrendelpal","B":"Schrijfbare haak en gedeeld hefmes",
         "C":"Voorgespannen bladpaar","D":"Schrijfkop met directe lift","E":"Magnetische excentercam"}
STEPS = {"A":["Veer opgespannen","Pal trekt terug","Veer drukt conus","Balk drukt pal vast","Meetplaat sluit"],
"B":["Mes onderaan","Kop zet haak","Mes op hoge rust","Mes daalt, wisser wist","Meetplaat sluit"],
"C":["Bladen naar onder","Kop duwt door midden","Bladen boven","Balk klapt door","Meetplaat sluit"],
"D":["Bovenpal vrij","Kop heft lip","Pal draagt lip","Wisser licht pal","Meetplaat sluit"],
"E":["Cam lage pool","Puls draait cam","Cam op hoge pool","Balk keert cam","Meetplaat sluit"]}
SPEC = {"A":("drukveer · kniepal · spoel",32),"B":("schrijfvinger · schuifhaak · hefmes",32),
"C":("zijankers · bladpaar · middenstift",37),"D":("liftvinger · draaglip · borgpal",31),
"E":("excenter · magneet · twee poolschoenen",34)}

@dataclass
class Part:
    key: str
    label: str
    x: float
    w: float
    yz: list
    group: int

def rect(y,z,l,h):
    return [(y,z),(y+l,z),(y+l,z+h),(y,z+h)]

def circle(y,z,r):
    return [(y+r*cos(i*pi/16), z+r*sin(i*pi/16)) for i in range(32)]

def bar(y,z,Y,Z,t):
    length=((Y-y)**2+(Z-z)**2)**.5
    a,b=-(Z-z)/length*t/2,(Y-y)/length*t/2
    return [(y+a,z+b),(Y+a,Z+b),(Y-a,Z-b),(y-a,z-b)]

def geometry(k, phase="DRIVE", chosen=True):
    # SELECT toont het einde van programmeren. RESET toont het einde van terughalen.
    on=chosen and (phase=="DRIVE" or (phase=="SELECT" and k!="B"))
    lift=LIFT*on
    sealed=phase in ("PARK","TRAVEL")
    low=phase in ("PARK","RESET","TRAVEL")
    s=26.6+lift
    parts=[]
    def add(key,label,poly,w,g,x=0):
        parts.append(Part(key,label,x,w,poly,g))
    def box(key,label,y,z,l,h,w,g,x=0):
        add(key,label,rect(y,z,l,h),w,g,x)
    for sign in (-1,1):
        add("resident","cup",[(sign*y,z) for y,z in [(1.9,29),(2.3,29),(2.3,31),(0,31),(0,30.386),(1.1,30.386)]],4.6,1)
    box("resident","hals", -1,31,2,2.1,2,1)
    box("huis","rotor / journal",-2,12,4,8,4,0)
    box("stift","vierkant",-1,s-18,2,18,2,3)
    box("stift","collar",-2.1,s-2.6,4.2,.8,4.2,3)
    add("stift","conus",[(-1.9,s),(1.9,s),(1.1,s+CONE),(-1.1,s+CONE)],3.8,3)
    # U-vork: projectie van beide zijtanden en hun brug achter de collar.
    for xx in (-1.95,1.95):
        for dz in (-3.5,-1.7):
            box("vork","U-tand",-2.15,s+dz,5.35,.8,.7,4,xx)
    box("vork","rug",2.55,s-3.5,2,2.6,4.6,4)
    box("vork","arm",4,s-3.5,7.7,1.25,3.0 if k=="C" else 4.4,4,-.80 if k=="C" else 0)
    box("vork","parkeeroor",8,s-2.3,2,1.4,4.4,4)
    box("park","drukvoet",8,25.75 if low else 28.22,2,.6,4.6,6)
    box("schuif","meetplaat",(-5.8 if sealed else -10.2),SHUT,8,.30,4.65,7)
    # De voet van de selector werkt achter de oude handjacks.
    a=23.1+lift
    if k=="A":
        box("vork","stang",11,a,6.8,1.25,3.6,4)
        box("huis","veerzitting",11.6,15.5,4,1,4.4,0)
        for i in range(10):
            zz=16.5+(a-16.5)*i/10
            add("veer","staalveer",bar(12.1 if i%2 else 15.1,zz,15.1 if i%2 else 12.1,zz+(a-16.5)/10,.32),2.9,8)
        # Pal boven rechter armrand, ontgrendeld uit contact.
        off=-.40 if phase=="SELECT" and chosen else 0
        add("select","pal",[(17.7+(y-17.7)*cos(off)-(z-21.9)*sin(off),21.9+(y-17.7)*sin(off)+(z-21.9)*cos(off)) for y,z in [(17.35,24.4),(18.1,24.4),(18.25,22.15),(24.8,21),(25.3,21.8),(18.4,22.9),(18.65,25.1),(18.0,25.2)]],2.2,9)
        add("pool","as",circle(17.7,21.9,.48),3.6,10)
        box("puls","spoel",24.4,13.8,4.2,4.0,4.2,11)
        add("pool","anker",[(17.7+(y-17.7)*cos(off)-(z-21.9)*sin(off),21.9+(y-17.7)*sin(off)+(z-21.9)*cos(off)) for y,z in rect(24.55,20.4,1.25,1)],2.2,12)
    else:
        # Bij ON buigt de 8 mm lange krachtlip t.o.v. zijn onbelaste stand.
        add("vork","krachtlip",bar(11.2,a+.45,19.2,a+.45+.4*on,.9),3.0 if k=="C" else 3.6,4,-.80 if k=="C" else 0)
        box("vork","schoen",18.6,a-.2+.4*on,3.2 if k=='E' else 1.6,.8,3.6,4)
        h=lift+.4*on
        if k=="B":
            shift=1.45 if chosen and phase in ("SELECT","DRIVE") else 0
            box("select","haakslede",15.85+shift,21.9+h,4.4,.95,2.9,9)
            box("select","haakteen",20+shift,20.6+h,.95,1.4,2.9,9)
            box("hef","mes",21.25,19.8+2.8*(phase=="DRIVE"),1.9,.8,4.65,10)
            box("huis","meeneemkooi",17.5,20.9+h,1,2,3.8,4)
            box("puls","schrijfvinger",13.15+shift,22.0,2.6,.55,2,11)
            box("park","wiskam",23.1 if not low else 21.15,20.65,1,1.25,4.4,12)
        if k=="C":
            mid=21.45+h
            box("select","middenstift",19.05,mid-1.3,1.1,2.95,4.5,4)
            # Bladen lopen langs de krachtlip in twee zijdelingse vlakken.
            for y,Y in [(7.6,19.6),(31.6,19.6)]:
                add("veer","knikblad",bar(y,22.85,Y,mid,.65),1.35,4,1.62)
                box("huis","anker",y-.55,21.8,1.1,2.2,1.35,4,1.62)
            box("puls","stelvinger",18.7,mid-2.4 if phase=="SELECT" else 17.4,1.8,1.1,2,11)
        if k=="D":
            box("select","hefvoet",18.55,20.5+h,2.45,2.4,3.6,8)
            box("select","draaglip",20.5,20.5+h,1.55,.9,3.6,8)
            dy=1.35 if phase=="RESET" else 0
            add("veer","borgpal",[(y+dy*min(1,max(0,(z-18)/4.2)),z) for y,z in [(21.5,23.3),(23.1,23.3),(24.6,18),(23.9,18),(22.5,22.2)]],2.5,9)
            box("huis","palsteun",22.7,21.8,1.2,1.4,3.8,0)
            box("park","resetlip voet",20.3,24.25 if low else 27.25,.6,.45,2.6,12)
            box("puls","stelvinger",18.6,22.2 if phase=="SELECT" and chosen else 18.2,1.7,1.1,2,11)
            box("park","wisblad",24 if not low else 24.8,18.4,.75,2.6,4.3,12)
        if k=="E":
            ang=radians(55 if on else -55)
            # Excentrische schijf, bovenste raaklijn beweegt 2,8 mm.
            cy,cz=19.4,21.3
            ey,ez=cy+1.709*cos(ang),cz+1.709*sin(ang)
            add("hef","nok",circle(ey,ez,3.0),2.7,9)
            add("pool","as",circle(cy,cz,.55),4.35,10)
            Y,Z=cy+4.6*cos(ang),cz+4.6*sin(ang)
            add("select","magneetarm",bar(cy,cz,Y,Z,1.65),2.25,9,-.15)
            add("magneet","NdFeB",[(Y+u*cos(ang)-v*sin(ang),Z+u*sin(ang)+v*cos(ang)) for u,v in [(-1,-1),(1,-1),(1,1),(-1,1)]],2,13,-.15)
            for sign in (-1,1):
                aa=radians(sign*55)
                py,pz=cy+6.2*cos(aa),cz+6.2*sin(aa)
                add("pool","poollip",[(py+u*cos(aa)-v*sin(aa),pz+u*sin(aa)+v*cos(aa)) for u,v in [(-.4,-1),(.4,-1),(.4,1),(-.4,1)]],2.8,12)
                add("pool","poolbrug",bar(py,pz,29.4,cz+sign*5.65,.8),2.8,12)
            box("puls","spoel",24.5,17.8,4.4,7,4.3,11)
            box("pool","juk",28.9,15.4,1,11.8,3.4,12)
            add("hef","resetarm",bar(cy,cz,cy+4.8*cos(ang),cz+4.8*sin(ang),.85),.7,9,1.72)
            box("park","terugstoter",21.8,17.9 if low else 26.1,2.4,.65,.7,6,1.72)
    return parts

def svgtext(x,y,t,size=17,weight=400,color=INK,anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{escape(t)}</text>'

def path(points,fill,stroke=INK,sw=.9):
    pts=" ".join(f"{x:.2f},{y:.2f}" for x,y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'

def panel(x,y,w,h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#fff" stroke="#d0dbdb"/>'

def section(parts,x,y,sc):
    out=[]
    for p in parts:
        out.append(path([(x+Y*sc,y-Z*sc) for Y,Z in p.yz],COL[p.key],sw=.72))
    return "".join(out)

def iso(parts,x,y,sc,explode=False):
    out=[]
    for p in sorted(parts,key=lambda p:(p.x, -sum(a for a,b in p.yz)/len(p.yz))):
        move=(p.group*5.0 if explode else 0)
        def project(dx, v):
            yy,zz=v
            return (x+sc*(yy+.58*(p.x+dx+move)),y+sc*(.30*(p.x+dx)+.10*move+.13*yy-zz))
        back=[project(-p.w/2,v) for v in p.yz]
        front=[project(p.w/2,v) for v in p.yz]
        out.append(path(back,COL[p.key],sw=.5))
        for i in range(len(front)):
            j=(i+1)%len(front)
            out.append(path([back[i],back[j],front[j],front[i]],COL[p.key],sw=.40))
        out.append(path(front,COL[p.key],sw=.65))
    return "".join(out)

def draw(k):
    w,h=1500,1080
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
         '<rect width="1500" height="1080" fill="#f3f6f4"/>',svgtext(35,50,f"{k}   {NAMES[k]}",32,700),
         svgtext(36,80,SPEC[k][0]+"   /   DES-010   /   maten in mm",18)]
    for i,phase in enumerate(["PARK","DRIVE"]):
        x=30+i*735
        out+=[panel(x,106,715,276),svgtext(x+18,138,("OFF  ·  geparkeerd","ON  ·  geselecteerd")[i],22,700),
             section(geometry(k,phase),x+112,414,7.7),
             svgtext(x+18,365,"Samengestelde langsdoorsnede y–z   ·   vorktanden in projectie",15,400,MUTED)]
        tags = {"A":[("drukveer",13.6,19),("pal op schouder",17.8,24.6),("spoel en anker",26,16)],
                "B":[("haakteen",21.6 if i else 20.5,23.8 if i else 21.2),("gemeenschappelijk mes",22.6,23.0 if i else 20.2),("schrijfvinger",14.6,22.2)],
                "C":[("middenstift",19.6,23 if i else 21),("knikblad",25.5,23.6 if i else 22.1),("anker",31.6,22.85)],
                "D":[("draaglip",21.2,23.6 if i else 21),("borgpal",23,22.5),("stelvinger",19.3,18.8)],
                "E":[("excentrische nok",20.5,23 if i else 20),("magneet op arm",22,25 if i else 17.6),("spoel met juk",27,19)]}[k]
        for j,(label,Y,Z) in enumerate(tags):
            X=x+112+Y*7.7; zz=414-Z*7.7
            out.append(f'<circle cx="{X}" cy="{zz}" r="7.4" fill="#243b43" stroke="white" stroke-width=".8"/>')
            out.append(svgtext(X,zz+3.5,str(j+1),9,700,"white","middle"))
            out.append(svgtext(x+417,189+32*j,f"{j+1}   {label}",17,600))
        out.append(svgtext(x+417,307,"Cup Ø4,6  /  z29",15,400,MUTED))
        out.append(svgtext(x+417,330,"Vork 4,60 breed  /  slag 2,40",15,400,MUTED))
    out += [panel(30,397,715,315),svgtext(48,429,"Drie buren   ·   1 en 3 gekozen",22,700)]
    parts=[]
    for i in range(3):
        pp=geometry(k,"DRIVE",chosen=i!=1)
        for p in pp:
            p.x+=PITCH*i
        parts.extend(pp)
    out += [iso(parts,195,689,7.4),svgtext(49,687,"x = 0 / 5,08 / 10,16    ·    drie kanaalbreedten samen 15,24",15,400,MUTED),
            panel(765,397,715,315),svgtext(783,429,"Explosie   ·   onderdelen langs x uiteen",22,700),
            iso(geometry(k,"PARK"),872,685,7.2),
            svgtext(784,687,"Gelijke kleur = functie. Prismatische enveloppen van rondwerk.",14,400,MUTED)]
    for i in range(3):
        # Voorvlak van de bediende assen: een echte recht-op-x orthoprojectie.
        xx=459+PITCH*10*i; base=26.6+(LIFT if i!=1 else 0)
        out.append(path([(xx+10*X,805-8*Z) for X,Z in [(-1.9,base),(1.9,base),(1.1,base+CONE),(-1.1,base+CONE)]],COL["stift"]))
        out.append(path([(xx+10*X,805-8*Z) for X,Z in [(-1,base-4),(1,base-4),(1,base),(-1,base)]],COL["stift"]))
        for sign in (-1,1):
            out.append(path([(xx+10*sign*X,805-8*Z) for X,Z in [(1.9,29),(2.3,29),(2.3,31),(0,31),(0,30.386),(1.1,30.386)]],COL["resident"]))
        out.append(svgtext(xx,653,"ON" if i!=1 else "OFF",13,600,INK,"middle"))
    out.append(svgtext(515,526,"Voorzijde",15,600,MUTED,"middle"))
    for i,(key,label) in enumerate([("resident","cup / schroef"),("stift","conusstift"),("vork","vangvork"),("park","reset / wisser"),("schuif","meetplaat"),("huis","huis / geleider"),("select","pal / slede"),("hef","mes / nok"),("veer","veer / blad"),("puls","pulsorgaan"),("pool","as / staal"),("magneet","magneet")]):
        xx=40+(i%6)*242; yy=744+(i//6)*26
        out.append(f'<rect x="{xx}" y="{yy-14}" width="18" height="14" fill="{COL[key]}"/>')
        out.append(svgtext(xx+25,yy,label,16))
    for i,phase in enumerate(["PARK","SELECT","DRIVE","RESET","TRAVEL"]):
        xx=30+i*292
        out += [panel(xx,804,280,231),svgtext(xx+12,835,phase,20,700),
                section(geometry(k,phase),xx+65,1003,4.7),svgtext(xx+12,1012,STEPS[k][i],15)]
    out += [svgtext(35,1060,"Studiegeometrie  •  axiale slag 2,40  •  vierkant 2,0  •  collar Ø4,2  •  cupvlak z29  •  getuigde meetlaag z28,36–28,66",16,400,MUTED),"</svg>"]
    (OUT/f"{k}.svg").write_text("\n".join(out))

if __name__=="__main__":
    OUT.mkdir(exist_ok=True)
    for concept in NAMES:
        draw(concept)
