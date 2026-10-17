#!/usr/bin/env python3
"""Inspect actual PLA cone paths: female annulus and male contact boundary.

Nominal deposited LINE_WIDTH footprints, never physical contact/torque evidence.
"""
import argparse,collections,hashlib,importlib.util,json,math,zipfile
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point,Polygon,LineString
ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('paths',ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 layout=json.loads(a.layout.read_text());whole=trimesh.load(a.layout.parent/'cone-friction-selector.stl',force='mesh')
 with zipfile.ZipFile(a.project) as ar:
  cfg=json.loads(ar.read('Metadata/project_settings.config'));bounds,*_=v.project_bounds(ar);g=ar.read('Metadata/plate_1.gcode').decode()
 off=np.array([float(x) for x in cfg['extruder_offset'][0].split('x')]);delta=(bounds[0]-whole.bounds[0])[:2]-off
 paths,_=v.parse(g);layers=collections.defaultdict(list)
 for p in paths:layers[p['z']].append(p)
 records=[]
 for part in layout:
  if part['name'] not in ['male-rotor','female-rotor']:continue
  b=np.array(part['bounds_mm']);xy=b.mean(axis=0)[:2]+delta;lo=b[0,:2]+delta-.1;hi=b[1,:2]+delta+.1;female=part['name']=='female-rotor';zs=(8.56,9.21) if female else (6.2,6.7);screen=[]
  for z,ps in sorted(layers.items()):
   center=z-.06
   if not zs[0]<=center<=zs[1]:continue
   local=[p for p in ps if lo[0]<=(p['x']+p['x1'])/2<=hi[0] and lo[1]<=(p['y']+p['y1'])/2<=hi[1]]
   foot=v.footprint(local);polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot];point=Point(*xy)
   if female:
    inner=1.3+center-8.56;radius=(inner+2.35)/2
   else:inner=0.;radius=1.9-(center-6.2)-.12
   circle=LineString([tuple(xy+radius*np.array([math.cos(t),math.sin(t)])) for t in np.linspace(0,2*math.pi,721)])
   missing=circle.difference(foot);gaps=list(missing.geoms) if hasattr(missing,'geoms') else [missing]
   screen.append(dict(layer_z_mm=z,layer_center_mm=center,expected_inner_radius_mm=inner,checked_ring_radius_mm=radius,checked_ring_material_fraction=1-missing.length/circle.length,max_checked_ring_gap_mm=max((q.length for q in gaps),default=0.),axis_clearance_mm=point.distance(foot),axis_enclosed_by_open_hole=any(Polygon(h).contains(point) for p in polys for h in p.interiors),component_count=sum(p.area>.005 for p in polys)))
  records.append(dict(name=part['name'],source_bounds_mm=b.tolist(),layers=screen))
 report=dict(project=a.project.name,project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),cone_reviews=records,caveat='Nominal toolpath footprint and layer centers. Does not prove surface roughness, fit, actual cone contact area, friction, breakaway or release.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(project=a.project.name,cone_objects=len(records),examined_layers=sum(len(q['layers']) for q in records)),indent=2))
if __name__=='__main__':main()
