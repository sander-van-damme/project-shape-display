#!/usr/bin/env python3
"""E-197: deterministic necessary-condition screens, not a qualified actuator.
SI internally except labelled diaphragm arguments; all scenarios in main().
No dependencies, generated files, random priors or hidden purchased components.
"""
import itertools
import json
import math

FARADAY = 96485.33212
R_GAS = 8.314462618
TEMP = 298.15
P0 = 101325.0


def advance(q, rate, k, t):
    """Generated-gas charge-equivalent inventory; rate is net production A."""
    return q + rate * t if k == 0 else q * math.exp(-k*t) + rate * (-math.expm1(-k*t))/k


def window(rows, slot, hold, k, spread=0, gain=0, threshold=0):
    """Earliest full-only target vs never-selected cell receiving every half slot.
    Production and threshold bounds may be spatially/batch correlated.
    Different fast/slow k corners are allowed; no probability is assigned.
    """
    fast, slow = k*(1+spread), k*(1-spread)
    target = advance(0, 1, fast, slot) * math.exp(-fast*((rows-1)*slot+hold))
    half = advance(0, 1, slow, rows*slot)
    r_max = target/half * (1-gain)/(1+gain) * (1-threshold)/(1+threshold)
    # Nominal full-pulse peak divided by nominal opening threshold.
    pulse = advance(0, 1, k, slot)
    overdrive = math.inf if target == 0 else pulse*(1+threshold)/((1-gain)*target)
    return {'r_max': r_max, 'minimum_nominal_pulse_multiple': overdrive}


def diaphragm(radius_mm, stroke_mm, depth_mm, preload_n, spring_n_mm):
    """Isothermal gas over incompressible liquid, rigid piston-equivalent membrane.
    Initial nonreactive dead gas P0*V0; excess H2/O2 creates pressure and stroke.
    No nanobubble Laplace pressure, dissolution, membrane inertia or seal friction.
    """
    a = math.pi*(radius_mm*1e-3)**2
    x, v0, ks = stroke_mm*1e-3, a*depth_mm*1e-3, spring_n_mm*1e3
    force = preload_n + ks*x
    p = P0 + force/a
    n = (p*(v0+a*x)-P0*v0)/(R_GAS*TEMP)
    charge = 4*FARADAY*n/3
    work = preload_n*x + ks*x*x/2
    return {'charge_C': charge, 'pressure_Pa': p, 'force_N': force,
            'work_J': work, 'volume_mm3': (v0+a*x)*1e9}


def copper_roundtrip(thickness_um, current_a_cm2, efficiency=1):
    # E-196 Cu(II) mass/charge conversion, not an empirical switching rate.
    return 2*(thickness_um/1000)*100*27.208906/(efficiency*current_a_cm2)


def check():
    assert advance(3, 2, 0, 4) == 11
    assert math.isclose(advance(0, 1, 2, 1), (1-math.exp(-2))/2)
    assert math.isclose(window(80, .01, .2, 0)['r_max'], 1/80)
    assert window(80, .01, .2, 0)['minimum_nominal_pulse_multiple'] == 1
    # Exhaust all histories in a 6-row analogue; extremal argument uses positivity.
    # A never-target cell sees half/zero, including half at its own row.
    k, dt, r = 3, .01, .2
    maxima = []
    for bits in itertools.product([0, 1], repeat=6):
        q = 0
        for b in bits:
            q = advance(q, b*r, k, dt)
            maxima.append(q)
    assert math.isclose(max(maxima), advance(0, r, k, 6*dt))
    minima = []
    for selected in range(6):
        for bits in itertools.product([0, 1], repeat=5):
            rates = iter(bits)
            q = 0
            for i in range(6):
                q = advance(q, 1 if i == selected else r*next(rates), k, dt)
            minima.append(advance(q, 0, k, .2))
    assert math.isclose(min(minima), advance(0, 1, k, dt)*math.exp(-k*(5*dt+.2)))
    # Real V/2 matrix witness: row r=+1/2, selected columns=-1/2,
    # other wires=0. Electrolytic gas depends on magnitude, not polarity.
    target_v, unwanted_v = [], []
    for row in range(6):
        cols = {1} if row < 5 else {2}
        if row == 0:
            cols.add(0)
        target_v.append(abs((.5 if row == 0 else 0)-(-.5 if 0 in cols else 0)))
        unwanted_v.append(abs((.5 if row == 5 else 0)-(-.5 if 1 in cols else 0)))
    assert target_v == [1,0,0,0,0,0] and unwanted_v == [.5]*6
    # Direct quadrature of the production/decay ODE, not the analytical recurrence.
    errors = []
    for nstep in [10, 20, 40]:
        q, h = .13, .2/nstep
        for _ in range(nstep):
            f = lambda y: .7-3*y
            a = f(q); b = f(q+h*a/2); c = f(q+h*b/2); d = f(q+h*c)
            q += h*(a+2*b+2*c+d)/6
        errors.append(abs(q-advance(.13, .7, 3, .2)))
    assert errors[0] > errors[1]*14 > errors[2]*14*14
    # Independent gas-law reconstruction and zero-stroke/no-preload limits.
    for radius, x, preload, spring in itertools.product([.25, .5, 1], [0, .025, .2], [0, .02], [0, .1]):
        z = diaphragm(radius, x, .1, preload, spring)
        area = math.pi*(radius*1e-3)**2
        n_total = P0*area*.0001/(R_GAS*TEMP) + 3*z['charge_C']/(4*FARADAY)
        reconstructed_p = n_total*R_GAS*TEMP/(area*(.1+x)*1e-3)
        assert math.isclose(reconstructed_p, z['pressure_Pa'], rel_tol=1e-12)
        if x == 0 and preload == 0:
            assert z['charge_C'] == 0
    # A preload at a hard stop has a finite breakaway charge even at x=0.
    assert diaphragm(.5, 0, .1, .02, .1)['charge_C'] > 0
    assert math.isclose(copper_roundtrip(1, 1), 5.4417812)
    return {'rk4_inventory_errors_C': errors, 'enumerated_histories': 64+6*32}


def move_time(distance_mm, speed=200, accel=5000):
    return 2*math.sqrt(distance_mm/accel) if distance_mm <= speed*speed/accel else distance_mm/speed+speed/accel


def main():
    out = {'evidence': 'scenario calculations and exact linear-state histories; self-review', 'checks': check()}
    out['mask_windows'] = [dict(rows=n, k_s=k, **window(n, .01, .24, k, .25, .1, .1))
                           for n in [80, 20, 10, 5, 1] for k in [0, .1, 1, 10, 100]]
    out['zero_decay_nominal_r_limit'] = {str(n): 1/n for n in [80, 20, 10, 5, 1]}
    # Grid of competing uncertainty bounds, not random yield estimates.
    grid = [dict(rows=n, slot_s=t, hold_s=h, k_s=k, half_ratio=r,
                 **window(n,t,h,k,.25,.1,.1))
            for n,t,h,k,r in itertools.product([80,20,10,5,1], [.001,.01,.05],
                 [.05,.2,.5], [0,.1,1,10,100], [.001,.01,.1,.25,.5])]
    survivors = [x for x in grid if x['half_ratio'] < x['r_max'] and x['minimum_nominal_pulse_multiple'] <= 2]
    out['grid'] = {'cases':len(grid), 'windows_with_minimum_nominal_pulse_at_most_2':len(survivors),
                   'by_rows':{str(n):sum(x['rows']==n for x in survivors) for n in [80,20,10,5,1]}}
    out['diaphragms'] = []
    for rad,x,f in itertools.product([.25,.5,1], [.025,.1,.2], [.005,.02,.1]):
        z = diaphragm(rad,x,.1,f,.1)
        z.update(radius_mm=rad, stroke_mm=x, preload_N=f,
                 minimum_current_10ms_A=z['charge_C']/.01,
                 ideal_board_charge_C=6400*z['charge_C'])
        out['diaphragms'].append(z)
    # Independent selected-only drive: charge full home->old->new->home path.
    # Parallel 80-head row; exhaustive 1-mm old/new grid at 40-mm travel.
    # .04 s support/reader allocation, actual rest-to-rest index, one row retry.
    route = max(move_time(old)+move_time(abs(new-old))+move_time(new)
                for old,new in itertools.product(range(41), repeat=2))
    assert math.isclose(route, .52)
    # Independent continuous upper bound: total path <=80 mm and <=3 ramps.
    assert math.isclose(route, 80/200+3*200/5000)
    index = move_time(5.08)
    out['direct_route_allocation'] = {'worst_1mm_grid_route_s':route, 'index_s':index,
                                    'speed_mm_s':200, 'accel_mm_s2':5000}
    out['serial_times'] = [dict(banks=b, reset_s=r,
                               map_s=6+(math.ceil(80/b)+1)*(.01+route+r+.04)+math.ceil(80/b)*index+move_time((math.ceil(80/b)-1)*5.08))
                           for b,r in itertools.product([1,2,4,8], [.001,.05,.4,10])]
    local = []
    for start in range(76):
        bank_times = []
        for bank in range(4):
            changed = [row % 20 for row in range(start,start+5) if row//20 == bank]
            if changed:
                bank_times.append((len(changed)+1)*(.01+route+.05+.04)
                                  + len(changed)*index
                                  + move_time(changed[0]*5.08)+move_time(changed[-1]*5.08))
        local.append(6+max(bank_times))
    out['local_5x5_four_bank_reset_50ms_s'] = [min(local),max(local)]
    gas_ref = diaphragm(.5,.2,.1,.02,.1)['charge_C']
    out['driven_gas'] = [dict(k_s=k, charge_10ms_current_A=gas_ref/advance(0,1,k,.01),
                              hold_current_A=k*gas_ref,
                              reset_to_tenth_s=math.log(10)/k)
                         for k in [.1,1,10,100]]
    out['copper_roundtrip_s'] = {str(j):copper_roundtrip(1,j) for j in [.175,1,10]}
    out['impulse_work_comparison'] = [dict(force_N=f, stroke_mm=x, needed_uJ=f*x*1000,
                                          ideal_reported_work_ratio=1.2/(f*x*1000))
                                     for f,x in itertools.product([.005,.02,.1], [.025,.1,.2])]
    out['reported_impulse_reference'] = {'board_energy_J_one_pulse_each':6400*.0073,
                                         'mean_power_W_over_24s':6400*.0073/24,
                                         'peak_force_times_stroke_uJ_not_work':.49*.1*1000}
    print(json.dumps(out, indent=2, allow_nan=False))

if __name__ == '__main__':
    main()
