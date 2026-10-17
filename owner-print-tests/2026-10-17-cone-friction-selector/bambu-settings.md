# Opgeslagen Bambu Studio-instellingen — E-300

Eén geconfigureerd **Bambu Studio 02.08.02.61**-project voor **Bambu Lab X1 Carbon, 0,4-mm nozzle, Generic PLA, Textured PEI Plate**. Open `cone-friction-selector.3mf` als **project** en behoud instellingen, plaatsing en oriëntatie. Het bevat de geometrie, instellingen en geslicede G-code voor één plaat met 17 printobjecten. Gewoon PLA; geen speciale contacttextuur, coating of slicerpatroon voor extra wrijving. De E-295/E-299-profielbasis blijft behouden. E-300 is nog niet fysiek getest.

## Tijd en materiaal

Slicerschattingen, geen fysieke printresultaten:

- model printing time: 3h 32m 8s; total estimated time: 3h 47m 48s
- total filament length [mm] : 3513.38
- total filament weight [g] : 10.48

CAD-plaat: 132.00, 70.00, 27.71 mm (X × Y × Z). Laatste geëxtrudeerde laag: 27.72 mm.

## Oriëntatie en werkelijke paden

- Framehelften liggen op hun splitvlak. De grootste vrije middenlijn van een brug-/overhangbaan is 21.98 mm; inspecteer fysieke doorhang vóór montage.
- Rijselector rust op de brede centrale achterzijde; driehoekige zijdelen laten de bredere romp geleidelijk groeien. De kolomselectoren staan eveneens op de achterzijde van hun handvat; schuine schouders laten de smalle steel naar de volle romp groeien. Alle kritische 0,46-mm rugverbindingen zijn expliciet gecontroleerd: 10 onderzochte laagdoorsneden, minimale materiaaldekking op de controlelijn 0.969051; grootste gat 0.145462 mm. Dit bewijst geen sterkte of laaghechting.
- Alle vier rotoren staan op hun vlakke flange, met de contactzijde omhoog; de vrouwelijke kommen blijven bovenaan open. De conische contactzones hebben 20 onderzochte lagen; minimale materiaaldekking op de gekozen cirkel 1.000000. Gewone printsporen blijven onderdeel van de fysieke proef.
- Ingangsassen staan op de flange; pinnen staan met hun gesloten top op het bed. De E-299-schroeven staan op hetzelfde getekende steunboompje. Alle 20 verbreekbare verbindingen zijn in de werkelijke banen aanwezig. Wegknippen en draadschade blijven fysieke inspectiepunten. De behouden E-299-pindraad toont lokale nominale wandonderbrekingen tot 0.207 mm; inspecteer draad en dunne wand vóór de krachtproef. Dit wordt niet als bewezen sterk gepresenteerd.
- Slicersupports, raft en brim zijn uitgeschakeld; steunboompje en PLA-contactvlakken zijn modelgeometrie. Geen supportmateriaal in boringen of schroefdraad. Reinig uitsluitend bramen; geen voorafgaande contactbehandeling.

## Heropening en herhaalbaarheid

Het opgeslagen project is zonder externe profielen heropend en opnieuw gesliced. Retourcode 0; verschillen in opgeslagen instellingen: `{}`. De G-code is niet bytegelijk. De maximale verandering van de nominale materiaalvoetafdruk per laag bij herhalen is 3.112035%; de afzonderlijke verschillen staan in `reslice-comparison.json`. Ook de heropende slice is opnieuw op de 20 conuslagen, 10 rugdoorsneden en alle 20 steunbrugjes gecontroleerd; kommen en ruggen blijven verbonden/open zoals bedoeld, zie `roundtrip-critical-checks.json`. Volgorde, materiaaltoevoer en printgedrag zijn daarmee niet fysiek gelijk bewezen.

## Waarden uit het geleverde archief

| Instelling | Opgeslagen waarde |
|---|---|
| `printer_model` | `Bambu Lab X1 Carbon` |
| `printer_variant` | `0.4` |
| `printer_settings_id` | `Bambu Lab X1 Carbon 0.4 nozzle` |
| `nozzle_diameter` | `0.4` |
| `filament_settings_id` | `Generic PLA` |
| `filament_type` | `PLA` |
| `filament_diameter` | `1.75` |
| `filament_density` | `1.24` |
| `filament_flow_ratio` | `0.98` |
| `nozzle_temperature` | `220` |
| `nozzle_temperature_initial_layer` | `220` |
| `curr_bed_type` | `Textured PEI Plate` |
| `textured_plate_temp` | `55` |
| `textured_plate_temp_initial_layer` | `55` |
| `layer_height` | `0.12` |
| `initial_layer_print_height` | `0.12` |
| `wall_generator` | `arachne` |
| `min_bead_width` | `75%` |
| `min_feature_size` | `10%` |
| `wall_loops` | `2` |
| `top_shell_layers` | `5` |
| `bottom_shell_layers` | `5` |
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

Project SHA-256: `d0d82881f5a56485b6e79375471f452b46620eee910037644c5d8466eb991b33`.

Volledige profielherkomst en bronhashes: `cone-friction-selector-build.json`. Onafhankelijke padencontroles: `slicer-review.json`, `cone-paths.json`, `selector-paths.json`, `brace-paths.json`. De `*-toolpaths.png`-beelden tonen nominale materiaalvoetafdrukken uit de werkelijk opgeslagen G-code; geen foto's of fysieke resultaten.
