from pathlib import Path
import sys,collections,json,argparse
sys.path.insert(0,str(Path(__file__).resolve().parent))
from independent_toolpath_review import parse_paths
from shapely.geometry import LineString,Point,box,Polygon
from shapely.ops import unary_union
ap=argparse.ArgumentParser(description='Independent E-295 compact plate all-layer nominal wall and bore footprint screen.')
ap.add_argument('--gcode',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True)
a=ap.parse_args()
p,t=parse_paths(a.gcode)
layers=collections.defaultdict(list)
for q in p:layers[q['z']].append(q)
records=[]
for z,paths in sorted(layers.items()):
 if z>.001 and z<=18.:
  for i in range(5):
   cx=98+i*15;cy=135.5
   local=[q for q in paths if abs((q['x']+q['x1'])/2-cx)<6.2 and abs((q['y']+q['y1'])/2-cy)<6.2]
   if not local:continue
   foot=unary_union([LineString([(q['x'],q['y']),(q['x1'],q['y1'])]).buffer(max(.05,min(1.,q['width']))/2,quad_segs=3) for q in local])
   square=box(cx-1.78,cy-1.78,cx+1.78,cy+1.78).buffer(.20).boundary
   polys=list(foot.geoms) if hasattr(foot,'geoms') else [foot]
   enclosed=any(Polygon(poly.exterior).contains(Point(cx,cy)) and not poly.contains(Point(cx,cy)) for poly in polys if poly.geom_type=='Polygon')
   records.append(dict(bore_enclosed_by_same_layer_wall=enclosed,pin=i+1,z_mm=z,uncovered_wall_skeleton_mm=square.difference(foot.buffer(.01)).length,central_radius_060_free=foot.intersection(Point(cx,cy).buffer(.60)).area<.001))
upper=[r for r in records if r['z_mm']>6.12]
result=dict(pin_layer_samples=len(records),upper_tube_samples=len(upper),upper_tube_enclosed_all_layers=all(r['bore_enclosed_by_same_layer_wall'] for r in upper),lower_thread_layers_with_local_wall_breaks=sum(not r['bore_enclosed_by_same_layer_wall'] for r in records if .24<r['z_mm']<=6.12),max_rounded_midwall_skeleton_gap_mm=max(r['uncovered_wall_skeleton_mm'] for r in records),central_bore_radius_060_free_all_layers=all(r['central_radius_060_free'] for r in records),method='Nominal E/XY bead footprints at exact centered STL positions. Wall closure topology and rounded midwall skeleton (1.98mmhalfwidth) are process diagnostics, not physical hole measurements. Central0.60mm radius test excludes deposited material but doesnot prove a full nominal helical profile.')
a.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
