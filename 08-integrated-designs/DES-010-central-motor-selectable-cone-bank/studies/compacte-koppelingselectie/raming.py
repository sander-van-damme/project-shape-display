"""Genereer de materiaalstaat (prijzen per regel voor één bank, geen offertes)."""
from pathlib import Path
import csv

# Bereik, aantal verbruikte onderdelen, subtotalen in euro. Arbeid afzonderlijk.
rows = [
("alle","10 modulehuizen + 10 klikdeksels + 10 drukvoeten + 10 noksets + 2 eindwangen + lagersteunen, borgstanggeleiders geïntegreerd","1 set ca. 165 g PETG",3.30,5.00),
("alle","Doorlopende stalen nokas Ø6 × 430, sleutelstang met tien nokken en 2 clips","1 + 1 + 2",2.50,5.50),
("alle","Meetplaten 40,2 × 8 × 0,30 uit bandstaal met omgezette staart, inclusief snijverlies","10 uit één strook",1.50,4.50),
("alle","Veerstalen invoervingers en normaal blokkerende palveren, pal-strip en pennen","10 + 10, uit 2 strips",1.00,3.00),
("alle","Rijpen met veer, haak, eindaanslagen en gemeenschappelijke bevestiging","1 + 1 + 1 + 2 + 8",1.20,3.00),
("alle","Parkgearmotor incl. reductie en askoppeling, stroombegrenzer/H-brug","1 + 1 + 1",6.50,15.00),
("alle","Kleine controller, voedingsaandeel DC-regelaar, zekering en buffer","1 set",3.00,6.00),
("alle","Park/eindcontacten, massabus, connectors en kabelboom","2 contacten + 1 set",1.50,3.50),
("alle","Vangvorken of geïntegreerde C-stiften, inclusief flexlip waar gebruikt","80 × ca. 0,70 g",1.12,1.68),
("ABCE","Extra mechanische wiskam of stoter geïntegreerd in tien noksets","10, inbegrepen",0,0),
("A","Stalen drukveer, OD 3,0–3,2, en geprinte pal met aangevormde retourlip","80 + 80",8,24),
("A","Spoellichaam, koper circa 100 windingen per kanaal, zachtstalen anker en pool, gemeenschappelijke scharnierdraad per module","80 + 80 + 80 + 80 + 10",8,23),
("AE","MOSFET, vrijloopdiode, gate/pulldown, 10 schuifregisters, printstroken, 160 draadlassen en voedingsverdeling","80 + 80 + 160 + 10 + 10 stroken",11,26),
("BCD","Scanmotor met driver, GT2-riem ca. 1 m, 2 poelies, geleiderstaf + glijgeleiding, eindcontact","1 + 1 + 1 + 2 + 1 set + 1",10.50,23.00),
("BCD","Kopkabel, flexlus en trekontlasting","1 set",1.00,2.50),
("B","Geprinte haaksledes met klikdetent, hefmesstroken en resetkam","80 + 10 + 10",1.20,3.00),
("B","Vier SG90-klasse schrijfkoppen, vingers, gekoppelde loopwagens en koppeldraad","4 + 4 + 4 + 1",12.80,20.00),
("C","Vervangbare monolithische bladparen met sokkels (extra polymeer), stelkop, vinger en wagen","80 geïntegreerd + 1 + 1 + 1",4.50,8.00),
("D","Hefvoeten met draaglip, tien achtvingerige palstrips, zijwaartse wiskam, aanslag","80 + 10 + 10 + 10 geïntegreerd",1.00,3.00),
("D","Eén SG90-klasse stelkop, vinger en wagen","1 + 1 + 1",3.70,6.50),
("E","Excenters met magneetclip en retourarm, module-aspennen en 2 borgclips per as","80 + 10 + 20",1.50,4.00),
("E","Axiale schijfmagneet Ø2 × 2, opgesloten in dwarszak","80",10.40,24.00),
("E","Enkele spoel/bobbin per kanaal, gestanst stalen retourjuk met twee poollippen","80 + 80 + 80",9.00,24.00),
]
def total(k):
    selected=[r for r in rows if r[0]=="alle" or k in r[0]]
    return tuple(round(sum(r[i] for r in selected),2) for i in (3,4))
if __name__=="__main__":
    with (Path(__file__).parent/"onderdelen.csv").open("w",newline="") as f:
        w=csv.writer(f,lineterminator="\n")
        w.writerow(("concept","onderdeel en bewerking","aantal per bank","laag EUR","hoog EUR"))
        w.writerows(rows)
    for k in "ABCDE":
        print(k,total(k))
