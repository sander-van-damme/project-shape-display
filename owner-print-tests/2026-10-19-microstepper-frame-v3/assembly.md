# Montage — E-302 v3

![Doorsnede en krachtpad](images/assembly.svg)

Benodigd: bestaande motor, **bestaande vlakke M3-ring ID3,2 / OD7 / 0,50 mm**,
twee elastiekjes en de nieuwe geprinte delen. Geen lijm, schroeven of veren.
Een bestaande goede 18-mm pin kan de meegeprinte pin vervangen. De oude losse
schroef/koppeling en oude framehelften worden niet gebruikt.

1. **Spanning uit.** Verwijder alleen de buitenbrim van de rotor. Laat de dunne
   vierkante printvoet van de pin zitten: die roteert niet en blijft onder de geleiding.
   Controleer de open tandwielholte en beide pinboringen op draadjes; geen
   functionele vlakken passend snijden. Draai schroef en pin eerst los met de hand.
2. Pas de lege helften. De twee Ø3-pennen gaan in een rond Ø3,5-gat en een
   4,2 × 3,5-langwerpig gat. Beide splitvlakken moeten volledig sluiten. De
   penpunten zijn afgeschuind, de gatdiepte 3,2 bij penlengte 2,8. Niet forceren.
3. Leg de motor op de bodemsteun Z2, met **PCB, soldeerpunten en vier draden
   naar de open −X-zijde**. De opening is 7 mm breed, Z2–10,5: een ontwerp-envelop,
   geen gemeten PCB-maat. Controleer ook de huisflens en de boss onder het tandwiel.
   Het metalen huis hoort in de stijve Ø8,2-zitting; alleen het huis mag contact maken.
4. Begin zonder spacer. Zit het huis los, leg **één** spacer in het rechthoekige
   vak aan de tegenoverliggende +X-zijde: de 2 × 5-mm strook tegen het metaal,
   het brede tabje bovenaan naar buiten. Begin 0,60 → 0,72 → 0,84 mm; gebruik de
   dunste waarbij de motor niet beweegt en de helften volledig sluiten. Niet stapelen.
   Het tabje ligt in zijn eigen uitsparing, buiten de harde splitvlakken. Het is
   geen veer. Verwijder het met de hand wanneer het frame open is.
   Op de plaat liggen de vier spacers **van links naar rechts: 0,60 / 0,72 / 0,72 / 0,84**;
   merk de tabjes bij afnemen met een pen. De twee 0,72-exemplaren zijn identiek.
5. Leg de ring in de ronde Ø7,3-uitsparing boven het motorvak. Schuif de rotor
   voorzichtig op het tandwiel, licht verdraaiend om de drie C-ribben te laten
   aangrijpen. **De vlakke rotoronderkant rust op de ring**, niet op motor, boss
   of tandwiel. Controleer de onderstaande hoogtematen voordat je sluit.
6. Sluit de tweede helft en plaats de elastiekjes in de buitenste groeven bij
   Z15 en Z35. Houd kabels buiten de naad. Draai de rotor een volle omwenteling:
   geen schuren of blokkeren. Nominale radiale speling 0,20 mm; axiale oplichting
   maximaal 0,30 mm tot de bovenste aanslag. Bij licht op/neer belasten hoort de
   motoras niet zichtbaar mee te bewegen. Controleer dat de motor ook niet draait
   of kantelt. Open en herstel de montage bij een afwijking.
7. Open opnieuw, schroef de pin op en leg de vierkante pin in de geleiding.
   Sluit. De **pinbovenkant staat 5,2–8,2 mm boven het 40-mm frame**; midden 6,7 mm.
   Controleer deze volledige 3-mm slag eerst handmatig. De printvoet raakt de
   aanslag of geleiding niet; er blijft nominale volledige 6-mm draadaangrijping.
8. Pas daarna met de **reeds werkende bediening en instellingen** vijf korte
   op/neercycli binnen die gecontroleerde slag. Geen eindstop opzoeken. Stop bij
   vastlopen, slip, motorbeweging, asbelasting, scheurvorming of druk op PCB/draden.
   Noteer waarnemingen in [resultaten.md](resultaten.md); demonteer en hermonteer
   desgewenst driemaal om de uitlijning te beoordelen.

## Werkelijke tandoverlap — vóór motorbedrijf

Meet tandonderkant **b** en tandbovenkant **t** vanaf de onderzijde van het frame.
De 4 mm uit de oude maatfoto is de totale uitsteking boven het motorhuis,
**niet** de tandlengte. De tweede motorvariant is niet opgemeten.

- Rotor op ring: mond **12,2**, rechte ribben **12,7–18,2**, holtedak **18,2 mm**.
- Bij volledig optillen: ribben **13,0–18,5 mm**. Vereis aan beide uiteinden van
  de axiale speling minstens **0,6 mm rechte overlap**:
  `min(max(0,min(t,18.2)-max(b,12.7)), max(0,min(t,18.5)-max(b,13.0))) ≥ 0.6`.
- Dakruimte in de laagste stand: **18,2 − t ≥ 0,5 mm**. Geen contact met boss,
  flens of motorhuis; controleer minstens 0,5 mm mond/bossruimte. Ook het Ø4-gat
  onder de ring moet vrij blijven van boss/as en de ring moet vlak liggen.
- Foto-afgeleide tandtop Z14,2 zou maximaal 1,2 mm overlap bij optillen geven,
  **alleen als de werkelijke tandonderkant laag genoeg ligt**. Dit vervangt de
  eerdere maximale 0,2 mm bij de ingekorte koppeling en 0,3-mm oplichting.
  Het is geen meting of koppelgarantie; 0,6 mm blijft een voorlopige testgrens.

Bij onvoldoende overlap, dakruimte of vrije motoras: **geen bewegingstest**.
Geen vulstuk onder de motor gebruiken om de onbekende hoogte te verbergen.
