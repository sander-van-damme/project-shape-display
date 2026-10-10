"""E-129: finite rigid contact counterexamples, mm/N/rad. Python 3 + NumPy.
No process distribution, strength, dynamic arrest or complete machine claim.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location(
    'previous', Path(__file__).parents[1]/'E-128'/'docking_arrest.py')
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
p = previous.p
RACE, ROLLER, PEG, ANGLE = 5., .6, .15, math.radians(5.)
X = (RACE-ROLLER)*math.sin(ANGLE)
Y = (RACE-ROLLER)*math.cos(ANGLE)
FLAT = Y-ROLLER
STUD_R, STUD_ORBIT, SLOT_HALF = .25, 2.6, .37
DRIVE_ANGLE = math.asin((SLOT_HALF-STUD_R)/STUD_ORBIT)
SPRING_PRELOAD, SPRING_K = 0., .5  # N, N/mm; uncalibrated design bounds


def clip(poly, axis, bound, sign):
    out = []
    for a, b in zip(poly, np.roll(poly, -1, axis=0)):
        da, db = sign*(a[axis]-bound), sign*(b[axis]-bound)
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            out.append(a+(b-a)*da/(da-db))
    return np.array(out)


def cam_polygon(n):
    t = np.linspace(0, 2*math.pi, n, endpoint=False)
    cam = 4.3*np.c_[np.cos(t), np.sin(t)]
    return clip(clip(cam, 1, FLAT, -1), 1, -FLAT, 1)


def released_geometry(delta):
    # Positive input lead: top peg pushes the load-blocking roller toward pocket
    # centre. Roller remains tangent to finite output flat. Ring is an exact circle.
    peg = p.rotate([[X+ROLLER+PEG, Y]], delta)[0]
    vertical = peg[1]-Y
    dx = math.sqrt((ROLLER+PEG)**2-vertical**2)
    center = np.array([peg[0]-dx, Y])
    q = X-center[0]
    ring_gap = RACE-ROLLER-float(np.linalg.norm(center))
    stud = p.rotate([[STUD_ORBIT, 0]], delta)[0]
    return dict(delta_rad=delta, roller_center_mm=center.tolist(),
                roller_withdrawal_mm=q, ring_gap_mm=ring_gap,
                peg_contact_residual_mm=float(np.linalg.norm(center-peg))-ROLLER-PEG,
                drive_flank_gap_mm=SLOT_HALF-STUD_R-stud[1],
                resisting_flank_gap_mm=SLOT_HALF-STUD_R+stud[1],
                spring_force_N=SPRING_PRELOAD+SPRING_K*q,
                released_flat_normal_N=(SPRING_PRELOAD+SPRING_K*q)*vertical/dx,
                released_cam_aiding_torque_Nmm=(SPRING_PRELOAD+SPRING_K*q)*(Y-center[0]*vertical/dx))


def equilibrium(torque, alpha, push=0.):
    # Seated, zero spring preload, frictionless peg. N is outer normal;
    # roller moment balance equates tangentials f; B is flat normal.
    x = (RACE-ROLLER)*math.sin(alpha)
    a = (RACE-ROLLER)*math.cos(alpha)-ROLLER
    sn, cs = math.sin(alpha), math.cos(alpha)
    matrix = np.array([[-sn, 1+cs], [x*cs, x*sn-a]])
    normal, f = np.linalg.solve(matrix, [push, torque])
    flat_normal = normal*cs+f*sn
    residual = [-normal*sn+f*(1+cs)-push,
                -normal*cs-f*sn+flat_normal,
                x*flat_normal-a*f-torque]
    assert max(abs(v) for v in residual) < 1e-10
    return np.array([normal, flat_normal, f])


def released_capacity(delta, mu_peg, mu_flat):
    # No race contact. Include BOTH peg and flat friction and cam spring reaction.
    # Peg force -P(c,s)+Q(-s,c); roller moment gives Q=-f.
    g = released_geometry(delta)
    peg = p.rotate([[X+ROLLER+PEG,Y]],delta)[0]
    center = np.array(g['roller_center_mm'])
    cs,sn = (peg-center)/(ROLLER+PEG)
    spring = g['spring_force_N']
    # x/y balance gives f=(P*c-S)/(1+s), B=P-S*c/(1+s).
    def forces(push):
        return np.array([push, push-spring*cs/(1+sn), (push*cs-spring)/(1+sn)])
    def margins(v):
        push, b, f = v
        return np.array([push,b,mu_peg*push-f,mu_peg*push+f,mu_flat*b-f,mu_flat*b+f])
    base = margins(forces(0.))
    slope = margins(forces(1.))-base
    lo,hi = 0.,math.inf
    for a,b in zip(slope,base):
        if a>1e-12: lo=max(lo,-b/a)
        elif a < -1e-12: hi=min(hi,-b/a)
        else: assert b>=-1e-12
    assert lo<=hi+1e-12 and math.isfinite(hi)
    capacity=[]
    for push in [lo,hi]:
        _,normal,f = forces(push)
        assert min(margins(forces(push)))>=-1e-12
        capacity.append(center[0]*normal-FLAT*f-Y*spring)
    return dict(mu_peg=mu_peg,mu_flat=mu_flat,
                max_resisting_torque_Nmm=max(capacity),peg_normal_range_N=[lo,hi])


def release_limit(torque, alpha, mu_ring, mu_flat):
    # Zero-preload return spring is relaxed at seated contact.
    # Each Coulomb cone inequality is affine in input extraction force P.
    # Find the entire feasible P>=0 interval analytically (no force-step grid).
    base = equilibrium(torque, alpha)
    slope = equilibrium(torque, alpha, 1.)-base
    def margins(v):
        n, b, f = v
        return np.array([n, b, mu_ring*n-f, mu_ring*n+f,
                         mu_flat*b-f, mu_flat*b+f])
    intercept, gradient = margins(base), margins(slope)
    if min(intercept) < -1e-10:
        return {'holds_at_zero_push': False, 'release_limit_N': None}
    upper = min([-b/a for a,b in zip(gradient,intercept) if a < -1e-12], default=math.inf)
    # Infinity = rigid static jam equilibrium remains possible for every P;
    # it is not a strength prediction or a proof against alternate unloading.
    return {'holds_at_zero_push': True,
            'release_limit_N': None if math.isinf(upper) else upper,
            'unbounded_sticking_equilibrium': math.isinf(upper),
            'normal_at_zero_N': base[:2].tolist(),
            'normal_at_20N_push_N': equilibrium(torque, alpha, 20.)[:2].tolist(),
            'still_static_at_20N': bool(upper >= 20.)}


def dimensional_cases():
    cases = []
    for bias in [-.05,-.025,0,.025,.05]:
        a = FLAT+bias
        ratio = (a+ROLLER)/(RACE-ROLLER)
        if ratio > 1:
            cases.append({'common_flat_bias_mm':bias,
                          'impossible_radial_fit_mm':a+2*ROLLER-RACE})
        else:
            angle = math.acos(ratio)
            cases.append({'common_flat_bias_mm':bias,
                          'wedge_angle_deg':math.degrees(angle),
                          'zero_spring_min_mu':math.tan(angle/2),
                          'zero_spring_normal_at_3_27N_N':3.27*p.R/(RACE*math.tan(angle/2))})
    return cases


def positive_stops():
    # Two finite E-127 collars in separate axial planes, B shifted half an index.
    # Ground-fixed bolts must overlap FULL insertion before releasing loaded A.
    half_index = math.pi/12
    widths = [p.fit_window(lambda t:p.lock_margin(t,segments=n), math.pi/6)
              for n in [256,1024,4096]]
    assert 2*widths[-1] < half_index
    count = sum(p.lock_margin(t,segments=256)>=0 and
                p.lock_margin(t-half_index,segments=256)>=0
                for t in np.linspace(0, math.pi/6, 721))
    assert count == 0
    return {'full_insertion_halfwindow_deg':list(map(math.degrees,widths)),
            'simultaneous_full_insertions_in_721_phases':count,
            'separation_between_insertion_windows_rad':half_index-2*widths[-1],
            'rack_equivalent_between_windows_mm':p.R*(half_index-2*widths[-1]),
            'both_retracted_nose_to_collar_clearance_mm':3.5-3.4,
            'scope':'No overlap-first fixed-bolt transfer; not a bound on partial capture or all escapements.'}


def geometry_checks():
    gaps = []
    for n in [64,256,1024]:
        cam = cam_polygon(n)
        assert abs(cam[:,1].max()-FLAT) < 1e-12
        # Distance to the generated flat edge through x=X, not a scalar envelope.
        edges = np.roll(cam,-1,axis=0)-cam
        center = np.array([X,Y])
        t = np.clip(np.sum((center-cam)*edges,axis=1)/np.sum(edges*edges,axis=1),0,1)
        gap = np.linalg.norm(center-(cam+t[:,None]*edges),axis=1).min()-ROLLER
        gaps.append(float(gap))
        assert abs(gap)<1e-12
    # Check every nominal peg/roller state up to actual positive stud contact.
    for delta in np.linspace(0,DRIVE_ANGLE,257):
        g = released_geometry(delta)
        assert abs(g['peg_contact_residual_mm'])<1e-12
        assert g['ring_gap_mm']>=-1e-12
        assert g['drive_flank_gap_mm']>=-1e-12
        stud = p.rotate([[STUD_ORBIT,0]],delta)[0]
        assert 2.1 < stud[0]-STUD_R < stud[0]+STUD_R < 3.1
        for sign in [-1,1]:
            peg = p.rotate([[X+ROLLER+PEG,sign*Y]],delta)[0]
            assert np.linalg.norm(peg)+PEG<RACE
            assert abs(peg[1])-PEG>FLAT # clears the actual flat body
    # Explicit finite spring seat/envelope, no qualified spring stiffness.
    # Spring along x from -1 to X-r; radius .08, free length adds preload/k.
    assert math.hypot(-1,Y)+.08<RACE and Y-.08>FLAT
    assert -1 < released_geometry(DRIVE_ANGLE)['roller_center_mm'][0]-ROLLER
    return {'cam_contact_gap_convergence_mm':gaps,
            'ring_inner_outer_radius_mm':[RACE,5.7],
            'roller_radius_mm':ROLLER,'flat_height_mm':FLAT,
            'roller_centers_mm':[[X,Y],[X,-Y]],
            'spring_installed_length_mm':X-ROLLER+1,
            'spring_free_length_mm':X-ROLLER+1+SPRING_PRELOAD/SPRING_K,
            'release_sample':released_geometry(.02),
            'at_positive_drive_contact':released_geometry(DRIVE_ANGLE),
            'angular_drive_half_play_rad':DRIVE_ANGLE}


def independent_control():
    # Two permanently applied opposing 4x10-mm pads on EACH local linear rack
    # driving its positive head gear. Same explicit E-128 brake geometry.
    return [{'mu':mu,'normal_each_N':normal,'site_load_N':load,
             'static_margin_N':2*mu*normal-load,
             'drag_at_300mm_s_W':2*mu*normal*.3,
             'raising_drive_force_N':load+2*mu*normal,
             'lowering_drive_force_N':2*mu*normal-load}
            for mu,normal,load in itertools.product([.05,.1,.3],[80.,100.],[3.27,10.])]


def main():
    geometry = geometry_checks()
    torque = 3.27*p.R
    # Independent zero-preload analytical solution vs assembled force balance.
    n,b,f = equilibrium(torque,ANGLE)
    q = math.tan(ANGLE/2)
    assert abs(n-torque/(RACE*q))<1e-10 and abs(n-b)<1e-10
    assert abs(f/n-q)<1e-12
    cases = []
    for load,angle,mu_o,mu_f in itertools.product([1.,3.27,10.],[3.,5.,8.],[.05,.1,.3],[.05,.1,.3]):
        cases.append(dict(load_N=load,angle_deg=angle,mu_ring=mu_o,mu_flat=mu_f,
                          **release_limit(load*p.R,math.radians(angle),mu_o,mu_f)))
    assert not release_limit(torque,ANGLE,0.,0.)['holds_at_zero_push']
    assert release_limit(torque,ANGLE,.05,.05)['release_limit_N']<1.
    assert release_limit(torque,ANGLE,.3,.3)['unbounded_sticking_equilibrium']
    release_friction_cases = [released_capacity(.02,mp,mf)
                              for mp,mf in itertools.product([0.,.1,.3],[.05,.1,.3])]
    assert max(c['max_resisting_torque_Nmm'] for c in release_friction_cases)<0
    released = geometry['release_sample']
    assert released['ring_gap_mm']>0 and released['drive_flank_gap_mm']>0
    # With no race contact, roller moment balance forces flat friction to zero.
    # Peg/flat/spring equilibrium then gives the reported positive (aiding)
    # output torque, including the spring reaction on the cam-mounted seat.
    assert released['released_cam_aiding_torque_Nmm'] > 0
    # Exact unilateral drive contact: aiding output needs negative-lead slot wall.
    # Top release occurs at positive lead, so no quasistatic lowering support
    # from either stud wall in this open interval. Opposite roller resists -T only.
    # Input removal: optimistic isolated spring/roller return with output FIXED.
    disp = released['roller_withdrawal_mm']/1000
    stiffness, mass = SPRING_K*1000, .0005
    return_time = math.acos(SPRING_PRELOAD/(SPRING_PRELOAD+stiffness*disp))/math.sqrt(stiffness/mass)
    wl = p.fit_window(p.lock_margin,math.pi/6)
    routing = previous.routing()
    result = {'evidence':'finite geometry + Coulomb static cones; counterexample, no admitted machine',
              'geometry':geometry,'force_cases':cases,'dimensional_cases':dimensional_cases(),
              'released_friction_capacity':release_friction_cases,
              'nominal_force':dict(torque_Nmm=torque,zero_preload_normal_N=n,required_mu=q,
                                  low_mu=release_limit(torque,ANGLE,.05,.05),
                                  high_mu=release_limit(torque,ANGLE,.3,.3)),
              'two_site_access':dict(heights_mm=[5*p.R*math.pi/6-p.R*wl,15*p.R*math.pi/6-p.R*wl],
                                    original_routing=routing,
                                    head_ring_pair_clearance_mm=(5.08+2*p.R)-2*5.7,
                                    ring_axial_interval_mm=[9.,10.2],peg_disk_interval_mm=[10.4,11.4]),
              'positive_fixed_stops':positive_stops(),
              'independent_permanent_drag_control':independent_control(),
              'input_removed_isolated_return':dict(roller_mass_kg=mass,first_contact_ms=return_time*1000,
                  spring_work_Nmm=SPRING_PRELOAD*disp*1000+.5*SPRING_K*(disp*1000)**2,
                  scope='fixed output, undamped, no contact friction during return; not an arrest bound'),
              'input_held_output_rejam_travel_from_0_02_rad_mm':p.R*.02,
              'scope':'Stud load sign and finite release gap reject controlled overhauling lowering in this topology. Rejam dynamics unknown.'}
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
