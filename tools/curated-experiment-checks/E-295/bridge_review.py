from pathlib import Path
import sys, collections, json, math, argparse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from independent_toolpath_review import parse_paths
from shapely.geometry import LineString,Point
from shapely.ops import unary_union
ap=argparse.ArgumentParser(description='Inspect unsupported bridge centerline spans against previous-layer nominal extrusion footprints; not physical validation.')
ap.add_argument('--gcode',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
a=ap.parse_args()
pp,txt=parse_paths(a.gcode)
layers=collections.defaultdict(list)
for p in pp: layers[p['z']].append(p)
previous=None; rows=[]
for z,ps in sorted(layers.items()):
 if previous is not None:
  prev=previous.buffer(.01)
  for p in ps:
   if p['role'] not in ['Bridge infill','Overhang perimeter']:continue
   line=LineString([(p['x'],p['y']),(p['x1'],p['y1'])])
   unsupported=line.difference(prev)
   comps=list(unsupported.geoms) if hasattr(unsupported,'geoms') else [unsupported]
   longest=max((s.length for s in comps),default=0)
   rows.append(dict(**p,max_free_centerline_mm=longest,start_distance_mm=Point(p['x'],p['y']).distance(prev),end_distance_mm=Point(p['x1'],p['y1']).distance(prev)))
 previous=unary_union([LineString([(p['x'],p['y']),(p['x1'],p['y1'])]).buffer(max(.05,min(1.,p['width']))/2,quad_segs=3) for p in ps])
a.output.write_text(json.dumps(rows,indent=2)+'\n')
for role in ['Bridge infill','Overhang perimeter']:
 s=[x for x in rows if x['role']==role]
 print(role,'max span',max(x['max_free_centerline_mm'] for x in s))
 print('Endpoint gaps >.25',sum(1 for x in s if x['start_distance_mm']>.25 or x['end_distance_mm']>.25))
 for z in sorted(set(x['z'] for x in s)):
  zz=[x for x in s if x['z']==z]
  print(z,'free_max',round(max(x['max_free_centerline_mm'] for x in zz),3),'anchor_distance_max',round(max(max(x['start_distance_mm'],x['end_distance_mm']) for x in zz),3))
