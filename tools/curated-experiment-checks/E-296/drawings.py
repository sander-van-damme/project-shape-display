#!/usr/bin/env python3
"""E-296 concept sections and packing; dimensions mm, not shop drawings.

Real BREP views are produced separately by cad_drawings.py. These drawings
explain the chosen logic and the two dimensioned alternatives.
"""
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon

OUT=Path(__file__).resolve().parent/'figures'
BLUE,RED,GOLD,GREY,GREEN='#2877a8','#b84946','#d79a32','#61707a','#368374'

def rect(ax,x,z,w,h,color,**kw):
    ax.add_patch(Rectangle((x,z),w,h,facecolor=color,edgecolor='white',linewidth=.5,**kw))

def ring(ax,inner,outer,z,t,color):
    rect(ax,-outer/2,z,(outer-inner)/2,t,color)
    rect(ax,inner/2,z,(outer-inner)/2,t,color)

def dim(ax,a,b,label,horizontal=False):
    ax.annotate('',b,a,arrowprops=dict(arrowstyle='<->',lw=.8,color='#303a43'))
    x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
    ax.text(x+(.1 if not horizontal else 0),y+(.09 if horizontal else 0),label,
            fontsize=8,ha='left' if not horizontal else 'center',va='center',
            rotation=0 if horizontal else 90,
            bbox=dict(facecolor='white',edgecolor='none',pad=.5))

def save(fig,name):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT/(name+'.svg'));fig.savefig(OUT/(name+'.png'),dpi=180)
    plt.close(fig)

def sleeve(ax,q):
    b=1.95/math.sqrt(3)
    ring(ax,2*b,3,-.6+q,4.3,GOLD)
    ring(ax,2*b,4.2,3.7+q,.4,GOLD)
    for sign in [-1,1]:
        ax.add_patch(Polygon([(sign*b,3.725+q),(sign*b,4.1+q),
                            (sign*2.7/math.sqrt(3),4.1+q)],facecolor='white',edgecolor='none'))
    ring(ax,2*b,3.4,-.6+q,.4,GOLD)

def truth():
    fig,axes=plt.subplots(1,4,figsize=(13,6),sharey=True)
    states=[(0,0,0,'00 — beide uit'),(1.4,0,0,'10 — alleen rij'),
            (0,1.4,.2,'01 — alleen kolom'),(1.4,1.4,1.4,'11 — gekoppeld')]
    for ax,(r,c,q,title) in zip(axes,states):
        ax.axvline(0,color='#acb5bc',ls='-.',lw=.6)
        rect(ax,-1.8/math.sqrt(3),-1.1,3.6/math.sqrt(3),4.4,GREY)
        rect(ax,-1.8/math.sqrt(3),4.7,3.6/math.sqrt(3),2.1,GREY)
        sleeve(ax,q);ring(ax,3.2,4.7,r,.3,BLUE);ring(ax,2.4,4.7,4.1+c,.4,RED)
        for sign in [-1,1]:
            ys=[r+.3+(3.4+q-r)*i/10 for i in range(11)]
            xs=[sign*(1.85+(.07 if i%2 else -.07)) for i in range(11)]
            ax.plot(xs,ys,color='#68727b',lw=1.2)
        gap=4.7-(4.1+q)
        if gap>0:dim(ax,(2.55,4.1+q),(2.55,4.7),f'vrij {gap:.2f}')
        else:dim(ax,(2.55,4.7),(2.55,4.1+q),'overlap 0,80')
        ax.text(0,-1.28,f'q = {q:.2f} mm\nveer L = {3.4+q-r:.2f} mm',ha='center',va='top',fontsize=9)
        ax.set_title(title,fontsize=11,pad=12);ax.set_xlim(-2.85,3.05);ax.set_ylim(-2,7)
        ax.set_aspect('equal');ax.axis('off')
    fig.suptitle('E-296 • één schuifhuls, rijveer en kolomplafond',fontsize=16,y=.98)
    fig.text(.5,.075,'Grijs: axiaal vaste input / output   •   geel: roterende schuifhuls   •   blauw: rijring   •   rood: kolomplafond',ha='center',fontsize=10)
    fig.text(.5,.035,'Principe-doorsneden in mm; veer schematisch. Kolom AAN heft het plafond op. Lagering en geleiding: zie STEP/CAD.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.015,right=.99,bottom=.12,top=.89,wspace=.12)
    save(fig,'01-four-states')

def packing():
    fig,axes=plt.subplots(1,3,figsize=(14,5.1));p=5.08
    for n,ax in enumerate(axes[:2]):
        for a in [-p/2,p/2,1.5*p]:
            ax.axvline(a,color='#d2d8dc',lw=.7);ax.axhline(a,color='#d2d8dc',lw=.7)
        for x in [0,p]:
            for y in [0,p]:
                ax.add_patch(Rectangle((x-2.2,y-2.2),4.4,4.4,fill=False,edgecolor=GREEN,lw=1,ls='--'))
                ax.add_patch(Circle((x,y),2.35,facecolor=BLUE if n==0 else RED,alpha=.28,edgecolor='none'))
                ax.add_patch(Circle((x,y),1.6 if n==0 else 1.2,facecolor='white',edgecolor='none'))
                ax.add_patch(Circle((x,y),1.5,fill=False,edgecolor=GOLD,lw=.8))
        if n==0:
            for y in [0,p]:rect(ax,2.35,y-.4,p-4.7,.8,BLUE)
        else:
            for x in [0,p]:rect(ax,x-.4,2.35,.8,p-4.7,RED)
        dim(ax,(0,8.15),(p,8.15),'5,08 pitch',True)
        dim(ax,(2.35,-2.85),(p-2.35,-2.85),'0,38',True)
        ax.set_xlim(-3.5,8.7);ax.set_ylim(-3.5,8.8);ax.set_aspect('equal');ax.axis('off')
        ax.set_title('Rijringen: z = 0 … 1,70' if n==0 else 'Kolomringen: z = 4,10 … 5,90',fontsize=11)
    ax=axes[2]
    rect(ax,-1,0,2,1.7,BLUE,alpha=.3);rect(ax,-1,4.1,2,1.8,RED,alpha=.3)
    rect(ax,-.5,-.6,1,6.1,GOLD,alpha=.4)
    rect(ax,-1.2,7.5,2.4,4,GREY,alpha=.25)
    ax.text(0,9.5,'Outputlagering\nzie CAD',ha='center',va='center',fontsize=9)
    dim(ax,(1.6,1.7),(1.6,4.1),'2,40 z-vrijloop')
    ax.text(0,-1.5,'Kammen kruisen in XY;\nhun volledige Z-sweeps\nblijven gescheiden.',ha='center',va='top',fontsize=10)
    ax.set_xlim(-2.8,3.2);ax.set_ylim(-3.4,12.1);ax.set_aspect('equal');ax.axis('off')
    ax.set_title('Gecombineerde slag-envelop',fontsize=11)
    fig.suptitle('E-296 • volledige actieve 2×2-envelop: 9,78 × 9,78 mm',fontsize=15,y=.98)
    fig.text(.5,.025,'Groen gestippeld: 4,40-mm pinnen op ander hoogteniveau. Buitenste kamgeleiders en bevestigingen vallen buiten deze actieve envelop.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.06,1,.92));save(fig,'02-packing')

def alternatives():
    fig,axes=plt.subplots(1,3,figsize=(13,7));ax=axes[0]
    ring(ax,1.95,3.5,3,4,GOLD)
    rect(ax,-.9,0,1.8,2.5,GREY);rect(ax,-.9,7.5,1.8,3,GREY)
    for x,col,start,end in [(-2,BLUE,1.5,3.5),(2,RED,9,6.5)]:
        ax.annotate('',(x,end),(x,start),arrowprops=dict(arrowstyle='->',color=col,lw=2))
    ax.text(0,12.8,'A • letterlijke tegenkracht',ha='center',fontsize=11)
    ax.text(0,11.5,'AFGEWEZEN',ha='center',color=RED,fontsize=11,weight='bold')
    ax.text(0,-1,'Eén starre vrijheidsgraad.\nGeen positieve permissie;\nrisico op klemmen of\nkrachtafhankelijke stand.',ha='center',va='top',fontsize=10)
    ax=axes[1]
    for z,h in [(-2,5.3),(4.7,3),(9.1,3),(13.5,5.3)]:rect(ax,-.9,z,1.8,h,GREY)
    rect(ax,-1,7.7,2,1.4,GREY);ring(ax,2.02,4.5,7.9,1,'#aeb8bf')
    for z in [.8,11.3]:ring(ax,1.95,3.4,z,4.7,GOLD)
    ring(ax,3.4,4.7,2.2,.35,BLUE);ring(ax,3.4,4.7,14.5,.35,RED)
    for x,col,start,end in [(-2,BLUE,2.4,3.8),(2,RED,14.2,12.8)]:
        ax.annotate('',(x,end),(x,start),arrowprops=dict(arrowstyle='->',color=col,lw=1.6))
    ax.text(0,21,'C • twee koppelingen in serie',ha='center',fontsize=11)
    ax.text(0,19.8,'Input → rij → tussenrotor → kolom → output',ha='center',fontsize=8)
    ax.text(0,-3,'Beide hulzen gekoppeld getekend.\nAparte tussenlagering. Veercassettes\nspiegelen de enkelhuls; niet in\ndeze vereenvoudigde sectie getoond.',ha='center',va='top',fontsize=9)
    ax.set_ylim(-7,23)
    ax=axes[2]
    rect(ax,-.9,-.8,1.8,4.1,GREY);ring(ax,1.95,3,.8,4.3,GOLD)
    ring(ax,1.95,4.2,5.1,.4,GOLD)
    for x in [-1.7,1.2]:
        rect(ax,x,5.5,.5,.8,GOLD);rect(ax,x,5.65,.5,1.05,GREY,alpha=.24)
    rect(ax,-1.7,6.5,3.4,.4,GREY);rect(ax,-.9,6.9,1.8,3,GREY)
    ring(ax,3.6,4.7,5.5,.4,RED)
    ax.text(0,12.8,'B2 • dezelfde EN, drie frontklauwen',ha='center',fontsize=11)
    ax.text(0,11.5,'Ring-ID 3,60; dog-OD 3,40',ha='center',fontsize=9)
    ax.text(0,-1,'Ringvormige klauwen op r = 1,2…1,7.\n3×35° tand, 3×50° venster;\n0,65 overlap in gekozen eindstand.\nMeer fasezoekhoek; grovere flanken.',ha='center',va='top',fontsize=9)
    for i,ax in enumerate(axes):
        ax.axvline(0,color='#aeb8bf',lw=.6,ls='-.');ax.set_xlim(-4,4)
        ax.set_aspect('equal');ax.axis('off')
        if i!=1:ax.set_ylim(-5,14)
    fig.suptitle('E-296 • mechanisch verschillende koppelroutes',fontsize=15,y=.98)
    fig.text(.5,.025,'Principetekeningen in mm. C en B2 zijn gedimensioneerde alternatieven; alleen B1 (hexhuls + MIN-gate) heeft volledige 2×2-STEP en BREP-controle.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.07,1,.93));save(fig,'03-alternatives')

def inverter():
    fig,ax=plt.subplots(figsize=(9,4.2))
    angle=math.asin(1.4/8)
    ax.plot([-8,8],[0,0],color='#b0b6bb',ls='--',lw=5,label='uit')
    a=8*math.cos(angle)
    ax.plot([-a,a],[-1.4,1.4],color=RED,lw=5,label='aan')
    ax.add_patch(Circle((0,0),.5,fc=GREY,ec='white'))
    ax.add_patch(Polygon([(-1,-2),(1,-2),(0,-.55)],fc=GREY))
    for x,z,color in [(-8,-1.4,BLUE),(8,1.4,RED)]:
        rect(ax,x-.45,z-.25,.9,.5,color)
        ax.plot([x,x],[-2.5,2.5],color=color,lw=.9,ls=':')
    ax.annotate('neergaand commando 1,40',(-8,-1.4),(-10,2.9),
                arrowprops=dict(arrowstyle='->',color=BLUE),fontsize=10)
    ax.annotate('kolomdak omhoog 1,40',(8,1.4),(2,3),
                arrowprops=dict(arrowstyle='->',color=RED),fontsize=10)
    dim(ax,(-8,-2.9),(0,-2.9),'arm 8,00',True)
    dim(ax,(0,-2.9),(8,-2.9),'arm 8,00',True)
    ax.text(0,-4,'Eén wip per kolom buiten het pinveld. Draaihoek 10,08°.\n'
            'Pen in horizontale sleuf vangt 0,124 mm zijwaartse baan op;\n'
            'reserveer ≥0,40 mm extra sleufslag. Beide daken blijven verticaal geleid.',
            ha='center',va='top',fontsize=10)
    ax.set_aspect('equal');ax.set_xlim(-12,12);ax.set_ylim(-6.5,5);ax.axis('off')
    ax.set_title('E-296 • externe bewegingsomkering, 1 : 1',fontsize=14)
    fig.tight_layout();save(fig,'04-inverter')

if __name__=='__main__':
    truth();packing();alternatives();inverter()
