#!/usr/bin/env python3
"""Inspect actual point extrusion, including finite summit width and layer support."""
import argparse,importlib.util,json,zipfile,math
from pathlib import Path
import numpy as np
from shapely.geometry import LineString,Point,Polygon
sp=importlib.util.spec_from_file_location('v',Path(__file__).with_name('validate-project.py'));v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
a=argparse.ArgumentParser();a.add_argument('folder',type=Path);a.add_argument('--review',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a=a.parse_args();a.out.mkdir(exist_ok=True,parents=True)
f=a.folder;layout=json.loads((f/'layout.json').read_text());review=json.loads(a.review.read_text());dx,dy=review['model_to_gcode_translation_xy_mm']
with zipfile.ZipFile(next(f.glob('*.3mf'))) as z:paths,_=v.parse(z.read('Metadata/plate_1.gcode').decode())
report=[];plots=[]
for n,p in enumerate(layout,1):
 if not p['name'].startswith('point'):continue
 lo,hi=np.array(p['bounds_mm']);cx,cy=(lo[:2]+hi[:2])/2+[dx,dy]
 ps=[q for q in paths if lo[0]+dx-.1< (q['x']+q['x1'])/2<hi[0]+dx+.1 and lo[1]+dy-.1<(q['y']+q['y1'])/2<hi[1]+dy+.1 and q['role']!='Brim']
 zs=sorted(set(q['z'] for q in ps));details=[];previous=None
 for z in zs:
  qs=[q for q in ps if q['z']==z];foot=v.footprint(qs)
  if z>=7.8:
   polys=[g for g in (foot.geoms if hasattr(foot,'geoms') else [foot]) if g.area>.001]
   details.append(dict(z_mm=z,components=len(polys),width_range_mm=[min(q['width'] for q in qs),max(q['width'] for q in qs)],components_bounds_mm=[[g.bounds[0]-cx,g.bounds[1]-cy,g.bounds[2]-cx,g.bounds[3]-cy] for g in polys],component_areas_mm2=[g.area for g in polys],component_previous_layer_overlap_mm2=[g.intersection(previous).area for g in polys] if previous is not None else []))
  previous=foot
 top=details[-1];report.append(dict(index=n,name=p['name'],cad_top_mm=float(hi[2]),top_extrusion_mm=zs[-1],tip_layers=details))
 if not any(q[0]==p['name'].split('#')[0] for q in plots):
  plots.append((p['name'].split('#')[0],cx,cy,ps,zs[-1]))
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(len(plots),3,figsize=(12,4*len(plots)),squeeze=False)
for row,(name,cx,cy,ps,topz) in enumerate(plots):
 for col,want in enumerate([8.12,topz-.08,topz]):
  z=min(set(q['z'] for q in ps),key=lambda t:abs(t-want));qs=[q for q in ps if q['z']==z]
  ax=axs[row,col]
  for q in qs:
   b=LineString([(q['x']-cx,q['y']-cy),(q['x1']-cx,q['y1']-cy)]).buffer(q['width']/2)
   ax.fill(*b.exterior.xy,color='#287eac',alpha=.5)
  ax.set_aspect('equal');ax.set_xlim(-2,2);ax.set_ylim(-2,2);ax.grid(alpha=.25);ax.set_title(f'{name}; real G-code Z={z:.2f} mm')
fig.tight_layout();fig.savefig(a.out/'point-toolpaths.png',dpi=170)
(a.out/'point-paths.json').write_text(json.dumps(dict(samples=report,caveats=['Buffered nominal widths, no physical accuracy claim.','Finite summit is wider than CAD crown; exact symmetric summit-on-summit remains a physical deadband.']),indent=2)+'\n')
print(json.dumps([{k:q[k] for k in ['index','name','cad_top_mm','top_extrusion_mm']} for q in report],indent=2))
