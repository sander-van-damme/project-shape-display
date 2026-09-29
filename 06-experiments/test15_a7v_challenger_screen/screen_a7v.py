"""SHA-8 challenger screen: A7-V (verified camshaft) vs A1.

Evidence class: CALCULATION over sourced-class figures from
08-integrated-designs/a1-reliability-first (A1 $181 / A7 $158) and the
DND-111 derived reader rate (164.5 cells/s/head, 71-228 band).
No print, purchase or measurement (DND-27). Ranges, not false precision.
"""

from __future__ import annotations

import json

A1_PARTS = 181.0
A7_PARTS = 158.0
READER_HEAD = 12.0          # A1 BOM sourced-class reader head row
SCAN_LOW = 38.0             # 14 stepper + 16 rail + 8 belt (sourced-class low)
SCAN_HIGH = 49.0            # + rail pair / switches / loom share (high)
A7_TIME = 13.05             # A7 base full cycle (no verify)
VERIFY_8HEAD = 5.864        # DND-111/DND-113 full 6400 verify at 8 heads
RATE_PER_HEAD = 164.5
RATE_BAND = (71.0, 228.0)


def screen() -> dict:
    headroom = round(A1_PARTS - A7_PARTS, 2)
    low = round(A7_PARTS + READER_HEAD + SCAN_LOW, 2)
    high = round(A7_PARTS + READER_HEAD + SCAN_HIGH, 2)
    # Reuse credit: even if the scan reuses the reset-carriage rail, a
    # belt + switches + loom share (~$20 low estimate) is still required.
    reuse_low = round(A7_PARTS + READER_HEAD + 20.0, 2)
    full_8head = round(A7_TIME + VERIFY_8HEAD, 3)
    single_head = round(A7_TIME + 6400.0 / RATE_PER_HEAD, 3)
    # hostile +35% soft-line uplift (DND-104 A7 audit convention)
    hostile_gap = round((A7_PARTS * 1.35 + READER_HEAD + SCAN_LOW) - (A1_PARTS * 1.35), 2)
    return {
        "evidence_class": "CALCULATION over sourced-class BOM + DND-111 rate; DND-27",
        "cost": {
            "a1_parts": A1_PARTS, "a7_parts": A7_PARTS, "headroom": headroom,
            "reader_head": READER_HEAD, "scan_motion_range": [SCAN_LOW, SCAN_HIGH],
            "a7v_range": [low, high], "a7v_reuse_credit_low": reuse_low,
            "gap_vs_a1_low": round(low - A1_PARTS, 2),
            "hostile_35pct_gap": hostile_gap,
            "k1_verdict": "KILL" if reuse_low >= A1_PARTS else "PASS",
        },
        "timing": {
            "a7_base": A7_TIME, "verify_8head": VERIFY_8HEAD,
            "a7v_full_8head": full_8head, "a7v_single_scan_row": single_head,
            "rate_band": list(RATE_BAND),
            "k3_verdict": "PASS only with 8-head reader (+cost); single scan row FAILS (52 s)",
        },
        "silent_error": {
            "a7_base_silent": 6400, "a7v_full_scan_silent": 0,
            "a7v_bank_coarse_silent": 6392,
            "k2_verdict": "full scan required for zero-silent; bank-coarse (A5 pattern) fails the SHA-8 constraint",
        },
        "density": {
            "lobes_per_shaft": 80, "shaft_length_mm": 406.4,
            "segments_in_256mm_volume": ">=2",
            "repeatability_budget_mm": 0.1,
            "k4_verdict": "RISK: segment joints + torsion over 406 mm PLA shaft; second independent kill risk (not the binding kill)",
        },
        "verdict": "REJECT A7-V on K1 cost ceiling",
    }


if __name__ == "__main__":
    print(json.dumps(screen(), indent=2))
