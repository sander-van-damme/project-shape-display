#!/usr/bin/env python3
"""Dimensioned explanatory section for the zero-print diagnostic.

Reproduce: python scripts/draw_section.py
Requires matplotlib + numpy. Reads the accompanying geometry audit and writes
one SVG. This is a schematic, not CAD or a new printable component.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
from matplotlib.lines import Line2D

BASE = Path(__file__).resolve().parents[1]
AUDIT = json.loads((BASE/'metadata/geometry-review.json').read_text())
D = AUDIT['contact_dimensions_from_cad']
assert D['rotor_radial_band_z_mm'] == [21.2, 24.9]
assert D['square_guide_z_mm'] == [32.7, 72.7]
assert AUDIT['travel_limits']['low_pin_bottom_z_mm'] == 27.9
assert D['radial_band_length_mm'] == 3.7
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
                     'svg.fonttype':'none', 'svg.hashsalt':'v3-contact-map',
                     'axes.titleweight':'bold'})
C = {'frame':'#d9dfe5','edge':'#6b7785','pin':'#177f99','rotor':'#d77a35',
     'washer':'#d6ad32','motor':'#8474a8','ink':'#243746','dim':'#526577'}
fig=plt.figure(figsize=(14,10.5),facecolor='white')
fig.text(.045,.95,'Where rising can change the contact',fontsize=22,weight='bold',color=C['ink'])
fig.text(.045,.918,'Current v3 nominal geometry • long screw + virtual footless 50-mm pin • all dimensions in mm',fontsize=11,color=C['dim'])
fig.text(.045,.891,'Owner: long screw, approximately 15-mm rise; exact pin length and later knife cuts are not reconstructed.',fontsize=10,color=C['dim'])

def box(ax,x,z,w,h,color,edge=None,lw=.8,zorder=3,**kw):
    ax.add_patch(Rectangle((x,z),w,h,facecolor=color,edgecolor=edge or color,lw=lw,zorder=zorder,**kw))

def dim(ax,x,z0,z1,label,side=1,fontsize=9):
    ax.annotate('',xy=(x,z1),xytext=(x,z0),arrowprops={'arrowstyle':'<->','color':C['dim'],'lw':.8},zorder=12)
    ax.plot([x-.5,x+.5],[z0,z0],color=C['dim'],lw=.6)
    ax.plot([x-.5,x+.5],[z1,z1],color=C['dim'],lw=.6)
    ax.text(x+side*.6,(z0+z1)/2,label,va='center',ha='left' if side>0 else 'right',fontsize=fontsize,color=C['dim'])

def lower(ax):
    # Schematic frame section: only functional axial surfaces shown.
    for sign in [-1,1]:
        x=2 if sign>0 else -6
        box(ax,x,11.4,4,1.0,C['frame'],C['edge'])
        x=3.65 if sign>0 else -6
        box(ax,x,12.4,2.35,.25,C['frame'],C['edge'])
        x=3.7 if sign>0 else -6
        box(ax,x,21.2,2.3,3.7,C['frame'],C['edge'])
        x=2.1 if sign>0 else -6
        box(ax,x,25.2,3.9,2,C['frame'],C['edge'])
    box(ax,-4,2,8,9.2,C['motor'],C['ink'])
    box(ax,-1.5,11.2,3,.25,C['motor'],C['ink'])
    box(ax,-.4,11.45,.8,3.1,C['motor'],C['ink'])
    box(ax,-3.5,12.9,7,12,C['rotor'],C['ink'])
    box(ax,-1.25,12.9,2.5,6,'white',C['rotor'],lw=.5,zorder=4)
    box(ax,-.4,11.45,.8,3.1,C['motor'],C['ink'],zorder=5)
    # Gear envelope; tooth profile is deliberately not invented.
    box(ax,-1.1,13.2,2.2,1.25,C['motor'],C['ink'],zorder=5)
    for x in [-3.5,1.6]:box(ax,x,12.4,1.9,.5,C['washer'],C['ink'],zorder=5)
    box(ax,-1.6,24.9,3.2,48,C['rotor'],C['ink'],lw=.5)
    # Thread helix represented as a symbol, not exact tooth geometry.
    for z in np.arange(25.2,72.5,3):
        ax.plot([-1.6,1.6],[z,z+1.1],lw=.45,color='#a84c1f',zorder=4)

def main(ax,rise,title):
    ax.set_xlim(-10,13);ax.set_ylim(0,99)
    ax.set_title(title,loc='left',fontsize=13,pad=8,color=C['ink'])
    lower(ax)
    for x in [-5,2.4]:box(ax,x,32.7,2.6,40,C['frame'],C['edge'])
    p=27.9+rise
    # Hollow square pin; lower 6-mm thread is symbolized, upper bore is square.
    for x in [-2.2,1.76]:box(ax,x,p,.44,50,C['pin'],C['pin'],lw=.7,zorder=6)
    for x in [-2.2,1.3]:box(ax,x,p,.9,6,C['pin'],C['pin'],zorder=6)
    ax.plot([-2.2,2.2],[p+50,p+50],color=C['pin'],lw=1.3,zorder=6)
    ax.plot([-2.2,2.2],[p,p],color=C['pin'],lw=.8,zorder=6)
    for z,txt in [(32.7,'32.7'),(72.7,'72.7')]:
        ax.plot([-9.2,5.5],[z,z],lw=.6,ls=(0,(3,3)),color='#9aa8b2',zorder=0)
        ax.text(-9.4,z+.8,txt,fontsize=8,color=C['dim'])
    ax.text(3,p+51.6,f'Pin tip Z{p+50:.1f}',fontsize=9,color=C['pin'],ha='center')
    ax.text(3,p+0.8 if rise==0 else p-2.2,f'Bottom Z{p:.1f}',fontsize=9,color=C['pin'])
    if rise==0:
        dim(ax,8,32.7,72.7,'40\nguide')
        ax.text(5.9,84,'5.2 tip\noverhang',fontsize=9,color=C['dim'])
        ax.annotate('',xy=(4,77.9),xytext=(6.3,84),arrowprops={'arrowstyle':'-','lw':.7,'color':C['dim']})
        ax.text(-8.7,7,'Motor',fontsize=9,color=C['motor'])
        ax.text(-8.7,18,'Rotor',fontsize=9,color=C['rotor'])
    else:
        dim(ax,8,42.9,72.7,'29.8\nguided')
        dim(ax,8,72.7,92.9,'20.2\nexposed')
    ax.plot([-9,9],[0,0],color=C['edge'],lw=1)
    ax.text(-9,-3.1,'Z0: frame bottom',fontsize=8,color=C['dim'])
    ax.axis('off')

ax1=fig.add_axes([.045,.225,.22,.61]); main(ax1,0,'A  Low reference')
ax2=fig.add_axes([.285,.225,.22,.61]); main(ax2,15,'B  +15 mm, diagnostic pose')
fig.text(.045,.19,'Same 48-mm screw; the lower 6-mm pin thread remains engaged in both poses.',fontsize=10,color=C['ink'])
fig.text(.045,.165,'Guide overlap decreases as the pin rises. A larger tip lever arm, bow or axis error\ncan nevertheless increase side reactions and cause binding.',fontsize=10,color=C['ink'],linespacing=1.45,va='top')
fig.text(.045,.115,'Axial positions are proportional; transverse widths are enlarged for legibility.\nFrame exterior, PCB, wires and bands omitted. This is not an assembly drawing.',fontsize=9,color=C['dim'],linespacing=1.45,va='top')

# Enlarged functional axial support section.
ax=fig.add_axes([.555,.485,.40,.35]);ax.set_xlim(-11,17);ax.set_ylim(8.4,30)
ax.set_title('C  The rotor is not inside a 12-mm sleeve',loc='left',fontsize=13,pad=12,color=C['ink'])
lower(ax)
dim(ax,-8,12.9,24.9,'12-mm\nbody',side=-1)
dim(ax,8,21.2,24.9,'3.7-mm\njournal')
ax.annotate('0.30 axial float\nthen upper thrust contact',xy=(3,25.05),xytext=(7.7,28.8),fontsize=9,color=C['dim'],arrowprops={'arrowstyle':'-','lw':.8,'color':C['dim']})
ax.annotate('Washer\nID3.2 / OD7 / 0.50',xy=(3,12.65),xytext=(7.7,16),fontsize=9,color=C['dim'],arrowprops={'arrowstyle':'-','lw':.8,'color':C['dim']})
ax.annotate('L gear + C cavity\nTorque; axial sliding needed',xy=(1,13.8),xytext=(7.7,10.7),fontsize=8.5,ha='left',color=C['dim'],arrowprops={'arrowstyle':'-','lw':.8,'color':C['dim']})
ax.axis('off')
fig.text(.555,.452,'Journal Ø7.4 around rotor Ø7 → 0.20 radial gap.\nDownward reaction: rotor → washer → deck.\nUpward reaction: shoulder → upper stop after float is taken up.',fontsize=10,color=C['ink'],linespacing=1.5,va='top')

# Cross-section of square guide and hollow pin, communicating side clearances.
a=fig.add_axes([.555,.238,.125,.15]);a.set_xlim(-4.5,4.5);a.set_ylim(-4.5,4.5);a.set_aspect('equal')
box(a,-3.9,-3.9,7.8,7.8,C['frame'],C['edge'])
box(a,-2.4,-2.4,4.8,4.8,'white',C['edge'])
box(a,-2.2,-2.2,4.4,4.4,C['pin'],C['pin'])
box(a,-1.76,-1.76,3.52,3.52,'white',C['pin'])
a.add_patch(Circle((0,0),1.6,fc=C['rotor'],ec=C['ink'],lw=.6,zorder=4))
a.axis('off')
fig.text(.69,.365,'D  Transverse contacts',fontsize=12,weight='bold',color=C['ink'])
fig.text(.69,.337,'Guide 4.8 square / pin 4.4 square\n0.20 per face, nominal\nPin bore 3.52 square / screw Ø3.2\nMinimum screw-to-bore gap 0.16',fontsize=10,color=C['ink'],linespacing=1.6,va='top')
fig.text(.555,.216,'These clearances are not measured print tolerances.\nClosing pressure can alter real alignment and contact.',fontsize=9,color=C['dim'],linespacing=1.5,va='top')

fig.text(.555,.165,'Retained-foot caveat',fontsize=11,weight='bold',color=C['ink'])
fig.text(.555,.14,'The source pin STL has a 12 × 12 × 0.24 print foot. If retained, it\nhits the guide after +4.56 mm from this low datum. The owner\nreports artifact removal; this is not the leading cause of the\nreported 15-mm run. No additional cutting is prescribed.',fontsize=9,color=C['dim'],linespacing=1.4,va='top')

legend=[Line2D([0],[0],color=C[k],lw=7,label=label) for k,label in [('frame','Stationary frame'),('pin','Moving pin'),('rotor','Screw + rotor'),('washer','Thrust washer'),('motor','Motor + gear')]]
fig.legend(handles=legend,loc='lower left',bbox_to_anchor=(.04,.042),ncol=5,frameon=False,fontsize=9,handlelength=1.2,columnspacing=2.5)
fig.text(.045,.025,'Digital contact schematic • 23 October 2026 • Existing-parts isolation test; no new print and no claim of proven low friction.',fontsize=9,color=C['dim'])
path=BASE/'images/contact-map.svg';path.parent.mkdir(exist_ok=True)
fig.savefig(path,format='svg',metadata={'Date':None,'Creator':'Shape Display contact diagnostic, draw_section.py'})
path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines()) + '\n')
plt.close(fig)
print(path)
