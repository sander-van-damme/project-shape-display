---
status: active
builds-on: [E-295, E-301, E-302, E-297]
---

# DES-009 — Verplaatsbare motorbank met compacte schroefpinnen

**Gekozen ontwikkelingsrichting, 18 oktober 2026; geen bewezen eindontwerp.** Dit dossier is het primaire vertrekpunt voor de huidige Shape Display-architectuur. Een verplaatsbare bank met individueel aangestuurde kleine stappenmotoren bedient de schroeven onder een vast pinnenraster. De positieve fysieke basis is **één microstappenmotor die één compacte schroefpin op en neer bewoog** (E-301). De volledige motorbank, automatische koppeling, passief hoogtebehoud en parallelle werking zijn nog niet fysiek bewezen.

Consolidatie van repositorybasis `84d265134fcb74266776f9f5d2cb7e0dea60a8ef`, inclusief de recente E-302-softwareaanvulling. `active` betekent gekozen richting, niet fysieke kwalificatie. E-297 in `builds-on` verwijst naar relevante lessen uit een historisch alternatief, niet naar een overgenomen rij-/kolomkoppeling.

## Leesroute

| Document | Gebruik |
|---|---|
| [Componenten en motoridentificatie](components.md) | Compacte geometrie, motorvarianten, bronkwaliteit en tegenstrijdigheden |
| [Elektronica en bestaande software](electronics.md) | Werkende E-301-bedrading, nieuwe E-302-variant, officiële datasheets en registers |
| [Experimenten en fysieke resultaten](experiments.md) | Wat werkelijk gebeurde op 15–18 oktober; directe links naar CAD, montage, afbeeldingen en 3MF |
| [Open technische vragen](open-questions.md) | Beperkte lijst van nog onbewezen onderdelen |
| [Bestanden en herkomst](sources.md) | Actuele originelen, herstel uit Git, externe bronnen en ontbrekende gegevens |
| [Controle van dit dossier](verification.md) | Linkcontrole, bronvergelijking en behoud van oorspronkelijke bestanden |

## Werking en mechanische grens

1. De motorbank verplaatst zich onder het raster naar de te bedienen pinnen. Bankgeleiding, indexering en opstelling van de motoren zijn nog niet gekozen.
2. Elke betrokken motor maakt een **verwijderbare koppelverbinding** met een resident aanwezige schroef. De motoren kunnen afzonderlijk starten, stoppen en omkeren; meerdere motoren kunnen potentieel parallel werken.
3. De schroef roteert en beweegt een geleid, **niet-roterend** staafje via diens binnendraad omhoog of omlaag. De geleiding neemt het reactiekoppel op. Schroeflagering en axiale ondersteuning blijven bij het raster.
4. Na loskoppelen blijven pin en schroef bij hun rasterpositie; de motorbank gaat verder. Het ontwerp moet de ingestelde hoogte zonder aanwezige motor kunnen behouden. **Zelfremming of een bruikbare eenvoudige houdvoorziening is niet aangetoond.** De motoras mag niet stilzwijgend de blijvende pinlast dragen.

Dit is de bedoelde werkcyclus, niet een reeds uitgevoerde cyclus. E-301 gebruikte een blijvende geïmproviseerde tapeverbinding. E-302 levert een handmatig te monteren opsteekkoppeling; ook die bewijst geen automatische koppeling van een reizende bank.

## Besluiten en voorlopige basis

| Besluit | Betekenis en grens |
|---|---|
| Verplaatsbare motorbank is de actieve richting | Nieuwe ontwikkeling bouwt hierop voort tenzij bewijs of een expliciete eigenaarsbeslissing heroverweging rechtvaardigt. Geen nieuwe architectuurwedstrijd nodig. |
| Eenvoudige, goedkope pinnen en schroeven | Beperk mechanische onderdelen die per pin duizenden keren terugkomen; tel ook bank, ondersteuning, montage, bekabeling en reparatie mee. |
| Voorlopig 4,4-mm vierkante pinnen op 5,08-mm pitch | Bestaande compacte schroefgeometrie uit E-295; vijf pitches per 25,4-mm spelvak. Geen vrijgave voor grote arrays. |
| Schroef nominale Ø3,2 mm, spoed 3 mm; 6 mm binnendraad | De drie korte nominale paren met 0,175-mm radiale CAD-relief liepen handmatig soepel. Relief is geen gemeten speling of productiegarantie. |
| Pico W + TMC2208 zijn de huidige testbasis | Fysieke E-301-proef ondersteunt die combinatie; toekomstige elektronica voor de volledige bank is niet definitief vastgelegd. |
| Historische rij-/kolomkoppelingen zijn referenties | E-297 en DES-001 t/m DES-008 blijven behouden. Hun oude aanbevelingen/statussen vormen geen actieve vervolgopdracht voor DES-009. |
| D&D-speelbaarheid blijft beslissend | Eén-inch spelvakken, dunne wanden en ruimte voor echte miniaturen; eenvoud en kosten tellen voor het hele mechanisme. |

### De motorbank past nog niet vanzelf op het raster

Het huidige motorhuis is volgens de maatbron **Ø8 mm**, tegenover **5,08 mm pinpitch**. Eén rechtopstaande motor recht onder elke opeenvolgende pin in één rechte rij zou nominaal **2,92 mm overlappen**, nog zonder PCB, houder, kabels of koppeling. Een dergelijke bank mag niet als bestaand ontwerp worden getekend of begroot.

Verspringende motorposities, meerdere passen of een korte overbrenging zijn denkbare oplossingsklassen, **geen gekozen uitvoering**. De bankindeling moet motorruimte, toegang tot de schroeven, ontkoppelen, blijvende ondersteuning en het gewenste aantal parallelle kanalen samen oplossen. Het dossier voert hiervoor geen nieuwe uitgebreide architectuurstudie uit.

## Stand van het bewijs

| Bewijsklasse | Wat bekend is | Wat daar niet uit volgt |
|---|---|---|
| **Fysiek, eigenaar 15 oktober** | Vijf compacte schroef-pinparen maken elk vijf handcycli; drie nominale 0,175-mm-paren voelen “supersoepel”. | Geen gemeten kracht, zelfremming, lange slag of onafhankelijke array. |
| **Fysiek, eigenaar 18 oktober / E-301** | Pico W + TMC2208 laten één schroefpin op/neer bewegen bij Vref circa 0,80 V, instelling S 100; EN aan GND, VIO na herstel 3,3 V. | S 100 is geen gemeten 100 rpm. Geen kwantitatief koppel, duurproef, exacte slag of meermotorbewijs. |
| **Fysieke beperkingen E-301** | Motorvak moest worden bijgesneden, ducttape koppelde de as; retourafwijking stapelde bij de losse motor. | Geen bewezen passende oorspronkelijke houder, reproduceerbare koppeling of nauwkeurige positionering. Oorzaak retourfout onbekend. |
| **CAD/slicer E-302** | Herzien frame, koppelingen, korte/lange schroef, 18-/50-mm pin en geconfigureerde 3MF bestaan. | Geen fysieke passing; 50 mm pinhoogte en 48 mm lange schroefdraad zijn geen bewezen slag. Frameproef blijft 3 mm. |
| **Software E-302** | Geïntegreerd testplatform, PIO-UART en desktop; hosttests en MicroPython-hostvalidatie gedocumenteerd. | Geen nieuwe fysieke Pico-, PIO-, stop- of motorbanktest. |
| **Ontwerpkeuze DES-009** | Motoren worden gedeeld via een verplaatsbare bank. | Geen gekwalificeerde bank, automatische koppeling, parallelle beweging of onbeïnvloede buurpinnen. |

De [experimentenkaart](experiments.md) geeft de exacte dossiers. Oudere teksten die vóór een eigenaarupdate zijn geschreven blijven historisch correct voor hun datum; het latere expliciete resultatenverslag bepaalt de actuele bewijsstatus.

## Productgrenzen en werkafspraak

De [missie](../../01-project-description/shape-display-mission.md) en [prototypeprioriteiten van 14 oktober](../../02-design-criteria/current-prototype-priorities.md) blijven van kracht voor speelbaarheid, zuinig leren en onafhankelijk op/neer bewegen. Hun nog open architectuurkeuze wordt voor de huidige richting ingevuld door deze eigenaarsbeslissing. De vroegere circa 400 × 400 mm, 6.400 pinnen, 40 mm nuttige hoogte, 30 seconden en $500 zijn vergelijkingswaarden, geen hier bewezen prestaties.

Een 5,08-mm pitch alleen lost dunne wanden en vrije doorgang voor miniatuurvoeten niet op. Hoogtebehoud, werkelijke slag, buurbeweging, snelheid, belastbaarheid en kosten blijven open. Uitgebreide optische meting, perfecte kalibratie en automatische recovery zijn geen zelfstandige huidige prioriteit.

**Stopconditie van deze opdracht:** dit navigeerbare dossier en bijgewerkte root-AGENTS.md. Geen nieuwe CAD, prototypes, firmware, fysieke experimenten of GitHub-issues; bestaande bestanden worden gelinkt en relevante verdwenen referenties exact hersteld. De open vragen zijn geen automatisch te starten takenlijst.
