# E-302 — montage, revisie 2

![Open frame, krachtpad en motorzitting](assembly.png)

Benodigd: bestaande Ø8 × 8,2-mm motor met messing tandwiel, meegeprinte of bestaande E-301
schroef en pin (10 × 10 × 2,4-mm schroefvoet), bestaande vlakke M3-ring
**ID3,2 / OD7 / dikte0,50 mm**, twee elastiekjes en verwijderbare markeerstift.
De plaat bevat twee schroeven, een standaardpin van 18 mm en een pin van 50 mm.
Beide pinnen gebruiken dezelfde schroef en dezelfde onderste 6-mm schroefdraad.
50 mm is de totale pinhoogte, **niet** de bewegingsslag.
Geen tape, lijm, slang, nieuwe elektronica of bewerking van functionele vlakken.
De ring blijft noodzakelijk: een dikkere ring kan de schroef tegen de keeper klemmen.

1. Maak de bestaande opstelling spanningsloos. Neem onderdelen van de afgekoelde
   plaat; herken A aan **één** inkeping in de vierkante kop, N aan **twee**, C
   aan **drie**. N1 en N2 zijn identiek: markeer ze volgens hun plaats op de
   [plaat](plate.png). Inspecteer de twee dunne motorbruggen op losse draden,
   scheuren of doorhang. Laat de dunne 12-mm printvoet aan beide pinnen zitten;
   die blijft onder de geleiding. Afkeur bij functionele nabewerking: niet passend snijden.
2. Probeer N1 eerst **los van het frame** op het tandwiel. Ondersteun het motorhuis,
   verdraai de kop licht om de drie ribben met tandruimtes uit te lijnen en schuif
   hem zonder druk over de tanden. Niet doorduwen naar de bodem. Trek weer recht
   af. Doe dit met N2; zo wordt printvariatie zichtbaar. Bij te strak: probeer C;
   bij vrij ronddraaien: probeer A. Stop als alle varianten klemmen of slippen.
3. Leg één framehelft met open zijde omhoog. Leg de motorbodem op de framevoet
   (Z2); richt het printplaatje naar **de open X-zijkant**, niet naar een veerbrug.
   Het metalen huis raakt de verende bruggen; PCB, soldeerpunten en alle vier
   draden blijven vrij. De uitsparing is 7 mm breed in Y, loopt van Z2 tot Z10,5 en is aan één zijde
   open naar buiten. De twee helften zijn complementair: richt hun uitsparingen
   naar dezelfde zijde. De veren blijven buiten deze uitsparing.
   Dit is een ontwerp-envelope, geen gemeten PCB-maat. Niet passend? Rapporteer
   de botsing; snijd of schuur niets weg en trek niet aan de draden.
4. Plaats de M3-ring over de Ø3-mm lagerhals van de gekozen koppeling. Schuif
   de koppeling voorzichtig over het tandwiel en leg de hals in het lagerdek.
   De ring ligt **boven op het dek**, onder de vierkante houder. Ondersteun het
   motorhuis zodat geen hefboom of merkbare duwkracht op de as ontstaat.
5. Controleer de vrije hoogte voordat het frame sluit. De mond ligt op Z11,2,
   de volledige ribben lopen van **Z11,7 tot Z19,5**; de holte is blind bij Z19,5.
   Meet tandonder- en tandbovenkant ten opzichte van de onderzijde van het frame.
   Vereis minstens **0,6 mm werkelijke overlap van tanden met het rechte ribgebied**
   en minstens **0,5 mm ruimte onder het holtedak**, ook wanneer de schroef licht
   omhoog wordt bewogen. Houd minstens 0,5 mm vrij tussen mond en motorflens/boss.
   De maatfoto geeft alleen totale uitsteking: die bewijst deze voorwaarden niet.
6. Leg de bestaande schroefvoet in de vierkante kop. Plaats de complementaire tweede framehelft, met de uitsparing aan dezelfde zijde,
   en twee elastiekjes in de buitenste groeven bij Z21 en Z38. Ze lopen niet over
   PCB, draden of motorbruggen. De harde splitvlakken sluiten zonder de motor
   axiaal vast te persen. Het huis moet stil blijven bij lichte handrotatie
   van de schroef. Loszitten, kantelen, scheuren of knellen betekent afkeur.
7. Draai spanningsloos één omwenteling voorzichtig. De koppeling moet vrij
   draaien; belast de schroef licht op/neer: de ring en keeper dragen de axiale
   kracht. De motoras mag daarbij niet zichtbaar verplaatsen. Nominale vrije
   keeperhoogte is 0,3 mm en ruimte onder het lagerdek 0,49 mm; echt nameten/voelen.
8. Open opnieuw en monteer de gekozen pin. De veilige proefslag blijft 3 mm:
   bij de **18-mm pin** is de bovenzijde **5,6–8,6 mm boven het frame**, midden 7,1 mm;
   bij de **50-mm pin** is dat **37,6–40,6 mm boven het frame**, midden 39,1 mm.
   Controleer dit eerst met de hand. Geen eindstop opzoeken met de motor.
9. Markeer motorhuis/frame en tandwiel/koppeling met een verwijderbaar lijntje.
   Gebruik uitsluitend de reeds werkende E-301-bediening, zonder firmware-,
   stroom- of snelheidswijzigingen. Doe vijf korte op/neerbewegingen binnen de
   handmatig gecontroleerde slag; stop bij vastlopen, slip of huisbeweging.
10. Spanning uit, open de elastiekjes, neem koppeling en motor uit en herhaal
    montage/demontage drie keer. Test een tweede beschikbare motor met andere
    tandwielhoogte op dezelfde manier. Verplaats de motor niet met vulstukken
    om een niet-passende hoogte kunstmatig passend te maken.

## Axiale tolerantie beoordelen

Bereken bij tandbereik `[onder, boven]` de overlap:
`max(0, min(boven,19,5) − max(onder,11,7))` mm.
Controleer daarnaast dakruimte `19,5 − boven ≥ 0,5 mm`, mond/flensruimte en de
maximale 0,3-mm beweging van de houder. De ribben zijn doorgaand over 7,8 mm,
maar **7,8 mm is geen bewezen toegestane variatie in tandwielhoogte**.
De minimale overlap van 0,6 mm is een voorlopige testgrens, geen berekende koppelgarantie.
Bij onvoldoende overlap: geen motorproef. Noteer de werkelijk gemeten hoogtes.

## De overschuifverbinding en de maatfoto

De foto noemt een tandwiel van Ø2,2 mm met 9 tanden/module 0,2. De koppeling
heeft een Ø2,5-mm vrijloopboring, onderbroken door drie ronde ribben. Het is dus
geen eenvoudige ronde Ø2,5-mm klemhuls. De nominale ribuiteinden liggen op
straal 0,95 / 1,00 / 1,05 mm (A / N / C) en grijpen 0,15 / 0,10 / 0,05 mm
binnen de tandtopcirkel aan. Begin met N; A is de krapste testvariant.

De 4 mm op de foto is de **totale uitsteking boven het huis**, niet de tandlengte.
De foto geeft geen drukhoek of exact tandprofiel. Een controle met een aangenomen
standaardprofiel toont geen nominale botsing, maar bewijst de werkelijke passing niet.
Zie [maatcontrole](dimension-review.json). Alle montage moet zonder forceren kunnen.
