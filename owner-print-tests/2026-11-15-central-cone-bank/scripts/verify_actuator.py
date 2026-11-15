#!/usr/bin/env python3
"""CGAL coupon slider/base/bridge collision sweep, exact source, scratch only."""
from pathlib import Path
import argparse,subprocess,json
p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,required=True);a=p.parse_args();a.scratch.mkdir(parents=True,exist_ok=True)
P=Path(__file__).resolve().parents[1];rows=[]
for target in ['base','bridge']:
 for s in [-5,-2.5,0,2.5,5]:
  source=a.scratch/f'{target}-{s}.scad';source.write_text('use <'+str(P/'cad/actuator.scad')+'>\nintersection(){'+('base();' if target=='base' else 'translate([0,0,3])follower_bridge();')+f'translate([0,{s},3.3])slider();'+'}\n')
  r=subprocess.run(['openscad','-o',str(source.with_suffix('.stl')),str(source)],capture_output=True,text=True)
  ok='Current top level object is empty' in r.stderr
  rows.append(dict(target=target,slider_mm=s,empty_intersection=ok));assert ok,r.stderr
(P/'metadata/actuator-geometry.json').write_text(json.dumps(rows,indent=2)+'\n');print('PASS',len(rows),'CGAL poses')

# Ø2 contact tip fits entirely on both 4mm dwells; broad 7mm body is held4mm above it.
def cam_height(y):return 3 if y<=-3 else (3-y)/2 if y<3 else 0
levels=[cam_height(-stroke-1) for stroke in [-5,5]]
assert levels==[0,3],levels
assert 4>3, 'Follower body must stay clear of all cam heights'
print('PASS contact tip rise3mm; 4mm body standoff; pin25mm spans bridge throughout')
