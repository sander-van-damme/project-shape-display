"""Render corrected meshes and an axial diagram; dimension values from design metadata."""
import json
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype']='none'
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from paths import COMPONENTS, METADATA, IMAGES, TEST_DIR
basis=json.loads((METADATA/'motor-interface.json').read_text())
front=trimesh.load(COMPONENTS/'front.stl',force='mesh')
front.apply_translation([0,0,-6.5])
front.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))
rotor=trimesh.load(COMPONENTS/'rotor-long.stl',force='mesh');rotor.apply_transform(trimesh.transformations.rotation_matrix(-np.pi,[0,0,1]));rotor.apply_translation([0,0,basis['rotor_z_mm']])
pin=trimesh.load(COMPONENTS/'pin-50.stl',force='mesh');pin.apply_translation([0,0,29.4]);pin=pin.slice_plane([0,0,0],[0,1,0])
body=trimesh.creation.cylinder(radius=4,height=9.2);body.apply_translation([0,0,6.6])
fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(121,projection='3d')
triangles=[];colors=[]
for mesh,color in [(front,'#7296ad'),(rotor,'#db9f43'),(pin,'#63a68f'),(body,'#999999')]:
 triangles.extend(mesh.triangles);colors.extend([color]*len(mesh.faces))
ax.add_collection3d(Poly3DCollection(triangles,facecolor=colors,linewidth=0))
ax.set(xlim=(-17,17),ylim=(-10,10),zlim=(0,85),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
ax.set_box_aspect((34,20,85));ax.view_init(24,-65)
ax.set_title('50 mm pin / 60 mm screw in guide\nPin cut open; one frame half omitted; motor L')
ax=fig.add_subplot(122,projection='3d')
plate=trimesh.load(COMPONENTS/'microstepper-frame-v3.stl',force='mesh')
ax.add_collection3d(Poly3DCollection(plate.triangles,facecolor='#7296ad',linewidth=0))
ax.set(xlim=(0,98),ylim=(0,92),zlim=(0,65),xlabel='X mm',ylabel='Y mm',zlabel='Z mm')
ax.set_box_aspect((98,92,65));ax.view_init(65,-90)
ax.set_title('Upright 50 mm pin and supported long screw\nShort pin and screw also included')
fig.tight_layout();fig.savefig(IMAGES/'cad.png',dpi=150);plt.close(fig)
fig,ax=plt.subplots(figsize=(9,8))
def box(x,z,w,h,c):ax.add_patch(Rectangle((x,z),w,h,facecolor=c,edgecolor='#333',lw=.7))
box(-4,2,8,9.2,'#aaaaaa');box(-1.5,11.2,3,.25,'#aaaaaa')
box(-.4,11.45,.8,3.1,'#777777');box(-1.1,13.2,2.2,1.25,'#d6a548')
for x in [-6,2]:box(x,11.4,4,1,'#7296ad')
for x in [-3.5,1.6]:box(x,12.4,1.9,.5,'#555555')
for x in [-3.5,1.25]:box(x,12.9,2.25,6,'#db9f43')
box(-3.5,18.9,7,1,'#db9f43')
box(-6,4,2,4,'#63a68f')
ax.annotate('Wires upwards in outer channel',xy=(-5,17),xytext=(-10,19),arrowprops={'arrowstyle':'->'})
ax.plot([-5,-5],[8,18],color='#26724a',lw=3)
for z,label in [(2,'2.00 motor support'),(11.2,'11.20 metal housing top'),(12.4,'12.40 washer underside'),(12.9,'12.90 rotor mouth'),(14.55,'14.55 shaft tip (approx.)'),(18.9,'18.90 socket roof')]:
 label_z={11.2:10.2,12.4:11.8,12.9:13.1,14.55:15.1}.get(z,z)
 ax.plot([3.6,6],[z,label_z],color='#666',lw=.6);ax.text(6.1,label_z,label,fontsize=9,va='center')
ax.text(-11,1,'Housing 9.2 mm; L teeth Z13.20–14.45\nMinimum straight overlap at lift 0.30: 1.00 mm\nRadial C-ribs not depicted; see actual CAD',fontsize=9)
ax.set(xlim=(-12,19),ylim=(0,21),xlabel='X (mm)',ylabel='Z from frame bottom (mm)')
ax.set_aspect('equal');ax.set_title('L axial section / schematic PCB and cable route')
ax.grid(alpha=.15);fig.tight_layout();fig.savefig(IMAGES/'assembly.svg');plt.close(fig)

p=IMAGES/"assembly.svg"
p.write_text("\n".join(line.rstrip() for line in p.read_text().splitlines())+"\n")
