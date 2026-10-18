#!/usr/bin/env python3
"""Run from any directory with openscad, numpy, trimesh, matplotlib installed."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
H=Path(__file__).resolve().parent
parts={}
for name,part,r in [('half-front','half-front',1),('half-back','half-back',1),('screw','screw',1),('pin-18','pin-18',1),('pin-50','pin-50',1),('coupling-A','cup',.95),('coupling-N','cup',1),('coupling-C','cup',1.05)]:
 subprocess.run(['openscad','-o',str(H/(name+'.stl')),'-D',f'part="{part}"','-D',f'tip_r={r}',str(H/'rig.scad')],check=True,capture_output=True)
 m=trimesh.load(H/(name+'.stl'),force='mesh'); assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
 m.export(H/(name+'.stl'));parts[name]=m
layout=[];meshes=[]
for name,x,y,label in [('half-front',20,44,'frame-front'),('half-back',60,44,'frame-back'),('coupling-A',10,57,'A'),('coupling-N',27,57,'N1'),('coupling-N',44,57,'N2'),('coupling-C',61,57,'C'),('screw',10,75,'screw-1'),('screw',27,75,'screw-2'),('pin-18',44,75,'pin-18'),('pin-50',61,75,'pin-50')]:
 m=parts[name].copy();m.apply_translation([x,y,0]);meshes.append(m)
 layout.append(dict(name=label,source=name,bounds_mm=m.bounds.tolist(),center_xy=[x,y]))
plate=trimesh.util.concatenate(meshes);plate.export(H/'microstepper-frame-v2.stl')
(H/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(H/'geometry-validation.json').write_text(json.dumps(dict(body_count=len(meshes),bounds_mm=plate.bounds.tolist(),parts={n:dict(volume_mm3=m.volume,watertight=m.is_watertight,sha256=hashlib.sha256((H/(n+'.stl')).read_bytes()).hexdigest()) for n,m in parts.items()},scope='CAD only; physical fitting unknown'),indent=2)+'\n')
fig=plt.figure(figsize=(10,7));ax=fig.add_subplot(111,projection='3d')
for i,m in enumerate(meshes):
 ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=['#90aabb','#90aabb','#cc7766','#d4aa44','#d4aa44','#66aa99','#55aa77','#55aa77','#8888cc','#8888cc'][i],linewidth=0))
 x,y=layout[i]['center_xy'];ax.text(x,y,m.bounds[1,2]+2,layout[i]['name'])
ax.set(xlim=(0,80),ylim=(0,83),zlim=(0,55),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='E-302 revision 2 • PCB recess + screws + 18/50 mm pins');ax.set_box_aspect((80,83,55));ax.view_init(45,-65);fig.tight_layout();fig.savefig(H/'plate.png',dpi=160)
