# Printtest — één ondersteunde S40-schroef

**Status:** READY  
**Prioriteit:** P1  
**Laatst beoordeeld:** 2026-10-13  
**Reden:** één ondersteund artikel kan ontbrekende gegevens over bewegen, vasthouden en stijfheid leveren.  
**Technische bron:** [E-263](../../06-experiments/E-263-supported-s40-screw-calibration-article.md), [CAD/controles](../../tools/curated-experiment-checks/E-263/).

Volledig vrijblijvend: geen deadline, aankoop of herinnering. Je hoeft geen CAD te compileren. Niet printen blokkeert ander onderzoek niet. Dit is nieuwe geometrie; je eerdere positieve houdproef én gemelde breuk blijven afzonderlijke waarnemingen.

## 1. Waarom deze test? — CTO

**Vraag:** beweegt één intacte, ondersteunde schroef in beide richtingen, houdt hij een lichte miniatuur vast en helpt een tweede onderste radiale steun?

**Waarom fysiek:** printvariatie, kromming, wrijving en stijfheid bepalen of snelheidsmodellen bruikbaar zijn. Goed resultaat kan later een ondersteunde aandrijfproef rechtvaardigen; stroef lopen, zakken of veel paswerk verzwakt die route. Deze proef kent geen motor-RPM toe.

**Stop:** buiging, scheur, openende framenaden, kantelende last, vastlopen of spontaan zakken. Niet forceren, schuren, uitboren of een reeks pasvarianten maken. Geen beschadigde oude schroef gebruiken.

## 2. Printklaar — CTO

| STL in deze map | Inhoud |
|---|---|
| `s40-calibration.stl` | één plaat, acht losse delen: 2 framehelften, schroef/handwiel, pin/laadplateau, 2 halve uitneembare steunplaten, 2 kleine uitlijnsleutels |

- **Instellingen:** bestaand PLA, X1C,0,4-mm nozzle,0,12-mm lagen,100% schaal; geen XY/passingcorrectie.3 wanden/20% infill frame; overige delen volledig vullen waar ruimte is. Controleer in slicer dat de0,44-mm buiswand wordt geprint. Brim circa3 mm waar nodig.
- **Oriëntatie:** meegeleverd, niet automatisch draaien. Framehelften met delingsvlak op bed; kleine uitsparingen overbruggen maximaal4,8 mm. Handwiel op bed. **Pin ondersteboven op zijn28-mm plateau.**
- **Supports:** alleen extern onder de8-mm stopschouder bovenaan de pin:1,8-mm overhang, circa84 mm hoog. Tree-support vanaf bed buiten het plateau, naar binnen vertakkend; nooit in draad/buis. Voorzichtig verwijderen terwijl je de schouder vasthoudt. Lukt slicing/verwijdering niet zonder buigen: stoppen, geen pascampagne.
- **Raming:**3–5 uur,40–65 g inclusief supports; geen slicerwaarden. Noteer eigen waarden.
- **Benodigd:** aanwezige tape, liniaal, eventueel telefoon/weegschaal en lichte miniatuur. Niets kopen.
- **CTO-controle 13 oktober:** finale binaire STL heropend; acht gescheiden waterdichte solids, correcte oriëntatie, bezette afmetingen224×116,2×86 mm binnen256-mm bed.252 nominale posities gecontroleerd; assemblage en finale STL visueel bekeken. Nog niet gesliced/geprint; fysieke passing onbekend.
- **Veilig:** langzaam met de hand, lage tafel en opvangbak/doos. Niet op plateau drukken; geen kilogram-, breuk-, motor- of boormachineproef.

## 3. Test — CTO

1. **Montage zonder last.** Draai pin voorzichtig op de nieuwe schroef, ongeveer tot middenstand. Leg één framehelft plat met open kant omhoog. Leg handwiel tussen de onderste twee vlakken, as in rond hoofdlager en pin in beide vierkante geleidingen. Plaats beide sleutels in hun pockets en beide losse steunhelften in de onderste sleuven. Sluit tweede framehelft met vlakke buitenranden; tape elke zijstijl op twee hoogtes dicht, vrij van bewegende delen. Tape losse steunhelften tegen uitschuiven. Vereist sluiten duwen/buigen/fijn uitlijnen: stoppen. Handwiel moet vrij kunnen draaien.
2. **Slag/uitlijning.** Rechtop: `h` is afstand onderkant plateau tot bovenkant bovenste geleiding; ontwerp0–40 mm, neutraal20. Zoek onbelast voorzichtig beide einden: plateau raakt bovenste geleiding bij0; onderste pinschouder raakt onderste geleiding bij40. Stop bij **eerste contact**, nooit doordraaien. Daarna20→5→35→20: tel draaien, noteer kijk-/draairichting. Ontwerplead3 mm/omwenteling. Film langzaam naast vaste liniaal: slingeren, kromming, schuren, naden/framebeweging?
3. **Omkeren/vasthouden.** Rond20: één draai op en terug; noteer hoogtes en draaihoek zonder zichtbare beweging na omkeren. Plaats daarna een gewogen lichte miniatuur stabiel centraal: **maximaal10 g totale externe last**, voorzichtige proefgrens, geen rating. Onbekend/zwaarder/instabiel: overslaan. Laat handen en handwiel helemaal los. Lees h bij0/60/600 s rond20 mm, en0/60 s rond5 en35. Eén pin draagt hier de volle miniatuur; op een bord kan die verdeeld zijn.
4. **Relatieve stijfheid/service.** Verwijder last. Bij5/20/35: heel lichte zijwaartse aanraking en loslaten; film plateau, as bij hoofdlager, frame/naden afzonderlijk. Herhaal zonder de twee losse onderste steunhelften; hoofdlager en thrustvlakken blijven dicht. Zonder bekende gelijke kracht is dit **kwalitatief**, geen N/mm. Noteer eventuele gemeten kracht/verplaatsing en resolutie. Open tenslotte onbelast het frame en vervang hetzelfde intacte paar; noteer tijd, moeite en schade.

**Aparte stresslast, optioneel:** alleen na stabiele miniatuurproef, aanwezig gewogen voorwerp, totaal maximaal10 g extern, rond20 mm in opvangbak. Apart registreren; nooit ophogen tot falen. Overslaan als het geen zinvolle vergelijking geeft.

**Succes:** eenvoudige montage/vervanging, gemeten signed slag, stabiele vrijgelaten last binnen afleesresolutie, geen binding/buiging. Onzichtbare drift is niet nul; gevoelde weerstand is geen koppelmeting. Geen bord-, duur- of snelheidskwalificatie. Het brede proefplateau past niet op bordpitch;50-mm variant blijft uitgesteld. Later motorwerk vereist ondersteunde aandrijving en gemeten compliance/runout.

## 4. Mijn resultaten — Sander

**Datum / printer / filament / laag / compensaties:** …  
**Print:** [ ] ja [ ] deels [ ] nee [ ] nog niet geprint  
**Sliceruren / gram / werkelijke printuren:** …  
**Supportverwijdering / montage / uitnemen-terugplaatsen (min):** …  
**Mislukte delen / paswerk / schade / stopreden:** …

| Meting | Waarde, eenheid of observatie |
|---|---|
| h-einden / slag / kijk- en draairichting / aantal draaien | … |
| h vóór, na één draai, na terugdraai / omkeerhoek / speling | … |
| Miniatuur + houder (g) / weegschaalstap | … |
| h bij20:0/60/600 s; bij5 en35:0/60 s | … |
| Handen geheel los / andere steun / afleesresolutie/parallax | … |
| Met tweede steun: beweging plateau/as/frame bij5/20/35 | … |
| Zonder tweede steun: idem / verschil draaigemak | … |
| Kracht onbekend of gemeten + meetwijze / verplaatsing | … |
| Slingeren/kromming/schuren/naden, met/zonder steun | … |
| Aparte stresslast:g/positie/duur/resultaat, of overgeslagen | … |

**Foto/video, prettig/vervelend handwerk (optioneel):** …

## 5. Interpretatie en vervolg — CTO, pas na feedback

Nog geen fysieke resultaten; GO/NO-GO blijft open. Stilte is geen succes of blokkade. Geen extra pasvarianten of aangedreven proef met dit pakket goedgekeurd.
