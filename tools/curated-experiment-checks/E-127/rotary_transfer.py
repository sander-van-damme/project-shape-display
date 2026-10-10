"""E-127: finite rigid sections, not a qualified assembly. mm, rad, N.

Python 3 + numpy. --svg PATH exports the actual sampled sections (not retained).
All errors/loads are explicit scenarios, never fitted process distributions.
"""
import argparse
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path

import numpy as np

PI = math.pi
ALPHA = math.radians(20)
M, Z = 0.4, 18
R = M * Z / 2
P = PI * M
BACKLASH = 0.10  # rack total tangential tooth thinning


def rotate(points, angle):
    c, s = math.cos(angle), math.sin(angle)
    return np.asarray(points) @ np.array([[c, s], [-s, c]])


def rectangle(x0, x1, y0, y1):
    return np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])


def gear(samples):
    """Involute flanks, radial below-base transitions, sharp root (no fillet)."""
    rb, rf, ra = R * math.cos(ALPHA), R - 1.25 * M, R + M
    inv_a = math.tan(ALPHA) - ALPHA
    rho = np.linspace(rb, ra, samples + 1)
    a = np.arccos(rb / rho)
    half = PI / (2 * Z) + inv_a - (np.tan(a) - a)
    pts = []
    for k in range(Z):
        center = (2 * k + 1) * PI / Z  # tooth gap faces rack tooth at y=0
        polar = [(rf, -half[0])]
        polar += list(zip(rho, -half))
        polar += [(ra, t) for t in np.linspace(-half[-1], half[-1], 9)[1:]]
        polar += list(zip(rho[::-1], half[::-1]))
        polar += [(rf, half[0])]
        polar += [(rf, t) for t in np.linspace(half[0], 2 * PI / Z - half[0], 9)[1:]]
        pts += [(rr * math.cos(center + t), rr * math.sin(center + t)) for rr, t in polar]
    return np.array(pts)


def rack_boundary(y, height=0, center_error=0, tooth_growth=0):
    # Exact piecewise-linear finite rack face, periodic interior. Its ends are
    # -48+h and +8+h; the full pinion stays inside that range over h=0..40.
    folded = np.abs((y - height + P / 2) % P - P / 2)
    x = R + (folded - P / 4 + BACKLASH / 2 - tooth_growth) / math.tan(ALPHA)
    return np.clip(x, R - M, R + 1.25 * M) + center_error


def finite_rack(height=0):
    ys=[-48.,8.]
    for k in range(-40,8):
        for offset in [-M,1.25*M]:
            half=P/4-BACKLASH/2+offset*math.tan(ALPHA)
            ys.extend(k*P+sign*half for sign in [-1,1]
                      if -48 < k*P+sign*half < 8)
    y=np.array(sorted(ys))+height
    face=np.c_[rack_boundary(y,height), y]
    return np.r_[face, [[R+1.25*M+.8,8+height], [R+1.25*M+.8,-48+height]]]


def mesh_scan(samples=128, phases=161, center_error=0, growth=0, seat=False):
    shape = gear(samples)
    gap = math.inf
    max_nearest = -math.inf
    for theta in np.linspace(0, 2 * PI / Z, phases):
        points = rotate(shape, theta)
        h = R * theta + (BACKLASH / 2 if seat else 0)
        clearance = rack_boundary(points[:, 1], h, center_error, growth) - points[:, 0]
        nearest = float(clearance.min())
        # Minimum of piecewise-linear rack-x minus polygon-edge-x also occurs
        # at rack corners crossed by an edge, not just at gear vertices.
        other = np.roll(points, -1, axis=0)
        active = np.maximum(points[:,0], other[:,0]) >= R-M+center_error
        a, b = points[active], other[active]
        dy = b[:,1]-a[:,1]
        valid = np.abs(dy)>1e-14
        a,b,dy = a[valid],b[valid],dy[valid]
        for k in range(-6,7):
            for offset in [-M,1.25*M]:
                half=P/4-BACKLASH/2+growth+offset*math.tan(ALPHA)
                for sign in [-1,1]:
                    y=k*P+h+sign*half
                    t=(y-a[:,1])/dy
                    crossing=(t>0)&(t<1)
                    if crossing.any():
                        x=a[crossing,0]+t[crossing]*(b[crossing,0]-a[crossing,0])
                        nearest=min(nearest,float(np.min(rack_boundary(y,h,center_error,growth)-x)))
        gap = min(gap, nearest)
        max_nearest = max(max_nearest, nearest)
    return [gap, max_nearest]


def dock_margin(angle, count=6, dx=0, dz=0, growth=0, shrink=0):
    """Rectangular face dogs in rectangular axial sockets, exact vertex fit.

    Dog radius 2.6, radial width .6, tangential width .5, axial length .8.
    Socket radial width .8, tangential width .8, axial depth 1.0.
    Positive margin means every convex dog fits its convex socket.
    """
    a = (angle + PI / count) % (2 * PI / count) - PI / count
    margin = math.inf
    for k in range(count):
        t = 2 * PI * k / count
        dog = rotate(rectangle(2.3-growth, 2.9+growth, -.25-growth, .25+growth), t+a)
        local = rotate(dog + [dx, dz], -t)
        margin = min(margin, float(np.min(local[:, 0] - (2.2+shrink))),
                     float(np.min((3.0-shrink) - local[:, 0])),
                     float(np.min((.4-shrink) - np.abs(local[:, 1]))))
    return margin


@lru_cache(maxsize=64)
def clipped_bolt(growth, tangent_error, segments):
    """Convex disk polygon intersected with the inserted rectangular bolt."""
    theta=np.linspace(0,2*PI,segments,endpoint=False)
    poly=np.c_[3.4*np.cos(theta),3.4*np.sin(theta)].tolist()
    for axis,bound,sign in [(0,2.6-growth,1),(0,4.4+growth,-1),
                            (1,-.25-growth+tangent_error,1),
                            (1,.25+growth+tangent_error,-1)]:
        out=[]
        for a,b in zip(poly,poly[1:]+poly[:1]):
            da,db=sign*(a[axis]-bound),sign*(b[axis]-bound)
            if da>=0: out.append(a)
            if (da>=0)!=(db>=0):
                t=da/(da-db)
                out.append([a[j]+t*(b[j]-a[j]) for j in [0,1]])
        poly=out
    return np.array(poly)


def lock_margin(angle, growth=0, shrink=0, tangent_error=0, segments=4096):
    """Positive radial bolt in one of twelve open radial slots.

    Collar R=3.4, root=2.4; slot tangential width .9. Bolt width .5,
    engaged nose x=2.6, outer end=4.4. Clip the bolt against the actual
    generated collar disk before checking containment in the open radial slot.
    """
    a = (angle + PI/12) % (PI/6) - PI/12
    local = rotate(clipped_bolt(growth,tangent_error,segments), -a)
    return min(float(np.min(local[:, 0] - (2.4+shrink))),
               float(np.min(.45-shrink - np.abs(local[:, 1]))))


def fit_window(fn, pitch):
    # Monotone near zero for these rectangular sections; bracket first boundary.
    lo, hi = 0., pitch/2
    assert fn(lo) > 0 and fn(hi) < 0
    for _ in range(60):
        mid = (lo+hi)/2
        if fn(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def phase_probe():
    w6 = fit_window(dock_margin, PI/3)
    w12 = fit_window(lambda a: dock_margin(a, 12), PI/6)
    wl = fit_window(lock_margin, PI/6)
    angles = np.linspace(0, 2*PI, 721, endpoint=False)
    simultaneous = sum(dock_margin(t) >= 0 and dock_margin(t-PI/6) >= 0 for t in angles)
    assert simultaneous == 0 and 2*w6 < PI/6  # continuous interval proof too
    assert all(dock_margin(k*PI/6, 12) > .099999 for k in range(12))
    # Same-index docking with bounded common translation plus local profile errors.
    errors = []
    for e in [0., .025, .05, .10]:
        margins = [dock_margin(0, 12, dx, dz, grow, shrink)
                   for dx, dz, grow, shrink in itertools.product([-e, e], repeat=4)]
        errors.append({'bound_mm': e, 'worst_common_xy_and_profile_margin_mm': min(margins)})
    return {'dock_half_window_deg': math.degrees(w6),
            'lock_half_window_deg': math.degrees(wl),
            'two_locked_phases_deg': [0, 30], 'shared_six_dog_fit_samples': simultaneous,
            'samples': len(angles), 'coindexed_12_dog_nominal_states': 12,
            'coindexed_errors': errors, 'height_grid_mm': R*PI/6,
            '22_steps_mm': 22*R*PI/6, 'ground_seating_height_offset_mm': R*wl,
            'full_bolt_insertion_blocked_arc_mm': R*(PI/6-2*wl),
            'next_slot_catch_assumed_drop_supremum_mm': R*PI/6,
            'lock_width_perturbations': [
                {'edge_error_mm': e, 'centered_margin_mm': lock_margin(0, e, e, e)}
                for e in [0, .025, .05, .10]],
            'lock_disk_convergence_deg': [
                [n,math.degrees(fit_window(lambda a: lock_margin(a,segments=n),PI/6))]
                for n in [256,1024,4096]]}


def supported_states():
    """Contact gaps matter: an inserted unloaded dock is not a load support.

    Positive theta lifts. Ground collar is seated on its negative stop. The
    drive first contacts the load flank, then lifts inside the lock clearance,
    then opens the bolt. On return the drive lowers onto the ground stop before
    withdrawing. This is one independent head's local rigid path, not a bank.
    """
    wd = fit_window(dock_margin, PI/3)
    wl = fit_window(lock_margin, PI/6)
    theta0 = -wl
    sequence = [
        ('parked', theta0, False, None, True),
        ('dock_inserted_unloaded', theta0, True, theta0, True),
        ('drive_flank_contact', theta0, True, theta0+wd, True),
        ('ground_unloaded', 0., True, wd, True),
        ('ground_retracted', 0., True, wd, False),
        ('moving_half_index', PI/12, True, PI/12+wd, False),
        ('target_bolt_inserted', PI/6, True, PI/6+wd, True),
        ('ground_reseated', PI/6-wl, True, PI/6-wl+wd, True),
        ('dock_unloaded', PI/6-wl, True, PI/6-wl, True),
        ('undocked', PI/6-wl, False, None, True),
    ]
    result = []
    for name, theta, inserted, head, bolt in sequence:
        fit = dock_margin(head-theta) if inserted else None
        assert fit is None or fit > -1e-10
        lm = lock_margin(theta)
        assert not bolt or lm > -1e-10
        drive = inserted and abs(head-theta-wd) < 1e-9
        ground = bolt and abs(((theta+wl+PI/12) % (PI/6))-PI/12) < 1e-9
        assert drive or ground
        result.append({'state': name, 'ground_load_contact': ground,
                       'powered_drive_load_contact': drive,
                       'power_off_without_extra_brake_supported': ground,
                       'spring_bolt_can_fully_insert_now': lm >= -1e-10})
    assert not next(s for s in result if s['state']=='moving_half_index')['spring_bolt_can_fully_insert_now']
    return result


def packaging():
    # Two alternating gear/rack axial lanes can separate gear disks. A straight
    # shaft crossing the other lane hits the adjacent full-travel rack backing.
    # Neighbor rack pitch line R-5.08; backing x=[pitch+1.25m,pitch+1.25m+.8].
    x0, x1 = R-5.08+1.25*M, R-5.08+1.25*M+.8
    shaft_r = .8
    nearest = max(x0, min(0., x1))
    shaft_collision = abs(nearest) < shaft_r
    assert shaft_collision
    # Exact circle/backing rectangle intersection at shaft-height z=0. Backing
    # spans z=-48+h..8+h, so this holds at every h=0..40 in the same tier.
    return {'pinion_outer_diameter_mm': 2*(R+M),
            'same_plane_gear_envelope_overlap_mm': 2*(R+M)-5.08,
            'alternate_lane_same_tier_backing_x_mm': [x0, x1],
            'straight_cross_lane_shaft_radius_mm': shaft_r,
            'shaft_backing_penetration_mm': shaft_r-abs(nearest),
            'straight_cross_lane_shaft_collision': shaft_collision,
            'shaft_bore_bounds': [{'edge_and_eccentricity_bound_mm': e,
                                   'minimum_radial_gap_mm': .15-3*e}
                                  for e in [0,.025,.05,.10]],
            'axial_parts_mm': {'rear_bearing': [-1.2,-.2], 'gear': [0,1.2],
                               'lock_collar': [1.4,2.6], 'front_bearing': [2.8,3.8],
                               'socket_disk': [4,5.2], 'docked_head': [5.2,7.2]},
            'stagger_scope': 'reject same-tier two-lane straight shaft only; remote/tiered routing unbuilt'}


def svg(path):
    polys = []
    def poly(points, ox, oy, color):
        data = ' '.join(f'{ox+12*x:.3f},{oy-12*y:.3f}' for x,y in points)
        polys.append(f'<polygon points="{data}" fill="{color}" fill-opacity=".4" stroke="{color}" stroke-width=".6"/>')
    poly(gear(128), 85, 105, '#3366aa')
    y = np.sort(np.r_[np.linspace(-6,6,1601), [-6,6]])
    rack = np.c_[rack_boundary(y), y]
    poly(np.r_[rack, [[4.9,6],[4.9,-6]]], 85, 105, '#aa7733')
    for ox, phase, count in [(270,PI/6,6), (450,PI/6,12)]:
        for k in range(count):
            t=2*PI*k/count
            poly(rotate(rectangle(2.2,3.,-.4,.4),t),ox,105,'#999999')
            poly(rotate(rectangle(2.3,2.9,-.25,.25),t+phase),ox,105,'#bb3333')
    circle=np.array([(3.4*math.cos(t),3.4*math.sin(t)) for t in np.linspace(0,2*PI,361)])
    poly(circle,630,105,'#3366aa')
    for k in range(12):
        poly(rotate(rectangle(2.4,3.7,-.45,.45), k*PI/6+PI/12),630,105,'#eeeeee')
    poly(rectangle(2.6,4.4,-.25,.25),630,105,'#bb3333')
    labels=[(15,'Involute rack / pinion'),(195,'6 dogs: 30 deg clash'),(375,'12 dogs: 30 deg fit'),(555,'Lock at half step: blocked')]
    out='<svg xmlns="http://www.w3.org/2000/svg" width="770" height="220" viewBox="0 0 770 220"><rect width="770" height="220" fill="white"/>'
    out+=''.join(polys)+''.join(f'<text x="{x}" y="205" font-family="sans-serif" font-size="12">{s}</text>' for x,s in labels)+'</svg>'
    Path(path).write_text(out)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--svg')
    args=parser.parse_args()
    for h in [0.,20.,40.]:
        rack=finite_rack(h)
        assert rack[:,1].min() < -(R+M) and rack[:,1].max() > R+M
    # Cross-check independent involute contact-path bound; rb is tangent to LOA.
    rb=R*math.cos(ALPHA)
    path=math.sqrt((R+M)**2-rb**2)-R*math.sin(ALPHA)+M/math.sin(ALPHA)
    contact_ratio=path/(P*math.cos(ALPHA))
    convergence=[{'flank_segments': n, 'seated_clearance_min_max_mm': mesh_scan(n, 321, seat=True)}
                 for n in [32,128,512]]
    assert convergence[-1]['seated_clearance_min_max_mm'][0] > -1e-8
    assert convergence[-1]['seated_clearance_min_max_mm'][1] < .00001
    errors=[{'center_error_mm': c, 'tooth_halfwidth_growth_mm': g,
             'clearance_min_max_mm': mesh_scan(128,161,c,g)}
            for c,g in itertools.product([-.10,0,.10], [0,.025,.05])]
    phase=phase_probe()
    result={'evidence':'finite rigid sections and analytic bounds; no hardware/process probabilities',
            'gear': {'module_mm': M,'teeth':Z,'pitch_radius_mm':R,
                     'rack_length_mm':56,'stroke_mm':40,'contact_ratio_ideal':contact_ratio,
                     'no_undercut_bound_teeth':2/math.sin(ALPHA)**2,
                     'convergence':convergence,'error_scenarios':errors},
            'phase':phase,'supported_states':supported_states(),'packaging':packaging(),
            'load_scenarios':[{'load_N':f,'shaft_torque_Nmm':f*R,
                               'next_slot_catch_assumed_energy_mJ':f*phase['next_slot_catch_assumed_drop_supremum_mm']}
                              for f in [1.,3.27,10.]],
            'counts_at_6400': {'racks':6400,'pinion_shaft_assemblies':6400,
                               'bearing_surfaces':12800,'ground_bolts':6400,
                               'ground_return_elements':6400,'dock_socket_patterns':6400},
            'checks':'profile convergence; exact rectangular fits; continuous disjoint phase intervals; contact-state replay; circle/backing intersection'}
    if args.svg:
        svg(args.svg)
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
