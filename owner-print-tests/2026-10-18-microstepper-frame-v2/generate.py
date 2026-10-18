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
for name,part,r in [('half','half',1),('coupling-A','cup',.95),('coupling-N','cup',1),('coupling-C','cup',1.05)]:
 subprocess.run(['openscad','-o',str(H/(name+'.stl')),'-D',f'part="{part}"','-D',f'tip_r={r}',str(H/'rig.scad')],check=True,capture_output=True)
 m=trimesh.load(H/(name+'.stl'),force='mesh'); assert m.is_watertight and m.is_winding_consistent and len(m.split())==1,name
 m.export(H/(name+'.stl'));parts[name]=m
layout=[];meshes=[]
for name,x,y,label in [('half',20,44,'frame-1'),('half',60,44,'frame-2'),('coupling-A',10,57,'A'),('coupling-N',27,57,'N1'),('coupling-N',44,57,'N2'),('coupling-C',61,57,'C')]:
 m=parts[name].copy();m.apply_translation([x,y,0]);meshes.append(m)
 layout.append(dict(name=label,source=name,bounds_mm=m.bounds.tolist(),center_xy=[x,y]))
plate=trimesh.util.concatenate(meshes);plate.export(H/'microstepper-frame-v2.stl')
(H/'layout.json').write_text(json.dumps(layout,indent=2)+'\n')
(H/'geometry-validation.json').write_text(json.dumps(dict(body_count=len(meshes),bounds_mm=plate.bounds.tolist(),parts={n:dict(volume_mm3=m.volume,watertight=m.is_watertight,sha256=hashlib.sha256((H/(n+'.stl')).read_bytes()).hexdigest()) for n,m in parts.items()},scope='CAD only; physical fitting unknown'),indent=2)+'\n')
fig=plt.figure(figsize=(10,7));ax=fig.add_subplot(111,projection='3d')
for i,m in enumerate(meshes):
 ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=['#90aabb','#90aabb','#cc7766','#d4aa44','#d4aa44','#66aa99'][i],linewidth=0))
 x,y=layout[i]['center_xy'];ax.text(x,y,19,layout[i]['name'])
ax.set(xlim=(0,80),ylim=(0,67),zlim=(0,22),xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='E-302 • 2 frame halves + A / N1 / N2 / C');ax.set_box_aspect((80,67,22));ax.view_init(45,-65);fig.tight_layout();fig.savefig(H/'plate.png',dpi=160)
