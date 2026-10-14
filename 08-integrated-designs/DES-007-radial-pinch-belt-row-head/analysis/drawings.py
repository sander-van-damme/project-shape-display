#!/usr/bin/env python3
"""Dimensioned engineering views and gameplay counterexamples. Output is generated."""
import argparse,json,math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle,Circle

def dim(ax,a,b,text,offset=0):
 ax.annotate('',a,b,arrowprops=dict(arrowstyle='<->',color='#343e48',lw=.8))
 ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+offset,text,ha='center',va='bottom',fontsize=8,backgroundcolor='white')
def rect(ax,x,y,w,h,c,**kw):ax.add_patch(Rectangle((x,y),w,h,facecolor=c,edgecolor='#34404a',lw=.5,**kw))
def setup(ax,title):ax.set_aspect('equal');ax.set_title(title,loc='left',fontsize=12);ax.grid(alpha=.12);ax.set_xlabel('mm');ax.set_ylabel('mm')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--system',type=Path);args=ap.parse_args();out=args.output;out.mkdir(parents=True,exist_ok=True)
 with PdfPages(out/'engineering-drawings.pdf') as pdf:
  fig,axs=plt.subplots(1,2,figsize=(11.7,8.3));ax=axs[0];setup(ax,'Bench assembly: front section X–Z')
  for z,t in [(-30,3),(0,3),(15,3),(20.2,1.6),(34,2),(44,2),(53.2,2)]:rect(ax,-12,z,43.05,t,'#c4cdd4')
  for x,q in zip(np.arange(4)*6.35,[6,0,4,3]):
   rect(ax,x-1.2,-4,2.4,22,'#e7aa53');rect(ax,x-2.5,-4,5,3,'#e7aa53');rect(ax,x-2.5,18,5,2,'#e7aa53')
   rect(ax,x-1.6,20,3.2,20,'#e7aa53');rect(ax,x-2.5,22+q,5,25,'#72b4cb',alpha=.8)
  dim(ax,(0,59),(6.35,59),'6.35 pitch',1);dim(ax,(36,20),(36,40),'20 thread',0)
  ax.set_xlim(-16,45);ax.set_ylim(-33,64)
  ax.text(-12,-20,'Integral rim + captured collar\nTwo radial lands; two square guides',fontsize=9)
  ax=axs[1];setup(ax,'Side section Y–Z: two resident rows')
  for y,z in [(0,-4),(6.35,-10)]:
   rect(ax,y-1.2,z,2.4,18-z,'#e7aa53');rect(ax,y-2.5,z,5,3,'#e7aa53')
   rect(ax,y-2.5,18,5,2,'#e7aa53');rect(ax,y-1.6,20,3.2,20,'#e7aa53');rect(ax,y-2.5,25,5,25,'#72b4cb',alpha=.8)
  for z,t in [(0,3),(15,3),(20.2,1.6),(34,2),(44,2)]:rect(ax,-11,z,32,t,'#c4cdd4',alpha=.45)
  rect(ax,-16,-25,14,4.2,'#7eb896');rect(ax,-4.4-.4,-23,.8,18.8,'#8997a5')
  rect(ax,-3.6,-6.4,.5,5.4,'#aa92c7');rect(ax,-3.0,-4,.2,3,'#303941')
  dim(ax,(25,-10),(25,-4),'6 tier offset');dim(ax,(28,34),(28,44),'10 guide spacing')
  ax.set_xlim(-20,33);ax.set_ylim(-33,64)
  fig.suptitle('DES-007 • mm • nominal geometry, NOT a qualified machine',fontsize=15)
  fig.subplots_adjust(bottom=.16)
  fig.text(.08,.04,'Prototype usable q = 0…6 mm; nut bottom = 22+q; top = 47+q.\nRoof stops upward travel at q≈6.2. Downward collar stop is q≈−2. Never drive either stop.',fontsize=10)
  pdf.savefig(fig);fig.savefig(out/'assembly-sections.png',dpi=140);plt.close(fig)
  fig,ax=plt.subplots(figsize=(11.7,8.3));setup(ax,'Selection plan: 1010 mask; all 16 masks checked in ideal geometry')
  for x in np.arange(4)*6.35:
   ax.add_patch(Circle((x,0),2.5,facecolor='#e7aa53',edgecolor='black'))
   for y in (-6.35,6.35):ax.add_patch(Circle((x,y),2.5,facecolor='none',edgecolor='#999',linestyle='--'))
  for x in np.arange(5)*6.35-3.175:ax.add_patch(Circle((x,-2.3),.5,facecolor='#687987'))
  # Piecewise taut constraint diagram, not a claim about elastic contact curvature.
  xx=[];yy=[]
  for i in range(4):
   x=i*6.35;xx.extend([x-3.175,x,x+3.175]);yy.extend([-2.8,-2.5 if i%2==0 else -2.8,-2.8])
   y=-4.0 if i%2==0 else -4.4
   rect(ax,x-1.2,y+.8,2.4,.5,'#aa92c7');ax.add_patch(Circle((x+3.175,y),.4,facecolor='#526a85'))
  ax.plot(xx,yy,color='#172b39',lw=3,label='belt front: ideal constraint diagram')
  dim(ax,(0,10),(6.35,10),'6.35 mm',.2);dim(ax,(10,-2.8),(10,-2.5),'0.30 off gap',.3)
  ax.text(-3,-12,'Solid: active rims Ø5. Dashed: lower-tier rows at Y±6.35; only +6.35 is present on bench.\nSeparators Ø1 force each OFF span away from its rim. No separators → unchanged middle pin can be driven.\nOffset steel links run between four screw axes; top arms cross above the lower tier.\nNarrow shared tip/rim clearance ≈0.14 mm: shared head needs measured fit/alignment.',fontsize=11)
  ax.set_xlim(-7,29);ax.set_ylim(-17,13);ax.legend(loc='upper right');pdf.savefig(fig);fig.savefig(out/'selection-plan.png',dpi=140);plt.close(fig)
  fig,axs=plt.subplots(1,3,figsize=(11.7,8.3));g=25.4
  for ax,p in zip(axs,[5.08,6.35,12.7]):
   setup(ax,f'{p:g} mm pitch / {round(g/p)} pins per square')
   cap={5.08:4.4,6.35:5.0,12.7:11.8}[p]
   for x in np.arange(p/2,g,p):
    for y in np.arange(p/2,g,p):rect(ax,x-cap/2,y-cap/2,cap,cap,'#cadbe0')
   for x in (0,g):rect(ax,x-.5,-1,1,g+2,'#92797e',alpha=.8)
   for d,c in [(25,'#287b94'),(25.4,'#ba4b43'),(32,'#7959a3')]:ax.add_patch(Circle((g/2,g/2),d/2,fill=False,edgecolor=c,label=f'Ø{d:g} base'))
   dim(ax,(.5,-3),(24.9,-3),'24.4 mm',-.1);ax.set_xlim(-5,31);ax.set_ylim(-7,33)
  axs[1].legend(loc='upper center',bbox_to_anchor=(.5,-.12),ncol=3)
  fig.suptitle('A finer pin pitch does not make grid-line walls zero thickness',fontsize=15)
  fig.text(.08,.11,'25 mm bases are manufacturer-specified by WizKids. One-inch bases also exist.\nAt 1 mm centered wall thickness: 24.4 mm nominal, 24.0 mm with 0.2 mm inward error per wall.\nAllowing Ø25.6 mm base envelope + 0.25 mm placement per side needs ≥26.1 mm clear.\nA 0.4 mm wall leaves 25.0 mm nominal: still no tolerance/placement margin for a 25 mm base.',fontsize=11)
  pdf.savefig(fig);fig.savefig(out/'gameplay-clearance.png',dpi=140);plt.close(fig)
  fig,axs=plt.subplots(1,2,figsize=(11.7,8.3));ax=axs[0];setup(ax,'Bottom-recess wall: placement only; passage gate remains')
  rect(ax,-.5,4.2,1,20,'#a98c8c');rect(ax,24.9,4.2,1,20,'#a98c8c')
  rect(ax,-.1,0,25.6,3.2,'#72b4cb');rect(ax,-2,-1,29.4,1,'#c4cdd4')
  dim(ax,(4,3.2),(4,4.2),'1.0 vertical');dim(ax,(0,-3),(25.4,-3),'25.4 grid')
  ax.text(-1,28,'Assumed base height ≤3.2 mm\n—not a manufacturer-qualified limit.',fontsize=10)
  ax.set_xlim(-5,30);ax.set_ylim(-5,35)
  ax=axs[1];setup(ax,'Corner feet restore support but obstruct traversal')
  for x in (0,25.4):
   rect(ax,x-2,0,4,4,'#a98c8c');rect(ax,x-2,25.4,4,4,'#a98c8c')
  ax.add_patch(Circle((12.7,12.7),12.7,fill=False,color='#287b94'))
  ax.add_patch(Circle((12.7,2),12.7,fill=False,color='#ba4b43',linestyle='--'))
  dim(ax,(2,-13),(23.4,-13),'21.4 between feet')
  ax.set_xlim(-5,31);ax.set_ylim(-15,34)
  fig.suptitle('Wall iteration: preserve the failed traversal witness',fontsize=15)
  fig.text(.08,.06,'An undercut can admit a centered base, but supporting posts still obstruct a one-square passage.\nDo not call this a solved wall system. A wider opening or displaced supports requires an explicit layout trade-off.\nDoors need the same actual-clearance check. Oversized 32 mm bases also overlap neighboring one-inch squares.',fontsize=11)
  pdf.savefig(fig);plt.close(fig)
  if args.system:
   data=json.loads(args.system.read_text())['grids']['64'];fig,axs=plt.subplots(1,2,figsize=(11.7,8.3));bs=[2,4,6,8]
   for kind,style in [('loop','--'),('strip','-')]:
    vals=[data[f'B{b}_rpm850_L3_{kind}']['scene']['seconds'] for b in bs]
    axs[0].plot(bs,vals,style,marker='o',label=kind+' (conditional)')
   axs[0].axhline(30,color='#b44',label='30 s benchmark');axs[0].set(xlabel='Full-row heads',ylabel='Worst sampled scene, seconds',title='Complete modeled mechanical cycle');axs[0].legend()
   low=[data[f'B{b}_rpm850_L3_loop']['cost_usd'][0] for b in bs];high=[data[f'B{b}_rpm850_L3_loop']['cost_usd'][1] for b in bs]
   axs[1].fill_between(bs,low,high,alpha=.25);axs[1].plot(bs,low,marker='o');axs[1].axhline(1500,color='#b44');axs[1].set(xlabel='Full-row heads',ylabel='USD scenario',title='Catalog servo selector implementation')
   fig.suptitle('More parallel heads do not establish an affordable solution',fontsize=15)
   fig.text(.08,.10,'850 rpm and 3 mm lead are assumptions, not qualified powered speed. Manual wall/miniature work is extra.\nSolid line pays finite-strip return; dashed loop omits that return but has no qualified belt construction.\nThe selected prototype is a manual four-output strip rig, not any of these full machines.',fontsize=11)
   pdf.savefig(fig);plt.close(fig)
 print(out/'engineering-drawings.pdf')
if __name__=='__main__':main()
