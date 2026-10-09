"""Finite polygon/prism screen for a shared-energy command writer (mm, seconds).
All geometry/error/acceleration inputs are epistemic bounds, not process priors.
No contact dynamics, retention model, fabrication, or manufacturing yield claim.
Run without arguments for checks and compact reproducible results; --svg PATH
exports the actual generated opposed profiles for inspection (not retained CAD).
"""
import argparse
import itertools
import json
import math
from dataclasses import dataclass
from pathlib import Path

PITCH = 5.08
STROKE = 1.2
BOSS_X = .8
LEAD_GAP = .2
DWELL = .4
LIFT = 1.2


def cycloid(u):
    return u - math.sin(2 * math.pi * u) / (2 * math.pi)


@dataclass(frozen=True)
class Cam:
    ramp: float = 3.
    boss_y: float = .6
    wall: float = .6
    overtravel: float = 0.
    segments: int = 160

    @property
    def length(self):
        return self.ramp + DWELL

    def center(self, s):
        u = min(1., max(0., s / self.ramp))
        return -LEAD_GAP + (STROKE + LEAD_GAP + self.overtravel) * cycloid(u)

    def polygon(self, reset=False):
        # Filled cam material left of its pushing edge. A finite square boss
        # contacts the maximum edge x within its occupied y band.
        outer = -BOSS_X / 2 - LEAD_GAP - self.wall
        edge = [(self.center(self.ramp * i / self.segments) - BOSS_X / 2,
                 self.ramp * i / self.segments) for i in range(self.segments + 1)]
        p = [(outer, 0.)] + edge + [(edge[-1][0], self.length), (outer, self.length)]
        return [(STROKE - x, y) for x, y in p] if reset else p


def clip(poly, axis, bound, above):
    """Sutherland-Hodgman half-plane clip; preserves the actual solid profile."""
    if not poly:
        return []
    result = []
    a = poly[-1]
    ain = a[axis] >= bound if above else a[axis] <= bound
    for b in poly:
        bin_ = b[axis] >= bound if above else b[axis] <= bound
        if ain != bin_:
            t = (bound - a[axis]) / (b[axis] - a[axis])
            result.append(tuple(a[j] + t * (b[j] - a[j]) for j in (0, 1)))
        if bin_:
            result.append(b)
        a, ain = b, bin_
    return result


def band(poly, lo, hi):
    return clip(clip(poly, 1, lo, True), 1, hi, False)


def area(poly):
    return abs(sum(a[0] * b[1] - b[0] * a[1]
                   for a, b in zip(poly, poly[1:] + poly[:1]))) / 2 if poly else 0.


def overlap(poly, x, y, width=BOSS_X, depth=.6):
    p = band(poly, y - depth / 2, y + depth / 2)
    return area(clip(clip(p, 0, x - width / 2, True), 0, x + width / 2, False))


def demand(poly, y, depth, reset=False, width=BOSS_X):
    p = band(poly, y - depth / 2, y + depth / 2)
    if not p:
        return None
    return min(x for x, _ in p) - width / 2 if reset else max(x for x, _ in p) + width / 2


def trace(cam, old, command, steps=160):
    """Contact -> terminal dwell -> free exit, with hard stops at 0 and d.
    Output retention on separation is an explicit boundary condition.
    Translation sign makes the follower sample the cam from y=0 to length.
    """
    reset = command == 'reset'
    p = cam.polygon(reset)
    x = old * STROKE
    collisions = 0
    neighbor_max = 0.
    axial_neighbor_max = 0.
    max_penetration = 0.
    for i in range(steps + 1):
        y = -.5 * cam.boss_y - .1 + (cam.length + cam.boss_y + .2) * i / steps
        if command != 'bypass' and -cam.boss_y / 2 <= y <= cam.length + cam.boss_y / 2:
            needed = demand(p, y, cam.boss_y, reset)
            if needed is not None:
                x = min(x, needed) if reset else max(x, needed)
                x = min(STROKE, max(0., x))
            collision = overlap(p, x, y, depth=cam.boss_y)
            max_penetration = max(max_penetration, collision)
            collisions += collision > 1e-9
            # All opposite-state lateral neighbors, not just same-state copies.
            for col in (-1, 1):
                for state in (0, 1):
                    neighbor_max = max(neighbor_max, overlap(
                        p, col * PITCH + state * STROKE, y, depth=cam.boss_y))
            for row in (-1, 1):
                for state in (0, 1):
                    axial_neighbor_max = max(axial_neighbor_max, overlap(
                        p, state * STROKE, y + row * PITCH, depth=cam.boss_y))
        # Raised bypass is disjoint in z: blade [1.4,2.0], boss [0,1].
    return dict(final_mm=x, collisions=collisions, max_overlap_mm2=max_penetration,
                neighbor_overlap_mm2=neighbor_max, axial_neighbor_overlap_mm2=axial_neighbor_max)


def geometry_checks():
    cam = Cam()
    outcomes = {}
    for old, command in itertools.product((0, 1), ('set', 'reset', 'bypass')):
        result = trace(cam, old, command)
        expected = old * STROKE if command == 'bypass' else STROKE * (command == 'set')
        assert abs(result['final_mm'] - expected) < 1e-10
        assert result['collisions'] == 0 and result['neighbor_overlap_mm2'] < 1e-9
        assert result['axial_neighbor_overlap_mm2'] < 1e-9
        outcomes[f'{old}_{command}'] = result
    # Reuse these actual finite-path outcomes through every 2x2 old/new map.
    maps = list(itertools.product((0, 1), repeat=4))
    for old, target in itertools.product(maps, repeat=2):
        state = list(old)
        for row in range(2):
            for col in range(2):
                i = 2 * row + col
                # Separate stages: set ones, then reset zeros; unchanged bypass.
                if old[i] != target[i]:
                    cmd = 'set' if target[i] else 'reset'
                    state[i] = round(outcomes[f'{old[i]}_{cmd}']['final_mm'] / STROKE)
        assert tuple(state) == target
    # Same-station opposed blades overlap on their terminal plateaus. A reset
    # blade descending past the parked set blade has an unavoidable collision.
    common_x = STROKE - BOSS_X
    assert common_x > 0
    prism_overlap = common_x * DWELL * .6
    # Independent polygon rectangle clipping reconstructs that witness.
    for p in (cam.polygon(), cam.polygon(True)):
        assert math.isclose(overlap(p, STROKE / 2, cam.ramp + DWELL / 2,
                                  width=common_x, depth=DWELL), common_x * DWELL,
                            abs_tol=1e-10)
    # Actual stuck set blade corrupts an intended unchanged zero on the next row.
    assert trace(cam, 0, 'set')['final_mm'] == STROKE
    # Positive overtravel hits the hard stop, rather than being silently accepted.
    assert trace(Cam(overtravel=.1), 0, 'set')['collisions'] > 0
    assert trace(Cam(overtravel=.1), 1, 'reset')['collisions'] > 0
    assert trace(cam, .5, 'set')['final_mm'] == STROKE
    assert trace(cam, .5, 'reset')['final_mm'] == 0.
    # Entire gate-lift path fits between adjacent-row y envelopes. Test both
    # schedule endpoints and midpoint under +/-0.2 relative head/row errors.
    # Disjoint xy means every intermediate blade z is clear.
    mid = (cam.length + PITCH) / 2
    for reset, bx, sx, dw, sy in itertools.product(
            (False, True), (-.1, .1), (-.1, .1), (-.1, .1), (-.2, .2)):
        p = [(x+bx,y) for x,y in cam.polygon(reset)]
        free = PITCH - cam.length - cam.boss_y - .4
        for row, state, phase in itertools.product((0, -1), (0, 1), (-1, 0, 1)):
            assert overlap(p, state * STROKE + sx,
                           mid + phase * free / 2 + row * PITCH + sy,
                           width=BOSS_X + dw, depth=cam.boss_y) < 1e-9
    return dict(nominal_paths=outcomes, exhaustive_2x2_maps=256,
                stacked_gate_collision_mm3=prism_overlap,
                stuck_set_corrupts_next_zero=True, hard_stop_negative_control=True)


def corner_checks(e=.1):
    cam = Cam()
    rows = []
    # Coherent cam position, stop position and full boss-width error. Values
    # can apply to all 80 columns: no independent-cell averaging is used.
    for shift, stop, dw in itertools.product((-e, e), repeat=3):
        poly = [(x + shift, y) for x, y in cam.polygon()]
        y = cam.ramp + DWELL / 2
        needed = demand(poly, y, cam.boss_y, width=BOSS_X + dw)
        mismatch = needed - (STROKE + stop)
        assert math.isclose(mismatch, shift - stop + dw / 2, abs_tol=1e-12)
        # Direct clipping at manufactured endpoint witnesses solid interference.
        collision = overlap(poly, STROKE + stop, y, width=BOSS_X + dw, depth=cam.boss_y)
        assert (collision > 1e-10) == (mismatch > 0)
        rows.append(mismatch)
    assert math.isclose(min(rows), -2.5 * e, abs_tol=1e-12)
    assert math.isclose(max(rows), 2.5 * e, abs_tol=1e-12)
    return dict(error_mm=e, mismatches_mm=rows, min_overtravel_to_reach_mm=2.5 * e,
                max_overtravel_without_collision_mm=-2.5 * e,
                rigid_robust_completion=False if e else True)


def screen(cam, banks, e=.1, gate_accel=20., proof=.001, transport_accel=20.):
    # Open-loop gate schedule: head and row each have +/-e phase uncertainty.
    # Expand BOTH ends of the occupied interval by 2e; a common unmeasured
    # head shift changes the safe schedule even though it cancels from pitch.
    free = PITCH - cam.length - cam.boss_y - 4 * e
    speed = .00508 / (24 * banks / 3440)
    gate_time = 2 * math.sqrt(LIFT / 1000 / gate_accel)
    # Two separate y stations => one full pitch of head overhang and flushing.
    # Conservative itinerary: return empty between 43 unidirectional masks.
    rows = 80 // banks
    scan_mm = (rows - 1) * PITCH + PITCH + cam.length + cam.boss_y + 4 * e
    # 43 forward writes, 42 empty returns; no compulsory final return.
    straight_roundtrip_s = 85 * scan_mm / 1000 / speed
    speed_cap = max(0., free / 1000 / (gate_time + proof))
    def leg_time(distance, v):
        if not v:
            return None
        return (distance / v + v / transport_accel if distance >= v * v / transport_accel
                else 2 * math.sqrt(distance / transport_accel))
    leg = leg_time(scan_mm / 1000, speed_cap)
    # A failed withdrawal is only declared after its stroke time plus proof.
    # Cancellation must then stop translation before the next row envelope.
    ready = gate_time + proof
    fault_cap = (2 * free / 1000 / (math.sqrt(ready * ready + 2 * free / 1000 / transport_accel)
                                  + ready)) if free > 0 else 0.
    fault_leg = leg_time(scan_mm / 1000, fault_cap)
    if fault_cap:
        assert math.isclose(fault_cap * ready + fault_cap ** 2 / (2 * transport_accel),
                            free / 1000, abs_tol=1e-12)
    channel_count = 160 * banks
    return dict(banks=banks, ramp_mm=cam.ramp, boss_y_mm=cam.boss_y,
                wall_mm=cam.wall, gate_accel_m_s2=gate_accel, free_switch_mm=free,
                gate_time_ms=1000 * gate_time, switch_window_ms=free / speed,
                one_lane_switch_pass=free / 1000 / speed > gate_time + proof,
                boundary_speed_m_s=speed,
                brake_margin_mm=free - 1000 * (speed * (gate_time + proof) + speed ** 2 / (2 * transport_accel)),
                two_gate_channels=channel_count,
                allowance_per_gate_USD=250 / channel_count,
                one_way_scan_mm=scan_mm,
                scan_return_plus_6s=straight_roundtrip_s + 6,
                switching_speed_cap_m_s=speed_cap,
                at_switch_cap_with_turns_plus_6s=85 * leg + 6 if leg else None,
                withdrawal_fault_speed_cap_m_s=fault_cap,
                at_fault_cap_with_turns_plus_6s=85 * fault_leg + 6 if fault_leg else None)


def discretization():
    # Analytic finite-square support differs from a point follower: lead corner
    # evaluates f(y+h/2). Check actual clipped polyline against this holdout.
    errors = []
    cam0 = Cam()
    for n in (40, 80, 160, 320):
        cam = Cam(segments=n)
        p = cam.polygon()
        err = 0.
        for i in range(503):
            y = cam.length * i / 502
            exact = cam.center(min(cam.length, y + cam.boss_y / 2))
            err = max(err, abs(demand(p, y, cam.boss_y) - exact))
        errors.append(err)
    assert all(a > 3 * b for a, b in zip(errors, errors[1:]))
    # Geometry is in mm, acceleration in m/s2. Capture starts at f(s)=old=0,
    # inside the nominal lead-in; its nonzero slope produces a velocity jump.
    lo, hi = 0., 1.
    for _ in range(60):
        u = (lo + hi) / 2
        if cam0.center(u * cam0.ramp) < 0:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    slope = (STROKE + LEAD_GAP) / cam0.ramp * (1 - math.cos(2 * math.pi * u))
    return dict(polyline_max_error_mm=errors, capture_u=u,
                capture_slope=slope, capture_speed_at_B4_m_s=slope * (.00508 / (24 * 4 / 3440)))


def svg(path):
    cam = Cam()
    def polygon(p, color):
        points = ' '.join(f'{100 * x:.4f},{100 * y:.4f}' for x, y in p)
        return f'<polygon points="{points}" fill="{color}" stroke="black" stroke-width="1"/>'
    # Actual synthesized finite profiles, side by side at one-pitch separation.
    items = [polygon(cam.polygon(), '#88bbee'),
             polygon([(x, y + PITCH) for x, y in cam.polygon(True)], '#eeaa77')]
    Path(path).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-180 -70 600 1050">'
                         + ''.join(items) + '</svg>')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--svg')
    args = parser.parse_args()
    geometries = [Cam(ramp=l, boss_y=h, wall=w)
                  for l, h, w in itertools.product((2., 3., 4.), (.6, 1.), (.6, .8))]
    # All finite nominal profiles are replayed, not accepted via scalar bounds.
    section_results = []
    for cam in geometries:
        axial_max = 0.
        for old, cmd in itertools.product((0, 1), ('set', 'reset', 'bypass')):
            r = trace(cam, old, cmd, steps=80)
            assert r['collisions'] == 0 and r['neighbor_overlap_mm2'] < 1e-9
            axial_max = max(axial_max, r['axial_neighbor_overlap_mm2'])
        section_results.append(dict(ramp_mm=cam.ramp, boss_y_mm=cam.boss_y, wall_mm=cam.wall,
                                    axial_overlap_mm2=axial_max,
                                    free_envelope_mm=PITCH-cam.length-cam.boss_y))
    if args.svg:
        svg(args.svg)
    print(json.dumps(dict(checks=geometry_checks(), convergence=discretization(),
                          corners=[corner_checks(e) for e in (0., .05, .1, .2)],
                          generated_sections=section_results,
                          scenarios=[screen(c, b, gate_accel=a) for c, b, a in itertools.product(
                              geometries, (1, 2, 4, 8, 16, 20), (20., 100.))]), indent=2))


if __name__ == '__main__':
    main()
