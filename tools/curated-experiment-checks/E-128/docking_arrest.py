"""Finite contact counterexamples, mm/N/s. Python3 + numpy; no process priors.
E-127 supplies the already-checked involute/positive-lock sections.
This constructs routed local access and contact cuts, NOT an admitted machine.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('prior', Path(__file__).parents[1]/'E-127'/'rotary_transfer.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
R, PITCH = p.R, 5.08


def rectangle_distance(cx, cz, rect):
    x0,x1,z0,z1 = rect
    return math.hypot(max(x0-cx,0,cx-x1),max(z0-cz,0,cz-z1))


def routing():
    # Mirrored OUTWARD pinions, unlike E-127's same-side straight-through bank.
    # Top centers x=0,5.08. Pitch lines x=0,5.08. Meshes face inward.
    axes = [-R, PITCH+R]
    shafts = [(x,-1.2,7.2,.8) for x in axes] # axis x,y0,y1,r; z=0
    backs = [(0.5,1.3), (PITCH-1.3,PITCH-.5)]
    gaps=[]
    for h0,h1 in itertools.product([0,40],repeat=2):
        for x,y0,y1,rad in shafts:
            for (a,b),h in zip(backs,[h0,h1]):
                gaps.append(rectangle_distance(x,0,(a,b,-48+h,8+h))-rad)
    # Both racks include z=0 at every intermediate h, so endpoint check is exact.
    assert min(gaps)>0
    # Actual gear polygon extents plus body intervals; not just a diameter test.
    g0=p.gear(512)+[axes[0],0]
    g1=p.gear(512)*[-1,1]+[axes[1],0]
    assert g0[:,0].max()<g1[:,0].min()
    # Head gear rack uses the same conjugate section rotated through 90 degrees.
    # Shared bar lies at z=3.2..4.9, y=6..9.2; collar y=1.4..2.6,
    # front bearing y=2.8..3.8; docking faces y=4..5.2.
    # Head gear slides axially from y=6..7.2 to 7.5..8.7 (1.5-mm undock),
    # remaining inside bar width without inventing a splined telescoping joint.
    assert 6 <= 7.5 and 8.7 <= 9.2
    # A 70-mm toothed bar covers both head centers over x-motion +/-20 mm.
    assert 70 > (axes[1]-axes[0])+40+2*4
    # Naive repeat of outward pairs: next pair left shaft is only 2.12 mm away.
    adjacent_axis = 2*PITCH-R
    return {'top_centers_x_mm':[0,PITCH], 'pinion_axes_x_mm':axes,
            'shaft_to_backing_min_clearance_mm':min(gaps),
            'gear_polygon_separation_mm':float(g1[:,0].min()-g0[:,0].max()),
            'local_width_mm':axes[1]-axes[0]+8,
            'two_top_width_mm':2*PITCH,
            'naive_pair_repeat_axis_separation_mm':abs(axes[1]-adjacent_axis),
            'naive_repeat_root_disk_overlap_mm':2*(R-1.25*p.M)-abs(axes[1]-adjacent_axis),
            'scope':'finite two-site shafts clear; same-tier repeated pairs collide; no board routing acceptance'}


def annulus(n, pressure='uniform'):
    # Single axial face, inner/outer radius 1.6/3.4 mm. Equal angle sectors;
    # integrate area strips exactly, evaluate torque at midpoint (converges).
    ri,ro=1.6,3.4
    edges=np.linspace(ri,ro,n+1)
    mids=(edges[1:]+edges[:-1])/2
    areas=math.pi*(edges[1:]**2-edges[:-1]**2)
    weights=areas if pressure=='uniform' else areas/mids # uniform wear p~1/r
    return float(np.dot(weights,mids)/sum(weights))


def torque_capacity(mu, normal, radius):
    return mu*normal*radius


def spring_brake(dt, mass=.02, stiffness=2000., gap=.0002):
    # SI isolated pad: spring force preload-k*x, no damping. Favourable earliest
    # contact, no electromagnetic lag, then instant full friction (optimistic).
    preload=100.+stiffness*gap # 100 N remains at contact, matching drag case
    t=x=v=0.
    while x<gap:
        a=(preload-stiffness*x)/mass
        x+=v*dt+.5*a*dt*dt
        v+=a*dt
        t+=dt
    exact=math.acos(1-gap*stiffness/preload)/math.sqrt(stiffness/mass)
    return t,exact


def contact_trace(mu=.3, normal=20., load=3.27):
    # Positive lock/dog contacts inherited exactly from E127. Two unequal retained
    # heights. Move site 0 one index, site 1's dock remains OUT and lock loaded.
    wl=p.fit_window(p.lock_margin, math.pi/6)
    wd=p.fit_window(lambda a:p.dock_margin(a,12),math.pi/6)
    step=math.pi/6
    h1=15*R*step-R*wl
    seq=[('parked',5*step-wl,False,True,False),
         ('face_or_dog_inserted',5*step-wl,True,True,False),
         ('drive_load_flank',5*step-wl,True,True,True),
         ('lift_to_unload_bolt',5*step,True,True,True),
         ('bolt_out',5*step,True,False,True),
         ('half_step',5.5*step,True,False,True),
         ('target_bolt_in',6*step,True,True,True),
         ('ground_seated',6*step-wl,True,True,True),
         ('head_unloaded',6*step-wl,True,True,False),
         ('undocked',6*step-wl,False,True,False)]
    result=[]
    for name,theta,dock,bolt,flank in seq:
        ground=bolt and abs(p.lock_margin(theta))<1e-8
        assert not bolt or p.lock_margin(theta)>-1e-8
        if dock:
            assert p.dock_margin(wd if flank else 0,12)>-1e-8
        dog=dock and flank
        friction=dock and torque_capacity(mu,normal,annulus(512))>=load*R
        # Shared continuously applied double-pad linear brake on driving bar.
        # At z=3.6 the rack transmits T/R; two faces, N=100 N each, mu=.1.
        brake=2*.1*100>=load
        result.append({'state':name,'heights_mm':[R*theta,h1],
                       'unselected_ground_contact':True,
                       'selected_ground_contact':ground,
                       'indexed_static_support_if_bar_connected':ground or (dog and brake),
                       'face_static_support_if_bar_connected':ground or (friction and brake)})
    assert all(s['indexed_static_support_if_bar_connected'] for s in result)
    return result


def main():
    ri,ro=1.6,3.4
    exact=2*(ro**3-ri**3)/(3*(ro**2-ri**2))
    conv=[annulus(n) for n in [16,64,256,1024]]
    assert abs(conv[-1]-exact)<1e-6
    assert abs(annulus(64,'wear')-(ri+ro)/2)<1e-12
    caps=[]
    for mu,n,f in itertools.product([.05,.1,.2,.3],[10.,20.,40.],[1.,3.27,10.]):
        # Contact-pressure uncertainty: any nonnegative pressure must put its
        # mean radius inside [ri,ro], independent of pressure model/tilt.
        caps.append({'mu':mu,'normal_N':n,'load_N':f,
                     'torque_needed_Nmm':R*f,'uniform_capacity_Nmm':mu*n*exact,
                     'best_possible_capacity_Nmm':mu*n*ro,
                     'impossible_even_outer_edge':mu*n*ro<R*f})
    assert .1*20*ro < 3.27*R # pressure-independent counterexample
    times=[spring_brake(dt) for dt in [1e-4,1e-5,1e-6]]
    assert abs(times[-1][0]-times[-1][1])<2e-6
    travel=[]
    # A grounded pad cannot exert torque until the gap actually closes.
    # Constant-velocity motion is enough to bound lost position from below
    # under nonnegative load acceleration; gravity-only is illustrative.
    for gap_mm in [.1,.2,.4]:
        _,t=spring_brake(1e-6,gap=gap_mm/1000)
        travel.append({'gap_mm':gap_mm,'first_contact_ms':1000*t,
                       'travel_at_300mm_s_no_acceleration_mm':300*t,
                       'gravity_only_travel_mm':300*t+.5*9810*t*t})
    # Selective loaded bolt: lift removes reaction before radial withdrawal.
    # If the face slips, no such unloading exists; straight slot walls require
    # at least mu_bolt*T/r_contact before spring/friction in guide is counted.
    release=[{'load_N':f,'bolt_mu':mu,'loaded_radial_pull_lower_bound_N':mu*f*R/3.4,
              'with_2N_return_before_guide_friction_N':2+mu*f*R/3.4}
             for f,mu in itertools.product([1.,3.27,10.],[.1,.3])]
    # Independent sleeve preserves arbitrary distal phase but the proximal
    # friction joint remains in series: same weakest torque cut, not a free lock.
    out={'evidence':'rigid contact cuts and bounded calculations, no admitted machine',
         'routing':routing(),'annulus_mean_radius_mm':exact,
         'annulus_convergence_mm':conv,'uniform_wear_radius_mm':annulus(64,'wear'),
         'capacity_scenarios':caps,'nominal_trace':contact_trace(),
         'adverse_face_trace':contact_trace(.1,20.,3.27),
         'brake_contact_time_convergence_s':times,'spring_brake_gap_cases':travel,
         'loaded_bolt_release':release,
         'drag_brake':{'pad_area_each_mm2':40,'normal_each_N':100,
                       'mu_bound_low':.1,'linear_hold_N':20,
                       'two_selected_10N_margin_N':0,
                       'loss_at_300mm_s_W':6,
                       '160_channels_10N_minimum_drag_power_W':480},
         'friction_cut_counterexample':{'load_N':3.27,'mu':.1,'normal_N':20,
             'demand_Nmm':3.27*R,'upper_capacity_Nmm':.1*20*ro,
             'outer_edge_min_normal_N':3.27*R/(.1*ro)},
         'checks':'annular integral; pressure-independent upper bound; pad-ODE analytic solution; exact backing clearance; inherited polygon lock/dog contacts'}
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    main()
