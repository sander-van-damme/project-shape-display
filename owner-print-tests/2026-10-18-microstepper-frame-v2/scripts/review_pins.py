#!/usr/bin/env python3
"""Review actual pin contours and local support in an E302 Bambu slice."""
import sys,json,zipfile,hashlib,importlib.util,collections
from pathlib import Path
from paths import TEST_DIR, CAD, COMPONENTS, METADATA, IMAGES
import numpy as np
from shapely.geometry import Point,Polygon
from shapely.affinity import translate
here=TEST_DIR
spec=importlib.util.spec_from_file_location('reader',here.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
project=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(project) as archive:
 cfg=json.loads(archive.read('Metadata/project_settings.config'));paths,_=reader.parse(archive.read('Metadata/plate_1.gcode').decode());bounds,*_=reader.project_bounds(archive)
layout=json.loads((METADATA / 'layout.json').read_text());source_lo=np.min([p['bounds_mm'][0] for p in layout],axis=0)
shift=bounds[0,:2]-source_lo[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')])
report={'scope':'Nominal deposited G-code footprint screening; does not prove physical bed adhesion, stiffness or thread fit.','project_sha256':hashlib.sha256(project.read_bytes()).hexdigest(),'pins':[]}
footprints={}
for part in layout:
 if not part['source'].startswith('pin-'):continue
 cx,cy=np.array(part['center_xy'])+shift
 layers=collections.defaultdict(list)
 for p in paths:
  if abs((p['x']+p['x1'])/2-cx)<6.1 and abs((p['y']+p['y1'])/2-cy)<6.1:layers[p['z']].append(p)
 rows=[];previous=None;local={}
 for z,ps in sorted(layers.items()):
  fp=translate(reader.footprint(ps),-cx,-cy);local[z]=fp;polys=list(fp.geoms) if hasattr(fp,'geoms') else [fp]
  encloses=any(poly.geom_type=='Polygon' and Polygon(poly.exterior).contains(Point(0,0)) and not poly.contains(Point(0,0)) for poly in polys)
  unsupported=[poly.area for poly in polys if poly.area>.005 and previous is not None and poly.intersection(previous.buffer(.01)).area<.001]
  rows.append(dict(z_mm=z,open_core_radius_060=fp.intersection(Point(0,0).buffer(.60)).area<.001,closed_wall_around_bore=encloses,unsupported_island_areas_mm2=unsupported,footprint_area_mm2=fp.area,support_paths=sum('support' in p['role'].lower() for p in ps),max_speed_mm_s=max(p['speed'] for p in ps),max_acceleration_mm_s2=max(p['accel'] for p in ps)))
  previous=fp
 first=local[min(local)];upper=[r for r in rows if r['z_mm']>6.12]
 summary=dict(name=part['name'],layers=len(rows),max_z_mm=max(local),bed_foot_bounds_mm=list(first.bounds),bed_contact_area_mm2=first.area,all_layers_open_core=all(r['open_core_radius_060'] for r in rows),upper_closed_contour_all_layers=all(r['closed_wall_around_bore'] for r in upper),upper_layer_count=len(upper),no_unsupported_islands=all(not r['unsupported_island_areas_mm2'] for r in rows),no_support_paths=all(r['support_paths']==0 for r in rows),upper_max_speed_mm_s=max(r['max_speed_mm_s'] for r in upper),upper_max_acceleration_mm_s2=max(r['max_acceleration_mm_s2'] for r in upper),layer_details=rows)
 assert summary['all_layers_open_core'] and summary['upper_closed_contour_all_layers'] and summary['no_unsupported_islands'] and summary['no_support_paths'],summary['name']
 assert abs(summary['max_z_mm']-part['bounds_mm'][1][2])<.13
 assert first.bounds[2]-first.bounds[0]>11.5 and first.bounds[3]-first.bounds[1]>11.5
 report['pins'].append(summary);footprints[part['name']]=local
comparison=[]
for z,a in footprints['pin-18'].items():
 if z>6.12:continue
 b=footprints['pin-50'][z];comparison.append(dict(z_mm=z,symmetric_difference_mm2=a.symmetric_difference(b).area,hausdorff_distance_mm=a.hausdorff_distance(b)))
report['lower_thread_comparison']=dict(layers=len(comparison),max_symmetric_difference_mm2=max(r['symmetric_difference_mm2'] for r in comparison),max_hausdorff_distance_mm=max(r['hausdorff_distance_mm'] for r in comparison),details=comparison)
report['stability_limits']=['50 mm tall, 4.4 mm wide upper tube; height/body-width ratio 11.36. Integral 12 x 12 x 0.24 mm foot provides bed contact but no lateral support above bed.','Continuous supported footprints only rule out disconnected islands; they do not qualify upright stability, adhesion, nozzle collision or PLA wall stiffness.','No generated supports touch the bore/thread; leave the integral thin foot attached, as it remains below the frame guide during this test.','Confirm clean bed and complete first-layer attachment; stop if the tube wobbles or foot lifts. Actual tall-print stability remains untested.']
out.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**report,'pins':[{k:v for k,v in p.items() if k!='layer_details'} for p in report['pins']],'lower_thread_comparison':{k:v for k,v in report['lower_thread_comparison'].items() if k!='details'}},indent=2))
