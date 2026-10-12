#!/usr/bin/env python3
"""Dated supplier inputs + deterministic bounds; no qualified channel or BOM.

Source URLs and conditions are in E-259. Stdlib; JSON stdout is disposable.
Schedules reuse the unchanged E-258 maps and E-255 stopped-motion assumptions.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path
from functools import lru_cache

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v = load('player_view', 'E-258/player_view.py')
e = load('drive_envelope', 'E-256/drive_envelope.py')
r = v.s.v.rotary


def cost(n):
    count = 2*n
    reserve = r.costs(2, n=n)['reserve']  # still an unquoted allocation
    # 128/160 motors qualify for 100+; 64/80 dual boards qualify for 10-99.
    motor, driver = 1.56, 5.36 / 2
    subtotal = reserve + count*(motor+driver)
    return dict(outputs=count, dual_boards=count//2, allocated_reserve=reserve,
        motor_driver_unit=motor+driver, allocated_plus_quoted=subtotal,
        missing_per_output={budget:(budget-subtotal)/count for budget in (500,1000,1500)},
        encoder_motor_only=count*25.27,
        encoder_motor_driver_plus_reserve=reserve+count*(25.27+driver),
        # Kit is NOT compatible with the 130 motor; price pressure only.
        incompatible_kit_price_comparator=subtotal+(count//2)*8.42,
        motors_kg=count*.0175, motor_nominal_load_current_A=count*.25,
        motor_stall_current_A=count*.5,
        nominal_load_motor_electrical_W=6*count*.25,
        body_only_lanes=math.ceil(15/(v.s.WIDTH/n)),
        sequential_one_minute_channel_assembly_h=count/60)


@lru_cache(maxsize=None)
def terrain(n, neutral, depth):
    maps,labs = v.s.v.variants(n)
    maps,labs = v.s.connected_walls(maps,labs,n)
    target = v.aligned(maps,neutral,depth)
    start = v.s.flat(n,neutral)
    return target, start


def suite(n, neutral, depth, rpm, accel, proof=.02):
    target, start = terrain(n, neutral, depth)
    result = {}
    for policy, keys in v.s.SUITES.items():
        pairs = [(start,target[k]) for k in keys] + [(target[a],target[b])
                 for a,b in itertools.permutations(keys,2)]
        result[policy] = max(r.schedule(r.delta(a,b),2,pitch=v.s.WIDTH/n,
                    rpm=rpm,accel=accel,proof=proof)['seconds'] for a,b in pairs)
    result['paid_neutral'] = r.schedule(v.s.flat(n,neutral),2,
                        pitch=v.s.WIDTH/n,rpm=rpm,accel=accel,proof=proof)['seconds']
    # Separate adversarial full +/-40-mm changes, not a typical map.
    result['dense_40mm'] = r.schedule([[40 if (x+y)%2 else -40 for x in range(n)]
                    for y in range(n)],2,pitch=v.s.WIDTH/n,
                    rpm=rpm,accel=accel,proof=proof)['seconds']
    full_range=neutral+20
    result['dense_full_range'] = r.schedule([[full_range if (x+y)%2 else -full_range
                    for x in range(n)] for y in range(n)],2,pitch=v.s.WIDTH/n,
                    rpm=rpm,accel=accel,proof=proof)['seconds']
    return result


def drive_bounds():
    # 10 gf cm from supplier -> N mm. Reduction ratio and efficiency are assumptions.
    rated = 10*.00980665*10
    ratio, efficiency = 1.5, .7
    supplied = rated*ratio*efficiency
    without_J = e.torque(20,.3,.05,1000,0)
    j_ceiling = (supplied-without_J)/1000/(2*math.pi*1000)
    gear = 35*37/(13*10)
    counts = 12*gear
    return dict(motor_rated_Nmm=rated, assumed_ratio=ratio, assumed_efficiency=efficiency,
        rated_low_speed_output_rpm=3000/ratio, output_rated_Nmm=supplied,
        assumed_20g_accelerating_torque_without_J_Nmm=without_J,
        necessary_effective_J_ceiling_kgm2=j_ceiling,
        # This is encoder quantization only, not measured positioning precision.
        pololu_output_counts_per_rev=counts,
        pololu_nominal_mm_per_count=3/counts,
        pololu_edges_s_per_output_at2000=counts*2000/60,
        pololu_total_edges_s_128=counts*2000/60*128,
        pololu_total_edges_s_160=counts*2000/60*160,
        open_loop_10mm_error_bounds_mm=[10*(3000/4500-1),10*(6000/4500-1)],
        latency_travel_mm_at2000={ms:2000/60*3*ms/1000 for ms in (1,5,20)},
        initial_torque_budget_Nmm=e.torque(20,.3,.05,1000,1e-8))


def checks():
    # Independently enumerate purchased quantities; do not give 100-board discounts.
    for n in (64,80):
        c=cost(n)
        assert math.isclose(c['allocated_plus_quoted'],250+.02*n*n+110+2*n*1.56+n*5.36)
        assert c['dual_boards']*2==c['outputs']
        assert n*5.36 < 100*4.76  # buying surplus boards does not reduce this total
        for budget,residual in c['missing_per_output'].items():
            assert math.isclose(c['allocated_plus_quoted']+2*n*residual,budget)
    d=drive_bounds()
    assert math.isclose(d['motor_rated_Nmm'],.980665)
    assert math.isclose(d['pololu_output_counts_per_rev'],119.53846153846153)
    assert math.isclose(d['rated_low_speed_output_rpm'],2000)
    # Energy-consistent inertia ceiling and a failing tenfold-inertia case.
    assert math.isclose(e.torque(20,.3,.05,1000,d['necessary_effective_J_ceiling_kgm2']),d['output_rated_Nmm'])
    assert e.torque(20,.3,.05,1000,1e-6)>d['output_rated_Nmm']
    # Existing schedule reference, plus direction symmetry and no-op.
    base=suite(64,20,20,2000,1000)
    assert abs(base['mixed']-22.0835)<.001
    assert r.schedule([[0]*64 for _ in range(64)],2)['seconds']==0
    dense=[[40]*64 for _ in range(64)]
    assert r.schedule(dense,2)==r.schedule([[-40]*64 for _ in range(64)],2)
    return 'quantity tiers, unit conversion, budget reconciliation, inertia limit, E-258 anchor, no-op and signed symmetry'


def main():
    output=dict(verification=checks(),costs={n:cost(n) for n in (64,80)},drive=drive_bounds(),schedules=[])
    for n, neutral, rpm, accel in itertools.product((64,80),(20,30),(1500,2000),(200,1000)):
        output['schedules'].append(dict(n=n,neutral=neutral,depth=neutral,rpm=rpm,accel=accel,
                               seconds=suite(n,neutral,neutral,rpm,accel)))
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
