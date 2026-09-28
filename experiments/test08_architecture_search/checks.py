"""Meaningful model regression/falsification checks. No optional test dependencies."""
import copy
import json
import math
import unittest
import analysis as a


class Checks(unittest.TestCase):
    def setUp(self):
        self.p=json.loads((a.HERE/'params.json').read_text())

    def test_triangular_and_trapezoidal_motion(self):
        self.assertAlmostEqual(a.move_time(1,10,4),1)
        self.assertAlmostEqual(a.move_time(100,10,10),11)
        with self.assertRaises(ValueError): a.move_time(-1,10,10)

    def test_adversarial_map_and_complete_timing_accounting(self):
        maps=a.patterns(self.p)
        high=a.schedule(self.p,maps['all_high'])
        checker=a.schedule(self.p,maps['checkerboard'])
        self.assertEqual(high['cells_written'],6400)
        self.assertAlmostEqual(high['time_s'],checker['time_s'])
        self.assertAlmostEqual(high['time_s'],sum(high['breakdown_s'].values()))
        self.assertGreater(high['breakdown_s']['home_rotors_to_stop'],5)
        self.assertGreater(high['breakdown_s']['lower_platen'],1)
        self.assertGreater(high['breakdown_s']['park_head'],1)
        self.assertLess(high['time_s'],30)
        self.assertGreater(a.schedule(self.p,maps['all_high'],step_rate=200)['time_s'],30)
        self.assertGreater(a.schedule(self.p,maps['all_high'],channels=40,step_rate=800)['time_s'],30)

    def test_nonsquare_partial_group_covers_every_cell(self):
        p=copy.deepcopy(self.p); p['grid']['rows']=3; p['grid']['columns']=7
        run=a.schedule(p,[[0]*7 for _ in range(3)],channels=4)
        self.assertEqual(run['cells_written'],21)
        self.assertEqual(run['row_groups'],6)

    def test_no_silent_height_or_homing_assumptions(self):
        p=copy.deepcopy(self.p); p['terrain']['levels']=9
        with self.assertRaises(ValueError): a.validate(p)
        p=copy.deepcopy(self.p); p['motion']['home_steps']=15
        with self.assertRaises(ValueError): a.validate(p)
        with self.assertRaises(ValueError): a.schedule(self.p,[[0]])

    def test_known_mechanical_failures_remain_visible(self):
        geo=a.geometry(self.p); force=a.forces(self.p,geo)
        self.assertEqual(len(geo['transition_cases']),25)
        self.assertGreater(geo['cam_to_guide_lip_clearance_mm'],0.15)
        self.assertLess(force['unbraced_follower_euler_n'],self.p['loads']['cell_test_load_n'])
        # Revised upper guide is positive but too thin for ordinary 0.4-mm extrusion.
        self.assertGreater(geo['minimum_body_guide_web_mm'],0)
        self.assertLess(geo['minimum_body_guide_web_mm'],.4)
        self.assertGreater(a.costs()['working_plus_20_percent_usd'],500)

    def test_guide_cannot_lose_follower_at_highest_level(self):
        a.validate(self.p)
        p=copy.deepcopy(self.p); p['cam']['follower_guide_top_mm']=40
        with self.assertRaisesRegex(ValueError,'loses guidance'): a.validate(p)
        geo=a.geometry(self.p)
        self.assertGreaterEqual(geo['guide_top_at_max_body_bottom_mm'],0)
        self.assertGreaterEqual(geo['unrelieved_upper_body_length_mm'],40)


if __name__=='__main__': unittest.main()
