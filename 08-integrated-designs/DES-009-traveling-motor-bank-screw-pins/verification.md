# Controle van de consolidatie

[Terug naar DES-009](DES-009-traveling-motor-bank-screw-pins.md) · [Herkomst](sources.md)

Uitgevoerd op **18 oktober 2026**, tegen repositorybasis `84d265134fcb74266776f9f5d2cb7e0dea60a8ef`. Dit is documentatiecontrole, geen mechanische, elektrische of softwarekwalificatie.

## Resultaten

- ID met `./repo ls DES` gecontroleerd en via `./repo new DES traveling-motor-bank-screw-pins --on E-295 E-301 E-302 E-297` toegewezen. Eén ID-dragend hoofddocument, status `active` voor de gekozen richting.
- Alle 149 relatieve Markdown-links/afbeeldingsverwijzingen in DES-009 en root-AGENTS.md op bestaand doel gecontroleerd; geen ontbrekende doelen. Bestaande actuele CAD, montagebeelden, firmware en 3MF worden alleen gelinkt.
- Alle vier herstelde bestanden opnieuw byte voor byte vergeleken met `git show` van de volledige commit en het oorspronkelijke pad. Daarnaast Git-blob-ID, SHA-256 en bestandsgrootte gecontroleerd tegen [manifest.json](historical/manifest.json). Geen regeneratie of gewijzigde binaries.
- Historische motorfoto, huidige E-301-motorfoto en rechtstreeks opgehaalde vierde Amazonafbeelding zijn byte-identiek. Dit is catalogusherkomst, geen bevestiging van motorpartijmaten.
- Alleen root-AGENTS.md is veranderd onder bestaande getrackte bestanden. E-295/E-297/E-301/E-302, proefresultaten, actuele CAD/binaries en firmware blijven intact. Nieuwe bestanden staan uitsluitend binnen DES-009.
- Inhoud vergeleken met eigenaarresultaten: compacte passing positief; één gemotoriseerde pin positief met geïmproviseerde montage; EN/VIO-problemen en oplopende retourafwijking behouden. E-302-CAD/slicer/software en historische READY-pakketten niet als fysieke passes gepresenteerd.
- DES-009 en AGENTS.md noemen dezelfde gekozen motorbankrichting, voorlopige compacte geometrie, Ø8/5,08-mm conflict, bewezen éénmotorbasis, onbewezen automatische koppeling/parallelbedrijf en voorlopige Pico W/TMC2208-keuze.
- `git diff --cached --check` voor nieuwe documentatie en AGENTS.md: geen whitespacefouten. De volledige staged check meldt zeven bestaande trailing-whitespace-regels in de byte-exact herstelde Trial 5-CAD; die zijn bewust niet gewijzigd. Geen nieuwe CAD, firmware, prototypes, experimenten of issues gemaakt; geen fysieke test uitgevoerd.

## Repositorycheck en grenzen

`./repo check` blijft **niet volledig groen wegens zes bestaande omvangsmeldingen**: E-266, E-283, E-286, E-288, E-293 en `owner-print-tests/AGENTS.md`. De oorspronkelijke basis had daarnaast een omvangsmelding voor root-AGENTS.md; die valt na compacte actualisering weg. Geen nieuwe DES-structuur- of `builds-on`-melding. Historische teksten zijn niet ingekort om deze opdracht groen te maken.

Externe broncontrole: Amazonlisting en vier productbeelden gelezen/geïnspecteerd; officiële ADI-datasheet rev.1.13 opgehaald en relevante secties gecontroleerd. Officiële Raspberry Pi-links gaven HTTP403; versie niet opnieuw vastgesteld. De interne-linkcontrole is geen garantie van blijvende beschikbaarheid van externe URLs. Nieuwe externe PDFs/productbeelden worden wegens niet vastgestelde herdistributietoestemming gelinkt; historische originelen zijn exact bewaard.

Geen passende OEM-motordatasheet, eigenaarsfoto's van beide daadwerkelijke motorvarianten, connectoridentificatie of eigen winding-/asmaten teruggevonden. Dit beperkt de componentidentificatie, niet de geslaagde herstelcontrole van geselecteerde Git-bestanden.
