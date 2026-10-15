#!/usr/bin/env python3
"""Render an actual-mesh section from the supplied nominal plate; requires matplotlib/trimesh/numpy."""
from pathlib import Path
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
import trimesh, numpy as np
P=Path(__file__).resolve().parent
parts=trimesh.load(P/'four-pin-demo-0175-plate.stl').split()
def extract(x,y):
 m=min(parts,key=lambda b:np.linalg.norm(b.bounds.mean(axis=0)[:2]-[x,y])).copy();m.apply_translation([-x,-y,0]);return m
base=extract(13,13);screw=extract(8,39);pin=extract(8,52);driver=extract(55,48)
cage=min(parts,key=lambda b:np.linalg.norm(b.bounds.mean(axis=0)[:2]-[40.85,13])).copy()
T=np.eye(4);T[:3,:3]=np.array([[0,0,1],[0,1,0],[-1,0,0]]);T[:3,3]=[-12,-13,56.1];cage.apply_transform(T)
fig,ax=plt.subplots(figsize=(10,9))
def section(mesh,color,label):
 s=trimesh.intersections.mesh_plane(mesh,plane_origin=[0,-2.54,0],plane_normal=[0,1,0])
 for i,l in enumerate(s):ax.plot(l[:,0],l[:,2],color=color,lw=1.2,label=label if i==0 else None)
def trans(m,vec,angle=0):
 m=m.copy();m.apply_transform(trimesh.transformations.rotation_matrix(np.deg2rad(angle),[0,0,1]));m.apply_translation(vec);return m
section(base,'#475569','Onderplaat')
section(cage,'#0284c7','Lagerdek + twee geleidingen')
for x,bot in [(-2.54,7.7),(2.54,13.7)]:
 section(trans(screw,[x,-2.54,1.2],240),'#b45309','Schroef' if x<0 else None)
 section(trans(pin,[x,-2.54,bot]),'#16a34a','Holle pin (6 mm binnendraad)' if x<0 else None)
section(trans(driver,[-2.54,-2.54,-10.5]),'#be123c','Handkop in linker socket')
for z,label in [(25.4,'Geleiding bovenzijde 25,4'),(14,'Ondergeleiding 14,0'),(6.7,'Lagerdek bovenzijde 6,7'),(1.2,'Kraagsteun 1,2')]:
 ax.annotate(label,xy=(12,z),xytext=(15,z+.8),fontsize=9,arrowprops={'arrowstyle':'-','color':'#64748b'})
ax.annotate('Laag: 25,7',xy=(-2.54,25.7),xytext=(-18,29),fontsize=9,arrowprops={'arrowstyle':'-'});ax.annotate('Hoog: 31,7',xy=(2.54,31.7),xytext=(8,34),fontsize=9,arrowprops={'arrowstyle':'-'})
ax.annotate('',xy=(-2.54,35),xytext=(2.54,35),arrowprops={'arrowstyle':'<->'});ax.text(0,36,'5,08 mm pitch',ha='center')
ax.set(xlim=(-22,36),ylim=(-13,40),xlabel='x (mm)',ylabel='z boven onderplaat (mm)',title='Doorsnede door twee van de vier pinnen — nominale CAD')
ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(loc='lower right',fontsize=8)
fig.tight_layout();fig.savefig(P/'assembly-section.png',dpi=170)
