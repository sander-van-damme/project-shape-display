# Opgeslagen Bambu-instellingen

Exact uit `Metadata/project_settings.config` van de geleverde 3MF; volledige export in `saved-settings.json`. Herhaalde arraywaarden horen bij het Bambu-formaat, niet bij meerdere benodigde extruders.

**Bambu Studio 02.08.02.61**, X1 Carbon / 0,4 / Generic PLA. Eén plaat, vijf objecten, supports uit. **10,43 g, 3,498 m, 2h 56m 41s totaal / 2h 41m 2s model** zijn slicerschattingen.

| Sleutel | Werkelijk opgeslagen waarde |
|---|---|
| `printer_model` | `"Bambu Lab X1 Carbon"` |
| `printer_variant` | `"0.4"` |
| `printer_settings_id` | `"Bambu Lab X1 Carbon 0.4 nozzle"` |
| `nozzle_diameter` | `["0.4"]` |
| `filament_settings_id` | `["Generic PLA"]` |
| `filament_type` | `["PLA"]` |
| `filament_flow_ratio` | `["0.98"]` |
| `nozzle_temperature_initial_layer` | `["220"]` |
| `nozzle_temperature` | `["220"]` |
| `curr_bed_type` | `"Textured PEI Plate"` |
| `textured_plate_temp_initial_layer` | `["55"]` |
| `textured_plate_temp` | `["55"]` |
| `layer_height` | `"0.12"` |
| `initial_layer_print_height` | `"0.12"` |
| `wall_generator` | `"arachne"` |
| `wall_loops` | `"2"` |
| `line_width` | `"0.45"` |
| `initial_layer_line_width` | `"0.45"` |
| `outer_wall_line_width` | `"0.45"` |
| `inner_wall_line_width` | `"0.45"` |
| `sparse_infill_density` | `"100%"` |
| `sparse_infill_pattern` | `"zig-zag"` |
| `min_bead_width` | `"75%"` |
| `min_feature_size` | `"10%"` |
| `outer_wall_speed` | `["15", "15"]` |
| `inner_wall_speed` | `["20", "20"]` |
| `small_perimeter_speed` | `["15", "15"]` |
| `initial_layer_speed` | `["15", "15"]` |
| `initial_layer_infill_speed` | `["15", "15"]` |
| `sparse_infill_speed` | `["30", "30"]` |
| `internal_solid_infill_speed` | `["30", "30"]` |
| `top_surface_speed` | `["30", "30"]` |
| `gap_infill_speed` | `["30", "30"]` |
| `bridge_speed` | `["15", "15"]` |
| `default_acceleration` | `["1000", "1000"]` |
| `outer_wall_acceleration` | `["500", "500"]` |
| `inner_wall_acceleration` | `["1000", "1000"]` |
| `initial_layer_acceleration` | `["500", "500"]` |
| `travel_acceleration` | `["1000", "1000"]` |
| `travel_speed` | `["150", "150"]` |
| `enable_support` | `"0"` |
| `support_on_build_plate_only` | `"0"` |
| `brim_type` | `"no_brim"` |
| `brim_width` | `"0"` |
| `raft_layers` | `"0"` |
| `xy_contour_compensation` | `"0"` |
| `xy_hole_compensation` | `"0"` |
| `elefant_foot_compensation` | `"0"` |
| `fan_min_speed` | `["100"]` |
| `fan_max_speed` | `["100"]` |
| `close_fan_the_first_x_layers` | `["1"]` |
| `additional_cooling_fan_speed` | `["0"]` |
| `slow_down_for_layer_cooling` | `["1"]` |
| `slow_down_min_speed` | `["10"]` |
| `slow_down_layer_time` | `["8"]` |
| `fan_cooling_layer_time` | `["100"]` |
| `print_sequence` | `"by layer"` |
| `enable_arc_fitting` | `"0"` |

De twee framehelften liggen met hun splitvlak op het bed. De houder heeft zijn vierkante socket naar het bed, met een controleerbare roofbrug van 10,38 mm. Schroef en pin staan rechtop op brede bestaande voeten. Framebruggen maximaal circa 6,98 mm. Geen steunen aan de functionele draad of in de pinholte. Geen brim nodig geacht voor deze brede bedcontacten; werkelijke hechting blijft een fysieke controle.

De 23 lokale nominale draadwandonderbrekingen in de pin zijn zichtbaar in de behouden geometrie/slice; de bovenste buis is gesloten. De schroefbanen zijn per laag verbonden, maar de kleine kern is niet als volledig massief geclaimd. Geen draadoptimalisatie uitgevoerd. Gebruik zo mogelijk het bestaande soepel bevonden paar.

De definitieve 3MF is zonder externe profielen met de officiële Bambu-runtime opnieuw geopend en gesliced; instellingen identiek, maximale nominale footprintverandering per onderdeel/laag 0,00406%. Dit is CLI-heropening, geen interactieve GUI-inspectie. Headless Wayland/GLFW-meldingen betroffen de previewrenderer. Bambu logde tevens vier `ZFiller: both point in subject`-meldingen bij de draadgeometrie; beide slices eindigden met code 0. De afzonderlijke baancontrole toetst de resulterende geometrie in plaats van deze meldingen te verbergen.

Zie `slicer-review.json`, `microstepper-rig-build.json` en `toolpaths.png` voor controleerbare herkomst en werkelijke banen. Geen van deze resultaten is een fysieke print-, montage- of motortest.
