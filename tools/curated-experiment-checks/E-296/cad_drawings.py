#!/usr/bin/env python3
"""Dimensioned explanatory drawings generated from the same E-296 parameters.

The coloured sections are analytical drawings; assembly-*.svg comes directly
from the nominal BREP. Neither is evidence of physical fit or reliable motion.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon
import cadquery as cq
import generate as g

HERE=Path(__file__).resolve().parent
OUT=HERE/"drawings"
C={"row":"#247fa9","column":"#c64d53","sleeve":"#dca447",
   "shaft":"#606971","spring":"#747464","pin":"#73ad88"}

def rect(ax,x,z,w,h,color,**kw):
    ax.add_patch(Rectangle((x,z),w,h,facecolor=color,edgecolor="#343a40",lw=.65,**kw))

def section(ax,r,c,title,phaseblocked=False):
    q=g.phase_block_q() if phaseblocked else g.q_nominal(r,c)
    # Accurate nominal center section through hex vertices, not an AF section.
    for x in [-1.5]:rect(ax,x,-.6+q,3,4.7,C["sleeve"])
    rect(ax,-2.1,3.7+q,4.2,.4,C["sleeve"])
    rect(ax,-1.7,-.6+q,3.4,.4,C["sleeve"])
    inner=1.95/math.sqrt(3);mouth=2.7/math.sqrt(3)
    rect(ax,-inner,-.61+q,2*inner,4.335,"white")
    ax.add_patch(Polygon([(-inner,3.725+q),(inner,3.725+q),
                          (mouth,4.1+q),(-mouth,4.1+q)],
                         closed=True,facecolor="white",edgecolor="#343a40",lw=.6))
    male=1.8/math.sqrt(3)
    rect(ax,-male,-1.9,2*male,5.2,C["shaft"])
    # In the blocked-phase section y=0 intersects the rotated male at AF/2.
    hm=.9 if phaseblocked else male
    rect(ax,-hm,4.7,2*hm,2.3,C["shaft"])
    rect(ax,-1.8,7.,3.6,.4,C["shaft"])
    for x in [-2.35,1.6]:rect(ax,x,r,.75,.3,C["row"])
    for x in [-2.35,1.2]:rect(ax,x,4.1+c,1.15,.4,C["column"])
    bot=.3+r;top=3.7+q
    for side in [-1,1]:
        for j in range(6):
            z=bot+.1+(top-bot-.2)*j/5
            ax.add_patch(Circle((side*1.85,z),.1,fc=C["spring"],ec="#343a40",lw=.4))
    ax.axvline(0,color="#999",lw=.5,ls="-.")
    ax.set_xlim(-2.75,2.75);ax.set_ylim(-1,7.7);ax.set_aspect("equal")
    ax.set_title(title+f"\nq={q:.3f} mm",fontsize=10)
    ax.set_xticks([-2,0,2]);ax.set_yticks([0,2,4,6]);ax.grid(alpha=.16)
    ax.set_xlabel("x [mm]");ax.set_ylabel("z [mm]")

def drawings():
    OUT.mkdir(exist_ok=True)
    fig,axs=plt.subplots(1,5,figsize=(14,5),layout="constrained")
    states=[(0,0,"R0 C0: uit"),(0,1.4,"R0 C1: uit"),
            (1.4,0,"R1 C0: geblokkeerd"),(1.4,1.4,"R1 C1: gekoppeld")]
    for ax,(r,c,t) in zip(axs,states):section(ax,r,c,t)
    section(axs[4],1.4,1.4,"R1 C1: fase 30°",True)
    fig.suptitle("E-296 — één schuifhuls; rij veert omhoog, kolomdak begrenst de hoogte\n"
                 "Nominale middendoorsneden [mm]; veren schematisch; invoer onder, schroef boven",fontsize=12)
    fig.savefig(OUT/"truth-sections.svg");fig.savefig(OUT/"truth-sections.png",dpi=190);plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(11,4.6),layout="constrained")
    for k,ax in enumerate(axs):
        ax.set_aspect("equal");ax.set_xlim(-3,8.1);ax.set_ylim(-3,8.1)
        rect(ax,-2.54,-2.54,10.16,10.16,"none",linestyle="--")
        for i,x in enumerate([0,5.08]):
            for j,y in enumerate([0,5.08]):
                if k==0:
                    rect(ax,x-2.2,y-2.2,4.4,4.4,C["pin"])
                    ax.text(x,y,"(0,0)\nEN" if i==j==0 else f"({i},{j})\nuit",ha="center",va="center",fontsize=9)
                else:
                    col=C["row"] if k==1 else C["column"]
                    ax.add_patch(Circle((x,y),2.35,fc=col,ec="#343a40",lw=.7))
                    ax.add_patch(Circle((x,y),1.6 if k==1 else 1.2,fc="white",ec="#343a40",lw=.7))
                    ax.add_patch(Circle((x,y),1.5 if k==1 else 1.039,fc=C["sleeve"] if k==1 else C["shaft"],ec="#343a40",lw=.6))
        if k==1:
            for y in [0,5.08]:
                rect(ax,2.35,y-.4,.38,.8,C["row"])
                ax.plot([-2.35,7.43],[y,y],color="white",lw=.7,ls="--")
        if k==2:
            for x in [0,5.08]:rect(ax,x-.4,2.35,.8,.38,C["column"])
        ax.annotate("",xy=(0,7.75),xytext=(5.08,7.75),arrowprops={"arrowstyle":"<->","lw":.8})
        ax.text(2.54,7.87,"5,08 mm",ha="center",fontsize=9)
        ax.set_xlabel("x [mm]");ax.set_ylabel("y [mm]");ax.grid(alpha=.16)
    axs[0].set_title("Pinnen: 4,40 mm vierkant\n0,68 mm nominale naad")
    axs[1].set_title("Rijvlak: ring Ø4,70 / Ø3,20\n0,38 mm tussen ringen")
    axs[2].set_title("Kolomvlak: ring Ø4,70 / Ø2,40\nMinimaal 2,40 mm boven rijvlak")
    fig.suptitle("2×2 actief veld 10,16 × 10,16 mm; externe geleideschoenen buiten dit veld",fontsize=12)
    fig.savefig(OUT/"layer-plans.svg");fig.savefig(OUT/"layer-plans.png",dpi=190);plt.close(fig)
    parts,_=g.model(include_springs=False)
    # A genuine BREP projection of only the clutch rig (pins omitted for an
    # unobscured mechanism view); the complete STEP contains all envelopes.
    shown=[s for n,(s,k) in parts.items() if k not in ("pin_envelope","screw_envelope")
           and "pin_guide" not in n and "post" not in n]
    shown=[s.intersect(g.box(-20,20,-20,20,-7,13)) for s in shown]
    compound=cq.Compound.makeCompound(shown)
    svg=cq.exporters.getSVG(compound,opts={"width":900,"height":650,
        "projectionDir":(1,-1,.9),"showHidden":False,"showAxes":False,
        "strokeWidth":.045,"marginLeft":30,"marginTop":30})
    (OUT/"assembly-brep-projection.svg").write_text(svg)
    print("Wrote 5 drawings in drawings/ (2 PNG + 3 SVG).")

if __name__=="__main__":drawings()
