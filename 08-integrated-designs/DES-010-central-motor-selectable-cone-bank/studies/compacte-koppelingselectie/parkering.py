"""Tekenblad voor de gedeelde rijvergrendeling. Maatkritische coupe uit model.py."""
from model import OUT, geometry, section, panel, svgtext as t, INK, MUTED, COL

def rect(x,y,w,h,c):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1" fill="{c}" stroke="{INK}" stroke-width="1.2"/>'

def line(x,y,X,Y,c=INK,sw=2):
    return f'<path d="M{x} {y} L{X} {Y}" fill="none" stroke="{c}" stroke-width="{sw}"/>'

def sheet():
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1040" viewBox="0 0 1500 1040">',
         rect(0,0,1500,1040,"#f1f5f4"),t(35,50,"Parkeren vraagt twee bewegingen",34,700),
         t(35,82,"Eerst trekt de vork de conus uit de cup. Daarna tast een stalen plaat de werkelijke baan van de stift af.",19)]
    for i,(state,title,txt) in enumerate([("PARK","Gesloten bij vrije conus","Plaat overlapt de as tot y +2,20."),
                                        ("DRIVE","Geopend bij aandrijving","De plaatneus staat op y −2,20."),
                                        ("DRIVE","Storing tijdens reset","Een hoge stift stopt de plaatneus.")]):
        x=30+i*490
        out.extend([panel(x,110,470,350),t(x+14,145,title,21,700)])
        shapes=[p for p in geometry("B",state) if p.key in ("resident","stift","schuif") and p.label not in ("vierkant","hals")]
        # Toon de vierkante stift wanneer deze in de meetlaag zit.
        stift=next(p for p in geometry("B",state) if p.label=="vierkant")
        stift.yz=[(y,max(25.2,z)) for y,z in stift.yz]
        shapes.insert(0,stift)
        if i==2:
            plate=next(p for p in shapes if p.key=="schuif")
            plate.yz=[(y+1.20,z) for y,z in plate.yz]
        out += [section(shapes,x+240,858,20),t(x+15,418,txt,16),
                t(x+15,443,["Rijpen mag vrij na alle tien modules.","Rijpen zit in het indexgat.","Rijpen blijft in het indexgat."][i],16,600)]
    out+=[panel(30,477,1440,332),t(49,514,"Bovenaanzicht  /  tien onafhankelijke sluitplaten van acht kanalen",23,700),
          t(49,545,"Drie modules afgebeeld. Midden blijft achter door één geblokkeerde stift.",17)]
    for j in range(3):
        x=95+j*405; jam=j==1; shift=0 if jam else 18
        for i in range(8):
            xx=x+36*i
            out.append(f'<circle cx="{xx}" cy="613" r="11" fill="{COL["stift"] if jam and i==4 else "#edf1f0"}" stroke="{INK}"/>')
        out.append(rect(x-17,627-shift,286,27,COL["schuif"]))
        out.append(rect(x+6,654-shift,14,34,COL["schuif"]))
        out.append(rect(x+6,675-shift,30,7,COL["pool"]))
        out.append(rect(x+37,662 if jam else 650,11,25,COL["select"]))
        out.append(t(x-16,720,["Plaat thuis · pal vrij","Plaat gestopt · pal blokkeert","Plaat thuis · pal vrij"][j],16,600))
    out.extend([rect(75,682,1200,8,COL["park"]),t(83,764,"Schuifstang met tien nokken beweegt 1,5 mm langs x. Eén blokkerende pal houdt de gemeenschappelijke rijpen gevangen.",17),
                t(83,789,"Elke pal valt door eigen bladveer in de blokkeerstand. Alleen de bijbehorende stalen plaattong kan haar lichten.",16,400,MUTED),
                panel(30,827,1440,180),t(48,861,"Mechanische volgorde en lokale ondersteuning",22,700)])
    rows=[("1  Drukas","Tien nokken op Ø6-as drukken 10 × 8 oren omlaag. Bovenlip van elke vork vangt de collar."),
          ("2  Meetschuif","Tweede nok spant tien begrensde vingers. Rechte plaatneuzen lopen tussen boven- en ondergeleiders."),
          ("3  Rijverplaatsing","Doorlopende sleutelstang valt achter alle tien plaatstaarten. De platen blijven boven de conussen."),
          ("4  Volgende rij","Rijpen moet eerst in een indexgat vallen. Pas dan kan de sleutelstang terug en de meetlaag open.")]
    for i,(a,b) in enumerate(rows):
        out.extend([t(49,893+i*29,a,16,700),t(253,893+i*29,b,16)])
    out.append("</svg>")
    (OUT/"parkering.svg").write_text("\n".join(out))
if __name__=="__main__":
    sheet()
