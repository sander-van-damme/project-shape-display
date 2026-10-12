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
