"""Regression + honesty gates for the DND-56 S5-R delivered-BOM ratification.

Run: python s5r_bom_ratify_checks.py
Standard library only (imports the s5r_bom_ratify module).

These checks fail if (a) a headline figure is mis-computed, (b) the DND-54 claim
silently stops reproducing, (c) the sourced actuator trace is mislabelled as
anything but sourced, or (d) the ADR document drifts from the model. They also
pin the no-channel identity (`218.70 + 63.64 = 282.34`) so the DND-52/S5-R
convention and this ratification cannot diverge.
"""
from __future__ import annotations

import unittest
from pathlib import Path

import s5r_bom_ratify as r

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ADR = REPO / "07-evidence-and-decisions" / "dnd54-s5r-bom-ratification.md"


class RatificationChecks(unittest.TestCase):
    def test_no_channel_identity_dnd52_convention(self):
        # 218.70 + 63.64 = 282.34 (the DND-52 checks.py identity).
        self.assertAlmostEqual(r.fixed_parts_from_csv(), 218.70, places=2)
        self.assertAlmostEqual(r.driver_block_parts(), 63.64, places=2)
        self.assertAlmostEqual(r.fixed_parts_with_driver(), 282.34, places=2)
        self.assertTrue(r.run()["identity_holds"])

    def test_dnd54_claim_reproduces_exactly(self):
        res = r.run()
        self.assertAlmostEqual(res["derived_s5r_parts"], 342.70, places=2)
        self.assertAlmostEqual(res["derived_s5r_delivered"], 397.53, places=2)
        self.assertAlmostEqual(res["derived_margin"], 102.47, places=2)
        self.assertTrue(res["claim_reproduces"])

    def test_uplift_is_additive_not_compounded(self):
        self.assertAlmostEqual(r.UPLIFT, 1.16, places=9)
        self.assertTrue(r.run()["uplift_is_additive"])
        # It must NOT be the compounded DND-37 defect value.
        self.assertNotAlmostEqual(r.UPLIFT, 1.10 * 1.06, places=6)

    def test_no_double_count_of_the_driver_block(self):
        # The claim's parts must equal no-channel base + actuators, with no
        # driver block added back anywhere.
        b = r.s5r_bom()
        self.assertAlmostEqual(
            b["parts"], b["fixed_no_channel_parts"] + b["actuator_parts"], places=2)
        self.assertAlmostEqual(b["fixed_no_channel_parts"], 218.70, places=2)
        # The 80-channel driver block is NOT in the S5-R BOM.
        self.assertNotAlmostEqual(b["parts"], 282.34 + b["actuator_parts"], places=2)

    def test_sourced_actuators_are_labelled_and_meet_the_class(self):
        t = r.actuator_trace_summary()
        self.assertEqual(t["bank_stepper"]["label"], "SOURCED-LIVE")
        self.assertTrue(t["bank_stepper"]["meets_torque"])
        self.assertLessEqual(t["bank_stepper"]["cheapest_matched_usd"], 13.0)
        self.assertEqual(t["writer_solenoid"]["label"], "SOURCED-LIVE")
        self.assertLessEqual(t["writer_solenoid"]["cheapest_matched_usd"], 2.60)
        # Each traced row must carry a URL and an evidence class.
        for row in t["bank_trace"] + t["writer_trace"]:
            self.assertTrue(row["url"].startswith("http"), row)
            self.assertIn(row["evidence"], ("SOURCED-LIVE", "UNVERIFIED-MARKETPLACE"))

    def test_block_channels_are_priced_once_and_bom_clears(self):
        wc = r.s5r_bom_with_channels()
        self.assertGreater(wc["channel_parts"], 0.0)
        self.assertTrue(wc["clears_with_channels"])
        self.assertAlmostEqual(
            wc["parts_with_channels"], wc["parts"] + wc["channel_parts"], places=2)
        cd = wc["channel_detail"]
        self.assertEqual(cd["bank_ics_conservative"], 2)
        self.assertEqual(cd["writer_chips"], 5)

    def test_scenarios_are_ordered_and_all_clear_the_ceiling(self):
        s = r.scenarios()
        self.assertTrue(s["all_clear_ceiling"])
        self.assertLess(s["optimistic_usd"], s["working_usd"])
        self.assertLess(s["working_usd"], s["high_usd"])
        self.assertAlmostEqual(s["claimed_dnd54_usd"], 397.53, places=2)
        # The honest end-to-end "working" figure is the claim plus its channels.
        self.assertAlmostEqual(s["working_usd"], 401.12, places=2)
        self.assertLess(s["high_usd"], 500.0)
        # The working figure misses the ideal <$400 band by a hair; that is a
        # finding, not a pass. Record it so a silent band change is caught.
        self.assertGreater(s["working_usd"], 400.0)
        self.assertGreater(s["optimistic_usd"], 400.0 * 0.9)

    def test_break_even_prices_are_positive_and_ordered(self):
        b = r.break_even()
        self.assertGreater(b["bank_motor_unit_max_for_ideal_usd"], 0.0)
        self.assertLess(b["bank_motor_unit_max_for_ideal_usd"],
                        b["bank_motor_unit_max_for_ceiling_usd"])
        self.assertGreater(b["writer_unit_max_for_ceiling_usd"], 3.0)
        self.assertGreater(b["bank_motor_unit_max_for_ceiling_usd"], 15.0)

    def test_reconciles_with_committed_cost_closure(self):
        rec = r.reconcile_with_committed()
        self.assertAlmostEqual(rec["cc_no_channel"], r.fixed_parts_from_csv(), places=2)
        self.assertAlmostEqual(rec["cc_uplift"], r.UPLIFT, places=9)
        self.assertAlmostEqual(rec["cc_ceiling"], r.CEILING, places=9)

    def test_csv_artifact_is_consistent(self):
        import csv

        out = Path(r.emit_bom_csv())
        self.assertTrue(out.exists())
        with out.open(newline="") as fh:
            rows = list(csv.DictReader(fh))
        body = [x for x in rows if not x["item"].startswith("TOTAL")]
        total = [x for x in rows if x["item"].startswith("TOTAL")][0]
        parts_sum = round(sum(float(x["parts_usd"]) for x in body), 2)
        self.assertAlmostEqual(parts_sum, float(total["parts_usd"]), delta=0.05)
        delivered_sum = round(sum(float(x["delivered_usd"]) for x in body), 2)
        self.assertAlmostEqual(delivered_sum, float(total["delivered_usd"]), delta=0.05)
        # At sourced actuator units the end-to-end total is inside the ideal band.
        self.assertLess(float(total["delivered_usd"]), r.IDEAL_BAND)

    def test_adr_document_carries_the_decisive_numbers(self):
        self.assertTrue(ADR.exists(), f"missing ADR {ADR}")
        text = ADR.read_text()
        for token in ("DND-56", "397.53", "401.12", "218.70", "63.64",
                      "1.16", "SOURCED-LIVE", "allowance", "RATIFIED"):
            self.assertIn(token, text, f"{token!r} missing from the ADR")


if __name__ == "__main__":
    unittest.main(verbosity=2)
