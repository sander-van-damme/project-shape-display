#!/usr/bin/env python3
"""Draw actual exported meshes and the saved plate layout, without altering CAD."""
from pathlib import Path
import importlib.util,json,os
os.environ.setdefault('MPLCONFIGDIR',str(Path(__file__).resolve().parents[3]/'work/matplotlib'))
os.environ.setdefault('XDG_CACHE_HOME',str(Path(__file__).resolve().parents[3]/'work/cache'))
import numpy as np
import trimesh as tm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Rectangle
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];CAD=HERE/'cad';OUT=HERE/'drawings';OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('cad',CAD/'generate.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
for p in (CAD/'parts').glob('*.stl'):
 if not p.stem.endswith('-print'):g.MESHES[p.stem]=tm.load(p,force='mesh')
# Orthographic oblique projection: x/y are both visible and vertical remains vertical.
u=np.array([.86,-.51,0]);v=np.array([.22,.37,.90]);w=np.cross(u,v)
def draw(ax,parts,explode=False):
 faces=[];colors=[];depth=[]
 for name,m in parts.items():
  if name.startswith('frame'):color='#aebcc5'
  elif 'holder' in name:color='#ba78c6'
  elif name.startswith(('row','column')):color='#1c98bd'
  elif name.startswith(('lower','upper')):color='#dc7445'
  elif name.startswith('pin'):color='#d6b43d'
  else:color='#688c66'
  mm=m.copy()
  if explode:
   if name=='frame-back':mm.apply_translation([0,-15,0])
   elif name=='frame-front':mm.apply_translation([0,15,0])
   elif 'holder' in name:mm.apply_translation([0,-9 if name.startswith('row') else 9,0])
  tri=mm.triangles;norm=mm.face_normals
  keep=norm@w>-.02
  tri=tri[keep];norm=norm[keep]
  proj=np.stack([tri@u,tri@v],axis=2)
  import matplotlib.colors as mc
  rgb=np.array(mc.to_rgb(color));shade=.65+.35*np.abs(norm@np.array([.3,-.4,.86]))
  faces.extend(proj);colors.extend(np.clip(shade[:,None]*rgb,0,1));depth.extend(tri.mean(axis=1)@w)
 order=np.argsort(depth);pc=PolyCollection([faces[i] for i in order],facecolors=[colors[i] for i in order],edgecolors='none',rasterized=True)
 ax.add_collection(pc);ax.autoscale();ax.set_aspect('equal');ax.axis('off')
fig,axs=plt.subplots(1,2,figsize=(12,7));a=g.assembly(r=1+.52/g.S,c=(1-.04/g.S,)*2,lower_offsets=(-.24,)*2,upper_offsets=(.24,)*2);draw(axs[0],a);draw(axs[1],a,True)
axs[0].set_title('1×2-test — beide conussen op eerste belast contact',fontsize=12);axs[1].set_title('Open frame — beide assen vanaf hetzelfde deelvlak',fontsize=12)
fig.text(.5,.035,'Grijs: frame  |  Blauw: selectoren  |  Oranje: koppelingen  |  Geel: pinnen  |  Paars: grote eindstandhouders',ha='center',fontsize=10)
fig.tight_layout(rect=[0,.06,1,1]);fig.savefig(OUT/'assembly.png',dpi=180);plt.close(fig)
folder=ROOT/'owner-print-tests/2026-10-17-cone-friction-selector';layout=json.loads((folder/'layout.json').read_text())
fig,ax=plt.subplots(figsize=(11,7));cmap=plt.get_cmap('tab20')
for i,p in enumerate(layout,1):
 lo,hi=np.array(p['bounds_mm']);ax.add_patch(Rectangle(lo[:2],*(hi-lo)[:2],facecolor=cmap(i%20),edgecolor='#334455',alpha=.65));ax.text(*(lo[:2]+hi[:2])/2,str(i),ha='center',va='center',fontsize=10,weight='bold')
ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('X (mm, CAD-plaat vóór centreren)');ax.set_ylabel('Y (mm)');ax.set_title('Vaste plaatindeling — niet automatisch oriënteren of plaatsen')
labels='\n'.join(f'{i:02d}  {p["name"]}' for i,p in enumerate(layout,1));fig.text(.78,.85,labels,va='top',fontsize=9,family='monospace');fig.tight_layout(rect=[0,0,.77,1]);fig.savefig(OUT/'plate-map.png',dpi=170);plt.close(fig)
print(OUT)

# Coupling detail deliberately omits the frame, keeping the actual selectors visible.
fig,ax=plt.subplots(figsize=(8,5));a=g.assembly(r=1+.52/g.S,c=(1-.04/g.S,)*2,lower_offsets=(-.24,)*2,upper_offsets=(.24,)*2);cropped={}
for name,m in a.items():
 if name.startswith(('row','column','lower','upper')) and 'holder' not in name:cropped[name]=m
draw(ax,cropped);ax.set_title('Werkelijke CAD: beide koppelingen gesloten, rij onder centrale druk')
fig.text(.5,.04,'Kolomslag 3 mm; rij-handbeweging circa 3,52 mm tot eerste belast contact. Eerst sluiten, dan draaien.',ha='center',fontsize=10)
fig.tight_layout(rect=[0,.08,1,1]);fig.savefig(OUT/'coupling-detail.png',dpi=180);plt.close(fig)
