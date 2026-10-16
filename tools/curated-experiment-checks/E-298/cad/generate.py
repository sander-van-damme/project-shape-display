#!/usr/bin/env python3
"""E298 pointed mating faces; unchanged E297 components loaded as immutable sources.
Run from repository root. CAD crown is not a claim of achievable printed sharpness.
"""
from pathlib import Path
import importlib.util,json,math,hashlib,shutil
import numpy as np
import cadquery as cq
import trimesh as tm
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OLD=HERE.parents[1]/'E-297'/'cad'
spec=importlib.util.spec_from_file_location('e297',OLD/'generate.py'); old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
OUT=HERE/'parts';OUT.mkdir(parents=True,exist_ok=True)
old.OUT=OUT
VARIANTS={'point48':dict(taper=.48,skew=0.),'point60':dict(taper=.60,skew=0.),'point60skew':dict(taper=.60,skew=12.)}
CROWN=.30; WIDTH=math.degrees(CROWN/1.2)

def wire(ri,ro,width,angle,z):
 aa=np.linspace(angle-width/2,angle+width/2,25)*math.pi/180
 pts=[cq.Vector(ro*math.cos(a),ro*math.sin(a),z) for a in aa]
 pts += [cq.Vector(ri*math.cos(a),ri*math.sin(a),z) for a in aa[::-1]]
 return cq.Wire.makePolygon(pts+[pts[0]])
def rotor(taper=.48,skew=0.):
 b=old.cyl(2.15,.72).fuse(old.cyl(1.6,1.29,.71)).fuse(old.cone(1.6,1.8,.2,2)).fuse(old.cyl(1.8,4.01,2.19))
 w0=wire(.6,1.8,76,0,6.2)
 w1=wire(.6,1.8,76,0,8.6-taper)
 w2=wire(1.2-CROWN/2,1.2+CROWN/2,WIDTH,skew,8.6)
 dog=cq.Solid.makeLoft([w0,w1,w2],True)
 b=b.fuse(dog).fuse(dog.rotate((0,0,0),(0,0,1),180))
 return b.cut(old.dd(2.5,1.9,5.49,-.01)).clean()
def reaction_jig():
 # Temporary test fixture, top of plate at assembled z=-.2; four plugs enter lower sockets.
 b=old.box(-6,-6,0,12,12,2)
 for x in [-2.54,2.54]:
  for y in [-2.54,2.54]: b=b.fuse(old.dd(2.2,1.6,2.4,1.99).translate((x,y,0)))
 return b.clean()
def import_old(label):
 for suffix in ['.step','.stl','-print.stl']:
  src=OLD/'parts'/(label+suffix)
  if src.exists():shutil.copyfile(src,OUT/(label+suffix))
 old.MESHES[label]=tm.load(OUT/(label+'.stl'),force='mesh')
 return tm.load(OUT/(label+'-print.stl'),force='mesh')
def plate(name,items,dest):
 positioned=[];manifest=[];cx=5.;cy=5.;rh=0
 for label,m in items:
  mm=m.copy();sz=mm.extents
  if cx+sz[0]>145:cx=5;cy+=rh+5;rh=0
  mm.apply_translation([cx-mm.bounds[0,0],cy-mm.bounds[0,1],-mm.bounds[0,2]])
  positioned.append(mm);manifest.append(dict(name=label,bounds_mm=mm.bounds.tolist(),source=str((OUT/(label.split('#')[0]+'-print.stl')).relative_to(ROOT))))
  cx+=sz[0]+4;rh=max(rh,sz[1])
 dest.mkdir(parents=True,exist_ok=True)
 tm.util.concatenate(positioned).export(dest/(name+'.stl'))
 (dest/'layout.json').write_text(json.dumps(manifest,indent=2)+'\n')

def main():
 exp={name:old.export_part(name,rotor(**p)) for name,p in VARIANTS.items()}
 for label in ['frame-left','frame-center','frame-right','row-selector','single-comb','input-shaft','screw','pin','hand-key','stop-spacer','coupon-shaft']:exp[label]=import_old(label)
 exp['reaction-jig']=old.export_part('reaction-jig',reaction_jig())
 a=[]
 for label in VARIANTS:
  for i in range(4): a.append((label+f'#{i+1}',exp[label]))
 for label,n in [('coupon-shaft',4),('single-comb',2)]:a += [(label+f'#{i+1}',exp[label]) for i in range(n)]
 plate('point-fit',a,ROOT/'owner-print-tests/2026-10-16-self-aligning-point-fit')
 b=[]
 for label,n in [('frame-left',1),('frame-right',1),('frame-center',1),('row-selector',4),('point48',8),('input-shaft',4),('screw',4),('pin',4),('hand-key',1),('stop-spacer',8),('reaction-jig',1)]:
  b += [(label+f'#{i+1}',exp[label]) for i in range(n)]
 plate('point-matrix',b,ROOT/'owner-print-tests/2026-10-16-self-aligning-point-matrix')
 old.MESHES['rotor']=old.MESHES['point48']
 for tag,r,c in [('off',(0,0),(0,0)),('r0-c0',(1,0),(1,0)),('all-on',(1,1),(1,1))]:
  assembled=old.assembly(r,c)
  assembled['reaction-jig']=old.shift(old.MESHES['reaction-jig'],[0,0,-2.2])
  tm.util.concatenate(list(assembled.values())).export(HERE/('assembly-'+tag+'.stl'))
 params=dict(old.PARAMS);params.pop('tip_chamfer',None);params.update(experiment='E-298',variants=VARIANTS,crown_radial_width=CROWN,crown_angular_width_deg=WIDTH,matrix_variant='point48',unchanged_component_source='E-297/cad/parts',two_identical_halves=True)
 (HERE/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
 records={k:dict(extents_mm=v.extents.tolist(),volume_mm3=float(v.volume),watertight=bool(v.is_watertight),sha256=hashlib.sha256((OUT/(k+'.stl')).read_bytes()).hexdigest()) for k,v in old.MESHES.items() if (OUT/(k+'.stl')).exists()}
 (HERE/'mesh-validation.json').write_text(json.dumps(records,indent=2)+'\n')
 print('Exported 18part TestA,37part TestB',flush=True)
if __name__=='__main__':main()
