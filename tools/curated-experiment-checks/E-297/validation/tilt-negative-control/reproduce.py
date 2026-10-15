import numpy as np, trimesh as tm, manifold3d as md, math, json
from pathlib import Path
root=Path(__file__).resolve().parent
def man(m):return md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
def vol(a,b):return abs((man(a)^man(b)).volume())
def moved(m,dx=0,dz=0,deg=0):
 a=m.copy();a.apply_translation([0,0,-.36]);a.apply_transform(tm.transformations.rotation_matrix(math.radians(deg),[0,1,0]));a.apply_translation([dx,0,.36+dz]);return a
rot=tm.load(root/'rotor.stl',force='mesh');comb=tm.load(root/'single-comb.stl',force='mesh')
shaft=tm.load(root/'input-shaft.stl',force='mesh');shaft.apply_translation([0,0,1.2-9.4])
records=[]
for deg in [2.5,2.7,2.8,2.9,3.0,3.1]:
 for dx in [0,.04,.06,.07,.08]:
  a=moved(rot,dx=dx,deg=deg)
  ca=vol(a,comb);sa=vol(a,shaft)
  b=moved(rot,dx=-dx,deg=-deg);b.apply_translation([5.08,0,0])
  vv=vol(a,b)
  if vv>1e-6:records.append(dict(deg=deg,dx=dx,rotor_comb_mm3=ca,rotor_shaft_mm3=sa,neighbor_rotor_mm3=vv,max_x=float(a.bounds[1,0])))
print(json.dumps(records,indent=2))
