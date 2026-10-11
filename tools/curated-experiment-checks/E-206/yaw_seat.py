"""E-206: finite yaw seat and shared-stock necessary conditions; mm, N, MPa.

Prescribed geometry and bounded linear elasticity, not a qualified mechanism.
Run from any directory with Python + NumPy. JSON is disposable.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np

spec = importlib.util.spec_from_file_location(
    "hook", Path(__file__).resolve().parents[1] / "E-166/probe.py")
hook = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook)


def rect(x0, x1, y0, y1):
    return hook.rectangle(x0, x1, y0, y1)


def rotate(p, angle):
    c, s = math.cos(angle), math.sin(angle)
    return (p - [0, -.4]) @ np.array([[c, -s], [s, c]]) + [0, -.4]


def disk(n=128):
    # Circumscribed polygon: radial overestimate < .00019 mm at n=128.
    a = np.arange(n) * 2 * math.pi / n
    return np.c_[.6 / math.cos(math.pi/n) * np.cos(a),
                 -.4 + .6 / math.cos(math.pi/n) * np.sin(a)]


def pawl(angle, offset=(0., 0.)):
    return [disk() + offset,
            rotate(rect(-.4, .4, -.4, 1.3), angle) + offset]


def prism_hit(a, az, b, bz):
    if min(az[1], bz[1]) - max(az[0], bz[0]) <= 1e-10:
        return False
    if np.any(np.minimum(a.max(axis=0),b.max(axis=0))
              - np.maximum(a.min(axis=0),b.min(axis=0)) <= 1e-10):
        return False
    return hook.overlap(a, b)


def old_obstruction():
    rel = hook.release()
    hits = []
    stop = rect(-1., -.2, 11.8, 12.8)
    for i in range(65):
        state = hook.equilibrium(266.6666667, 12., H=rel['H']*i/64)
        if any(hook.overlap(p, stop) for p in hook.bodies(state)):
            hits.append(i)
    assert len(hits) == 55 and hits[0] == 10
    return {'blocked_of_65': len(hits), 'first_fraction': hits[0]/64}


def geometry(steps=64, angle_deg=65):
    t = .2
    checks = 0
    end_gaps = []
    contact_width = []
    # Coherent bank/rack/frame errors: reuse each draw throughout its sequence.
    # These are adversarial scenarios, not random process priors.
    for px, py, rx, ry, fy in itertools.product((-.05, .05), repeat=5):
        frame = [
            (rect(-.6, .6, -1.6+fy, .3+fy), (-.8, 0.)),
            (rect(-.8, .8, -1.6+fy, -.7+fy), (t, t+.8)),
            (rect(-.8, .8, -1.6+fy, -1.15+fy), (-.8, t+13.)),
            (rect(-.8, .8, -1.6+fy, -.15+fy), (t+12., t+13.)),
        ]
        rack = rect(-.4+rx, .4+rx, .6+ry, 1.7+ry)
        web = rect(-.4+rx, .4+rx, 1.7+ry, 2.2+ry)
        assert hook.overlap(pawl(0., (px, py))[1], rack)
        contact_width.append(min(.4+rx,.4+px)-max(-.4+rx,-.4+px))
        # Actual points on the generated upper hub / lower nose contact faces.
        x = (px+rx)/2
        lower_y, upper_y, r = .2+fy, -.85+fy, 1.3+py
        assert (x-px)**2+(upper_y+.4-py)**2 < .6**2
        assert -.4+px < x < .4+px and -.4+py < lower_y < 1.3+py
        upper = (r-lower_y)/(lower_y-upper_y)
        lower = 1+upper
        assert upper > 0 and lower > 0
        assert abs(lower*lower_y-upper*upper_y-r)<1e-12
        # Other four of the five 10-mm-spaced teeth are clear by z intervals.
        for i in range(steps+1):
            angle = math.radians(angle_deg)*i/steps
            for p in pawl(angle, (px, py)):
                for f, z in frame:
                    assert not prism_hit(p, (0., t), f, z)
                    checks += 1
                assert not prism_hit(p, (0., t), rack, (t+1.,t+3.))
                assert not prism_hit(p, (0., t), web, (-42.,42.))
                checks += 2
        # Open xy disjointness excludes every intermediate rack height exactly.
        for p in pawl(math.radians(angle_deg), (px, py)):
            assert not hook.overlap(p, rack)
        # Ground solids also clear the rack's entire vertical swept envelope.
        for f, _ in frame:
            assert not hook.overlap(f, rack) and not hook.overlap(f, web)
        # Closest infinite-line gap on the rotated nose's left edge; positive
        # implies the complete rack rectangle lies outside the nose polygon.
        a = math.radians(angle_deg)
        inv_max = (.4+rx-px)*math.cos(a)-(.6+ry+.4-py)*math.sin(a)
        end_gaps.append(-.4-inv_max)
    assert min(end_gaps) > 0
    # A circle bounds all pawl angles and opposite neighboring commands.
    radial = math.hypot(.4,1.7)
    neighbor_gap = 5.08 - 2*(radial+.05)
    assert neighbor_gap > 0
    # Ribbon at a real interior z cross-section, including positive z overlap
    # with the cap. Broad ribbon collides; narrow one has all-angle bound.
    ribbons = []
    cap = rect(-.8,.8,-1.6,-.7)
    for w in (.4,.8,1.2):
        section = rotate(rect(-w/2,w/2,-.5,-.3),
                         math.radians(angle_deg)*(1-.05/12))
        hit = hook.overlap(section,cap)
        coherent_hits=sum(hook.overlap(section+[0,py],cap+[0,fy])
                          for py,fy in itertools.product((-.05,.05),repeat=2))
        ribbons.append({'width':w,'cap_collision_at_z_t_plus_005':bool(hit),
                        'coherent_cap_collisions_of_4':coherent_hits,
                        'all_angle_cap_gap':.3-math.hypot(w/2,.1)})
    assert not ribbons[0]['cap_collision_at_z_t_plus_005']
    assert ribbons[0]['coherent_cap_collisions_of_4'] > 0
    assert ribbons[-1]['cap_collision_at_z_t_plus_005']
    return {'coherent_corners':32,'steps':steps,'prism_checks':checks,
            'min_open_separating_gap':min(end_gaps),
            'min_contact_width':min(contact_width),'neighbor_circle_gap':neighbor_gap,
            'ribbons':ribbons,'unequal_height_transitions_per_corner':20}


def shear_coefficient(w, t, terms=50):
    """Saint-Venant rectangle: broad-face midpoint stress/(G*twist_rate).

    Separation-of-variables solution of Laplacian(phi)=-2G*twist_rate,
    phi=0 on the rectangular boundary. Reduces to the smaller dimension in
    the thin-strip limit. Return has units mm, not a torsion constant.
    """
    b, h = max(w,t), min(w,t)
    correction = 0.
    for n in range(1,2*terms,2):
        arg = n*math.pi*b/(2*h)
        correction += 0. if arg > 700 else 1/(n*n*math.cosh(arg))
    return h*(1-8/math.pi**2*correction)


def poisson_holdout(w, t, n):
    """Independent finite-difference stress-function solve; normalized G*k=1."""
    nx = round(n*w/t)
    dx,dy = w/nx,t/n
    u = np.zeros((nx+1,n+1))
    parity = np.indices((nx-1,n-1)).sum(axis=0) % 2
    den = 2/dx**2+2/dy**2
    for iteration in range(30000):
        change=0.
        for color in (0,1):
            target=((u[2:,1:-1]+u[:-2,1:-1])/dx**2
                    +(u[1:-1,2:]+u[1:-1,:-2])/dy**2+2)/den
            delta=1.7*(target-u[1:-1,1:-1])*(parity==color)
            u[1:-1,1:-1]+=delta
            change=max(change,float(np.max(abs(delta))))
        if change < 1e-12: break
    else: raise AssertionError('Poisson iteration limit')
    return (4*u[nx//2,-2]-u[nx//2,-3])/(2*dy)


def force_screen():
    # Force equilibrium for horizontal service faces. Front lower reaction at
    # y=.2, opposing rear upper reaction at y=-.85; both inside finite pads.
    reactions=[]
    for W in (.1,1.,10.):
        r=1.3
        upper=W*(r-.2)/(.2+.85)
        lower=W+upper
        assert abs(lower-upper-W)<1e-12
        assert abs(lower*.2+upper*.85-W*r)<1e-12
        reactions.append({'W':W,'lower':lower,'upper':upper})
    # Whole-bank corners; service load may occur at the nose's far edge.
    # Thickness is shared by toe and neck; no free reinforcement is granted.
    cases=[]
    for W in (.1,1.,10.):
        for G,sigma,tau in ((77000,400,400),(60000,800,800),(700,40,20)):
            for L,b,lever in itertools.product((11.5,12.5),(.7,.9),(.9,1.1)):
                tmin=math.sqrt(6*W*lever/(b*sigma))
                lo,hi=0.,.4
                for _ in range(60):
                    mid=(lo+hi)/2
                    stress=G*math.radians(65)/L*shear_coefficient(.4,mid)
                    if stress<=tau:lo=mid
                    else:hi=mid
                # t<=.4 is the explicit maximum sheet thickness search bound.
                cases.append({'W':W,'G':G,'sigma':sigma,'tau':tau,'L':L,
                              'b':b,'lever':lever,'tmin':tmin,'tmax':lo,
                              'interval':bool(tmin<=lo),
                              'Lneeded_at_tmin':G*math.radians(65)
                              *shear_coefficient(.4,tmin)/tau})
    assert not any(c['interval'] for c in cases if c['W']==10.)
    summary=[]
    for W in (.1,1.,10.):
        for G in (77000,60000,700):
            rows=[c for c in cases if c['W']==W and c['G']==G]
            summary.append({'W':W,'G':G,'surviving_corners_of_8':sum(c['interval'] for c in rows),
                            'tmin_range':[min(c['tmin'] for c in rows),max(c['tmin'] for c in rows)],
                            'tmax_range':[min(c['tmax'] for c in rows),max(c['tmax'] for c in rows)],
                            'Lneeded_range':[min(c['Lneeded_at_tmin'] for c in rows),max(c['Lneeded_at_tmin'] for c in rows)]})
    # A thickness tolerance eats both ends, coherently across the comb.
    favorable=[c for c in cases if c['G']==60000 and c['W']==1.]
    robust=sum(c['tmin']+.02 <= c['tmax']-.02 for c in favorable)
    # Exact corner/left-edge tangency gives the minimum angle for the worst
    # specified planar offsets. No endpoint-clearance margin is included.
    min_angle=math.atan2(.5,.9)+math.asin(.4/math.hypot(.5,.9))
    best_toe=math.sqrt(6*10*.9/(.9*800))
    min_L=60000*min_angle*shear_coefficient(.4,best_toe)/800
    assert min_L>12.5
    return {'reactions':reactions,'corners':len(cases),'summary':summary,
            'angle_optimization_holdout':{'minimum_degrees':math.degrees(min_angle),
                                           'best_10_N_required_L':min_L},
            'one_N_optimistic_corners_with_plusminus_002_stock':robust}


def verify():
    assert not prism_hit(rect(0,1,0,1),(0,1),rect(0,1,0,1),(1,2))
    assert prism_hit(rect(0,1,0,1),(0,1),rect(.5,2,.5,2),(.5,2))
    assert abs(shear_coefficient(100.,.1)-.1)<1e-10
    assert abs(shear_coefficient(.4,.2)-shear_coefficient(.2,.4))<1e-12
    holds=[]
    exact=shear_coefficient(.4,.2)
    for n in (16,32,64):
        got=poisson_holdout(.4,.2,n)
        assert abs(got/exact-1)<.008
        holds.append({'n':n,'shear_length':got,'relative_error':got/exact-1})
    return {'series_shear_length':exact,'PDE_holdout':holds}


def main():
    out={'self_checks':verify(),'E166_reconstruction':old_obstruction(),
         'geometry':[geometry(n) for n in (16,64,256)],'force':force_screen()}
    out['machine']={'sheet_placements':160,'resident_toes_and_ribbons':6400,
                    'sheet_area_at_15_mm_height_m2':160*203.2*15/1e6,
                    'nominal_slot_ceiling_s':{str(H):(30-6)/math.ceil(6400/H) for H in (40,80,160)},
                    'resident_budget_if_250_dollars_elsewhere':250/6400}
    gaps=[roof-floor-stock for roof,floor,stock in
          itertools.product((-.05,.05),(-.05,.05),(-.02,.02))]
    out['vertical_fit_bounds']={'corners':len(gaps),'interference_corners':sum(g<0 for g in gaps),
                                'slot_gap_range':[min(gaps),max(gaps)],
                                'with_015_extra_gap':[.15+min(gaps),.15+max(gaps)]}
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
