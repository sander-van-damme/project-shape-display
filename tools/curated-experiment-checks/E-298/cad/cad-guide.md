# E-298 CAD — nieuwe puntvlakken, bestaande E-297-onderdelen

`generate.py` importeert uitsluitend functies uit de bestaande E-297-generator en schrijft uitsluitend naar E-298 en de twee nieuwe testfolders. E-297-bronbestanden blijven ongewijzigd. De bestaande geprinte framehelften, selectors, assen, schroeven, pinnen, sleutel, afstandsblokjes en couponassen worden byte-identiek gekopieerd. Vooral de echte E-295-schroef- en pinmesh wordt niet door een vereenvoudigde schroefdraadenveloppe vervangen.

## Nieuwe geometrie

Elke helft heeft twee tegenoverliggende punten op dezelfde bestaande rotor, en twee open complementaire sectorholtes. De tegenhelft is **hetzelfde onderdeel**, omgedraaid om X en vervolgens 90° om Z voor de nominale gekoppelde stand. De twee punten hebben wortelstraal 0,60–1,80 mm en wortelbreedte 76°. Boven de rechte dragende flanken lopen zowel de radiale als de omtreksmaat sterk terug. De drie varianten verschillen uitsluitend in taperhoogte en kruinverschuiving:

| Onderdeel | Taperhoogte | Kruinverschuiving | Rechte flankoverlap bij nominale sluiting |
|---|---:|---:|---:|
| point48 | 0,48 mm | 0° | 0,48 mm |
| point60 | 0,60 mm | 0° | 0,24 mm |
| point60skew | 0,60 mm | 12° | 0,24 mm |

Alle kruinen zijn **0,30 mm radiaal**, met 14,323945° omtrekbreedte (0,30 mm booglengte bij r=1,20 mm). Dit zijn eindige kleine vlakjes, geen ideale wiskundige punten. De eerste 0,16-mm-kruinversie werd door de slicer gedeeltelijk verwijderd en is geen aangeboden printgeometrie. De werkelijke gedeponeerde puntvorm volgt uit de slicercontrole en uiteindelijk de fysieke print.

De nieuwe puntvlakken blijven binnen dezelfde nominale radiale en axiale enveloppe als E-297 en nemen materiaal weg van de functionele toppen. De oude en nieuwe sectoren gebruiken verschillende polygonale boogverdelingen; de STL-driehoeken zijn daarom niet letterlijk een exacte deelverzameling. Externe montage- en buurvrijruimten zijn opnieuw gecontroleerd voor alle 16 nominale selectiestanden; dit is geen nieuwe fysieke kwalificatie van scheefstand of passing.

Rotorhoogte blijft 8,60 mm; tandwortel z=6,20 en tandhoogte 2,40. De bestaande 2,40-mm rij- en kolomslag, 5,08-mm pitch, lagering, selectorvangflens en DD-boring blijven behouden. De maximale rotordiameter blijft 4,30 mm. De matrix gebruikt point48 wegens de grotere resterende rechte flankoverlap. De oude axiale foutbegroting mag **niet** zonder aanpassing worden overgenomen: beide helften hebben elk 0,24 mm vangspeling, samen even groot als de nominale rechte overlap van point48. De uiteindelijke sluiting moet fysiek voldoende rechte flankoverlap houden; een op alleen de schuine toppen dragende koppeling kan onder koppel uit elkaar drukken.

## Montagecoördinaten en meting

Alle coördinaten in mm, in het bestaande E-297-frame:

- Onderste rotorbase: z=7,00 OFF, z=9,40 ON.
- Bovenste omgekeerde rotorbase: z=27,56 OFF, z=25,16 ON.
- Afstand tussen de buitenzijden van de twee vangflenzen: 20,56 OFF/OFF; 18,16 bij één selector ON; **15,76 ON/ON**.
- Afstand tussen tandwortelvlakken ON/ON: 3,36.
- Nominale tipafstand OFF/OFF 3,36; één selector ON 0,96; ON/ON 1,44 mm interdigitatie.
- Bovenste schroef draait met de bovenste rotor mee; de pin wordt tegen draaien geleid. De actuele hoogteverandering is 3,00 mm per volledige schroefomwenteling, plus bestaande speling.

Test A bevat vier helften per variant: twee identieke paren. Vier losse couponassen en twee enkele selectors kunnen tussen de paren worden hergebruikt. Gebruik de plaatkaart voor identificatie; geen minieme reliëfletters op de functionele koppelingen. De kop van een couponas steekt buiten de rotorflens: meet de flensranden, niet de buitenmaat over de couponaskoppen.

## Tijdelijke reactiemal, uitsluitend testgereedschap

`reaction-jig` is een losse vierpluggenmal onder het frame. Hij wijzigt geen selector of aandrijving. De basis is 12 × 12 × 2 mm; de vier DD-pluggen staan op het 5,08-mm raster. In de nominale montage ligt de bovenzijde van de basis op z=−0,20 mm en de plugtop op z=2,19. De pluggen gaan door de bestaande 2,80-mm framegaten en grijpen ongeveer 1,00 mm in de onderste assockets; 0,21 mm eindspeling blijft over. Houd de mal tegen rotatie tijdens de proef: zo zijn alle vier ingangszijden tegelijk stilstaand, zonder fasezoekactie. De plugpassing heeft speling, dus observeer ook de ingaande markeringen. Trek de mal recht naar beneden weg voor de afzonderlijke sleutelproef.

## Bestanden en reproductie

- `parts/point*.step` en `.stl`: drie nieuwe parametrische rotorvarianten.
- `parts/reaction-jig.step` en `.stl`: losse testmal.
- Bestaande onderdelen zijn als afzonderlijke STL en, waar beschikbaar, STEP gekopieerd. De echte schroefdraadonderdelen blijven hun oorspronkelijke functionele STL.
- `assembly-off.stl`, `assembly-r0-c0.stl`, `assembly-all-on.stl`: complete nominale assemblages, **geen printplaten**.
- De twee gedateerde testfolders bevatten de eigen printplaatmesh en `layout.json`; de 3MF is het primaire printbestand.

Vanaf repositoryroot:

```sh
python tools/curated-experiment-checks/E-298/cad/generate.py
python tools/curated-experiment-checks/E-298/cad/validate.py
python tools/curated-experiment-checks/E-298/cad/drawings.py
```

CadQuery, NumPy, trimesh, manifold3d en Matplotlib zijn nodig. De validatie controleert alle 16 harde selectiestanden met 1.504 daadwerkelijke meshdoorsneden, inclusief de reactiemal; alle onverwachte doorsneden moeten nul zijn. Verder zijn positieve en negatieve faseproeven opgenomen. Dit bewijst geometrische montage op nominale maat, **niet** zelfuitlijning onder wrijving, gedrukte puntsterkte, alle mogelijke scheefstanden of gelijktijdig fysiek koppelen. Eén geblokkeerd paar kan zonder lokale compliance de gezamenlijke selector stilzetten.

## Aanvullende 2×2-controle met verschillende beginfasen

`mixed_phase_path.py` controleert 18 voorgeschreven nominale poses van de werkelijke complete 2×2-meshes. Alle vier ingangszijden blijven op 0° vastgehouden. De bovenste koppelingen en schroeven beginnen op 30°, 60°, 120° en 150° en eindigen onafhankelijk op 90°. De bijbehorende pinpositie volgt exact de in E-297 gecontroleerde draadrichting: `z_pin = 38,21 − 3 × (fase − 90) / 360`. De hoogteverandering tussen begin en einde is respectievelijk −0,50, −0,25, +0,25 en +0,50 mm.

Eerst bewegen beide rijen omhoog; daarna bewegen beide kolommen met dezelfde slag. De vereiste axiale opening wordt afgeleid van het maximum van de vier bemonsterde contact-enveloppen, met 0,03 mm rekenmarge. De losse blokjes zijn tijdens beweging verwijderd; de vierpluggen-reactiemal blijft aanwezig. Resultaat: **1.622 kandidaatdoorsneden, 759 unieke booleaanse berekeningen, nul onverwachte botsingen**; zie `mixed-phase-path.json`.

Dit is een extern voorgeschreven geometrisch pad: de vier bovenfasen worden in de berekening opgelegd, niet uit contactkrachten opgelost. Het bewijst daarom geen spontane zelfuitlijning of gegarandeerd vrijlopen van een gedeelde selector. De kleine rekenmarge vermijdt bovendien werkelijk contact in een deel van de poses. Alleen deze 18 nominale poses zijn gecontroleerd, niet iedere tussenliggende stand, wrijving of printafwijking. Eén vastgelopen paar kan de gezamenlijke selectie nog steeds blokkeren.

Reproductie na het genereren van `mesh-contact-envelope.json`:

```sh
python tools/curated-experiment-checks/E-298/cad/mixed_phase_path.py
```
