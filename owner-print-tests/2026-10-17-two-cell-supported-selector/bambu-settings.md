# Opgeslagen Bambu Studio-instellingen — E-299

Dit is één geconfigureerd **Bambu Studio 02.08.02.61**-project voor **Bambu Lab X1 Carbon, 0,4-mm nozzle, Generic PLA, Textured PEI Plate**. Het bevat geometrie, vaste plaatsing/orientatie, printer-, filament- en procesinstellingen en daadwerkelijk geslicede G-code. Open `two-cell-selector.3mf` als **project** en behoud de projectinstellingen. De E-295-profielbasis heeft eigenaar-gerapporteerde fysieke printhistorie; E-299 zelf is nog niet fysiek getest.

**Slicerschatting:** 3 uur 33 min 55 s totaal, 3 uur 18 min 16 s model; **9,37 g / 3,142 m PLA**. Opstart/purge en werkelijke snelheid kunnen afwijken. Eén plaat, 18 geprinte objecten; het schroefboompje levert twee schroeven na het verwijderen van de steunen. Maximumhoogte CAD 27,71 mm, laatste toolpathlaag 27,72 mm. Geen slicersupports, raft of brim. De schroeven hebben meegetekende, weg te knippen steunen; dit zijn modelbanen.

## Printorientatie en inspectie

- Framehelften: splitvlak op het bed, ongeveer 7,2 mm hoog. Dit houdt de lager-/selectorgaten zijdelings open. Buitenwanden boven vensters vereisen nog bruggen.
- Rijselecteur: brede rug op het bed. Kolomselecteurs: op de lange zijkant, 4,6 mm hoog; werkelijke binnenbrug bij Z 0,72 is 2,280 mm en aan beide uiteinden ondersteund.
- Vier rotors: vlakke flange op het bed; bedcontact elk 9,89–9,94 mm². Hals en blinde DD-boring blijven vrij van slicersupports. De kleine sluitbrug in de blinde boring heeft een vrije middenlijn van maximaal 1,491 mm.
- Ingangsassen: flange op het bed; pinnen: gesloten bovenvlak op het bed, boring naar boven. Schroeven rechtop in één breed gesteund boompje; 160,38 mm² eerste-laagcontact, vier zijpilaren en 20 dwarslipjes.
- De eerste laag is daadwerkelijk gesliced: alle 18 objecten hebben bedcontact en in alle objectlagen zijn modelbanen aanwezig. Geen door supports gevulde draadboringen.

**Bewuste resterende risico's:** bij Z 6,12 bevat het achterframe echte brugbanen van 21,980 mm met ondersteunde uiteinden. Het voorframe heeft overhangwandbanen tot 19,642 mm waarvan eindpunten circa 0,59–0,97 mm buiten het vorige-laagmateriaal liggen; deze volgen de brugstructuur van dezelfde laag. Dit betreft de buitenwand/vensterdaken, buiten de draad en DD-sockets. PLA-brugvorming en eventuele doorhang zijn fysiek onbekend: inspecteer ze voor montage. De lage brugsnelheid (15 mm/s), volledige koeling na de eerste laag en brede framevoet zijn hiervoor behouden. Deze slicecontrole bewijst geen succesvolle brugprint.

## Controle en expliciete beperkingen

- Nieuw opgeslagen project opnieuw geopend en opnieuw gesliced **zonder externe printer-/filament-/procesprofielen**: beide returncode 0; **geen opgeslagen instelling verschilt**. De nominale gedeponeerde laag-footprints verschillen maximaal **2,7961%** tussen beide slices. Dit zijn slicerpad-/naadvariaties; de G-code is niet byte-identiek. Zie `reslice-comparison.json`.
- Alle **20** scaffoldcontacten hebben in zowel het geleverde project als de opnieuw geslicede versie in minstens één van hun betreffende lagen een daadwerkelijk verbonden nominale baan van schroef naar zijpilaar. Zie `scaffold-path-review.json` en `scaffold-reslice-review.json`. Dit bewijst geen stevigheid of beschadigingsvrije verwijdering; knip de steun los en vermijd wringen aan de draad.
- Vier rotorhalzen: alle **60 onderzochte halslagen** hebben een gesloten wand rond de open boring. Alle **72 onderzochte tandlagen** hebben exact twee losse tandvlakken, aangesloten op de voorgaande wortellagen. Zie `slicer-review.json` en `rotor-toolpaths.png`.
- Beide schroefdraden: elk **129 werksectielagen** met één verbonden materiaalcomponent. Minimum nominale dekking van de centrale 0,45-mm-radiusdisk circa **84,1%**; minimum gevonden crest-materiaalradius **1,5927 mm**. Geen claim van massieve kern of exacte geprinte draaddimensies. Zie `thread-path-review.json`.
- **Bambu-waarschuwing blijft behouden:** “It seems object 17-pin has floating regions. Please re-orient the object or enable support generation.” Beide pinnen hebben in alle 150 lagen vorige-laagverbinding (geen los component >0,005 mm²); de boring is open met minimaal 0,839 mm nominale asvrijheid. Dit neemt de dunne-wandbeperking niet weg.
- **Dunne draadwanden:** bij de pinnen missen respectievelijk **21 en 26** draadlagen een volledig gesloten nominale footprint; met 0,005-mm geometrische buffer blijven **19 en 22** lagen open. Maximale onderbreking van de nominale middenwandlijn is **0,2074 mm**. Dit is een expliciet resterend risico van de behouden E-295-pin/draadgeometrie. De gladde buiszone heeft deze onderbrekingen niet. Die draad wordt in deze selectorproef niet verder geoptimaliseerd. Inspecteer gaatjes/losse draadsecties; noteer ze, forceer geen slecht passende schroef en claim geen wandsterkte op basis van deze slice.
- De nominale banen gebruiken de door Bambu opgegeven `LINE_WIDTH`. Zij bewijzen geen bedhechting, materiaaldikte, passing, lijnaansluiting in werkelijk PLA, wrijving of mechanische werking. Kleine Arachne-overgangssegmenten kunnen smaller zijn dan de ingestelde nominale minimumbreedte.
- CLI-slice en CLI-heropening zijn uitgevoerd met de officiële Bambu-runtime. De log bevat headless-displaymeldingen (`Wayland`/`glfw`); beide slices slagen en leveren de controleerbare G-code. Er is geen interactieve scherminspectie geclaimd.

## Exacte waarden uit het definitieve 3MF

Herhaalde waarden in een cel komen letterlijk uit de Bambu-arrayinstelling. Alleen de geselecteerde X1C-nozzle wordt gebruikt. Alle hieronder vermelde waarden zijn uit `Metadata/project_settings.config` gelezen, niet uit geschreven aanbevelingen.

| Instelling | Opgeslagen waarde |
|---|---|
| `printer_model` | `Bambu Lab X1 Carbon` |
| `printer_variant` | `0.4` |
| `nozzle_diameter` | `0.4` |
| `filament_settings_id` | `Generic PLA` |
| `filament_type` | `PLA` |
| `filament_diameter` | `1.75` |
| `filament_density` | `1.24` |
| `filament_flow_ratio` | `0.98` |
| `nozzle_temperature_initial_layer` | `220` |
| `nozzle_temperature` | `220` |
| `curr_bed_type` | `Textured PEI Plate` |
| `textured_plate_temp_initial_layer` | `55` |
| `textured_plate_temp` | `55` |
| `layer_height` | `0.12` |
| `initial_layer_print_height` | `0.12` |
| `wall_generator` | `arachne` |
| `min_bead_width` | `75%` |
| `min_feature_size` | `10%` |
| `wall_loops` | `2` |
| `sparse_infill_density` | `100%` |
| `sparse_infill_pattern` | `zig-zag` |
| `line_width` | `0.45` |
| `initial_layer_line_width` | `0.45` |
| `outer_wall_line_width` | `0.45` |
| `inner_wall_line_width` | `0.45` |
| `top_surface_line_width` | `0.45` |
| `sparse_infill_line_width` | `0.45` |
| `internal_solid_infill_line_width` | `0.45` |
| `support_line_width` | `0.45` |
| `outer_wall_speed` | `15, 15` |
| `inner_wall_speed` | `20, 20` |
| `small_perimeter_speed` | `15, 15` |
| `small_perimeter_threshold` | `20, 20` |
| `initial_layer_speed` | `15, 15` |
| `initial_layer_infill_speed` | `15, 15` |
| `sparse_infill_speed` | `30, 30` |
| `internal_solid_infill_speed` | `30, 30` |
| `top_surface_speed` | `30, 30` |
| `gap_infill_speed` | `30, 30` |
| `bridge_speed` | `15, 15` |
| `internal_bridge_speed` | `MISSING` |
| `travel_speed` | `150, 150` |
| `default_acceleration` | `1000, 1000` |
| `outer_wall_acceleration` | `500, 500` |
| `inner_wall_acceleration` | `1000, 1000` |
| `top_surface_acceleration` | `1000, 1000` |
| `sparse_infill_acceleration` | `1000, 1000` |
| `travel_acceleration` | `1000, 1000` |
| `initial_layer_acceleration` | `500, 500` |
| `initial_layer_travel_acceleration` | `1000, 1000` |
| `enable_support` | `0` |
| `support_type` | `normal(auto)` |
| `support_on_build_plate_only` | `0` |
| `brim_type` | `no_brim` |
| `brim_width` | `0` |
| `brim_object_gap` | `0.12` |
| `raft_layers` | `0` |
| `print_sequence` | `by layer` |
| `xy_contour_compensation` | `0` |
| `xy_hole_compensation` | `0` |
| `elefant_foot_compensation` | `0` |
| `enable_circle_compensation` | `0` |
| `enable_arc_fitting` | `0` |
| `fan_min_speed` | `100` |
| `fan_max_speed` | `100` |
| `slow_down_for_layer_cooling` | `1` |
| `slow_down_min_speed` | `10` |
| `slow_down_layer_time` | `8` |
| `fan_cooling_layer_time` | `100` |
| `close_fan_the_first_x_layers` | `1` |
| `additional_cooling_fan_speed` | `0` |

Project SHA-256: `32526470ca517584ea6acfa9368a22a5142ed55c0825b4ddde8f888ef3834fa8`.

Bronprofielen, exacte versies en hashes staan in `two-cell-selector-build.json`; geometrie-/toolpathcontrole in `slicer-review.json`. De beelden `toolpaths.png`, `pin-toolpaths.png`, `rotor-toolpaths.png`, `column-selector-toolpaths.png` en `screw-tree-toolpaths.png` tonen de daadwerkelijke geslicede banen, geen fysieke resultaten.
