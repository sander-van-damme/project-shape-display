#!/usr/bin/env python3
"""Dimensioned concept envelope, not printable CAD or physical qualification."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'tools/curated-experiment-checks/E-295/research/playable-envelope.svg'
pitch=5.08; top=4.88; wall=.8
fig,axs=plt.subplots(1,2,figsize=(12,5))
a=axs[0]
for i in range(5):
 for j in range(5):
  a.add_patch(Rectangle((i*pitch+.1,j*pitch+.1),top,top,facecolor='#e0edf4',edgecolor='#50778b',lw=.5))
for x in [0,25.4]:
 a.add_patch(Rectangle((x-wall/2,-1),wall,27.4,facecolor='#49515b',alpha=.8))
a.add_patch(Circle((12.7,12.7),11.5,fill=False,ec='#25834c',lw=2))
a.add_patch(Circle((12.7,12.7),12.5,fill=False,ec='#c1564a',ls='--',lw=1.5))
a.annotate('',xy=(.4,28),xytext=(25,28),arrowprops={'arrowstyle':'<->'})
a.text(12.7,28.5,'24.6 mm between inner wall faces',ha='center',fontsize=9)
a.annotate('',xy=(.1,-2.5),xytext=(4.98,-2.5),arrowprops={'arrowstyle':'<->'})
a.text(2.54,-3.8,'4.88 top',ha='center',fontsize=9)
a.text(15,-3.8,'0.20 gap; pitch 5.08',ha='center',fontsize=9)
a.text(12.7,13.5,'23 mm base: green\n25 mm base: red dashed',ha='center',fontsize=9)
a.set(xlim=(-3,29),ylim=(-5,31),aspect='equal',title='Top view: 25.4 mm D&D square')
a.set_axis_off()
a=axs[1]
# Schematic section with genuine dimensions, no lower wall penetration.
for i in range(5):
 c=(i+.5)*pitch
 a.add_patch(Rectangle((c-2.2,0),4.4,13,fc='#b1ccdc',ec='#50778b'))
 a.add_patch(Rectangle((c-top/2,13),top,1,fc='#e0edf4',ec='#50778b'))
a.add_patch(Rectangle((7.12,14),6.08,.8,fc='#49515b'))
a.add_patch(Rectangle((9.76,14.8),.8,12,fc='#49515b'))
a.annotate('removable wall + surface foot\nremove before underlying pins move',xy=(10.2,21),xytext=(27,23),arrowprops={'arrowstyle':'->'},fontsize=9)
a.annotate('0.24 mm top overhang per side\n4.4 mm guided body',xy=(7.52,13.6),xytext=(27,12),arrowprops={'arrowstyle':'->'},fontsize=9)
a.annotate('seam admits only 0.20 mm:\n0.8 mm wall cannot descend here',xy=(10.16,13),xytext=(27,3),arrowprops={'arrowstyle':'->'},fontsize=9)
a.set(xlim=(-1,49),ylim=(-2,30),aspect='equal',title='Section: wall stays above pin sweep')
a.set_axis_off()
fig.suptitle('Geometry study only — not the fit coupon or a qualified wall interface',fontsize=11)
fig.tight_layout()
fig.savefig(OUT,metadata={'Date':None})
OUT.write_text('\n'.join(line.rstrip() for line in OUT.read_text().splitlines())+'\n')
print(OUT.relative_to(ROOT))
print({'pitch_mm':pitch,'top_mm':top,'top_area_fraction':round((top/pitch)**2,4), 'body_area_fraction':round((4.4/pitch)**2,4),'corridor_clear_mm':25.4-wall,'minimum_pin_engagement_mm_assumed':6,'stroke_mm_reference':40})
