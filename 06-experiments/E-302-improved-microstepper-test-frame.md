---
status: complete
builds-on: [E-301, E-295]
---

# E-302 — Improved Microstepper Test Frame

Eigenaarsopdracht18 oktober2026; basiscommit0383489 na fast-forward pull.
**Hypothese:** een open PCB-zitting met twee verende huissteunen en een diepe
vrouwelijke koppeling met drie ronde lobben maakt de bestaande aandrijving
zonder snijwerk/tape monteerbaar en verdraagt verschillende tandwielhoogtes.

## Actuele eigenaarfeedback en levering — 19 oktober 2026

De eigenaar heeft revisie 3 geprint: A (één inkeping) te strak, beide N-koppen
(twee inkepingen) kapot, C (drie inkepingen) goed. De kop past door haar lengte
niet samen met de motor in het frame. De horizontale lange schroef printte slecht,
haar supports waren moeilijk te verwijderen en zij werkte niet goed. De korte
schroef is geen probleem. Geen gemeten maten, exacte printinstellingen of
complete geslaagde motor/frameproef gerapporteerd; [volledig verslag](../owner-print-tests/2026-10-18-microstepper-frame-v2/resultaten.md).

Revisie 4: twee identieke C-koppen, 2 mm korter aan het motoruiteinde
(17,6 → 15,6 mm), met behoud van lagerhals, ringvlak en schroefzitting.
Dezelfde lange schroef staat rechtop met twee meegetekende afneembare zijtorens en
vier kleine afbreekcontacten per zijde, 12 mm uit elkaar. Automatische supports
staan uit; alleen dit object heeft een 3-mm brim. Korte schroef, pinnen en
framegeometrie behouden. Eén opnieuw gesliced en heropend X1C/0,4-mm/PLA-project;
13,22 g / circa 4u12m voor de volledige plaat. De nieuwe lengte, tandoverlap,
printstabiliteit en verwijderbaarheid zijn fysiek nog onbekend.

Dit vervangt de printinstructies van revisie 3. De onderstaande levering en
controlegetallen beschrijven de **historische revisies tot 18 oktober**;
actuele controles staan in de [verificatie revisie 4](../owner-print-tests/2026-10-18-microstepper-frame-v2/verification.md).

## Geleverde eindige proef — historie tot 18 oktober


[Printtest](../owner-print-tests/2026-10-18-microstepper-frame-v2/test.md):
één geconfigureerde X1 Carbon/0,4-mm/PLA Bambu3MF, twee complementaire framehelften en vier
koppelingen: drie passingen, nominale tweemaal identiek. Revisie op eigenaarfeedback
bevat één korte en één lange schroef, een18-mm pin en een50-mm pin.
De lange schroef heeft48 mm draad en wordt horizontaal met eigen normale
supports geprint; de andere negen objecten blijven supportvrij. De onderste
6-mm draad blijft gelijk;50 mm is hoogte, niet slag. Hergebruik de0,50-mm sluitring. CAD/STLs, geïllustreerde montage, kort
resultatenformulier en reproduceerbare CAD-/toolpathcontroles meegeleverd.
Herziene slicerplaat14,13 g /4u17m totaal; geen fysieke print gedaan.

## Bewijs en resultaat

- **Eigenaar E-301:** pin bewoog op/neer, uitgesneden zitting onvoldoende stevig,
  ducttape werkte maar was lastig. Dit is bestaand fysiek bewijs, geen E-302-pass.
- **Maatbron:** foto noemtØ2,2/9 tanden/module0,2; geen fysieke meting van motoren.
  PCB/tandlengte/tweede hoogte onbekend. Geen ander motor-PDF-profiel overgenomen.
- **CAD:** één gezamenlijke PCB-uitsparing7 mm breed over volledige huislengte,
  veren erbuiten en extra cilindrische steun behouden; alle10 plaatmeshes gesloten; drie varianten ×25 standen,3-mm pinverplaatsing,
  geen nominale botsing van draaiende houder/lange schroef of50-mm pin met frame;
  werkelijke draadmeshing ook gecontroleerd met bijpassende draairichting. Bewuste verende
  huiscontact-interferentie is afzonderlijk gerapporteerd, niet als passing bewezen.
- **Bambu Studio02.08.02.61:** opgeslagen project zelfstandig heropend en geresliced,
  instellingen gelijk. Alle drie lobben blijven aanwezig op64 rechte boringlagen
  bij alle vier koppelingen in beide slices; centrale radius0,80 mm vrij.
- **Revisieprint:** lange pin417 lagen, bovenbuis gesloten met open kern;
  geen ongeankerde eilanden. Koppelingsmaten getoetst aan foto en expliciet
  aangenomen20° tandprofiel; geen nominale botsing, A marginaal; geen fysieke garantie.
- **Fysiek E-302:** onbekend. Geen claim dat de motor past, tandflanken aangrijpen,
  slip uitblijft of de as onbelast blijft op basis van CAD/slicer.

[Verificatie](../owner-print-tests/2026-10-18-microstepper-frame-v2/verification.md)
en [bronnen/ontwerpgrenzen](../owner-print-tests/2026-10-18-microstepper-frame-v2/sources.md).

## Beslissing en stopconditie

Gereed voor de gevraagde kleine eigenaarstest; geen definitief mechanisch ontwerp.
Handmatig N1/N2 vergelijken, hoogtes en PCB-vrijloop controleren, vijf bestaande
op/neerbewegingen en drie montagecycli. Afkeur bij forceren, druk op PCB/soldeer,
asbelasting, losse motor, blijvende vervorming of slip. Hoogtevariatie zonder
geteste tweede motor blijft onbekend. Werk stopt bij dit gecontroleerde printpakket;
geen firmware/elektronica-, kalibratie-, connector- of meermotoronderzoek gestart.

## Revisie op eigenaarfeedback, 18 oktober

Eerste printpakket vastgelegd in3d554a3. Eigenaar vroeg daarna schroeven en pinnen
op de plaat, inclusief50-mm pin, en een ondubbelzinnige PCB-uitsparing. Deze
revisie vervangt die plaat en handleiding; de oude toestand blijft in Git-historie.
De overschuifmaten zijn expliciet opnieuw gecontroleerd; bronmaten zijn geen
metingen aan individuele motoren. Geen elektronica of firmware gewijzigd.

Revisie3 op vervolgfeedback: lange schroef toegevoegd, horizontale pose met echte
Bambu-supports onder de draad en lokale3-mm brim. Lokale supportinstellingen
blijven na heropening behouden; pinboringen blijven supportvrij. De vraag of
supports zonder draadschade verwijderd kunnen worden is expliciet onderdeel
van de eigenaarstest. Geen50-mm slag geclaimd; frameproef blijft3 mm.

## E-302-softwareplatform — 18 oktober 2026

Aanvullende eigenaarsopdracht op basis van `c1a8a0d`: de bestaande fysieke
E-301-proef bruikbaar maken voor systematische motortests, zonder nieuwe
mechanica of wijziging van historische resultaten. De implementatie staat in
[de softwaremap van deze test](../owner-print-tests/2026-10-18-microstepper-frame-v2/software/handleiding.md).

Geleverd: één zelfstandige MicroPython `main.py`, één-GPIO PIO-UART plus de
bestaande tweepins-UART als fallback, gevalideerde TMC2208-registerconfiguratie,
RPM/rampen/cycli, expliciete pintestgrenzen, desktop-GUI/CLI, lokale profielen,
fail-fast vergelijkingsreeksen en CSV/JSON met gescheiden meetherkomst.
Nieuwe standaardbedrading houdt EN hoog tot configuratie en STEP/DIR vast laag.
Een heartbeat stopt bij verdwenen desktop; volledige UART-uitval heeft zonder
de EN-draad geen gegarandeerde softwarestop. Meerdere drivers gebruiken
onafhankelijke communicatiekanalen, want de TMC2208 heeft vast UART-adres 0.

**Bewijs:** unit-/integratiesimulatie, PIO-instructiecyclusmodel en uitvoering
onder MicroPython 1.26.1 op een host, inclusief float32-variant; details en
reproduceerbare opdrachten in [softwarevalidatie](../owner-print-tests/2026-10-18-microstepper-frame-v2/software/VALIDATION.md).
Geen nieuwe fysieke motor-, elektrische of mechanische test uitgevoerd.
Berekende RPM, fasestroom en positie zijn geen echte metingen. Het doel circa
40 mm in minder dan één seconde blijft een onderzoeksdoel; 50 mm pinlengte
wordt niet als slag aangenomen.

Stopconditie van deze aanvulling: geïntegreerde software, tests en praktische
bedrading/bediening geleverd. Kleinste vervolg is een onbelaste motortest op
lage snelheid, STOP/heartbeat en vergelijking van PIO met hardware-UART;
daarna pas een pintest met zelf vastgestelde bruikbare slag. CAD, STL, 3MF en
E-301-resultaten zijn ongewijzigd.
