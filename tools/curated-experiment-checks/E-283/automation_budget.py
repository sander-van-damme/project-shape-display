#!/usr/bin/env python3
"""Invert the E-283 maker ledger; necessary bounds, not automation evidence."""
import json
import math
from closed_stock import route, ledger


def budget(n, hours=32, side=0, usable=1., extra_setup_h=0.,
           batch=16, batch_s=60., reject_s=60.):
    """usable is a deterministic completed fraction, not independent probability.

    Residual seconds cover ALL attempted-body manual work: preparing/deburring,
    feeding every component, dosing, unloading, checking and routine cleanup.
    Batch time is additional shared operator work, not unattended cure/machine
    time. Reject time is additional disposal/diagnosis; remakes are in attempts.
    Accepted-pair installation remains in the inherited base.
    """
    assert n > 0 and 0 < usable <= 1 and batch > 0
    r = route(n, usable=usable)
    attempts = r['attempts']
    fixed = (ledger(n)['base_maker_h'][side] + (4, 12)[side]
             + (2, 4)[side] + extra_setup_h
             + (r['gang_groups'] * (60, 180)[side]
                + r['saw_strokes'] * (5, 15)[side]) / 3600)
    shared = math.ceil(attempts / batch) * batch_s
    rejected = (attempts - n) * reject_s
    room = (hours - fixed) * 3600 - shared - rejected
    return dict(attempts=attempts, fixed_h=fixed,
                shared_h=shared / 3600, reject_h=rejected / 3600,
                residual_s_per_attempt=room / attempts,
                feasible_even_at_zero_handling=room >= 0)


def checks():
    # Inversion independently reconstructs the target total, including signed
    # deficits: negative allowances are impossible, never clipped into a pass.
    for n in (1, 17, 1024, 4096, 6400):
        for usable in (1., .8):
            for side in (0, 1):
                r = budget(n, side=side, usable=usable)
                total = (r['fixed_h'] + r['shared_h'] + r['reject_h']
                         + r['attempts'] * r['residual_s_per_attempt'] / 3600)
                assert math.isclose(total, 32)
    # Manual E-283 adhesive route: ten 5-second touches and no batch surcharge.
    from end_assembly import comparison
    r = budget(1024, batch_s=0)
    assert math.isclose(r['fixed_h'] + 1024 * 50 / 3600,
                        comparison(1024, 'adhesive')[0]['total_maker_h'])
    a = budget(1024)
    b = budget(1024, extra_setup_h=8)
    assert math.isclose(a['residual_s_per_attempt']
                        - b['residual_s_per_attempt'], 8 * 3600 / 1024)
    assert budget(1024, usable=.8)['residual_s_per_attempt'] < a['residual_s_per_attempt']
    assert budget(17)['shared_h'] == 120 / 3600
    assert not budget(1024, side=1)['feasible_even_at_zero_handling']


if __name__ == '__main__':
    checks()
    print(json.dumps({str(n): {
        'low_16h': budget(n, hours=16),
        'low_32h': budget(n),
        'high_32h': budget(n, side=1),
        'low_32h_plus8h_setup': budget(n, extra_setup_h=8),
        'low_32h_plus8h_setup_80pct': budget(n, extra_setup_h=8, usable=.8),
    } for n in (1024, 4096, 6400)}, indent=2))
