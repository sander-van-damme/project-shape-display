#!/usr/bin/env python3
"""Actual mesh views and dimensioned geometric explanation, not print photographs."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh as tm
H=Path(__file__).resolve().parent;D=H.parent/'drawings';D.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'figure.facecolor':'white','axes.titlesize':12})
def draw(ax,m,color):
 from matplotlib.colors import to_rgb
 light=np.array([-.3,-.5,1.]);light/=np.linalg.norm(light)
 shades=.45+.55*np.clip(m.face_normals@light,0,1)
 colors=np.array(to_rgb(color))[None,:]*shades[:,None]
 pc=Poly3DCollection(m.triangles,facecolors=colors,edgecolors='none',linewidths=0,alpha=1,rasterized=True)
 ax.add_collection3d(pc)
 b=m.bounds;cen=b.mean(axis=0);span=max(m.extents)*.54
 ax.set(xlim=(cen[0]-span,cen[0]+span),ylim=(cen[1]-span,cen[1]+span),zlim=(cen[2]-span,cen[2]+span));ax.set_box_aspect((1,1,1));ax.view_init(28,-60);ax.set_axis_off()
def save(fig,name):
 fig.savefig(D/(name+'.png'),dpi=160,bbox_inches='tight');fig.savefig(D/(name+'.svg'),bbox_inches='tight');plt.close(fig)
fig=plt.figure(figsize=(12,6))
for i,(name,title) in enumerate([('point48','A · taper 0,48 mm · symmetrisch'),('point60','B · taper 0,60 mm · symmetrisch'),('point60skew','C · taper 0,60 mm · 12° scheef')]):
 m=tm.load(H/'parts'/(name+'.stl'),force='mesh');m=m.submesh([np.where(m.triangles_center[:,2]>6.199)[0]],append=True)
 ax=fig.add_subplot(1,3,i+1,projection='3d');draw(ax,m,'#50a5ad');ax.set_title(title)
fig.suptitle('E-298 · werkelijke CAD-mesh van de twee punten per helft\nWortel r=0,60–1,80 mm; kruin 0,30 mm radiaal; wortelsector 76°',y=.95)
fig.text(.5,.12,'De twee open sectoren vormen de complementaire holtes. Tegenhelft is dezelfde geometrie, omgekeerd.\nKruin heeft een eindig vlak: perfecte punt-op-puntstand kan nog blokkeren.',ha='center')
save(fig,'point-variants')
fig,axs=plt.subplots(1,2,figsize=(12,5))
for ax,t,title in zip(axs,[.48,.60],['A / matrix · 0,48 mm taper','B / C · 0,60 mm taper']):
 # Angular unwrapped profile at nominal mean radius; schematic excludes radial taper.
 x=np.array([-38,-38, -7.16197,7.16197,38,38]);z=np.array([0,2.4-t,2.4,2.4,2.4-t,0])
 ax.fill(x,z,color='#51a6ad',alpha=.8);ax.fill(x+90,3.36-z,color='#e4a449',alpha=.8)
 ax.set(xlim=(-45,135),ylim=(-.3,3.7),xlabel='Hoek rond as (graden)',ylabel='z vanaf onderste tandwortel (mm)',title=title)
 ax.axhline(0,color='gray',lw=.7);ax.axhline(3.36,color='gray',lw=.7)
 ax.text(45,1.68,f'Rechte overlap\n{1.44-2*t:.2f} mm',ha='center',bbox=dict(facecolor='white',alpha=.9,edgecolor='none'))
 ax.grid(alpha=.2)
fig.suptitle('Nominale volledige aangrijping · 90° relatieve fase\nOmgeklapte hoekdoorsnede als uitleg; radiale puntversmalling niet afgebeeld')
fig.tight_layout();save(fig,'engagement-section')
fig=plt.figure(figsize=(10,9));ax=fig.add_subplot(111,projection='3d')
# Actual assembled parts, omitting bulky front frame only for visibility; all retained in STL.
import importlib.util
s=importlib.util.spec_from_file_location('g',H/'generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for name in ['frame-left','frame-center','frame-right','row-selector','input-shaft','screw','pin','stop-spacer']:g.old.MESHES[name]=tm.load(H/'parts'/(name+'.stl'),force='mesh')
g.old.MESHES['rotor']=tm.load(H/'parts/point48.stl',force='mesh')
pp=g.old.assembly((1,1),(1,1));allm=[]
for name,m in pp.items():
 if name.startswith('frame'):continue
 color='#51a6ad' if name.startswith('lower') else '#e4a449' if name.startswith('upper') else '#67768a' if name.startswith(('row','column')) else '#b5c0cc'
 ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=color,edgecolors='none',linewidths=0,rasterized=True));allm.append(m)
ax.set(xlim=(-20,20),ylim=(-20,20),zlim=(0,55));ax.set_box_aspect((40,40,55));ax.view_init(22,-53);ax.set_axis_off();ax.set_title('E-298 · 2×2, alle vier gekoppeld\n5,08-mm pitch · frame weggelaten om koppelingen zichtbaar te maken')
save(fig,'matrix-assembly')
for short in ['fit','matrix']:
 directory=g.ROOT/'owner-print-tests'/('2026-10-16-self-aligning-point-'+short);layout=json.loads((directory/'layout.json').read_text())
 fig,ax=plt.subplots(figsize=(12,6))
 for i,item in enumerate(layout):
  b=np.array(item['bounds_mm']);ax.add_patch(plt.Rectangle(b[0,:2],*(b[1,:2]-b[0,:2]),facecolor='#cce4e7',edgecolor='#23727a'))
  ax.text(*b[:,:2].mean(axis=0),str(i+1),ha='center',va='center',fontsize=8)
 ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)');ax.set_title(f'Test {"A" if short=="fit" else "B"} · brondelen vóór slicer · nummers = layout.json-volgorde')
 save(fig,'plate-'+short)
manifest={str(p.relative_to(g.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((H/'parts').glob('*.stl'))}
(D/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
