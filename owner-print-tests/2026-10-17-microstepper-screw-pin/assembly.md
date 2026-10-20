# Montage — één schroefpin, directe aandrijving

> **Maatcorrectie 20 oktober 2026:** huis circa Ø8 ×9,2 mm, kale as circa Ø0,8 mm; twee benaderend gemeten tandwieluitstekingen. Zie [actuele eigenaarmetingen](../../08-integrated-designs/DES-009-traveling-motor-bank-screw-pins/motor-variants-limits.md). Oude 8,2-mm huishoogte/Ø1,5-mm as en catalogusuitstekingen hieronder zijn historische brongegevens, geen actuele motorafmetingen. Bestaande CAD wordt hiermee niet aangepast of vrijgegeven.

Zie [montagetekening](mechanism.svg) en [CAD-overzicht](assembly.png).
Vijf printdelen, circa 36 × 20 × 53 mm gemonteerd; alle maten hieronder in mm.
De twee framehelften zijn identiek. De rotorhouder neemt de ongewijzigde
10 × 10 × 2,4-mm voet van de bestaande compacte schroef op. De schroef draait
1:1; de vierkante pin wordt over 8 mm geleid. De eigen printvoet van de pin
blijft zitten en blijft tijdens de 3-mm-proef onder de geleiding.

## Fysieke eigenaarfeedback (18 oktober 2026)

**Bij het daadwerkelijk gemonteerde exemplaar** moest de eigenaar plastic
uit de motorzitting snijden om het kleine printplaatje/de aansluitingen voor
de vier motordraden aan één motoruiteinde vrij te maken. Daardoor was de motor
niet stevig genoeg gefixeerd. De hieronder getekende motorzitting is dus
**niet ongewijzigd als passend bevestigd**.

De voorgeschreven siliconenslang-koppeling is in deze proef **niet**
aangetoond: de eigenaar verbond motor en schroef voorlopig met **ducttape**.
Dat bleek voldoende om een bestaande compacte pin bij **Vref ~0,80 V** op en
neer te bewegen, maar was onaangenaam en lastig te monteren. De motoren hebben
al tandwielen; er zijn ten minste twee uitvoeringen met verschillend axiaal
uitstekende tandwielen. Een volgende variant zou een gemakkelijk te plaatsen
opsteekkop rond het tandwiel moeten onderzoeken, met tolerantie voor
verschillende insteekdieptes en framevariatie. Nog niet dimensioneel gemeten.

**Behouden:** tweedelig, toegankelijk frame en de mogelijkheid de helften
met elastiekjes samen te houden; dit beviel de eigenaar (ook al vraagt de
eerste montage wat moeite). Ruimte voor twee of drie motoren naast elkaar
kan nuttig zijn, maar er is **nog maar één motor fysiek getest**. Het
[volledige proefverslag](pico/resultaten.md) bevat alle waarnemingen.
Deze feedback vervangt geen nieuwe CAD, print of montagevalidatie.

## Losse mechanische benodigdheden

- Eén bevestigde Ø8 × 8,2-mm motor. Vier draden, windingen eerst doormeten.
- Eén vlakke, braamvrije **M3-sluitring: ID 3,2 / OD 7 / dikte 0,50 mm**.
  Meet de dikte; gebruik geen 0,8/1-mm ring. Een dikkere ring tilt schroef en
  houder tegen de keeper. Geen stapel ringen of geprinte ring als stilzwijgende vervanging.
- **6,5 mm zachte siliconenslang, ID 2,0 / OD 4,0 mm**, voor het Ø2,2-mm
  tandwieltje. Het past tevens over de Ø2,4-mm geprinte aandrijfstift.
- Drie smalle kabelbinders, maximaal 2,5 mm breed; liever herbruikbaar.
  Een smalle strook papier van ongeveer 0,2 mm dik als motorpakking.
- Schuifmaat/liniaal, pincet, klein mesje voor alleen buitenste printbraampjes,
  en verwijderbare markeerstift. Tape om de voet aan de tafel vast te zetten.

**Kale Ø1,5-mm as?** Laat de motor intact. Gebruik voor die asvariant zachte
siliconenslang **ID 1,5 / OD circa 3,5 mm** in plaats van ID 2; proef de rek
over de Ø2,4-mm stift eerst zonder motor. Bevestig alleen als die slang zonder
grote duwkracht op beide zijden past en bij handrotatie niet slipt. Een Ø0,8-mm
as of een ander huis valt buiten deze maatvariant: forceer de standaardkoppeling niet.

## Montagevolgorde

1. **Alles spanningsloos.** Controleer vooral de draadwand, open gaten en
   overbrugde socketbodem. Geen slicersupports verwijderen: die staan uit.
   Eventuele losse brugdraadjes alleen uit het vierkante koppelgat en de
   framezitting halen. **Schuur/snijd de functionele draad niet passend.**
2. Pas de pin/schroef **droog, zonder nieuwe smering**, met de hand. Hergebruik
   gerust een van de drie bestaande 0,175-mm exemplaren; de nieuwe plaat bevat
   een reservepaar. De voet moet 10 × 10 × 2,4 zijn. Geen motorproef bij stroeve
   draad, scheuren of losse draadsecties.
3. Leg één framehelft plat met het splitvlak naar boven. De uitsparing Ø8,5
   onderaan is de motorzitting; Ø3,5 in het lagere dwarsvlak is het glijlager.
   De vierkante geleiding bovenaan is 4,8 × 4,8. Pas de sluitring over de
   Ø3-mm lagerhals: vrij draaien, geen klemmen.
4. Wikkel één dunne papierstrook om het motorhuis (niet om de lagers/as of
   terminals) totdat het zonder radiaal rammelen in de Ø8,5-zitting ligt.
   De motorbodem rust op de 2-mm framevoet; het huis steekt tot Z10,2.
   De laatste 1 mm heeft Ø11,5-mm vrijloop voor de niet volledig bemate frontflens.
   Draai de terminals naar de zijdelingse uitsparing. Houd de draden vrij van
   beide splitvlakken. Niet aan de draadjes trekken om de motor te positioneren.
5. Schuif het slangetje **eerst op de losse geprinte stift**, circa 4,3 mm
   overlap. Laat het 2,2 mm voorbij de stift uitsteken. Leg de houder met
   sluitring in de lagerzitting; de ring ligt tussen framevlak en houderkraag.
   Breng de slang zonder zijdelingse hefboom op het tandwieltje. Ondersteun het
   motorhuis; druk niet hard op het motorlager. Het tandwieltje blijft zitten.
6. Controleer de axiale ruimte. Bij de maatfoto eindigt het tandwieltje rond
   Z14,2; de geprinte stift begint op Z15,2: **ongeveer 1 mm luchtspleet**.
   De slang ligt ongeveer Z13,0–19,5, raakt de lagerbrug op Z20,2 niet en
   staat niet axiaal strak. Werkelijke tandwielhoogte eerst nameten. Motor en
   stift mogen elkaar nergens raken. De last moet via kraag → ring → frame
   lopen, niet via slang of motoras. Stop als dit niet realiseerbaar is.
7. Voor de eerste motortest laat je de pin weg. Plaats de schroefvoet in het
   vierkante gat (10,4 mm) van de houder. Leg de tweede framehelft erop.
   Zet drie kabelbinders in de buitenste groeven bij Z6, 21 en 38. Ze lopen
   rondom de buitenkant, niet door het centrale venster. Trek geleidelijk
   gelijkmatig aan tot de splitvlakken sluiten. Controleer vrij draaien na
   iedere binder; niet het frame krom trekken. Zet de voet met tape vast.
8. Controleer met de hand een volledige draai: motorhuis staat stil, houder
   draait, niets schuurt aan de keeper of kabelbinders. Er is ongeveer
   **0,3 mm opwaartse speling** tussen schroefvoet en keeper. Geen merkbare
   motorasverplaatsing bij zacht axiaal belasten van de schroef.
9. Voer nu de losse-motorcontrole uit volgens `test.md`. Daarna spanning uit,
   bovenste binders openen, tweede helft wegnemen, schroef en pin met de hand
   koppelen en samen in het frame terugleggen. Houd de pin vierkant.
   Stel de neutrale hoogte handmatig in: **bovenzijde pin 7,1 mm boven de
   bovenzijde van het frame/geleideblok**. Dat is Z51,1 boven de onderkant van
   de framevoet, of Z33,1 voor de onderkant van de 18-mm pin.
10. Sluit het frame weer, controleer de volledige **handmatige** veilige slag:
    pin steekt **5,6 tot 8,6 mm** boven het frame uit, of 1 omwenteling totaal.
    Zet terug op 7,1 mm. Markeer middenstand en koppelingshelften. Iedere
    verschuiving/slip/stroomonderbreking maakt de softwarepositie onzeker:
    opnieuw spanningsloos centreren. De grenzen zijn geen homingpunten.

## Wat draagt welke kracht?

De schroefvoet rust in de houder. De houderkraag rust via de metalen ring op
de lagere framebrug; Ø3-mm hals in Ø3,5-mm gat geeft radiale geleiding.
De bovenste brug houdt de schroefvoet tegen oplichten, met 0,3 mm speling.
De slang brengt alleen draaikoppel over en verdraagt kleine uitlijnfouten.
Een ring/glijlager geeft enige extra wrijving: de proef toetst de complete
kleine aandrijving inclusief die wrijving, geen zuivere motorcataloguswaarde.

De nominale CAD is op 41 standen gecontroleerd op botsing. Dat voorspelt geen
printpassing. Een scheef zittende motor, doorhangend koppelgat, te dikke ring
of een slippend slangetje maakt de uitkomst onbeslist over motorkoppel.
**Niet forceren en geen motorlager gebruiken om een verkeerde passing recht te trekken.**
