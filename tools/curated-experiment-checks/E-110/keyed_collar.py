#!/usr/bin/env python3
"""Finite axisymmetric key screen. mm, N, MPa=N/mm2, J; no material priors.

Exact piecewise cylindrical solids, not contact FEA. Capacity is an ideal
parallel-key cut screen, NOT a lower bound on real capacity. --all emits every
case; no seed because enumeration and uncertainty corners are deterministic.
"""
import argparse
from dataclasses import dataclass, asdict
from itertools import product
from math import pi, ceil, isclose
import json


@dataclass(frozen=True)
class Geometry:
    radius: float
    gap: float
    depth: float
    width: float
    period: float
    length: float
    fraction: float = 1.0  # ideal angular segmentation; walls/seals omitted


def grooves(g, shift):
    # Finite track covers all z in collar for shifts 0..40 (one extra pitch).
    return [(i*g.period+shift, i*g.period+shift+g.width)
            for i in range(-ceil(40/g.period)-2, ceil(g.length/g.period)+2)]


def overlap(a, b, c, d):
    return max(0., min(b, d)-max(a, c))


def groove_length(g, shift):
    return sum(overlap(a, b, 0, g.length) for a, b in grooves(g, shift))


def phases(g):
    # Extrema of piecewise-linear volume occur at boundary crossings.
    events = {0., g.period}
    for edge in (0., g.width):
        for end in (0., g.length):
            events.add((end-edge) % g.period)
    events = sorted(events)
    return sorted(set(events+[(a+b)/2 for a, b in zip(events, events[1:])]))


def volume(g, shift):
    r, b, k = g.radius, g.radius+g.gap, g.depth
    inner = pi*(r*r-(r-k)**2)*groove_length(g, shift)
    # Fixed cup recesses have same profile at phase zero.
    outer = pi*((b+k)**2-b*b)*groove_length(g, 0.)
    return g.fraction*(pi*(b*b-r*r)*g.length+inner+outer)


def sliced_volume(g, shift, n):
    # Independent midpoint integration of actual radial solid boundaries.
    total = 0.
    for i in range(n):
        z = (i+.5)*g.length/n
        r = g.radius-(g.depth if (z-shift) % g.period < g.width else 0.)
        b = g.radius+g.gap+(g.depth if z % g.period < g.width else 0.)
        total += pi*(b*b-r*r)*g.length/n*g.fraction
    return total


def frozen_collision(g, freeze_shift, move_shift):
    """Volume where moved solid tail intersects the frozen collar solid.

    Split at every actual groove edge; evaluate the piecewise constant radial
    intervals exactly. Cup material always starts beyond maximum tail radius.
    """
    cuts = {0., g.length}
    for shift in (freeze_shift, move_shift):
        for a, b in grooves(g, shift):
            cuts.update(x for x in (a, b) if 0 < x < g.length)
    cuts = sorted(cuts)
    collision = 0.
    for a, b in zip(cuts, cuts[1:]):
        z = (a+b)/2
        original_r = g.radius-(g.depth if (z-freeze_shift) % g.period < g.width else 0.)
        moved_r = g.radius-(g.depth if (z-move_shift) % g.period < g.width else 0.)
        collision += max(0., pi*(moved_r*moved_r-original_r*original_r))*(b-a)
    return collision*g.fraction


def screen(g, tau, sigma, error, force=10.):
    # error is a coherent bound on combined radial closure, independently on
    # key depth/width loss. It is NOT an FDM distribution or dimensional sigma.
    k, w = g.depth-error, g.width-error
    clearance = g.gap-error
    states = phases(g)
    # Only complete keys credited. Arbitrary phase can lose an edge key.
    n = min(sum(a >= -1e-9 and b <= g.length+1e-9
                for a, b in grooves(g, s)) for s in states)
    nc = sum(a >= -1e-9 and b <= g.length+1e-9 for a, b in grooves(g, 0.))
    r, b = g.radius, g.radius+g.gap
    capacity = 0.
    if k > 0 and w > 0:
        capacity = g.fraction*min(n*tau*2*pi*r*w,
                                 n*sigma*pi*(r*r-(r-k)**2),
                                 nc*tau*2*pi*b*w,
                                 nc*sigma*pi*((b+k)**2-b*b))
    vs = [volume(g, s) for s in states]
    # Full periodic 40-mm track; occupancy in exiting grooves if completely wet.
    carried = g.fraction*pi*(r*r-(r-g.depth)**2)*40*g.width/g.period
    failures = []
    if clearance <= 0: failures.append('molten_radial_collision_bound')
    if k <= 0 or w <= 0: failures.append('key_erased_by_error_bound')
    if capacity < force: failures.append('ideal_key_cut_below_load')
    if 2*(b+g.depth+.3) > 5.08: failures.append('pitch_with_assumed_0.3mm_cup_wall')
    return dict(geometry=asdict(g), tau=tau, sigma=sigma, error=error,
                full_keys=n, ideal_cut_N=capacity, clearance_mm=clearance,
                volume_mm3=[min(vs), max(vs)], displacement_mm3=max(vs)-min(vs),
                wetted_export_mm3=carried,
                board_W_at_0_5_J_mm3_30s=6400*max(vs)*.5/30,
                failures=failures)


def verify():
    g = Geometry(1.5, .1, .2, .4, 1., 5.)
    assert isclose(volume(g, 0), volume(g, .713), abs_tol=1e-10)
    # Midpoint quadrature converges to exact interval integral, off-grid holdout.
    h = Geometry(1.37, .17, .23, .37, 1.13, 5.27)
    exact = volume(h, .193)
    errors = [abs(sliced_volume(h, .193, n)-exact) for n in (1000, 10000, 100000)]
    assert errors[-1] < .001 and errors[-1] < errors[0]
    # Independent brute phase samples stay within exact event extrema.
    ext = [volume(h, p) for p in phases(h)]
    for i in range(1001):
        v = volume(h, h.period*i/1000)
        assert min(ext)-1e-10 <= v <= max(ext)+1e-10
    # Degenerate smooth annulus and fraction scaling; collision fault injection.
    smooth = Geometry(1.5, .1, 0, .4, 1, 5)
    assert isclose(volume(smooth, .32), pi*(1.6**2-1.5**2)*5)
    half = Geometry(1.5, .1, .2, .4, 1, 5, .5)
    assert isclose(volume(half, .123)*2, volume(g, .123))
    assert 'molten_radial_collision_bound' in screen(g, 1, 5, .1)['failures']
    assert screen(g, 1, 5, .25)['ideal_cut_N'] == 0
    # Actual frozen-collar / moved-tail intersections. Full-period endpoint
    # fits but the intervening trajectory collides: endpoint-only is inadequate.
    assert frozen_collision(g, 0., 0.) == 0.
    assert frozen_collision(g, 0., .1) > .8
    assert frozen_collision(g, 0., -.1) > .8
    assert frozen_collision(g, 0., 1.) < 1e-10
    assert frozen_collision(smooth, 0., .1) == 0.
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    errors = verify()
    rows = []
    # Two geometry families (annular / ideal sector bridges); alloy versus
    # thermoplastic does not create another geometry family or imply properties.
    for gap, depth, width, length, fraction, strengths, error in product(
            (.1, .2), (.1, .2, .3), (.25, .5), (2., 5., 10.), (1., .25),
            ((.25, 1.), (1., 5.), (5., 20.)), (0., .05, .15)):
        rows.append(screen(Geometry(1.5, gap, depth, width, 1., length, fraction),
                           *strengths, error))
    summary = []
    for strengths, error, fraction in product(((.25, 1.), (1., 5.), (5., 20.)),
                                               (0., .05, .15), (1., .25)):
        subset = [r for r in rows if (r['tau'], r['sigma']) == strengths
                  and r['error'] == error and r['geometry']['fraction'] == fraction]
        passed = [r for r in subset if not r['failures']]
        summary.append(dict(strengths=strengths, error=error, fraction=fraction,
                            count=len(passed), minimum_volume_case=
                            min(passed, key=lambda r:r['volume_mm3'][1]) if passed else None))
    witness = Geometry(1.5, .1, .2, .4, 1., 5.2)
    output = dict(cases=len(rows), failures={reason:sum(reason in r['failures'] for r in rows)
                  for reason in sorted({f for r in rows for f in r['failures']})},
                  quadrature_errors_mm3=errors, summary=summary,
                  witness=screen(witness, 1, 5, .05),
                  witness_frozen_collision_mm3=frozen_collision(witness, 0., .1))
    if args.all: output['population'] = rows
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
