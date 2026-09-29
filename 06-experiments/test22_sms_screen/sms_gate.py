"""SHA-24 competing architecture — G1 scanning multi-spindle screw-column gate.

Cheapest analytic test for the Architecture Challenger lane: a shared-XY-gantry
spindle bar drives printed captive nuts on static screws (thread = memory +
brake + load path, zero per-cell bought parts), screened against the A1
baseline ($181 parts / <30 s sustained / zero-silent-error frame).

Evidence class: CALCULATION over design-criteria geometry (02) + textbook
thread mechanics + sourced-class actuator ratings. No print, no purchase, no
measurement (DND-27).

Binding insight asserted and checked below: 40 mm at the coarsest credible
printed multi-start lead (8 mm, 4-start x 2 mm pitch) still needs 5 turns per
full-stroke cell; at a generous 1,200 rpm spindle with engage/settle overhead
that is >= 0.25 s/cell of rotation time (NOT touch rate — E3's kill does not
bind here, this rotation bound does). 6,400 cells need >= 1,600
spindle-seconds, so < 30 s needs >= 54 spindles at the most favorable corner;
the nominal corner needs > 150. Dozens of Z-compliant spindles reintroduce
the per-channel bought cost A1 avoids (KC1), and open-loop turns are a full
6,400 silent set without the reader that killed A7-V on cost (KC3).

Kill criteria (up front, binding):
  KC2 timing .... spindles needed for <30 s must be buildable (<= ~16, the
                  S3-class bar ceiling); KILL if the optimistic corner needs
                  >= 54.
  KC1 cost ...... spindle bar + forced reader must beat A1 $181; KILL if the
                  optimistic spindle-count floor alone breaks it.
  KC3 silent .... open-loop screw drive must not be silently wrong 6,400x;
                  KILL as drawn (reader-fitted variant collapses into K1).
  (KC4 thread printability recorded in the verdict note; rotation time kills
  first and needs no coupon.)

Run:  python 06-experiments/test22_sms_screen/sms_gate.py
Gate: python 06-experiments/test22_sms_screen/sms_gate.py --gate
"""

from __future__ import annotations

import argparse

# ---- Board geometry (design criteria 02) ----
N_CELLS = 6400           # 80x80
TRAVEL_MM = 40.0         # minimum usable vertical travel
TIME_BUDGET_S = 30.0     # full-map change strictly < 30 s

# ---- Screw geometry (generous printable corner) ----
# Coarsest credible printed multi-start lead: 4-start x 2 mm pitch = 8 mm
# lead on a ~4-5 mm screw (0.5 mm flank features at 0.4 mm nozzle — already
# aggressive; finer pitch only adds turns and worsens the gate).
LEAD_MM = {"optimistic": 8.0, "nominal": 4.0}
# Turns per full-stroke cell = travel / lead.
# Spindle speed: generous small-DC-motor class under load.
SPINDLE_RPM = {"optimistic": 1200.0, "nominal": 600.0}
# Engage + settle overhead per cell (descend, seat bit, release).
OVERHEAD_S = {"optimistic": 0.05, "nominal": 0.15}

# ---- Bar ceilings ----
# Buildable spindle-bar ceiling: 16 (S3-class 4-row bar analogue; 16
# Z-compliant bits at 5.08 mm pitch with individual clutch/dog elements).
BAR_CEILING = 16
# Sourced-class floor per spindle channel (bit + clutch/dog share + belt
# share + drive share): $8 optimistic (E3 finger-floor class).
SPINDLE_FLOOR_USD = 8.0
A1_PARTS = 181.0         # SHA-7 sourced-class BOM (medium)

CHECKS: list[tuple[str, str]] = [
    ("turns_bound_holds",
     "full-stroke cell needs >= 5 turns even at the coarsest printed lead"),
    ("per_cell_screw_time_kills_serial",
     "per-cell screw time >= 0.25 s optimistic (vs A1 3 ms toggle)"),
    ("spindle_seconds_kill",
     "full map needs >= 1,600 spindle-seconds optimistic"),
    ("spindle_count_kills",
     "spindles for <30 s exceed the buildable bar ceiling at every corner"),
    ("spindle_cost_floor_kills",
     "optimistic spindle-count floor alone breaks the A1 cost ceiling"),
]


def evaluate(corner: str) -> dict[str, float]:
    """Evaluate one corner; returns the quantities the gate asserts."""
    turns = TRAVEL_MM / LEAD_MM[corner]
    screw_s = turns / (SPINDLE_RPM[corner] / 60.0)
    per_cell_s = screw_s + OVERHEAD_S[corner]
    spindle_seconds = N_CELLS * per_cell_s
    spindles_needed = spindle_seconds / TIME_BUDGET_S
    bar_cost_floor = spindles_needed * SPINDLE_FLOOR_USD
    return {
        "turns": turns,
        "per_cell_s": per_cell_s,
        "spindle_seconds": spindle_seconds,
        "spindles_needed": spindles_needed,
        "bar_cost_floor": bar_cost_floor,
    }


def run_gate() -> tuple[int, int, list[str]]:
    """Run all checks. Returns (passed, total, detail_lines)."""
    lines: list[str] = []
    passed = 0

    opt = evaluate("optimistic")
    nom = evaluate("nominal")

    # 1. turns bound holds (the geometry both corners share)
    ok = opt["turns"] >= 5.0 - 1e-9
    passed += ok
    lines.append(
        f"[{'PASS' if ok else 'FAIL'}] turns_bound_holds: "
        f"optimistic {opt['turns']:.1f} turns/cell "
        f"(40 mm / 8 mm lead), nominal {nom['turns']:.1f} (40/4)."
    )

    # 2. per-cell screw time vs A1 toggle class
    ok = opt["per_cell_s"] >= 0.25 - 1e-9
    passed += ok
    lines.append(
        f"[{'PASS' if ok else 'FAIL'}] per_cell_screw_time_kills_serial: "
        f"optimistic {opt['per_cell_s']:.2f} s/cell "
        f"({opt['turns']:.0f} turns @1200rpm + 0.05 s overhead) vs A1 "
        f"3 ms toggle — ~100x slower per cell."
    )

    # 3. spindle-seconds for a full map
    ok = opt["spindle_seconds"] >= 1600.0 - 1e-9
    passed += ok
    lines.append(
        f"[{'PASS' if ok else 'FAIL'}] spindle_seconds_kill: optimistic "
        f"{opt['spindle_seconds']:.0f} spindle-s, nominal "
        f"{nom['spindle_seconds']:.0f} (6400 cells x per-cell time)."
    )

    # 4. THE BINDING GATE: spindles needed vs buildable bar ceiling
    ok = opt["spindles_needed"] > BAR_CEILING
    passed += ok
    lines.append(
        f"[{'PASS' if ok else 'FAIL'}] spindle_count_kills: optimistic "
        f"{opt['spindles_needed']:.1f} spindles for <30 s "
        f"(>{BAR_CEILING} bar ceiling), nominal {nom['spindles_needed']:.1f}. "
        f"KILL — KC2."
    )

    # 5. cost corroboration: spindle floor alone vs A1
    ok = opt["bar_cost_floor"] > A1_PARTS
    passed += ok
    lines.append(
        f"[{'PASS' if ok else 'FAIL'}] spindle_cost_floor_kills: optimistic "
        f"bar floor ${opt['bar_cost_floor']:.0f} "
        f"({opt['spindles_needed']:.1f} x ${SPINDLE_FLOOR_USD:.0f}) > A1 "
        f"${A1_PARTS:.0f} before gantry/reader — KILL corroboration, KC1."
    )

    return passed, len(CHECKS), lines


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="SHA-24 G1 screw-matrix gate.")
    parser.add_argument(
        "--gate", action="store_true",
        help="exit non-zero unless every check passes",
    )
    args = parser.parse_args()
    passed, total, lines = run_gate()
    print(f"SHA-24 G1 screw-matrix gate: {passed}/{total} checks")
    for line in lines:
        print(f"  {line}")
    if args.gate and passed != total:
        print("GATE: FAIL — G1 killed (see verdict note).")
        return 1
    if args.gate:
        print("GATE: PASS — all kill conditions hold; G1 REJECTED.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
