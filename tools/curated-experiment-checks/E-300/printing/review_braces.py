#!/usr/bin/env python3
"""Check custom screw scaffold contact corridors in actual Bambu deposited paths."""
import argparse,collections,importlib.util,json,zipfile
from pathlib import Path
import numpy as np
import trimesh
from shapely.geometry import box
ROOT=Path(__file__).resolve().parents[4]
sp=importlib.util.spec_from_file_location('review',ROOT/'tools/curated-experiment-checks/E-298/printing/validate-project.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--project',type=Path,required=True);ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 with zipfile.ZipFile(a.project) as ar:
  cfg=json.loads(ar.read('Metadata/project_settings.config'));bounds,*_=v.project_bounds(ar);g=ar.read('Metadata/plate_1.gcode').decode()
 layout=json.loads(a.layout.read_text());tree=next(i for i in layout if i['name']=='screw-tree')
 whole=trimesh.load(a.layout.parent/'cone-friction-selector.stl',force='mesh')
 source=trimesh.load(ROOT/tree['source'],force='mesh');local_to_plate=np.array(tree['bounds_mm'])[0]-source.bounds[0]
 no=cfg['extruder_offset'][0];off=np.array([float(x) for x in no.split('x')]);delta=(bounds[0]-whole.bounds[0])[:2]-off+local_to_plate[:2]
 contacts=json.loads((ROOT/'tools/curated-experiment-checks/E-299/cad/tree-contacts.json').read_text())
 paths,_=v.parse(g);layers=collections.defaultdict(list)
 for p in paths:layers[p['z']].append(p)
 records=[]
 for i,c in enumerate(contacts):
  x=c['screw_x']+delta[0];sgn=c['sign'];rad=c.get('radial_contact',1.98)
  zlo,zhi=(c['z']+1-.18,c['z']+1+.18) if c['part']=='threadcrest' else (c['z']+1,c['z']+1+.4)
  ys=sorted([sgn*(rad-.25)+delta[1],sgn*4.1+delta[1]])
  roi=box(x-.65,ys[0],x+.65,ys[1]);screen=[]
  for z,ps in sorted(layers.items()):
   if not zlo+.015 <= z-.06 <= zhi-.015:continue
   local=[p for p in ps if min(p['x'],p['x1'])<=x+.9 and max(p['x'],p['x1'])>=x-.9 and min(p['y'],p['y1'])<=ys[1]+.3 and max(p['y'],p['y1'])>=ys[0]-.3]
   if not local:continue
   footprint=v.footprint(local).intersection(roi).buffer(.005)
   components=list(footprint.geoms) if hasattr(footprint,'geoms') else [footprint]
   contact=box(x-.3,delta[1]+min(sgn*(rad-.20),sgn*(rad+.10)),x+.3,delta[1]+max(sgn*(rad-.20),sgn*(rad+.10)))
   pillar=box(x-.3,delta[1]+sgn*3.8-.3,x+.3,delta[1]+sgn*3.8+.3)
   linked=any(p.intersection(contact).area>.003 and p.intersection(pillar).area>.003 for p in components)
   screen.append(dict(layer_z_mm=z,nominal_layer_center_mm=z-.06,connected_thread_to_pillar=linked,segments=len(local)))
  records.append(dict(index=i,contact=c,center_z_window_mm=[zlo,zhi],layers=screen,at_least_one_connected_layer=any(q['connected_thread_to_pillar'] for q in screen)))
 report=dict(project=a.project.name,contact_source='tools/curated-experiment-checks/E-299/cad/tree-contacts.json (unchanged E-299 screw-tree)',brace_count=len(records),all_braces_have_at_least_one_deposited_connection=all(q['at_least_one_connected_layer'] for q in records),brace_reviews=records,caveat='Nominal line-width footprints and layer centers only. Does not establish bond strength, scaffold stiffness or scar-free physical removal.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='brace_reviews'},indent=2))
if __name__=='__main__':main()
