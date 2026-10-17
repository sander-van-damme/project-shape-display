#!/usr/bin/env python3
"""Screen both supported screw thread cores in actual deposited paths."""
import argparse,collections,importlib.util,json,zipfile,math
from pathlib import Path
import numpy as np
from shapely.geometry import Point,box
ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('v',ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--project',type=Path,required=True);ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 r=json.loads(a.review.read_text());delta=np.array(r['geometry']['source_to_gcode_translation_xy_mm']);layout=json.loads(a.layout.read_text());tree=next(x for x in layout if x['name']=='screw-tree');center=np.array(tree['bounds_mm']).mean(axis=0)[:2]+delta
 with zipfile.ZipFile(a.project) as z:paths,_=v.parse(z.read('Metadata/plate_1.gcode').decode())
 layers=collections.defaultdict(list)
 for p in paths:layers[p['z']].append(p)
 screws=[]
 for dx in [-5,5]:
  cx,cy=center+[dx,0];samples=[];core=Point(cx,cy).buffer(.45)
  for z,ps in sorted(layers.items()):
   if not 11.04<=z<=26.4:continue
   local=[p for p in ps if abs((p['x']+p['x1'])/2-cx)<2.1 and abs((p['y']+p['y1'])/2-cy)<2.1]
   foot=v.footprint(local).intersection(box(cx-2,cy-2,cx+2,cy+2));polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
   samples.append(dict(z_mm=z,core_radius_045_coverage=foot.intersection(core).area/core.area,components_over_002mm2=sum(p.area>.02 for p in polys),max_material_radius_mm=max((math.hypot(x-cx,y-cy) for p in polys for x,y in p.exterior.coords),default=0.)))
  screws.append(dict(local_screw_x_mm=dx,examined_layers=len(samples),minimum_core_coverage=min(p['core_radius_045_coverage'] for p in samples),max_components=max(p['components_over_002mm2'] for p in samples),minimum_crest_material_radius_mm=min(p['max_material_radius_mm'] for p in samples),samples=samples))
 a.out.write_text(json.dumps(dict(project=a.project.name,screws=screws,caveat='Deposited footprint continuity only. Crest radius may include scaffold contact lips; this does not prove exact thread dimensions or physical fit.'),indent=2)+'\n');print(json.dumps([{k:v for k,v in q.items() if k!='samples'} for q in screws],indent=2))
if __name__=='__main__':main()
