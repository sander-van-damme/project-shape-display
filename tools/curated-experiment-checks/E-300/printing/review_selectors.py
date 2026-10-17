#!/usr/bin/env python3
"""Screen actual continuity of the 0.46-mm tall selector back spine.

Part transforms match E-300 generate.py: row and columns X+90.
"""
import argparse,collections,hashlib,importlib.util,json,zipfile
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import Point,LineString
ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('paths',ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 layout=json.loads(a.layout.read_text());whole=trimesh.load(a.layout.parent/'cone-friction-selector.stl',force='mesh')
 with zipfile.ZipFile(a.project) as ar:
  cfg=json.loads(ar.read('Metadata/project_settings.config'));bounds,*_=v.project_bounds(ar);g=ar.read('Metadata/plate_1.gcode').decode()
 delta=(bounds[0]-whole.bounds[0])[:2]-np.array([float(x) for x in cfg['extruder_offset'][0].split('x')]);paths,_=v.parse(g);layers=collections.defaultdict(list)
 for p in paths:layers[p['z']].append(p)
 records=[]
 for part in layout:
  if not part['name'].endswith('-selector'):continue
  source=trimesh.load(ROOT/part['source'],force='mesh');b=np.array(part['bounds_mm']);loc=b[0]-source.bounds[0];xyoff=loc[:2]+delta;row=part['name']=='row-selector';screen=[]
  for z,ps in sorted(layers.items()):
   center=z-.06
   if row:
    if not 10.23<=center<=10.69:continue
    ends=[[-4.7,-.36],[4.7,-.36]]
   else:
    if not 11.23<=center<=11.69:continue
    ends=[[-2.1,-.36],[2.1,-.36]]
   line=LineString([np.array(p)+xyoff for p in ends]);lo=b[0,:2]+delta-.1;hi=b[1,:2]+delta+.1
   local=[p for p in ps if lo[0]<=(p['x']+p['x1'])/2<=hi[0] and lo[1]<=(p['y']+p['y1'])/2<=hi[1]]
   foot=v.footprint(local);missing=line.difference(foot);pieces=list(missing.geoms) if hasattr(missing,'geoms') else [missing];polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
   linked=any(q.buffer(.005).covers(Point(line.coords[0])) and q.buffer(.005).covers(Point(line.coords[-1])) for q in polys)
   screen.append(dict(layer_z_mm=z,layer_center_mm=center,check_line_xy_mm=list(line.coords),material_fraction=1-missing.length/line.length,max_gap_mm=max((q.length for q in pieces),default=0.),both_ends_in_same_material_component=linked))
  records.append(dict(name=part['name'],source_bounds_mm=b.tolist(),layers=screen))
 report=dict(project=a.project.name,project_sha256=hashlib.sha256(a.project.read_bytes()).hexdigest(),nominal_spine_thickness_mm=.46,selector_reviews=records,caveat='Nominal line-width footprints on specific continuous-spine lines only. Does not prove print fusion, layer adhesion, shear capacity, creep or selection-force capacity.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(selector_objects=len(records),examined_layers=sum(len(r['layers']) for r in records)),indent=2))
if __name__=='__main__':main()
