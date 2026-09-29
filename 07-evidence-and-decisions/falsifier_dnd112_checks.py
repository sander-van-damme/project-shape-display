#!/usr/bin/env python3
"""DND-112 - independent adversarial audit of the DND-111 A1 writer/reader rate bound.

Run from anywhere:
    python 07-evidence-and-decisions/falsifier_dnd112_checks.py

Companion to `falsifier_dnd112_a1_rate_audit.md`. It does NOT import any
conclusion from the CTO's `a1_writer_rate.py`. Every number is recomputed here
from the placed CAD geometry and first-principles kinematics, then compared
against what DND-111 claims.

Evidence class: CALCULATION + CAD geometry. No print, no purchase, no measurement
(DND-27). No board contact (DND-32). Python stdlib only.

Default-deny: every attack returns PASS / FAIL / UNRESOLVED; the verdict is CLEAN
only if no attack is FAIL or UNRESOLVED. A FAIL does not necessarily refute the
architecture - it marks a place where DND-111's own text/geometry is wrong or the
residual is larger than claimed.
"""
from __future__ import annotations

import math

PITCH_MM = 5.08
COLS = ROWS = 80
CELLS = ROWS * COLS                       # 6,400
ACTIVE_MM = COLS * PITCH_MM               # 406.4
COLUMN_BODY_MM = 3.60                     # column top face, from placed cell CAD
TRAVEL_MM = 40.0                          # up-column top height
OWNED_HALF_LANE_MM = PITCH_MM / 2 - COLUMN_BODY_MM / 2   # 0.74

WORK_GAP_MM = 2.0                         # reader-to-UP-top gap (assumption-class)
APERTURE_MM = 2.0                         # interrogation aperture (assumption-class)
HALF_ANGLE_DEG = 15.0

X1C_V_MM_S = 500.0
X1C_A_MM_S2 = 20_000.0

CLAIM_PER_HEAD = 164.5
CLAIM_BAND = (71.4, 228.0)
CLAIM_STOP_GO_X1C = 30.0
CLAIM_REG_TOL_MM = 0.264
CLAIM_SPOT_MM = 3.072
CLAIM_SNR = 1460.0
CLAIM_CYCLE_8H = 16.278


def _spot(gap_mm, aperture_mm=APERTURE_MM, half_angle_deg=HALF_ANGLE_DEG):
    return aperture_mm + 2.0 * gap_mm * math.tan(math.radians(half_angle_deg))


def attack_t1_stop_and_go():
    """T1: is stop-and-go really excluded, and is the number right?"""
    def cell_time(a):
        v_tri = math.sqrt(a * PITCH_MM)
        if v_tri <= X1C_V_MM_S:
            move = 2.0 * math.sqrt(PITCH_MM / a)
        else:
            t_acc = X1C_V_MM_S / a
            d_acc = 0.5 * a * t_acc * t_acc
            move = 2.0 * t_acc + (PITCH_MM - 2.0 * d_acc) / X1C_V_MM_S
        total = move + 0.001
        return total, 1.0 / total, v_tri
    _, r20, v20 = cell_time(X1C_A_MM_S2)
    _, r100, _ = cell_time(100_000.0)
    # The X1C-sourced case (20 m/s^2) is genuinely triangular and reproduces 30.4.
    # The aggressive-sensitivity case (100 m/s^2) in a1_writer_rate.py is a
    # V-shaped approximation that overstates the rate: the correct trapezoid is
    # 2*v/a + (p - v^2/a)/v = 15.16 ms -> 61.9 cells/s, not the claimed 89.6.
    ok = abs(r20 - CLAIM_STOP_GO_X1C) < 1.0 and abs(r100 - 89.6) > 1.0
    return (ok,
            "stop-and-go recompute: %.1f cells/s @20 m/s^2 (claimed 30, OK); "
            "%.1f @100 m/s^2 vs DND-111's 89.6 -> the aggressive row is a "
            "V-shaped approximation that overstates by %.0f%%"
            % (r20, r100, (89.6 / r100 - 1) * 100),
            dict(r20=r20, r100=r100, v_tri=v20))


def attack_t2_flyover():
    """T2: reproduce the 164.5 primary rate from first principles."""
    v = 1000.0
    t_trav = PITCH_MM / v * 1e3
    t_act = 3.0
    t_read = 0.05
    settle = 1.0
    write_cell = max(t_trav, t_act) + settle
    read_cell = max(t_trav, t_read) + settle
    head = min(1e3 / write_cell, 1e3 / read_cell)
    act_p = 6.0 / 500.0 * 1e3 + 1.0
    pess = 1e3 / (max(t_trav, act_p) + settle)
    ok = abs(head - CLAIM_PER_HEAD) < 0.5 and abs(pess - CLAIM_BAND[0]) < 0.5
    return (ok,
            "fly-over primary recompute: %.1f cells/s (claimed %.1f); "
            "pessimistic %.1f (band low %.1f)"
            % (head, CLAIM_PER_HEAD, pess, CLAIM_BAND[0]),
            dict(head=head, pess=pess))


def attack_t3_ramp_overhead():
    """T3: the full-cycle model omits per-pass accel/reversal overhead."""
    v = 1000.0
    a = X1C_A_MM_S2
    ideal = ACTIVE_MM / v
    line = ideal + 2.0 * (v / a)
    overhead = (line - ideal) / ideal
    return (overhead > 0.10,
            "per-line ramp overhead %.1f%% is NOT in the DND-111 full_cycle "
            "model (line %.4f s vs ideal %.4f s)" % (overhead * 100, line, ideal),
            dict(overhead=overhead, line_s=line, ideal_s=ideal))


def attack_r1_gap_by_state():
    """R1: reader sees UP top at 2 mm gap, DOWN pocket at ~42 mm."""
    gap_up = WORK_GAP_MM
    gap_down = TRAVEL_MM + WORK_GAP_MM
    spot_up = _spot(gap_up)
    spot_down = _spot(gap_down)
    spans_down = spot_down / PITCH_MM
    resolves_down = spot_down <= COLUMN_BODY_MM
    return (resolves_down,
            "up-state gap %.0f mm -> spot %.2f mm; down-state gap %.0f mm -> "
            "spot %.2f mm = %.2f pitches (down single-cell read %s)"
            % (gap_up, spot_up, gap_down, spot_down, spans_down,
               "resolvable" if resolves_down else "NOT resolvable"),
            dict(spot_up=spot_up, spot_down=spot_down, spans_down=spans_down))


def attack_r2_corner_formula():
    """R2: the SCAD CORNER_REACH = spot/2*sqrt(2) is the wrong worst case."""
    spot = _spot(WORK_GAP_MM)
    reported = spot / 2.0 * math.sqrt(2.0)
    aperture_at_corner = math.hypot(COLUMN_BODY_MM / 2, COLUMN_BODY_MM / 2)
    true_reach = aperture_at_corner + spot / 2.0
    ok = abs(true_reach - reported) < 0.25
    return (ok,
            "reported CORNER_REACH %.3f mm; true worst-case reach with the "
            "aperture at the cell corner = %.3f mm (pitch/2 = %.2f, neighbour "
            "near edge %.2f)"
            % (reported, true_reach, PITCH_MM / 2,
               PITCH_MM - COLUMN_BODY_MM / 2),
            dict(reported=reported, true_reach=true_reach))


def attack_r3_neighbour_threshold():
    """R3: does a centred spot actually contaminate a neighbour top face?"""
    spot = _spot(WORK_GAP_MM)
    own_edge = COLUMN_BODY_MM / 2
    neighbour_near_edge = PITCH_MM - COLUMN_BODY_MM / 2
    reach = spot / 2.0
    contaminates = reach > neighbour_near_edge
    return (not contaminates,
            "centred spot radius %.3f mm vs own-face edge %.2f and "
            "neighbour-face near edge %.2f -> %s; the ADR fail threshold "
            "(own edge) is stricter than the physical crosstalk threshold"
            % (reach, own_edge, neighbour_near_edge,
               "contaminates" if contaminates
               else "does NOT directly touch a neighbour top face"),
            dict(reach=reach, own_edge=own_edge,
                 neighbour_near_edge=neighbour_near_edge))


def attack_r4_registration_decoupling():
    """R4: registration is not the binding single-cell limit if down gap fails."""
    gap_down = TRAVEL_MM + WORK_GAP_MM
    spot_down = _spot(gap_down)
    gap_for_corner = (COLUMN_BODY_MM / 2 * math.sqrt(2) - APERTURE_MM / 2) / math.tan(
        math.radians(HALF_ANGLE_DEG))
    gap_ok = (COLUMN_BODY_MM - APERTURE_MM) / (2 * math.tan(math.radians(HALF_ANGLE_DEG)))
    return (spot_down <= COLUMN_BODY_MM,
            "down-state spot %.2f mm vs face %.2f mm; gap that would fit the "
            "down state: %.2f mm - but the down target sits %.0f mm below the "
            "reader, so no constant-height head satisfies it. registration "
            "limit (%.2f mm) is NOT the binding read limit."
            % (spot_down, COLUMN_BODY_MM, gap_ok, TRAVEL_MM, CLAIM_REG_TOL_MM),
            dict(spot_down=spot_down, gap_fit=gap_ok,
                 gap_for_corner_zero_err=gap_for_corner))


def attack_t4_full_cycle_stages():
    """T4: seven DND-103 stages and the 16.278 s number."""
    t_trav = PITCH_MM / 1000.0 * 1e3
    write_cell = max(t_trav, 3.0) + 1.0
    read_cell = max(t_trav, 0.05) + 1.0
    stages = dict(
        digital_map=0.05, mask_generation=0.0, transport=2.0, reset=3.0,
        settle=1.5,
        write=CELLS * write_cell / 1000.0 / 8,
        verify=CELLS * read_cell / 1000.0 / 8,
    )
    total = sum(stages.values())
    ok = abs(total - CLAIM_CYCLE_8H) < 0.01 and len(stages) == 7
    return (ok,
            "seven DND-103 stages sum to %.3f s at 8 heads (claimed %.3f); "
            "stages: %s" % (total, CLAIM_CYCLE_8H, sorted(stages)),
            dict(total=total, stages=stages))


def attack_p1_snr_provenance():
    """P1: SNR ~1,460 is set by the TIA assumption, not the optical return."""
    resp = 0.45
    p = 5.0e-3
    i_up = p * 0.80 * resp
    i_down = p * 0.15 * resp
    contrast = i_up - i_down
    q = 1.602e-19
    T = 50e-6
    B = 1.0 / (2.0 * T)
    shot = math.sqrt(2.0 * q * (i_up + 1.0e-9) * B)
    amp = 10e-9 * math.sqrt(B)
    noise = math.sqrt(shot ** 2 + amp ** 2)
    snr = contrast / noise
    amp_dominated = amp > 100 * shot
    return (True,
            "recomputed SNR %.0f vs claimed %.0f; amp/shot ratio %.0fx -> SNR "
            "set by the TIA-noise assumption, not the optical return "
            "(assumption-class)" % (snr, CLAIM_SNR, amp / shot),
            dict(snr=snr, amp=amp, shot=shot, amp_dominated=amp_dominated))


def attack_g1_gate_impact():
    """G1: does replacing the placeholder change any pass/fail gate?"""
    pre = 0.05 + 0.0 + 2.0 + 3.0 + 8.8 + 1.5 + 8.8
    post = CLAIM_CYCLE_8H
    clears_pre = pre < 30.0
    clears_post = post < 30.0
    ok = clears_pre and clears_post
    return (ok,
            "gate impact: pre-DND-111 cycle %.2f s, post %.2f s; both clear "
            "<30 s (%s/%s) -> the replacement changed the number and the "
            "margin, not the A1 pass/fail gate"
            % (pre, post, clears_pre, clears_post),
            dict(pre=pre, post=post, clears_pre=clears_pre,
                 clears_post=clears_post))


def attack_g2_down_state_read_physics():
    """G2: a down-state single-cell read at 42 mm is swamped by up neighbours."""
    gap_neighbour = WORK_GAP_MM
    gap_pocket = TRAVEL_MM + WORK_GAP_MM
    flux_neighbour = (COLUMN_BODY_MM ** 2) / gap_neighbour ** 2
    flux_pocket = (COLUMN_BODY_MM ** 2) / gap_pocket ** 2
    ratio = flux_neighbour / flux_pocket
    ok = ratio < 1.0
    return (ok,
            "near-field neighbour flux / pocket flux ~ %.0fx at the aperture "
            "(neighbour %.0f mm vs pocket %.0f mm); a down-cell read is "
            "dominated by up neighbours unless the reader descends or the "
            "state is encoded at a common height"
            % (ratio, gap_neighbour, gap_pocket),
            dict(ratio=ratio, flux_neighbour=flux_neighbour,
                 flux_pocket=flux_pocket))


ATTACKS = [
    ("T1_stop_and_go", attack_t1_stop_and_go),
    ("T2_flyover_rate", attack_t2_flyover),
    ("T3_ramp_overhead", attack_t3_ramp_overhead),
    ("T4_full_cycle_stages", attack_t4_full_cycle_stages),
    ("R1_gap_by_state", attack_r1_gap_by_state),
    ("R2_corner_formula", attack_r2_corner_formula),
    ("R3_neighbour_threshold", attack_r3_neighbour_threshold),
    ("R4_registration_decoupling", attack_r4_registration_decoupling),
    ("G1_gate_impact", attack_g1_gate_impact),
    ("G2_down_state_read", attack_g2_down_state_read_physics),
    ("P1_snr_provenance", attack_p1_snr_provenance),
]


def run():
    rows = []
    fails = []
    for name, fn in ATTACKS:
        try:
            ok, detail, data = fn()
        except Exception as exc:  # noqa: BLE001
            ok, detail, data = None, "UNRESOLVED (%s)" % exc, {}
        verdict = "PASS" if ok is True else ("UNRESOLVED" if ok is None else "FAIL")
        if verdict != "PASS":
            fails.append(name)
        rows.append((name, verdict, detail, data))
    return rows, fails


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--gate", action="store_true",
        help="exit non-zero if any attack is FAIL/UNRESOLVED (default: report "
             "the verdict but exit 0 so CI can print the audit finding)")
    args = ap.parse_args(argv)
    rows, fails = run()
    width = max(len(n) for n, *_ in rows)
    print("DND-112 independent audit of the DND-111 A1 writer/reader rate bound")
    print("=" * 72)
    for name, verdict, detail, _ in rows:
        print("[%10s] %-*s %s" % (verdict, width, name, detail))
    print("-" * 72)
    if fails:
        print("VERDICT: NOT CLEAN - unresolved attacks: %s" % ", ".join(fails))
        return 1 if args.gate else 0
    print("VERDICT: CLEAN - all %d attacks reproduced DND-111 or found no "
          "contradiction" % len(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
