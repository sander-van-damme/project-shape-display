#!/usr/bin/env python3
"""Regenerate E-297 assembly/section/plate figures from the delivered STL meshes.

Dependencies: numpy, trimesh, matplotlib, shapely, cadquery, manifold3d.
Run from any directory: python tools/curated-experiment-checks/E-297/drawings.py
Never invokes the CAD generator or changes printable meshes/projects.
"""
from pathlib import Path
import importlib.util, json, hashlib, os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/e297-matplotlib')
import numpy as np
import trimesh as tm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import PathPatch, Patch
from matplotlib.path import Path as MPath
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import Polygon
from shapely.geometry.polygon import orient

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
DEST=HERE/'drawings'; DEST.mkdir(exist_ok=True)
SPEC=importlib.util.spec_from_file_location('e297_cad',HERE/'cad/generate.py')
cad=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(cad)
for name in ['rotor','row-selector','single-comb','input-shaft','screw','pin','frame-left','frame-center','frame-right','stop-spacer']:
    cad.MESHES[name]=tm.load(HERE/'cad/parts'/f'{name}.stl',force='mesh')
P=json.loads((HERE/'cad/parameters.json').read_text())
COL={'row':'#159b99','lower':'#197e8c','column':'#eea03c','upper':'#d57922','input':'#4a6191','screw':'#746ea6','pin':'#ccd5df','frame':'#bec7cf','hand':'#4a6191','stop':'#8e969f'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':12,'svg.fonttype':'none','figure.facecolor':'white'})

def color(name):
    return next((v for k,v in COL.items() if name.startswith(k)), '#9ca6af')

def add3(ax,m,c,alpha=1):
    # Keep exact triangles; the read-only z-buffer renderer below handles occlusion.
    if not hasattr(ax,'_actual_meshes'):ax._actual_meshes=[]
    ax._actual_meshes.append((m,c))

def render_surfaces(items,elev,azim,height=1100):
    """Orthographic depth-buffer rasterization of the supplied actual mesh triangles."""
    from matplotlib.colors import to_rgb
    e=np.radians(elev);a=np.radians(azim)
    view=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    right=np.array([-np.sin(a),np.cos(a),0.])
    up=np.cross(view,right)
    basis=np.array([right,up,view]).T
    triangles=[];colors=[]
    light=np.array([-.4,-.7,1]);light/=np.linalg.norm(light)
    for m,c in items:
        keep=m.face_normals@view>1e-9
        triangles.append(m.triangles[keep]@basis)
        shade=.6+.4*np.maximum(0,m.face_normals[keep]@light)
        colors.append(np.array(to_rgb(c))[None,:]*shade[:,None])
    tri=np.concatenate(triangles);rgb=np.concatenate(colors)
    lo=tri[:,:,:2].reshape(-1,2).min(0);hi=tri[:,:,:2].reshape(-1,2).max(0)
    pad=(hi-lo)*.025;lo-=pad;hi+=pad;span=hi-lo
    width=max(150,int(height*span[0]/span[1]))
    pix=(tri[:,:,:2]-lo)/span*np.array([width-1,height-1])
    depth=np.full((height,width),-np.inf)
    canvas=np.ones((height,width,4));canvas[:,:,3]=0
    for t,xy,col in zip(tri,pix,rgb):
        xmin=max(0,int(np.floor(xy[:,0].min())));xmax=min(width-1,int(np.ceil(xy[:,0].max())))
        ymin=max(0,int(np.floor(xy[:,1].min())));ymax=min(height-1,int(np.ceil(xy[:,1].max())))
        if xmin>xmax or ymin>ymax:continue
        x,y=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
        x0,y0=xy[0];x1,y1=xy[1];x2,y2=xy[2]
        denominator=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
        if abs(denominator)<1e-9:continue
        w0=((y1-y2)*(x-x2)+(x2-x1)*(y-y2))/denominator
        w1=((y2-y0)*(x-x2)+(x0-x2)*(y-y2))/denominator
        w2=1-w0-w1
        z=w0*t[0,2]+w1*t[1,2]+w2*t[2,2]
        block=depth[ymin:ymax+1,xmin:xmax+1]
        mask=(w0>=-1e-7)&(w1>=-1e-7)&(w2>=-1e-7)&(z>block)
        block[mask]=z[mask]
        target=canvas[ymin:ymax+1,xmin:xmax+1]
        target[mask,:3]=col;target[mask,3]=1
    return canvas[::-1]

def setup3(ax,lim,elev=20,azim=-62):
    for setter,b in zip([ax.set_xlim,ax.set_ylim,ax.set_zlim],lim):setter(*b)
    ax.set_box_aspect([b[1]-b[0] for b in lim]); ax.view_init(elev,azim)
    ax.set_proj_type('ortho'); ax.set_axis_off()

def save(fig,name):
    for ax in list(fig.axes):
        if hasattr(ax,'_actual_meshes'):
            picture=render_surfaces(ax._actual_meshes,ax.elev,ax.azim)
            overlay=fig.add_axes(ax.get_position(),frameon=False)
            overlay.imshow(picture,interpolation='bilinear');overlay.axis('off')
        fig.savefig(DEST/(name+'.png'),dpi=185,bbox_inches='tight',facecolor='white')
    fig.savefig(DEST/(name+'.svg'),bbox_inches='tight',facecolor='white')
    plt.close(fig)
    print(name,flush=True)

def section(ax,m,normal,origin,axes=(0,2),c='#999',alpha=1,lw=.7):
    path=m.section(plane_normal=normal,plane_origin=origin)
    if path is None:return
    geom=None
    for curve in [entity.discrete(path.vertices) for entity in path.entities]:
        xy=curve[:,axes]
        if len(xy)<4:continue
        poly=Polygon(xy)
        if not poly.is_valid:poly=poly.buffer(0)
        geom=poly if geom is None else geom.symmetric_difference(poly)
    if geom is None or geom.is_empty:return
    polys=list(geom.geoms) if geom.geom_type=='MultiPolygon' else [geom]
    paths=[]
    for poly in polys:
        if poly.geom_type!='Polygon':continue
        poly=orient(poly,sign=1)
        for ring in [poly.exterior,*poly.interiors]:
            xy=np.asarray(ring.coords); codes=np.full(len(xy),MPath.LINETO,dtype=np.uint8)
            codes[0]=MPath.MOVETO;codes[-1]=MPath.CLOSEPOLY
            paths.append(MPath(xy,codes))
    if paths:ax.add_patch(PathPatch(MPath.make_compound_path(*paths),facecolor=c,edgecolor='#344454',alpha=alpha,lw=lw))

def dimension(ax,p1,p2,label,offset=(0,0)):
    p1=np.asarray(p1);p2=np.asarray(p2)
    ax.annotate('',p2,p1,arrowprops={'arrowstyle':'<->','lw':.9,'color':'#334155'})
    mid=(p1+p2)/2+np.asarray(offset)
    ax.text(*mid,label,ha='center',va='center',fontsize=9,bbox={'facecolor':'white','edgecolor':'none','pad':1})

def assembly():
    parts=cad.assembly((1,0),(1,0))
    fig=plt.figure(figsize=(14,9.2))
    ax=fig.add_axes([.01,.12,.61,.79],projection='3d')
    setup3(ax,[(-30,30),(-15,35),(0,59)],19,-64)
    for name,m in parts.items():
        mm=m.copy()
        if name=='frame-left':mm.apply_translation([-15,0,0])
        if name=='frame-right':mm.apply_translation([15,0,0])
        if name=='frame-center':mm.apply_translation([0,20,0])
        add3(ax,mm,color(name))
    setup3(ax,[(-30,30),(-15,35),(0,59)],19,-64)
    ax.set_title('Montageoverzicht — drie framegedeelten uit elkaar',pad=7)
    ax2=fig.add_axes([.62,.31,.36,.60],projection='3d')
    setup3(ax2,[(-16,16),(-16,16),(0,59)],19,-60)
    for name,m in parts.items():
        if not name.startswith('frame'):add3(ax2,m,color(name))
    setup3(ax2,[(-16,16),(-16,16),(0,59)],19,-60)
    ax2.set_title('Hetzelfde binnenwerk, zonder frame',pad=7)
    fig.text(.65,.275,'Onderdeelkleuren',weight='bold',fontsize=11)
    texts=[('input','Vier axiaal ondersteunde inputassen.'),('lower','Onderste koppelingshelften en rijkammen.'),('upper','Bovenste koppelingshelften en kolomkammen.'),('screw','Schroeven met vormgesloten DD-staart.'),('pin','Vier geleide pinnen van 4,4 mm.'),('frame','Drie framegedeelten met vaste axiale steun.')]
    for i,(k,t) in enumerate(texts):fig.text(.65,.242-i*.029,t,color=COL[k] if k not in ['pin','frame'] else '#526170',fontsize=9)
    fig.suptitle('E-297  ·  tweedelige rij-/kolomkoppeling op 5,08 mm pitch',fontsize=16,weight='bold',y=.98)
    fig.text(.025,.025,'Werkelijke STL-oppervlakken. Frame-uitwaaiering is uitsluitend voor zichtbaarheid; het binnenwerk staat op zijn echte CAD-posities.\nRij 1 en kolom 1 geselecteerd. Montage begint bij het middenframe; volg test.md voor de exacte zijwaartse montagevolgorde.',fontsize=9,color='#475569')
    save(fig,'assembly-exploded')

def four_states():
    fig=plt.figure(figsize=(14,8.6))
    x0=y0=-P['pitch']/2
    bh=float(cad.MESHES['rotor'].bounds[1,2])
    for k,(r,c,label) in enumerate([(0,0,'Geen selectie'),(1,0,'Alleen rij'),(0,1,'Alleen kolom'),(1,1,'Rij én kolom')]):
        ax=fig.add_axes([.015+k*.246,.15,.24,.73],projection='3d')
        zlo=P['lower_base']-1.6; zhi=P['upper_base']+2.0
        setup3(ax,[(-3,3),(-3,3),(zlo,zhi)],13,-61)
        parts=cad.assembly((r,0),(c,0))
        for name in ['input-0','lower-0','upper-0','screw-0','row-0','column-0']:
            m=parts[name].copy()
            # Actual cutaway of the full selector/screw: hides only geometry outside this cell/window.
            for normal,origin in [([1,0,0],[x0-2.3,0,0]),([-1,0,0],[x0+2.3,0,0]),([0,1,0],[0,y0-2.3,0]),([0,-1,0],[0,y0+2.3,0]),([0,0,1],[0,0,zlo]),([0,0,-1],[0,0,zhi])]:
                m=m.slice_plane(origin,normal)
            m.apply_translation([-x0,-y0,0]); add3(ax,m,color(name))
        setup3(ax,[(-3,3),(-3,3),(zlo,zhi)],13,-61)
        ax.set_title(f'{label}\nR{r} C{c}',fontsize=12,pad=8)
        lower=P['lower_base']+P['stroke']*r+bh
        upper=P['upper_base']-P['stroke']*c-bh
        gap=upper-lower
        caption=(f'{gap:.2f} mm vrije tipgap' if gap>=0 else f'{-gap:.2f} mm axiale overlap').replace('.',',')
        fig.text(.137+k*.246,.11,caption,ha='center',fontsize=11,weight='bold',color='#b64237' if gap<0 else '#334155')
    fig.suptitle('Vier toestanden van één werkelijke koppeling',fontsize=16,weight='bold',y=.97)
    fig.legend(handles=[Patch(color=COL['row'],label='rij: onderste meenemer'),Patch(color=COL['lower'],label='onderste rotor'),Patch(color=COL['column'],label='kolom: bovenste meenemer'),Patch(color=COL['upper'],label='bovenste rotor')],loc='lower center',bbox_to_anchor=(.5,.055),ncol=4,frameon=False,fontsize=9)
    fig.text(.025,.017,'Nominale CAD op het midden van de 0,24-mm axiale vangspeling. Slag per selector 2,40 mm. Twee brede klauwen per helft, 2,40 mm hoog.\nDe volledige bladverbindingen en aslengten zijn hier afgeknipt om het koppelvlak te tonen; fasezoeken en fysieke passing zijn nog te testen.',fontsize=9,color='#475569')
    save(fig,'four-states')

def collar_pitch():
    fig,axs=plt.subplots(1,2,figsize=(13,6.8),gridspec_kw={'width_ratios':[1,1.1]})
    ax=axs[0]
    # True y=-0.30 section, no invented rectangle substitutes.
    section(ax,cad.MESHES['single-comb'],[0,1,0],[0,-.3,0],c=COL['row'])
    section(ax,cad.MESHES['rotor'],[0,1,0],[0,-.3,0],c=COL['lower'])
    shaft=cad.MESHES['input-shaft'].copy();shaft.apply_translation([0,0,-5.8])
    section(ax,shaft,[0,1,0],[0,-.3,0],c=COL['input'])
    ax.set_xlim(-3.1,3.1);ax.set_ylim(-1.8,3.1);ax.set_aspect('equal')
    ax.set_title('Echte doorsnede door de flensvangst\n(0,30 mm naast de rotoras)')
    ax.set_xlabel('x (mm)');ax.set_ylabel('z vanaf rotorflens (mm)')
    dimension(ax,(-2.65,0),(-2.65,.72),'0,72',(-.10,0))
    dimension(ax,(2.65,-.12),(2.65,.84),'0,96',(.07,0))
    ax.text(0,-1.52,'0,24 mm totale axiale vrije slag',ha='center',fontsize=10,weight='bold')
    ax.annotate('Vlak flensvlak:\nactief duwen én trekken',xy=(1.9,.72),xytext=(.2,2.4),fontsize=9,arrowprops={'arrowstyle':'->','color':'#334155'})
    ax.grid(alpha=.15)
    ax=axs[1]
    parts=cad.assembly()
    for i in range(2):
        section(ax,parts[f'row-{i}'],[0,0,1],[0,0,P['lower_base']-.5],axes=(0,1),c=COL['row'],alpha=.75)
        section(ax,parts[f'column-{i}'],[0,0,1],[0,0,P['upper_base']+.5],axes=(0,1),c=COL['column'],alpha=.55)
    for i in range(4):
        section(ax,parts[f'lower-{i}'],[0,0,1],[0,0,P['lower_base']+.36],axes=(0,1),c=COL['lower'],alpha=.75)
    for x in [-P['pitch']/2,P['pitch']/2]:
        for y in [-P['pitch']/2,P['pitch']/2]:
            ax.plot([x-.01,x+.01],[y,y],'+',ms=7,color='white')
    dimension(ax,(-2.54,5.5),(2.54,5.5),'5,08 mm',(0,.25))
    dimension(ax,(5.5,-2.54),(5.5,2.54),'5,08 mm',(.42,0))
    ax.set_xlim(-5.5,6.2);ax.set_ylim(-5.6,6.2);ax.set_aspect('equal');ax.grid(alpha=.15)
    ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)')
    ax.set_title('Bovenaanzicht 2×2: twee selectorhoogten\nprojecties van werkelijke doorsneden')
    fig.suptitle('Meenemer, vrije rotatie en werkelijke rasterruimte',fontsize=16,weight='bold',y=.99)
    fig.subplots_adjust(top=.83,bottom=.20,wspace=.25)
    fig.text(.04,.08,'De twee U-bladen vormen samen één stijve selector. Alleen de rotor draait; de selector schuift axiaal.\nZijmontage door de open U-mond vóór het sluiten van de framegeleiding. Bladverbindingen en handgrepen liggen buiten deze uitsnede.',fontsize=10)
    fig.text(.04,.025,'Flens Ø4,30 mm · hals Ø3,20 mm · vork buitenbreedte 4,60 mm · nominale buurvrijloop 0,48 mm.\nDe over elkaar getekende groene en oranje staven liggen op verschillende z-niveaus en zijn geen doorsnijding op één hoogte.',fontsize=9,color='#475569')
    save(fig,'collar-and-pitch')

def plate_map(test,short):
    folder=ROOT/'owner-print-tests'/test
    layout=json.loads((folder/'layout.json').read_text())
    fig=plt.figure(figsize=(14,8.4));ax=fig.add_axes([.045,.18,.66,.70]);txt=fig.add_axes([.735,.13,.25,.75]);txt.axis('off')
    for idx,item in enumerate(layout,1):
        m=tm.load(ROOT/item['source'],force='mesh')
        bounds=np.array(item['bounds_mm']);m.apply_translation(bounds[0]-m.bounds[0])
        name=item['name'];c='#4a6191' if 'tight' in name else '#edaa4d' if 'loose' in name else '#159b99' if 'nominal' in name else color(name)
        coll=PolyCollection(m.triangles[:,:,:2],facecolors=c,edgecolors='none',rasterized=True)
        ax.add_collection(coll)
        mid=bounds[:,:2].mean(axis=0)
        ax.text(*mid,str(idx),ha='center',va='center',fontsize=8,weight='bold',bbox={'facecolor':'white','edgecolor':'#64748b','lw':.35,'boxstyle':'round,pad=.18'})
    maxxy=np.array([it['bounds_mm'][1][:2] for it in layout]).max(axis=0)
    ax.set_xlim(0,maxxy[0]+5);ax.set_ylim(0,maxxy[1]+5);ax.set_aspect('equal');ax.set_xlabel('plaat x (mm)');ax.set_ylabel('plaat y (mm)');ax.grid(alpha=.15)
    fig.suptitle(f'Test {short} — kaart van de daadwerkelijke printplaat',fontsize=16,weight='bold',y=.97)
    names={'rotor-tight':'rotor, krap','rotor-nominal':'rotor, nominaal','rotor-loose':'rotor, ruim','comb-tight':'meenemer, krap','comb-nominal':'meenemer, nominaal','comb-loose':'meenemer, ruim','coupon-shaft':'handas','frame-left':'linker framedeel','frame-center':'middelste framedeel','frame-right':'rechter framedeel','row-selector':'rij-/kolomselector','rotor':'koppelingshelft','input-shaft':'onderste inputas','screw':'schroef met DD-staart','pin':'holle 4,4-mm pin','hand-key':'gedeelde handkop','stop-spacer':'selector-vulblokje'}
    txt.text(0,1,'Onderdeelnummer → herkenning',weight='bold',fontsize=11,va='top')
    if short=='A':
        groups=[(1,5,'Krap',.12,.18),(6,10,'Nominaal 1',.15,.24),(11,15,'Nominaal 2',.15,.24),(16,20,'Ruim',.20,.30)]
        for n,(lo,hi,label,relief,play) in enumerate(groups):
            y=.9-n*.21
            txt.text(0,y,f'{lo}–{hi}  {label}',weight='bold',fontsize=11)
            txt.text(0,y-.04,f'{lo}, {lo+1}: twee rotoren\n{lo+2}: één meenemer\n{lo+3}, {lo+4}: twee handassen',fontsize=10,va='top',linespacing=1.5)
            txt.text(0,y-.145,f'relief {relief:.2f} / axiaal spel {play:.2f} mm'.replace('.',','),fontsize=8,color='#475569')
    else:
        groups=[]
        for i,it in enumerate(layout,1):
            if groups and groups[-1][2]==it['name']:groups[-1][1]=i
            else:groups.append([i,i,it['name']])
        for n,(lo,hi,name) in enumerate(groups):
            txt.text(0,.9-n*.073,f'{lo}' + (f'–{hi}' if hi!=lo else '') + ': '+names.get(name,name),fontsize=10)
    fig.text(.045,.065,'Bovenaanzicht op de geleverde oriëntatie. Nummers staan alleen op deze kaart, niet als reliëf op de kleine delen.\nBewaar de volgorde bij het afnemen; neem liefst eerst een foto van de hele plaat. Geen automatisch heroriënteren.',fontsize=10)
    fig.text(.045,.02,'Bron: exacte onderdelen en bounds_mm uit layout.json; de figuur verplaatst of schaalt geen onderdeel.',fontsize=9,color='#475569')
    save(fig,'plate-'+short.lower())

if __name__=='__main__':
    assembly();four_states();collar_pitch()
    plate_map('2026-10-16-two-half-clutch-fit','A')
    plate_map('2026-10-16-two-half-clutch-matrix','B')
    files=[Path(__file__).resolve(),HERE/'cad/generate.py',HERE/'cad/parameters.json',ROOT/'owner-print-tests/2026-10-16-two-half-clutch-fit/layout.json',ROOT/'owner-print-tests/2026-10-16-two-half-clutch-matrix/layout.json',*sorted((HERE/'cad/parts').glob('*.stl'))]
    manifest={'method':'Read-only actual STL surfaces, actual section curves and assembly() transforms. No CAD regeneration.', 'parameters':P,'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (DEST/'source-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
