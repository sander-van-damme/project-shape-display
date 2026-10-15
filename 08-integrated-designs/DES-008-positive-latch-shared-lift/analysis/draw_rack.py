#!/usr/bin/env python3
"""Draw actual exported CAD meshes and explicit nominal contact sections."""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
HERE=Path(__file__).resolve().parent
COLORS={'pin':'#de9b29','ground_comb':'#bd354d','root_clamp':'#9555a5','drive_key':'#2c9c71','carriage_base':'#29466e','carriage_lid':'#4473a2','ground_seat':'#9b9fa3','upper_guide':'#bdc3c9','lower_guide':'#bdc3c9','bottom_guide':'#bdc3c9','spacer':'#aeb6be','frame_foot':'#535a61','dog_keeper':'#9bc542','bolt':'#4e5359','nut':'#4e5359'}
def dim(ax,a,b,label,offset=(0,0),textoffset=(0,0)):
 a=np.array(a,float);b=np.array(b,float);d=np.array(offset,float);aa=a+d;bb=b+d
 ax.plot([a[0],aa[0]],[a[1],aa[1]],color='#6b7280',lw=.6);ax.plot([b[0],bb[0]],[b[1],bb[1]],color='#6b7280',lw=.6)
 ax.annotate('',xy=aa,xytext=bb,arrowprops=dict(arrowstyle='<->',lw=.8,color='#243040'))
 mid=(aa+bb)/2+np.array(textoffset);ax.text(*mid,label,ha='center',va='center',fontsize=9,backgroundcolor='white')
def box(ax,x,y,w,h,c,alpha=1):ax.add_patch(Rectangle((x,y),w,h,facecolor=c,edgecolor='#303640',lw=.7,alpha=alpha))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--meshes',type=Path,default=Path('work/des008-handoff-review/components'));ap.add_argument('--output',type=Path,default=Path('work/des008-rack'));ap.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'cad/rack_handoff.scad');ap.add_argument('--provenance',type=Path,default=Path('work/des008-handoff-review/poses.json'));a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
 sha=hashlib.sha256(a.source.read_bytes()).hexdigest();meshes=[]
 assert json.loads(a.provenance.read_text())['source_sha256']==sha, 'Component provenance differs from CAD'
 assert a.meshes.is_dir(), 'Missing verified component directory'
 COUNTS={'pin':8,'ground_comb':2,'drive_key':4,'carriage_base':1,'carriage_lid':1,'root_clamp':2,'lower_guide':1,'upper_guide':1,'ground_seat':1,'bottom_guide':1,'frame_foot':4,'spacer':12,'dog_keeper':4,'bolt':10,'nut':10}
 expected={f'{name}-{i}' for name,count in COUNTS.items() for i in range(count)}
 assert all((a.meshes/(name+'.stl')).is_file() for name in expected), 'Incomplete assembly components'
 for path in sorted(a.meshes.glob('*.stl')):
  if path.stem not in expected:continue
  key=path.stem.rsplit('-',1)[0];m=trimesh.load_mesh(path)
  color=COLORS.get(key,'#888888')
  if key=='pin' and int(path.stem.rsplit('-',1)[1])>=4:color='#62a5c3'
  meshes.append((key,m,color))
 def footer(fig):fig.text(.04,.025,'DES-008 manual support-transfer article | mm | nominal CAD, no physical qualification | source '+sha[:16],fontsize=9,color='#44505f')
 with PdfPages(a.output/'dimensioned-rig.pdf') as pdf:
  f=plt.figure(figsize=(16.54,11.69));f.suptitle('Four active racks + four untouched witnesses',x=.04,y=.965,ha='left',fontsize=24,weight='bold')
  f.text(.04,.92,'6.35-mm pitch  •  0–10-mm permitted terrain heights  •  signed 5-mm pulses  •  manual selection and load handoff',fontsize=13)
  ax=f.add_axes([.025,.20,.53,.67],projection='3d')
  for key,m,c in meshes:
   poly=Poly3DCollection(m.triangles,facecolors=c,edgecolors='none',linewidths=0,alpha=1);ax.add_collection3d(poly)
  ax.set(xlim=(-28,48),ylim=(-16,18),zlim=(-32,86));ax.set_box_aspect((76,34,118));ax.view_init(elev=20,azim=-62);ax.set_axis_off()
  f.text(.04,.17,'Orange: active racks. Blue: witnesses. Red: stationary ground pawls.\nGreen: moving captured dogs. Purple: clamped comb roots. Grey plates carry load.',fontsize=11)
  ax2=f.add_axes([.58,.30,.36,.53]);ax2.set_aspect('equal');ax2.set_xlim(-31,68);ax2.set_ylim(-38,91);ax2.axis('off')
  for z,h in [(-14,5),(29,3),(48,4),(59,3)]:box(ax2,-25,z,70.05,h,'#c1c7ce')
  for x in [-22,42.05]:box(ax2,x-2.75,-9,5.5,38,'#a8b0b8');box(ax2,x-4.5,-31,9,17,'#59616a')
  for i,h in enumerate([0,5,10,5]):box(ax2,i*6.35-2.3,-25+h,4.6,95,'#de9b29');box(ax2,i*6.35-2.3,70+h,5,2,'#de9b29')
  ax2.plot([-22,42.05],[6.725,6.725],lw=7,color='#29466e')
  dim(ax2,(-25,59),(45.05,59),'70.05 frame width',(0,31),(0,2))
  dim(ax2,(-22,-31),(42.05,-31),'64.05 bolt centers',(0,-5),(0,1))
  dim(ax2,(45.05,-31),(45.05,82),'113 maximum cap height',(7,0),(2,0))
  ax2.text(-24,37,'Lower guide: Z29–32',fontsize=9);ax2.text(-24,54,'4-mm rigid pawl seat: Z48–52',fontsize=9)
  ax2.text(-24,-22,'Bottom guide: Z−14–−9',fontsize=9)
  f.text(.57,.18,'Frame stack, bottom to top:\n5 guide + 38 sleeves + 3 guide + 16 sleeves + 4 seat + 7 sleeves + 3 guide = 76 mm.\nM3×80 heads above; 2.4-mm nuts below; nominal 1.6-mm thread protrusion.\nFour 17-mm gravity foot cups clear nuts and keep pin tips 6 mm above bench.',fontsize=11,linespacing=1.5)
  footer(f);pdf.savefig(f);f.savefig(a.output/'assembly.png',dpi=160);plt.close(f)
  f=plt.figure(figsize=(16.54,11.69));f.suptitle('Nominal contact geometry and manual transaction',x=.04,y=.96,ha='left',fontsize=24,weight='bold')
  ax=f.add_axes([.05,.43,.42,.42]);ax.set_aspect('equal');ax.set_xlim(-7.2,3);ax.set_ylim(47,55.5);ax.axis('off')
  box(ax,-2.7,48,1.2,4,'#9b9fa3');box(ax,-1.4,47,2.8,3,'#de9b29');box(ax,-.55,50,1.1,3.2,'#de9b29');box(ax,-1.4,53.2,2.8,2.0,'#de9b29')
  box(ax,-3.45,47,.6,5,'#bd354d');box(ax,-3.45,52,1.8,1.2,'#bd354d');box(ax,-1.65,52,.70,1.2,'#bd354d')
  dim(ax,(-1.4,53.2),(-.95,53.2),'0.45 engagement',(0,1),(0,.3));dim(ax,(-.95,52),(-.55,52),'0.40 root gap',(0,-1.1),(0,-.3));dim(ax,(-2.7,48),(-1.5,48),'1.20 ledge',(0,-.7),(0,-.3))
  ax.text(0,1.06,'Ground support: middle of groove, X=0',transform=ax.transAxes,fontsize=13,weight='bold');ax.text(-6.8,49,'Load → pawl foot\n→ fixed seat\n→ clamped frame',fontsize=10)
  ax=f.add_axes([.55,.43,.40,.42]);ax.set_aspect('equal');ax.set_xlim(-2.2,5.0);ax.set_ylim(3.5,10.4);ax.axis('off')
  box(ax,-1.4,3.5,2.8,1.5,'#de9b29');box(ax,-.55,5,1.1,3.2,'#de9b29');box(ax,-1.4,8.2,2.8,1.8,'#de9b29')
  box(ax,.95,5.3,.90,2.6,'#2c9c71');box(ax,1.85,5.3,1.65,2.6,'#2c9c71')
  dim(ax,(.55,8.2),(1.4,8.2),'0.85 groove depth',(0,.65),(0,.3));dim(ax,(3.5,5.3),(3.5,7.9),'2.60 dog',(0.8,0),(.15,0))
  ax.text(0,1.06,'Captured dog: both groove flanks are functional',transform=ax.transAxes,fontsize=13,weight='bold');ax.text(2.1,4.0,'3.20 groove opening\n0.60 reversal backlash\n+ up to 0.25 key-slot play',fontsize=10)
  f.text(.05,.32,'Rail and guidance dimensions',fontsize=15,weight='bold')
  f.text(.05,.295,'Pin 4.6 × 2.8; guide aperture 5.0 × 3.0; groove width 3.4; tooth width 2.4.\nContinuous 0.6-mm X-edge lands preserve Y guidance through every rack phase.\nSleeves OD 5.5 / ID 3.2; carriage bore 5.9, effective bearing length 18.4.\nPin guides at Z−14…−9, Z29…32 and Z59…62. Cap 5×5×2; pin body 95 mm.\nCarrier floor 3.6; lid 6.0; root-clamp underside relief 0.30.',fontsize=12,linespacing=1.6,va='top')
  f.text(.55,.32,'Order is essential',fontsize=15,weight='bold')
  f.text(.55,.295,'1. Capture only selected dogs; lock both ON and OFF handles.\n2. Raise gently until selected ground pawls are visibly unloaded.\n3. Retract only those pawls and insert their grounded keepers.\n4. Move until every target groove admits its ground pawl.\n5. Restore all pawls; seat and retire each dog individually.',fontsize=12,linespacing=1.6,va='top')
  f.text(.05,.08,'These sections omit continuous edge rails outside X=0. Clearance arithmetic is nominal.\nUse observed pin/groove alignment for lowering; head displacement alone does not prove forced descent.\nInspect every pawl and keeper. Stop on binding, lost support, damaged fingers or unintended neighbor motion.',fontsize=12,color='#9a3412',linespacing=1.4)
  footer(f);pdf.savefig(f);f.savefig(a.output/'contact-sections.png',dpi=160);plt.close(f)
if __name__=='__main__':main()
