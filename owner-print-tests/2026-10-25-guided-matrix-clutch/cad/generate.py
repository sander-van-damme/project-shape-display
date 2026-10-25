#!/usr/bin/env python3
"""E-304: millimetres. Explicit parametric solids, exact retained E-295 thread meshes.
Run from any directory. Python cadquery/trimesh/manifold3d/shapely/numpy required.
No physical qualification is implied by exported geometry.
"""
from pathlib import Path
import sys,json,math,hashlib
import numpy as np
import cadquery as cq
import trimesh as tm
import manifold3d as md
from shapely.geometry import LineString, Polygon
HERE=Path(__file__).resolve().parent; PACK=HERE.parent; ROOT=PACK.parents[1]
ANA=ROOT/'tools/curated-experiment-checks/E-304/analysis';sys.path.insert(0,str(ANA))
from flexure import solve
OUT=PACK/'components'; OUT.mkdir(exist_ok=True)
ENG=ROOT/'tools/curated-experiment-checks/E-304/cad';ENG.mkdir(exist_ok=True)
P=5.08; S=P/2; RISE=1.4; Q=.6; M=.3; N=12; RP=M*N/2; PA=math.radians(25)
PART={}; PRINT={}; SOL={}
def box(x,y,z,dx,dy,dz):return cq.Solid.makeBox(dx,dy,dz,cq.Vector(x,y,z))
def cyl(r,h,z=0):return cq.Solid.makeCylinder(r,h,cq.Vector(0,0,z))
def cone(r1,r2,h,z=0):return cq.Solid.makeCone(r1,r2,h,cq.Vector(0,0,z))
def sphere(r,x=0,y=0,z=0):return cq.Solid.makeSphere(r,cq.Vector(x,y,z),cq.Vector(0,0,1),-90,90)
def union(sh):
 s=sh[0]
 for t in sh[1:]:s=s.fuse(t)
 return s.clean()
def mesh(s):
 v,f=s.tessellate(.015,.10);m=tm.Trimesh(np.array([p.toTuple() for p in v]),np.array(f),process=True)
 m.merge_vertices(digits_vertex=5);m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices();return m
def mani(m):return md.Manifold(md.Mesh(np.asarray(m.vertices,dtype=np.float32),np.asarray(m.faces,dtype=np.uint32)))
def merge(mm):
 s=mani(mm[0])
 for m in mm[1:]:s=s+mani(m)
 a=s.to_mesh();return tm.Trimesh(a.vert_properties[:,:3],a.tri_verts,process=True)
def move(m,x=0,y=0,z=0,rz=0):
 n=m.copy();n.apply_transform(tm.transformations.rotation_matrix(math.radians(rz),[0,0,1]));n.apply_translation([x,y,z]);return n
def orient(m,axis,deg):
 n=m.copy();n.apply_transform(tm.transformations.rotation_matrix(math.radians(deg),axis));return n
def xz(poly,y,width):
 def wire(coords):return cq.Wire.makePolygon([cq.Vector(x,y,z) for x,z in coords])
 return cq.Solid.extrudeLinear(wire(poly.exterior.coords),[wire(p.coords) for p in poly.interiors],cq.Vector(0,width,0))
def xy(poly,z,h):
 w=cq.Wire.makePolygon([cq.Vector(x,y,z) for x,y in list(poly)+[poly[0]]]);return cq.Solid.extrudeLinear(w,[],cq.Vector(0,0,h))
def export(name,s,rotation=None):
 m=s if isinstance(s,tm.Trimesh) else mesh(s)
 assert m.is_watertight,(name,'open mesh')
 PART[name]=m
 if not isinstance(s,tm.Trimesh):SOL[name]=s;cq.exporters.export(s,str(ENG/(name+'.step')))
 m.export(ENG/(name+'.stl'))
 p=orient(m,*rotation) if rotation else m.copy();p.apply_translation(-p.bounds[0]);PRINT[name]=p;p.export(OUT/(name+'.stl'))
 print(name,len(m.faces),flush=True)
def cam(x,rise=RISE):
 v=abs((x+P/2)%P-P/2)
 return rise*min(1,max(0,(v-.30)/(S-.60)))
def rowbar(length=32,holes=True):
 lo=-12;hi=lo+length
 b=box(lo,-2.3,0,length,4.6,10.4)
 # Box beam, 0.8-mm skins, two continuous 2-mm reinforcement channels.
 b=b.cut(box(lo-.1,-1.5,.8,length+.2,3,8.8))
 b=b.fuse(box(lo,-.4,3.3,length,.8,4.8))
 for z in [2.2,8.1]:
  tube=cq.Solid.makeCylinder(1.6,length,cq.Vector(lo,0,z),cq.Vector(1,0,0))
  b=b.fuse(tube)
  if holes:b=b.cut(cq.Solid.makeCylinder(1.1,length+.2,cq.Vector(lo-.1,0,z),cq.Vector(1,0,0)))
 xs=np.linspace(lo-.5,hi+.5,int(length/.04)+26);path=LineString([(float(x),12+cam(x)) for x in xs]).buffer(.57,cap_style=2,join_style=2)
 for y in [-2.3,1.3]:
  side=box(lo,y,10.35,length,1.,4.35).cut(xz(path,-1.90 if y<0 else 1.29,.61));b=b.fuse(side)
 # Large accessible handle, outside active raster.
 b=b.fuse(box(lo-6,-2.3,0,6.01,4.6,4))
 return b.clean()
def rowpieces():
 full=rowbar();lo=-12;hi=20;xx=np.linspace(lo-.2,hi+.2,900)
 above=Polygon([(lo-.2,16),(hi+.2,16)]+[(float(x),12+cam(x)) for x in xx[::-1]])
 cutter=xz(above,-2.5,5.)
 lower=full.cut(cutter).clean();cap=full.intersect(cutter)
 for x in [lo,hi-1.0]:cap=cap.fuse(box(x,-2.3,14.1,1.0,4.6,.6))
 lower=lower.cut(box(lo-.01,-2.5,10.4,.31,5,5)).clean()
 cap=cap.cut(box(hi-.3,-2.5,10.4,.31,5,6)).clean()
 return lower,cap
def colbar(length=32):
 lo=-12;hi=lo+length
 xs=np.linspace(lo,hi,int(length/.04)+1)
 # Model along X, rotate 90 degrees for columns; groove gap admits fixed follower stem.
 roof=Polygon([(lo,28.4),(hi,28.4)]+[(float(x),21.9+cam(x,1.0)) for x in xs[::-1]])
 b=union([xz(roof,-2.3,1.1),xz(roof,1.2,1.1),box(lo-5,-2.3,21.9,5.02,4.6,6.5)])
 return b.rotate((0,0,0),(0,0,1),90)
def follower(t=.40,delta=0,q=0):
 # Lower foot rises by q+delta; upper foot by q. Actual elastic mode, linear-frame approximation.
 model=solve(thick=t,b=3.6,L=3.2,p=.9)
 pts=np.asarray(model['points']);u=np.asarray(model['u_per_N']).reshape(-1,3)
 force=delta*model['k_N_mm'];pts=pts+u[:,:2]*force
 pts[:,1]+=15.2+q+delta
 poly=LineString(pts).buffer(t/2,cap_style=2,join_style=1)
 spring=xz(poly,-1.8,3.6)
 # Wide feet receive separate stationary square guides; spring does not locate the rotor.
 low=12+q+delta;up=21.4+q
 sh=[spring,box(-1.85,-1.2,low+.2,3.7,2.4,3.05),box(-1.85,-1.8,19.45+q,3.7,3.6,1.15),box(-.9,-1.8,20.5+q,1.8,2.7,9.0),box(-2.1,-1.8,21.0+q,4.2,1.8,.4)]
 sh += [cq.Solid.makeCylinder(.4,3.6,cq.Vector(0,-1.8,low),cq.Vector(0,1,0)),cq.Solid.makeCylinder(.4,4.2,cq.Vector(-2.1,0,up),cq.Vector(1,0,0))]
 # Contact is a central printed dome. Retaining lip has 0.3-mm running clearance.
 sh += [cyl(2.2,.6,29.0+q),sphere(.4,z=29.4+q)]
 cage=cyl(2.2,3.0,29.0+q).cut(cyl(1.80,1.85,29.55+q)).cut(cyl(1.40,3.2,29.0+q))
 cage=cage.cut(box(-2.3,-2.3,29.5+q,4.6,2.3,3.))
 sh.append(cage)
 return union(sh).cut(box(-3,-3,10,6,1.2,24)).clean()
def gear(z=34.3,h=2.4,teeth=N,module=M,backlash=.08):
 rp=module*teeth/2;rb=rp*math.cos(PA);ra=rp+module;rf=rp-1.25*module
 inv=math.tan(PA)-PA;half=math.pi/(2*teeth)-backlash/(2*rp)
 pp=[]
 for j in range(teeth):
  a=2*math.pi*j/teeth
  def psi(r):
   t=math.sqrt(max(0,(r/rb)**2-1));return half+inv-(t-math.atan(t))
  flank=np.linspace(max(rf,rb),ra,14)
  pp.append((rf*math.cos(a-psi(rb)),rf*math.sin(a-psi(rb))))
  for r in flank:pp.append((r*math.cos(a-psi(r)),r*math.sin(a-psi(r))))
  for ang in np.linspace(a-psi(ra),a+psi(ra),5)[1:]:pp.append((ra*math.cos(ang),ra*math.sin(ang)))
  for r in flank[::-1][1:]:pp.append((r*math.cos(a+psi(r)),r*math.sin(a+psi(r))))
  pp.append((rf*math.cos(a+psi(rb)),rf*math.sin(a+psi(rb))))
  end=2*math.pi*(j+1)/teeth-psi(rb)
  for ang in np.linspace(a+psi(rb),end,5)[1:-1]:pp.append((rf*math.cos(ang),rf*math.sin(ang)))
 gg=xy(pp,z,h)
 if teeth==12:gg=gg.intersect(cyl(ra,h-.60,z).fuse(cone(ra,rf,.60,z+h-.60)))
 return gg.clean()
def rotor(d=1.8):
 return union([sphere(.4,z=30.2),cyl(.4,.55,30.15),cyl(1.6,.6,30.5),cyl(d/2,9.9,31.0),cone(1.6,d/2,.7,31.1),gear(),cone(1.425,d/2,.6,36.69),cone(d/2,1.9,1.01,40.0),cone(1.9,1.1,.8/math.tan(math.pi/6),41.0)])
def outputbase():
 # Cup opens down; blind floor has axial clearance to male tip. Narrow neck and collar support screw.
 cup=cyl(2.3,2.2,41.4).cut(cone(2.01547,1.0,1.75885,41.4))
 return union([cup,cone(2.3,.8,1.5,43.59),cyl(.8,10.0,45.08),cyl(1.4,.8,52.6),cone(.8,1.6,.8,54.2)])
def rack_profile(lo=-19,hi=24,z=34.3,h=3.2,y=RP+.08):
 pitch=math.pi*M;tip=math.pi*M/2-.06-2*M*math.tan(PA);root=math.pi*M/2-.06+2*1.25*M*math.tan(PA)
 b=box(lo,y+1.25*M,z,hi-lo,.45,h)
 for k in range(math.floor(lo/pitch)-1,math.ceil(hi/pitch)+1):
  x=k*pitch
  b=b.fuse(xy([(x-root/2,y+1.25*M+.01),(x-tip/2,y-M),(x+tip/2,y-M),(x+root/2,y+1.25*M+.01)],z,h))
 return b.intersect(box(lo,y-M-.01,z-.01,hi-lo,1.0,h+.02)).clean()
def rack_shuttle():
 r=rack_profile();r2=r.translate((0,P,0))
 return union([r,r2,box(-21,1.8,34.3,2.1,P+1.1,3.2),box(-31,1.8,34.3,10.1,2,3.2)])
def drive():
 # A larger pinion at the side engages the same positive rack; one rotary input drives all four rotors.
 b=union([gear(34.3,3.2,teeth=36),cyl(1.4,5.3,29),cyl(2.0,.6,31),cyl(7,1.2,37.5)])
 for a in np.arange(36)*math.pi/18:b=b.cut(cyl(.22,1.5,37.4).translate((7*math.cos(a),7*math.sin(a),0)))
 return b.clean()
def keeper(upper=False):
 levels=[(38.,1.2,1.03),(46.,1.2,.94),(51.2,1.2,.94),(64.5,1.2,2.35),(75.8,1.2,2.35)] if upper else [(20.2,.9,1.95),(33.,1.2,1.03)]
 za=levels[0][0];zb=levels[-1][0]+levels[-1][1]
 sh=[box(x,-3.15,za,1.,.8,zb-za) for x in [-4.6,8.6]]
 for z,h,r in levels:sh.append(box(-4.6,-3.15,z,14.2,3.15-r,h))
 for x in [-6.1,9.59]:sh.append(box(x,-3.15,za,1.51,.8,levels[0][1]))
 return union(sh)
def frame():
 lo=-6;hi=11.08;w=hi-lo
 sh=[box(lo,lo,-1.2,w,w,1.2)]
 for x in [lo,hi-1.2]:sh.append(box(x,lo,0,1.2,w,78))
 levels=[(20.2,.9,'follower'),(33.,1.2,'input'),(38.,1.2,'input'),(46.,1.2,'output'),(51.2,1.2,'output'),(53.4,.7,'output'),(54.1,4.4,'thread'),(64.5,1.2,'pin'),(75.8,1.2,'pin')]
 for z,h,kind in levels:
  pl=box(lo,lo,z,w,w,h)
  for iy,y in enumerate([0,P]):
   rr={'foot':2.3,'follower':1.95,'input':1.03,'output':.94,'thread':1.9,'pin':2.35}[kind]
   # Opposite open sides for the two bench rows. Shared covers close each guide.
   if kind not in ['foot','thread'] and z!=53.4:
    yy=lo-.1 if iy==0 else y+rr
    hh= -rr-yy if iy==0 else hi+.1-yy
    pl=pl.cut(box(-4.8,yy,z-.1,14.6,hh,h+.2))
   for x in [0,P]:
    if kind=='pin':cut=box(x-2.35,y-2.35,z-.1,4.7,4.7,h+.2)
    elif kind=='foot':cut=box(x-2.05,y-2.3,z-.1,4.1,4.6,h+.2)
    elif kind=='follower':cut=box(x-2.2,y-1.95,z-.1,4.4,3.9,h+.2)
    else:cut=cyl(rr,h+.2,z-.1).translate((x,y,0))
    # Entry slot reaches bore centre; back semicircle remains in one continuous frame.
    width=4.1 if kind=='foot' else (4.4 if kind=='follower' else 2*rr)
    yy=lo-.1 if iy==0 else y
    hh=y-yy if iy==0 else hi+.1-y
    cut=cut.fuse(box(x-width/2,yy,z-.1,width,hh,h+.2))
    pl=pl.cut(cut)
  sh.append(pl)

 for x in [-5.2,9.1]:sh.append(box(x,lo,0,1.,w,9.8))
 for y in [-5.2,9.1]:sh.append(box(lo,y,28.55,w,1.2,2.6))
 b=union(sh)
 for y in [0,P]:b=b.cut(box(lo-.1,y-2.45,-.01,w+.2,4.9,18.11))
 for x in [0,P]:b=b.cut(box(x-2.45,lo-.1,21.7,4.9,w+.2,6.85))
 b=b.cut(box(-25,1.35,34.21,55,P+1.9,3.8))
 for y in [0,P]:
  for xa,xb in [(-3.3,-2.05),(2.05,3.03),(7.13,8.38)]:b=b.fuse(box(xa,y-1.1,11.2,xb-xa,2.2,9.6))
 wing=box(-21,-6.0,29.5,15.1,6.8,1.5).cut(cyl(1.55,1.7,29.4).translate((-13.5,-3.6,0)))
 b=b.fuse(wing).cut(cyl(7.25,8,31.65).translate((-13.5,-3.6,0)))
 for x in [-4.8,8.5]:
  b=b.cut(box(x,lo-.1,37.9,1.3,3.85,39.3))
  b=b.cut(box(x,P+2.25,37.9,1.3,hi-P-2.15,39.3))
 # Keeper tab sockets give a positive position stop; external tape retains the four shared covers.
 for z,h in [(20.2,.9),(38.,1.2)]:
  for x in [-6.2,9.5]:
   b=b.cut(box(x,lo-.1,z-.12,1.7,lo*-1-2.15,h+.24))
   b=b.cut(box(x,P+2.25,z-.12,1.7,hi-P-2.15,h+.24))
 return b.clean()
def supported_screws(m):
 # Cup UP. The terminal thread tip is sacrificial; the 6-mm working pin engagement never reaches it.
 mm=[];pm=orient(m,[1,0,0],180);pm.apply_translation([0,0,-pm.bounds[0,2]])
 for i in range(4):
  x=i*8;sc=move(pm,x=x);mm.append(sc)
  sh=[box(x-3.3,-2.7,0,6.6,5.4,.48),box(x-3.3,-.5,.4,.8,1,27),box(x+2.5,-.5,.4,.8,1,27)]
  for sign in [-1,1]:
   vv=pm.vertices
   for za,zb in [(2,5),(7,10),(12,15)]:
    vv2=vv[(vv[:,2]>za)&(vv[:,2]<zb)&(abs(vv[:,1])<.18)&(sign*vv[:,0]>1.49)]
    assert len(vv2)>0
    pt=vv2[np.argmin(abs(vv2[:,2]-(za+zb)/2))];z=float(pt[2])
    sh.append(box(x+1.40 if sign>0 else x-3.0,-.22,z-.12,1.6,.44,.24))
   # Plain neck brace, outside both fixed journal lands.
   sh.append(box(x+.69 if sign>0 else x-3.,-.22,22.4,2.31,.44,.24))
  mm.append(mesh(union(sh)))
 return merge(mm)
def assembly(rows=(0,0),cols=(0,0),travel=0,phases=(0,0,0,0),blocked=(),stalled=()):
 a={'frame':PART['frame']}
 for name in ['keeper-lower','keeper-upper']:
  a[name+'-0']=PART[name]
  mm=PART[name].copy();mm.apply_transform(np.diag([1,-1,1,1]));mm.apply_translation([0,P,0]);a[name+'-1']=mm
 for i in range(2):
  a[f'row-{i}']=move(PART['row-base'],x=S*rows[i],y=i*P)
  a[f'row-cap-{i}']=move(PART['row-cap'],x=S*rows[i],y=i*P)
  a[f'column-{i}']=move(PART['column'],x=i*P,y=S*cols[i])
 for iy in range(2):
  for ix in range(2):
   j=iy*2+ix;r=rows[iy];c=cols[ix];lift=cam(S*r);cap=min(21.9+cam(float(u)-S*c,1.0)-math.sqrt(max(0,.4**2-u*u)) for u in np.linspace(-.4,.4,401))-21.4;q=min(lift,cap,Q);q=min(q,.1) if j in blocked else q;delta=lift-q
   a[f'follower-{j}']=move(mesh(follower(delta=delta,q=q)),ix*P,iy*P)
   a[f'rotor-{j}']=move(PART['rotor'],ix*P,iy*P,q,rz=(ix*P-travel)/RP*180/math.pi+15)
   angle=phases[j]-(travel/RP*180/math.pi if q>=Q-.0001 and j not in stalled else 0)
   a[f'output-{j}']=move(PART['output-screw'],ix*P,iy*P,rz=angle)
   a[f'pin-{j}']=move(PART['pin'],ix*P,iy*P,61-3*angle/360)
 a['shared-rack']=move(PART['rack'],x=travel)
 a['hand-drive']=move(PART['drive'],x=-13.5,y=-3.6,rz=(-13.5-travel)/(M*36/2)*180/math.pi+5)
 return a

def main():
 base,cap=rowpieces();export('row-base',base);export('row-cap',cap,([1,0,0],180));export('column',colbar(),([1,0,0],180))
 for name,t in [('follower',.40),('follower-soft',.35),('follower-stiff',.45)]:export(name,follower(t),([1,0,0],90))
 for name,d in [('rotor',1.8),('rotor-loose',1.7),('rotor-tight',1.9)]:export(name,rotor(d),([1,0,0],180))
 export('rack',rack_shuttle());export('drive',drive())
 base=outputbase();cq.exporters.export(base,str(ENG/'output-interface.step'))
 source=ROOT/'tools/curated-experiment-checks/E-297/cad'
 thread=tm.load(source/'e295-thread.stl');thread.apply_translation([0,0,55])
 out=merge([mesh(base),thread]);export('output-screw',out,([1,0,0],180))
 export('pin',tm.load(source/'e295-pin.stl'),([1,0,0],180))
 ff=frame();export('frame',ff,([0,1,0],90))
 scaffold=[ff]
 for y in [0,P]:
  scaffold.append(cq.Solid.makeCylinder(.5,14.43,cq.Vector(-3.35,y,10.6),cq.Vector(1,0,0)))
  for xa,xb in [(-3.3,-2.05),(2.05,3.03),(7.13,8.38)]:scaffold.append(box(xa,y-.22,10.9,xb-xa,.44,.5))
 for y in [-5.5,10.58]:
  for z in [45,55,65,75]:scaffold.append(cq.Solid.makeCylinder(.5,16.08,cq.Vector(-5,y,z),cq.Vector(1,0,0)))
 export('frame-print',union(scaffold),([0,1,0],90))
 export('keeper-lower',keeper(False),([1,0,0],90));export('keeper-upper',keeper(True),([1,0,0],90))
 export('screw-tree',supported_screws(out))
 export('beam-100',rowbar(100))
 # Small test support pair, 50/75 mm span selectable by ordinary ruler; no special fixture needed.
 export('beam-support',box(0,0,0,8,12,4).cut(box(0,3.55,3.2,8,4.9,1)))
 manifests=[];x=5;y=5;rowh=0;placed=[]
 items=[('frame-print',1),('keeper-lower',2),('keeper-upper',2),('row-base',2),('row-cap',2),('column',2),('follower',4),('follower-soft',1),('follower-stiff',1),('rotor',4),('rotor-loose',1),('rotor-tight',1),('rack',1),('drive',1),('screw-tree',1),('pin',4),('beam-100',1),('beam-support',2)]
 for name,n in items:
  for k in range(n):
   m=PRINT[name].copy();dx,dy,dz=m.extents
   if x+dx>220:x=5;y+=rowh+5;rowh=0
   m.apply_translation([x,y,0]);placed.append(m);manifests.append({'name':f'{name}-{k+1}','source':f'components/{name}.stl','bounds_mm':m.bounds.tolist()});x+=dx+5;rowh=max(rowh,dy)
 assert y+rowh<240,(y,rowh)
 tm.util.concatenate(placed).export(PACK/'components/plate.stl')
 (PACK/'metadata/layout.json').write_text(json.dumps(manifests,indent=2)+'\n')
 # Engineering assemblies are distinct from print orientation. Individual components retained.
 for name,r,c in [('off',(0,0),(0,0)),('one',(1,0),(1,0)),('all',(1,1),(1,1)),('half',(1,1),(0,0))]:
  a=assembly(r,c);tm.util.concatenate(list(a.values())).export(ENG/f'assembly-{name}.stl')
  (ENG/f'assembly-{name}.json').write_text(json.dumps({k:{'bounds_mm':v.bounds.tolist()} for k,v in a.items()},indent=2))
 report={n:{'watertight':bool(m.is_watertight),'bodies':len(m.split()),'bounds_mm':m.bounds.tolist(),'volume_mm3':float(m.volume),'sha256':hashlib.sha256((OUT/(n+'.stl')).read_bytes()).hexdigest()} for n,m in PART.items()}
 (PACK/'metadata/meshes.json').write_text(json.dumps(report,indent=2)+'\n')
 params={'pitch':P,'row_stroke':S,'column_stroke':S,'cam_lift':RISE,'clutch_lift':Q,'cone_half_angle':30,'cone_radii':[1.1,1.9],'input_journal_d':1.8,'input_bore_d':2.06,'output_journal_d':1.6,'output_bore_d':1.88,'gear_module':M,'gear_teeth':N,'gear_pressure_angle':25,'flexure_thickness':.40,'flexure_depth':3.6,'flexure_horizontal_span':3.2,'flexure_vertical_pitch':.9,'source_commit':'1071f695b93951246a2865038e7fb9de9bdf2a05'}
 params.update(input_journal_centres=[33.6,38.6],output_journal_centres=[46.6,51.8],output_thrust_z=53.4,thread_start=55,pin_neutral_bottom=61,pin_guides=[64.5,75.8],cam_cap_separate=True)
 (PACK/'metadata/parameters.json').write_text(json.dumps(params,indent=2)+'\n')
 print('DONE',len(manifests),flush=True)
if __name__=='__main__':main()
