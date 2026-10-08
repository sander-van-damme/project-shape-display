"""Sourced actuator-only cost exclusion; nominal ideal rack transmission.
Source provenance/limits: E-059. No loaded speed or hardware qualification.
"""
from fractions import Fraction as F
from math import pi, isclose
import json

PARTS = {
    'FS0307': dict(price=F('9.35'), seconds60=.09, stall_kgfcm=.6),
    'FS90': dict(price=F('7.90'), seconds60=.10, stall_kgfcm=1.5),
}


def evaluate(part, heads):
    angle = 2*pi/3  # published 120-degree range
    radius = .040/angle  # ideal rack effective radius, m
    torque = part['stall_kgfcm']*.0980665  # kgf cm -> N m
    omega = (pi/3)/part['seconds60']
    return dict(heads=heads, actuator_only_usd=float(heads*part['price']),
                cap500_rejected=heads*part['price']>500,
                complete_channel_ceiling_usd=float(F(250, heads)),
                minimum_price_reduction_fraction=float(1-F(250, heads)/part['price']),
                effective_radius_mm=1000*radius,
                nominal_no_load_speed_mm_s=1000*radius*omega,
                ideal_stall_force_N=torque/radius,
                nominal_80mm_motion_s=.080/(radius*omega))


def main():
    rows = {name:[evaluate(p,80*r) for r in range(1,81)]
            for name,p in PARTS.items()}
    assert all(x['cap500_rejected'] for group in rows.values() for x in group)
    assert PARTS['FS0307']['price']*80 == 748
    assert PARTS['FS90']['price']*80 == 632
    for name,p in PARTS.items():
        x=rows[name][0]
        assert isclose(x['nominal_80mm_motion_s'],4*p['seconds60'])
        # Independent conservation check: F v = torque omega at paired
        # mathematical endpoints; endpoints are NOT simultaneous operation.
        assert isclose(x['ideal_stall_force_N']*x['nominal_no_load_speed_mm_s']/1000,
                       p['stall_kgfcm']*.0980665*(pi/3)/p['seconds60'])
        assert all(a['actuator_only_usd'] < b['actuator_only_usd']
                   for a,b in zip(rows[name],rows[name][1:]))
    print(json.dumps(dict(evidence='catalog cost; ideal nominal transmission only',
                         tested_row_banks=160,
                         representatives={n:[g[i] for i in (0,1,2)] for n,g in rows.items()}),indent=2))

if __name__ == '__main__':
    main()
