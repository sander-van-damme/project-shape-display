# Feedback van Sander op lopend onderzoek

Dit bestand is een eenvoudige inbox voor feedback van Sander aan de CTO. Lees nieuwe opmerkingen mee met de overige bestanden in `.agents/advice/` en beoordeel ze op een passend moment. Het zijn observaties en suggesties, niet automatisch bewezen onderzoeksresultaten of verplichte nieuwe taken.

**Opruimregel (toestemming van Sander):** zodra de CTO een feedbackpunt inhoudelijk heeft verwerkt, of er daadwerkelijk mee aan de slag is gegaan en het eventuele vervolg elders heeft vastgelegd, mag hij **dat afgehandelde punt uit dit bestand verwijderen**. Laat nog niet opgepakte feedback staan. De Gitgeschiedenis blijft beschikbaar. Deze toestemming geldt alleen voor dit feedbackbestand, niet voor andere bestanden in `.agents/advice/`.

---

## 13 oktober 2026 — Feedback op S40-calibration-STL en toekomstige staafjesprints

**Huidig S40-testbestand:** Sander heeft `owner-print-tests/supported-s40/s40-calibration.stl` bekeken en **gaat deze versie niet printen**. Er zijn geen meegeleverde supportstructuren in de STL. Voor zulke lange en fijne onderdelen verwacht hij een degelijker print- en supportontwerp; alleen achteraf supports in de slicer toevoegen overtuigt hem voor deze proef niet.

**Printoriëntatie en stabiliteit:** zeer fijne, hoge staafjes gaan bij rechtop printen gemakkelijk wiebelen, met risico op mislukte of onnauwkeurige prints. Sander heeft daarom een **voorkeur voor liggend printen**. Onderzoek welke oriëntatie voor het gekozen onderdeel daadwerkelijk het betrouwbaarst is, rekening houdend met supportverwijdering en maatkritische of schroefdraadoppervlakken.

**Batchprint en gezamenlijke ondersteuning:** bij een groot aantal staafjes is het interessant om die netjes naast elkaar te leggen en met tijdelijke, eenvoudig te verwijderen supports of onderlinge verbindingen te ondersteunen. Zo kunnen de onderdelen elkaar tijdens het printen meer stabiliteit geven. Onderzoek dit als maakbaarheidsprincipe, niet alleen als eenmalige slicerinstelling.

**Variatie tussen identieke objecten:** neem bij een nuttige toekomstige proef bij voorkeur **enkele identieke staafjes op dezelfde printplaat** op, in plaats van slechts één exemplaar. Sander wil kunnen bekijken hoeveel de feitelijke dikte, rechtheid en passing per printobject verschillen, ondanks identieke CAD-geometrie. Houd testopzet en meetwijze eenvoudig; één kleine batch bewijst nog geen opbrengst of betrouwbaarheid op displayschaal.

**Verzoek aan CTO:** neem deze printpraktijk en de vraag naar natuurlijke object-tot-objectvariatie mee bij de beoordeling van huidige en toekomstige fysieke proeven. Bepaal zelf of en wanneer een herwerkte, werkelijk printvriendelijke proef zinvol is. **Deze feedback is geen opdracht om nu de bestaande STL, testdocumentatie of andere bestanden te wijzigen**, en er is geen deadline of verwachting dat Sander onmiddellijk gaat printen.
