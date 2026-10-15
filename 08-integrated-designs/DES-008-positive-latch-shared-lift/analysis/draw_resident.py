#!/usr/bin/env python3
"""Dimensioned schematic sections matching resident_cell.scad; not shop drawings."""
from pathlib import Path
import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Polygon,Circle
from matplotlib.backends.backend_pdf import PdfPages
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=Path('work/des008-resident'));args=parser.parse_args()
ROOT=args.output;ROOT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.size':10,'font.family':'DejaVu Sans'})
def rect(ax,x,y,w,h,c,**kw):ax.add_patch(Rectangle((x,y),w,h,facecolor=c,edgecolor='black',lw=.5,**kw))
def dim(ax,a,b,label,off=(0,0)):
 ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='<->',lw=.9));ax.text((a[0]+b[0])/2+off[0],(a[1]+b[1])/2+off[1],label,ha='center',va='center',fontsize=9,bbox=dict(facecolor='white',alpha=.8,edgecolor='none',pad=1))
with PdfPages(ROOT/'resident-study-sections.pdf') as pdf:
 f,axs=plt.subplots(1,2,figsize=(11.7,8.3));f.suptitle('Rejected reference C-guide — moving A dog section\nSource 78042351; see the separate bounded guide revision',fontsize=14)
 for ax,b in zip(axs,[1,0]):
  cy=-2.2-1.6*(1-b)
  rect(ax,-1.4,-1.2,2.8,2.4,'lightgray');rect(ax,-1.4,-7.55,2.8,2.4,'lightgray')
  # Actual groove at this Z cuts only the nose's rack pocket.
  rect(ax,.3,-1.2,1,.65,'white')
  rect(ax,2.2,cy-1.2,1.6,2.4,'orange')
  rect(ax,2.5,cy-.85,1,1.7,'white');rect(ax,2.1,cy-.5,.5,1,'white')
  rect(ax,1.65,cy-.4,.35,4,'firebrick',alpha=.8)
  rect(ax,.4,cy-.2,1,.4,'firebrick');rect(ax,1.4,cy-.4,1.25,.8,'firebrick')
  rect(ax,.4,cy-.2,.8,1.7,'firebrick');rect(ax,2.75,cy-.75,.5,1.5,'firebrick')
  rect(ax,2.6,cy-.4,.2,.8,'firebrick')
  rect(ax,1.5,-1.65,.65,.5,'steelblue',alpha=.5)
  ax.set_aspect('equal');ax.set_xlim(-2,4.8);ax.set_ylim(-5.8,1.8);ax.grid(alpha=.2)
  ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_title(('ON: positive capture' if b else 'OFF: terrain remains grounded'))
  dim(ax,(2.2,cy-1.55),(3.8,cy-1.55),'1.6',off=(0,-.2))
  ax.text(-1.8,1.5,'Pin tail 2.8 × 2.4',fontsize=9)
  ax.text(-1.8,-5.6,'Previous row pin starts at Y=−5.15',fontsize=8)
 f.text(.07,.05,'Channel: outer 1.6 × 2.4; cavity 1.0 × 1.7; mouth 1.0. T-foot: 0.5 × 1.5.\nCapture overlap 0.25/side; Y free play ±0.10. A withdrawal 0.85; OFF bit adds 1.60.\nFar-OFF beam clearance to previous pin is only 0.30 nominal before free play and fabrication error.',fontsize=10)
 f.subplots_adjust(bottom=.18,top=.82);pdf.savefig(f);f.savefig(ROOT/'resident-section.png',dpi=160);plt.close(f)
 f,ax=plt.subplots(figsize=(8.3,11.7));f.suptitle('Reference 78042351 — vertical stack and support planes',fontsize=14)
 rect(ax,-1.4,-85,2.8,130,'lightgray');rect(ax,-2.4,45,4.8,90,'lightgray');rect(ax,-2.4,135,4.8,1.2,'gray')
 rect(ax,-2.4,95,4.8,91.2,'none',linestyle='--')
 rect(ax,2.2,-104,1.6,136,'orange');rect(ax,1.65,-52.4,.4,20.45,'slategray');rect(ax,1.65,6.55,.4,20,'navy')
 for z,txt in [(-107,'Memory underside −107'),(-104,'Lower positive Y register −104'),(-96.5,'Lower pocketed code bars −98..−95'),(-30.4,'A acquisition −30.4 (pulse ±20)'),(0,'Ground pawl datum 0'),(30,'Upper positive Y register 30'),(34.4,'Pocketed code bars 34.4–37.4'),(40,'Fixed spring-root frame 40'),(45,'Broad upper body begins 45'),(100,'Lower broad-body guide 100'),(130,'Upper broad-body guide 130'),(136.2,'Low cap 136.2'),(186.2,'High cap 186.2')]:
  ax.plot([-3,7],[z,z],lw=.65,color='gray');ax.text(7.3,z,txt,va='center',fontsize=9)
 ax.annotate('',xy=(-5,186.2),xytext=(-5,-107),arrowprops=dict(arrowstyle='<->'));ax.text(-6.1,40,'293.2 mm before base enclosure',rotation=90,va='center')
 ax.set_xlim(-8,27);ax.set_ylim(-115,195);ax.set_xlabel('X / mm (horizontal magnification)');ax.set_ylabel('Z / mm');ax.grid(alpha=.15)
 f.text(.11,.03,'The tall channels are positively registered at both ends while terrain moves.\nBoth registrations release with the addressed row’s 2-mm lift.\nUpper guide holes, frame joints, actuators, drive and assembly fasteners are not released.',fontsize=10)
 f.subplots_adjust(bottom=.1,top=.93);pdf.savefig(f);f.savefig(ROOT/'resident-stack.png',dpi=150);plt.close(f)
 f,ax=plt.subplots(figsize=(11.7,8.3));f.suptitle('Reference B release — captured follower and grounded pawl ramp',fontsize=14)
 for rel,c,alpha in [(0,'green',.6),(.85,'goldenrod',.5)]:
  rect(ax,-2.45-rel,0,1.75,1.2,c,alpha=alpha)
  ax.add_patch(Polygon([[-2.45-rel,2],[-2.45-rel,3.3],[-1.3-rel,2.15],[-1.3-rel,2]],facecolor=c,alpha=alpha,edgecolor='black'))
 rect(ax,-1.9,-.8,.5,.8,'gray');rect(ax,-1.2,-1.9,1.3,3.1,'none')
 for y,col in [(-2.2,'purple'),(-3.8,'blue')]:
  for z,alpha in [(3.682843,1),(2.482843,.5)]:ax.add_patch(Circle((y,z),.2,facecolor=col,alpha=alpha))
  ax.annotate('',xy=(y,2.482843),xytext=(y,3.682843),arrowprops=dict(arrowstyle='->',color=col))
 ax.text(-2.2,4.2,'ON',ha='center');ax.text(-3.8,4.2,'OFF',ha='center');ax.text(-.9,-1,'Pin\nface',ha='center')
 dim(ax,(-4.4,2.482843),(-4.4,3.682843),'B 1.20',off=(-.3,0))
 ax.set_aspect('equal');ax.set_xlim(-5,1);ax.set_ylim(-2,4.8);ax.set_xlabel('Y / mm');ax.set_ylabel('Z / mm');ax.grid(alpha=.2)
 f.text(.1,.055,'Approach 0.35 mm, then nominal pawl withdrawal 0.85 mm.\nOFF tip clears the fully withdrawn ramp by 0.30 mm nominal; channel free play consumes 0.10 mm.\nA fixed rounded nose is shown, not thousands of roller bearings. Friction, dust and wear remain unqualified.',fontsize=10)
 f.subplots_adjust(bottom=.2,top=.88);pdf.savefig(f);f.savefig(ROOT/'resident-B-ramp.png',dpi=160);plt.close(f)
print(ROOT/'resident-study-sections.pdf')
