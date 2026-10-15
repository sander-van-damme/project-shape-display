from pathlib import Path
import trimesh,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import Rectangle,Polygon
import argparse
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=Path('work/des008-memory'));R=p.parse_args().input
def T(x,y,z):
 a=np.eye(4);a[:3,3]=[x,y,z];return a
def RX(a):return trimesh.transformations.rotation_matrix(np.deg2rad(a),[1,0,0])
fig=plt.figure(figsize=(14,9),dpi=160)
ax=fig.add_subplot(221,projection='3d')
def add(name,matrix,color,alpha=1):
 m=trimesh.load(R/(name+'.stl'));m.apply_transform(matrix)
 ax.add_collection3d(Poly3DCollection(m.triangles,facecolor=color,edgecolor='#303942',linewidth=.055,alpha=alpha))
add('base',np.eye(4),'#c6cfd4',.35)
for i,row in enumerate([12,18.35]):
 lift=2.7 if i==0 else 0
 add('cassette',T(0,row,3.9+lift)@np.linalg.inv(T(-1.1,10,2.7)@RX(90)),'#e2b35e')
 for j,col in enumerate([12,18.35]):
  bit=[[0,1],[1,0]][i][j]
  add('flag',T(col+2*bit,row,1.4+lift)@np.linalg.inv(T(1.7,8,2)@RX(90)),'#cb573d')
for j,col in enumerate([12,18.35]):add('codebar',T(col+2*j,0,9.9)@np.linalg.inv(T(1.9,29.5,3.5)@RX(180)),'#4184af')
add('shim',T(-4,12-2.9,3.9),'#72a48f')
M=np.eye(4);M[0,0]=-1
add('shim',T(35.5,12,3.9)@M@T(-4,-2.9,0),'#72a48f')
for y in [4,28]:
 add('keeper',T(0,y,11)@np.linalg.inv(T(-2.4,2.8,4.2)@RX(180)),'#687780')
 for x in [5,27]:add('key',T(x-1.8,y-4.5,11.5),'#de8e37')
ax.set_xlim(-4,40);ax.set_ylim(0,33);ax.set_zlim(0,18)
ax.set_box_aspect((44,33,18));ax.view_init(elev=36,azim=-55)
ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_zlabel('Z / mm')
ax.set_title('One row lifted; other row retained',fontsize=12)
bx=fig.add_subplot(222)
for dx,label,lift in [(0,'Stored / down',0),(9,'Selected / up',2.7)]:
 bx.add_patch(Rectangle((dx-3,0),6,3.5,color='#c6cfd4'))
 for pos in [0,2]:bx.add_patch(Rectangle((dx+pos-.6,1.2),1.2,2.3,color='white',ec='black',lw=.5))
 bx.add_patch(Rectangle((dx-3,3.9+lift),6,.8,color='#e2b35e'))
 bx.add_patch(Rectangle((dx-2,3.8+lift),4,1,color='white',ec='none'))
 bx.add_patch(Rectangle((dx-1.9,9.9),3.8,3.5,color='#4184af'))
 bx.add_patch(Rectangle((dx-.7,9.85),1.4,2.65,color='white',ec='none'))
 bx.add_patch(Rectangle((dx-.4,1.4+lift),.8,3.3,color='#cb573d'))
 bx.add_patch(Rectangle((dx-1.7,4.7+lift),3.4,1.2,color='#cb573d'))
 bx.add_patch(Rectangle((dx-.5,5.9+lift),1,3.5,color='#cb573d'))
 bx.text(dx,14,label,ha='center',fontsize=10)
 if lift==0:bx.text(dx+1,9.4,'0.5 idle\ngap',fontsize=9)
 else:bx.text(dx+1.8,12.4,'0.4 roof\ngap',fontsize=9)
bx.text(0,-.4,'Foot engagement 2.1\nPocket floor ≥1.2 thick\nNominal overlap 1.6',ha='center',va='top',fontsize=9)
bx.text(9,-.4,'Row lift 2.7\nFoot release gap 0.6\nLug/channel X: 1.0 / 1.4',ha='center',va='top',fontsize=9)
bx.set_xlim(-3.5,13.5);bx.set_ylim(-2.7,14.6);bx.set_aspect('equal');bx.set_title('X–Z section / mm (cassette roof omitted here)',fontsize=12);bx.axis('off')
cx=fig.add_subplot(223)
cx.add_patch(Rectangle((-2.7,0),5.4,3,color='#e2b35e'))
cx.add_patch(Rectangle((-2.2,.8),4.4,1.4,color='white'))
cx.add_patch(Rectangle((-1.4,-.1),2.8,3.2,color='white'))
cx.add_patch(Rectangle((-1.2,-2.5),2.4,3.3,color='#cb573d'))
cx.add_patch(Rectangle((-2,.8),4,1.2,color='#cb573d'))
cx.add_patch(Rectangle((-1.2,2),2.4,3.5,color='#cb573d'))
cx.annotate('Retaining roof: 0.8 thick',xy=(2.05,2.6),xytext=(3.6,4.4),arrowprops={'arrowstyle':'->'},fontsize=10)
cx.annotate('4.0 × 1.2 shoulder\nin 4.4 × 1.4 slot',xy=(-1.8,1.5),xytext=(-7,4.2),arrowprops={'arrowstyle':'->'},fontsize=10)
cx.annotate('2.8 wide central opening',xy=(1.4,0),xytext=(3.6,-1.5),arrowprops={'arrowstyle':'->'},fontsize=10)
cx.text(0,-3.2,'Cassette outer Y = 5.4; neighboring rows = 6.35\nLoad flags through the X=23.2–27.5 window off the base.\nSlide first flag to X=12, then load the second at X=18.35.',ha='center',va='top',fontsize=9)
cx.set_xlim(-7.5,8.5);cx.set_ylim(-5,6);cx.set_aspect('equal');cx.set_title('Y–Z section: positive shoulder capture',fontsize=12);cx.axis('off')
dx=fig.add_subplot(224)
dx.add_patch(Rectangle((3.5,0),1.2,4,color='#cb573d'))
dx.add_patch(Rectangle((0,.8),3.5,2.4,color='#cb573d'))
dx.add_patch(Rectangle((4.7,.8),3.3,2.4,color='#cb573d'))
for x in [-1.5,8.3]:dx.add_patch(Rectangle((x,0),1.2,.96,color='#687780'))
for x in [-.3,8]:dx.add_patch(Rectangle((x,.8),.3,.16,color='#de8e37'))
dx.plot([-1.5,9.5],[0,0],color='black',lw=.8)
dx.annotate('Clip only the 0.16-thick end necks',xy=(8.15,.88),xytext=(2.5,5.2),arrowprops={'arrowstyle':'->'},fontsize=10)
dx.annotate('',xy=(-.15,.88),xytext=(2.5,5.0),arrowprops={'arrowstyle':'->'})
dx.text(4,-.8,'Side-down flag with sacrificial end towers\n3.8 and 3.6 mm bridges; no support under the functional sides.\nInspect bridges and measure the clipped height before testing.',ha='center',va='top',fontsize=9)
dx.set_xlim(-2.5,10.5);dx.set_ylim(-3,6.2);dx.set_aspect('equal');dx.set_title('Flag print section / mm',fontsize=12);dx.axis('off')
fig.suptitle('Revision 3 — 2 × 2 positive-pocket memory at 6.35 mm pitch',fontsize=16)
fig.text(.06,.022,'A restricted planar screen is not a general tolerance proof; use deliberate side/tilt-bias handoff tests.\nPhysical fit, bridge quality, friction, wear and powered timing are unqualified. Keep all four keeper keys fully inserted.',fontsize=10)
fig.tight_layout(rect=[0,.075,1,.95]);fig.savefig(R/'assembly.png');fig.savefig(R/'assembly.pdf');plt.close(fig)
