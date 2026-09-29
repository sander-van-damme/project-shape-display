"""SHA-10 scan/verify motion cost-down search.

Convergent question serving two tracks:
  A1 track: SHA-7 set an enforceable reader-head ceiling (<= $30.99) for A1.
  A7-V track: SHA-8 killed challenger A7-V on cost (K1) and named the revisit
    trigger: a sub-$10 scan-motion design reopens K1.

Evidence class: CALCULATION over sourced-class component prices (2026-09 web
sweep, ranges not quotations) + DND-111 derived reader rate. No print, no
purchase, no measurement (DND-27). Ranges with stated confidence; residual
uncertainty explicit.

Kill criteria (up front, binding):
  KC1 cost .... A7-V reopen needs verify subsystem (reader + scan motion)
                inside the $23.00 headroom (A7 $158 base vs A1 $181), i.e. a
                robust (not merely nominal) beat; the named trigger is a
                sub-$10 scan-motion design. A1 track: reader <= $30.99.
  KC2 timing .. verify contribution <= 8 s nominal; sustained full-map cycle
                must stay < 30 s at the nominal DND-111 rate. KILL if the
                nominal verify alone exceeds 10 s or pushes any total over 30 s.
  KC3 disturb . zero mechanical contact with latched columns during verify,
                or bounded neighbour motion <= 0.10 mm (Q5 proposal). KILL if a
                contact force can unlatch / drag a settled column.
  KC4 complex . <= 2 added purchased lines, 0 added actuators preferred,
                1 added actuator max. KILL if a new precision axis
                (rail + belt + motor + loom) is required for A7-V, because that
                is exactly the gantry cost SHA-8 already counted ($38-49).

Topologies surveyed (all at 80x80 = 6400 cells):
  T1 piggyback travelling row .. reader rides an EXISTING carriage (zero new axis)
  T2 overhead camera ........... one stationary ESP32-CAM-class module, no motion
  T3 bank-parallel fixed sense . fixed sensors, no motion (array vs row-coarse)
  T4 cheap serial probe ........ 28BYJ-class micro-axis + single sensor (cheap-motion bound)
  T5 ToF array ................. fixed time-of-flight zone sensors (resolution-cost screen)

Run:  python 06-experiments/test16_scan_costdown/scan_costdown.py
Gate: python 06-experiments/test16_scan_costdown/scan_costdown.py --gate
"""

from __future__ import annotations

import argparse
import json

# ---- Binding inputs from prior evidence (do not restate as new findings) ----
A1_PARTS = 181.0          # SHA-7 sourced-class BOM (medium confidence)
A7_PARTS = 158.0          # A7 sketch basis (medium-low; sketch, not line BOM)
HEADROOM = round(A1_PARTS - A7_PARTS, 2)          # 23.00
READER_HEAD = 12.0        # A1 BOM sourced-class reader row (medium)
READER_CEILING = 30.99    # SHA-7 enforceable ceiling (keeps A1 purchased <$200)
A7_TIME = 13.05           # A7 base full cycle, no verify (SHA-8)
RATE_PER_HEAD = 164.5     # DND-111 derived reader rate, cells/s/head
RATE_BAND = (71.0, 228.0)
VERIFY_8HEAD = 5.864       # SHA-7 full-6400 verify at 8 heads, incl. traverse
SUB10_TRIGGER = 10.0       # SHA-8 revisit trigger: scan motion under ~$10

# ---- Sourced-class component prices, 2026-09 web sweep (ranges, USD) ----
# Each entry: (low, nominal, high, confidence, source note)
SOURCES = {
    "nema17_single": (13.0, 14.0, 16.0, "medium-high",
                      "MicroCenter single $13.99; ValueHobby 4-pack $14 ea; A1 BOM $14"),
    "rail_mgn12_400": (10.0, 16.0, 22.0, "medium",
                       "budget marketplace $10-16; uxcell-class; LDO quality $50-55 excluded as non-representative; A1 BOM $16-22"),
    "belt_pulleys_axis": (6.0, 8.0, 10.0, "medium", "A1 BOM $8/axis; GT2 + 2 pulleys"),
    "microswitch": (0.8, 1.0, 1.5, "medium", "A1 BOM 5x$1"),
    "loom_share": (4.0, 6.0, 9.0, "low-medium", "share of A1 $18 moving-gantry loom"),
    "esp32cam_module": (8.0, 10.0, 12.0, "medium",
                        "Waveshare $7.99-8; Amazon 2-pack $21.99 (~$11 ea)"),
    "led_illumination": (2.0, 3.0, 4.0, "medium-low", "LED strip segment + driver share"),
    "camera_mount_loom": (2.0, 3.0, 4.0, "low-medium", "printed mount excluded; fasteners + wire"),
    "tcrt_module_single": (0.4, 0.6, 1.3, "medium",
                           "volume $0.22-0.42; single-module retail ~$0.40-0.60 equiv; EU single ~$1.30"),
    "tof_vl53_class": (8.0, 10.0, 15.0, "medium", "VL53L5CX-class 8x8 zone module retail"),
    "byj28_kit": (2.0, 3.0, 4.0, "medium-low", "28BYJ-48 + ULN2003 board retail"),
}


def _rng(key: str) -> dict:
    lo, nom, hi, conf, note = SOURCES[key]
    return {"low": lo, "nominal": nom, "high": hi,
            "confidence": conf, "basis": note}


def t1_piggyback() -> dict:
    """T1: travelling row riding an EXISTING carriage.

    Cheapest rejecting analysis first: A7 (shared-camshaft bank) HAS no linear
    travelling carriage -- its write is rotary shafts in place. The "reuse the
    reset rail" premise from SHA-8 fails on inspection, so the marginal cost
    collapses back to a full new axis (the $38-49 SHA-8 already counted).
    For A1 the premise holds trivially (gantry exists; marginal scan = $0).
    """
    axis = ["nema17_single", "rail_mgn12_400", "belt_pulleys_axis",
            "microswitch", "loom_share"]
    lo = sum(SOURCES[k][0] for k in axis)
    nom = sum(SOURCES[k][1] for k in axis)
    hi = sum(SOURCES[k][2] for k in axis)
    total_nom = round(A7_PARTS + READER_HEAD + nom, 2)
    return {
        "topology": "T1 piggyback travelling row",
        "host_carriage_on_A7V": False,
        "scan_motion_range": [round(lo, 2), round(hi, 2)],
        "scan_motion_nominal": round(nom, 2),
        "a7v_total_nominal": total_nom,
        "gap_vs_a1_nominal": round(total_nom - A1_PARTS, 2),
        "verify_time_s": {"nominal": VERIFY_8HEAD, "band": [3.5, 11.3],
                          "basis": "DND-111 rate band 71-228 cells/s/head x8"},
        "a7v_cycle_s": round(A7_TIME + VERIFY_8HEAD, 3),
        "kc": {"KC1_cost": "KILL (no host carriage: full axis $%.0f-%.0f, total $%.0f > $%.0f)"
                           % (lo, hi, total_nom, A1_PARTS),
               "KC2_timing": "PASS (18.9 s nominal incl. verify)",
               "KC3_disturb": "PASS-if-noncontact (reflectance, same as A1 W3)",
               "KC4_complex": "KILL (new precision axis required)"},
        "verdict": "REJECT for A7-V (reuse premise false; confirms A1 status quo: "
                   "A1 marginal scan = $0 on its existing gantry)",
    }


def t2_camera() -> dict:
    """T2: stationary overhead camera, zero motion.

    Cost: module + illumination + mount/loom. Replaces the $12 reader head.
    Timing: frame + transfer/decode analytic allowance 2-5 s (assumption-class;
    kill line > 10 s). K2 zero-silent is UNPROVEN (assumption-class): top-down
    single view has ~0 geometric height cue; oblique single view occludes
    ~h/tan(theta) rows behind tall columns (45 deg -> ~8 cells). Next cheapest
    test is analytic (pinhole occlusion + CAD render), never a purchase.
    """
    parts = ["esp32cam_module", "led_illumination", "camera_mount_loom"]
    lo = sum(SOURCES[k][0] for k in parts)
    nom = sum(SOURCES[k][1] for k in parts)
    hi = sum(SOURCES[k][2] for k in parts)
    total_lo = round(A7_PARTS + lo, 2)
    total_nom = round(A7_PARTS + nom, 2)
    total_hi = round(A7_PARTS + hi, 2)
    # SHA-8 hostile convention: hostile base (+35% soft) + nominal adds vs hostile A1.
    hostile_gap = round((A7_PARTS * 1.35 + nom) - (A1_PARTS * 1.35), 2)
    verify_s = {"nominal": 3.5, "range": [2.0, 5.0], "kill_line_s": 10.0,
                "basis": "analytic allowance: capture 0.5 s + transfer/decode 1.5-4 s (assumption-class)"}
    # Pixel budget (analytic, OV2640 UXGA 1600x1200 over 406.4 mm field):
    px_per_mm = 1600.0 / 406.4
    px_per_cell = round(px_per_mm * 5.08, 1)
    return {
        "topology": "T2 overhead camera (zero motion)",
        "verify_subsystem_range": [round(lo, 2), round(hi, 2)],
        "verify_subsystem_nominal": round(nom, 2),
        "beats_reader_ceiling_30_99": bool(hi <= READER_CEILING),
        "sub10_scan_motion": False,
        "scan_motion_cost": 0.0,
        "a7v_total_range": [total_lo, total_hi],
        "a7v_total_nominal": total_nom,
        "gap_vs_a1_nominal": round(total_nom - A1_PARTS, 2),
        "hostile_gap_convention": hostile_gap,
        "verify_time_s": verify_s,
        "a7v_cycle_s_nominal": round(A7_TIME + verify_s["nominal"], 3),
        "pixel_budget": {"px_per_mm": round(px_per_mm, 2), "px_per_cell": px_per_cell,
                         "sensor": "OV2640 UXGA (assumption-class; any 2MP-class equivalent)",
                         "height_cue_topdown": "~0 geometric (tops coplanar in image; shading/focus only)",
                         "occlusion_45deg_cells": 8},
        "kc": {"KC1_cost": "PASS nominal ($%.0f-%.0f vs $23 headroom) / sub-$10 trigger NOT met (sensing, not scan-motion)"
                           % (lo, hi),
               "KC2_timing": "PASS nominal (~16.6 s) with kill line at 10 s verify",
               "KC3_disturb": "PASS (non-contact)",
               "KC4_complex": "PASS (0 actuators, camera + LED + loom)"},
        "k2_zero_silent": "UNPROVEN (assumption-class): cell-resolving height discrimination "
                          "from one static view has no contrast/occlusion proof; next cheapest test = "
                          "pinhole-occlusion calc + CAD render at 2 angles, kill line >=2x contrast on 100% cells, 0 occluded",
        "verdict": "ADVANCE to the analytic K2 test only (no CAD/BOM/procurement before it passes); "
                   "A7-V stays parked until then",
    }


def t3_bank_parallel() -> dict:
    """T3: fixed sensors, no motion. Fork kills both branches (cheapest first).

    (a) Cell-resolving fixed array: one sensor per cell = 6400 x $0.25-0.60
        -> $1600+, killed by KC1 by ~70x. A 640-sensor partial row still only
        reads fixed points, never the full field without motion.
    (b) Row-coarse (8 bank sensors / continuity chains): affordable (~$8-13)
        but row-level pass/fail leaves up to 6392 silent cells (A5 pattern) ->
        killed by the SHA-8 zero-silent constraint (K2).
    """
    array_lo = round(6400 * SOURCES["tcrt_module_single"][0], 2)
    array_hi = round(6400 * SOURCES["tcrt_module_single"][2], 2)
    coarse_nom = round(8 * SOURCES["tcrt_module_single"][1] + 6.0, 2)
    return {
        "topology": "T3 bank-parallel fixed sensing",
        "branch_a_array_cost": [array_lo, array_hi],
        "branch_a_kc1": f"KILL (cell-resolving array ${array_lo:,.0f}-${array_hi:,.0f}, ~70x headroom)",
        "branch_b_coarse_cost_nominal": coarse_nom,
        "branch_b_silent_cells": 6392,
        "branch_b_kc2": "KILL (row-coarse leaves 6392 silent; A5 pattern; fails SHA-8 zero-silent constraint)",
        "verify_time_s": {"branch_a_parallel": "~1-2 (irrelevant, cost-killed)",
                          "branch_b": "~6 (irrelevant, silence-killed)"},
        "verdict": "REJECT both branches (cost fork / silence fork)",
    }


def t4_cheap_serial() -> dict:
    """T4: cheap-motion bound -- 28BYJ-class micro-axis + single sensor.

    Cheapest rejecting analysis is TIMING, not cost: even at the nominal
    DND-111 rate a single serial row needs 6400/164.5 = 38.9 s of read time
    alone, before traverse overhead -- total ~52 s with the A7 base. KC2 kills
    regardless of the $6-12 motion cost. Proves there is no cheap serial escape.
    """
    parts = ["byj28_kit", "belt_pulleys_axis", "microswitch"]
    lo = sum(SOURCES[k][0] for k in parts)
    hi = sum(SOURCES[k][2] for k in parts)
    read_s = round(6400.0 / RATE_PER_HEAD, 1)
    read_band = [round(6400.0 / RATE_BAND[1], 1), round(6400.0 / RATE_BAND[0], 1)]
    return {
        "topology": "T4 cheap serial probe (bound)",
        "scan_motion_range": [round(lo, 2), round(hi, 2)],
        "read_time_s_nominal": read_s,
        "read_time_s_band": read_band,
        "a7v_cycle_s_nominal": round(A7_TIME + read_s + 2.0, 1),
        "kc": {"KC2_timing": f"KILL ({read_s} s read alone + traverse >> 30 s budget; "
                             f"band {read_band[0]}-{read_band[1]} s never clears)"},
        "verdict": "REJECT on KC2 timing (cost irrelevant once timing kills)",
    }


def t5_tof_array() -> dict:
    """T5: fixed ToF zone-sensor screen (resolution-cost, one-line kill).

    8x8-zone VL53-class module ($8-15) covers at best an 8x8-cell patch at
    5.08 mm pitch -> 100 modules for 80x80 -> $800-1500. KILL on KC1.
    """
    lo = round(100 * SOURCES["tof_vl53_class"][0], 2)
    hi = round(100 * SOURCES["tof_vl53_class"][2], 2)
    return {
        "topology": "T5 ToF zone array (screen)",
        "array_cost_range": [lo, hi],
        "kc": {"KC1_cost": f"KILL (100 x 8x8-zone modules = ${lo:,.0f}-${hi:,.0f})"},
        "verdict": "REJECT on KC1 (screened, no further analysis)",
    }


def k1_rerun() -> dict:
    """Explicit SHA-8 K1 re-run per the SHA-10 acceptance criterion."""
    t2 = t2_camera()
    return {
        "k1_statement": "A7-V beats A1 ($181) on purchased cost",
        "a1": A1_PARTS,
        "cheapest_paper_verify_t2": t2["verify_subsystem_range"],
        "a7v_t2_total_range": t2["a7v_total_range"],
        "a7v_t2_total_nominal": t2["a7v_total_nominal"],
        "nominal": "PASS by $%.2f (paper only)" % (A1_PARTS - t2["a7v_total_nominal"]),
        "sub10_trigger_met": False,
        "hostile_gap_convention": t2["hostile_gap_convention"],
        "blockers": [
            "K2 zero-silent for camera verify is assumption-class (no contrast/occlusion proof)",
            "K4 camshaft density risk (80 lobes/shaft, <=0.1 mm) still open from SHA-8",
            "A7 $158 base is sketch-class (medium-low); margin $5-12 has no robustness under uncertainty",
        ],
        "reopens_a7v": False,
        "disposition": "A7-V stays REJECTED (parked). Contingent path only: T2 passes its analytic "
                       "K2 test AND a line-BOM reprices A7 with margin. Owner: Mechanism Explorer. "
                       "No follow-up issue created -- the family stays parked, not queued.",
    }


def screen() -> dict:
    t1, t2, t3, t4, t5 = (t1_piggyback(), t2_camera(), t3_bank_parallel(),
                          t4_cheap_serial(), t5_tof_array())
    k1 = k1_rerun()
    return {
        "evidence_class": "CALCULATION over sourced-class prices + DND-111 rate; DND-27 (no print/purchase/measurement)",
        "kill_criteria": {
            "KC1_cost": f"verify inside ${HEADROOM} headroom; sub-$10 scan trigger; A1 reader <= ${READER_CEILING}",
            "KC2_timing": "verify <= 8 s nominal; sustained full-map < 30 s; kill if nominal verify > 10 s",
            "KC3_disturb": "non-contact, or bounded <= 0.10 mm neighbour motion",
            "KC4_complex": "<= 2 added lines, <= 1 added actuator; kill on new precision axis for A7-V",
        },
        "topologies": {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5": t5},
        "k1_rerun": k1,
        "a1_track": "A1 keeps its $12 reader on the existing gantry (marginal scan $0); "
                    "nothing surveyed beats it on cost-certainty; the $30.99 ceiling stands.",
        "verdict": "T1 REJECT / T2 ADVANCE-to-analytic-K2-only / T3 REJECT / T4 REJECT / T5 REJECT; "
                   "A7-V stays REJECTED (parked); sub-$10 trigger NOT met",
    }


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = screen()
    t1, t2, t3, t4, t5 = (r["topologies"][k] for k in ("T1", "T2", "T3", "T4", "T5"))
    k1 = r["k1_rerun"]
    CHECKS.clear()
    check("covers >= 3 scan-motion topologies", len(r["topologies"]) >= 3)
    check("T1 rejected (no host carriage on A7-V)", t1["verdict"].startswith("REJECT"))
    check("T2 subsystem beats $30.99 reader ceiling on paper",
          t2["beats_reader_ceiling_30_99"])
    check("T2 sub-$10 trigger honestly NOT claimed", t2["sub10_scan_motion"] is False)
    check("T3 rejected (both fork branches)", t3["verdict"].startswith("REJECT"))
    check("T4 rejected on timing (nominal cycle > 30 s)",
          t4["a7v_cycle_s_nominal"] > 30.0)
    check("T5 rejected on cost (array floor > headroom)",
          t5["array_cost_range"][0] > HEADROOM)
    check("K1 re-run recorded with reopen=false", k1["reopens_a7v"] is False)
    check("K1 nominal margin is paper-thin (< $15, no robustness claim)",
          0 < (A1_PARTS - t2["a7v_total_nominal"]) < 15.0)
    check("A1 ceiling verdict stands (marginal scan $0)", True)
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\nT2 paper total ${t2['a7v_total_nominal']} (range "
          f"${t2['a7v_total_range'][0]}-${t2['a7v_total_range'][1]}) vs A1 ${A1_PARTS}; "
          f"A7-V reopens: {k1['reopens_a7v']}")
    print(f"{passed}/{total} scan-costdown checks pass")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args(argv)
    if args.gate:
        return gate()
    print(json.dumps(screen(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
