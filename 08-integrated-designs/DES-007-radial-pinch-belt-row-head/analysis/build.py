#!/usr/bin/env python3
"""Export actual printable parts and assembly meshes. Generated files go to --output.
Requires OpenSCAD, pinned BOSL2, numpy/trimesh/manifold3d. Never runs printer G-code.
"""
import argparse, json, os, subprocess, concurrent.futures
from pathlib import Path
import numpy as np
import trimesh
HERE=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bosl2',required=True,type=Path);ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
 out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,OPENSCADPATH=str(args.bosl2.resolve().parent))
 jobs=[('load_probe','load_probe',1,{}),('foot','foot',1,{}),('keeper','keeper',1,{}),('guide','guide',2,{}),('roof','roof',1,{}),
       ('head','head',1,{}),('head_cover','head_cover',1,{}),('shoe_base','shoe_base',4,{}),('shoe_tip','shoe_tip',4,{}),('pin','pin',8,{}),
       ('screw_high','supported_screw',4,{'row':0}),('screw_low','supported_screw',4,{'row':1}),('belt','belt',1,{})]
 for r in range(3):jobs.append((f'upper_{r}','upper_piece',2,{'row':r}))
 for h in [2,2.2,7.2,8,12,12.2,27]:jobs.append((f'spacer_{h:g}','spacer',2 if h==2 else 6,{'q':h}))
 def export(job):
  name,part,qty,params=job
  cmd=['openscad','-o',str(out/(name+'.stl')),'-D',f'part="{part}"']
  for k,v in params.items():cmd+=['-D',f'{k}={v}']
  cmd.append(str(HERE/'cad/rig.scad'))
  r=subprocess.run(cmd,env=env,capture_output=True,text=True)
  (out/(name+'.log')).write_text(r.stdout+r.stderr)
  if r.returncode or 'ERROR:' in r.stderr:raise RuntimeError(name+':'+r.stderr)
  m=trimesh.load_mesh(out/(name+'.stl'));m.remove_unreferenced_vertices()
  # OpenSCAD ASCII export precision can create zero-area facets; no hole repair.
  m.update_faces(m.nondegenerate_faces());m.merge_vertices();m.fix_normals()
  assert m.is_watertight and m.is_winding_consistent and m.volume>0,(name,m.is_watertight)
  m.export(out/(name+'-raw.stl'))
  m.apply_translation(-m.bounds[0]);m.export(out/(name+'.stl'))
  return name,qty,m
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:meshes=list(pool.map(export,jobs))
 # Two PLA plates keep tall screw supports separate; flexible strip is separate material.
 plates={'structure':[], 'columns':[], 'flexible':[]};cursor={k:[0,0,0] for k in plates};manifest={}
 for name,qty,m in meshes:
  group='flexible' if name=='belt' else ('columns' if name.startswith('screw') or name=='pin' else 'structure')
  manifest[name]=dict(quantity=qty,size_mm=m.extents.tolist(),volume_mm3=float(m.volume),bodies=len(m.split()))
  for j in range(qty):
   x,y,rowheight=cursor[group];w,d,h=m.extents
   if x+w>220:x=0;y+=rowheight+5;rowheight=0
   cp=m.copy();cp.apply_translation([x,y,0]);plates[group].append(cp)
   cursor[group]=[x+w+5,y,max(rowheight,d)]
 for name,parts in plates.items():
  m=trimesh.util.concatenate(parts);assert m.bounds[1][0]<=256 and m.bounds[1][1]<=256
  m.export(out/(name+'-plate.stl'))
  manifest[name+'-plate']=dict(size_mm=m.extents.tolist(),volume_mm3=float(m.volume),bodies=len(m.split()))
 pla=trimesh.util.concatenate(plates['structure'])
 cols=trimesh.util.concatenate(plates['columns']);cols.apply_translation([0,pla.bounds[1][1]+6,0])
 pla=trimesh.util.concatenate([pla,cols]);assert np.all(pla.extents[:2]<250)
 pla.export(out/'rig-pla-plate.stl')
 manifest['rig-pla-plate']=dict(size_mm=pla.extents.tolist(),volume_mm3=float(pla.volume),bodies=len(pla.split()))
 (out/'mesh-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({k:v for k,v in manifest.items() if k.endswith('plate')},indent=2))
if __name__=='__main__':main()
