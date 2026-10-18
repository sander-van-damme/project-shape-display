---
status: complete
builds-on: [E-301, E-295]
---

# E-302 — Improved Microstepper Test Frame

Eigenaarsopdracht18 oktober2026; basiscommit0383489 na fast-forward pull.
**Hypothese:** een open PCB-zitting met twee verende huissteunen en een diepe
vrouwelijke koppeling met drie ronde lobben maakt de bestaande aandrijving
zonder snijwerk/tape monteerbaar en verdraagt verschillende tandwielhoogtes.

## Geleverde eindige proef

[Printtest](../owner-print-tests/2026-10-18-microstepper-frame-v2/test.md):
één geconfigureerde X1 Carbon/0,4-mm/PLA Bambu3MF, twee framehelften en vier
koppelingen: drie passingen, nominale tweemaal identiek. Hergebruik bestaande
schroef, pin en0,50-mm sluitring. CAD/STLs, geïllustreerde montage, kort
resultatenformulier en reproduceerbare CAD-/toolpathcontroles meegeleverd.
Slicer oorspronkelijk11,88 g /3u26m totaal; geen fysieke print gedaan.

## Bewijs en resultaat

- **Eigenaar E-301:** pin bewoog op/neer, uitgesneden zitting onvoldoende stevig,
  ducttape werkte maar was lastig. Dit is bestaand fysiek bewijs, geen E-302-pass.
- **Maatbron:** foto noemtØ2,2/9 tanden/module0,2; geen fysieke meting van motoren.
  PCB/tandlengte/tweede hoogte onbekend. Geen ander motor-PDF-profiel overgenomen.
- **CAD:** alle meshes gesloten; drie varianten ×25 standen,3-mm pinverplaatsing,
  geen nominale botsing van draaiende houder/schroef met frame. Bewuste verende
  huiscontact-interferentie is afzonderlijk gerapporteerd, niet als passing bewezen.
- **Bambu Studio02.08.02.61:** opgeslagen project zelfstandig heropend en geresliced,
  instellingen gelijk. Alle drie lobben blijven aanwezig op64 rechte boringlagen
  bij alle vier koppelingen in beide slices; centrale radius0,80 mm vrij.
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
