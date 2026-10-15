---
status: complete
builds-on: [E-295, E-076, E-082, E-118]
---

# E-296 — compacte EN-koppeling: één huls, rijveer en kolomplafond

**Advies:** valideer eerst één schuifhuls met lokale rijveer, positieve rijterugtrekking en een kolomplafond. Deze aangepaste enkele koppeling heeft een geometrisch gecontroleerde EN-functie op **5,08-mm pitch**, met 4,4-mm pinnen op een hoger niveau. De oorspronkelijke twee tegengestelde duwbewegingen op dezelfde stijve huls vormen zonder extra mechaniek geen betrouwbare EN. **Kolom AAN moet het plafond omhoog vrijgeven**; een neergaand bedienuiteinde kan buiten het veld worden omgekeerd.

15 oktober 2026; basis `origin/main` **9ce8648**. Dit is analyse, engineering-CAD en reproduceerbare botsingscontrole, **geen fysieke werking, FDM-vrijgave of productiekwalificatie**. Geen issues, aankopen of automatische vervolgproeven.

**Oplevering:** [volledig ontwerprapport, vergelijkingen en fysieke proef](../tools/curated-experiment-checks/E-296/design-report.md), [CAD / reproductie](../tools/curated-experiment-checks/E-296/CAD-README.md), [gemengde 2×2 STEP](../tools/curated-experiment-checks/E-296/cad/matrix_R10_C10.step), [fasegeblokkeerde STEP](../tools/curated-experiment-checks/E-296/cad/matrix_phase_blocked.step), [onafhankelijke review](../tools/curated-experiment-checks/E-296/review.md).

![Vier mechanische toestanden](../tools/curated-experiment-checks/E-296/figures/01-four-states.png)

## Mechanisme en keuze

Input en schroef zijn onafhankelijk axiaal/radiaal in het frame opgesloten. Een roterende huls blijft op de inputhex en kan naar de outputhex schuiven. De rijring drukt via een lokale drukveer omhoog. Het kolomplafond blokkeert deze slag zolang de kolom uitstaat. De integrale onderflens wordt bij rijterugkeer gevangen; het terugkerende plafond drukt de bovenflens omlaag. Beide selectoren kunnen dus positief ontkoppelen.

Voor eindslagen `r,c ∈ {0;1,40}` en voldoende zetkracht geldt `q=min(c,r+0,20)`:

| Rij | Kolom | Huls q | Output |
|---|---|---:|---|
| 0 | 0 | 0 | 0,60 mm vrij |
| 1 | 0 | 0 | 0,60 mm vrij; veer vangt geblokkeerde rijslag op |
| 0 | 1 | maximaal 0,20 | minstens 0,40 mm vrij |
| 1 | 1 | 1,40 indien gezet | 0,80 mm profieloverlap; 0,425 mm rechte flank |

Zonder lokale compliance zou één halfgeselecteerde of tand-op-tand geblokkeerde huls de gehele starre rij stoppen. De veer voorkomt dat, maar garandeert nog geen fysieke zetting.

| Kandidaat | Besluit |
|---|---|
| Tegenkrachten / middenvenster | Afwijzen: klem-/krachtbalansprobleem of tijdelijk aangrijpen tijdens halfselectie. |
| **Eén hexhuls + rijveer + plafond** | **Eerste precisieproef:** minste lokale delen van de concrete EN-mechanismen. |
| Drie frontklauwen met dezelfde gate | Gedimensioneerd alternatief met grovere outputtanden; langer fasezoeken en smallere plafondrand. |
| Twee koppelingen in serie | Geometrische reserve; eigen tussenrotor/lagering, twee faseringen en circa 18-mm koppellengte in plaats van 6,5 mm. Behoudt rechtstreeks rij-omhoog/kolom-omlaag. |
| Wrijving / conus | Fasevrij, maar onbekende slip en veel hogere druk; niet kiezen zonder gemeten veel lager loopkoppel. |

## Ruimte, toleranties en negatieve resultaten

Ringen OD4,70 laten 0,38 mm onderlinge vrije ruimte. Actieve 2×2-envelop: 9,78 × 9,78 mm. De volledige rij-sweep eindigt op z1,70; kolomsweep begint op z4,10: **2,40 mm verticale vrijloop**. STEP bevat bovendien lagerplaten, twee vaste pingeleidingsvlakken en buiten het actieve veld geleide en geklemde kamuiteinden. De schroefdraad is een gelabelde ruimte-envelop; functionele draad blijft het E-295-profiel. De output/schroef is één integraal gereserveerd onderdeel, geen verzwegen verbinding tussen rakende losse vlakken.

De vergrote AF2,70-vangmond geeft 0,0578 mm berekende invangreserve bij expliciete ±0,02-mm profielmaten en **gemeten** hubasoffset ≤0,030 mm. Dat is een mogelijk geometrisch centreerpad, geen wrijvingsbewijs. ±0,10-mm AF-variatie kan zowel vastlopen als verlies van positieve torqueoverdracht geven; meer FDM-slop is dus geen oplossing. De 0,175-mm **draad**relief uit de succesvolle fysieke test kwalificeert deze hexpassing niet.

Alle 16 binaire 2×2-commando's zijn berekend. De zes getoonde assemblages zijn op nominale volumetrische botsingen gecontroleerd; de scripts bewaren ook faseblokkering en verkeerde trajecten als negatieve controles. Twee rijen plus twee kolommen koppelen alle vier kruispunten: diagonalen vereisen twee passes. Een gelijktijdige OFF→OFF-adrescrossfade kan tijdelijk 0,20 mm outputoverlap geven. Daarom: **input stoppen/ontlasten → rijen positief terug → kolommen wijzigen → gewenste rij heffen → zacht fasezoeken/volledig zetten → draaien**.

De review heeft een ongeschikte microclip vervangen door een integrale onderflens met gesplitste rijkam, onvoldoende kamgeleiding vervangen door geleideschoenen en een te kleine vangmond vergroot. Resterende fysieke risico's zijn tipmeeloop zonder seating, lage veerkracht tegenover echte glijwrijving, retourvangrand, toleranties en slijtage van permanent roterende hulzen. Lange 80-celstaven zijn niet als vrijdragende dunne strips vrijgegeven.

## Kosten en één fysieke beslisproef

B1 voegt per pin een huls en veer toe: **12.800 lokale extra delen** bij 6.400 pinnen, naast assen, schroeven en lagering. Iedere €0,10 per lokale set kost €640; 10 seconden montage per cel kost 17,8 uur. Dit zijn drempelberekeningen, geen leveranciersprijzen. De volledige vergelijking en een onzeker prototypebudget staan in het rapport. Eén resident koppeling is eenvoudiger dan twee, maar economisch nog niet overtuigender dan E-295's reizende bank.

**Eerste fysieke proef:** één handbediende 2×2-cartridge op werkelijke pitch. Meet eerst passing, asoffset, retourvangrand en minstens 0,15 mm OFF-spouw. Draai de vier inputs beurtelings in beide richtingen met dezelfde handkop; test alle vier toestanden, beide inschakelvolgordes en beide positieve retourroutes. Test zes startfasen, inclusief 30°, zowel onbelast als met een kleine gewogen miniatuurlast. Controleer volledige hulsseating en markeer alle outputassen/pinhoogtes. Deze takgewijze handproef ontwerpt of valideert geen gedeelde transmissie.

Doorgaan alleen bij zacht volledig zetten, onafhankelijke op/neerbeweging, vrijblijvende halfselecties en positieve terugkeer zonder buurbeweging boven de genoteerde meetresolutie. Stop bij vastlopen, schade, tipmeeloop zonder seating of false engagement. Bij falen volgt een keuze tussen de uitgewerkte alternatieven, geen automatische onderzoeksketen.

Nieuwste fysieke onderbouwing: [eigenaarresultaat compact-five-pairs](../owner-print-tests/2026-10-15-compact-screw-fit/test.md), 5/5 handpassingen positief; geen koppelingstest. De volledige bronnen, beperkingen, exacte bestanden en reproductiecommando's staan in het [ontwerppakket](../tools/curated-experiment-checks/E-296/CAD-README.md). **Stopconditie bereikt: concrete keuze, gecontroleerde CAD en één afgebakend fysiek experiment; geen fysieke succesclaim.**
