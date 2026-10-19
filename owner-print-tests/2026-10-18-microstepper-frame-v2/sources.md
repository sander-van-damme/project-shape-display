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
radiale tipposities A0,95/N1,00/C1,05 mm. Historische A/N/C hadden 7,8-mm rechte lengte plus 0,5-mm inloop.
Revisie 4 behoudt alleen C met 5,8-mm rechte lengte plus dezelfde inloop. Een werkelijk afwijkend tandprofiel kan elke variant afkeuren.

De lobben zijn verbonden met een dikke Ø5-mm buitencilinder, geen losse
sub-nozzle tandjes. Toolpathcontrole meet daadwerkelijk de binnencontour en
open boring op alle relevante lagen. Dit kwalificeert alleen de digitale slice.
PLA-samentrekking, stringing, oppervlaktekwaliteit en werkelijke flankpassing
blijven eigenaarstest. Geen claim van productierijpheid of bewezen herbruikbaarheid.

## Motorsteun — gecorrigeerd op eigenaarfeedback

De vorige E-302-plaat in commit 3d554a3 bevatte twee zijvensters; de eigenaar
wilde een duidelijke uitsparing aan één zijde en behoud van de oorspronkelijke
steun. Revisie 2 gebruikt complementaire helften met één gemeenschappelijke,
naar buiten open uitsparing: X −8…−2,5, Y −3,5…3,5, Z 2…10,5 mm.
Deze ruimte is na vereniging met de veren uitgesneden en als volledig vrij
gecontroleerd in de gemonteerde CAD. Het blijft een ontwerp-envelope; de foto
bevat geen PCB-maten. De tegenoverliggende cilindrische steun blijft behouden.

De vrije ruimte achter de aanvullende veren is verkort tot Z4,5…8,5, zodat
onder- en bovenaan meer van de cilindrische huiszitting blijft staan. Veren:
vrije span 10, dikte 0,6, axiale breedte 2,4 mm, binnenvlak op radius 3,9.
Nominaal Ø8 geeft 0,1-mm uitbuiging. Ideale vast-vast balkberekening
ε≈12tδ/L²≈0,72%; geen gemeten montagekracht of garantie van klemkracht.
De veren liggen buiten de PCB-opening. Boordiameter 8,30 blijft parametrisch.

## Pin van 50 mm

De E-301-schroef en standaardpin zijn byte-identiek meegeleverd. De 50-mm pin
verlengt uitsluitend de rechte bovenbuis van de standaardpin (4,4 mm vierkant,
3,52 mm binnenruimte); onderste draad, 6-mm aangrijping en 12-mm printvoet blijven
behouden. Onderste 18 mm geometrisch vergeleken. Hoogte 50 mm betekent geen
50-mm slag: het frame behoudt de 3-mm proefslag. Printbaarheid van de slanke
buis wordt afzonderlijk over alle lagen gecontroleerd; fysieke stabiliteit blijft
te observeren. Geen support in de draad en geen functionele nabewerking.

## Controle overschuifmaten

`scripts/review_dimensions.py` rekent de foto-opgave na: m0,2 × 9 geeft steekdiameter
1,8 mm en standaard tandtopdiameter 2,2 mm. Vrijloopboring 2,5 mm laat 0,15 mm
radiale ruimte buiten de tandtoppen, behalve de drie aangrijpingsribben.
Een **aangenomen**, niet gemeten 20° standaard-involuut geeft minimale berekende
flankboogruimte A≈0,014 / N≈0,070 / C≈0,143 mm. A is analytisch marginaal en bleek fysiek te strak.
De werkelijke drukhoek, ondersnijding en tandvorm ontbreken; dit is geen
gevalideerde maatvoering voor alle motoren. De eigenaar koos C; beide N-exemplaren gingen kapot. Alleen C wordt opnieuw aangeboden. De 4-mm foto-uitsteking is geen tandlengte.

## Parameters voor feedback

`cad/rig.scad`: `body_d`, `pcb_half_width`, `pin_height`, springvlak3,9/dikte0,6/span10,
`tip_r`, `socket_bottom`, `socket_top`. Geen wijziging van de schroef/pin nodig.
Bij aanpassen altijd STL en3MF opnieuw genereren, heropenen en opnieuw controleren.

## Historie: lange schroef met supports — revisie 3 (vervangen)

Na de eerdere toevoeging van de 50-mm pin vroeg de eigenaar ook een bijpassende
lange schroef en supports tegen wiebelen. `cad/long-screw.scad` gebruikt dezelfde
vastgezette BOSL2-kernel, diameter3,2/spoed3/diepte0,9/profiel90° en voet10×10×2,4,
met48 mm draad in plaats van16. Totale hoogte50,4 mm; laatste0,6 mm afgeschuind.
De lange schroef vervangt één van de twee korte exemplaren op dezelfde plaat.

Printpose:90° om Y gedraaid, as5 mm boven bed. Dit maakt de constructie10 mm hoog;
alleen de lange schroef heeft echte Bambu-supportbanen langs de onderzijde en een
3-mm brim. Het globale supportprofiel blijft uit, met één expliciete objectoverride.
`scripts/build_project.py` bewaart en heropent ook die lokale instellingen. Horizontaal
printen verandert de laagoriëntatie en kan littekens op de onderste draadflanken
geven. De digitale controle bewijst ondersteuning, niet schadevrije verwijdering
of fysieke passing. Beide worden apart in het resultatenformulier geregistreerd.

## Eigenaarfeedback en revisie 4 — 19 oktober 2026

Remote eerst opgehaald met `git pull --ff-only origin main`; basis `9a57fd6`.
[Fysieke eigenaarresultaten](resultaten.md): A te strak, beide N kapot, C goed;
kop met motor te lang voor frame; horizontale lange schroef slecht geprint en
supports lastig te verwijderen; korte schroef geen probleem. Werkelijk gebruikte
instellingen onbekend. Geen nieuwe gemeten slag, koppel of volledige montageslaag.

C is 2 mm aan het motoruiteinde ingekort, mond Z13,2 en rechte ribben Z13,7–19,5;
ringvlak, lagerhals en schroefvoet blijven op dezelfde hoogte. De foto-afgeleide
Z14,2-tandtop zou nog slechts 0,5 mm rechte overlap geven: fysieke hoogtemeting
blijft nodig, geen passingclaim op basis van die foto.

`cad/long-screw-supported.scad` voegt aan de ongewijzigde lange schroef twee torens
met acht kleine afbreekverbindingen toe; de functionele schroef wordt rechtop
geprint. Contacten zitten bij de draadtoppen, per zijde 12 mm uit elkaar. De
steunen zijn geometrie, automatische supports blijven uit. Schadevrije verwijdering
en printstabiliteit zijn nog onbekend; controleer de werkelijke banen en test met de hand.
`components/archive/coupling-A.stl`, `components/archive/coupling-N.stl` en `components/archive/screw-long-horizontal.stl` zijn uitsluitend
historische bronnen. De oude C en complete revisie 3 zijn terug te vinden op `9a57fd6`.
