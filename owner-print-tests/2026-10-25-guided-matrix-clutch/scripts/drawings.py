#!/usr/bin/env python3
"""Dimensioned sections and exploded projections from the delivered meshes, not illustrations of imagined parts."""
from pathlib import Path
import importlib.util,math,json,argparse
import numpy as np
import trimesh as tm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection,PolyCollection
args=argparse.ArgumentParser();args.add_argument('--preview-dir',type=Path);args=args.parse_args()
if args.preview_dir:args.preview_dir.mkdir(parents=True,exist_ok=True)
H=Path(__file__).resolve().parent;P=H.parent
s=importlib.util.spec_from_file_location('g',P/'cad/generate.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
for name in json.load(open(P/'metadata/meshes.json')):g.PART[name]=tm.load(g.ENG/(name+'.stl'))
O=P/'images';O.mkdir(exist_ok=True)
C={'frame':'#9aa5af','keeper':'#b0bbc2','row':'#246eaa','column':'#b57912','follower':'#8e4e9f','rotor':'#22896b','output':'#b84d36','pin':'#b84d36','shared':'#344b67','hand':'#344b67'}
def color(k):return next((v for n,v in C.items() if k.startswith(n)),'gray')
def sec(ax,m,color,plane='xz',offset=0,lw=.65):
 normal=[0,1,0] if plane=='xz' else [0,0,1];origin=[0,offset,0] if plane=='xz' else [0,0,offset]
 seg=tm.intersections.mesh_plane(m,normal,origin)
 if len(seg):ax.add_collection(LineCollection(seg[:,:,[0,2]] if plane=='xz' else seg[:,:,:2],colors=color,linewidths=lw))
def dim(ax,a,b,text,dx=0):
 ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='<->',color='#333',lw=.7));ax.text((a[0]+b[0])/2+dx,(a[1]+b[1])/2,text,fontsize=7,ha='center',va='center',bbox=dict(facecolor='white',edgecolor='none',pad=.5))
a=g.assembly((1,1),(1,1))
fig,axs=plt.subplots(1,3,figsize=(13,9),gridspec_kw={'width_ratios':[1.2,1,1]})
for name,m in a.items():
 if name not in ['hand-drive','shared-rack']:sec(axs[0],m,color(name))
axs[0].set(xlim=(-8,13),ylim=(-2,81),xlabel='X (mm)',ylabel='Z (mm)',title='Loaded 2×2: section through first row\nActual nominal meshes; elastic follower is a linear model')
axs[0].set_aspect('equal');dim(axs[0],(0,80),(g.P,80),'5.08 pitch')
for z,t in [(4,'Inserted reinforcement channels'),(13,'Captured cam foot / row cap'),(17,'Integral compliant follower'),(23,'Column roof gate'),(30,'Central thrust + withdrawal lip'),(35.5,'Shared rack / permanent input gear'),(41.8,'30° cone contact'),(49,'Two output journals'),(53.5,'Stationary axial keeper'),(66,'Actual retained screw / pin thread')]:
 axs[0].annotate(t,xy=(0,z),xytext=(12,z),fontsize=6.5,arrowprops=dict(arrowstyle='-',lw=.5),ha='left')
for name in ['rotor-0','output-0','frame','keeper-upper-0']:
 sec(axs[1],a[name],color(name))
axs[1].set(xlim=(-3.2,4.8),ylim=(37.5,55),xlabel='X (mm)',ylabel='Z (mm)',title='Supported clutch intersection')
axs[1].set_aspect('equal');dim(axs[1],(-2.3,40.5),(2.3,40.5),'Ø4.60 cup')
dim(axs[1],(3,46.6),(3,51.8),'5.20 mm\njournal span',dx=.5)
axs[1].annotate('Torque → cup → neck → screw',xy=(.9,47),xytext=(-2.9,54.1),fontsize=7,arrowprops=dict(arrowstyle='->'))
axs[1].annotate('Axial reaction to fixed deck',xy=(1.4,53.4),xytext=(-2.9,52.4),fontsize=7,arrowprops=dict(arrowstyle='->'))
for name,m in a.items():sec(axs[2],m,color(name),plane='xy',offset=42.2)
axs[2].set(xlim=(-3.4,8.5),ylim=(-3.4,8.5),xlabel='X (mm)',ylabel='Y (mm)',title='Four neighboring cones, 5.08-mm pitch')
axs[2].set_aspect('equal');dim(axs[2],(2.3,-2.8),(2.78,-2.8),'.48 cup gap')
fig.subplots_adjust(wspace=.65,left=.05,right=.97,top=.94,bottom=.06);fig.savefig(O/'sections.svg',bbox_inches='tight')
if args.preview_dir:fig.savefig(args.preview_dir/'sections.png',dpi=140,bbox_inches='tight')
plt.close(fig)
# Projection with hidden ordering, orthographic engineering exploded view.
fig,axs=plt.subplots(1,2,figsize=(13,9));a=g.assembly((0,0),(0,0));view=np.array([[.82,-.57,0],[.26,.37,.89],[.51,.73,-.45]])
def proj(ax,parts):
 tri=[];colors=[];depth=[]
 for name,m in parts.items():
  # Coarse display tessellation; underlying exported meshes remain unchanged.
  vertices=m.vertices@view.T;ff=m.faces
  for f in ff:
   tri.append(vertices[f,:2]);depth.append(float(vertices[f,2].mean()));colors.append(color(name))
 ix=np.argsort(depth)
 ax.add_collection(PolyCollection([tri[i] for i in ix],facecolors=[colors[i] for i in ix],edgecolors='none',alpha=1,rasterized=True));ax.autoscale();ax.set_aspect('equal');ax.axis('off')
core={k:v for k,v in a.items() if k!='frame' and not k.startswith('keeper')}
proj(axs[0],core);axs[0].set_title('2×2 mechanism, stationary frame hidden for visibility')
expl={}
for k,m in a.items():
 dx=0;dy=0;dz=0
 if k=='frame':dx=30
 elif k.startswith('keeper'):dy=-18 if k.endswith('-0') else 18
 elif k.startswith('pin'):dz=20
 elif k.startswith('output'):dz=12
 elif k.startswith('rotor'):dz=5
 elif k.startswith('column'):dx=-12
 elif k.startswith('row-cap'):dz=4
 expl[k]=g.move(m,dx,dy,dz)
proj(axs[1],expl);axs[1].set_title('Exploded layout: shared covers, open cam caps, resident shafts')
fig.text(.03,.03,'Blue: row bases/caps  •  gold: columns  •  purple: guided elastic followers  •  green: input rotors\nRed: supported screws and terrain pins  •  grey: stationary frame/covers  •  navy: one common rack drive',fontsize=9)
fig.tight_layout(rect=(0,.08,1,1));fig.savefig(O/'assembly-exploded.svg')
if args.preview_dir:fig.savefig(args.preview_dir/'exploded.png',dpi=130)
plt.close(fig)
# Four truth states, actual local meshes. Single row/column moves cannot establish contact.
fig,axs=plt.subplots(1,4,figsize=(12,7))
for ax,(r,c) in zip(axs,[(0,0),(1,0),(0,1),(1,1)]):
 b=g.assembly((r,0),(c,0))
 for k in ['row-0','row-cap-0','column-0','follower-0','rotor-0','output-0']:sec(ax,b[k],color(k))
 ax.set(xlim=(-3.1,3.1),ylim=(10,44.5),title=f'R={r}, C={c}',xlabel='X (mm)');ax.set_aspect('equal')
 ax.text(-3,10.3,'CONTACT' if r and c else 'OPEN',fontsize=9,weight='bold')
fig.suptitle('Mechanical AND — row lift is absorbed locally when the column roof remains low');fig.tight_layout();fig.savefig(O/'selection-states.svg');plt.close(fig)
# Named plate map, source layout in mm.
layout=json.load(open(P/'metadata/layout.json'));fig,ax=plt.subplots(figsize=(12,8))
for j,e in enumerate(layout,1):
 lo,hi=np.array(e['bounds_mm']);rect=plt.Rectangle(lo[:2],*(hi-lo)[:2],facecolor='#e5edf2',edgecolor='#456');ax.add_patch(rect);ax.text(lo[0],hi[1]+.8,f'{j}: {e["name"]}',fontsize=5.5)
ax.set(xlim=(0,235),ylim=(0,max(np.array(e['bounds_mm'])[1,1] for e in layout)+8),xlabel='Plate-layout X before centering (mm)',ylabel='Y (mm)',title='Fixed plate layout — keep the saved orientation and placement');ax.set_aspect('equal');fig.tight_layout();fig.savefig(O/'plate-map.svg');plt.close(fig)
print('Drawings exported')
# Actual transverse structural section and sampled cone contact envelope.
fig,axs=plt.subplots(1,2,figsize=(11,7));m=g.PART['beam-100'];seg=tm.intersections.mesh_plane(m,[1,0,0],[0,0,0]);axs[0].add_collection(LineCollection(seg[:,:,[1,2]],colors='#246eaa',linewidths=1))
for z in [2.2,8.1]:axs[0].add_patch(plt.Circle((0,z),1,edgecolor='#333',facecolor='#ddd',linestyle='--'))
axs[0].set(xlim=(-4,7),ylim=(-1,16.5),xlabel='Y (mm)',ylabel='Z (mm)',title='Actual beam section at a cam dwell\nDashed: optional purchased Ø2-mm rods');axs[0].set_aspect('equal');dim(axs[0],(-2.3,-.5),(2.3,-.5),'4.60');dim(axs[0],(3.2,0),(3.2,10.4),'10.40 core',dx=1.2);dim(axs[0],(5.5,0),(5.5,14.7),'14.70 max',dx=1.0)
axs[0].annotate('Ø2.20 channels',xy=(0,8.1),xytext=(-3.8,15.5),fontsize=8,arrowprops=dict(arrowstyle='->'))
import csv
phasefile=P/'metadata/cone-phase-clearance.csv'
if phasefile.exists():
 data=list(csv.DictReader(phasefile.open()))
 for e,t in [(0,0),(.1,0),(.2,0),(.27,0),(0,2)]:
  dd=[q for q in data if float(q['radial_offset_mm'])==e and float(q['relative_tilt_deg'])==t];axs[1].plot([float(q['relative_angle_deg']) for q in dd],[float(q['first_contact_lift_mm']) for q in dd],label=f'Offset {e:.2f} mm; tilt {t}°')
axs[1].axhline(.6,color='gray',ls='--',label='Ideal coaxial cone .60 mm');axs[1].set(xlim=(0,360),ylim=(0,.65),xlabel='Initial relative phase (degrees)',ylabel='First-contact input lift (mm)',title='Actual faceted cone: all72 sampled phases\nContact geometry only; no friction qualification');axs[1].legend(fontsize=7)
fig.tight_layout();fig.savefig(O/'beam-and-contact.svg');plt.close(fig)
