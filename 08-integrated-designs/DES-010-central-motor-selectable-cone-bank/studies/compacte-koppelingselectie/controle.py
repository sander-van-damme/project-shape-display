"""Gerichte 2,5D-controles. Geen algemene botsingszoeker, FEA of sterktekwalificatie."""
from math import cos, radians, hypot, sin
from model import geometry, PITCH, CONE, CUP, LIFT, SHUT
from raming import total

def report():
    park_tip=CUP-LIFT+CONE
    assert abs(park_tip-27.986)<1e-8
    for k in "ABCDE":
        for phase in ("PARK","SELECT","DRIVE","RESET","TRAVEL"):
            for selected in (True,False):
                pp=geometry(k,phase,selected)
                assert all(abs(p.x)+p.w/2<=PITCH/2 for p in pp)
                cone=next(p for p in pp if p.label=="conus")
                plate=next(p for p in pp if p.label=="meetplaat")
                tip=max(z for _,z in cone.yz)
                if max(y for y,_ in plate.yz)>0:
                    assert tip<min(z for _,z in plate.yz)
                if phase=="DRIVE":
                    assert abs(tip-(CUP+CONE if selected else park_tip))<1e-7
        print(k,"min. x-rest tussen lokale enveloppen, meest ongunstige gelijke buren:",
              round(PITCH-max(2*abs(p.x)+p.w for p in geometry(k)),3),"mm",total(k),"EUR")
    # Een tip boven de plaat is verbonden met de vierkante stift; aan de
    # hartlijn is er in deze hele slag materiaal van stiftvoet tot tip.
    hits=0
    for i in range(241):
        lift=i/100
        occupied=26.6+lift-18 < SHUT <= park_tip+lift
        if occupied: hits+=1
        assert occupied==(lift>=.38)
    print("Meetlaag onderschept",hits,"van 241 standen; eerste botsing +0,38 mm vanaf PARK.")
    print("Ruimte onder/boven plaat:",round(SHUT-park_tip,3),round(CUP-SHUT-.3,3))
    for deg in range(-55,56):
        cy=19.4+1.709*cos(radians(deg))
        assert 18.6<=cy<=21.8
    print("E raakpunt blijft op de schoen. Noklift:",round(2*1.709*sin(radians(55)),3))
    for E in (1200,1800,2200):
        a=12
        force=max(2*E*.65*1.35*(1-hypot(a,z/100)/hypot(a,1.4))*(z/100)/hypot(a,z/100) for z in range(141))
        print("C ideale piek",E,"MPa:",round(force,3),"N")
    for lift in (1.2,1.8,2.0,2.2,2.4):
        print("retractie",lift,"vrije tipruimte",round(lift-CONE,3),"mm")
if __name__=="__main__":
    report()
