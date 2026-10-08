"""Rigid seated pitch equilibrium, N/mm; explicit scenarios, not measured priors."""
import importlib.util
import itertools
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'cheeks', Path(__file__).parents[1] / 'E-054/side_cheeks.py')
cheeks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cheeks)


def reactions(force, horizontal, x, height, left, right):
    # H applied at z=height, balanced by shelf friction at z=0.
    # Sum of moments: left*Rleft + right*Rright = F*x + H*height.
    rr = (force * (x-left) + horizontal * height) / (right-left)
    rl = force-rr
    assert abs(rl+rr-force) < 1e-10
    assert abs(left*rl+right*rr-force*x-horizontal*height) < 1e-10
    return rl, rr


def run():
    L, height = .8, 2.
    results = {}
    checks = 0
    for e in (.15, .35):
        assert not cheeks.geometry(e, 1.6, .4, .4, .8)['failures']
        overlap = .4+e+.02
        reach = max(.8, overlap+e+.1)+.02
        contacts = []
        for dr, dp in itertools.product((-e/2, e/2), repeat=2):
            # Coordinates relative to seated wing's leading edge.
            rack_left = overlap-reach+dr-dp
            rack_right = overlap+dr-dp
            lo, hi = max(0., rack_left), min(L, rack_right)
            assert lo == 0. and hi >= .4
            contacts.append((lo, hi))
        scenarios = []
        for inset in (0., .05, .1):
            left, right = inset, L-inset
            margin = min(min((lo+hi)/2-left, right-(lo+hi)/2)
                         for lo, hi in contacts)
            limit = margin/height
            for lo, hi in contacts:
                x = (lo+hi)/2  # Explicit uniform tooth-pressure scenario.
                for F, hratio in itertools.product((1., 10., 100.), (-limit, 0., limit)):
                    rl, rr = reactions(F, F*hratio, x, height, left, right)
                    assert min(rl, rr) >= -1e-10
                    checks += 1
                # Independent center-of-pressure criterion and reaction signs.
                for hratio in (-.25, -.1, 0., .1, .25):
                    cop = x+height*hratio
                    rr = reactions(10., 10.*hratio, x, height, left, right)
                    assert (min(rr) >= -1e-10) == (left-1e-10 <= cop <= right+1e-10)
                    checks += 1
            # Just outside the worst-case symmetric limit must tip a corner case.
            assert any(min(reactions(10., 10.*sign*(limit+1e-6), (lo+hi)/2,
                                     height, left, right)) < 0.
                       for lo, hi in contacts for sign in (-1, 1))
            scenarios.append({'shelf_contact_inset_mm': inset,
                              'uniform_pressure_min_margin_mm': round(margin, 6),
                              'symmetric_abs_H_over_F_limit': round(limit, 6)})
        # Arbitrary nonnegative tooth pressure can concentrate at either edge.
        # Vertical loads remain supported on the full wing; margin may be zero.
        for lo, hi in contacts:
            for x in (lo, hi):
                assert min(reactions(10., 0., x, height, 0., L)) >= -1e-10
        assert min(reactions(10., -.001, 0., height, 0., L)) < 0.
        assert min(reactions(10., 0., 0., height, .05, L-.05)) < 0.
        results[str(e)] = {'contact_intervals_mm': contacts, 'scenarios': scenarios}
    assert reactions(10., 0., .4, 2., 0., .8) == (5., 5.)
    # Zero height eliminates horizontal-force pitch moment, not friction demand.
    assert reactions(10., 20., .4, 0., 0., .8) == (5., 5.)
    results['equilibrium_checks'] = checks
    return results


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
