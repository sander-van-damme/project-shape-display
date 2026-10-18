from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,Polygon
H=Path(__file__).resolve().parent
fig,(a,b)=plt.subplots(1,2,figsize=(12,10))
a.set_title('1 • Open frame: zijaanzicht X–Z (mm)')
for x in [-15,12]:a.add_patch(Rectangle((x,2),3,42,color='#9cb3c3'))
a.add_patch(Rectangle((-18,0),36,2,color='#9cb3c3'))
for z,h in [(20.2,3.5),(28.9,2.1)]:
 for x in [-15,2]:a.add_patch(Rectangle((x,z),13,h,color='#9cb3c3'))
a.add_patch(Rectangle((-4,2),8,8.2,color='#aaa'))
a.add_patch(Rectangle((-6.5,3),2.5,6,color='#568b67'))
a.plot([-6,-9,-10],[8,10,16],color='#ba6550',lw=3)
a.add_patch(Rectangle((-1.1,12.7),2.2,1.5,color='#d3b45c'))
a.add_patch(Rectangle((-.6,10.2),1.2,2.5,color='#999'))
a.add_patch(Rectangle((-2.5,11.2),5,8.5,fill=False,edgecolor='#bb872a',lw=2))
a.add_patch(Rectangle((-1.5,19.7),3,4.5,fill=False,edgecolor='#bb872a',lw=2))
a.add_patch(Rectangle((-3.5,23.7),7,.5,color='#555'))
a.add_patch(Rectangle((-6.5,24.2),13,2,color='#d4aa44'))
a.add_patch(Rectangle((-5,26.2),10,2.4,color='#66aa99'))
a.add_patch(Rectangle((-1.65,28.6),3.3,16,color='#66aa99'))
a.add_patch(Rectangle((-2.2,33.1),4.4,50,fill=False,edgecolor='#447788',lw=2))
a.annotate('Pin 50 mm + bestaande schroef',xy=(2.2,75),xytext=(6,80),arrowprops=dict(arrowstyle='->'),fontsize=9)
a.annotate('Sluitring 0,50 mm\nlast naar frame',xy=(3.5,24),xytext=(7,17),arrowprops=dict(arrowstyle='->'),fontsize=9)
a.annotate('PCB + vier draden\nnaar open zijkant',xy=(-6,7),xytext=(-20,13),arrowprops=dict(arrowstyle='->'),fontsize=9)
a.annotate('Schuifkop: mond Z11,2\nrechte ribben vanaf Z11,7',xy=(2.5,11.5),xytext=(5,4),arrowprops=dict(arrowstyle='->'),fontsize=9)
a.text(-19,-5,'Tandwiellengte in tekening illustratief, niet gemeten.\nElastiekjes rondom buitenzijde bij Z21 en Z38.',fontsize=9)
a.set(xlim=(-22,23),ylim=(-7,86),xlabel='X',ylabel='Z');a.set_aspect('equal');a.grid(alpha=.15)
b.set_title('2 • Werkelijke CAD-doorsnede motorvak op Z6,2')
import trimesh
import numpy as np
h=trimesh.load(H/'half-front.stl',force='mesh')
h.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0]))
r=h.copy();r.apply_scale([1,-1,1])
for m in [h,r]:
 section=m.section(plane_origin=[0,0,6.2],plane_normal=[0,0,1])
 for loop in section.discrete:
  b.plot(loop[:,0],loop[:,1],color='#447788',lw=2)
b.add_patch(Circle((0,0),4,color='#aaa',alpha=.5))
b.add_patch(Rectangle((-8,-3.5),5.5,7,color='#77bb99',alpha=.18))
b.annotate('OPEN PCB-uitsparing\n7 mm breed; volledig huis hoog\nnaar buiten aan één zijde',xy=(-6,0),xytext=(-11,-10),arrowprops=dict(arrowstyle='->'),fontsize=10)
b.annotate('Veren blijven BUITEN\nde PCB-uitsparing',xy=(0,4.2),xytext=(-9,9),arrowprops=dict(arrowstyle='->'),fontsize=10)
b.text(-11,-13,'Groen = vrije ontwerpruimte; PCB-maten niet gemeten.\nBlauw = echte CAD-contour; grijs = Ø8-mm motorhuis.',fontsize=9)
b.set(xlim=(-12,12),ylim=(-14,12));b.set_aspect('equal');b.axis('off')
fig.suptitle('E-302 revisie 2 • Eén PCB-uitsparing + pin van 50 mm',fontsize=15)
fig.tight_layout();fig.savefig(H/'assembly.png',dpi=160);fig.savefig(H/'assembly.svg')
p=H/'assembly.svg';p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')
