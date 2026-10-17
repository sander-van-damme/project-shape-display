#!/usr/bin/env python3
"""Check the final review evidence against the delivered meshes/project/settings."""
from pathlib import Path
import hashlib,json,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[3]; HERE=Path(__file__).resolve().parent;TEST=ROOT/'owner-print-tests/2026-10-17-two-cell-supported-selector'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
g=read(HERE/'review/geometry-review.json');assert not g['unexpected_intersections'] and not g['exclusions'];assert g['checks']==7180
for n,h in g['mesh_sha256'].items():assert sha(HERE/'cad/parts'/(n+'.stl'))==h,n
layout=read(TEST/'layout.json');assert len(layout)==18
for part in layout:assert (ROOT/part['source']).is_file(),part['source']
project=TEST/'two-cell-selector.3mf';build=read(TEST/'two-cell-selector-build.json');assert sha(project)==build['final_project_sha256']
assert build['roundtrip']['return_code']==0 and not build['roundtrip']['settings_differences']
r=read(TEST/'slicer-review.json');assert r['project_sha256']==sha(project)
assert r['source_stl_sha256']==sha(TEST/'two-cell-supported-selector.stl')
assert r['geometry']['body_count']==18 and r['geometry']['watertight']
assert r['geometry']['source_facet_count']==r['geometry']['archive_facet_count']
assert r['geometry']['max_bidirectional_vertex_error_mm']<.00003
lo,hi=r['geometry']['bounds_mm'];assert min(lo)>=0 and hi[0]<256 and hi[1]<256 and hi[2]<256
with zipfile.ZipFile(project) as z:
 assert z.testzip() is None
 assert 'Metadata/plate_1.gcode' in z.namelist()
 s=json.loads(z.read('Metadata/project_settings.config'))
 assert s['printer_model']=='Bambu Lab X1 Carbon' and s['nozzle_diameter']==['0.4']
 assert s['filament_type']==['PLA'] and s['layer_height']=='0.12'
 assert s['enable_support']=='0' and s['brim_type']=='no_brim'
 assert s['wall_generator']=='arachne' and s['curr_bed_type']=='Textured PEI Plate'
 assert hashlib.sha256(z.read('Metadata/plate_1.gcode')).hexdigest()==r['gcode_sha256']
hist=read(HERE/'review/history-integrity.json');assert hist['tracked_files_checked']==1257 and not hist['changed']
br2=read(TEST/'scaffold-reslice-review.json');assert br2['brace_count']==20 and br2['all_braces_have_at_least_one_deposited_connection']
br=read(TEST/'scaffold-path-review.json');assert br['brace_count']==20 and br['all_braces_have_at_least_one_deposited_connection']
assert 'Support' not in r['roles'] and 'Support interface' not in r['roles']
for n in ['test.md','bambu-settings.md','resultaten.md','montage-en-test.pdf','resultatenformulier.pdf']:
 assert (TEST/n).stat().st_size>100,n
result=dict(status='PASS',evidence='Final artifact hashes, archive CRC, reviewed geometry, archived process and reopen checks; no physical claims.',project_sha256=sha(project),mesh_checks=g['checks'],geometry_poses=len(g['states']),print_objects=len(layout),plate_bounds_mm=r['geometry']['bounds_mm'],scaffold_braces=br['brace_count'],physical_results='unknown')
(HERE/'review/delivery-integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
