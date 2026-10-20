# E-302 v3 — gecorrigeerde motorinterface, variant L

**Status: READY — digitaal gecontroleerd; fysieke passing nog niet getest.**
20 oktober2026. Alleen voor **L: A≈2,0 / B≈3,25 mm boven het metalen huis**.
Gebruik de kortere K niet voor deze uitvoering. Geen printdeadline.

Open [microstepper-frame-v3.3mf](microstepper-frame-v3.3mf) in Bambu Studio.
Printer, materiaal, proces, oriëntatie en lokale rotorbrim zijn opgeslagen;
het project is zelfstandig heropend en opnieuw gesliced.

| Onderdeel | Aantal |
|---|---:|
| Stijve framehelften, pennen/gaten | elk1 |
| Geïntegreerde ronde rotor met C-koppeling en originele draad | 1 |
| Bestaande18-mm pin | 1 |
| Spacers0,60 /0,72 /0,84 | 1 /2 /1 |

Hergebruik bestaande ring ID3,2/OD7/0,50, motor L en elastieken. Huis9,2 mm hoog,
nieuwe zittingØ8,4. Ruimte voor PCB, variabele lijm en omhooglopende kabels.
Ring/rotor0,7 mm hoger met circa1-mm draagdek; C-inloop0,25 voor meer rechte
riboverlap. Bewezen radiale C-vorm, draadspoed3 en proefslag3 behouden.

![Gecorrigeerde montage](images/cad.png)

**Bambu Studio02.08.02.61; X1 Carbon/0,4-mm nozzle; Generic PLA / Textured PEI.**
Schatting **2u58m23 /10,20g**. Geen fysieke printmeting.
Laag/eerste laag0,12; Arachne,2 wanden, nominale lijn0,45;100% zigzag-infill.
Nozzle220°C, bed55°C. Buitenwand/kleine omtrek/eerste laag/brug15mm/s,
binnenwand20; acceleratie default/binnen1000, buiten/eerste500mm/s².
Supports uit, raft0, per laag. Alleen rotor buitenbrim2mm met gap0,12.
XY/gat/elephant-footcompensatie0; fan100% na eerste laag, hulpfan0,
minimum laagtijd8s. Geen automatische heroriëntatie/herschikking.

Framehelften op vlakke buitenzijde, uitsparingen omhoog; rotor rechtop met mond
op bed; pin op bestaande vierkante printvoet; spacers vlak. Vier spacers op de
plaat van links naar rechts0,60 /0,72 /0,72 /0,84. Modelbereik67×54×28mm.

Volg de [montagehandleiding](assembly.md): eerst spanningsloos passen, kabels in
buitenste kanaal, ring vlak,360° handrotatie en volledige3-mm slag. Pas daarna
vijf korte op/neercycli met bestaande bediening. Stop bij klemmen, open naad,
PCB-/kabeldruk, asbeweging of slip. Noteer alleen waarnemingen in [resultaten](resultaten.md).

[Maattabel, maatketen en verificatie](verification.md). READY is digitale
printvrijgave voor deze kleine proef, geen bewezen mechanische betrouwbaarheid.

`cad/`: parametrische bron; `components/`: actuele STLs; `scripts/`: generatie,
CAD-/slicecontrole; `metadata/`: bronnen, instellingen en rapporten; `images/`:
montage en banen. `components/archive/2026-10-19/` bevat oude meshes en3MF;
`metadata/archive/` oudere controles. Gebruik die oude plaat niet meer.

Stop na deze gerichte correctie; geen nieuw mechanisme, elektronica of motorbankonderzoek.
