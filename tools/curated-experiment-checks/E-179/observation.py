"""E-179: finite mirror synthesis and bounded observability. mm, s.
Standard-library deterministic epistemic scenarios, no manufactured yield.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec=importlib.util.spec_from_file_location('height',Path(__file__).parents[1]/'E-178/readback.py')
height=importlib.util.module_from_spec(spec);spec.loader.exec_module(height)
P=5.08

def ray(target,camera,center,angle):
    a=math.radians(angle)
    n=(0,math.cos(a),math.sin(a)); tangent=(0,math.sin(a),-math.cos(a))
    virtual=height.sub(target,height.mul(2*height.dot(height.sub(target,center),n),n))
    direction=height.sub(virtual,camera)
    den=height.dot(direction,n)
    if abs(den)<1e-12:return None
    f=height.dot(height.sub(center,camera),n)/den
    if not 0<f<1:return None
    m=height.add(camera,height.mul(f,direction))
    # Visible +Y face, not a ray reaching the back of the opaque output.
    if m[1]<=target[1]:return None
    incident=height.sub(m,camera);out=height.sub(target,m)
    refl=height.sub(incident,height.mul(2*height.dot(incident,n),n))
    assert height.dot(refl,out)>0
    assert abs(height.dot(refl,out)**2-height.dot(refl,refl)*height.dot(out,out))<1e-5
    assert abs(math.dist(camera,m)+math.dist(m,target)-math.dist(camera,virtual))<1e-9
    return m,height.dot(height.sub(m,center),tangent)

def targets(kind):
    if kind in ('ground','profile'):
        zs=(-.08,.08) if kind=='ground' else (-.5,.6)
        return [(1.7,.9*(j-2)+.25,z) for j in range(5) for z in zs]
    if kind=='pickup':return [(-1.7,q+.5,-2.5) for q in (0,1.7)]
    return targets('ground')+targets('pickup')

def search(kind,error,step):
    # Continuous row-spanning mirror must fit between the E-173 spines.
    # Same e independently expands each neighboring spine and mirror envelope.
    half_y=.24-2*error
    if half_y<=0:return None
    best=None
    for angle in range(15,76,step):
        sn=math.sin(math.radians(angle));cs=math.cos(math.radians(angle))
        half_length=half_y/sn
        for iz in range(round(-8/step*10),round(4/step*10)+1):
            z=iz*step/10
            margin=1e10
            for t in targets(kind):
                # Reduced YZ reflection for search, checked against full 3D rays below.
                d=(t[1]-2.54)*cs+(t[2]-z)*sn
                vy=t[1]-2*d*cs;vz=t[2]-2*d*sn
                den=(vy-2.54)*cs+(vz+60)*sn
                if abs(den)<1e-12:margin=-1e10;break
                f=(z+60)*sn/den
                my=2.54+f*(vy-2.54);mz=-60+f*(vz+60)
                if not 0<f<1 or my<=t[1]:margin=-1e10;break
                along=(my-2.54)*sn-(mz-z)*cs
                margin=min(margin,half_length-abs(along))
            if best is None or margin>best['margin_mm']:
                best=dict(kind=kind,error_mm=error,angle_deg=angle,z_mm=z,
                          half_length_mm=half_length,margin_mm=margin)
    margins=[]
    for t in targets(kind):
        full=ray(t,(0,2.54,-60),(0,2.54,best['z_mm']),best['angle_deg'])
        margins.append(-1e10 if full is None else best['half_length_mm']-abs(full[1]))
    assert abs(min(margins)-best['margin_mm'])<1e-9
    return best

def original_route():
    misses={}
    for kind in ('ground','pickup'):
        values=[]
        for t in targets(kind):
            r=ray(t,(0,1.6,-50),(0,1.6,0),45)
            values.append(None if r is None else .7*math.sqrt(2)-abs(r[1]))
        misses[kind]=dict(trials=len(values),misses=sum(x is None or x<0 for x in values),margins_mm=values)
    # Real finite mirror segment intersects a spine even at highest column.
    a=(0,.9,.7);b=(0,2.3,-.7)
    collisions=[height.hit_box(a,b,(-.6,-2.3,h-41.4),(.6,2.3,h+50)) for h in height.LEVELS]
    assert all(collisions)
    return dict(mirror_spine_collisions=collisions,output_faces=misses)

def fiducials():
    L=101.6;A=.3;K=A*(math.pi/L)**2
    # Translation + scale + a smooth between-fiducial bow; affine part cancels.
    def actual(x):return .7+.003*x+A*math.sin(math.pi*x/L)
    out=[]
    for intervals in (1,2,4,8):
        dx=L/intervals;max_error=0
        for i in range(10001):
            x=L*i/10000;k=min(intervals-1,int(x/dx));w=(x-k*dx)/dx
            fitted=(1-w)*actual(k*dx)+w*actual((k+1)*dx)
            max_error=max(max_error,abs(actual(x)-fitted))
        bound=K*dx*dx/8
        assert max_error<=bound+1e-12
        out.append(dict(intervals=intervals,max_residual_mm=max_error,curvature_bound_mm=bound,
                        total_bound_mm=bound+.04+.04+.08))
    # Adversarial alternating local offsets are invisible to stationary fiducials.
    return dict(span_mm=L,bow_amplitude_mm=A,curvature_per_mm=K,
                interpolation=out,other_bounds_mm=dict(fiducial=.04,optics=.04,local_part=.08),
                local_unobservable_error_mm=.25,
                max_spacing_for_point2mm=math.sqrt(8*(.2-.16)/K))

def aliases():
    # Exact orthographic silhouette of a cuboid looking along +Y. Translation
    # in Y cannot be observed, even with infinite spatial resolution in X/Z.
    def silhouette(box):lo,hi=box;return lo[0],hi[0],lo[2],hi[2]
    a=((-2.2,-.5,-3),(-1.2,.5,-2))
    b=((-2.2,1.2,-3),(-1.2,2.2,-2))
    assert silhouette(a)==silhouette(b)
    # E-179 relocated 45-degree mirror: virtual camera is (48.26,60.04,-2.5).
    # An unsafe active cuboid is a homothetic copy of a safe clear cuboid.
    C=(9.5*P,60.04,-2.5);cx=10*P
    safe=((cx-2.2,1.2,-3),(cx-1.2,2.2,-2))
    scale=(C[1]-.5)/(C[1]-2.2)
    unsafe=tuple(height.add(C,height.mul(scale,height.sub(v,C))) for v in safe)
    nominal_active=((cx-2.2,-.5,-3),(cx-1.2,.5,-2))
    max_edge_error=max(abs(a-b) for v,w in zip(unsafe,nominal_active) for a,b in zip(v,w))
    assert max_edge_error<.05
    def project(v):return ((v[0]-C[0])/(C[1]-v[1]),(v[2]-C[2])/(C[1]-v[1]))
    for bits in it.product((0,1),repeat=3):
        p=tuple(safe[b][i] for i,b in enumerate(bits));q=tuple(unsafe[b][i] for i,b in enumerate(bits))
        assert math.dist(project(p),project(q))<1e-14
    # A second X viewpoint breaks this exact homothety; access is still owed.
    stereo=[]
    for baseline in (5,10,20):
        dnear=C[1]-2.2;dfar=C[1]-.5
        delta=baseline*(1/dnear-1/dfar)*dfar
        stereo.append(dict(baseline_mm=baseline,object_plane_disparity_mm=delta,
                           pixels_at_1280_per_101point6=delta*1280/101.6))
    # E-166 toe shortening removes depth overlap but preserves XZ silhouette.
    hook=((-1,0,12),(1,1,12.2));short=((-1,0,12),(1,.3,12.2))
    assert silhouette(hook)==silhouette(short)
    assert hook[1][1]-.4>.0 and short[1][1]-.4<0
    # Friction jaw geometry identical while hidden friction differs.
    force=120.;jaw=[dict(mu=m,capacity_N=m*force,holds_10N=m*force>=10) for m in (.02,.1)]
    assert jaw[0]['holds_10N']!=jaw[1]['holds_10N']
    return dict(pad_orthographic_alias=True,virtual_camera=C,
                perspective_scale_ratio=scale,safe_clear_box=safe,unsafe_active_box=unsafe,
                max_active_edge_error_mm=max_edge_error,second_view=stereo,
                hook_orthographic_overlap_mm=[.6,-.1],jaw_same_geometry=jaw,
                projection_scope='exact identical 8-vertex pinhole projections, untextured cuboids; not photometric equivalence')

def finite_pickup_paths():
    # New lower strip is deliberately tested alone. A second strip can occlude it;
    # two positive individual paths do not certify a multi-strip assembly.
    center=(0,2.54,-2.5);camera=(9.5*P,2.54,-60)
    counts={};witness={}
    for q in (0,1.7):
        blocked=0
        for col in range(20):
            t=(col*P-1.7,q+.5,-2.5)
            m,_=ray(t,camera,center,45)
            # Search actual finite spines over every discrete neighbor height.
            hit=None
            for c,r,h in it.product(range(-1,21),(-1,0,1),height.LEVELS):
                lo=(c*P-.6,r*P-2.3,h-41.4);hi=(c*P+.6,r*P+2.3,h+50)
                if height.hit_box(camera,m,lo,hi) or height.hit_box(m,t,lo,hi):
                    hit=(c,r,h);break
            if hit is not None:
                blocked+=1;witness.setdefault(str(q),dict(column=col,occluder=hit,mirror=m,target=t))
        counts[str(q)]=dict(targets=20,spine_blocked=blocked)
    return dict(counts=counts,witness=witness,scope='center rays and real finite spines only; other supports and apertures not certified')

def stacked_mirrors():
    # Finite lower strip blocks camera-to-upper-strip rays; zero-thickness sheet
    # is already opaque. No need to invent a housing to get this failure.
    camera=(9.5*P,2.54,-60);hits=0;n=0
    for col in range(20):
        for t in targets('ground'):
            t=(col*P+t[0],t[1],t[2])
            upper,_=ray(t,camera,(0,2.54,0),45)
            direction=height.sub(upper,camera)
            f=(.04-camera[1]-camera[2])/(direction[1]+direction[2])
            p=height.add(camera,height.mul(f,direction))
            along=((p[1]-2.54)-(p[2]+2.5))/math.sqrt(2)
            hit=0<f<1 and abs(along)<=.14*math.sqrt(2) and -2.54<=p[0]<=79*P+2.54
            hits+=hit;n+=1
    assert hits==n
    return dict(upper_rays=n,lower_strip_obstructions=hits,lower_half_y_mm=.14)

def timing():
    s=height.scan(80)
    return dict(one_scan_s=s,two_serial_scans_s=2*s,
                direct_plus_two_s=19.469+2*s,broadcast_plus_two_s=21.494+2*s,
                one_pass_dual_slot_s=height.scan(80,slot=.04),
                direct_plus_dual_slot_s=19.469+height.scan(80,slot=.04))

def main():
    # Independent central 90-degree reflection limiting check.
    m,s=ray((0,.6,0),(0,1.6,-50),(0,1.6,0),45)
    assert math.dist(m,(0,1.6,0))<1e-10 and abs(s)<1e-10
    results=[search(k,e,step) for k in ('ground','profile','pickup','both') for e in (0,.05) for step in (2,1)]
    print(json.dumps(dict(original=original_route(),synthesis=results,fiducials=fiducials(),
                         aliases=aliases(),pickup_paths=finite_pickup_paths(),stacked=stacked_mirrors(),timing=timing()),indent=2))
if __name__=='__main__':main()
