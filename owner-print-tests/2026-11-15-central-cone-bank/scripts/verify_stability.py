#!/usr/bin/env python3
"""Check sacrificial brace connectivity and actual deposited tie contacts, not strength."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util
import numpy as np,trimesh,manifold3d as md
from shapely.geometry import LineString,Point
p=argparse.ArgumentParser();p.add_argument('--project',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();P=Path(__file__).resolve().parents[1]
def solid(m):return md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
specs={'pin-supported':dict(clean='pin',face=2.25,post=5.5,top=35.5,ties=[8,17,26,35]),'male-supported':dict(clean='male',face=1,post=4.25,top=14.8,ties=[6,10.2,14.4])}
report=dict(scope='Nominal geometry and deposited tie contacts; no physical wobble/adhesion/removal guarantee',geometry=[],printed=[])
for name,s in specs.items():
 mesh=trimesh.load(P/'components'/(name+'.stl'),force='mesh');clean=solid(trimesh.load(P/'components'/(s['clean']+'.stl'),force='mesh'));whole=solid(mesh)
 assert mesh.is_watertight and mesh.is_winding_consistent and len(mesh.split())==1,name
 missing=abs((clean-whole).volume());assert missing<1e-5,(name,missing)
 if s['clean']=='pin':
  extra_inside=abs(((whole-clean)^md.Manifold.cube([4.5,4.5,40]).translate([-2.25,-2.25,0])).volume());assert extra_inside<1e-5,extra_inside
 else:extra_inside=None
 for z in [.12,*s['ties'],s['top']-.1]:
  section=whole.slice(z)
  for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
   area=(section^md.CrossSection.square([1.8,1.8]).translate([dx*s['post']-.9,dy*s['post']-.9])).area();assert area>3.2,(name,z,area)
 report['geometry'].append(dict(part=name,clean_geometry_missing_mm3=missing,extra_material_in_pin_envelope_mm3=extra_inside,connected_bodies=1,four_towers=True,tie_heights_mm=s['ties'],maximum_unbraced_height_mm=max(np.diff([0,*s['ties'],mesh.bounds[1,2]]))))
if a.project:
 rs=importlib.util.spec_from_file_location('reader',P.parents[1]/'owner-print-tests/validate-bambu-project.py');r=importlib.util.module_from_spec(rs);rs.loader.exec_module(r)
 with zipfile.ZipFile(a.project) as z:
  paths,_=r.parse(z.read('Metadata/plate_1.gcode').decode());bounds,*_=r.project_bounds(z);cfg=json.loads(z.read('Metadata/project_settings.config'))
 job=a.project.stem;layout=json.loads((P/'metadata/layout.json').read_text())[job];original=np.array([v['bounds_mm'] for v in layout]);shift=bounds[0]-original[:,0,:].min(axis=0);off=cfg['extruder_offset'][0];shift[:2]-=np.array([float(v) for v in off.split('x')])
 report['project_sha256']=hashlib.sha256(a.project.read_bytes()).hexdigest()
 for item in layout:
  if item['source'] not in specs:continue
  s=specs[item['source']];center=np.array(item['center_xy'])+shift[:2];lo,hi=np.array(item['bounds_mm'])+shift;groups={}
  for q in paths:
   if 'support' in q['role'].lower() or q['role'] in ['Brim','Skirt']:continue
   if lo[0]-.03<=(q['x']+q['x1'])/2<=hi[0]+.03 and lo[1]-.03<=(q['y']+q['y1'])/2<=hi[1]+.03:groups.setdefault(q['z'],[]).append(q)
  ties=[]
  for z in s['ties']:
   levels=[zz for zz in groups if abs(zz-z)<.125];fp=r.footprint([q for zz in levels for q in groups[zz]]).buffer(.02)
   for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:
    line=LineString([center+np.array([dx,dy])*(s['face']-.1),center+np.array([dx,dy])*(s['face']+.40)])
    covered=line.intersection(fp).length/line.length;assert covered>.95,(item['name'],z,dx,dy,covered)
    ties.append(dict(z_mm=z,direction=[dx,dy],deposited_neck_fraction=covered))
  fp=r.footprint(groups[min(groups)])
  for dx,dy in [(1,0),(0,1),(-1,0),(0,-1)]:assert fp.intersection(Point(*(center+np.array([dx,dy])*s['post'])).buffer(.6)).area>.9,item['name']
  report['printed'].append(dict(name=item['name'],source=item['source'],tie_checks=ties,bed_feet_deposited=True))
a.output.write_text(json.dumps(report,indent=2)+'\n');print('PASS geometry',len(report['geometry']),'supported prints',len(report['printed']))
