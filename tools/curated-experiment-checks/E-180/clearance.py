"""E-180. Deterministic finite pickup-access and proof-probe screen; mm,N,s.
No process distributions, optical rendering or physical qualification.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path
s=importlib.util.spec_from_file_location('opt',Path(__file__).parents[1]/'E-178/readback.py')
o=importlib.util.module_from_spec(s);s.loader.exec_module(o)
P=5.08

def overlap(a,b):
    return all(min(a[1][j],b[1][j])-max(a[0][j],b[0][j])>1e-10 for j in range(3))

def solids(c,r,h,q):
    x=c*P;y=r*P
    yield 'spine',((x-.6,y-2.3,h-41.4),(x+.6,y+2.3,h+50))
    yield 'lip',((x-1.8,y-.5,h+.95),(x-.2,y+.5,h+1.95))
    yield 'pad',((x-2.2,y+q-.5,-3),(x-1.2,y+q+.5,-2))
    for j in range(5):
        yield 'tooth',((x+.2,y+.9*(j-2)-.25,h-j*10.1),(x+1.8,y+.9*(j-2)+.25,h-j*10.1+1.2))
    # Union of all grounded dog lanes is conservative for optical access.
    yield 'dog envelope',((x+1.2,y-2.05,-1),(x+2.2,y+2.05,0))
    yield 'reset tooth',((x-2.8,y-1.3,-2.8),(x-1.3,y-.9,-2.2))
    yield 'reset post',((x-2.8,y-1.3,-3.5),(x-2.5,y-.9,-2.2))
    yield 'reset rail',((x-2.8,y-2.54,-4),(x-2.5,y+2.54,-3.5))

def expand(box,e):return tuple(tuple(v+sign*e for v in corner) for corner,sign in zip(box,(-1,1)))

def optical(e=.05,subdivisions=1):
    # Direct underside cameras: two Y positions, same X lane. One also suffices
    # for known pad plane; no credit for unspecified deck/guide transparency.
    n=0;blocked=0;witness=None
    obstacles=[]
    for c,r,h,q in it.product((-1,0,1),(-1,0,1),o.LEVELS,(0,1.7)):
        for name,box in solids(c,r,h,q):
            if c==r==0 and name=='pad':continue # target surface, not occluder
            obstacles.append((name,c,r,expand(box,e)))
    obstacles=list(dict.fromkeys(obstacles))
    for q,cy,sx,sy,sz,tx,ty,tz in it.product((0,1.7),(-2.,2.),(-1,1),(-1,1),(-1,1),(-1,1),(-1,1),(-1,1)):
        camera=(-1.7+sx*(.15+e),cy+sy*e,-50+sz*e)
        # Four inset bottom-face points; ray errors include local edge/plane shift.
        target=(-1.7+tx*(.4+e),q+ty*(.4+e),-3+tz*e)
        n+=1
        hit=None
        for name,c,r,box in obstacles:
            if any(max(camera[j],target[j])<box[0][j] or min(camera[j],target[j])>box[1][j] for j in range(3)):continue
            if any(o.hit_box(tuple(a+(b-a)*k/subdivisions for a,b in zip(camera,target)),
                             tuple(a+(b-a)*(k+1)/subdivisions for a,b in zip(camera,target)),*box)
                   for k in range(subdivisions)):
                hit=(name,c,r);break
        if hit:
            blocked+=1;witness=witness or dict(camera=camera,target=target,obstacle=hit)
    return dict(e_mm=e,rays=n,blocked=blocked,witness=witness)

def shared_camera():
    # Attempt sharing one direct camera over 20 cells, with actual low spines.
    camera=(9.5*P-1.7,.85,-50);out=[]
    for q in (0,1.7):
        blocked=[]
        for c in range(20):
            t=(c*P-1.7,q,-3)
            for k in range(20):
                box=((k*P-.6,-2.3,-41.4),(k*P+.6,2.3,50))
                if o.hit_box(camera,t,*box):blocked.append(c);break
        out.append(dict(q=q,blocked_columns=blocked,total=20))
    return out

def projection():
    # Single underside view with explicit aggregate localization errors.
    # y_measured=.85+47*(y-.85)/(z+50), then +/- .1 registration/read error.
    out=[]
    for e in (.05,.1,.2):
        vals=[]
        for q in (0,1.7):
            v=[.85+47*(q+sy*e-.85)/(47+sz*e)+sr*.1
               for sy,sz,sr in it.product((-1,1),repeat=3)]
            vals.append((min(v),max(v)))
        out.append(dict(edge_or_center_error_mm=e,active=vals[0],clear=vals[1],gap_mm=vals[1][0]-vals[0][1]))
    return out

def probe():
    # Probe beneath the entire potential lip overlap. Shaft is 1.2 by 1.4 mm,
    # from lower crossbar to tip; 2-mm up/down approach each row.
    broad=((-2.3,-.7,-47),(-1.1,.7,-1.5))
    narrow=((-1.9,-.2,-45),(-1.5,.2,-1.5))
    partial=((-2.2,.49,-3),(-1.2,1.49,-2))
    assert not overlap(narrow,partial) and overlap(broad,partial)
    # Partial pad still overlaps lip Y by .01 mm on the next ascent.
    assert min(partial[1][1],.5)-max(partial[0][1],-.5)>.0099
    counts=[]
    for e in (0,.05,.1,.2):
        false_clear=0;unsafe=0;clear_collisions=0;n=0
        # Independent pad lower-edge, lip upper-edge, probe upper-edge and
        # X-facing errors; intervals also provide a continuous q certificate.
        for a,b,c,d in it.product((-1,1),repeat=4):
            for i in range(401):
                q=1.7*i/400;lo=q-.5+a*e;lip=.5+b*e;tip=.7+c*e
                dangerous=lo<lip
                detected=lo<tip and (-1.2-d*e)>(-2.3+e) and (-2.2+d*e)<(-1.1-e)
                unsafe+=dangerous;false_clear+=dangerous and not detected;n+=1
            clear_collisions+=1.2+a*e<.7+c*e
        counts.append(dict(e_mm=e,samples=n,unsafe=unsafe,false_clear=false_clear,
                           nominal_clear_collisions=clear_collisions,
                           continuous_coverage_margin_mm=.2-2*e,
                           clear_gap_mm=.5-2*e))
    # Actual swept probe volume against neighboring low/high columns and comb.
    # Scan at retracted tip z=-3.5 (below pad -3); advance only at row datum.
    collisions=[]
    for c,r,h,q in it.product((-1,0,1),(-1,0,1),o.LEVELS,(0,1.7)):
        for name,box in solids(c,r,h,q):
            if c==r==0 and name=='pad':continue
            if overlap(expand(broad,.05),expand(box,.05)):collisions.append((c,r,h,q,name))
    assert not collisions
    # Continuous row scan envelopes: spine in X, pad/comb tooth in Z,
    # lip in Z, reset rails in X. Test neighboring solids through two pitches.
    scan_box=((-2.3,-.7,-47),(-1.1,2*P+.7,-3.5))
    scan_hits=[]
    for c,r,h,q in it.product((-1,0,1),range(-1,4),o.LEVELS,(0,1.7)):
        for name,box in solids(c,r,h,q):
            if overlap(expand(scan_box,.05),expand(box,.05)):scan_hits.append((c,r,name))
    assert not scan_hits
    return dict(narrow_probe_false_clear_q_mm=.99,broad_sweep_collisions=collisions,
                retracted_scan_collisions=scan_hits,coverage=counts,
                scope='known boxes only; deck/guide housing and crossbar not constructed')

def stability():
    # Unbraced rectangular cantilever; perfect Euler screen, not a safe load.
    # Independent Rayleigh integral over exact first mode checks factor 4.
    L=43.5;out=[]
    for b,E in it.product((1.0,1.2,1.4),(500.,1500.,3000.)):
        I=min(1.4*b**3,b*1.4**3)/12;critical=math.pi**2*E*I/(4*L**2)
        out.append(dict(width_mm=b,E_MPa=E,ideal_critical_N=critical,
                        force_ceiling_if_factor2_N=critical/2))
    convergence=[]
    for n in (16,64,256):
        dx=L/n
        # w=1-cos(pi*x/(2L)), Rayleigh P=EI integral(w''²)/integral(w'²).
        k=math.pi/(2*L)
        num=sum((k*k*math.cos(k*(i+.5)*dx))**2*dx for i in range(n))
        den=sum((k*math.sin(k*(i+.5)*dx))**2*dx for i in range(n))
        ratio=num/den/k**2;assert abs(ratio-1)<1e-12
        convergence.append(dict(n=n,normalized_critical=ratio))
    return dict(cases=out,energy_checks=convergence,
                assumptions='perfect elastic fixed-free column; effective E is epistemic, not sourced PLA property')

def timing():
    out=[]
    for B in (4,8,16):
        rows=80//B
        # Same row scan, .02-s proof slot is replaced by approach/retract + .02.
        extra=2*rows*o.move(2.)+2*o.move(2.) # one repeated row attempt
        baseline={4:21.494,8:13.127,16:8.944}[B]
        out.append(dict(banks=B,reusable_probes=80*B,extra_probe_motion_s=extra,
                        broadcast_plus_probe_s=baseline+extra))
    serial=[]
    for cams in (4,8,16):
        rows=80//cams
        # Snake full rows, v=200; path-length lower bound only, no accel/return.
        path=rows*79*P+(rows-1)*P
        serial.append(dict(cameras=cams,distance_mm=path,scan_lower_bound_s=path/200))
    return dict(probe=out,sparse_camera_snake=serial)

def causal_check():
    # Two grounded columns, only column 0 requested. Perfect clear proof at
    # home precedes arming. A wrong-address arm creates unsafe next ascent.
    wanted=(1,0);proved_clear=(0,0);faulted_write=(0,1)
    assert proved_clear==(0,0) and faulted_write!=wanted
    # E-173 h=max(grounded,d-delta) with delta=1: d=3 lifts stale active by 2.
    lifted=tuple(max(0.,3.-1.) if q else 0. for q in faulted_write)
    assert lifted[1]==2.
    # A missing tooth gives the same common-bar endpoint as a clear pad.
    pad_active=(False,True);probe_present=(True,False)
    bar_passes=not any(a and p for a,p in zip(pad_active,probe_present))
    assert bar_passes
    return dict(missing_probe_false_clear=bar_passes,requested_pickups=wanted,perfect_home_clear_proof=proved_clear,
                wrong_address_write=faulted_write,next_heights_mm=lifted,
                implication='clear-only probe cannot replace post-arm mask proof or retention')


def main():
    optics=[optical(e) for e in (0,.05,.1)]
    for subdivisions in (4,16):assert optical(.05,subdivisions)==optics[1]
    assert all(x['blocked']==0 for x in optics)
    p=probe();assert all(x['false_clear']==0 for x in p['coverage'][:3])
    print(json.dumps(dict(local_optics=optics,shared_camera=shared_camera(),
                         projected_centers=projection(),probe=p,stability=stability(),timing=timing(),causal=causal_check()),indent=2))
if __name__=='__main__':main()
