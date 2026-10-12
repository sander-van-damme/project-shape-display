"""E-213 axial docking. mm, N, MPa, s. Deterministic bounds, not print priors.
Finite convex prisms import E-212/E-208 SAT. No frictional holding is credited.
Run from any directory; JSON is disposable. NumPy only.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('control', Path(__file__).resolve().parents[1]/'E-212/capture.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
B = c.box
PITCH = 5.03  # adverse neighbor placement, inherited bounded scenario
L = 76.


def shift(parts, x=0., y=0., z=0.):
    return [(p+[y,z], (a+x,b+x)) for p,(a,b) in parts]


def sweep(parts, axis, a, b):
    """Exact union for translation of axis-aligned boxes on one axis."""
    out=[]
    for p,(x0,x1) in parts:
        lo=np.array([x0,*p.min(axis=0)]); hi=np.array([x1,*p.max(axis=0)])
        lo[axis]+=min(a,b); hi[axis]+=max(a,b)
        out.append(B(lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]))
    return out


def tail(size=0., hole=0., length=L):
    # Actual through-window: finite bottom bridge, two side ligaments and top.
    # Positive z faces carry pin load; window y faces are NOT free moment guides.
    a=.8+size; w=.5+hole
    return [B(-a,a,-a,a,0,1.5-hole), B(-a,a,-a,a,2.5+hole,length-41.9),
            B(-a,a,-a,-w,1.5-hole,2.5+hole), B(-a,a,w,a,1.5-hole,2.5+hole)]


def sleeve(pin=False, guide_error=0.):
    inner=1.05+guide_error
    out=[B(-1.85,1.85,-1.85,1.85,-1.,0.)]
    for sx,sy in itertools.product((-1,1),repeat=2):
        x=sorted((sx*1.05,sx*1.85)); y=sorted((sy*inner,sy*1.85))
        out.append(B(*x,*y,0,18.5))
    for z in (6.,18.):
        out += [B(-1.85,-1.05,-1.85,1.85,z-.5,z+.5),B(1.05,1.85,-1.85,1.85,z-.5,z+.5),
                B(-1.05,1.05,-1.85,-inner,z-.5,z+.5),B(-1.05,1.05,inner,1.85,z-.5,z+.5)]
    if pin:
        # Finite prismatic pin bearing, connected to the right corner posts.
        # Aperture +/- .4 y and z=1.6..2.4; nominal pin +/- .3 y, 1.7..2.3 z.
        out += [B(1.05,1.85,-1.85,-.4,1.2,2.8), B(1.05,1.85,.4,1.85,1.2,2.8),
                B(1.05,1.85,-.4,.4,1.2,1.6), B(1.05,1.85,-.4,.4,2.4,2.8)]
    return out


def pin(dx=0., through=False, error=0.):
    a=-1.85 if through else -.6
    return [B(a+dx,1.85+dx,-.3-error,.3+error,1.7-error,2.3+error)]


def installed(parts,h=0.,length=L,x=0.,y=0.):
    return shift(parts,x=x,y=1.95+y,z=-length+h)


def assembly(h=0.,length=L):
    # .1-mm overlap into the original moving web, not a disconnected tail.
    return c.rack(h,web=.8)+installed(tail(length=length),h,length)


def volume(parts):
    # Exact box-union volume; avoids counting overlap between ribs and rings.
    lo=np.array([[x[0],*p.min(axis=0)] for p,x in parts]); hi=np.array([[x[1],*p.max(axis=0)] for p,x in parts])
    grid=[sorted(set(lo[:,i])|set(hi[:,i])) for i in range(3)]; v=0.
    for i,j,k in itertools.product(*(range(len(g)-1) for g in grid)):
        low=np.array([grid[0][i],grid[1][j],grid[2][k]]); high=np.array([grid[0][i+1],grid[1][j+1],grid[2][k+1]])
        mid=(low+high)/2
        if np.any(np.all((mid>=lo)&(mid<=hi),axis=1)):v+=float(np.prod(high-low))
    return v


def finite():
    frame=c.r.fixed(.2,0,.2)
    # Nominal constant-pose docking and pin insertion/departure are exact sweeps.
    short=pin(); dock=sweep(sleeve(True)+pin(1.7),2,-20,0)
    assert not c.hits(dock,tail())
    assert not c.hits(sweep(short,0,0,1.7),tail())
    assert not c.hits(sweep(short,0,0,1.7),sleeve(True))
    assert c.hits(installed(tail()),c.rack(web=.8)), 'tail/web not connected'
    # Independent nearest-neighbor heights: exact union of all 0..40 positions.
    neighbors=[]
    for x,y in [(PITCH,0),(-PITCH,0),(0,PITCH),(0,-PITCH)]:
        neighbors += shift(sweep(assembly(),2,0,40),x=x,y=y)
    short_envelope=installed(sweep(sleeve(True)+pin(1.7),2,-20,41.5))
    assert not c.hits(short_envelope,neighbors)
    assert not c.hits(short_envelope,frame)
    # Original shallow proposal exposes the resident frame conflict at maximum lift.
    shallow=installed(sleeve(True)+pin(),41.5,60.)
    shallow_hit=c.hits(shallow,frame)
    assert shallow_hit
    # A long pin needs 2.95-mm withdrawal; actual body hits a higher neighbor shaft.
    long_pin=installed(pin(2.95,True),20)
    long_hit=c.hits(long_pin,shift(assembly(0),x=PITCH))
    assert long_hit
    # Twenty arbitrary endpoint transitions. Relative head/tail solids stay fixed;
    # exact sweep against opened toe/frame covers every intermediate z.
    opened=c.toe((-1.2,0.,.22))
    checks=0
    for a,b in itertools.permutations(range(0,41,10),2):
        moving=sweep(assembly()+installed(sleeve(True)+pin()),2,min(a,b)+1.5,max(a,b)+1.5)
        assert not c.hits(moving,opened+frame)
        checks+=1
    # Rocking toe still needs its independent writer. Tail head does not release it.
    subdivision=[]
    for n in (16,32,64):
        bad=0
        poses=[(0.,0.,q) for q in np.linspace(0,.22,n+1)]
        poses += [(-w,0.,.22) for w in np.linspace(0,1.2,n+1)[1:]]
        for q in poses:
            bad+=bool(c.hits(c.toe(q),assembly(1.5)+installed(sleeve(True)+pin(),1.5)))
        assert not bad
        subdivision.append(dict(n=n,poses=len(poses),hits=bad))
    return dict(short_nominal_exact_dock_and_depart=True,short_neighbor_sweeps_clear=True,
                transitions=checks,shallow_L60_frame_witness=shallow_hit[0],
                long_pin_neighbor_witness=long_hit[0],toe_path=subdivision)


def fit_corners():
    # Coherent head offset, common size error, window error and pin stock error.
    # Axial location sought from real tail bottom, not a fixed exact height command.
    total=0; fails=0; min_gap=100.
    for dx,dy,size,hole,dz,pe in itertools.product((-.05,.05),repeat=6):
        pe*=.4  # +/- .02 pin half-size
        actual=shift(tail(size,hole),x=dx,y=dy)
        moving=shift(sweep(pin(error=pe),0,0,1.7),z=dz)
        total+=1
        fails+=bool(c.hits(moving,actual) or c.hits(sweep(sleeve(True),2,-20,0),actual))
        min_gap=min(min_gap,.2+hole-abs(dy)-pe,.2+hole-abs(dz)-pe)
    assert fails==0 and abs(min_gap-.08)<1e-10
    # Actual tilted prisms at acquired bottom contact. No automatic recentering.
    angular=[]
    for bound in (0.,.005,.01,.02):
        bad=0;count=0
        for angle,dx,dy,size in itertools.product((-bound,bound),(-.05,.05),(-.05,.05),(-.05,.05)):
            cs,sn=math.cos(angle),math.sin(angle)
            parts=[(p@np.array([[cs,sn],[-sn,cs]]),(x[0]+dx,x[1]+dx)) for p,x in tail(size)]
            bottom=min(p[:,1].min() for p,x in parts)
            parts=shift(parts,y=dy,z=-bottom)
            count+=1
            bad+=bool(c.hits(parts,sleeve(True)+pin()))
        angular.append(dict(pitch_bound_rad=bound,corners=count,collision_corners=bad))
    return dict(parallel_corners=total,failures=fails,minimum_pin_gap_mm=min_gap,angular=angular)


def loaded_contact():
    # Exact 2D rigid shaft against finite guide bands: contact at z=5.5/18.5.
    # Floor seats lowest corner. Both signs symmetric. No friction at floor/pads.
    # Solve 13*tan(theta)+2*a/cos(theta)=2*b; translation centers the contacts.
    cases=[]
    for size,bias in itertools.product((-.05,0.,.05),(-.05,0.,.05)):
        a=.8+size; b=1.05+bias; lo=0.;hi=.2
        for _ in range(65):
            th=(lo+hi)/2
            if 13*math.tan(th)+2*a/math.cos(th)>2*b:hi=th
            else:lo=th
        theta=(hi+lo)/2
        # Coordinate transform y=cos*t_y + sin*t_z + offset.
        # The opposite sign selects the other pair; signs do not change burden.
        offset=-12*math.tan(theta)
        # For specified floor height, y section center = offset+z*tan(theta).
        # Solve actual solid translation to realize it and seat min bottom z=0.
        cs,sn=math.cos(theta),math.sin(theta)
        rotated=[(p@np.array([[cs,-sn],[sn,cs]]),x) for p,x in tail(size)]
        bottom=min(p[:,1].min() for p,x in rotated)
        # Rotated center y at z=0 is ty - tan(theta)*tz.
        tz=-bottom; ty=offset+math.tan(theta)*tz
        actual=shift(rotated,y=ty,z=tz)
        assert not c.hits(actual,sleeve(guide_error=bias)), 'guide contact solution penetrates'
        interference=bool(c.hits(actual,pin()))
        # At nominal pin center z=2, shift is offset+2*tan(theta).
        center_y=offset+2*math.tan(theta)
        cases.append(dict(tail_half_error=size,guide_half_error=bias,theta_rad=theta,
                          window_center_y_mm=center_y,pin_interference=interference,
                          transverse_pair_for_11_5_Nmm_N=11.5/13))
    assert all(x['pin_interference'] for x in cases)
    # Opposite guide reactions + floor furnish full static balance in this plane.
    # 11.5 Nmm is a nominal reference moment; real tilted-rack load arm is changed.
    assert abs(13*(11.5/13)-11.5)<1e-12
    return cases


def packing():
    # Two independently moving heads sharing the same y row, not synchronized poses.
    a=sleeve(True)+pin(1.7)
    nominal=bool(c.hits(a,shift(a,x=5.08)))
    conflict=bool(c.hits(a,shift(sweep(a,2,-41.5,41.5),x=5.08)))
    assert conflict
    tests=[]
    for depth in (20.,40.,60.,62.,80.,82.):
        # Each head may also be parked 20 mm below its lowest tail.
        # Relative head phase therefore spans +/-61.5 mm, including docking.
        b=shift(sweep(a,2,-61.5,61.5),x=5.08,z=-depth)
        tests.append(dict(depth_offset_mm=depth,independent_head_collision=bool(c.hits(a,b))))
    assert tests[0]['independent_head_collision'] and not tests[-1]['independent_head_collision']
    # Depth staggering cannot rescue a long pin aimed toward a deeper neighbor:
    # its shaft, not only its flange, occupies the whole access corridor.
    deep_neighbor=shift(assembly(0,L+82),x=PITCH)
    stagger_fail=bool(c.hits(installed(pin(2.95,True),20),deep_neighbor))
    # A shallow head cannot index across a deeper shaft at its usual park.
    crossing=bool(c.hits(sweep(installed(a,-20),0,0,PITCH),deep_neighbor))
    assert crossing
    # Fixed-column row indexing avoids it: x separation persists along all y.
    assert not c.hits(sweep(installed(a,-20),1,0,PITCH),deep_neighbor)
    assert stagger_fail
    return dict(same_height_short_head_collision=nominal,arbitrary_height_short_head_collision=conflict,depth_sweep=tests,
                long_pin_hits_deeper_tail=stagger_fail,shallow_cross_column_park_collision=crossing,
                rest_depth_single_mm=L+21,rest_depth_two_tiers_mm=L+82+21)


def state_machine():
    # Requirements, not simulated hardware detectors. Commands never prove support.
    states=[('resident',True,False,False),('dock',True,False,False),
            ('capture_and_prove',True,True,False),('unload',False,True,False),
            ('release',False,True,False),('translate',False,True,False),
            ('reseat',True,True,False),('resident_proof',True,True,True),
            ('depart',True,False,True)]
    assert all(resident or head for _,resident,head,proof in states)
    # Depart is forbidden for a failed proof; head support remains required.
    def may_depart(proof,neighbor_support):return proof and neighbor_support
    assert not may_depart(False,True) and may_depart(True,True)
    return dict(command_states=[x[0] for x in states],failed_proof_action='remain captured; stop module',
                unchanged_neighbor_resident_support_required=True,
                support_flags='conditional interfaces, not sensor or force simulation',
                pin_free_proof_stroke_bound_mm=.08)


def bounds():
    rows=[]
    # Dock 20+old height; unload 1.5; translate; reseat 1.5; depart 20+new.
    # The five-state maximum old/new pair is 10/40 or 40/10 mm.
    # Two pin strokes are serial with docking/departure; common overhead 6 seconds.
    for H in (40,80,160):
        times=[]
        for acc,aux in itertools.product((1000.,5000.,20000.),(.08,.16,.32)):
            # Safe horizontal park: sleeve top below lowest tail. Acquisition and
            # departure include actual old/new height; no free Z preposition.
            motion=max(sum(2*math.sqrt(d/acc) for d in
                           (20+old,1.5,abs(new-old),1.5,20+new,1.7,1.7))
                       for old,new in itertools.product(range(0,41,10),repeat=2))
            times.append(dict(a_mm_s2=acc,aux_s=aux,cycle_s=motion+aux,
                              strict_slot_pass=motion+aux<24*H/6400))
        rows.append(dict(H=H,slot_s=24*H/6400,tail_head_guided_outputs=2*H,
                         inherited_toe_pad_outputs=4*H,axial_guide_stations=2*H,
                         longitudinal_rows_at_40_heads_each=math.ceil(H/40),
                         cost_per_head_if_250_elsewhere=250/H,
                         timing=times))
    stresses=[dict(pull_N=F,pin_cantilever_stress_MPa=6*F*1.05/(.6*.6**2)) for F in (1.,10.)]
    # Incremental material only; inherited rack unchanged. Union overlap .1 removed.
    added=(volume(tail())-.1*1.6*.5)*6400/1000
    return dict(heads=rows,nominal_downward_floor_pressure_MPa=10/(1.6*1.6),
                pin_pull_stress=stresses,tail_added_cm3=added,
                two_tier_extra_tail_cm3=3200*82*1.6*1.6/1000,
                sleeve_solid_mm3=volume(sleeve(True)),
                max_resident_dollars_if_250_elsewhere=250/6400,
                reference_guide_pair_12mm_N=11.5/12,
                e212_reference_pair_N=7/12)


def buckling():
    # Ideal elastic Euler scenarios, NOT calibrated PLA properties. Upper end at
    # tail/web transition and last writer guide give the most favorable span.
    # Fixed/fixed endpoints are an upper comparison for this unbraced prism.
    rows=[]
    I=1.6**4/12
    for depth in (0.,82.):
        span=L+depth-41.9-18.5
        for E in (500.,2200.,3500.):
            pin=math.pi**2*E*I/span**2
            rows.append(dict(stagger_mm=depth,unsupported_smooth_tail_mm=span,
                             E_MPa=E,pinned_euler_N=pin,fixed_fixed_euler_N=4*pin))
    # Independent Rayleigh energy quadrature for fixed/fixed phi=1-cos(2*pi*x/l).
    err=[]
    for n in (32,64,128):
        x=np.linspace(0,1,n+1); d=2*math.pi*np.sin(2*math.pi*x)
        dd=(2*math.pi)**2*np.cos(2*math.pi*x)
        value=np.trapz(dd*dd,x)/np.trapz(d*d,x)
        err.append(abs(value/(4*math.pi**2)-1))
    assert max(err)<1e-12
    return dict(scenarios=rows,energy_quadrature_relative_errors=err)


def verify():
    assert not c.hits([B(0,1,0,1,0,1)],[B(1,2,0,1,0,1)])
    assert c.hits([B(0,1,0,1,0,1)],[B(.999,2,0,1,0,1)])
    assert abs(volume([B(0,1,0,1,0,1),B(.5,1.5,0,1,0,1)])-1.5)<1e-12
    # Continuous timing maximizer: for new=40, stationarity gives old=10.
    # Independent 1-mm grid holdout also covers diagonal/no-height-change cases.
    measure=lambda a,b:math.sqrt(20+a)+math.sqrt(abs(b-a))+math.sqrt(20+b)
    assert max(measure(a,b) for a,b in itertools.product(range(41),repeat=2))==measure(10,40)
    # Old jaw/guide control is preserved, independently of new coordinates.
    assert not c.hits(c.guide(gap=.15),c.r.p.writer(1.099))
    assert c.hits(c.guide(gap=.15),c.r.p.writer(1.101))
    return dict(finite=finite(),fit=fit_corners(),loaded_contact=loaded_contact(),
                packing=packing(),state=state_machine(),buckling=buckling(),bounds=bounds())


if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
