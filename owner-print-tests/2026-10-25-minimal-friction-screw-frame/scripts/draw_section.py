#!/usr/bin/env python3
"""Dimensioned X/Z mesh sections, all assembly heights in mm from frame bottom."""
from pathlib import Path
import numpy as np,trimesh,manifold3d as md
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.path import Path as MP
from matplotlib.patches import PathPatch,Rectangle
P=Path(__file__).resolve().parents[1];V3=P.parent/'2026-10-19-microstepper-frame-v3'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','font.size':9})
def load(path):
 m=trimesh.load(path,force='mesh');return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def frame(pack,prefix=''):
 f=load(pack/'components'/(prefix+'front.stl')).translate([0,0,-6.5]).rotate([90,0,0]);b=load(pack/'components'/(prefix+'back.stl')).translate([0,0,-6.5]).rotate([90,0,0]).rotate([0,0,180]);return f+b
def section(ax,solid,color,alpha=1):
 pol=solid.rotate([90,0,0]).slice(.001).to_polygons();verts=[];codes=[]
 for q in pol:
  q=np.array(q);q[:,1]*=-1;verts.extend(list(q)+[q[0]]);codes.extend([MP.MOVETO]+[MP.LINETO]*(len(q)-1)+[MP.CLOSEPOLY])
 if verts:ax.add_patch(PathPatch(MP(np.array(verts),codes),facecolor=color,edgecolor=color,lw=.35,alpha=alpha))
def draw(ax,new,high=False):
 pack=P if new else V3;fr=frame(pack,'A-' if new else '');r=load(pack/'components'/('A-screw.stl' if new else 'rotor-long.stl')).translate([0,0,12.9]);pin=load(P/'components/C-pin-50-upright.stl').translate([0,0,19.5 if new else 27.9]);washer=(md.Manifold.cylinder(.5,3.5,3.5,96)-md.Manifold.cylinder(.5,1.6,1.6,96)).translate([0,0,12.4])
 section(ax,fr,'#8995a2');section(ax,pin,'#2996ab',.65);section(ax,r,'#df8c35');section(ax,washer,'#273544')
 if high:section(ax,pin.translate([0,0,15]),'#2996ab',.17)
 ax.add_patch(Rectangle((-4,2),8,9.2,facecolor='#bad8c7',edgecolor='#3c6e53',lw=.8))
 ax.add_patch(Rectangle((-1.5,11.2),3,.25,facecolor='#bad8c7',edgecolor='#3c6e53',lw=.4))
 ax.add_patch(Rectangle((-.4,11.2),.8,3.35,facecolor='#3c6e53'))
 ax.add_patch(Rectangle((-1.1,13.2),2.2,1.25,facecolor='#3c6e53',alpha=.8))
 ax.axvline(0,color='#9aa2ad',lw=.5,ls='--');ax.set_aspect('equal');ax.set_xlabel('X (mm)');ax.grid(alpha=.12)
def dim(ax,x,a,b,text):
 ax.annotate('',(x,a),(x,b),arrowprops=dict(arrowstyle='<->',lw=.8,color='#24354b'));ax.text(x-.7,(a+b)/2,text,ha='right',va='center',rotation=90,fontsize=8)
fig=plt.figure(figsize=(14,10),facecolor='white');gs=fig.add_gridspec(1,3,width_ratios=[1,1,1.6],wspace=.35)
a=fig.add_subplot(gs[0]);b=fig.add_subplot(gs[1]);right=gs[2].subgridspec(2,1,height_ratios=[1,1.35]);c=fig.add_subplot(right[0]);d=fig.add_subplot(right[1]);d.axis('off')
for ax,new in [(a,False),(b,True)]:
 draw(ax,new,True);ax.set(xlim=(-19,17),ylim=(0,97),ylabel='Z from frame bottom (mm)',title='NEW A — 15 mm CAD stroke' if new else 'v3 — owner-tested baseline')
 dim(ax,-15,12.9,16.5 if new else 24.9,'3.6 body' if new else '12 body')
 for z,label in ([(36,'2 mm guide'),(56,'2 mm guide'),(16.5,'thread starts 16.5'),(19.5,'pin low 19.5')] if new else [(24.9,'thread starts 24.9'),(32.7,'guide starts 32.7'),(72.7,'guide ends 72.7')]):
  ax.annotate(label,xy=(3,z),xytext=(5,z+2 if z<25 else z),fontsize=7,arrowprops=dict(arrowstyle='-',lw=.5))
 if new:dim(ax,15,19.5,34.5,'15 travel')
draw(c,True);c.set(xlim=(-5.5,5.5),ylim=(10.7,20.3),title='A thrust / coupling detail — nominal, seated',ylabel='Z (mm)')
for z,label in [(11.2,'motor top 11.2'),(12.4,'washer bottom 12.4'),(12.9,'rotor bottom 12.9'),(14.1,'flange top 14.1'),(14.4,'upper stop 14.4'),(15.3,'socket roof 15.3'),(16.5,'thread start 16.5'),(19.5,'pin bottom 19.5')]:
 c.plot([-5.3,-3.6],[z,z],lw=.4,color='#52657c');c.text(-5.3,z+.06,label,fontsize=6.5)
rows=[['Axial feature (mm)','v3','New A'],['Motor top / L gear','11.2 / 13.2–14.45','same'],['L shaft tip','14.55','14.55'],['C straight zone','13.15–18.9','13.15–15.3'],['Lower thrust / flange top','12.9 / 24.9','12.9 / 14.1'],['Upper stop underside','25.2','14.4'],['Rotor axial float','0.30','0.30'],['Thread start / end','24.9 / 72.9','16.5 / 43.5'],['Pin lower thread at low','27.9–33.9','19.5–25.5'],['At +15 (float excluded)','42.9–48.9','34.5–40.5'],['Thread overlap at 0 / 15','6 / 6 (long)','6 / 6'],['Guide stations','32.7–72.7','36–38; 56–58'],['Frame height','72.7','60.0'],['Radial land length / gap','3.7 / 0.20','0.6 / 0.20*']]
t=d.table(cellText=rows,cellLoc='left',colWidths=[.49,.29,.25],bbox=[-.05,.18,1.1,.82]);t.auto_set_font_size(False);t.set_fontsize(7)
for (i,j),cell in t.get_celld().items():
 cell.set_linewidth(.4);cell.set_edgecolor('#cbd2dc')
 if i==0:cell.set_facecolor('#e5edf2');cell.set_text_props(weight='bold')
d.text(-.05,.12,'* Loose emergency land at Z15.4–16.0; no nominal radial contact.\nMay react misalignment. It does not guarantee zero motor shaft load.',fontsize=8,va='top')
fig.suptitle('Minimal screw frame • section through actual meshes • 25 October 2026',fontsize=17,y=.99)
fig.text(.08,.025,'Gray: frame   Orange: rotor/screw   Blue: pin (faint = +15 mm)   Green: approximate L motor   Dark: reused washer\nCAD clearance and toolpaths are digital evidence. Physical fit, friction, shaft load and durability remain untested.',fontsize=10)
fig.savefig(P/'images/assembly-section.svg',bbox_inches='tight');plt.close(fig)
# Compact 3x3 plan with actual boundary and two gap states.
fig,axs=plt.subplots(1,2,figsize=(10,5))
for ax,ang,title in [(axs[0],0,'Nominal grid — 0.68 mm gaps'),(axs[1],22.76915768596,'Fixed-neighbor first contact — 22.77°')]:
 for i in [-1,0,1]:
  for j in [-1,0,1]:
   q=np.array([[-2.2,-2.2],[2.2,-2.2],[2.2,2.2],[-2.2,2.2]])
   if i==j==0:
    a=np.radians(ang);q=q@np.array([[np.cos(a),np.sin(a)],[-np.sin(a),np.cos(a)]])
   q+=np.array([i*5.08,j*5.08]);ax.fill(q[:,0],q[:,1],color='#e99b48' if i==j==0 else '#8cc4cb',ec='#234456',alpha=.8)
 ax.add_patch(Rectangle((-7.5,-7.5),15,15,fill=False,ls='--',ec='#52657c'));ax.set(xlim=(-9,9),ylim=(-9,9),title=title,xlabel='mm',ylabel='mm');ax.set_aspect('equal');ax.grid(alpha=.15)
axs[0].annotate('',(0,8),(5.08,8),arrowprops=dict(arrowstyle='<->'));axs[0].text(2.54,8.2,'5.08 mm',ha='center')
fig.text(.08,.01,'Boundary opening 15.0 mm, removable. Free neighbors can translate/rotate: 22.77° is a fixed-center calculation, not a measured limit.',fontsize=9)
fig.tight_layout(rect=[0,.05,1,1]);fig.savefig(P/'images/neighbor-plan.svg');plt.close(fig)

# Keep generated SVG text free of trailing whitespace.
for svg in (P/'images').glob('*.svg'):
 svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
