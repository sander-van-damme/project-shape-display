"""Finite pin/socket row clutch screens; all inputs are epistemic scenarios.
mm, N, MPa internally; motion converts mm to m. No process probabilities.
Run directly: deterministic corner checks, synthesis and strip budget as JSON.
"""
import itertools
import json
import math


def section(d, slot, pin, e, wall=.4):
    # ±e: each center and full width; stop travel has additional ±e.
    # Slot edge/body/guide dimensions not covered by this box are explicit below.
    gap = (slot-pin)/2
    return dict(d=d,slot=slot,pin=pin,e=e,
        insertion=gap-4*e,
        # Dog width=slot+2*wall, actual width error ±e; two center errors ±e.
        # Engaged stop uncertainty adds e beyond that.
        neighbor=5.08-d-(slot+2*wall)-4*e-.8,
        # Upper boss/cam .8; include engaged stop error beyond the center box.
        cam_overlap=.8-4*e,cam_bypass=d-.8-3*e,
        withdrawn=.4-2*e,engaged=.6-2*e,roof=2.-.4-.6-2*e,
        overtravel_gap=gap+4*e)


def accepted(s):
    return all(s[k]>1e-10 for k in ('insertion','neighbor','cam_overlap',
                                  'cam_bypass','withdrawn','engaged','roof'))


def interval_corners(s):
    e=s['e'];gap=(s['slot']-s['pin'])/2
    insert=[];contacts=[]
    for pin_shift,dog_shift,slot_error,pin_error,stop_error in itertools.product((-e,e),repeat=5):
        actual_gap=gap+(slot_error-pin_error)/2
        insert.append(actual_gap-abs(pin_shift-dog_shift-stop_error))
        # Drive coordinate needed for RIGHT contact at uncertain final stop.
        contacts.append(stop_error+dog_shift+actual_gap-pin_shift)
    return min(insert),min(contacts),max(contacts)


def force_window(s,k,friction_per_foot=.01,detent=.3,allowable=10.,lever=1.):
    # 80 captive z keys on each column bar slide along stationary row rails.
    # All friction may shift coherently. No load sharing in a one-pin jam.
    # Transverse pin bending, not E-077 axial neck capacity. Single-pin jam
    # can receive full column force. Rectangular cantilever sigma=6FL/b^3.
    limit=allowable*(s['pin']-s['e'])**3/(6*lever)
    required=80*friction_per_foot+detent
    # No preload. Minimum compression required to overcome bounded resistance.
    compression=required/k
    contact_range=8*s['e']
    peak=required+k*contact_range
    return dict(k_N_mm=k,foot_drag_N=friction_per_foot,required_N=required,
                peak_N=peak,pin_limit_N=limit,force_reserve_N=limit-peak,
                x_drive_mm=s['d']+s['overtravel_gap']+compression,
                # Pin must be recentered before it can leave a narrow socket:
                # otherwise x spring preload creates extraction friction.
                x_unload_mm=s['overtravel_gap']+compression,
                admissible=peak<limit)


def rest(distance_mm,a):
    return 2*math.sqrt(distance_mm/1000/a)


def budget(s,f,writes,a,other=6.):
    # A chosen stop-and-go row cycle, not the optimal multirow scheduler.
    # prepare old state (worst d), engage z, drive target + overtravel,
    # recenter to target (unload), disengage z. Prior row ended recentered.
    # Required settling/readback/row address costs are omitted, not zero in reality.
    dists=[s['d'],1.,f['x_drive_mm'],f['x_unload_mm'],1.]
    cycle=sum(rest(d,a) for d in dists)
    return dict(writes=writes,a_m_s2=a,cycle_ms=cycle*1000,
                chosen_motion_s=writes*cycle,
                z_only_lower_s=2*writes*rest(1.,a),
                with_other_s=other+writes*cycle,
                strict_pass=other+writes*cycle<30.,
                z_acceleration_needed_24s=16*.001*(writes/24.)**2)


def replay_row(old,new,s):
    """Piecewise rigid pin/socket kinematics, nominal dimensions, no force ODE.
    The compliant actuator can reach endpoint at positive force; it is then
    unloaded/recentered before z extraction. Detent retention is a prerequisite.
    """
    g=(s['slot']-s['pin'])/2;d=s['d']
    q=[v*d for v in old];bar=q.copy();height=-.4
    before=q.copy()
    # Withdrawn preparation may traverse the entire horizontal range.
    assert height<0
    height=.6
    assert all(abs(p-x)<g for p,x in zip(bar,q))
    for j,target in enumerate(new):
        sign=1 if target else -1
        endpoint=target*d
        end_pin=endpoint+sign*g
        start=bar[j]
        # Contact onset and endpoint split the continuous affine paths.
        for t in (0.,.25,.5,.75,1.):
            p=start+(end_pin-start)*t
            pos=min(d,max(0.,p-sign*g)) if target!=old[j] else endpoint
            assert 0<=pos<=d
            assert abs(p-pos)<=g+1e-12
            if target==old[j]: assert pos==before[j]
        q[j]=endpoint;bar[j]=end_pin
    # Relax input back to each slot center. Dog remains at retained endpoint.
    bar=q.copy();height=-.4
    assert q==[v*d for v in new]
    # Direct x/z rectangles: withdrawn pin never overlaps either socket wall.
    def collision(pin_x,top,dog_x):
        pin_box=(pin_x-s['pin']/2,pin_x+s['pin']/2,top-2.,top)
        outer=s['slot']/2+.4;inner=s['slot']/2
        walls=[(dog_x-outer,dog_x-inner,0.,1.6),
               (dog_x+inner,dog_x+outer,0.,1.6)]
        return any(min(pin_box[1],w[1])>max(pin_box[0],w[0])+1e-12
                   and min(pin_box[3],w[3])>max(pin_box[2],w[2])+1e-12 for w in walls)
    for dog in q:
        for x in (-1.,0.,d,d+1.): assert not collision(x,height,dog)
        assert collision(dog+s['slot']/2,.1,dog)  # failed withdrawal is detectable
    return q


def checks(witness):
    # Independent corner construction vs algebra for insertion and endpoint reach.
    cases=0
    for e,d,slot,pin in itertools.product((.05,.1,.2),(1.2,1.5,1.8),
                                         (1.2,1.4,1.6,1.8,1.85,2.),(.6,.8,1.,1.2)):
        s=section(d,slot,pin,e);low,cmin,cmax=interval_corners(s)
        assert math.isclose(low,s['insertion'],abs_tol=1e-12)
        assert math.isclose(cmax,s['overtravel_gap'],abs_tol=1e-12)
        assert math.isclose(cmax-cmin,8*e,abs_tol=1e-12)
        # Neighbor adverse endpoints reconstructed as actual interval edges.
        width=slot+.8
        left_right=d+e+e+(width+e)/2 # travel error, center error, width error
        right_left=5.08-e-(width+e)/2
        assert math.isclose(right_left-left_right-.8,s['neighbor'],abs_tol=1e-12)
        cases+=1
    # All two-cell old/new combinations exercise set/reset/unchanged concurrently.
    maps=0
    for old,new in itertools.product(itertools.product((0,1),repeat=2),repeat=2):
        replay_row(old,new,witness);maps+=1
    # Exact limiting case and independently integrated bang-bang travel.
    assert rest(0.,100.)==0.
    t=rest(1.,100.);assert math.isclose(100.*(t/2)**2,.001)
    # Wide fit failure and force amplification are deliberate negative controls.
    assert not accepted(section(1.5,1.4,.6,.2))
    assert not force_window(witness,8.)['admissible']
    assert not force_window(witness,4.,friction_per_foot=.03)['admissible']
    return dict(corner_sections=cases,two_cell_maps=maps)


def main():
    witness=section(1.2,1.85,1.,.1)
    assert accepted(witness)
    synth=[]
    for e in (.05,.1,.2):
        population=[section(d,slot,pin,e) for d,slot,pin in itertools.product(
                    (1.2,1.5,1.8),(1.2,1.4,1.6,1.8,1.85,2.),(.6,.8,1.,1.2))]
        synth.append(dict(e=e,total=len(population),survivors=[s for s in population if accepted(s)],
            rejection_counts={k:sum(s[k]<=1e-10 for s in population) for k in
                ('insertion','neighbor','cam_overlap','cam_bypass','withdrawn','engaged','roof')}))
    forces=[force_window(witness,k,f) for k,f in itertools.product((.1,.5,1.,2.,4.,8.),(.005,.01,.03))]
    f=force_window(witness,.5,friction_per_foot=.005)
    print(json.dumps(dict(checks=checks(witness),witness=witness,synthesis=synth,
        forces=forces,slender_pin=force_window(section(1.5,1.4,.6,.1),1.),budgets=[budget(witness,f,w,a) for w,a in itertools.product(
            (320,800,3360),(20.,100.))],
        force_mass_acceleration=[dict(moving_mass_g=m,upper_a_m_s2=(f['pin_limit_N']-f['required_N'])/(m/1000))
                                 for m in (5.,20.,50.)]),indent=2))

if __name__=='__main__':main()
