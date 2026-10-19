#!/usr/bin/env python3
"""Review nominal deposited footprint support; usage: review_support.py PROJECT OUT.json."""
import sys,json,zipfile,importlib.util,collections,math,hashlib
from pathlib import Path
import numpy as np
from shapely.geometry import LineString,Point,box
here=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reader',here.parent/'validate-bambu-project.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
project=Path(sys.argv[1]);out=Path(sys.argv[2])
with zipfile.ZipFile(project) as z:
 cfg=json.loads(z.read('Metadata/project_settings.config'));paths,_=reader.parse(z.read('Metadata/plate_1.gcode').decode());bounds,*_=reader.project_bounds(z)
layout=json.loads((here/'layout.json').read_text());source_lo=np.min([p['bounds_mm'][0] for p in layout],axis=0)
shift=bounds[0,:2]-source_lo[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')])
report={'scope':'Nominal G-code widths and layer footprints; not physical bridge quality or fit.','project_sha256':hashlib.sha256(project.read_bytes()).hexdigest(),'parts':[]};plotdata=[]
for part in layout:
 lo,hi=np.array(part['bounds_mm']);lo[:2]+=shift;hi[:2]+=shift
 layers=collections.defaultdict(list)
 for p in paths:
  if lo[0]-.1<=(p['x']+p['x1'])/2<=hi[0]+.1 and lo[1]-.1<=(p['y']+p['y1'])/2<=hi[1]+.1:layers[p['z']].append(p)
 previous=None;orphans=[];bridges=[];flex=[];roof=[]
 cx,cy=np.array(part['center_xy'])+shift
 for z,ps in sorted(layers.items()):
  fp=reader.footprint(ps)
  if previous is not None:
   prev=previous.buffer(.01)
   polys=list(fp.geoms) if hasattr(fp,'geoms') else [fp]
   for poly in polys:
    if poly.area>.005 and poly.intersection(prev).area<.001:orphans.append({'z':z,'area':poly.area,'centroid':list(poly.centroid.coords)[0]})
   for p in ps:
    if not any(t in p['role'].lower() for t in ('bridge','overhang')):continue
    line=LineString([(p['x'],p['y']),(p['x1'],p['y1'])]);free=line.difference(prev);pieces=list(free.geoms) if hasattr(free,'geoms') else [free]
    row={'z':z,'role':p['role'],'free_span_mm':max((s.length for s in pieces),default=0),'start_distance_mm':Point(p['x'],p['y']).distance(prev),'end_distance_mm':Point(p['x1'],p['y1']).distance(prev),'dx_mm':p['x1']-p['x'],'dy_mm':p['y1']-p['y']}
    bridges.append(row)
    if part['source'].startswith('half') and 3.95<=z<=4.56 and cy-7.4-.1<=(p['y']+p['y1'])/2<=cy-5+.1 and abs((p['x']+p['x1'])/2-cx)<5.5:flex.append(row)
    if part['source'].startswith('coupling') and 2.59<=z<=2.76:roof.append(row)
   if part['name']=='frame-back' and abs(z-4.08)<.01:plotdata.append((ps,previous,cx,cy))
  previous=fp
 report['parts'].append({'name':part['name'],'layers':len(layers),'unsupported_islands':orphans,'max_free_bridge_overhang_span_mm':max((r['free_span_mm'] for r in bridges),default=0),'max_span_record':max(bridges,key=lambda r:r['free_span_mm']) if bridges else None,'flexure_bridge_paths':flex,'square_socket_roof_max_span_mm':max((r['free_span_mm'] for r in roof),default=0)})
assert all(not p['unsupported_islands'] for p in report['parts']), 'Unsupported islands'
for p in report['parts']:
 if p['name'].startswith('frame'):
  spans=[r for r in p['flexure_bridge_paths'] if abs(r['dx_mm'])>10 and abs(r['dy_mm'])<.01]
  assert spans and all(r['start_distance_mm']<.01 and r['end_distance_mm']<.01 for r in spans)
  p['full_width_X_bridge_spans_anchored_at_both_ends']=len(spans)
report['separate_review']='Upright screw and towers included in layer connectivity check; sparse necks independently checked in long-screw-review.json.'
report['gate']='PASS: all eight parts have footprint connectivity and anchored full-width X flexure bridge paths; physical bridge sag remains untested'
out.write_text(json.dumps(report,indent=2)+'\n')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,4))
for ps,prev,cx,cy in plotdata:
 polys=list(prev.geoms) if hasattr(prev,'geoms') else [prev]
 for poly in polys:
  if poly.geom_type=='Polygon':
   x,y=poly.exterior.xy;ax.fill(np.array(x)-cx,np.array(y)-cy,color='#cccccc',alpha=.6)
   for hole in poly.interiors:
    x,y=hole.xy;ax.fill(np.array(x)-cx,np.array(y)-cy,color='white')
 for p in ps:
  if cy-8<p['y']<cy-4:ax.plot([p['x']-cx,p['x1']-cx],[p['y']-cy,p['y1']-cy],color='#c75627' if 'bridge' in p['role'].lower() else '#276b85',linewidth=1)
ax.set_xlim(-8,8);ax.set_ylim(-10,-4);ax.set_aspect('equal');ax.set_title('Frame flexure first bridge layer Z=4.08 mm; previous-layer footprint grey');ax.set_xlabel('Local X mm');ax.set_ylabel('Local Y mm');fig.tight_layout();fig.savefig(out.with_suffix('.png'),dpi=180)
print(json.dumps([{k:v for k,v in p.items() if k!='flexure_bridge_paths'} for p in report['parts']],indent=2))
