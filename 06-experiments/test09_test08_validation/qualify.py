"""Replay explicit measured timing inputs. Blank records are NOT_MEASURED.

No friction, reliability or mechanical qualification is inferred from timing.
Use a copy of measurements/timing.csv; never write simulations into that file.
"""
import argparse
import csv
import json
import math
from pathlib import Path
import analyze as a

SLOW=['command_s','engage_s','home_settle_s','write_settle_s','disengage_s','seat_s',
      'reference_s','ready_s','inspection_s','recovery_s']
FAST=['rate_hz','scan_v_mm_s','scan_a_mm_s2','lift_v_mm_s','lift_a_mm_s2']
CONDITIONS={'cold','warm','worn','misaligned'}


def evaluate(path):
    with path.open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    if not rows:return {'timing_gate':'NOT_MEASURED','product_gate':'UNVERIFIED','rows':0}
    values={}
    for r in rows:
        if not all(r.get(k) for k in ['run_id','part_lot','condition','trace_path']):
            raise ValueError('measurement provenance missing')
        if not (path.parent / r['trace_path']).is_file():raise ValueError('trace file missing')
        for k in SLOW+FAST+['home_steps','failures']:
            x=float(r[k])
            if not math.isfinite(x) or x<0 or (k in FAST and x==0):raise ValueError('invalid '+k)
            values.setdefault(k,[]).append(x)
    if len({r['run_id'] for r in rows})!=len(rows):raise ValueError('duplicate run IDs')
    if any(x!=int(x) for k in ['home_steps','failures'] for x in values[k]):raise ValueError('counts must be integers')
    p=json.loads((a.HERE/'params.json').read_text())
    if min(values['home_steps'])*p['timing']['step_deg']<360:raise ValueError('incomplete homing in measurement record')
    # Deliberately conservative envelope; no statistical quantile claim.
    for k in SLOW:p['timing'][k]=max(values[k])*1.2
    for k in FAST:p['timing'][k]=min(values[k])/1.2
    p['timing']['home_steps']=int(max(values['home_steps']))
    elapsed=a.schedule(p,a.maps(p)['high'])['time_s']
    adequate=len(rows)>=1000 and CONDITIONS <= {r['condition'] for r in rows}
    failures=sum(values['failures'])
    gate='CONDITIONAL_TIMING_ONLY' if adequate and failures==0 and elapsed<=27 else 'DO_NOT_SCALE'
    return {'timing_gate':gate,'product_gate':'UNVERIFIED','rows':len(rows),'sample_and_condition_gate':adequate,
            'reported_failures':failures,'conservative_time_s':elapsed,'envelope_inputs':p['timing'],
            'limits':'20% envelope over observed maxima/minima is an engineering rule, not a statistical bound; full-scale fan-in and structural data still required'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--timing',type=Path,default=a.HERE/'measurements/timing.csv');args=ap.parse_args()
    result=evaluate(args.timing);a.save('measurement_gate.json',result);print(json.dumps(result,indent=2))


if __name__=='__main__':main()
