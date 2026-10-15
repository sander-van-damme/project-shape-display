from pathlib import Path
import math,json,hashlib
import numpy as np,trimesh as tm,manifold3d as md
ROOT=Path(__file__).resolve().parent
def man(m):return md.Manifold(md.Mesh(np.array(m.vertices,dtype=np.float32),np.array(m.faces,dtype=np.uint32)))
def meshman(m):
 q=m.to_mesh();return tm.Trimesh(q.vert_properties[:,:3],q.tri_verts,process=False)
def vol(a,b):return abs((a^b).volume())
def translate(m,xyz):return m.translate(xyz)
def shaft_shift(m,sx,sy,z):return translate(m,[sx,sy,z])
def rotor_moved(rot,theta,az,shift,dz):
 axis=[-math.sin(az),math.cos(az),0]
 m=rot.copy();m.apply_translation([0,0,-.36]);m.apply_transform(tm.transformations.rotation_matrix(theta,axis));m.apply_translation([shift*math.cos(az),shift*math.sin(az),.36+dz]);return m
parts=ROOT/'cad/parts'
rot=tm.load(parts/'rotor.stl',force='mesh');comb=man(tm.load(parts/'single-comb.stl',force='mesh'));shaft=man(tm.load(parts/'input-shaft.stl',force='mesh'))
# Fixed guide is the actual 4.0mm circular opening, modeled over a local finite square large enough for the rotor.
def guide(z,d=4):
 block=tm.creation.box([10,10,1.2]);block.apply_translation([0,0,z+.6]);hole=tm.creation.cylinder(radius=d/2,height=1.4,sections=160);hole.apply_translation([0,0,z+.6]);return man(block)-man(hole)
result={'kind':'finite actual mesh wobble checks, not a proof of all friction/print tolerances','cad_sha256':{f:hashlib.sha256((parts/f).read_bytes()).hexdigest() for f in ['rotor.stl','single-comb.stl','input-shaft.stl']},'old_negative_case_replay':[],'samples':[]}
for state in [0,1]:
 base=7+2.4*state;gd=guide(11.8-base)
 for dx,deg in [(.06,3),(.06,3.1)]:
  m=rotor_moved(rot,math.radians(deg),0,dx,0);mm=man(m)
  result['old_negative_case_replay'].append(dict(state=state,deg=deg,dx=dx,comb_overlap=vol(mm,comb),shaft_overlap=vol(mm,shaft_shift(shaft,0,0,1.2-base)),new_fixed_guide_overlap=vol(mm,gd)))
for diameter in [4.0,4.1]:
 for state in [0,.5,1]:
  base=7+2.4*state;gd=guide(11.8-base,diameter)
  legal=[];checks=0
  for azdeg in range(0,360,45):
   az=math.radians(azdeg)
   for deg in [0,1,2,3,4,5,6]:
    th=math.radians(deg)
    for offset in [-.20,-.10,0,.10,.20]:
     # Approximate a best-centered input shaft within its explicitly swept +/-0.2mm transverse range.
     ddmid=(11.92-base)/2
     ideal=offset+(ddmid-.36)*math.sin(th)
     shaftoff=max(-.2,min(.2,ideal))
     sf=shaft_shift(shaft,shaftoff*math.cos(az),shaftoff*math.sin(az),1.2-base)
     for dz in [-.08,0,.08]:
      m=rotor_moved(rot,th,az,offset,dz);mm=man(m);checks+=1
      if vol(mm,gd)>1e-6 or vol(mm,sf)>1e-6:continue
      for coff in [-.2,0,.2]:
       cb=translate(comb,[coff*math.cos(az),coff*math.sin(az),0])
       if vol(mm,cb)>1e-6:continue
       radius=float(np.linalg.norm(m.vertices[:,:2],axis=1).max())
       legal.append(dict(deg=deg,azimuth_deg=azdeg,offset_mm=offset,z_offset_mm=dz,selector_offset_mm=coff,shaft_offset_mm=shaftoff,max_radius_mm=radius))
  worst=max(legal,key=lambda d:d['max_radius_mm'])
  result['samples'].append(dict(guide_diameter_mm=diameter,state_fraction=state,checked_orientations=checks,legal_sample_count=len(legal),worst=worst,conservative_pair_gap_of_sampled_envelopes_mm=5.08-2*worst['max_radius_mm']))
print(json.dumps(result,indent=2))
