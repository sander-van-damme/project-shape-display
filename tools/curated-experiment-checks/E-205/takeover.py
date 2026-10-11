#!/usr/bin/env python3
"""Finite split-jaw handoff, mm/N; bounded scenarios, no hardware/yield claim."""
import importlib.util
from pathlib import Path
import sys
import json
import math
from itertools import product

spec = importlib.util.spec_from_file_location('under', Path(__file__).resolve().parents[1]/'E-204/orthogonal_service.py')
u = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = u
spec.loader.exec_module(u)
Box, sweep = u.Box, u.sweep
EPS = 1e-9


def jaw(face, left):
    # Independently guided/clamped roots below z=-49 are an explicit boundary.
    # No resident distal bearing or free rigid tie between independent blades.
    tip = (face-.4, face) if left else (face, face+.4)
    blade = (face-1.4, face) if left else (face, face+1.4)
    return [Box(tip,(1.5,1.85),(-4.8,-3.6)),
            Box(blade,(1.5,1.85),(-49,-4.8))]


def gate(dz=0, local=False):
    # E-204 had a .1-mm web/spine disconnect and zero tang/spine clearance.
    # Extend webs to lowered spine; .30 nominal tang-bottom clearance.
    end=2.34 if local else 2.54
    return [Box(x,(1.,1.25),(-4.8+dz,-3.6+dz))
            for x in ((-end,-1.5),(-.5,end))] + [
        Box((-end,end),(1.,1.25),(-5.4+dz,-4.8+dz))]


def area(q, nose=0, rack=0):
    island=u.slider(q)[0]
    tooth=Box((.4+rack,1.2+rack),(-.8,.8),(0,2))
    return max(0,min(island.x[1]+nose,tooth.x[1])-max(island.x[0],tooth.x[0])) * \
        max(0,min(island.y[1],tooth.y[1])-max(island.y[0],tooth.y[0]))


def geometry():
    count=0
    obstacles=u.frame()+[Box((.4,2.2),(-.8,.8),(-42,42.2))]
    # Adjacent fixed rows/sites, including all rack heights via swept envelopes.
    for x,y in product((-u.P,0,u.P),repeat=2):
        if x or y:
            obstacles += [b.move(x=x,y=y) for b in u.frame()]
            obstacles += [Box((.4+x,2.2+x),(-.8+y,.8+y),(-42,42.2))]
    # Full permitted face ranges include bounded tab translation and q.
    # Insertion at open pose; subsequent contact search / command is horizontal.
    for left,openface,lo,hi in ((True,-1.85,-2.15,-.9),(False,-.15,-1.55,-.15)):
        for a in jaw(openface,left):
            for b in obstacles:
                assert not sweep(a.grow(.1).move(z=-50),b.grow(.05),(0,0,50))
                count+=1
        for a in jaw(lo,left):
            for b in obstacles+gate(-1.5):
                assert not sweep(a.grow(.1),b.grow(.05),(hi-lo,0,0)), (a,b)
                count+=1
    # Shared gate stays in a distinct y lane even while adaptive jaws overlap.
    for a in gate():
        for b in obstacles+jaw(-1.85,True)+jaw(-.15,False):
            assert not sweep(a.grow(.05),b.grow(.05),(0,0,-1.5)),(a,b)
            count+=1
    # Connected finite gate at closed state, not disconnected ideal webs.
    assert all(a.z[0]==gate()[-1].z[1] for a in gate()[:2])
    inherited_gap=u.comb()[0].z[0]-u.comb()[-1].z[1]
    assert inherited_gap>0
    assert abs(inherited_gap-.1)<EPS
    for q in (-.2,0,.2):
        for a in gate():
            for b in u.slider(q):
                # Intended slot contacts use explicit correlated corners below.
                assert not sweep(a,b,(0,0,-1.5))
    # Actual unilateral jaw-face contact; opposite parts never penetrate.
    for q in (-.75,-.35,0,.35):
        for a in jaw(-1.3+q,True)+jaw(-.7+q,False):
            for b in u.slider(q):
                assert a.overlap(b)==0
        for a in u.slider(-.75):
            for b in gate(-1.5):
                assert not sweep(a.grow(.05),b.grow(.05),(1.1,0,0))
    # Conservative rank extrema, including open right jaw and retracted left.
    gap=u.P+(-2.15-1.4)-(-.15+1.4)-.2
    assert gap>0
    return dict(expanded_sweeps=count,rank_gap_mm=gap,
                inherited_disconnected_gate_gap_mm=inherited_gap,
                repaired_spine_tang_gap_mm=.3,
                blade_span_mm=45.4,tip_thickness_mm=.4,blade_width_mm=1.4)


def corners():
    # comb datum and left/right tab/slot errors are reused through all phases.
    # Common tab translation is NOT an independent retained-q error as well.
    mins={'acquisition':1e9,'area':1e9,'reseat_gap':1e9,'command_clearance':1e9}
    cases=0
    for c,sl,sr,t,n,r,j,d in product((-.05,.05),repeat=8):
        qlo=-.2+c+sl-t; qhi=.2+c+sr-t
        for q in (qlo,qhi):
            l=-1.3+t+q; h=-.7+t+q
            mins['acquisition']=min(mins['acquisition'],l-(-1.85+j+d),(-.15+j+d)-h)
            mins['area']=min(mins['area'],area(q,n,r))
            assert l<=h and area(q,n,r)>0
            # Contact-following search stops at physical faces, then roots lock.
            # q does not need to recenter. Traverse every finite contact state.
            for k in range(17):
                f=k/16
                lf=(-1.85+j+d)*(1-f)+l*f
                rf=(-.15+j+d)*(1-f)+h*f
                assert lf<=l+EPS and rf>=h-EPS
            # changed cell: separate rack load-head boundary before q retracts;
            # unchanged cells hold acquired q. Re-seat to q=0 with load head on.
            mins['reseat_gap']=min(mins['reseat_gap'],(-1.3+t)-(-1.5+c+sl),
                                   (-.5+c+sr)-(-.7+t))
            mins['command_clearance']=min(mins['command_clearance'],
                                         .4+r-(.9+n-.75))
            cases+=1
    assert abs(mins['acquisition']-.15)<EPS
    assert abs(mins['area']-.02)<EPS
    assert abs(mins['reseat_gap']-.05)<EPS
    assert abs(mins['command_clearance']-.15)<EPS
    return dict(cases=cases,**mins,nominal_area_mm2=area(0))


def sequence(n):
    """Finite poses + interface conditions, not a fictitious physical load-head."""
    # One coherent adverse row: c=sl=-.05,t=.05,n=-.05,r=.05 => q=-.35.
    q=[-.35]*40
    phase=[]
    minimum=1e9
    def verify(name,gate_on,jaws_on,rack_head=False):
        nonlocal minimum
        for i in range(40):
            a=area(q[i],-.05,.05)
            supported=(i==0 and rack_head) or (a>EPS and (gate_on or jaws_on))
            assert supported,(name,i,a)
            if i: minimum=min(minimum,a)
        phase.append(name)
    verify('arrive',True,False)
    verify('acquire physical tang faces',True,True)
    verify('root locks engaged',True,True)
    verify('open comb',False,True)
    verify('changed rack taken by external load head',False,True,True)
    for k in range(n+1):
        q[0]=-.35-.4*k/n
        verify('retract changed slider',False,True,True)
    # Granted rack head holds throughout any 0..40-mm rack move; no load-head
    # hardware invented here. Slider withdrawal clearance proved in corners().
    for k in range(n+1):
        q[0]=-.75+.75*k/n
        verify('reseat changed slider',False,True,True)
    verify('close comb before jaw departure',True,True,True)
    verify('transfer/prove rack load',True,True)
    verify('open jaws and depart',True,False)
    # Jam/failure controls: release permission demands EVERY physical restraint.
    restraints=[True]*40; restraints[17]=False
    assert not all(restraints) # jaw failure -> comb stays closed, supported.
    # Gate closure failure: retaining jaws must persist; no departure permitted.
    gate_closed=False
    depart=gate_closed and all(area(v,-.05,.05)>0 for v in q)
    assert not depart
    # One lost unchanged jaw after release leaves the E-204 escape available.
    assert area(-.55)==0
    return dict(min_unchanged_area_mm2=minimum,changed_final_q=q[0],
                acquisition_failure='retain closed gate; abort',
                gate_failure='retain every jaw and changed rack head; no departure',
                false_acceptance_or_power_loss='unsafe unless actual passive root retention and load proof supplied')


def local_gate():
    # Finite split gate + stem + crossbolt. Nominal fit control only; no free
    # robust latch, actuator, return or bolt retention is credited.
    stem=[Box((-2.3,-1.9),(1.,1.25),z) for z in ((-10,-8.2),(-7.8,-5.4))]
    stem += [Box(x,(1.,1.25),(-8.2,-7.8)) for x in ((-2.3,-2.25),(-1.95,-1.9))]
    pin=Box((-2.2,-2.),(.5,1.3),(-8.2,-8.0))
    # Back guide with bolt window, front cheek, side cheeks; tie to negative-y
    # grounded post. Widths are explicit and include unqualified .05 ligaments.
    guide=[Box((-2.4,-1.8),(.6,.95),z) for z in ((-11.5,-8.2),(-7.8,-7.))]
    guide += [Box((-2.4,-1.8),(1.3,1.4),(-11.5,-7.))]
    guide += [Box(x,(.6,1.4),(-11.5,-7.)) for x in ((-2.4,-2.35),(-1.85,-1.8))]
    guide += [Box((-2.5,-1.7),(-2.35,.95),(-9.5,-9.))]
    parts=gate(local=True)+stem
    count=0
    for a in parts:
        for b in guide:
            assert not sweep(a,b,(0,0,-1.5)), (a,b)
            count+=1
        assert not sweep(pin,a,(0,-.5,0))
    retracted=pin.move(y=-.5)
    for a in parts:
        assert not sweep(a,retracted,(0,0,-1.5))
    # Pin bottom rests on lower back-guide lip at z=-8.2; stem catches after
    # .20 mm descent, with .7-mm tang/web overlap. Pin y retention remains owed.
    assert pin.z[0]==guide[0].z[1]
    caught=max(a.move(z=-.21).overlap(pin) for a in stem)
    assert caught>0
    # Acquired jaws never collide with finite guide/bolt/grounding construction.
    for left,lo,hi in ((True,-2.15,-.9),(False,-1.55,-.15)):
        for a in jaw(lo,left):
            for b in guide+[pin]:
                assert not sweep(a,b,(hi-lo,0,0))
    for a in parts:
        for dx in (-u.P,u.P):
            for b in parts:
                assert not sweep(a.grow(.05),b.move(x=dx).grow(.05),(0,0,-1.5))
                count+=1
    assert area(-.35,-.05,.05)>0
    # Side stem/guide nominal clearance .05; two adverse .05 surfaces consume .1.
    return dict(sweeps=count,segment_gap_mm=u.P-4.68-.1,
                closed_bolt_catch_witness_mm3=caught,
                guide_nominal_gap_mm=.05,guide_adverse_gap_mm=.05-.1,
                smallest_stem_ligament_mm=.05,
                retained_z_channels=6400,extra_channels_over_shared=6400-160,
                bolt_y_retention_and_actuation_constructed=False,
                unchanged_reusable_jaws_required=0,assembly_advantage_demonstrated=False)


def ramp_holdout():
    # Finite contact holdout: replace only nose top x=q+.15..q+.9 by a
    # downward-to-right plane z=-tan(a)*(x-q-.15). A horizontal tooth's left
    # corner rides on it; its remaining bottom never penetrates the lower ramp.
    # This constructs the horizontal force scenario, not a sourced defect prior.
    m=math.tan(math.radians(2)); rack_left=.45; nose_error=-.05
    min_gap=1e9
    for q in (-.35,-.375,-.399):
        right=.9+nose_error+q
        assert right>rack_left
        zcontact=-m*(rack_left-q-.15)
        for k in range(17):
            x=rack_left+(right-rack_left)*k/16
            top=-m*(x-q-.15)
            min_gap=min(min_gap,zcontact-top)
            assert top<=zcontact+EPS
    # Contact ends at q=-.40, matching the adverse .05-mm overlap at q=-.35.
    return dict(angle_deg=2,normal_ratio_horizontal_to_vertical=m,
                minimum_tooth_to_ramp_gap_mm=min_gap,
                evidence='finite frictionless corner/ramp construction; no friction prior')


def mechanics():
    # More favorable constant wide blade upper bound versus actual thin tip.
    # Clamp at z=-49, distributed contact resultant z=-4.05 => L=44.95.
    # Piecewise bending compliance: integral (L-s)^2/(E I(s)) ds.
    L=44.95; tip=.75; w=1.4; t=.35
    I=t*w**3/12; It=t*.4**3/12
    rows=[]
    for E in (1000,3000,200000):
        compliance=(L**3-tip**3)/(3*E*I)+tip**3/(3*E*It)
        k=1/compliance
        favorable=3*E*I/L**3
        # Partial retained-state overlap only .05; allocate .02 root lost motion.
        force_limit=k*(.05-.02)
        # Unit-load virtual work / numerical quadrature independent check.
        N=20000; ds=L/N
        numerical=sum((L-(i+.5)*ds)**2/(E*(I if (i+.5)*ds<L-tip else It))*ds
                      for i in range(N))
        assert abs(numerical/compliance-1)<2e-5
        rows.append(dict(E_MPa=E,k_N_per_mm=k,favorable_k=favorable,
                         force_before_overlap_loss_N=force_limit,
                         recentered_force_limit_N=k*(.4-.02),
                         minimum_area_at_1N_2deg_mm2=max(0,.05-.02-math.tan(math.radians(2))/k)*.4))
    # Static slope creates horizontal force without claiming friction always
    # slides. Frictionless tilted contact is an explicit competing model.
    loads=[]
    for W,angle in product((.1,1,10),(0,.25,2)):
        F=W*math.tan(math.radians(angle))
        loads.append(dict(W_N=W,angle_deg=angle,horizontal_N=F,
                          support_margin_mm=.05-.02-F/rows[-1]['k_N_per_mm']))
    F=math.tan(math.radians(2))
    threshold=rows[-1]['force_before_overlap_loss_N']
    assert 2*threshold<F # even optimistic bilateral preload doubles k only
    # A limiter tripping below restraint load forfeits support; one above the
    # overlap-loss threshold allows loss before isolation. No scalar trip works.
    assert not (F<threshold)
    return dict(blades=rows,load_cases=loads,root_stress_MPa_per_N=6*L/(t*w*w),
                blade_load_case='cantilever tip force, initially closed face; opposite jaw unloads',
                local_limiter_window_1N_2deg_N=[F,threshold],
                optimistic_preloaded_window_N=[F,2*threshold],
                backlash_sensitivity=[dict(lost_motion_mm=b,one_blade_limit_N=rows[-1]['k_N_per_mm']*max(0,.05-b),
                    two_preloaded_limit_N=2*rows[-1]['k_N_per_mm']*max(0,.05-b)) for b in (0,.01,.02,.05)],
                one_jam_common_limit_factor=40,
                friction_recenter_force_scenarios_N=[mu*W for W,mu in product((1,10),(.05,.2,.5))],
                power_off_retention_constructed=False)


def main():
    seq=sequence(16)
    for n in (1,64,256): assert sequence(n)==seq
    result=dict(evidence='finite geometry + bounded elastic falsification; self-review',
                geometry=geometry(),corners=corners(),sequence=seq,
                local_control=local_gate(),mechanics=mechanics(),ramp=ramp_holdout(),
                scaling=dict(sites=6400,shared_gates=160,
                             blades_for_H_40_80_160=[80,160,320],
                             slot_limits_s=[.15,.30,.60]))
    # Inherited failure control stays a failure after adaptive construction.
    assert not u.takeover()['fixed_open_U_takeover_pass']
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
