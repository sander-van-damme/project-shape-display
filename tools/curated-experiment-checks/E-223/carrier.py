"""E-223: necessary carrier constraints, not contact or hardware validation.

Standard library, deterministic. All dimensions/times are labelled scenarios
in the canonical result. No process probability or qualified brake is assumed.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

PITCH = 5.08
LEVELS = (0, 10, 20, 30, 40)


def overlap(stroke, separation=PITCH):
    # Material coordinates visited by point followers x=0 and x=separation.
    # Closed intervals: equality also requires the same material height.
    lo = max(-stroke, separation-stroke)
    hi = min(0., separation)
    return lo <= hi


def relief_on_run(heights, x):
    """Generous continuous piecewise-linear support; return/joins are granted.

    This bypasses the finite flat shoe's tendency to bridge narrow valleys.
    It cannot make failure of unchanged point followers less decisive.
    """
    if not 0 <= x <= PITCH*(len(heights)-1):
        raise ValueError('outside defined loaded run')
    i = min(int(x/PITCH), len(heights)-2)
    t = (x-i*PITCH)/PITCH
    return heights[i]*(1-t) + heights[i+1]*t


def main():
    # Independent material-identity and interval proofs, including equality.
    assert not overlap(PITCH-1e-9)
    assert overlap(PITCH) and overlap(80*PITCH)
    mismatches = sum(a != b for a,b in itertools.product(LEVELS, repeat=2))
    assert mismatches == 20
    # One-pitch exchange can supply a free leading code, but the second site's
    # target MUST be its upstream neighbor's old code.
    endpoints = sum(t1 == o0 for o0,o1,t0,t1 in
                    itertools.product(LEVELS, repeat=4))
    assert endpoints == 125   # of 625 arbitrary old/target pairs

    # Unchanged 0,40,0,40,... row: translating the prewritten run one pitch
    # lowers x=p by 40 mm and raises x=2p by 40 mm. These two sites can remain
    # unchanged while a distant third site requests a new height.
    trace = []
    for intervals in (16, 64, 256):
        descending = [relief_on_run((0,40,0), PITCH-PITCH*k/intervals)
                      for k in range(intervals+1)]
        ascending = [relief_on_run((0,40,0), 2*PITCH-PITCH*k/intervals)
                     for k in range(intervals+1)]
        assert descending[0] == ascending[-1] == 40
        assert descending[-1] == ascending[0] == 0
        trace.append(dict(intervals=intervals, unchanged_excursion_mm=40))

    # Finite broad support is more restrictive: r <= column height everywhere
    # under its foot, with equality somewhere. At stroke p an old height-40
    # support point enters an unchanged height-0 foot. No valley interpolation
    # or shape between samples can remove that material-point obstruction.
    assert relief_on_run((40,0), 0) > 0

    # Rate floors only: external programming and transport overlap perfectly.
    # Two global seconds match the E-222 allocation. No retry/support pass.
    writer_floor = [dict(seconds_per_code=tau,
        minimum_writers_for_floor_below_30=math.floor(6400*tau/28)+1)
        for tau in (.01,.02,.05,.10)]

    # Separate constant-code loops: each cell owns all five rigid code pads.
    cells=6400
    width=3.4
    base=2
    pad_volume_L=cells*width**2*sum(base+h for h in LEVELS)/1e6
    assert math.isclose(pad_volume_L, 8.13824)
    # Illustrated two-pulley route: top-run center spacing D=p, pulley R=4.
    # Adjacent inline loop end pulleys coincide. Box-isolated tiers are only
    # a sufficient alternative allocation, NOT a universal packing bound.
    D=PITCH; R=4.; H=base+max(LEVELS)
    assert math.isclose(D/2, PITCH-D/2)
    box_width=D+2*(R+H)
    tiers=math.ceil(box_width/PITCH)
    assert tiers == 20

    source=Path(__file__).resolve().parents[1]/'E-222'/'screen.py'
    spec=importlib.util.spec_from_file_location('e222',source)
    baseline=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    banks=baseline.first_banks(baseline.stack_service())
    assert banks == 8
    print(json.dumps(dict(
        evidence='necessary conditions; no constructed machine',
        unequal_unchanged_pairs_failing_at_one_pitch=f'{mismatches}/25',
        one_pitch_reachable_two_cell_endpoints=f'{endpoints}/625',
        continuous_witness=trace,
        bias_bounds_mm={str(e):dict(min_high_low_difference=40-2*e,
            greatest_neighbor_spacing=PITCH+2*e)
            for e in (.15,.35,.70)},
        transport_floor_406p4mm_at_200mm_s=80*PITCH/200,
        writer_floors=writer_floor,
        isolated_loop=dict(code_pads=5*cells, pulleys=2*cells,
            phase_retention_functions=cells, pad_stock_L=pad_volume_L,
            box_width_mm=box_width, box_isolated_tiers=tiers,
            box_isolated_depth_mm=tiers*2*(R+H),
            pad_print_hours_at_15_to_5mm3_s_10pct_scrap=
                [pad_volume_L*1e6/(rate*.9*3600) for rate in (15,5)]),
        e222=dict(banks=banks, forks=80*banks,shuttles=80*banks,
            seconds=baseline.schedule(baseline.stack_service(),banks))), indent=2))


if __name__ == '__main__':
    main()
