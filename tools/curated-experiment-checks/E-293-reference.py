#!/usr/bin/env python3
"""Shared three-depth reference control, not camera or calibration qualification.

Only d=b/(D-z)+a is fitted. Known heights and correspondence are granted.
Finite endpoint scenarios are witnesses, NOT certified worst-case bounds.
"""
import itertools
import json
import numpy as np


def disparity(z, D=300., b=90., a=.0002):
    return b / (D - np.asarray(z)) + a


def recover(d, step=25.):
    # Equal-depth reference steps at 0,h,2h. Algebraic inverse, no cap height.
    ratio = (d[2] - d[1]) / (d[1] - d[0])
    D = 2 * step * ratio / (ratio - 1)
    b = (d[1] - d[0]) * D * (D-step) / step
    a = d[0] - b / D
    return D, b, a


def height(d, params):
    D, b, a = params
    return D - b / (np.asarray(d) - a)


def main():
    refs = np.array([0., 25., 50.])
    zs = np.linspace(0., 50., 1001)
    truth = (300., 90., .0002)
    d = disparity(refs, *truth)
    fitted = recover(d)
    assert np.max(abs(np.array(fitted)-truth)) < 1e-9
    assert np.max(abs(height(disparity(zs), fitted)-zs)) < 1e-9
    # Independently check local identifiability by derivatives wrt (D,b,a).
    ranks = []
    for planes in ([0., 0., 0.], [0., 25., 25.], refs):
        t = 300-np.array(planes)
        J = np.column_stack((-90/t**2, 1/t, np.ones(3)))
        ranks.append(int(np.linalg.matrix_rank(J)))
    assert ranks == [1, 2, 3]
    # Exact coplanar alias: at zero, D=301 and b=90.3 give same reading.
    assert abs(disparity(0.,301.,90.3)-d[0]) < 1e-12
    plane_alias = float(height(disparity(50.), (301.,90.3,.0002))-50.)
    assert abs(plane_alias-1/6) < 1e-10
    rows=[]
    # Labelled reading error, not inferred from pixel count or iid noise.
    eps=.00015
    for signs in itertools.product((-1,1), repeat=3):
        observed=d+eps*np.array(signs)
        p=recover(observed)
        assert np.max(abs(disparity(refs,*p)-observed)) < 1e-12
        exact_error=np.max(abs(height(disparity(zs),p)-zs))
        target_error=max(np.max(abs(height(disparity(zs)+s*eps,p)-zs))
                         for s in (-1,1))
        rows.append(dict(signs=signs,fit=p,
                         exact_target_max_error_mm=float(exact_error),
                         perturbed_target_max_error_mm=float(target_error)))
    # A rigid vertical shift of head AND head-mounted references is invisible.
    shift=.5
    before=disparity(refs)
    after=disparity(refs+shift,D=300+shift)
    assert np.max(abs(before-after)) < 1e-12
    blind=height(disparity(zs,D=300+shift),truth)-zs
    assert np.max(abs(blind+shift)) < 1e-10
    # Board references moved together .2 mm also supply a false global datum.
    datum=.2
    wrong=recover(disparity(refs+datum))
    errors=height(disparity(zs),wrong)-zs
    assert np.max(abs(errors+datum)) < 1e-9
    # Original finite-camera summary bounds are not independent measurements.
    # Do not manufacture a posterior from them or call these 8 cases an envelope.
    print(json.dumps(dict(model='d=b/(D-z)+a; perfect reference identity and height',
          rank_by_distinct_depth=ranks,exact_fit=fitted,
          coplanar_alias_at_50_mm=plane_alias,reference_error_slope=eps,
          endpoint_scenarios=rows,head_shift_unseen_mm=shift,
          common_reference_datum_error_mm=datum,
          timing_seconds=dict(reference_scan=24*.1,
             dense_recalibrate_each_group={str(n):n/4*24*.1 for n in (1024,4096,6400)})),indent=2))


if __name__ == '__main__':
    main()
