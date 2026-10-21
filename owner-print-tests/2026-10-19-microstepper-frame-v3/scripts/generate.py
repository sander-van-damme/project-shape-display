"""Rebuild exact E-301 mesh-derived rotor and v3 parts with OpenSCAD."""
import subprocess,json,hashlib,sys
import numpy as np
import trimesh
import manifold3d as md
def solid(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
from paths import *
if json.loads((METADATA / "motor-interface.json").read_text())["status"] != "READY" and "--draft" not in sys.argv:
    raise SystemExit("DRAFT/BLOCKED: motor interface unresolved; see verification.md. Use --draft for engineering meshes only.")

parts={}
for name,part,t in [('front','front',.6),('back','back',.6),('rotor','rotor-base',.6),('pin','pin',.6),('pin-50','pin-50',.6),('rotor-long','rotor-base',.6),('spacer-060','spacer',.6),('spacer-072','spacer',.72),('spacer-084','spacer',.84)]:
 p=COMPONENTS/(name+'.stl')
 result=subprocess.run(['openscad','-o',str(p),'-D',f'part="{part}"','-D',f'shim={t}',str(CAD/'rig.scad')],check=True,capture_output=True)
 assert b'ERROR' not in result.stderr,result.stderr.decode()
 m=trimesh.load(p,force='mesh')
 if part=='rotor-base':
  source='screw-long.stl' if name=='rotor-long' else 'screw.stl'
  length=48 if name=='rotor-long' else 16
  original=trimesh.load(TEST_DIR.parent/'2026-10-18-microstepper-frame-v2/components'/source,force='mesh')
  thread=solid(original)^md.Manifold.cube([4,4,length+.01]).translate([-2,-2,2.399])
  joined=solid(m)+thread.translate([0,0,9.6])
  mesh=joined.to_mesh();m=trimesh.Trimesh(mesh.vert_properties,mesh.tri_verts)
 assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
 m.apply_translation([0,0,-m.bounds[0,2]]);m.export(p);parts[name]=m
# Generate sacrificial towers only after the clean functional long rotor exists.
p=COMPONENTS/'rotor-long-supported.stl'
result=subprocess.run(['openscad','-o',str(p),str(CAD/'long-screw-supported.scad')],check=True,capture_output=True)
assert b'ERROR' not in result.stderr,result.stderr.decode()
m=trimesh.load(p,force='mesh');assert m.is_watertight and m.is_winding_consistent and len(m.split())==1
m.export(p);parts['rotor-long-supported']=m
layout=[];meshes=[]
for name,x,y,label in [('front',18,2,'front'),('back',53,2,'back'),('pin-50',83,20,'pin-50'),('rotor-long-supported',83,54,'rotor-long-supported'),('rotor',10,82,'rotor'),('pin',24,82,'pin'),('spacer-060',36,78,'S060'),('spacer-072',44,78,'S072a'),('spacer-072',52,78,'S072b'),('spacer-084',60,78,'S084')]:
 m=parts[name].copy();m.apply_translation([x,y,0]);meshes.append(m)
 layout.append(dict(name=label,source=name,bounds_mm=m.bounds.tolist(),center_xy=[x,y]))
plate=trimesh.util.concatenate(meshes);plate.export(COMPONENTS/'microstepper-frame-v3.stl')
(METADATA/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(METADATA/'geometry.json').write_text(json.dumps(dict(bounds_mm=plate.bounds.tolist(),parts={n:dict(bounds=m.bounds.tolist(),volume_mm3=m.volume,watertight=m.is_watertight,sha256=hashlib.sha256((COMPONENTS/(n+'.stl')).read_bytes()).hexdigest())for n,m in parts.items()}),indent=2)+'\n')
print(plate.bounds)
