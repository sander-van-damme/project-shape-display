#!/usr/bin/env python3
"""Supplier acceptance ceilings and dimensional bounds, not quotes or yields."""
import json
from math import ceil, isclose


def supply(n=1024, usable=1., budget=1500., hardware=797.68,
           other=0., receiving_s=10., setup_h=2., install_h=10.94):
    assert n > 0 and 0 < usable <= 1
    attempts = ceil(n / usable)
    allowance = budget-hardware-other
    return dict(ordered=attempts, delivered_body_ceiling_usd=allowance/attempts,
                body_allowance_usd=allowance,
                maker_h=setup_h+install_h*n/1024+attempts*receiving_s/3600)


def radial_margin(diameter_error, screw_radius_error=0., axis_error=0.):
    # 0.15 radial nominal clearance; a diametral error contributes half.
    # Necessary radial-envelope bound only: does not prove helical flank fit.
    return .15-diameter_error/2-screw_radius_error-axis_error


def check():
    a=supply(); assert a['ordered']==1024
    assert isclose(a['delivered_body_ceiling_usd']*1024+797.68,1500.)
    assert supply(usable=.8)['ordered']==1280
    assert supply(n=17,usable=.8)['ordered']==22
    assert supply(budget=500)['delivered_body_ceiling_usd']<0
    assert isclose(supply(other=100)['body_allowance_usd'],602.32)
    assert isclose(radial_margin(.3),0.)
    assert radial_margin(.25+.002*3.5,.05)<0
    assert radial_margin(0.)==.15
    assert supply(receiving_s=60)['maker_h']>supply()['maker_h']
    # Common dimensional bias does not average away with more copies.
    assert all(radial_margin(.3, e)<=0 for e in [0.,.05,.1])


if __name__=='__main__':
    check()
    print(json.dumps(dict(
        quote_ceilings=[dict(n=n,usable=y,total_usd=b,**supply(n,y,b))
                        for n in [1024,4096,6400] for y in [1.,.8]
                        for b in [500,1000,1500]],
        coarse_receiving=[dict(usable=y,touch_s=t,**supply(usable=y,receiving_s=t))
                          for y in [1.,.8] for t in [10.,60.]],
        radial_margin_mm={
            'materialise_nominal_screw':radial_margin(.3),
            'protolabs_nominal_screw':radial_margin(.25+.002*3.5),
            'protolabs_assumed_0p05_screw_radius_error':radial_margin(.25+.002*3.5,.05)},
        tolerance_length_mm={'materialise':max(.3,.003*136),
                             'protolabs':.25+.002*136}),indent=2))
