# Onafhankelijke ChatGPT-review — eerst een speelbare kaart, daarna mechanica

**12 oktober 2026 · beoordeeld t/m E-254 (`208c134ac99834bb42d8a1a63ec561af65359147`)**  
**Oordeel: ORANJE — één belangrijke ontwerpkeuze is nog te eng onderzocht.** De CTO heeft een transparante, reproduceerbare kaartanalyse gemaakt. De fysieke terreinvorm én de *mechanische rusthoogte* moeten echter vanuit het perspectief van spelers worden gekozen vóór architectuurselectie. De correctie is concreet: onderzoek een verhoogde neutralestand en coarser grid, niet alleen andere maskers en koppen.

## GOED

- **E-254** telt expliciet het aantal aangeraakte rijen, in plaats van te veronderstellen dat weinig verhoogde staafjes automatisch korte wachttijden betekenen: de ruïnes verhogen 13,55% van de kolommen maar raken 74/80 rijen. De CTO vermeldt terecht dat zijn drie bronkaarten en de gekozen hoogtes geen representatieve speldata zijn. [E-254](../../06-experiments/E-254-sourced-gameplay-occupancy-and-service-comparison.md)
- De herontdekking van de door Sander eerder fysiek uitgeprobeerde **schroefstaafjes** is een nuttige onderzoekspiste. De houdproef is positieve, maar niet gekwantificeerde, gebruikerservaring. [Notities van Sander](sander-ideas.md)

## NIET GOED GENOEG — expliciete correctie van mijn eerdere analyse

**Een numeriek correcte hoogtekaart is niet vanzelf een goede D&D-speelkaart.** De **69,52% verhoogde kolommen bij Riverside Road** zijn grotendeels grond die 10 mm wordt opgetild om water lager te tonen; bij de ravijnkaart is dat vergelijkbaar. **De bomen zijn hier niet als hoogte geïnterpreteerd**: E-254 liet vegetatie en kleine decoratie juist weg. De alternatieve vlakke rivier vereist slechts **2,77%** verhoogde kolommen. Die cijfers hangen dus sterk af van een nog niet door spelers gekozen visualisatiestrategie. Mijn vorige review nam de percentages en tijdconclusies te gemakkelijk over zonder te vragen of spelers het resultaat zo willen zien. **Dat was onvoldoende kritisch.**

**Mijn vorige review miste nog een derde mogelijkheid, en dat is een wezenlijke fout in mijn eigen kritiek:** hetzelfde relatieve rivierprofiel kan worden behouden door gewone grond op een verhoogde **neutrale/middenstand** te plaatsen, vervolgens **1.951 watercellen (30,48%) te verlagen**, **4.272 grondcellen te laten staan** en **177 rotscellen (2,77%) te verhogen**. Dat is niet hetzelfde als de rivier vlak tekenen. Het vereist echte neerwaartse verplaatsing, mogelijk langere staafjes, veilige ondersteuning en reële initiele ruststandtijd. Ook kunnen vele rijen nog bezocht worden. De exacte E-254-hoogtetabel bewijst alleen de rekenkundige mogelijkheid, niet de machine. **De CTO mag dus niet automatisch aannemen dat de pinnen op minimale hoogte rusten.**

Even belangrijk: **~5,08 mm / ~6.400 pinnen en ~$500 zijn referentiedoelen**, niet het enige acceptabele ontwerp. Een grove kwart-square 6,35-mm-granulariteit met minder onderdelen of een echt leuke premium uitvoering kan meer waarde leveren. Alleen de werkelijke D&D-ervaring kan dat onderscheid rechtvaardigen.

De CTO mag E-254 bewaren als scenario, maar **niet als definitieve workload of spelvereiste** gebruiken voordat de fysieke versus visuele terreinvorm, mechanische hoogte-nulstand en gekozen pitch bewust zijn vergeleken. Een massieve pinmuur waar eigenlijk bomen staan zou slecht zijn; een echte klif mag juist veel fysieke hoogte rechtvaardigen. Projectie/props zijn opties, geen gratis bewezen oplossing.

## Concreet GO / NO-GO

1. **GO — vergelijk drie échte fysieke mogelijkheden voor de rivier:** (A) minimumstand en 69,52% optillen, (B) verhoogde neutralestand en ongeveer 30,5% water omlaag plus 2,8% rotsen omhoog, en (C) overwegend vlakke visuele rivier. Laat de speelbare vorm zien, niet alleen een histogram. Voor een ravijn zijn echte negatieve hoogtes extra relevant; controleer miniaturen, diepte, zichtbaarheid en wandvormen.
2. **NO-GO — geen architectuurselectie uit één aanname over rusthoogte of rasterdichtheid.** Vergelijk 5,08-mm-pitch met een speelbare coarser 6,35-mm-grid en kosten/betrouwbaarheid van minder herhaalde onderdelen. E-254 blijft historisch correct onder zijn aannames; niet elk oud numeriek criterium is een definitieve productspecificatie.
3. **VERGELIJK OPNIEUW —** tel opstaande, afdalende, onveranderde cellen en werkelijk bezochte rijen per *speelbare variant*, inclusief initiële positionering op neutraal. Screen bidirectionele schroefkoppen, gedeelde aandrijving en relevante alternatieven op volledige tijd/kost/veiligheid. **Minder pinnen, andere hoogte-nulstand of iets meer geld zijn mogelijk betere UX-keuzes**, mits bewust onderbouwd.

**CTO:** controleer deze kritiek zelf; je blijft technisch verantwoordelijk. Dit bestand is extern advies, geen geheugeninstructie of vervanging van een Paperclip-taak.

---

## 14 oktober 2026 — nieuw advies: fail forward met een kleine fysieke printproef

**Nieuw verzoek van Sander:** de CTO mag nu **proactief één kleine, daadwerkelijk printklare prototype-/tolerantieproef klaarzetten**, zodat Sander kan testen zodra hij tijd heeft. Het doel is **vroeg leren met weinig filament**, niet een volledige machine of dure printcampagne maken. Dit is geen printdeadline, aankooptoestemming of bewijs van werking. De CTO blijft eigenaar van de geometrie, de technische keuze, de afkeurcriteria en het moment van handoff.

### GOED

1. De CTO trok de oorspronkelijke ongeschikt ondersteunde S40-proef terecht in toen Sander de slanke printdelen en supports bekritiseerde. De oude STL mag niet simpelweg opnieuw als READY worden aangeboden. [E-263](../../06-experiments/E-263-supported-s40-screw-calibration-article.md) · [ingetrokken opdracht](../../owner-print-tests/supported-s40/test.md).
2. Recente analyses maken de vraag voor een gerichte proef concreet: E-277 onderzoekt een open kanaal, een intacte schroefmoer en draadprofielen; E-279 vergelijkt werkelijke slicerpaden van lange schroeven met uiteenlopende oriëntatie/ondersteuning. **Fysieke passing, laag-op-laagvariatie, stabiliteit tijdens printen en schade bij supportverwijdering zijn daarmee nog niet gemeten.** [E-277](../../06-experiments/E-277-integral-coarse-column-guidance-envelope.md) · [E-279](../../06-experiments/E-279-long-screw-batch-deposition-and-release.md).

### NIET GOED

De [printtestmap](../../owner-print-tests/AGENTS.md) bevat nog **geen READY proef**. E-279 stelt terecht vast dat geen van de huidige volledige schroefroutes al klaar is voor een onbewezen lange prototypeprint. Dat mag echter **niet** betekenen dat zelfs een zorgvuldig ontworpen *klein, representatief tolerantietestje* eindeloos op nieuwe simulaties moet wachten. Sliceranalyses kunnen niet waarnemen of twee echte FDM-delen soepel passen of beschadigen. **Fail forward: maak een zo klein mogelijk fysiek falsifieerbaar experiment, niet blind een fragiel lang model.**

### VOLGENDE GO/NO-GO voor de CTO

1. **GO: één kleine P1-testplaat voorbereiden.** Kies de meest informatieve deelvraag van de bestaande staaf/schroef/geleiding (bijvoorbeeld korte functionele schroef-moer-passingen, of alleen indien noodzakelijk een verantwoord ondersteunde langere stabiliteitsproef). De CTO kiest na vergelijking met de bestaande CAD/slicerdata de kleinste test die een beslissing kan wijzigen. Lever onder [owner-print-tests/](../../owner-print-tests/AGENTS.md) **complete ready-to-slice \`.stl\`-bestanden** met duidelijke onderdeel-/variantnamen, de ingevulde [resultatenfiche](../../owner-print-tests/TEST-TEMPLATE.md), exacte aantallen, materiaal, oriëntatie, supports, eenvoudige teststappen en een geschatte filamenthoeveelheid/printtijd. **NO-GO: niet READY verklaren** wanneer de mesh, printsteun, verwijderbaarheid of functionele montage niet voldoende onderbouwd is. Geen SCAD/Python-compileerwerk voor Sander. Maximaal drie READY plaatjes totaal; liever één.
2. **GO: kleine tolerantiesweep met natuurlijke spreiding.** Bijvoorbeeld 2–3 door de CTO gekozen, betekenisvolle spelings-/draadvarianten, aangevuld met minstens twee identieke exemplaren van de nominale versie; varianten duidelijk labelen en slim op één plaat groeperen. Geen grote matrix en geen materiaalverspilling. Laat Sander eenvoudig *printbaarheid, passing, draait/beweegt, wrijving/vastlopen, hoogtehouden bij een lichte miniatuurbelasting (als relevant), supportschade en eventuele nabewerking* aanduiden. **NO-GO voor een variant** wanneer normale montage herhaaldelijk forceren, schade of individueel schuren vereist. Een geslaagd exemplaar bewijst geen hoge yield bij duizenden staven.
3. **Na resultaten: bijsturen of stoppen.** Meet of noteer per variant wat werkelijk gebeurd is, vergelijk met de vooraf bepaalde hypotheses en verbeter één gericht ontwerpdetail of verwerp de richting. Zet verouderde tests op DEFERRED/RETIRED en ruim achterhaalde STL's op. **Sander kan pas veel later of nooit printen**: geen termijn, reminders of stilvallen van de rest van het CTO-onderzoek.

**Koersbijstelling tegenover eerdere review:** het stopzetten van de slecht voorbereide S40-print was juist; **nu is een veilig, minimaal fysiek leerexperiment actiever waard om voor te bereiden**. Dit advies schrijft geen mechanisme voor, verandert geen ontwerpcriteria en vraagt geen wijzigingen aan CTO-memory, prompts, Paperclip of issues.

