#!/usr/bin/env python3
"""Actual STL plane sections; run from repository root after CAD generation."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path('tools/curated-experiment-checks/E-300/cad').resolve()))
import generate as g
import trimesh as tm
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
base=Path('tools/curated-experiment-checks/E-300')
for n in ['male-rotor','female-rotor','row-selector-core']:
 g.MESHES[n]=tm.load(base/'cad/parts'/f'{n}.stl',force='mesh')
fig,axes=plt.subplots(1,2,figsize=(11.5,6.5),layout='constrained')
ax=axes[0]
for name,m,color in [('Male',g.shift(g.MESHES['male-rotor'],[0,0,11.28]),'#196b88'),('Female',g.shift(g.rotate(g.MESHES['female-rotor'],[1,0,0],180),[0,0,26.64]),'#b55a34')]:
 sec=tm.intersections.mesh_plane(m,plane_origin=[0,0,0],plane_normal=[1,0,0])
 for line in sec:ax.plot(line[:,1],line[:,2],color=color,lw=2,label=name if len(ax.lines)==0 else None)
ax.set(xlim=(-2.7,2.7),ylim=(16.95,19.2),xlabel='Y (mm)',ylabel='Z in gemonteerde proef (mm)',title='Werkelijke meshdoorsnede: gesloten conus')
ax.set_aspect('equal');ax.grid(alpha=.2)
ax.annotate('45° contact\nz 17,48–17,98',xy=(1.7,17.68),xytext=(.5,18.7),arrowprops={'arrowstyle':'->'},fontsize=10)
ax.annotate('0,10 mm tipvrijloop',xy=(0,18.03),xytext=(-2.6,18.9),arrowprops={'arrowstyle':'->'},fontsize=9)
ax.annotate('',xy=(-2.35,17.05),xytext=(2.35,17.05),arrowprops={'arrowstyle':'|-|','lw':1})
ax.text(0,17.10,'Ø4,70 buiten / 0,38 rastervrijloop',ha='center',fontsize=9)
ax.text(-2.6,16.88,'Blauw: mannelijke helft; bruin: cup',fontsize=8)
ax=axes[1]
sec=tm.intersections.mesh_plane(g.MESHES['row-selector-core'],plane_origin=[2.54,0,0],plane_normal=[1,0,0])
for line in sec:ax.plot(line[:,1],line[:,2],color='#285846',lw=2)
ax.set(xlim=(-3.4,1.1),ylim=(-3,5.9),xlabel='Y (mm)',ylabel='Z t.o.v. selectorbasis (mm)',title='Werkelijke rij-kern bij één uitsparing')
ax.set_aspect('equal');ax.grid(alpha=.2)
for yy,z0,z1,label in [(.2,-2.64,-.24,'2,40'),(.2,-.24,.96,'1,20 groef'),(.2,.96,5.36,'4,40')]:
 ax.annotate('',xy=(yy,z0),xytext=(yy,z1),arrowprops={'arrowstyle':'|-|','lw':1})
 ax.text(yy+.13,(z0+z1)/2,label,va='center',fontsize=9)
ax.annotate('Rug 0,46 mm\nvolledige kernhoogte 8,00 mm',xy=(-2.54,.36),xytext=(-3.3,3.5),arrowprops={'arrowstyle':'->'},fontsize=8)
ax.annotate('Laatste 0,90 mm:\nYZ-printhelling in cap',xy=(-2.6,4.9),xytext=(-1.4,4.7),arrowprops={'arrowstyle':'->'},fontsize=8)
ax.text(-3.3,-2.93,'Alleen herhaalbare kern; proefpaddle en einden weggelaten.',fontsize=8)
fig.suptitle('E-300 — doorsneden uit definitieve STL-meshes (geen fysieke meetgegevens)',fontsize=13)
fig.savefig(base/'drawings/section.png',dpi=190)
fig.savefig(base/'drawings/section.svg')
