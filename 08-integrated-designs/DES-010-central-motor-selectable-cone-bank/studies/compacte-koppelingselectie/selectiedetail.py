"""Laat de beslissende beweging per kanaal vergroot zien, uit dezelfde contouren."""
from model import *
from parkering import line
def draw():
    phases={"A":("PARK","SELECT"),"B":("SELECT","DRIVE"),"C":("PARK","DRIVE"),
            "D":("PARK","DRIVE"),"E":("PARK","DRIVE")}
    captions={"A":("Pal vangt de lage schouder","Anker kantelt de pal, veer heft","Veerdruk op de stift"),
              "B":("Schrijfkop schuift de teen boven het lage mes","Mes tilt de gekozen teen met de vork","Hefmes op hoge rust"),
              "C":("Midden van het bladpaar staat beneden","Stelvinger heeft het bladpaar doorgeklikt","Elastisch evenwicht"),
              "D":("Voet beneden, pal boven de draaglip","Draaglip rust op de teruggeklikte pal","Druk via harde palsteun"),
              "E":("Magneet aan onderste pool, cam laag","Magneet aan bovenste pool, cam hoog","Magnetische eindstand")}
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1360" viewBox="0 0 1500 1360">',
         panel(1,1,1498,1358),svgtext(35,50,"Waar wordt de keuze bewaard?",35,700),
         svgtext(36,84,"Dezelfde kanaalcontouren vergroot. In de rechterkolom is de schrijfenergie weer weg, behalve tijdens de ontgrendelpuls van A.",18)]
    for i,k in enumerate("ABCDE"):
        top=107+i*246
        out.extend([panel(28,top,1444,232),svgtext(48,top+34,k+"   "+NAMES[k],23,700),
                    svgtext(1040,top+34,captions[k][2],19,600,MUTED)])
        for j,phase in enumerate(phases[k]):
            xmin=7 if k=="C" else 11
            left=50+720*j
            cid=f"z{k}{j}"
            out.append(f'<defs><clipPath id="{cid}"><rect x="{left}" y="{top+46}" width="675" height="145"/></clipPath></defs>')
            pp=[p for p in geometry(k,phase) if p.key not in ("resident","stift","schuif") and p.label not in ("drukvoet","rotor / journal")]
            out.extend([f'<g clip-path="url(#{cid})">',section(pp,left+135-xmin*10,top+328,10.25),'</g>',
                        svgtext(left+5,top+215,captions[k][j],17,600)])
            target={"A":(17.6,24.6),"B":(21.8,21.1 if j==0 else 23.9),
                    "C":(19.6,21.45 if j==0 else 24.25),"D":(21.5,20.9 if j==0 else 23.3),
                    "E":(22.0,17.55 if j==0 else 25.07)}[k]
            xx=left+135-xmin*10+target[0]*10.25
            yy=top+328-target[1]*10.25
            out.append(f'<circle cx="{xx:.2f}" cy="{yy:.2f}" r="11" stroke="#bd522b" stroke-width="2" fill="none"/>')
    out.append('</svg>')
    (OUT/'selectiedetail.svg').write_text('\n'.join(out))
if __name__=="__main__":
    draw()
