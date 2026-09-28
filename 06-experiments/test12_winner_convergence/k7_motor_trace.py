"""DND-49 K7 — trace a matched 8 mm 18° bipolar PM stepper to <= $1.86 delivered.

Question. [DND-44]/[DND-47] established the S5 machine-preserving cost path at
**$424.95 delivered** *conditional on a matched 8 mm 18° bipolar PM stepper at
<= $1.86 delivered-inclusive*. The only traceable matched part was MOONS
8PM020S1 at $40. This module does the sourcing trace and answers:

  Does a matched, traced 8 mm 18° bipolar PM stepper exist at <= $1.86
  delivered? If not, what is the cheapest matched price and the resulting
  delivered total, and what minimum-cost design lever could bring the machine
  back under the $500 ceiling?

Requirement envelope (derived from the winner definition, NOT a chosen part).
The S5 head must, for each of 80 columns, engage a permanent-magnet stepper,
home it, write up to 16 full steps, and detent-seat, within a full-map budget
that clears 30 s. From `06-experiments/test08_architecture_search/params.json`
and README.md (motor qualification section):

  frame        8 mm can (head is one motor per 5.08 mm column, so the can must
               fit inside the 5.08 mm pitch cell envelope with the coupler)
  step angle   18 deg (200 steps/rev fraction; head homes in 22 steps and
               writes <= 16 steps per column)
  excitation   2-phase, BI-POLAR (one dual H-bridge per motor; unipolar is not
               interchangeable with the modelled winding)
  winding      ~20 ohm phase, 3.3-5 V class (params.json carries 40 ohm /
               3.3 V for the archived PM08; MOONS is 20 ohm / 5 V)
  running       >= 0.15 mN.m RUNNING torque at the 400 pps design point, with
  torque       measured rotor/coupler friction < half of it (test08 README)
  interface    shaft/gear the print coupler can drive; the archived class uses
               a screw-slider (linear) variant, so the rotary shaft form is
               preferred

Evidence class. SOURCED-LISTING and SOURCED-LIVE observations of real
distributor/marketplace pages, retrieved 2026-09-28. No purchase, no print, no
measurement ([DND-27]). Prices are point-in-time and volatile.
"""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# The machine-preserving fixed base (E1-E6 applied, motor=0) and delivered
# uplift are re-used from cost_closure so the two modules cannot drift.
import cost_closure as cc  # noqa: E402

CEILING = cc.CEILING
UPLIFT = cc.UPLIFT
CHANNELS = 80


def _fixed_parts() -> float:
    return cc.reduced_lines(0.0)[2]


# ---------------------------------------------------------------------------
# Sourced candidate table. Each row: exact listing title, vendor, URL, price,
# evidence class, and the specs that decide whether it meets the envelope.
# 'matched' means: same 8 mm can, 18 deg, 2-phase BIPOLAR, specified winding,
# and a listing we actually retrieved. The marketplace multipacks are NOT
# matched: no step angle, no bipolar confirmation, no lot.
# ---------------------------------------------------------------------------
CANDIDATES = [
    dict(
        id="MOONS-8PM020S1",
        title="8PM020S1-02001 8mm PM stepper, 18deg, bipolar, 20ohm, 0.25A",
        vendor="MOONS' online shop",
        url="https://www.moonsindustries.com/p/8mm-permanent-magnet-stepper-motors/8pm020s1-02001-000004611120002314",
        unit_usd=40.00,
        qty_basis="1 (list)",
        evidence="SOURCED-LIVE",
        matched=True,
        specs="8mm, 18deg, 2ph bipolar, 20ohm, 0.25A, 0.4mNm HOLDING, "
              "0.15mNm DETENT, 8.5mm long, 2g",
        note="Only fully-specified matched retail part. Holding 0.4 mNm; detent "
             "0.15 mNm equals the target running torque (caution: detent is "
             "unpowered drag that subtracts from running torque).",
    ),
    dict(
        id="CCHT-07-005-032",
        title="Compact 8mm 3.3V DC Micro Stepper Motor (model 07-005-032)",
        vendor="Chengdu Century Huasha (CCHT), via Made-in-China",
        url="https://cn-ccht.en.made-in-china.com/product/TOLAylwxCbYh/China-Compact-8mm-3-3V-DC-Micro-Stepper-Motor-for-Precision-Control.html",
        unit_usd=8.20,
        qty_basis="3001+ pieces (MOQ 100 at $11.20)",
        evidence="SOURCED-LIVE",
        matched=True,
        specs="8mm x (8.5+4.2), 18deg step, 2-phase 4-wire BI-POLAR, 3.3V, "
              "165mA, 20ohm, 1.50 gf-cm output torque (0.147 mNm)",
        note="Cheapest matched unit found at the 3,001+ tier; the 100-1,000 "
             "tier (the real 80+spares order) is $11.20. 1.50 gf-cm = 0.147 "
             "mN.m, ~= the target and ~3x below MOONS holding.",
    ),
    dict(
        id="CCHT-07-005-036",
        title="Compact 8mm 5V DC Micro Stepper Motor (model 07-005-036)",
        vendor="Chengdu Century Huasha (CCHT), via Made-in-China",
        url="https://cn-ccht.en.made-in-china.com/product/GZITWbJrHeRj/China-Compact-8mm-5V-DC-Micro-Stepper-Motor-for-Precision-Control.html",
        unit_usd=11.20,
        qty_basis="100-1000 pieces",
        evidence="SOURCED-LIVE",
        matched=True,
        specs="8mm, 18deg step, 2-phase, BI-POLAR drive, 5.0V, 50ohm, "
              "0.23 gf-cm output torque (0.023 mNm)",
        note="Matched but 0.23 gf-cm = 0.023 mN.m, well under the 0.15 mN.m "
             "running-torque requirement. Fails the envelope on torque.",
    ),
    dict(
        id="DFRobot-FIT0708",
        title="18 deg Micro Stepper Motor for Arduino (FIT0708)",
        vendor="DFRobot",
        url="https://www.dfrobot.com/product-2199.html",
        unit_usd=11.90,
        qty_basis="10+ items",
        evidence="SOURCED-LIVE",
        matched=False,
        specs="10mm frame (NOT 8mm), 18deg, bipolar drive, 20ohm, 3.3-5V, "
              "1500 PPS min auto-start, 80g max thrust",
        note="Different frame (10 mm) and a linear screw-slider assembly; no "
             "holding/running torque published. Evidence for the motor class, "
             "not a drop-in 8 mm part.",
    ),
    dict(
        id="PM08-2-archived",
        title="Archived PM08-2 micro stepper datasheet",
        vendor="legacy repo asset (historical surplus)",
        url="06-experiments/legacy/test00_pneumatic_multiplexer/docs/micro-stepper-datasheet.pdf",
        unit_usd=0.26,
        qty_basis="historical EUR 0.52/pair (NOT a current price)",
        evidence="SOURCED-ARCHIVE (historical, non-actionable)",
        matched=False,
        specs="8mm, 18deg, 3.3V, 40ohm, 5 gf-cm (0.490 mNm) PULL-IN torque, "
              ">800 pps no-load",
        note="The original design hypothesis. No current supply, no lot, no "
             "loaded torque curve; price is not a 2026 delivered quote.",
    ),
    dict(
        id="Amazon-Abovehill",
        title="Abovehill 10 pair 8mm Micro Stepper Motor 2-Phase 4-Wire DC 5-6V",
        vendor="Amazon",
        url="https://www.amazon.com/dp/B08346RFVZ",
        unit_usd=1.05,
        qty_basis="10-pair pack (20 pcs); listing EUR0.97/pc",
        evidence="UNVERIFIED-MARKETPLACE",
        matched=False,
        specs="8mm, 2-phase 4-wire, 5-6V, ~39.2 ohm (per partial snippet); "
              "step angle NOT published; bipolar NOT confirmed; lot unknown",
        note="This is the untraced basis of the $1.05 line. Product page is "
             "JS-only/bot-walled; step angle cannot be confirmed. It is the "
             "exact source of K7's uncertainty.",
    ),
    dict(
        id="AliExpress-10pc",
        title="10 Pcs 3-5V DC 2 Phase 4 Wire Dia 8mm Micro Stepper Motor (8x9.5mm)",
        vendor="AliExpress",
        url="https://nl.aliexpress.com/item/32908973633.html",
        unit_usd=0.86,
        qty_basis="10-pc pack (EUR7.89 total)",
        evidence="UNVERIFIED-MARKETPLACE",
        matched=False,
        specs="8x9.5mm, 3-5V, 2-phase 4-wire; step angle NOT published; "
              "bipolar NOT confirmed",
        note="Cheapest per-unit marketplace found, but no step-angle or "
             "bipolar spec and item page is JS-only.",
    ),
    dict(
        id="AliExpress-micro-8mm",
        title="Micro Mini 8 mm 2-phase 4-wire stepper with copper gear",
        vendor="AliExpress",
        url="https://nl.aliexpress.com/item/4000806393169.html",
        unit_usd=2.66,
        qty_basis="1 pc (EUR2.66)",
        evidence="UNVERIFIED-MARKETPLACE",
        matched=False,
        specs="8mm, 2-phase 4-wire, copper gear; step angle NOT published",
        note="The 'sourced $2.66' downside used in cost_closure. Still not a "
             "matched part (no 18deg confirmation) and already over the ceiling.",
    ),
    dict(
        id="AliExpress-linear-8-10",
        title="8/10mm 2-phase 4-wire screw-slide micro stepper linear actuator",
        vendor="AliExpress",
        url="https://nl.aliexpress.com/item/1005008916092796.html",
        unit_usd=3.59,
        qty_basis="1 pc (EUR3.59)",
        evidence="UNVERIFIED-MARKETPLACE",
        matched=False,
        specs="8/10mm, 2-phase 4-wire, screw-slider; step angle NOT published",
        note="Linear variant, different interface; not a drop-in rotary part.",
    ),
]

# Mainstream distributors that do NOT stock a bare 8 mm 18 deg bipolar PM
# stepper as a discrete part (recorded so the negative is auditable).
MAINSTREAM_NOT_STOCKED = [
    "LCSC (search + wwwapi endpoints returned no 8 mm PM stepper)",
    "DigiKey (HTTP 403 bot wall)",
    "Mouser (Access Denied)",
    "Octopart (only large/NEMA hybrid + integrated PANdrives)",
    "Adafruit (nearest is NEMA-8 20x30 mm hybrid at $19.95)",
    "Pololu (no 8 mm micro PM stepper; NEMA11+ only)",
    "SparkFun (no match)",
    "Made-in-China / Alibaba factory listings (8 mm 18deg family bottoms at "
    "~$8.20 at 3,000+ units)",
]


def matched_candidates() -> list[dict]:
    """Matched = same 8 mm/18deg/2-phase-bipolar format AND currently
    actionable (live listing, orderable quantity). Historical surplus
    (PM08-2) and marketplace multipacks with no published step angle are
    excluded even though a few carry the right format on paper."""
    return [c for c in CANDIDATES
            if c["matched"] and c["evidence"].startswith("SOURCED-LIVE")]


def delivered_total(motor_unit_usd: float, channels: int = CHANNELS) -> float:
    """Delivered purchased total on the machine-preserving E1-E6 basis."""
    return round((_fixed_parts() + channels * motor_unit_usd) * UPLIFT, 2)


def verdict() -> dict:
    fixed = _fixed_parts()
    break_even_motor = (CEILING / UPLIFT - fixed) / CHANNELS
    cheapest = min(matched_candidates(), key=lambda c: c["unit_usd"])
    rows = sorted(
        (dict(id=c["id"], unit=c["unit_usd"], delivered=delivered_total(c["unit_usd"]),
              margin=round(CEILING - delivered_total(c["unit_usd"]), 2),
              evidence=c["evidence"], matched=c["matched"])
         for c in CANDIDATES),
        key=lambda r: r["unit"],
    )
    return dict(
        fixed_parts_usd=round(fixed, 2),
        break_even_motor_usd=round(break_even_motor, 4),
        cheapest_matched_id=cheapest["id"],
        cheapest_matched_unit_usd=cheapest["unit_usd"],
        cheapest_matched_at_100qty_usd=11.20,
        cheapest_matched_delivered_usd=delivered_total(11.20),
        moons_delivered_usd=delivered_total(40.00),
        untraced_multipack_delivered_usd=delivered_total(1.05),
        rows=rows,
        verdict=("REFUTED: no matched, traced 8 mm 18deg bipolar PM stepper "
                 "exists at or below $1.86 delivered. The cheapest matched "
                 "part is CCHT at $11.20 @100 (or $8.20 @3001+), which puts "
                 "the machine at $1,088.47-$1,366.87 delivered, over the "
                 "$500 ceiling. The sub-$1.86 path exists only for an "
                 "untraced marketplace multipack with no published step angle."),
    )


def design_lever() -> dict:
    """Timing cost of reducing the head channel count (the only machine-level
    lever that would let an $8.20 matched motor fit)."""
    import timing_closure as tc

    base = tc.full_map_s(400)
    rows = []
    for width in (80, 40, 20, 10, 5):
        passes = 80 / width
        row = passes * tc.per_row_assumption_s() + (tc.HOME_STEPS + tc.PROGRAM_STEPS) / 400
        idx = (passes - 1) * tc._travel(width * 5.08, tc.TIMING["scan_v_mm_s"],
                                        tc.TIMING["scan_a_mm_s2"]) \
            + tc._travel(5.08, tc.TIMING["scan_v_mm_s"], tc.TIMING["scan_a_mm_s2"])
        t = tc.fixed_s() + tc.ROWS * row + tc.ROWS * idx
        rows.append(dict(width=width, motors=width, est_full_map_s=round(t, 2),
                         under_30s=t < 30.0))
    return dict(baseline_s=round(base, 3), rows=rows,
                conclusion="reducing the head below 80 channels blows the 30 s "
                "budget (W=40 -> ~104 s); the reduced-head lever is NOT viable.")


if __name__ == "__main__":
    import json
    print(json.dumps(verdict(), indent=2))
    print(json.dumps(design_lever(), indent=2))
