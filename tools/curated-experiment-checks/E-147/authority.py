#!/usr/bin/env python3
"""E-147: reset causality, isolated-source graphs and energy bounds.
SI internally. Explicit scenarios, not calibrated priors or hardware simulation.
Print disposable JSON; run assertions as model checks. No third-party packages.
"""
from collections import deque
from itertools import product
import json
import math


def connected(edges, start, end):
    todo, seen = [start], {start}
    while todo:
        a = todo.pop()
        if a == end:
            return True
        for u, v in edges:
            b = v if a == u else u if a == v else None
            if b is not None and b not in seen:
                seen.add(b)
                todo.append(b)
    return False


def source_graph(q, error=0., stuck_charge=False):
    # Single transfer slider, 1-mm stroke. q in metres.
    # Finite contact intervals, including adverse coherent edge displacement.
    charge = stuck_charge or q <= .0004 + error
    release = q >= .0006 - error
    edges = []
    if charge:
        edges.append(('live_source', 'store'))
    if release:
        edges.append(('store', 'release_actuator'))
    return connected(edges, 'live_source', 'release_actuator')


def repeat_trace(mode, cycles=20):
    # State cycle: supported/charge -> isolated/armed -> released -> spent/seat.
    # Ideal support and successful seats deliberately favor all variants.
    state, armed, count = 'supported', False, 0
    trace = []
    commands = ['charge', 'isolate', 'fire', 'seat'] * cycles
    if mode == 'held':
        commands = ['charge', 'isolate', 'fire', 'seat'] + ['fire'] * cycles
    for command in commands:
        if state == 'supported' and command == 'charge':
            state = 'charging'
        elif state == 'charging' and command == 'isolate':
            state, armed = 'isolated', True
        elif state == 'isolated' and armed and command == 'fire':
            state, armed, count = 'released', False, count + 1
        elif state == 'released' and command == 'seat':
            state = 'supported'
        trace.append((command, state, count))
    return count, trace


def local_reset_search(guard, depth=16):
    # Mechanical-state abstraction: seat, output motion, CLOSE and input work
    # are separate events. No local source exists after initialization.
    # State=(supported, armed, close_seen, net_available_energy_units, packets).
    # Each work event spends one unit into a guaranteed sink in this model.
    initial = (True, True, False, 2, 0)
    todo = deque([(initial, [])])
    seen = {initial}
    best = (initial, [])
    while todo:
        (supported, armed, edge, energy, count), trace = todo.popleft()
        if count > best[0][-1]:
            best = ((supported, armed, edge, energy, count), trace)
        if len(trace) >= depth:
            continue
        successors = []
        if armed and supported:
            successors.append(('release', (False, False, False, energy, count + 1)))
        if not supported:
            successors.append(('seat_without_drive', (True, armed, edge, energy, count)))
        if not edge:
            successors.append(('shared_CLOSE', (supported, armed, True, energy, count)))
        if supported and not armed:
            if guard == 'seat' or guard == 'edge' and edge:
                successors.append(('reset', (True, True, False, energy, count)))
            elif guard == 'work' and energy > 0:
                successors.append(('input_work_from_residual_energy',
                                   (True, True, False, energy - 1, count)))
        for event, new in successors:
            if new not in seen:
                seen.add(new)
                todo.append((new, trace + [event]))
    return {'states': len(seen), 'max_packets': best[0][-1], 'trace': best[1]}


def ledger(energy, loss, force, step=.002, gravity_fraction=0., recovery=0.,
           source_replenishes=False, max_packets=20):
    """Exact cycle ledger for a granted work barrier and return fraction.
    Input shaft/store pays loss joules before each transfer; return recovers
    recovery*loss. Gravity may inject gamma*F*step after downward motion.
    Equality cases are admissible energy counterexamples, not built mechanisms.
    Packet authorization does not imply that an unloaded output actually moves.
    """
    rows = []
    for n in range(max_packets):
        if source_replenishes:
            energy = max(energy, loss)
        if energy + 1e-14 < loss:
            break
        before = energy
        gravity = force * step
        energy += gravity_fraction * gravity - (1 - recovery) * loss
        heat = (1 - recovery) * loss + (1 - gravity_fraction) * gravity
        assert abs(before + gravity - energy - heat) < 1e-12
        rows.append(energy)
    return {'packets': len(rows), 'permitted_travel_mm': step * len(rows) * 1000,
            'remaining_J': energy}


def catch_compression(energy, force, stiffness):
    # energy at first contact; F may be signed. Grounded bilateral spring.
    d = (force + math.sqrt(force * force + 2 * stiffness * energy)) / stiffness
    assert abs(.5 * stiffness * d * d - energy - force * d) < 1e-11
    return d


def main():
    out = {}
    # Contact interval intersection is an exact certificate over all q,
    # not inferred from the sampled consistency checks.
    out['disconnect'] = []
    for e in (0., .000025, .00005, .0001, .00015):
        margin = .0002 - 2 * e
        sampled = any(source_graph(i * .001 / 2000, e) for i in range(2001))
        exact = (.0006 - e <= .0004 + e)
        assert sampled == exact
        out['disconnect'].append({'edge_error_mm': e * 1000,
                                  'dead_band_mm': margin * 1000,
                                  'live_source_overlap': exact})
    assert any(source_graph(i * .001 / 100, stuck_charge=True) for i in range(101))
    out['held_vs_repeating'] = {m: repeat_trace(m)[0] for m in ('held', 'repeat')}
    assert out['held_vs_repeating'] == {'held': 1, 'repeat': 20}
    out['reset_search'] = {g: local_reset_search(g) for g in ('seat', 'edge', 'work')}
    assert out['reset_search']['work']['max_packets'] == 3
    assert all(out['reset_search'][g]['max_packets'] > 3 for g in ('seat', 'edge'))
    out['energy_witnesses'] = {
        'irreversible_isolated': ledger(.005, .001, 1),
        'recycled_spring_zero_load': ledger(.001, .001, 0, recovery=1),
        'gravity_backfeed': ledger(.001, .001, 1, gravity_fraction=.5),
        'live_recharge': ledger(0, .001, 0, source_replenishes=True),
        'small_gravity_backfeed': ledger(.00125, .001, .02, gravity_fraction=.5),
    }
    assert out['energy_witnesses']['irreversible_isolated']['packets'] == 5
    assert out['energy_witnesses']['gravity_backfeed']['packets'] == 20
    # All arbitrary failure phases have at most one partly/fully prearmed packet;
    # remaining *nonrecovered* reset debits w draw on all accessible residual E.
    # With gravity isolated, 1+floor(E/w) is a conservative count bound.
    bounds = []
    for J, x, loss in product((1e-6, 1e-5), (0., .0001, .001), (.001, .005, .02)):
        E = .5 * J * 50**2 + .5 * 1e5 * x*x
        count = 1 + math.floor((E + 1e-14) / loss)
        bounds.append({'J': J, 'capture_deflection_mm': x*1000,
                       'irreversible_debit_J': loss, 'residual_J': E,
                       'packet_count_upper': count,
                       'geometric_excursion_upper_mm': 2.4 + 2 * count})
    out['isolated_phase_envelope'] = bounds
    # Independent endpoint reconstruction of E-146 interval translations.
    # Initial position may be anywhere in [0, 2.4] mm; each transition moves
    # that window by +/-2 mm, including the already armed transition.
    for n in range(9):
        farthest = 0.
        for signs in product((-1, 1), repeat=n):
            shift = 0.
            for sign in signs:
                shift += sign * 2.
                farthest = max(farthest, abs(shift), abs(shift + 2.4),
                               abs(shift - 2.4))
        assert farthest <= 2.4 + 2*n + 1e-12
    # Manufacturing lower-debit uncertainty must monotonically worsen count.
    for J, x in product((1e-6, 1e-5), (0., .0001, .001)):
        rows = [r for r in bounds if r['J'] == J and
                r['capture_deflection_mm'] == x*1000]
        assert rows[0]['packet_count_upper'] >= rows[1]['packet_count_upper'] >= rows[2]['packet_count_upper']
    # A finite release-energy store supplies no output-motion energy cap.
    # Zero F but finite velocity coasts; gravity supplies F*H independently.
    out['unrestrained'] = []
    for F, v in product((0., .02, 1., 10.), (0., .1, -.1)):
        H, m = .04, 1.1
        if F == 0:
            t = H/abs(v) if v else None
        else:
            a = F/m
            t = (-v + math.sqrt(v*v + 2*a*H))/a
        out['unrestrained'].append({'F_N': F, 'initial_downward_velocity_m_s': v,
                                    'downward_40mm_time_s': t if F or v >= 0 else None,
                                    'either_end_time_at_zero_F_s': t if F == 0 else None,
                                    'gravity_work_J': F*H})
    # Signed force and speed, finite catch beyond capture; accessible elastic
    # energy is charged once, not hidden by fixing the motor coordinate.
    impacts = []
    for F, v, Es in product((0., .02, 1., 10.), (-.1, 0., .1), (0., .05)):
        direction = -1 if v < 0 else 1
        signed_force = direction * F
        K = .5 * 1.1 * v*v + Es
        d = .0024
        Ehit = K + signed_force * d
        if Ehit < 0:  # Turns before the opposed catch; later gravity reverses.
            continue
        delta = catch_compression(Ehit, signed_force, 1e5)
        impacts.append({'F_N': F, 'v_m_s': v, 'elastic_J': Es,
                        'catch_sign': direction, 'compression_mm': delta*1000})
    out['signed_catch_scenarios'] = impacts
    # Positive-side 10 N witness, exact independent quadratic energy check.
    d = catch_compression(.5*1.1*.1**2 + 10*.0024 + .05, 10, 1e5)
    assert abs(d - .0013649110640673518) < 1e-12
    assert catch_compression(0, 0, 1e5) == 0
    assert abs(catch_compression(.005, 0, 1e5) - math.sqrt(.01/1e5)) < 1e-15
    # Isolated delivery stores; ideal energy equivalence, not real sizing.
    W = .005
    out['ideal_5mJ_stores'] = {'spring_k_at_1mm_N_m': 2*W/.001**2,
        'capacitor_at_12V_F': 2*W/12**2,
        'constant_pressure_volume_at_0_5MPa_m3': W/5e5}
    # Bound pressure-volume work without calling a trapped accumulator a brake.
    # Distinct negative-work receiver: output piston -> sealed fluid -> finite
    # receiving piston -> grounded end stop. No atmosphere/return-tank path.
    A, V = math.pi * .002**2 / 4, math.pi * .002**2 / 4 * .002
    out['finite_volume_receiver'] = []
    for compliance, leak in product((0., 1e-15, 1e-14), (0., 1e-12, 1e-10)):
        pressure = 10/A
        excursion = (V + compliance*pressure + leak*30)/A
        out['finite_volume_receiver'].append({'C_m3_Pa': compliance,
            'Q_m3_s': leak, 'static_30s_excursion_mm': excursion*1000})
    out['schedule'] = []
    for overhead in (0., .005, .01, .02, .05):
        H = next(h for h in range(1, 6401)
                 if 6 + math.ceil(6400/h) * (.45 + 21*overhead) < 30)
        out['schedule'].append({'packet_overhead_s': overhead, 'heads': H,
                                'complete_head_allowance_USD': 250/H})
    out['reset_heat_J_map'] = {str(w): 6400*21*w for w in (.001, .005, .02)}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
