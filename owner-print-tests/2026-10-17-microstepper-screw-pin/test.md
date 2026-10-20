# Microstappenmotor → één compacte schroefpin

> **Maatcorrectie 20 oktober 2026:** huis circa Ø8 ×9,2 mm, kale as circa Ø0,8 mm; twee benaderend gemeten tandwieluitstekingen. Zie [actuele eigenaarmetingen](../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md). Oude 8,2-mm huishoogte/Ø1,5-mm as en catalogusuitstekingen hieronder zijn historische brongegevens, geen actuele motorafmetingen. Bestaande CAD wordt hiermee niet aangepast of vrijgegeven.

> **E-301 — aanbevolen voor de beschikbare elektronica:** gebruik de
> [Pico W-handleiding](pico/handleiding.md), het [nieuwe schema](pico/wiring.svg)
> en [Pico-resultatenformulier met eerste fysieke verslag (18 oktober 2026)](pico/resultaten.md).
> Eigenaar heeft **daadwerkelijke op/neerbeweging** van een compacte pin gemeld
> bij **Vref ~0,80 V en S 100**. De succesvolle bedrading had **EN naar GND**,
> in afwijking van het oorspronkelijke UART-only-schema met zwevende EN.
> Kracht, snelheid en nauwkeurigheid zijn niet gekwantificeerd.
> [E-301](../../06-experiments/E-301-pico-w-motorcontroller.md).
>
> De onderstaande print-/montagegegevens blijven geldig als bestaande bron.
> De oudere elektronische instructies/commando-uitleg hieronder beschrijven de
> bewaarde **Uno/6V-variant**; volg voor Pico uitsluitend de gekoppelde handleiding.


**Status:** COMPLETED voor eerste eigenaarproof van op/neerbeweging; systematische karakterisering nog open\
**Prioriteit:** eerste fysieke haalbaarheidsvraag beantwoord\
**Laatst beoordeeld:** 2026-10-18\
**Vraag:** kan de bestaande Ø8 × 8,2-mm motor de bewezen compacte schroefpin
droog, betrouwbaar en met bruikbare snelheid in beide richtingen bewegen?\
**Bron:** [E-295](../../06-experiments/E-295-compact-screw-drive-development.md),
[motorbronnen en driverkeuze](sources.md).

Voor de limiet van drie READY-aanbiedingen zijn de oudere clutch-fit-,
clutch-matrix- en point-fit-aanbiedingen administratief DEFERRED; hun CAD/resultaten zijn behouden.
Er is geen verdere ontwikkeling aan die mechanismen gedaan.

## Fysiek geobserveerde uitkomst (18 oktober 2026)

Bij een **Pico W + TMC2208**, ongeveer **9 V VM**, **3,3 V VIO**,
**Vref ~0,80 V** en via UART ingestelde **S 100** kon de geprinte
schroefpin door de motor worden bewogen, zowel omhoog als omlaag.
De eigenaar gebruikte een **bijgesneden motorvak** en een
**ducttape-koppeling**. De motor past zonder extra uitsparing bij het
draadprintje niet goed; de oorspronkelijke slang-koppeling is niet
beproefd. Het frame is wel prettig toegankelijk en met elastiekjes
te sluiten. `M 1` leverde op de losse motor niet nauwkeurig 360°
en de retourfout stapelde zich op. De volledige hoogte, belasting,
temperatuur, werkelijk toerental en betrouwbare retourhoogte zijn
niet gemeten.

**Conclusie:** positieve eerste *beweegbaarheidsproef*, niet een
geslaagde volledige prestatie-/duurproef. Het volledige chronologische
verslag, bedrading, meetwaarden en suggesties voor de volgende motorzitting
staan in [pico/resultaten.md](pico/resultaten.md). De onderstaande
eerder ontwikkelde instructies en geplande meetmatrix blijven historische
testdocumentatie; ze zijn niet automatisch als uitgevoerd af te vinken.

## 1. Printklaar

Open **[microstepper-rig.3mf](microstepper-rig.3mf) als project** in Bambu Studio
en behoud de opgeslagen instellingen. Je hoeft geen CAD te compileren of STL's
te plaatsen. Eén plaat met vijf delen: **2 identieke framehelften, 1 houder,
1 schroef, 1 pin met 0,175-mm-passing**. Het functionele draadprofiel is behouden:
Ø3,2, spoed 3, vierkante pin 4,4. Een bestaand soepel nominaal paar mag worden
hergebruikt; de onderdelen heten afzonderlijk in de 3MF, zodat je dan schroef en
pin kunt uitschakelen. De tijd hieronder geldt voor alle vijf onderdelen.

- **Bambu Lab X1 Carbon, 0,4-mm nozzle, Generic PLA, Textured PEI**, nozzle
  220 °C, bed 55 °C. **0,12-mm lagen inclusief eerste laag**, Arachne, 2 wanden,
  0,45-mm nominale lijn, 100% infill. Geen supports, raft of brim; per laag printen.
- Eerste laag/buitenwand/kleine omtrekken/bruggen 15 mm/s, binnenwand 20 mm/s,
  infill/top/gap fill 30 mm/s. Acceleratie 1000 mm/s², buitenwand en eerste laag
  500. XY-/gat-/elephant-footcompensatie 0. Volledige koeling na eerste laag.
  Exacte instellingen: [bambu-settings.md](bambu-settings.md).
- Framehelften met splitvlak op bed; koppelsocket naar beneden; schroef en pin
  rechtop op hun brede bestaande voeten. Geen supportmateriaal in de draad.
- **Slicerschatting: 10,43 g PLA, 3,498 m, 2 uur 56 min 41 s totaal.**
  Plaat circa 103,5 × 73 mm, maximale modelhoogte 18,4 mm. Geen gemeten printtijd.
- Bambu Studio **02.08.02.61** heeft het opgeslagen project zonder externe
  profielen opnieuw geopend en gesliced. Beide slagen; instellingen identiek.
  [Baancontrole](slicer-review.json) en [detailbeelden](toolpaths.png).
- Inspectiepunten: brug in socket tot circa **10,38 mm**, framebruggen tot
  **6,98 mm**; doorhang kan passing verstoren. De dunne binnendraad heeft op
  **23 lagen** lokale nominale wandonderbrekingen; de bovenste buis is gesloten.
  Geen nieuw geïsoleerd laagdeel gevonden; dat bewijst geen fysieke wandsterkte.
  Bestaand goed passend paar heeft daarom de voorkeur wanneer beschikbaar.

## 2. Benodigd en monteren

Lees [assembly.md](assembly.md) voor montage en [electronics.md](electronics.md)
voor de **verplichte stroominstelling**, bedrading en software-installatie.
De [doorsnede](mechanism.svg) en het [bedradingsschema](wiring.svg) zijn meegeleverd.

Naast motor/PLA: Uno R3, geschikte TMC2208/R110 met UART, geregelde 6-V-voeding,
beveiligings- en ontkoppelonderdelen volgens de onderdelenlijst, **M3-ring
3,2 × 7 × 0,50 mm**, 6,5 mm siliconenslang ID2/OD4 bij het bestaande tandwieltje,
drie kabelbinders en een multimeter. Dit is geen aankoopopdracht; controleer
wat al aanwezig is. Een kale 1,5-mm as vereist de beschreven kleinere slang.

De schroefvoet staat in een vierkante houder; de houder rust op een metalen
ring op het frame. De motor draagt de pinlast niet. Een korte slang koppelt
1:1 en laat een circa 1-mm luchtspleet tussen motoras/tandwiel en geprinte stift.
Verwijder geen tandwiel. Zet de opstelling met tape aan de tafel vast.

**Vóór stroom:** het complete mechanisme moet met de hand droog over de
gekozen 3-mm-slag bewegen. Geen nieuwe smering, draadschuren, geforceerde passing
of aangedreven eindstop. Controleer vrije slangloop, terminals en axiale ruimte.

## 3. Korte fysieke proef

1. **Motorcontrole met pin los.** Meet spoelparen, stel Vref zonder motor op
   **0,80 V**, sluit pas spanningsloos aan. Installeer/upload de Uno-code en
   open Serial Monitor, 115200 baud/Newline. Typ `ARM MOTOR`, `S 5`, `M 1`.
   Tel één werkelijke volle omwenteling aan een verwijderbare markering;
   daarna `M -1`. Geen ratelen, slangslip of bewegend motorhuis. De aangenomen
   **20 hele stappen/omw moet hiermee worden bevestigd**, anders eerst de
   constante corrigeren en zonder pin opnieuw testen. Zie electronics.md.
2. **Centreren, spanningsloos.** Typ `OFF`, VM uit, wacht op <0,5 V.
   Monteer de pin en stel hem met de hand op **7,1 mm boven het geleideblok**.
   Controleer vrij handbereik **5,6–8,6 mm**, zet terug op 7,1. Noteer/markeer
   middenstand en slang/houder zodat slip zichtbaar is.
3. **Eerste pinbeweging.** VM aan, `ARM PIN`, `S 5`, `M 0.25`, `M -0.25`.
   Dat vraagt ±0,75 mm. Bekijk de werkelijke richting. De vierkante pin moet
   geleid blijven en de motor/schroef moeten werkelijk draaien. Verifieer
   terugkeer rond de markering; kleine afwijking registreren, niet automatisch corrigeren.
4. **Volledige kleine slag.** Vanuit de verklaarde nul: `C 1`. Dit beweegt
   midden → +1,5 → −1,5 → midden, dus **3 mm totale slag**. De firmware stuurt
   geen eindstop aan. Blijf kijken en houd de VM-schakelaar bereikbaar.
5. **Snelheid verhogen.** Als dit soepel gaat: `S 10`, `C 1`; daarna 20, 40,
   eventueel 60 en 120 rpm. Nominale continue pinsnelheden zijn respectievelijk
   0,5 / 1 / 2 / 3 / 6 mm/s; korte rampen verlagen het gemiddelde. Meet bij een
   bruikbare snelheid bijvoorbeeld de tijd van 10 cycli; dit is geen automatische
   meetfunctie. Stop bij de eerste fout, niet door alle snelheden heen forceren.
6. **Herhaling.** Op een geslaagde snelheid bijvoorbeeld `S 30`, `C 10`
   (nominaal 1,5 mm/s). Noteer alle 10 cycli en controleer starten/omkeren,
   retourhoogte, slanggrip en temperatuur na afloop. Zo nodig volledig afkoelen.
   Na 30 s zonder commando of een stop vervalt nul: **opnieuw handmatig centreren**.
7. **Optioneel 5 g last.** Alleen na een geslaagde onbelaste proef. Leg een
   licht kaartje van circa 10 × 10 mm op de holle pintop en daarop een stabiel
   gecentreerde, **gewogen totale massa van 5 g inclusief kaartje** (≈0,049 N).
   Raak het frame niet en laat niets in de holle pin vallen. Begin weer bij
   5 rpm en één cyclus; stop als de last kantelt. Last wegnemen vóór uitschakelen
   want de pin kan terugzakken. Geen handdruk als ongedefinieerde belasting.
8. **Alleen indien koel en niet geblokkeerd:** een herhaling bij Vref 1,00 V
   of maximaal 1,20 V mag volgens de uitschakel-/meetprocedure in electronics.md.
   Noteer de gewijzigde stroominstelling; vergelijk geen verschillende
   instellingen alsof ze één meting zijn.

**Direct stoppen:** blokkeert, ratelt zonder beweging, mist zichtbaar stappen,
slipt de koppeling, scheurt een onderdeel, ontstaat geur of wordt het motorhuis
rond 45 °C / snel merkbaar warmer: **`!` of VM-schakelaar uit**. Niet blijven
duwen/draaien; afkoelen en spanningsloos onderzoeken. Geen gevaarlijke beweging
naar mechanische eindstanden. Softwaregrenzen beschermen alleen bij correcte
staphoek, middenstand en daadwerkelijk gevolgde beweging; er is geen sensor.
Na stoppen met VM uit: ook `!` sturen of Uno RESET indrukken terwijl VM uit
blijft. Pas daarna VM herstellen, handmatig centreren en opnieuw ARM: de driver
moet zijn lage stroominstelling opnieuw krijgen vóór een nieuwe beweging.

## 4. Oorspronkelijk meetformulier — niet volledig doorlopen

Testdatum: ____  Werkelijk geprint project/instellingswijzigingen: ____\
Filament: ____  Bestaand paar hergebruikt? ____  Droog, geen nieuwe smering? ____\
Motorhuis Ø/lengte: ____  As/tandwiel: ____  Winding A/B Ω: ____\
Driver/PCB + R110 bevestigd: ____  VM onder last: ____ V  Vref: ____ V\
Gemeten omwentelingen bij `M 1`: ____  `FULL_STEPS` gebruikt: ____\
Printpassing motor/geleiding/houder/ring, brugdoorhang of draadschade: ____

| Vref | Doel rpm | Last g | Cycli gevraagd / geslaagd | Hoogtes min/max/retour mm boven frame | Tijd s | Stappen missen / slip / startproblemen | Motor-/driverwarmte |
|---|---:|---:|---|---|---|---|---|
| 0,80 V | 5 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 10 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 20 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 40 | 0 | 1 / ____ | ____ | ____ | ____ | ____ |
| ____ | 60 / 120 indien soepel | 0 | ____ | ____ | ____ | ____ | ____ |
| ____ | gekozen ____ | 0 | 10 / ____ | ____ | ____ | ____ | ____ |
| ____ | 5 / gekozen ____ | 5 optioneel | ____ | ____ | ____ | ____ | ____ |

Temperatuur: meetwaarde met methode indien beschikbaar, anders “koel/lauw/warm”;
geen verzonnen graden. Hoogte/tijd eveneens als meting of schatting benoemen.

**Succes:** meerdere volledige droge op/neercycli bij een voor mij bruikbare
snelheid, zonder vastlopen, zichtbare stapuitval, slangslip of overmatige warmte.\
**Bruikbare snelheid volgens eigenaar:** ____  **Hoogste foutloze geteste snelheid:** ____\
**Uitkomst:** [ ] voldoende voor deze proef [ ] onvoldoende [ ] onbeslist [ ] nog niet getest.\
**Oorzaak bij fout:** [ ] motorstappen [ ] koppeling slipt [ ] verkeerde passing
[ ] voeding/driver [ ] draadschade [ ] onbekend. Opmerkingen: ____

## 5. Interpretatie

Eerste fysieke op/neerbeweging is door de eigenaar bevestigd, maar de
systematische resultaten voor kracht, stabiliteit, herhaalbaarheid en volledige
slag blijven open. Een slippende tijdelijke koppeling, scheve montage of
onjuiste staphoek is **geen zuivere afwijzing van motorkoppel**. Een goede droge
3-mm-proef bewijst uitsluitend deze ene motor/pin/stroom/snelheid/lastcombinatie.
Er wordt geen 40-mm-slag of complete displayarchitectuur mee gekwalificeerd.
Geen vervolgopdracht of extra printserie is ingepland.
