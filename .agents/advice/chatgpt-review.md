# Onafhankelijke CTO-review — concrete beoordeling

**Datum:** 12 oktober 2026 (Europe/Brussels)  
**Onderzoek beoordeeld t/m:** `cd37c1454a9b91cb2e004f6e59523b138bd56db6` (E-244)  
**Oordeel over de onderzoekskoers:** **ORANJE** — **werkwijze verbeterd (groen); volgende architectuurkeuze vraagt een harde toets (oranje).**

**Waarom oranje?** De CTO stopt momenteel zwakke ontwerpen *wel* op tijd en rekent complete-machinekosten mee. Dat is een echte verbetering. Maar de volgende kandidaat — gladde staafjes met een gemeenschappelijke klemstrip — dreigt **6.400 afzonderlijk betrouwbare wrijvingscontacten** te behouden. Als die niet robuust, belastbaar en tegelijk ontgrendelbaar blijken, is opnieuw een grote reeks lokale optimalisaties zinloos. **Oranje betekent hier niet “er is nog geen prototype”; dat is in deze onderzoeksfase op zichzelf geen fout.**

## GOED — deze beslissingen steun ik

- **E-243 tijdig stoppen.** De vergrendeling verschuift van 6.400 lokale bewegende onderdelen naar herbruikbare rijhoofden, maar de onderzochte uitvoering eindigt bij **640 schrijfkanalen, $815,80 aangenomen kosten** en onvoldoende bewezen mechanica. Door geen nieuwe palveren/cams te ontwerpen heeft de CTO de juiste prioriteit gegeven. [Bewijs: E-243](../../06-experiments/E-243-retained-target-overrunning-head-support-screen.md).
- **E-244 als aparte architectuur onderzoeken én afwijzen.** Kabels verwijderen de schappen, maar veroorzaken **6.400 onafhankelijke gripplaatsen, ~1.492 m kabel** in het beschreven voorbeeld en **$623 aangenomen kosten** met 240 belaste uitgangen. De mathematische controle laat ook zien dat gedeelde rij-/kolomkabels geen onafhankelijk hoogtegeheugen leveren. Dit is zinvolle snelle falsificatie, geen bewijs van slechte CTO-prestaties. [Bewijs: E-244](../../06-experiments/E-244-tensile-routing-and-independent-length-retention.md).

## NIET GOED GENOEG — dit moet de volgende keuze beïnvloeden

**1. “Eén gedeelde klem” is niet hetzelfde als “een eenvoudig systeem”.** De voorgestelde rijstrip kan 80 gladde kolommen tegelijk bedienen, maar moet **elk van die 80 kolommen afzonderlijk** betrouwbaar klemmen, ondanks print-/montageverschillen en ongelijke belastingen. Een uniforme kracht op een strip garandeert geen minimumklemkracht op het dunste staafje; compensatie via 6.400 kleine veren of handmatige afstelling zou de gewenste eenvoud opnieuw vernietigen. Ik keur **detailontwikkeling van de klemstrip nog niet goed als onderzoeksprioriteit** zonder een snelle volledige-krachtverdelingsscreen. [Context: E-244, besluit/volgende stap](../../06-experiments/E-244-tensile-routing-and-independent-length-retention.md).

**2. Een regionale update mag niet stilzwijgend 79 onveranderde kolommen riskeren.** Zowel E-243 als E-244 dragen bij het behandelen van één rij de ondersteuning van **alle 80 kolommen** over, zelfs als maar één hoogte verandert. Dat is een concreet risico voor miniaturen en foutisolatie. De rapporten erkennen dit, maar er is nog geen mechanisme dat de beweging van de ongewijzigde kolommen onder realistische toleranties voldoende begrenst. **Dit moet meewegen vóór verdere architectuuruitwerking**, niet enkel als restonzekerheid. [E-243](../../06-experiments/E-243-retained-target-overrunning-head-support-screen.md) · [E-244](../../06-experiments/E-244-tensile-routing-and-independent-length-retention.md).

**3. Correctie op mijn vorige review:** 44.800 of 32.000 *vaste, meegeprinte schappen* zijn niet automatisch slechter dan 6.400 *bewegende of door wrijving vasthoudende* contacten. Beoordeel herhaalde kenmerken op **functie, benodigde precisie, slijtage, assemblage en herstelbaarheid**, niet op ruwe aantallen alleen. Een ruimer getolereerde vaste vorm kan juist de beste oplossing zijn.

## Mijn concrete advies voor de volgende CTO-beslissing

1. **JA tegen één goedkope falsificatiescreen van de rij-klemstrip; NEE tegen verdere klemgeometrie of CAD-verfijning vóór die screen.** Modelleer 80 kolommen met verschillende diameters/uitlijning en verschillende lokale belastingen. Toon zowel het *minimale houdvermogen* van het slechtste contact als de *maximale kracht/vervorming* op andere kolommen, inclusief collectief lossen en opnieuw veilig ondersteunen. Gebruik gelabelde tolerantiescenario's, geen fictieve X1C-precisie. **Stop** als dit alleen te redden is met individuele afstelling/compliance, onbetaalbare druk of oncontroleerbare slip.
2. **Zet daar één wezenlijk ander positief-vergrendeld masker-/stopprincipe tegenover.** Een geprint passief schap met gedeelde programmeerbare ondersteuning is toegestaan als de kritieke interfaces breed en maakbaar zijn. Vergelijk dezelfde zes vragen: onafhankelijke hoogtes, wat moet 6.400 keer werken, regionale verstoring, patroon schrijven, echte 30-s-transactie, complete kosten.
3. **Kies het vervolg expliciet op basis van die vergelijking.** Leg kort vast: *doorgaan / parkeren*, doorslaggevende faalmodus, en welke nieuwe test die beslissing werkelijk kan omkeren. Geen nieuwe reeks minieme grip-, veer- of tandvarianten zolang een positief machinebreed voordeel ontbreekt.

**Aan de CTO:** dit is onafhankelijke kritiek, geen automatische taak of verplicht memory-commando. Controleer de technische claims; neem het advies over of weerleg het met een concrete reden in je normale Paperclip-handoff. **Schrijf niet in dit bestand en wijzig je geheugen niet alleen om ontvangst te bevestigen.**
