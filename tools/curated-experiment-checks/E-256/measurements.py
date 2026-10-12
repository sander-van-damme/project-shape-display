#!/usr/bin/env python3
"""Reduce screw-pair observations with explicit intervals; never infer a pass.

--blank emits an unmeasured record; --check runs synthetic numerical controls.
Raw observation records belong with actual physical evidence, not this source.
All intervals are absolute bounds, not confidence intervals or calibrated priors.
"""
import argparse
import json
import math
from pathlib import Path

G = 9.80665


def interval(value, name, nonnegative=False):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f'{name}: expected [lower, upper]')
    if any(isinstance(x, bool) or not isinstance(x, (int, float))
           or not math.isfinite(x) for x in value):
        raise ValueError(f'{name}: finite numbers required')
    lo, hi = value
    if lo > hi or (nonnegative and lo < 0):
        raise ValueError(f'{name}: invalid bounds')
    return lo, hi


def difference(after, before):
    return [after[0] - before[1], after[1] - before[0]]


def quotient(numerator, denominator):
    if denominator[0] <= 0 <= denominator[1]:
        raise ValueError('turn interval contains zero; lead is unresolved')
    corners = [n / d for n in numerator for d in denominator]
    return [min(corners), max(corners)]


def reduce_record(record):
    if record.get('evidence') not in ('physical_measurement', 'synthetic'):
        raise ValueError('Set evidence only after observations exist')
    for field in ('specimen', 'setup', 'bounds_basis', 'raw_source'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f'{field}: a nonempty description is required')
    mass = interval(record['total_supported_mass_g'], 'mass', True)
    result = {key: record[key] for key in
              ('evidence', 'specimen', 'setup', 'bounds_basis', 'raw_source')}
    result.update(total_supported_mass_g=mass, holds=[], travel=[], torque=[])
    for hold in record.get('holds', []):
        observations = hold['observations']
        if len(observations) < 2:
            raise ValueError('Hold needs a baseline and later observation')
        baseline = interval(observations[0]['height_mm'], 'height')
        last_time = -1
        reduced = []
        for observation in observations:
            time = observation['elapsed_s']
            if (isinstance(time, bool) or not isinstance(time, (int, float))
                    or not math.isfinite(time) or time < 0 or time <= last_time):
                raise ValueError('Hold times must be finite, nonnegative and increasing')
            if last_time == -1 and time != 0:
                raise ValueError('First hold observation must be at elapsed_s=0')
            height = interval(observation['height_mm'], 'height')
            # Same observation subtracts itself exactly; later observations have
            # conservative independent bounds. Do not assume fixture bias cancels.
            drift = [0., 0.] if time == 0 else difference(height, baseline)
            reduced.append(dict(elapsed_s=time, signed_drift_mm=drift,
                interpretation=('resolved_downward' if drift[1] < 0 else
                                'resolved_upward' if drift[0] > 0 else
                                'zero_not_excluded')))
            last_time = time
        result['holds'].append(dict(position=hold['position'], observations=reduced))
    for travel in record.get('travel', []):
        delta = difference(interval(travel['after_mm'], 'after'),
                           interval(travel['before_mm'], 'before'))
        turns = interval(travel['signed_turns'], 'turns')
        result['travel'].append(dict(signed_displacement_mm=delta,
            effective_mm_per_signed_turn=quotient(delta, turns),
            note='Includes lost motion; not thread lead unless backlash was taken up'))
    for torque in record.get('torque', []):
        if torque['direction'] not in ('raise', 'lower'):
            raise ValueError('Torque direction must be raise or lower')
        if torque['observation'] not in ('no_motion', 'onset', 'slow_running'):
            raise ValueError('Unknown torque observation')
        force = interval(torque['force_N'], 'force', True)
        # Perpendicular distance to the force line, not just lever length.
        arm = interval(torque['perpendicular_arm_mm'], 'arm', True)
        result['torque'].append(dict(direction=torque['direction'],
            observation=torque['observation'],
            applied_torque_Nmm=[force[0] * arm[0], force[1] * arm[1]],
            note='Applied apparatus torque; parasitics/side-load effects not removed'))
    if not any(result[key] for key in ('holds', 'travel', 'torque')):
        raise ValueError('No observations supplied')
    result['limitations'] = ('Bounds describe supplied observations only. Zero not '
        'excluded is not proof of zero drift. No holding, moving-loss, speed, '
        'endurance or array qualification follows. No synthetic value is a measurement.')
    return result


def blank():
    return dict(evidence='unmeasured', specimen='', setup='', bounds_basis='',
                raw_source='', total_supported_mass_g=None,
                holds=[], travel=[], torque=[])


def checks():
    record = dict(evidence='synthetic', specimen='numerical control',
        setup='invented input for code checks', bounds_basis='chosen test intervals',
        raw_source='inline synthetic fixture; no hardware', total_supported_mass_g=[19.9,20.1],
        holds=[dict(position='mid', observations=[
            dict(elapsed_s=0, height_mm=[9.9,10.1]),
            dict(elapsed_s=60, height_mm=[9.9,10.1]),
            dict(elapsed_s=600, height_mm=[9.6,9.8])])],
        travel=[dict(before_mm=[0,0], after_mm=[-6,-6], signed_turns=[-2,-2])],
        torque=[dict(direction='raise', observation='onset',
                     force_N=[.001,.003], perpendicular_arm_mm=[9.8,10.2])])
    result = reduce_record(record)
    hold = result['holds'][0]['observations']
    assert hold[1]['interpretation'] == 'zero_not_excluded'
    assert math.isclose(hold[1]['signed_drift_mm'][1], .2)
    assert hold[2]['interpretation'] == 'resolved_downward'
    assert result['travel'][0]['effective_mm_per_signed_turn'] == [3,3]
    assert math.isclose(result['torque'][0]['applied_torque_Nmm'][1], .0306)
    assert quotient([-6.1,-5.9],[-2.1,-1.9])[0] > 2.8
    rejected = 0
    for invalid in ([2,1], [0,float('nan')], [0,float('inf')], [True,2]):
        try:
            interval(invalid, 'invalid')
        except ValueError:
            rejected += 1
    for invalid in (blank(), dict(record, total_supported_mass_g=[-1,1]),
                    dict(record, holds=[],travel=[],torque=[])):
        try:
            reduce_record(invalid)
        except ValueError:
            rejected += 1
    try:
        quotient([1,2],[-1,1])
    except ValueError:
        rejected += 1
    assert rejected == 8
    # g -> N -> N mm, checked against direct m*g*r in SI.
    assert math.isclose(1/1000*G*10, .00001*G*1000)
    return dict(evidence='synthetic_checks_only',
        checks='signed travel, drift ambiguity/detection, torque endpoints, invalid inputs',
        torque_Nmm_for_1g_at_10mm=G*.01,
        mass_error_g_for_001Nmm_at_10mm=.01/(G*.01),
        equal_height_readings_with_plus_minus_01mm_error_drift_bound_mm=[-.2,.2])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--blank', action='store_true')
    group.add_argument('--check', action='store_true')
    group.add_argument('--record', type=Path)
    args = parser.parse_args()
    try:
        result = (blank() if args.blank else checks() if args.check
                  else reduce_record(json.loads(args.record.read_text())))
    except (ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
