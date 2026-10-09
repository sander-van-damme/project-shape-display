#!/usr/bin/env python3
"""E-067: exhaustive logical drive-access synthesis, not contact geometry.
Units mm, s; no random sampling, fitted manufacturing or hardware claims.
"""
import itertools as it
import json
import math
import sys

STROKES = (10, 20, 40)


def trace(old, new, clear_order, set_order, policy):
    state = old
    events = []
    if old == new:
        return events
    for kind, order in [('clear', clear_order), ('set', set_order)]:
        for i in order:
            bit = 1 << i
            if kind == 'clear':
                act = bool(state & bit) and (policy == 'normalize' or not new & bit)
            else:
                act = bool(new & bit) and not state & bit
            if not act:
                continue
            lower_offset = 10 * (state & (bit - 1))
            before = 10 * state
            state = state & ~bit if kind == 'clear' else state | bit
            events.append(dict(kind=kind, layer=i, lower_offset_mm=lower_offset,
                               before_mm=before, after_mm=10*state,
                               accessible=lower_offset == 0))
    assert state == new
    assert all(0 <= e['after_mm'] <= 10*max(old, new) for e in events)
    return events


def population(states):
    rows = []
    for policy, clear, set_ in it.product(['changed_bits', 'normalize'],
                                         it.permutations(range(3)),
                                         it.permutations(range(3))):
        failures = []
        operations = 0
        pairs_with_failure = 0
        for old, new in it.product(states, repeat=2):
            events = trace(old, new, clear, set_, policy)
            operations += len(events)
            bad = [e for e in events if not e['accessible']]
            pairs_with_failure += bool(bad)
            failures += [dict(old=10*old, new=10*new, **e) for e in bad]
        rows.append(dict(policy=policy, clear=clear, set=set_,
                         failing_pairs=pairs_with_failure,
                         failing_events=len(failures), operations=operations,
                         first_failure=failures[0] if failures else None))
    return rows


def move(d, v=100, a=500):
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def checks():
    # Independently reasoned normal form for arbitrary n-bit words: clearing
    # least significant first and setting most significant first always sees
    # a zero lower prefix. Extend outside the three-bit synthesis domain.
    for bits in range(1, 7):
        for old, new in it.product(range(1 << bits), repeat=2):
            s = old
            for i in range(bits):
                if s & (1 << i):
                    assert s % (1 << i) == 0
                    s -= 1 << i
            assert s == 0
            for i in reversed(range(bits)):
                if new & (1 << i):
                    assert s % (1 << i) == 0
                    s += 1 << i
            assert s == new
    assert trace(3, 3, (0,1,2), (2,1,0), 'normalize') == []
    assert any(not e['accessible'] for e in trace(1,3,(0,1,2),(2,1,0),'changed_bits'))
    assert all(e['accessible'] for e in trace(1,3,(0,1,2),(2,1,0),'normalize'))
    assert move(0) == 0
    assert math.isclose(move(20), .4)


def main():
    checks()
    result = {}
    for count in [5,8]:
        rows = population(range(count))
        result[str(count)+'_states'] = {
            'protocols': len(rows),
            'survivors': [r for r in rows if not r['failing_events']],
            'changed_bit_best_failing_pairs': min(r['failing_pairs'] for r in rows if r['policy']=='changed_bits'),
            'normalized_total_operations': next(r['operations'] for r in rows if r['policy']=='normalize'),
            'changed_bit_total_operations': next(r['operations'] for r in rows if r['policy']=='changed_bits'),
        }
        if '--all' in sys.argv: result[str(count)+'_states']['population']=rows
    result['witness_10_to_30_mm'] = trace(1,3,(0,1,2),(2,1,0),'normalize')
    # Positioning shared rails at the start of each of six phases is mandatory.
    # Every rail must be raised unloaded to start clearing; it returns unloaded
    # after setting. Both traverse all three strokes in the worst full-map case.
    result['motion_ledger'] = dict(
        six_loaded_passes_mm=2*sum(STROKES),
        positioning_and_return_mm=2*sum(STROKES),
        loaded_only_s=2*sum(move(d) for d in STROKES),
        serial_all_traversals_s=4*sum(move(d) for d in STROKES),
        six_event_max_dwell_s=(30-6-4*sum(move(d) for d in STROKES))/6,
        assumed_other_overhead_s=6,
        repeated_load_stages=3*6400,
        lateral_retracted_clearance_rule='projection + 2*placement_error < available_bypass',
    )
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
