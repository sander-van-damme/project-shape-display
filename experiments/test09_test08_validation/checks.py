"""Regression and falsification checks; model correctness is not mechanism success."""
import copy
import json
import math
import csv
import tempfile
from pathlib import Path
import unittest
import analyze as a
import qualify


class Checks(unittest.TestCase):
    def setUp(self):self.p=json.loads((a.HERE/'params.json').read_text())

    def test_motion_limits(self):
        self.assertEqual(a.travel(0,10,4),0)
        self.assertAlmostEqual(a.travel(1,10,4),1)
        self.assertAlmostEqual(a.travel(100,10,10),11)
        with self.assertRaises(ValueError):a.travel(-1,10,4)

    def test_independent_schedule_matches_reference(self):
        old=a.old_module();op=json.loads((old.HERE/'params.json').read_text())
        for rate in [200,400,800]:
            p=copy.deepcopy(self.p);p['timing']['rate_hz']=rate
            for name,values in a.maps(p).items():
                got=a.schedule(p,values,True)
                self.assertAlmostEqual(got['time_s'],old.schedule(op,values,step_rate=rate)['time_s'])
                self.assertEqual(got['cells_commanded'],6400)
                self.assertEqual(sum(e['kind']=='home' for e in got['events']),80)
                self.assertAlmostEqual(sum(e['duration_s'] for e in got['events']),got['time_s'])

    def test_adversarial_and_detection_budget(self):
        m=a.maps(self.p);base=a.schedule(self.p,m['high'])['time_s']
        for name in ['checker','one_high_per_row']:
            self.assertAlmostEqual(a.schedule(self.p,m[name])['time_s'],base)
        p=copy.deepcopy(self.p);p['timing']['inspection_s']=1
        self.assertGreater(a.schedule(p,m['high'])['time_s'],27)
        p['timing'].update(engage_s=.05,disengage_s=.05)
        self.assertGreater(a.schedule(p,m['high'])['time_s'],30)

    def test_invalid_inputs_are_not_passes(self):
        with self.assertRaises(ValueError):a.schedule(self.p,[[0]])
        for key,val in [('rate_hz',0),('home_steps',19),('inspection_s',-1)]:
            p=copy.deepcopy(self.p);p['timing'][key]=val
            with self.assertRaises(ValueError):a.schedule(p,a.maps(p)['high'])
        p=copy.deepcopy(self.p);p['grid']['levels']=6
        with self.assertRaises(ValueError):a.schedule(p,a.maps(p)['high'])

    def test_reliability_bound(self):
        r=a.reliability();q=r['cell_q_for_99pct_map']
        self.assertAlmostEqual((1-q)**6400,.99)
        self.assertGreater(r['zero_failure_trials_95pct'],1900000)
        self.assertGreater(r['zero_failures_80000_cell_trials_upper_q'],q)
        self.assertIsNone(r['measured_cycles'])

    def test_rejected_geometry_and_cost_stay_rejected(self):
        toe=math.degrees(math.atan2(.5,1.15))
        self.assertLess(180/9-toe,0)
        self.assertLess(math.degrees(math.asin(.25/1.65)),18)
        self.assertGreater(a.bom(self.p)['with_contingency_usd']['realistic'],500)

    def test_partial_multirow_stops_and_cost(self):
        rows=a.multirow(self.p)
        case=next(r for r in rows if r['rows']==3 and r['columns']==80 and r['mode']=='independent_full_stroke')
        self.assertEqual(case['stops'],27)
        self.assertEqual(case['actuators'],240)
        self.assertGreater(case['realistic_allowance_usd'],500)
        self.assertTrue(all(r['qualified'] is False for r in rows))

    def test_missing_measurements_never_pass(self):
        result=qualify.evaluate(a.HERE/'measurements/timing.csv')
        self.assertEqual(result['timing_gate'],'NOT_MEASURED')
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.csv'
            path.write_text('run_id,part_lot,condition,trace_path\nx,lot,cold,missing.txt\n')
            with self.assertRaisesRegex(ValueError,'trace file missing'):qualify.evaluate(path)

    def test_register_and_bom_integrity(self):
        with (a.HERE/'uncertainties.csv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),31)
        self.assertEqual(len({r['id'] for r in rows}),31)
        self.assertTrue(all(None not in r and all(r.values()) for r in rows))
        with (a.HERE/'multirow_bom.csv').open(newline='',encoding='utf-8') as f:
            self.assertEqual(sum(float(r['allowance_usd']) for r in csv.DictReader(f)),self.p['multirow']['base_cost_usd'])

    def test_synthetic_timing_replay_is_not_physical_evidence(self):
        # Temporary software fixture ONLY, never stored in measurements/.
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'synthetic.csv';(Path(tmp)/'synthetic.txt').write_text('unit-test fixture, NOT MEASURED')
            row={k:self.p['timing'][k] for k in qualify.SLOW+qualify.FAST+['home_steps']}
            row.update(run_id='test',part_lot='synthetic',condition='cold',trace_path='synthetic.txt',failures=0)
            with path.open('w',newline='') as f:
                w=csv.DictWriter(f,fieldnames=list(row));w.writeheader();w.writerow(row)
            got=qualify.evaluate(path)
            self.assertEqual(got['timing_gate'],'DO_NOT_SCALE')
            self.assertGreater(got['conservative_time_s'],30)


if __name__=='__main__':unittest.main()
