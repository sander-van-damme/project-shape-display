---
status: complete
builds-on: [E-281, E-277]
---

# E-295 — compacte schroefstaafjes en gedeelde schroefaandrijving

**Opdracht en datum:** eigenaargerichte ontwikkeling, 15 oktober 2026. Uitgangspunt: actuele `main`, commit `117549a74448259f6691f74cf7a0bd6f8a25395b`. Het vaste principe blijft een roterende schroef met een geleid, niet-roterend hol staafje met korte binnendraad. Dit pakket bevat CAD, slicercontrole, berekeningen en onderzoeksbronnen; **geen nieuwe fysieke succesclaim**.

**Aanbeveling:** onderzoek de compacte passing eerst met één kleine plaat. De uitgewerkte vierpins-proef toetst daarna één verwijderbare aandrijfkop onder het raster. Voor een groter display is een **verplaatsbare bank van enkele individueel aankoppelbare schroefkoppen** de belangrijkste gedeelde uitbreiding. Zo worden selectie, uitlijning en eventuele koppelbegrenzing enkele keren gebouwd, terwijl iedere terreinpin eenvoudig blijft. Een enkele XY-kop is een geloofwaardig begin voor onafhankelijke beweging en lokale wijzigingen, maar geen snelle schrijver van duizenden willekeurige hoogtes. Volledig globale initialisatie blijft een alternatief waarvoor veilige slip in iedere aangesloten krachttak nodig is.

## Voor Sander: wat eerst printen

1. **Eerst alleen [compact-five-pairs.stl](../owner-print-tests/2026-10-15-compact-screw-fit/compact-five-pairs.stl)** — de [korte instructies en het resultatenformulier](../owner-print-tests/2026-10-15-compact-screw-fit/test.md) zijn leidend. Vijf schroeven en vijf 4,4-mm staafjes; radiale spelingen 0,15 / 0,175 / 0,20 mm, met drie exemplaren van 0,175. Geleverde oriëntatie behouden, supports uit, externe voeten zijn al ontworpen. Circa 42 minuten / 3,2 g PLA in het vastgelegde vergelijkingsprofiel, geen gemeten X1C-tijd.
2. **Daarna eventueel [vierpins-demonstratie](../owner-print-tests/2026-10-15-four-pin-screw-demo/test.md)**, status DEFERRED tot een compacte passing bruikbaar blijkt. Complete STL-platen voor de drie spelingen zijn inbegrepen; kies precies één passende variant. Eén handkop selecteert vier aangrenzende schroeven op 5,08 mm pitch, met op/neerbeweging en werkelijke verhoogde middenstand. Er hoeft niets gecompileerd te worden.

Er is één actieve READY-printproef, geen groeiende printwachtrij en geen deadline. Slecht passende of beschadigde onderdelen niet met een tang, boormachine of schuren passend maken: juist die uitkomst bepaalt de volgende ontwerpkeuze.

## Wat de ontwikkeling concreet verbetert

De nieuwe compacte proef behoudt het **3,2-mm buitendraadprofiel met 3-mm spoed, 0,9-mm diepte en 90° profielhoek** uit de recent soepel bevonden proef. Het wordt niet proportioneel verkleind. De brede moer van 10,3 mm wordt vervangen door een **4,4-mm vierkant hol lichaam**: 57% smaller. Alleen de onderste 6 mm is geschroefd; daarboven ligt een 3,52-mm vierkante holte. De wand bij de diepste draadgroef is nominaal 0,45 / 0,425 / 0,40 mm voor de drie spelingen.

Het concept combineert dus het recente profiel met de compacte bouwvorm uit Trial 5. De veranderingen in wandstijfheid, kortere inschakeling en printoriëntatie maken een nieuwe fysieke proef noodzakelijk. **Minder materiaal, passende CAD-afmetingen en gecontroleerde toolpaths zijn aangetoond; betere fysieke soepelheid dan de brede paren is nog niet aangetoond.**

De externe dunne printvoeten verankeren de korte holle staafjes zonder materiaal in de binnendraad. De onafhankelijke slicercontrole vindt kleine lokale materiaalonderbrekingen bij de overgang naar de dunne draadwand; alle nieuwe laagcomponenten overlappen de vorige laag. Deze kwetsbare plekken moeten fysiek worden bekeken, naast passing en soepelheid. Het rapport vergelijkt rechtop en liggend printen; een liggende functionele draad zou hier steuncontact en nabewerking toevoegen. Dit rechtvaardigt uitsluitend de kleine korte proef, geen ongestutte 50-mm productiepin. De demonstratie gebruikt een op zijn zij geprinte geleidekooi en controleerbare korte bruggen.

## Bewijs en herkomst

- **Fysieke eigenaarobservaties:** de vijf recente brede paren maakten elk vijf cycli zonder schade/nabewerking; 0,20 mm voelde het soepelst. Historisch zijn er positieve ervaringen met smalle Trial 5-pinnen. Geen gekalibreerd koppel, snelheid of productieopbrengst.
- **Historische CAD:** commit `41484f9` bevat 4,4-mm lichamen, 0,44-mm wand en 10-mm onderdraad. De werkelijk succesvolle variant en BOSL2-versie zijn onbekend; `$slop=0.65` is niet blind overgenomen.
- **Ongeldige passingtest:** de verkorte replica had supports in de binnendraad. Dat is geen bewijs tegen compacte schroeven.
- **Nieuwe resultaten:** gesloten CAD-meshes, botsingsberekeningen en echte slicerpaden. Passing, hechting, sterkte en buurvrijloop blijven fysiek onbekend. Handmatig koppelen bewijst nog geen automatische uitlijning.
- **Aandrijfstudie:** technische bronnen en reproduceerbare scenario's, geen gemeten machinesnelheden of leveranciersgaranties.

Details: [compacte geometrie](../tools/curated-experiment-checks/E-295/research/compact-geometry.md), [onafhankelijke review](../tools/curated-experiment-checks/E-295/research/independent-review.md), [bestaande fysieke resultaten](../owner-print-tests/2026-10-14-short-thread-fit/test.md). Historische experimenten zijn niet herschreven.

## Aandrijvingen op systeemniveau

| Kandidaat | Selectie en herhaalde onderdelen | Beoordeling |
|---|---|---|
| Eén XY-kop onder het veld | Positie + intrekbare hexkop; eenvoudige integrale tip per schroef, geen resident koppeling. | Beste eerste demonstratie. Uitlijning, fasezoeken en seriële tijd blijven bepalend. |
| Meerdere XY-koppen | Zelfde passieve pin; meer koppen/motoren in eigen werkgebieden. | Helpt verspreide wijzigingen. Kosten, grensbotsingen en ongelijke werklast tellen mee. |
| Reizende bank, gedeelde rotatiemotor | Bankpositie kiest groep; iedere kop schuift zelfstandig in/uit. Slechts `k` selectoren/begrenzers. | Sterkste gedeelde uitbreiding; stoppen/vrijgave en fijnmazige kopmechaniek nog onbewezen. |
| Vaste rijassen of rij/kolomselectie | Tot 6.400 mechanische koppelingen, naven en retourfuncties onder de pinnen. | Minder motoren, maar veel kritische onderdelen en montage. Lagere prioriteit. |
| Reizende riem of tandlat als schroeftransmissie | Contact kiest rij/groep; omkeren geeft op/neer. Individuele selectie blijft nodig. | Slechts 0,68 mm tussen Ø4,4-mm flenzen; druk, retourloop en vrijgave zijn knelpunten. |
| Volledig globale bus/reset | Alle aangesloten schroeven; veilige reset vraagt lokale slip in iedere krachttak. | Centrale motorbegrenzer beschermt een geblokkeerde tak niet. Gezamenlijk draaien is geen homing. |
| Magnetische/Jacquardachtige selectie | Magneten of selectiefuncties bij iedere pin, tenzij meegenomen op een bank. | Relevante inspiratie; nog geen bewijs van eenvoud of buurvrijloop op 5,08 mm. |

Krachtroutes, steunvlakken, toleranties, motorverdeling en kleine falsificatieproeven staan in [XY-aandrijving](../tools/curated-experiment-checks/E-295/research/xy-drive.md) en [gedeelde/globale aandrijving](../tools/curated-experiment-checks/E-295/research/shared-global-drive.md). Primaire bronnen omvatten schroefautomaten, boorkoppen, printerkoppelingen, schroefvijzels, Jacquardselectie en slipbegrenzers. Hun functies zijn relevant; catalogusmaten worden niet als passende 5-mm onderdelen voorgesteld.

### Waarom een hybride zinvol kan zijn

Een kleine bank kan groepen tijdens voorbereiding naar een onderniveau brengen en daarna naar bijvoorbeeld +20 mm neutraal. Een gerichte kop of selectieve bankpass stelt uitzonderingen en latere lokale wijzigingen in. Dat spaart werk als veel terrein op een gemeenschappelijk niveau blijft. Het bespaart niets wanneer dezelfde scène onnodig opnieuw wordt genuld: een bekend bestaand terrein rechtstreeks aanpassen kan sneller zijn. Dezelfde eenvoudige schroeven kunnen voor beide werkwijzen worden gebruikt; de resetvoorziening moet tijdens lokale updates volledig vrij zijn.

Veilige reset vereist per aangesloten tak een aantoonbaar venster **normaal loopkoppel < slipkoppel < schadelijk stopkoppel**, én weer omhoog kunnen komen na stoppen. Verschillende starthoogtes maken onafhankelijke slip noodzakelijk. Een 80-kops bank houdt die last bij 80 bereikbare modules; een wereldwijde koppeling vraagt 6.400 gelijktijdige contactfuncties. Geen reset tegen vastgelopen draad of bijna uitgeschroefde moeren is voorgesteld.

## Realistische tijd- en kostenvergelijking

De [reproduceerbare systeemstudie](../tools/curated-experiment-checks/E-295/research/hybrid-systems.md) onderscheidt volledige scènes, lokale veranderingen en neutraalvoorbereiding. De onderstaande **synthetische scenario's zijn geen gemeten D&D-gebruik of machinesnelheid**. Planningsaannames: spoed 3 mm, 600 rpm, XY 150 mm/s met 1.500 mm/s², 0,75 s volledige aankoppel-/ontkoppelhandeling, motorversnelling en verwachte herpogingen. De bankwaarden tellen stoppen van de gedeelde motor, afzonderlijk terugtrekken en opnieuw starten bij iedere verschillende doelhoogte. Tegengestelde richtingen krijgen afzonderlijke aankoppelpasses. De selectie zelf is nog onbewezen; continu loslaten zonder eerst te stoppen is alleen een apart optimistisch scenario.

| Wijziging | Eén XY-kop | Vier zelfstandige XY-gebieden | Bank met 16 koppen |
|---|---:|---:|---:|
| 25 pinnen in één compacte patch | 32 s | 32 s | circa 20 s |
| 25 pinnen verspreid | 52 s | 19 s | circa 52 s |
| 100 pinnen in één patch | 127 s | 127 s | circa 55 s |
| Volledige willekeurige scène, 6.400 wijzigingen | 161 min | 41 min | circa 64 min |

De 30-secondenreferentie is nuttig om wachttijd zichtbaar te maken. Zij sluit een langzamere maar bruikbare scènevoorbereiding niet vooraf uit. Omgekeerd mogen gunstige lokale voorbeelden een urenlange volledige scène niet verhullen. Een 80-kops bank zou met veilige gestopte vrijgave onder deze aannames circa 38 minuten vragen en introduceert bovendien de nog onbewezen dichte kopmechaniek. Het snellere continue-vrijgavemodel vraagt gekwalificeerde timing: 50 ms ongecompenseerde vrijgave bij 600 rpm is al 1,5 mm extra verplaatsing. Die winst wordt dus niet als bewezen mogelijkheid ingeboekt. Een geheel globale reset van circa 10 seconden is slechts een procesondergrens met 6.400 gelijktijdig werkende veilige koppelingen, geen aanbevolen productprestatie. Zie de bronstudie voor gewijzigde bankoverhead, gevoeligheden en afzonderlijke homingtijden.

Voor 6.400 cellen liggen de voorlopige **ontwerpbudgetten, geen offertes**, op circa $365–876 voor één XY-systeem, $713–1.692 voor vier zelfstandige koppen en $540–1.385 voor een 16-kops bank; inclusief geraamd pinfilament, zonder arbeid, belasting/verzending en onvoorziene ontwikkeling. Goedkope componentkeuzes zijn nog geen werkende BOM. Per extra $0,10 per pin komt $640 erbij; per extra tien seconden montage komt 17,8 uur erbij. Zelfs twintig seconden per compleet paar betekent 35,6 uur voor 6.400 paren, exclusief het frame. Dit maakt eenvoudige, batchgewijs assembleerbare pinnen veel belangrijker dan alleen het aantal motoren.

## Speeloppervlak en mechanische grenzen

[Het gedimensioneerde bovenaanzicht en de doorsnede](../tools/curated-experiment-checks/E-295/research/playable-envelope.md) behouden vijf pinnen per D&D-vak. 80×80 op 5,08 mm is 406,4×406,4 mm; het is geen exact 400-mm veld. Een 4,88-mm top zou de naad tot 0,20 mm verkleinen, maar past niet automatisch bij de toegestane verdraaiing en zijwaartse speling. De demonstratie houdt daarom 4,4-mm vierkante toppen; een vrijwel doorlopend eindoppervlak is een expliciete resterende ontwerpbeslissing.

Een 0,8-mm muur op de vakgrenzen laat 24,6 mm vrije corridorbreedte. Dat past niet automatisch rond een 25-mm miniatuurbasis. Werkelijke bases en plaatsingsmarge moeten worden gecontroleerd. Voor deze fase ligt een losse muur met voet boven het terrein, en wordt verwijderd vóór beweging van de pinnen onder die voet. De wand steekt niet door een te smalle pinnaad en kan de onderliggende kop niet blokkeren.

## Welke fysieke uitkomst beslist wat?

| Waarneming | Ontwerpbeslissing |
|---|---|
| Nominale compacte exemplaren allemaal soepel, intact en zonder draadnabewerking | De compacte schroefgeometrie is een bruikbare basis voor de vierpins-proef; nog geen productiekwalificatie. |
| Alleen ruime variant werkt, of nominale exemplaren verschillen sterk | Passing/wand en printspreiding eerst begrijpen; niet automatisch 0,20 mm als productiespeling kiezen. |
| Vierpins-proef beweegt individueel in beide richtingen, buren blijven staan | Onderkoppeling en gedeelde geleiding zijn fysiek aannemelijk; volgende keuze kan een motorische kop of kleine gedeelde bank zijn. |
| Koppeling grijpt vaak mis, of socket/keeper vervormt | Koppeling/herbruikbare kop verbeteren; geen bewijs tegen het schroef-staafprincipe. |
| Pin zakt/roteert na ontkoppelen onder lichte praktische last | Vasthouden is nog onvoldoende; historisch positief handgevoel vervangt deze meting niet. Een hoge spoed is niet automatisch zelfremmend. |
| Normaal loopkoppel en veilig slip-/losbreekkoppel zijn duidelijk gescheiden | Kopbegrensde groepsreset wordt interessant. Zonder dit venster geen automatische reset vrijgeven. |

De eigenaar kan de volgende richting kiezen op basis van printspreiding, merkbare weerstand/speling, buurbeweging, supportverwijdering, koppeling en vasthouden. Er wordt geen vervolgonderzoek, aankoop of nieuwe printketen automatisch gestart. De opdracht stopt bij dit samenhangende pakket en de pull request.

## Verificatie en reproduceerbaarheid

- Volledige bronnen en gebruiksinstructies staan naast de geleverde STL's in `owner-print-tests/`.
- Compacte CAD: tien gesloten lichamen; 305 nominale montagestanden zonder volumetrische botsing; verkeerde draairichting levert botsing als negatieve controle. De geometriecontrole meet geen wrijving.
- De [onafhankelijke review](../tools/curated-experiment-checks/E-295/research/independent-review.md) documenteert exacte STL-hashes, gebruikte slicer/profielen, wandpaden, laagondersteuning, bruggen en resterende onzekerheden. PrusaSlicer is een expliciete vergelijking, geen nagebootste Bambu Studio-validatie.
- [XY-geometriescript](../tools/curated-experiment-checks/E-295/research/xy_geometry.py), [timing/kostenscript](../tools/curated-experiment-checks/E-295/hybrid_timing_cost.py) en [vlak/doorsnedebron](../tools/curated-experiment-checks/E-295/playable_envelope.py) behouden aannames en reproduceerbare resultaten.
