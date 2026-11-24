"""Opengelegde onderdelen en het gedeelde montageprofiel."""
from model import *
from parkering import rect,line

LABELS = {
 0:"Bank / rotor / vaste steun",1:"Cup met schroef",3:"Conus + collar + schuifstift",
 4:"Vangvork met parkeeroor",6:"Drukvoet op nokvolger",7:"Stalen meetplaat",
}
EXTRA={
"A":{8:"Stalen drukveer",9:"Pal met retourlip",10:"Scharnierdraad",11:"Spoel op klikbobbin",12:"Zachtstalen anker"},
"B":{9:"Haakslede met klikdetent",10:"Hefmes op dwarsas",11:"Schrijfvinger op wagen",12:"Gezamenlijke wiskam"},
"C":{11:"Stelvinger op wagen"},
"D":{8:"Hefvoet met draaglip",9:"Palvinger in kamstrip",11:"Stelvinger op wagen",12:"Wiskam + terughaalvoet"},
"E":{9:"Excentrische nok met arm",10:"Dwarsas",11:"Spoel op klikbobbin",12:"Juk met twee poollippen",13:"Geklemde Ø2 × 2 magneet"}}
def make(k):
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1200" viewBox="0 0 1500 1200">',
         panel(1,1,1498,1198),svgtext(36,48,k+"   Opengelegde montage",32,700),
         svgtext(37,79,"Gescheiden volgens montagestuk. Vaste huizen en drukorganen herhalen per acht kanalen.",18)]
    parts=geometry(k,"PARK")
    labs=LABELS|EXTRA[k]
    if k=="C": labs[4]="Eén stift, vork, bladen en ankers"
    for i,(g,lab) in enumerate(labs.items()):
        xx=35+(i%4)*366; yy=105+(i//4)*165
        out += [panel(xx,yy,350,151),svgtext(xx+12,yy+25,lab,15,650)]
        pp=[p for p in parts if p.group==g]
        pts=[(y,z) for p in pp for y,z in p.yz]
        ymin,zmin=map(min,zip(*pts)); ymax,zmax=map(max,zip(*pts))
        scale=min(12.5,255/(ymax-ymin+3),83/(zmax-zmin+2))
        out.append(iso(pp,xx+34-ymin*scale,yy+49+zmax*scale,scale))
    out += [svgtext(37,648,"Achter de kanaalmodules",25,700),svgtext(37,679,"Uiteengelegd langs de montagerichting. Lengten onderbroken. Kleuren volgen de functie in de doorsnede.",17)]
    configs=[(742,"Stalen meetplaat en eigen invoerveer",COL["schuif"]),
             (815,"Achtkanaalshuis en klikdeksel",COL["huis"]),
             (885,"Drukvoet, nok en gemeenschappelijke as",COL["park"]),
             (960,"Normaal gesloten pal en sleutelstang",COL["select"])]
    for yy,label,color in configs:
        out.extend([svgtext(59,yy,label,17,600),line(415,yy-5,455,yy-5,MUTED,1)])
        for j in range(3):
            xx=475+190*j
            if yy==742:
                out.extend([rect(xx,yy-21,155,14,color),rect(xx+65,yy-8,10,19,color),line(xx+70,yy+11,xx+94,yy+23,COL["veer"],4)])
            elif yy==815:
                out.extend([rect(xx,yy-26,155,6,color),rect(xx,yy+12,155,8,color)])
                for q in range(8):
                    out.append(rect(xx+q*19,yy-8,4,20,color))
            elif yy==885:
                out.extend([rect(xx,yy-20,155,7,color),rect(xx+66,yy-14,16,29,color),rect(xx-16,yy+2,198,6,COL["pool"])])
            else:
                out.extend([rect(xx-16,yy+7,198,5,COL["pool"]),rect(xx+80,yy-5,8,13,color),line(xx+65,yy-17,xx+82,yy-4,COL["veer"],4)])
    out += [svgtext(1080,736,"10 × staalplaat",18,650),svgtext(1080,811,"10 × klikcassette",18,650),
            svgtext(1080,883,"1 × reductiemotor + koppeling",17,650),svgtext(1080,957,"1 × geveerde rijpen",18,650)]
    extras={"A":"80 spoelen op klikstroken • 10 driverstroken • 160 spoelaansluitingen",
            "B":"4 schrijfservos op gekoppelde wagens • 1 scanmotor • 1 GT2-riem • 2 poelies • 1 geleider",
            "C":"1 stelservo op wagen • 1 scanmotor • 1 GT2-riem • 2 poelies • 1 geleider",
            "D":"1 stelservo op wagen • 1 scanmotor • 1 GT2-riem • 2 poelies • 1 geleider",
            "E":"80 spoelen op klikstroken • 10 driverstroken • 160 spoelaansluitingen"}
    out.extend([line(38,1000,1460,1000,"#d2dada"),svgtext(40,1043,extras[k],18,600),
                svgtext(40,1082,"Gedeeld: controller, vermogensdriver, eindcontacten, voedingsbuffer, zekering, kabelboom en eindbevestiging.",17),
                svgtext(40,1118,"Eindmontage en inkoopaantallen staan in onderdelen.csv. Cup, transmissie en schroef behoren tot de bestaande bank.",17),
                svgtext(40,1163,"Ontwerpstudie  /  de directe mechanische meetlaag en rijpen staan op het afzonderlijke parkeerblad.",15,400,MUTED),"</svg>"])
    (OUT/f"{k}-montage.svg").write_text("\n".join(out))
if __name__=="__main__":
    for concept in NAMES: make(concept)
