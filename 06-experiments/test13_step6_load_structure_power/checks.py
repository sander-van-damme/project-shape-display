"""CI checks for the DND-43 Step-6 load/structure/power model.

These checks do two jobs:
  1. freeze the arithmetic (regression), so the numbers cannot drift silently;
  2. assert the *honesty* rules of the Step: the structural result must be
     reported as a support-spacing finding, the lift-torque result must be
     allowed to fail, and the power-cut result must not be hidden.

They do NOT assert that the machine passes -- some gates fail on purpose,
because a failing gate here is the evidence that kills or bounds a design
detail. A check that flips PASS->FAIL without a matching README change should
break CI; a check that records a known FAIL is green by design.

Run: python checks.py
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import model as m  # noqa: E402

FAILURES: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    status = "PASS" if cond else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f": {detail}"
    print(line)
    if not cond:
        FAILURES.append(name)


def main() -> int:
    d = m.step6_disposition(platen_kg=4.0, drag_n_per_cell=0.01)
    f = d["lift_force"]
    t = d["lift_torque"]
    sp = d["required_support_spacing"]
    pc = d["power_cut"]

    print("== Step 6 arithmetic regression ==")
    check("one column mass ~ 2.18 g (Test08 geometry)", 2.10 < f["column_mass_each_g"] < 2.25,
          f"{f['column_mass_each_g']:.3f} g")
    check("6400 columns ~ 13.9 kg", 13.5 < f["columns_total_kg"] < 14.5,
          f"{f['columns_total_kg']:.3f} kg")
    check("total lift force ~ 276 N", 250 < f["total_lift_force_n"] < 300,
          f"{f['total_lift_force_n']:.2f} N")

    print("\n== Structure: unsupported span must FAIL the flatness gate ==")
    check("unsupported 401.3 mm span defl > 0.25 mm gate",
          d["unsupported_full_span_defl_mm"] > m.FLATNESS_GATE_MM,
          f"{d['unsupported_full_span_defl_mm']:.3f} mm vs {m.FLATNESS_GATE_MM} mm")

    print("\n== Structure: spliced support spacing finding ==")
    # The Step's headline finding: at the soft printed modulus the 203.2 mm
    # support spacing assumed by 08-current-design does NOT meet the 0.25 mm
    # flatness gate once the splice is modelled.
    soft_203 = d["supported"]["203.2"]["soft_E700"]["spliced_defl_mm"]
    check("203.2 mm spliced span FAILS flatness at soft E700 (kills that spacing)",
          soft_203 > m.FLATNESS_GATE_MM, f"{soft_203:.3f} mm > {m.FLATNESS_GATE_MM} mm")
    bulk_203 = d["supported"]["203.2"]["bulk_E2500"]["spliced_defl_mm"]
    check("203.2 mm spliced span PASSES flatness at bulk E2500 (modulus is the lever)",
          bulk_203 <= m.FLATNESS_GATE_MM, f"{bulk_203:.3f} mm <= {m.FLATNESS_GATE_MM} mm")
    soft_101 = d["supported"]["101.6"]["soft_E700"]["spliced_defl_mm"]
    check("101.6 mm spliced span PASSES flatness even at soft E700",
          soft_101 <= m.FLATNESS_GATE_MM, f"{soft_101:.3f} mm")
    check("max spliced support spacing (soft E700) is 120-203 mm",
          120.0 < sp["max_spliced_span_mm"] < 203.5,
          f"{sp['max_spliced_span_mm']:.1f} mm")

    print("\n== Splice actually matters ==")
    # A spliced beam must deflect more than the monolithic uniform model on the
    # same span; otherwise the splice term is dead code and the Step proves
    # nothing about joints.
    uni = d["supported"]["203.2"]["soft_E700"]["uniform_defl_mm"]
    check("spliced defl > uniform defl on same span (joint adds compliance)",
          soft_203 > uni, f"spliced {soft_203:.3f} > uniform {uni:.3f} mm")

    print("\n== Lift torque-speed: the sourced allowance must be allowed to fail ==")
    check("8 mm lead running torque margin < 1.5 (baseline detail fails)",
          t["running_torque_margin"] < 1.5, f"{t['running_torque_margin']:.2f}x")
    sweep = {r["lead_mm"]: r for r in m.lift_lead_sweep()}
    check("2 mm lead running margin >= 1.5 (recovery lever works)",
          sweep[2.0]["running_margin"] >= 1.5, f"{sweep[2.0]['running_margin']:.2f}x")
    check("8 mm lead fails, 4 mm lead fails, 2 mm lead passes (monotone in lead)",
          (not sweep[8.0]["passes_1p5"]) and (not sweep[4.0]["passes_1p5"])
          and sweep[2.0]["passes_1p5"])
    check("4 mm/2 mm lead screw rpm stay under a 1200 rpm bearing bound",
          sweep[4.0]["screw_rpm_at_35mms"] <= 1200 and
          sweep[2.0]["screw_rpm_at_35mms"] <= 1200,
          f"{sweep[4.0]['screw_rpm_at_35mms']:.0f} / {sweep[2.0]['screw_rpm_at_35mms']:.0f} rpm")

    print("\n== Power-cut: the 8 mm lead does NOT self-lock ==")
    check("8 mm lead not self-locking (tan lambda 0.318 > mu 0.15)",
          pc["screw_self_locking"] is False)
    check("power-cut therefore requires a brake or detent",
          pc["requires_brake_or_detent"] is True)
    check("1 mm unload clearance gives >= 10 ms before toe impact",
          pc["fall_time_over_clearance_s"] >= 0.010,
          f"{pc['fall_time_over_clearance_s']*1000:.1f} ms")

    print("\n== Terrain patch load is not a frame killer at 1 N ==")
    tl = d["terrain_1N_20pct"]
    check("20% map at 1 N/cell rib stress < PLA yield",
          tl["passes"], f"{tl['rib_bending_stress_mpa']:.2f} MPa vs {m.PLA_YIELD_MPA} MPa")

    print("\n== Honesty rule: disposition is derived, not asserted ==")
    # The disposition dict must carry the failing lift gate so no reader can
    # mistake this for an all-pass Step.
    check("disposition exposes the failing running-margin gate",
          t["passes_running"] is False)
    check("disposition exposes the required support spacing",
          sp["max_spliced_span_mm"] > 0)
    check("platen blocks: 2 cartridges/axis at 203.2 mm (X1C limit)",
          d["platen_blocks"]["cartridges_axis"] == 2)

    print()
    if FAILURES:
        print(f"{len(FAILURES)} CHECK(S) FAILED: {FAILURES}")
        return 1
    print("ALL STEP-6 CHECKS PASS (findings are encoded, incl. the failing lift gate)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
