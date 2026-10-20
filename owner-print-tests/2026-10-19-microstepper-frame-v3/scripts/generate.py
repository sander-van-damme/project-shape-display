"""Rebuild exact E-301 mesh-derived rotor and v3 parts with OpenSCAD."""
import subprocess,json,hashlib
import numpy as np
import trimesh
import manifold3d as md
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
from paths import *
parts={}
for name,part,t in [('front','front',.6),('back','back',.6),('rotor','rotor-base',.6),('pin','pin',.6),('spacer-060','spacer',.6),('spacer-072','spacer',.72),('spacer-084','spacer',.84)]:
 p=COMPONENTS/(name+'.stl')
 result=subprocess.run(['openscad','-o',str(p),'-D',f'part="{part}"','-D',f'shim={t}',str(CAD/'rig.scad')],check=True,capture_output=True)
 assert b'ERROR' not in result.stderr,result.stderr.decode()
 m=trimesh.load(p,force='mesh')
 if part=='rotor-base':
  original=trimesh.load(TEST_DIR.parent/'2026-10-18-microstepper-frame-v2/components/screw.stl',force='mesh')
  thread=solid(original)^md.Manifold.cube([4,4,16.01]).translate([-2,-2,2.399])
  joined=solid(m)+thread.translate([0,0,9.6])
  mesh=joined.to_mesh();m=trimesh.Trimesh(mesh.vert_properties,mesh.tri_verts)
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
 m.apply_translation([0,0,-m.bounds[0,2]]);m.export(p);parts[name]=m
layout=[];meshes=[]
for name,x,y,label in [('front',18,2,'front'),('back',53,2,'back'),('rotor',10,50,'rotor'),('pin',24,50,'pin'),('spacer-060',36,46,'S060'),('spacer-072',44,46,'S072a'),('spacer-072',52,46,'S072b'),('spacer-084',60,46,'S084')]:
 m=parts[name].copy();m.apply_translation([x,y,0]);meshes.append(m)
 layout.append(dict(name=label,source=name,bounds_mm=m.bounds.tolist(),center_xy=[x,y]))
plate=trimesh.util.concatenate(meshes);plate.export(COMPONENTS/'microstepper-frame-v3.stl')
(METADATA/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(METADATA/'geometry.json').write_text(json.dumps(dict(bounds_mm=plate.bounds.tolist(),parts={n:dict(bounds=m.bounds.tolist(),volume_mm3=m.volume,watertight=m.is_watertight,sha256=hashlib.sha256((COMPONENTS/(n+'.stl')).read_bytes()).hexdigest())for n,m in parts.items()}),indent=2)+'\n')
print(plate.bounds)
