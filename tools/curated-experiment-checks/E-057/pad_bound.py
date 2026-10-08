"""Inset-pad necessary conditions, millimetres; deterministic bounds, no priors."""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('equilibrium', Path(__file__).parents[1]/'E-056/contact_equilibrium.py')
eq = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eq)


def intersection(a, b):
    return max(a[0], b[0]), min(a[1], b[1])


def run():
    L, h, amin = .8, 2., .42
    rows = []
    checks = 0
    for e in (.15, .35):
        o = .4+e+.02
        r = max(.8, o+e+.1)+.02
        for width in (.2, .4):
            for d in (0., .1):
                # Pawl-fixed pad [m,L-m]; retain >=width at every rack position.
                # Maximum inset follows from both pad width and worst rack edge.
                m = min((L-width)/2, amin-width)
                for family in ('pawl_fixed', 'rack_fixed'):
                    center = min(L/2, o-width/2)
                    pad = (m, L-m) if family == 'pawl_fixed' else (center-width/2, center+width/2)
                    # Rack-fixed centered pad must lie on the original tooth.
                    if family == 'rack_fixed':
                        assert o-r <= pad[0] and pad[1] <= o
                    margin = m-d if family == 'pawl_fixed' else min(pad[0], L-pad[1])-e-d
                    supported = margin >= 0
                    # Dense deterministic holdouts supplement affine endpoint proof.
                    for step in range(1001):
                        delta = -e+2*e*step/1000
                        tooth = (o-r+delta, o+delta)
                        p = pad if family == 'pawl_fixed' else (pad[0]+delta,pad[1]+delta)
                        lo, hi = intersection(intersection(p,tooth), (0.,L))
                        if supported:
                            assert hi-lo >= width-1e-10
                            for x in (lo,hi):
                                for sign in (-1,1):
                                    reactions = eq.reactions(10.,sign*10.*margin/h,x,h,d,L-d)
                                    assert min(reactions) >= -1e-9
                                    checks += 1
                    # An adverse endpoint realizes the claimed positive-margin bound.
                    if supported:
                        delta = -e
                        lo, hi = intersection(intersection(pad if family=='pawl_fixed' else (pad[0]+delta,pad[1]+delta), (o-r+delta,o+delta)), (0.,L))
                        assert min(eq.reactions(10.,-10.*(margin/h+1e-6),lo,h,d,L-d)) < 0
                    rows.append(dict(e=e, minimum_contact_width=width, shelf_edge_loss=d,
                                     family=family, pad=pad, signed_margin=round(margin,6),
                                     pitch_ratio_limit=round(margin/h,6) if supported else None))
    # Pawl-fixed optimum: increasing m violates contact width or pad width.
    for width in (.2,.4):
        m=min((L-width)/2,amin-width)+1e-6
        assert min(L-2*m,amin-m)<width
    return dict(rows=rows, equilibrium_checks=checks)


if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
