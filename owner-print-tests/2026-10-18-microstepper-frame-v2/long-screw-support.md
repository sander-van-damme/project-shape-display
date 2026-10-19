# E-302 — rechtopstaande lange schroef met plaatselijke zijsteunen

**Revisie 4, 19 oktober 2026.** De eigenaar rapporteerde dat de horizontaal
geprinte revisie 3 slecht printte en dat de moeilijk verwijderbare supports de
werking hinderden. Deze revisie vervangt die printopstelling; zij is nog niet
fysiek geprobeerd. De functionele schroef blijft **48 mm draad / 50,4 mm totaal**.

![Werkelijke G-code van rechtopstaande schroef en zijsteunen](images/long-screw-review.png)

## Constructie en instellingen

`cad/long-screw-supported.scad` voegt aan `components/screw-long.stl` twee torens toe. Ze staan
op X ±7,5 mm; elke toren heeft een 3 × 3-mm doorsnede en een voet van 4 × 8 × 0,48 mm.
Vier oplopende armen per toren eindigen bij een draadtop, met een kleine nek van
**0,45 mm breed × 0,24 mm hoog** (0,85 mm lang, deels overlappend). De armen stijgen
ongeveer 45° en worden laag voor laag vanuit de toren opgebouwd. Per zijde zit
12 mm tussen de contacten; het bovenste contact ligt slechts circa 3 mm onder de punt.

| Zijde | Nominale contacthoogtes vanaf bed, mm | Werkelijke contactlagen in beide slices, mm |
|---|---|---|
| X− | 9,96 / 21,96 / 33,96 / 45,96 | Elke genoemde hoogte en de laag 0,12 mm erboven |
| X+ | 11,40 / 23,40 / 35,40 / 47,40 | Elke genoemde hoogte en de laag 0,12 mm erboven |

De contacten raken de draadtop plaatselijk. Er is **geen lossingsafstand**:
het zijn dunne vaste afbreekverbindingen, geen automatisch gegenereerde supports.
Knip ze lokaal door. Een garantie van schadevrije verwijdering volgt hier niet uit.

Object `08-screw-50-supported` omvat de schroef én de beide torens; het heeft een
3-mm buitenbrim met 0,12-mm afstand. Automatische supports staan globaal en op
**alle acht objecten uit**, zodat geen supportmantel of gevulde binnendraad ontstaat.
X1 Carbon / 0,4-mm nozzle / PLA, 0,12-mm lagen. Volledig proces in
[metadata/saved-settings.json](metadata/saved-settings.json), lokale brim in
[metadata/saved-object-settings.json](metadata/saved-object-settings.json).

## Werkelijke slicecontrole

Bambu Studio **02.08.02.61** heeft de opgeslagen 3MF zelfstandig heropend en opnieuw
gesliced zonder externe profielen. Globale en objectinstellingen bleven gelijk.
`scripts/review_long_screw.py` controleert beide G-codes; resultaten:

- 420 model-lagen tot Z50,40; doorlopende schroefkerncontour op alle lagen.
- Alle 16 draadgangen behouden een uitgesproken draadtop in de nominale baanvoetafdruk.
- Alle acht nekken verbinden draad en arm op twee lagen. De oplopende arm wordt
  via opeenvolgende overlappende laagcontouren teruggevolgd tot zijn toren.
- Beide torens zijn aanwezig vanaf de bouwplaat tot Z47,52, met brede eerste-laagvoeten.
- Geen losse nieuwe laageilandjes, geen extra arm/draadverbindingen buiten de acht contactzones.
- Geen automatische supportbanen op de hele plaat; pinboringen blijven vrij.

Het volledige pakket wordt geschat op **13,22 g en 4u12m01s**; na heropening
4u12m07s. Dit zijn slicerschattingen, geen werkelijk verbruik of printtijd.
Nominale baanoverlap bewijst geen hechting, materiaalsterkte of trillingsvrij printen.

## Verwijderen en testen

Laat afkoelen, maak de brim los en neem de complete constructie van de plaat.
Ondersteun de schroef vlak naast het contact. Knip met een kleine vlakke kniptang
de dunne nekken afzonderlijk door, van boven naar beneden en afwisselend links/rechts.
Buig of trek niet aan de hele toren. Verwijder torens en brim; behoud de vierkante
schroefvoet. Controleer alle acht contactplaatsen op PLA-resten, scheuren,
afgebroken draadtoppen en kromming. Draai eerst met de hand door de 50-mm pin.
Stop bij klemmen; de motor mag de verbinding niet forceren.

De torens beperken de vrije schroeflengte tijdens printen. Hun praktische
stabiliteit en de verwijderbaarheid blijven fysieke testpunten in [resultaten.md](resultaten.md).
De pinnen behouden hun bestaande integrale printvoet; die blijft aan de pin zitten.

Bewijs: [eerste slice](metadata/long-screw-review.json),
[heropende slice](metadata/long-screw-review-reopened.json),
[bouw en roundtrip](metadata/microstepper-frame-v2-build.json).
De oude horizontale STL is historische evidence, geen actuele printinstructie.
