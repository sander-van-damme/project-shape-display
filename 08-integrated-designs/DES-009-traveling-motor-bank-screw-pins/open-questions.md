# Open technische vragen

[Terug naar DES-009](DES-009-traveling-motor-bank-screw-pins.md). Deze lijst begrenst wat nog onbekend is; zij start geen experimenten.

| Vraag | Huidige grens / waarom relevant |
|---|---|
| Hoe past de motorbank onder 5,08-mm pitch? | Ø8-mm motoren passen niet naast elkaar op elke pinpositie in één rechte rij. Opstelling, aantal passen, eventuele overbrenging en aantal parallelle kanalen nog kiezen. PCB/kabels/steunen tellen mee. |
| Hoe koppelt de bank automatisch aan en af? | E-301 gebruikte tape; E-302-opsteekkoppelingen zijn CAD/slicerwerk. Tandwielfase, hoogtes van beide motorvarianten, uitlijning, axiale bewegingsruimte en slip onbekend. |
| Hoe blijven schroef en pin ondersteund en op hoogte na vertrek? | Zelfremming, backdrive, axiale lagering en loskoppelkrachten niet gemeten. Voeg niet ongemerkt complexe onderdelen per pin toe. |
| Hoe bewegen meerdere pinnen zonder buren te verstoren? | Compact handcontact en één motor/pin zijn positief; automatisch selecteren, bankverplaatsing en simultane bediening fysiek onbewezen. |
| Wat is de echte motorprestatie? | Exact model, staphoek, beide windingweerstanden, stroom, koppel, snelheid, temperatuur en veilige duty nog niet aan de voorraad gekarakteriseerd. Verkoperwaarden zijn geen metingen. |
| Waar komt de afwijkende retourpositie vandaan? | Kwalitatief stapelende afwijking bij E-301; tijdplanning, klokaanname, gemiste stappen, loslaten en koppeling zijn mogelijke bijdragen, geen diagnoses. Volledige kalibratiestudie is nu geen voorwaarde. |
| Werkt het herziene frame en de lange schroef fysiek? | Motor-PCB-zitting, tandwielhoogtes, koppeling, verwijderen van supports zonder draadschade en bruikbare slag onbekend. 50 mm pinlengte is geen 50 mm verplaatsing. |
| Welke elektronica schaalt naar een bank? | Pico W/TMC2208 is de testbasis; kanaalaantal, afzonderlijke UART-kanalen (vast adres 0), enable, voeding, lage-stroomkwaliteit en bedrading nog bepalen. E-302-hosttests bewijzen geen hardware. |
| Welk exact motorstekkertje is gebruikt? | Eigenaar meldt kleine vierpolige connector; familie, steek en pinvolgorde niet bevestigd. Verkoperskleurentabel bevat een fout; windingparen niet gokken. |
| Blijft dit goedkoop, maakbaar en speelbaar? | Printvoetjes lastig te verwijderen; batchspreiding, slijtage en belasting onbekend. Echte miniatuurvoeten, dunne wanden, terreinondersteuning en speelbare overgangstijd moeten nog samen blijken. |

[Concrete bewijsbasis](experiments.md) · [Componenten](components.md) · [Elektronica](electronics.md)
