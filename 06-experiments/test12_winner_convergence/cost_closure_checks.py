"""Regression + honesty gates for the DND-44 K5/K7 cost closure.

Run: python cost_closure_checks.py
Standard library only.
"""
from __future__ import annotations

import unittest

import cost_closure as cc


class CostClosureChecks(unittest.TestCase):
    def test_honest_expected_baseline_is_over_the_ceiling(self):
        # The reconciled 08 doc printed $501.12 using a $0.80 driver and a
        # best-case motor. On the BOM's own expected column the baseline is
        # materially worse; the closure must not hide this.
        b = cc.expected_baseline()
        self.assertAlmostEqual(b["parts"], 510.40, places=2)
        self.assertAlmostEqual(b["delivered"], 592.06, places=2)
        self.assertEqual(b["verdict"], "OVER CEILING (>=$500)")

    def test_reduction_path_is_below_the_ceiling_with_margin(self):
        c = cc.closure()
        self.assertLess(c["sourced_delivered_usd"], cc.CEILING)
        self.assertGreater(c["margin_usd"], 25.0)  # meaningful, not razor-thin
        self.assertEqual(c["verdict"], "BELOW CEILING (<$500)")

    def test_driver_swap_is_the_largest_single_reduction(self):
        audit = cc.closure()["reduction_audit"]
        by_item = {a["item"]: a["line_delta"] for a in audit}
        drv = next(v for k, v in by_item.items() if k.startswith(cc.DRIVER_MATCH))
        self.assertLess(drv, 0)
        self.assertLess(drv, min(v for k, v in by_item.items()
                                 if not k.startswith(cc.DRIVER_MATCH)))

    def test_every_reduction_preserves_the_machine(self):
        # No reduction may delete the motor, driver, controller, register or any
        # structural line: only price substitutions and the spares allowance.
        out, audit, _ = cc.reduced_lines()
        items_out = {l["item"] for l in out}
        changed = {a["item"] for a in audit}
        self.assertIn(cc.DRIVER_MATCH, " ".join(changed))
        self.assertIn(cc.MOTOR_MATCH, " ".join(changed))
        self.assertIn(cc.CTRL_MATCH, " ".join(changed))
        # Structural lines are repriced, never dropped from the BOM.
        for kept in ("Guide rods/rails and bearings", "Power supplies and protection",
                     "Four lift screws and nuts", "Lift motor"):
            self.assertIn(kept, items_out, f"{kept} must remain in the BOM")
        # The only line whose unit is driven to zero is the spares allowance.
        zeroed = {l["item"] for l in out if l["unit_sourced"] == 0.0}
        self.assertEqual(zeroed, {cc.SPARES_MATCH})

    def test_k7_is_the_binding_residual(self):
        c = cc.closure()
        # At the sourced $2.66 AliExpress motor the machine is over the ceiling:
        # the cost path is only as strong as the motor price.
        self.assertGreater(c["downside_motor_2p66_delivered_usd"], cc.CEILING)
        self.assertIn("motor", c["k7_residual"])

    def test_motor_break_even_price(self):
        lo, hi = 0.5, 5.0
        for _ in range(100):
            mid = (lo + hi) / 2
            d = cc.reduced_lines(mid)[2] * cc.UPLIFT
            if d > cc.CEILING:
                hi = mid
            else:
                lo = mid
        break_even = (lo + hi) / 2
        # The path clears below the ceiling only for a motor under ~$1.86.
        self.assertGreater(break_even, 1.5)
        self.assertLess(break_even, 2.2)


if __name__ == "__main__":
    unittest.main()
