#!/usr/bin/env python3
"""E-152: finite smooth-front virtual-work bound. N, mm, MPa; stdlib.
Not contact dynamics: unilateral wall geometry + an admissible feed direction
bound ALL yield-limited stress histories; no feasible reaction field is claimed.
"""
import itertools
import json
import math


def trap(values, dx):
    return dx * (sum(values) - .5 * (values[0] + values[-1]))


def geometry(R=3., alpha=.25, t=.25, b=3., n=1024):
    # Arclength s; vertical tangent at both ends, one positive/negative lobe.
    L = 2 * math.pi * R * alpha
    ds = L / n
    theta = [alpha * (1 - math.cos(2*math.pi*i/n)) for i in range(n+1)]
    k = [math.sin(2*math.pi*i/n)/R for i in range(n+1)]
    kp = [2*math.pi/(L*R)*math.cos(2*math.pi*i/n) for i in range(n+1)]
    x = z = 0.
    points = [(x, z)]
    for a, c in zip(theta, theta[1:]):
        x += .5*ds*(math.sin(a)+math.sin(c))
        z += .5*ds*(math.cos(a)+math.cos(c))
        points.append((x, z))
    # Strip at normal eta has velocity (1-eta*k)*tangent for unit signed feed.
    # Walls at eta=+/-t/2 are two unilateral no-penetration constraints.
    # Finite wall thickness .5 mm is an assumption, not a strength check.
    normal_work = []
    envelope_x = []
    faces = {-1: [], 1: []}
    for (x,z), a, curvature in zip(points, theta, k):
        tangent = (math.sin(a), math.cos(a))
        normal = (math.cos(a), -math.sin(a))
        for sign in (-1, 1):
            eta = sign*t/2
            faces[sign].append((x+eta*normal[0], z+eta*normal[1]))
            v = tuple((1-eta*curvature)*v for v in tangent)
            normal_work.append(sum(vv*nn for vv,nn in zip(v,normal)))
        envelope_x += [x + sign*(t/2+.5)*normal[0] for sign in (-1,1)]
    for face in faces.values():
        assert all(c[1] > a[1] for a,c in zip(face,face[1:]))
    assert min(math.cos(a) for a in theta) > 0
    assert 1-t/(2*R) > 0  # offset paths have no cusp and are z-monotone
    assert max(map(abs,normal_work)) < 1e-14
    assert abs(theta[0])+abs(theta[-1]) < 1e-14
    tv = trap(list(map(abs,kp)),ds)
    # q translates material along the SAME spatial path, changes only straight
    # tail lengths. 80+L strip: input 80-q, output q, q in [0,40].
    for q in (0.,5.,20.,40.):
        assert 80-q >= 40 and q >= 0
        assert abs((80-q)+L+q-(80+L)) < 1e-12
    return dict(length_mm=L, end_x_mm=points[-1][0], end_z_mm=points[-1][1],
                x_envelope_mm=max(envelope_x)-min(envelope_x),
                y_envelope_mm=b+1., curvature_TV_per_mm=tv,
                TV_exact_per_mm=4/R, max_normal_speed_per_unit_feed=max(map(abs,normal_work)),
                offset_regular_margin=1-t/(2*R))


def section_path(E, sy, b, t, R, n, nf, elastic=False):
    """Three forward and reverse material passages; stress history is explicit.
    Each passage is section curvature 0,+K,0,-K,0 (or reversed).
    Work per transported length has units N. Front R = integral M dk.
    This validates the bound/energy accounting, NOT a parked state.
    """
    y = [(i+.5)*t/nf-t/2 for i in range(nf)]
    area = b*t/nf
    p = [0.]*nf
    stress = [0.]*nf
    strain = [0.]*nf
    records = []
    for sign in (1.,1.,1.,-1.,-1.,-1.):
        u0 = sum(v*v/(2*E)*area for v in stress)
        work = heat = 0.
        max_m = 0.
        for j in range(1,n+1):
            k = sign*math.sin(2*math.pi*j/n)/R
            for i,yi in enumerate(y):
                e = yi*k
                trial = E*(e-p[i])
                sig = trial if elastic else min(sy,max(-sy,trial))
                plastic = e-sig/E
                work += .5*(stress[i]+sig)*(e-strain[i])*area
                if not elastic:
                    heat += sy*abs(plastic-p[i])*area
                stress[i],strain[i],p[i] = sig,e,plastic
            moment = sum(v*yi*area for v,yi in zip(stress,y))
            max_m = max(max_m,abs(moment))
        u1 = sum(v*v/(2*E)*area for v in stress)
        records.append(dict(direction=int(sign),work_N=work,heat_N=heat,
                            inventory_change_N=u1-u0,residual_N=work-heat-u1+u0,
                            max_moment_Nmm=max_m))
    return records


def bounds(E, sy, b, t, R):
    mp = sy*b*t*t/4
    I = b*t**3/12
    length = 80 + 2*math.pi*R*.25
    cap = 4*mp/R
    return dict(moment_cap_Nmm=mp, feed_force_cap_N=cap,
                stabilized_loss_N=b*sy/R*max(t-2*sy*R/E,0)**2,
                all_strip_elastic_inventory_cap_Nmm=sy**2/(2*E)*b*t*length,
                elastic_front_inventory_Nmm=E*I*(length-80)/(4*R**2),
                pinned_40mm_Euler_N=math.pi**2*E*I/40**2,
                fixed_40mm_Euler_N=4*math.pi**2*E*I/40**2,
                max_pinned_span_for_10N_mm=math.pi*math.sqrt(E*I/10),
                strain=t/(2*R))


def main():
    nominal = (200000.,200.,3.,.25,3.)
    weak = (160000.,160.,2.9,.20,3.2)
    out = {'evidence':'analytical necessary bound + geometry/constitutive quadrature; no dynamics'}
    out['geometry_refinement'] = [geometry(n=n) for n in (64,256,1024)]
    assert abs(out['geometry_refinement'][-1]['curvature_TV_per_mm']-4/3)<5e-6
    out['nominal'] = bounds(*nominal)
    out['weak'] = bounds(*weak)
    refinements = []
    for n,nf in ((64,32),(256,64),(1024,128)):
        r = section_path(*nominal,n,nf)
        refinements.append(dict(steps=n,fibers=nf,virgin=r[0],stabilized=r[2],reverse=r[-1]))
        assert all(v['max_moment_Nmm'] <= out['nominal']['moment_cap_Nmm'] for v in r)
        assert abs(r[2]['work_N']-r[-1]['work_N']) < 1e-10
    out['constitutive_refinement'] = refinements
    assert abs(refinements[-1]['stabilized']['heat_N']-out['nominal']['stabilized_loss_N'])<.001
    assert abs(refinements[-1]['stabilized']['residual_N']) < .001
    elastic = section_path(*nominal,256,64,elastic=True)
    assert max(abs(r['work_N'])+r['heat_N'] for r in elastic) < 1e-9
    out['elastic_control'] = {'max_cycle_work_N':max(abs(r['work_N']) for r in elastic),
        'feed_force_N':0.,'rest_at_W0':'neutral','rest_at_W1_W10':'absent',
        'moving_W0':'no dissipation; no arrest in feed coordinate'}
    # Independent maximization over ALL bounded fiber stresses: choose
    # sigma(s,y) = sy sign(y*kprime(s)), not assumed physically attainable.
    # It saturates the unrestricted virtual-work upper bound, proving that no
    # OTHER stress history can exceed it. Midpoint fiber integration is exact
    # for integral |y| when nf even; curvature quadrature converges separately.
    upper = []
    E,sy,b,t,R = weak
    for n in (64,256,1024):
        nf=64
        y=[(i+.5)*t/nf-t/2 for i in range(nf)]
        m=sum(sy*abs(v)*b*t/nf for v in y)
        tv=geometry(R=R,t=t,b=b,n=n)['curvature_TV_per_mm']
        upper.append(m*tv)
    out['independent_stress_box_bound_N'] = upper
    assert abs(upper[-1]-out['weak']['feed_force_cap_N']) < 2e-5
    # All E-151 coherent corners, not random samples or manufacturing yield.
    corners=[bounds(E,sy,b,t,R)['feed_force_cap_N'] for b,t,R,E,sy in
             itertools.product((2.9,3.1),(.2,.3),(2.8,3.2),(160000.,240000.),(160.,240.))]
    out['32_corner_force_cap_range_N']=[min(corners),max(corners)]
    # Manufacture/assembly scenarios: common smooth radius and angle changes,
    # independent .1 mm poses of adjacent cartridges; no curvature microtexture.
    gs=[geometry(R=R,alpha=a,t=.2,b=2.9,n=256) for R,a in
        itertools.product((2.8,3.2),(.2,.3))]
    out['weak_guide_box'] = dict(
        force_cap_range_N=[160*2.9*.2**2/3.2,160*2.9*.2**2/2.8],
        with_20percent_extra_curvature_TV_cap_N=1.2*160*2.9*.2**2/2.8,
        max_x_envelope_mm=max(g['x_envelope_mm'] for g in gs),
        min_x_neighbor_clearance_mm=5.08-max(g['x_envelope_mm'] for g in gs)-.2,
        min_y_neighbor_clearance_mm=5.08-3.9-.2,
        min_top_clearance_mm=5.08-4.8-.2,
        frame_cross_compliance_mm_per_N=[0,.001,.01],
        neighbor_motion_at_10N_mm=[0,.01,.1])
    # Moving downward, mass constant: dK/dd = W - resistance >= W-cap.
    # q=0 is an END STOP, never counted as intended-height arrest.
    cuts=[]
    cap=out['weak']['feed_force_cap_N']
    for h,W,v in itertools.product((5.,20.,40.),(0.,1.,10.),(-.1,0.,.1)):
        m=1.1 if W==10 else (.12 if W==1 else .02)
        K0=.5*m*v*v*1000  # J -> N mm
        cuts.append(dict(height_mm=h,load_N=W,downward_speed_m_s=v,
            history='any bounded stress: raising/reversing/lowering/parked',
            necessary_result='no equilibrium; no downward turning point before bottom' if W>cap else 'unresolved',
            bottom_kinetic_lower_bound_Nmm=K0+(W-cap)*h if W>cap and v>=0 else None,
            upward_turn_distance_upper_mm=K0/(W-cap) if W>cap and v<0 else None,
            upward_turn_before_upper_end_guaranteed=(K0/(W-cap)<40-h) if W>cap and v<0 else None))
    out['free_input_cuts']=cuts
    assert all(c['bottom_kinetic_lower_bound_Nmm']>0 for c in cuts if c['load_N']==10 and c['downward_speed_m_s']>=0)
    out['elastic_inventory_check']=dict(
        weak_40mm_gravity_minus_max_internal_work_Nmm=(10-cap)*40,
        weak_initial_kinetic_1p1kg_0p1mps_Nmm=5.5,
        note='stress-power bound already includes elastic release; do NOT add inventory again')
    # Explicit discrepancy reopening thresholds, not probabilities or margins.
    out['reopening']=dict(weak_required_TV_per_mm=10/out['weak']['moment_cap_Nmm'],
        weak_required_bound_multiplier=10/cap,
        weak_min_thickness_mm=math.sqrt(10*3.2/(160*2.9)),
        weak_min_yield_MPa=10*3.2/(2.9*.2**2),
        note='equalities are necessary zero-margin conditions, never sufficient hold')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
