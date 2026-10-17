#!/usr/bin/env python3
"""Write the saved-settings handoff from the final 3MF and actual-path reviews."""
import argparse,json,re,zipfile
from pathlib import Path
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--directory',type=Path,required=True);a=ap.parse_args();d=a.directory
 r=json.loads((d/'slicer-review.json').read_text());b=json.loads((d/'cone-friction-selector-build.json').read_text());rr=json.loads((d/'reslice-comparison.json').read_text());sel=json.loads((d/'selector-paths.json').read_text());cones=json.loads((d/'cone-paths.json').read_text());braces=json.loads((d/'brace-paths.json').read_text())
 with zipfile.ZipFile(d/r['project']) as z:s=json.loads(z.read('Metadata/project_settings.config'))
 keys='printer_model printer_variant printer_settings_id nozzle_diameter filament_settings_id filament_type filament_diameter filament_density filament_flow_ratio nozzle_temperature nozzle_temperature_initial_layer curr_bed_type textured_plate_temp textured_plate_temp_initial_layer layer_height initial_layer_print_height wall_generator min_bead_width min_feature_size wall_loops top_shell_layers bottom_shell_layers sparse_infill_density sparse_infill_pattern line_width initial_layer_line_width outer_wall_line_width inner_wall_line_width top_surface_line_width sparse_infill_line_width internal_solid_infill_line_width support_line_width outer_wall_speed inner_wall_speed small_perimeter_speed small_perimeter_threshold initial_layer_speed initial_layer_infill_speed sparse_infill_speed internal_solid_infill_speed top_surface_speed gap_infill_speed bridge_speed travel_speed default_acceleration outer_wall_acceleration inner_wall_acceleration top_surface_acceleration sparse_infill_acceleration travel_acceleration initial_layer_acceleration initial_layer_travel_acceleration enable_support support_type support_on_build_plate_only brim_type brim_width brim_object_gap raft_layers print_sequence xy_contour_compensation xy_hole_compensation elefant_foot_compensation enable_circle_compensation enable_arc_fitting fan_min_speed fan_max_speed slow_down_for_layer_cooling slow_down_min_speed slow_down_layer_time fan_cooling_layer_time close_fan_the_first_x_layers additional_cooling_fan_speed'.split()
 f=lambda v: ', '.join(str(x) for x in v) if isinstance(v,list) else str(v)
 estimates='\n'.join('- '+q.lstrip('; ') for q in r['gcode_estimates'] if 'filament volume' not in q)
 table='\n'.join(f'| `{k}` | `{f(s[k])}` |' for k in keys if k in s)
 rows=sel['selector_reviews'];checks=[q for p in rows for q in p['layers']];cs=[q for p in cones['cone_reviews'] for q in p['layers']]
 bridge=max(p['max_free_bridge_overhang_centerline_mm'] for p in r['part_toolpath_screens'] if p['name'].startswith('frame-'))
 pin_gap=max(p['pin_open_bore_screen']['nominal_midwall_max_gap_mm'] for p in r['part_toolpath_screens'] if p['name']=='pin')
 text=f'''# Opgeslagen Bambu Studio-instellingen — E-300

Eén geconfigureerd **Bambu Studio 02.08.02.61**-project voor **Bambu Lab X1 Carbon, 0,4-mm nozzle, Generic PLA, Textured PEI Plate**. Open `cone-friction-selector.3mf` als **project** en behoud instellingen, plaatsing en oriëntatie. Het bevat de geometrie, instellingen en geslicede G-code voor één plaat met {r['geometry']['body_count']} printobjecten. Gewoon PLA; geen speciale contacttextuur, coating of slicerpatroon voor extra wrijving. De E-295/E-299-profielbasis blijft behouden. E-300 is nog niet fysiek getest.

## Tijd en materiaal

Slicerschattingen, geen fysieke printresultaten:

{estimates}

CAD-plaat: {', '.join(f'{v:.2f}' for v in [r['geometry']['bounds_mm'][1][i]-r['geometry']['bounds_mm'][0][i] for i in range(3)])} mm (X × Y × Z). Laatste geëxtrudeerde laag: {max(p['top_extrusion_z_mm'] for p in r['part_toolpath_screens']):.2f} mm.

## Oriëntatie en werkelijke paden

- Framehelften liggen op hun splitvlak. De grootste vrije middenlijn van een brug-/overhangbaan is {bridge:.2f} mm; inspecteer fysieke doorhang vóór montage.
- Rijselector rust op de brede centrale achterzijde; driehoekige zijdelen laten de bredere romp geleidelijk groeien. De kolomselectoren staan eveneens op de achterzijde van hun handvat; schuine schouders laten de smalle steel naar de volle romp groeien. Alle kritische 0,46-mm rugverbindingen zijn expliciet gecontroleerd: {len(checks)} onderzochte laagdoorsneden, minimale materiaaldekking op de controlelijn {min(q['material_fraction'] for q in checks):.6f}; grootste gat {max(q['max_gap_mm'] for q in checks):.6f} mm. Dit bewijst geen sterkte of laaghechting.
- Alle vier rotoren staan op hun vlakke flange, met de contactzijde omhoog; de vrouwelijke kommen blijven bovenaan open. De conische contactzones hebben {len(cs)} onderzochte lagen; minimale materiaaldekking op de gekozen cirkel {min(q['checked_ring_material_fraction'] for q in cs):.6f}. Gewone printsporen blijven onderdeel van de fysieke proef.
- Ingangsassen staan op de flange; pinnen staan met hun gesloten top op het bed. De E-299-schroeven staan op hetzelfde getekende steunboompje. Alle {braces['brace_count']} verbreekbare verbindingen zijn in de werkelijke banen aanwezig. Wegknippen en draadschade blijven fysieke inspectiepunten. De behouden E-299-pindraad toont lokale nominale wandonderbrekingen tot {pin_gap:.3f} mm; inspecteer draad en dunne wand vóór de krachtproef. Dit wordt niet als bewezen sterk gepresenteerd.
- Slicersupports, raft en brim zijn uitgeschakeld; steunboompje en PLA-contactvlakken zijn modelgeometrie. Geen supportmateriaal in boringen of schroefdraad. Reinig uitsluitend bramen; geen voorafgaande contactbehandeling.

## Heropening en herhaalbaarheid

Het opgeslagen project is zonder externe profielen heropend en opnieuw gesliced. Retourcode {b['roundtrip']['return_code']}; verschillen in opgeslagen instellingen: `{json.dumps(b['roundtrip']['settings_differences'])}`. De G-code is niet bytegelijk. De maximale verandering van de nominale materiaalvoetafdruk per laag bij herhalen is {rr['max_layer_footprint_change_percent']:.6f}%; de afzonderlijke verschillen staan in `reslice-comparison.json`. Ook de heropende slice is opnieuw op de 20 conuslagen, 10 rugdoorsneden en alle 20 steunbrugjes gecontroleerd; kommen en ruggen blijven verbonden/open zoals bedoeld, zie `roundtrip-critical-checks.json`. Volgorde, materiaaltoevoer en printgedrag zijn daarmee niet fysiek gelijk bewezen.

## Waarden uit het geleverde archief

| Instelling | Opgeslagen waarde |
|---|---|
{table}

Project SHA-256: `{r['project_sha256']}`.

Volledige profielherkomst en bronhashes: `cone-friction-selector-build.json`. Onafhankelijke padencontroles: `slicer-review.json`, `cone-paths.json`, `selector-paths.json`, `brace-paths.json`. De `*-toolpaths.png`-beelden tonen nominale materiaalvoetafdrukken uit de werkelijk opgeslagen G-code; geen foto's of fysieke resultaten.
'''
 (d/'bambu-settings.md').write_text(text)
 print(d/'bambu-settings.md')
if __name__=='__main__':main()
