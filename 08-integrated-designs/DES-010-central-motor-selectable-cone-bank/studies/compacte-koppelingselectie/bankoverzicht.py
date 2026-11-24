"""Maatblad van bank, schrijfwagen en magnetische lijnvariant."""
from model import *
from parkering import rect,line
def make():
    a=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1020" viewBox="0 0 1500 1020">',
       panel(1,1,1498,1018),svgtext(35,49,"Van enkele kanaaldoorsnede naar één bank",31,700),
       svgtext(36,82,"Bovenaanzicht  /  x langs de tachtig stiften  /  y naar de schrijfkoppen",18)]
    x0=92; scale=3.15
    for i in range(10):
        x=x0+scale*(i*8-.5)*PITCH
        a.append(rect(x,160,scale*40.2,102,"#e4ecea"))
        a.append(rect(x,135,scale*40.2,17,COL["schuif"]))
        for j in range(8):
            xx=x0+(i*8+j)*PITCH*scale
            a.append(f'<circle cx="{xx:.2f}" cy="179" r="5.8" fill="{COL["stift"]}"/>')
        a.extend([rect(x,199,scale*40.2,8,COL["park"]),rect(x+57,227,10,22,COL["hef"])])
    a.extend([line(60,237,1408,237,COL["pool"],6),svgtext(70,121,"10 platen × 8 stiften   ·   modulepitch 40,64",17,600),
              line(x0,287,x0+79*PITCH*scale,287),svgtext(580,313,"Hart-op-hart uitersten 401,32",18,600)])
    for i in range(4):
        x=x0+20*PITCH*scale*i
        a.extend([rect(x-7,347,15,26,COL["puls"]),rect(x-14,373,45,21,COL["select"]),
                  line(x,421,x+19*PITCH*scale,421,COL["hef"],3),svgtext(x+85,449,"20 adressen",15)])
    a.extend([line(51,397,1425,397,COL["pool"],5),svgtext(53,482,"B  /  vier vingers op één riem. Iedere vinger schrijft 96,52 mm. Asafstand tussen de wagens 101,60 mm.",19,650),
              rect(85,518,16,26,COL["puls"]),rect(78,544,46,18,COL["select"]),line(50,568,1425,568,COL["pool"],5),
              svgtext(53,605,"D en C  /  één wagen over 401,32 mm. Een tweede wagen halveert de schrijfafstand.",19,650),
              line(45,640,1450,640,"#bccbc9"),svgtext(47,682,"E  /  alternatief met lineaire magneet",22,700)])
    for i,high in enumerate([False,True]):
        xx=130+220*i; yy=841
        a.extend([rect(xx-34,yy-83,25,9,COL["pool"]),rect(xx+9,yy-83,25,9,COL["pool"]),rect(xx-34,yy+45,68,9,COL["pool"]),
                  rect(xx-48,yy-49,17,66,COL["puls"]),rect(xx+31,yy-49,17,66,COL["puls"]),
                  rect(xx-24,yy-69 if high else yy-7,48,44,COL["magneet"]),
                  rect(xx-7,yy-122 if high else yy-60,14,53,COL["vork"]),
                  svgtext(xx,933,"ON" if high else "OFF",16,650,INK,"middle")])
    a.extend([svgtext(510,741,"Magneet Ø2 × 2, poolafstand circa 5,2, één axiale spoel.",20,650),
              svgtext(510,785,"De verticale drukstang loopt door de bovenste open poolschoen.",18),
              svgtext(510,819,"De onderste pool houdt de ruststand, de bovenste moet de cupdruk dragen.",18),
              svgtext(510,853,"Bij het losbreken bedraagt de afstand tot de doelpool nog circa 3 mm.",18),
              svgtext(510,887,"Het nokalternatief gebruikt hetzelfde ene pulskanaal en een mechanische reset.",18),
              svgtext(46,987,"Bank in plan op schaal langs x. y-afstanden en afzonderlijke magneetdoorsneden ter verduidelijking uitvergroot.",16,400,MUTED),"</svg>"])
    (OUT/"bankoverzicht.svg").write_text("\n".join(a))
if __name__=="__main__":
    make()
