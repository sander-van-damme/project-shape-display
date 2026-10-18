# Maatbronnen, ontwerpkeuzes en grenzen

Remote eerst opgehaald met `git pull --ff-only`, basis0383489. Gelezen:
root/owner-print-tests/06-experiments AGENTS, missie, huidige prioriteiten,
E-301 CAD, montage, maatbronnen en vooral [fysiek verslag](../2026-10-17-microstepper-screw-pin/pico/resultaten.md).

- Eigenaarobservatie18 oktober: bestaande motor beweegt pin omhoog/omlaag bij
  circa0,80 V; houder moest uitgesneden worden; ducttape lastig; twee uitvoeringen
  met verschillende tandwieluitsteking. Niet gekwantificeerd.
- [Originele maatfoto](../2026-10-17-microstepper-screw-pin/motor-dimensions-original.jpg):
  Ø8×8,2-mm huis, Ø2,2-mm tandwiel,9 tanden,module0,2,4-mm totale uitsteking.
  Foto-opdruk/catalogusbron, **geen meting aan eigenaarsmotoren**. De derde
  motorfoto toont dezelfde motor uit andere hoek, geen derde type.
- PCB-envelope, soldeerhoogte, tandwortel, tandprofiel, tandlengte en tweede
  uitsteking zijn onbekend. De PM08-02 PDF beschrijft een ander huis/as; niet gebruikt.

## Waarom drie ronde lobben?

Module0,2 geeft berekende steekπm≈0,628 mm en nominale tanddikte op de
steekcirkel≈0,314 mm. Negen kleine interne involuuttanden zijn daarmee geen
betrouwbare standaardkeuze bij een0,4-mm-nozzle. Drie120° verdeelde ronde
wandlobben grijpen bij9 tanden telkens elke derde tandruimte aan. Er wordt
slechts ondiep op buitenste flanken gemikt. Rondingradius0,5 mm, basisboringØ2,5;
radiale tipposities A0,95/N1,00/C1,05 mm. Alle hebben identieke7,8-mm rechte lengte
plus0,5-mm inloop. Een werkelijk afwijkend tandprofiel kan elke variant afkeuren.

De lobben zijn verbonden met een dikke Ø5-mm buitencilinder, geen losse
sub-nozzle tandjes. Toolpathcontrole meet daadwerkelijk de binnencontour en
open boring op alle relevante lagen. Dit kwalificeert alleen de digitale slice.
PLA-samentrekking, stringing, oppervlaktekwaliteit en werkelijke flankpassing
blijven eigenaarstest. Geen claim van productierijpheid of bewezen herbruikbaarheid.

## Motorsteun

Behouden: tweedelig frame, Ø3/Ø3,5 lager, ring, keeper, geleiding, schroef en pin.
Nieuwe volledige zijvensters laten PCB/draden naar buiten. Twee dwarse
PLA-veerbruggen (vrije span10, dikte0,6, axiale breedte2,4 mm) hebben binnenvlak
op radius3,9; nominale Ø8 motor geeft0,1-mm uitbuiging per kant. Ruwe ideale
vast-vast balkberekening ε≈12tδ/L²≈0,72%; geen FEA of gemeten montagekracht.
Bruggen worden in printoriëntatie vanaf twee einden ondersteund. Een eerdere
los hangende contactpad is tijdens review verworpen vóór de definitieve slice.
Resterende cilindervlakken steunen de motor axiaal gespreid. Motorbodem rust
op framevoet; rubberbanden sluiten harde framevlakken en raken geen printplaatje.

## Parameters voor feedback

`rig.scad`: `body_d`, `pcb_half_width`, springvlak3,9/dikte0,6/span10,
`tip_r`, `socket_bottom`, `socket_top`. Geen wijziging van de schroef/pin nodig.
Bij aanpassen altijd STL en3MF opnieuw genereren, heropenen en opnieuw controleren.
