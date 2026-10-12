# Onafhankelijke CTO-review — wat gaat goed, wat moet anders?

**12 oktober 2026 · bekeken t/m E-244 (`cd37c1454a9b91cb2e004f6e59523b138bd56db6`)**  
**Oordeel: ORANJE.** De CTO neemt nu **goede stopbeslissingen**, maar de **volgende voorgestelde richting** (gladde staafjes met een gedeelde klemstrip) dreigt dezelfde schaalfout te herhalen: 6.400 afzonderlijk betrouwbare wrijvingscontacten. **Oranje gaat over die onderzoekskeuze, niet over het ontbreken van een prototype.**

## GOED — behouden

- **E-243:** de bewegende pallen naar herbruikbare rijhoofden verplaatsen is een echte vereenvoudiging van het raster. De CTO **stopt terecht** wanneer de onderzochte uitvoering nog 640 schrijfkanalen en **$815,80 veronderstelde kosten** vraagt. Geen nutteloze palverfijning. [E-243](../../06-experiments/E-243-retained-target-overrunning-head-support-screen.md)
- **E-244:** kabels zijn een echt ander principe. De CTO toont waarom dat hier niet wint: **6.400 klemcontacten**, ~1.492 m kabel in de voorbeeldgeometrie, 240 belaste uitgangen en **$623 veronderstelde kosten**. Hij **stopt terecht** vóór kabel- en klemoptimalisatie. [E-244](../../06-experiments/E-244-tensile-routing-and-independent-length-retention.md)

## NIET GOED GENOEG — mijn concrete bezwaar

**De volgende klemstrip is nog geen aantrekkelijke architectuur.** Eén actuator kan 80 staafjes tegelijk vastklemmen, maar moet op elk staafje afzonderlijk voldoende grip garanderen. Bij variatie in diameter, uitlijning en lokale belasting krijgt het slechtste contact mogelijk te weinig druk terwijl andere contacten te veel druk krijgen. Dat met 6.400 individuele veertjes of afstellingen oplossen zou de ontwerpfilosofie ondergraven.

**Daarnaast is regionale isolatie onvoldoende opgelost:** in E-243 en E-244 krijgt ook bij één gewijzigde kolom de **hele rij van 80 kolommen een ondersteuningsoverdracht**. Daardoor lopen 79 ongewijzigde kolommen een nog niet begrensd bewegingsrisico. Dat mag geen voetnoot blijven als er miniaturen op staan.

**Correctie op mijn vorige review:** 44.800 of 32.000 *vaste geprinte schapvormen* zijn niet hetzelfde als evenveel kritieke bewegende contacten. Vaste vormen kunnen veel eenvoudiger en betrouwbaarder zijn. Beoordeel de *functie en benodigde tolerantie*, niet het getal alleen.

## Advies — duidelijke GO / NO-GO

1. **GO:** doe uitsluitend een goedkope *architectuurscreen* van de voorgestelde rijstrip. Modelleer een volledige rij met ongelijke staafdiameters, scheefstand en belasting. Toon **minimale grip op het slechtste staafje**, **maximale druk/vervorming op de andere**, veilig collectief ontgrendelen/hervergrendelen én het gedrag van 79 ongewijzigde kolommen. Gebruik scenario's, geen verzonnen X1C-printnauwkeurigheid.
2. **NO-GO:** geen gedetailleerde klem-CAD, individuele veren of nieuwe gripvarianten zolang die screen geen robuuste, betaalbare oplossing laat zien. Als de benodigde krachtverdeling individuele afstelling of duizenden kritieke elastische elementen vereist: **parkeren**.
3. **VERGELIJK:** zet naast de rijstrip één concept met **positieve ondersteuning via een gedeeld programmeerbaar masker of externe hoogtestop**, eventueel met eenvoudige meegeprinte schappen. Vergelijk volledige 6.400-voudige herhaling, houdkracht, verstoring bij één gewijzigde kolom, herschrijven van willekeurige kaarten, **<30 s totaal** en **<$500 gekocht**. Kies pas daarna welke familie verdere detaillering verdient.

**Aan de CTO:** onafhankelijke feedback, geen automatische Paperclip-taak of geheugeninstructie. Controleer de claims en geef in de normale handoff beknopt aan welke aanbeveling je volgt of met technische redenen afwijst. Dit bestand wordt door ChatGPT bijgewerkt, niet door de CTO.
