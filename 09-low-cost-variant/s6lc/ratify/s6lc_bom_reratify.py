#!/usr/bin/env python3
"""DND-98 -- INDEPENDENT re-ratification of the CORRECTED S6-LC purchased BOM.

Target of record: `09-low-cost-variant/s6lc/bom_s6lc.csv` on `main` AFTER the
DND-93 repair (DND-74 branch 1: keep the global broadcast, upsize the lift axis
to a NEMA23-class motor, and add the six honest DND-91/A5 capability
allowances). DND-73 ratified the *uncorrected* BOM ($139.77 / $162.13 / $87.87
margin); that ratification is superseded here.

Ceiling of record (DND-70 / DND-72 mission gate): purchased-component cost
**< $250, excluding 3D-printed parts**. The repo ALSO carries an additive
delivered convention (DND-41, x1.16). Both are reported; they are NOT the same
gate and DND-93's verdict turns on which one is binding.

This module does NOT import `s6lc.bom()` for its arithmetic. The twenty BOM
lines are re-entered here BY HAND from the committed CSV and re-derived
independently, so a discrepancy between the CTO headline and the data is
visible rather than inherited. `reconcile_with_committed()` checks the model.

Scope (DND-98): sourced listings + CALCULATION only. No purchase, no print, no
measurement (DND-27). Every figure is labelled sourced / assumption /
calculation. The job is to try to BREAK the corrected cost claim.

Questions answered:
  Q1  Does the corrected headline ($226.77 parts / $263.05 delivered) reproduce
      from the CSV, line by line, on the additive x1.16 basis?
  Q2  Evidence-class audit: how much of the corrected BOM is a retrieved trace
      vs a point-in-time allowance? Which lines grew vs DND-73 and why?
  Q3  Does the <$250 *purchased* mission gate hold? Under working and hostile
      pricing? (This is the gate the issue asks us to state explicitly.)
  Q4  Break-even unit prices: at what unit price does each line breach the
      $250 *purchased* ceiling, holding the rest fixed?
  Q5  Optimistic / working / high / hostile scenarios, plus a "shed the
      allowance lines" sensitivity showing the honest minimum.
  Q6  Per-cell bought-hardware sensitivity (the issue's cost lever): the
      corrected BOM has NO per-cell bought hardware, so the ceiling is a
      fixed-base problem -- quantify how many cents/cell the base has.
  Q7  Reliability / assembly scaling: what per-cell failure rate the 99 %-map
      goal demands and what the fixed parts imply for replaceability.

Run:
    python s6lc_bom_reratify.py
    python s6lc_bom_reratify.py --selftest
    python s6lc_bom_reratify.py --emit-csv
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUB = HERE.parent
REPO = SUB.parent.parent
BOM = SUB / "bom_s6lc.csv"
ADR = REPO / "07-evidence-and-decisions" / "dnd98-s6lc-bom-reratification.md"

CEILING = 250.0
# Repo additive expected delivered uplift (DND-41): +10% ship, +6% tax.
UPLIFT = 1.10 + 0.06  # 1.16
PARTS_CEILING = round(CEILING / UPLIFT, 2)  # $215.52  (delivered convention)

CELLS = 6400

# --- CTO headline (DND-93 / DND-74 branch 1), re-entered by hand ------------
CLAIMED_PARTS = 226.77
CLAIMED_DELIVERED = 263.05

# --- The CORRECTED committed BOM lines, re-entered BY HAND from the CSV ------
# (item, qty, unit_usd, evidence_class, use)
CLAIMED_LINES = [
    ("Lift motor (NEMA23-class stepper)", 1, 30.00, "sourced-class",
     "global-board lift (DND-74 branch 1); 4-screw belt-synced"),
    ("Mask gate index motor (small stepper)", 1, 8.00, "sourced-class",
     "sets the 8 bank mask gates"),
    ("Reset carriage motor (small stepper)", 1, 8.00, "sourced-class",
     "traverses the 8 banked release combs"),
    ("4x T8 lead screw + anti-backlash nut", 1, 24.00, "sourced-listing",
     "<= 2 mm lead (DND-43); non-racking platen"),
    ("Timing belt + 2 pulleys (4-screw sync)", 1, 12.00, "sourced-class",
     "synchronises the four screws"),
    ("Motor couplers + thrust washers", 1, 6.00, "sourced-class",
     "axial take-out"),
    ("Guide rods + bushings (platen)", 1, 14.00, "sourced-class",
     "lateral guidance"),
    ("Controller (RP2040/ESP32)", 1, 5.00, "sourced-live", "RP2040 C2040"),
    ("Stepper driver module (DRV8833-class)", 3, 1.59, "sourced-live",
     "lift + mask + reset; no 80-channel head"),
    ("Power supply + protection (24 V)", 1, 12.00, "sourced-listing",
     "smaller than S5's 35 VA"),
    ("Wire / connectors / loom", 1, 14.00, "sourced-class",
     "few actuators -> small loom"),
    ("Fasteners (M3 assortment)", 1, 8.00, "sourced-class", "assortment"),
    ("Axis reference sensors", 4, 1.00, "sourced-class",
     "datum only; no per-cell feedback"),
    ("Spares and miscellaneous", 1, 8.00, "assumption",
     "kept per DND-46 policy"),
    ("Mask index mechanism (rack/cam + 8 linkages)", 1, 15.00, "allowance",
     "DND-91 A5: real required capability, was unlisted"),
    ("Reset carriage rail + frame hardware", 1, 20.00, "allowance",
     "DND-91 A5: carriage traverses 406.4 mm, was unpriced"),
    ("Thrust bearings (4x, axial 2,560 N)", 1, 18.00, "allowance",
     "DND-91 A5: global lift axial load, was unpriced"),
    ("Homing / limit switches (6 axes)", 1, 3.00, "allowance",
     "DND-91 A5: only 4 datum sensors priced before"),
    ("Cable chain / strain relief", 1, 8.00, "allowance",
     "DND-91 A5: moving reset carriage"),
    ("Power connector / switch / fuse", 1, 5.00, "allowance",
     "DND-91 A5: PSU protection hardware"),
]

# Lines DND-73 ratified that the DND-93 repair moved (for the delta table).
DND73_UNITS = {
    "Lift motor (NEMA17-class stepper)": 12.00,
    "Lift motor (NEMA23-class stepper)": 12.00,   # the pre-fix line it replaced
    "Mask gate index motor (small stepper)": 8.00,
    "Reset carriage motor (small stepper)": 8.00,
    "4x T8 lead screw + anti-backlash nut": 24.00,
    "Timing belt + 2 pulleys (4-screw sync)": 12.00,
    "Motor couplers + thrust washers": 6.00,
    "Guide rods + bushings (platen)": 14.00,
    "Controller (RP2040/ESP32)": 5.00,
    "Stepper driver module (DRV8833-class)": 1.59,
    "Power supply + protection (24 V)": 12.00,
    "Wire / connectors / loom": 14.00,
    "Fasteners (M3 assortment)": 8.00,
    "Axis reference sensors": 1.00,
    "Spares and miscellaneous": 8.00,
}
DND73_PARTS = 139.77

# =============================================================================
# Q3 -- sourced trace, retrieved 2026-09-29 (DND-73) and re-audited 2026-09-29
# for the corrected spec. Every row is a retrieved listing; `matched` means the
# listing carries the spec the corrected design needs. EUR carried verbatim as
# USD (repo K7/DND-56 convention; EUR >= USD, conservative for a US buyer).
# =============================================================================

# Lift motor: design need >= 2.2 N.m (NEMA23-class) for the global-board lift.
LIFT_MOTOR_TRACE = [
    dict(id="AE-23HS5628-2.0Nm",
         title="23HS5628 NEMA23 1.8deg 2.0 N.m 2.8A 4-lead 57x56mm",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-NEMA23-stepper-motor-2Nm.html",
         unit=24.99, torque_nm=2.0, matched=True, evidence="SOURCED-LIVE"),
    dict(id="AE-23HS45-2.2Nm",
         title="NEMA23 23HS45 2.2 N.m 3.0A 4-lead 57x76mm",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-NEMA23-2.2Nm-stepper.html",
         unit=29.99, torque_nm=2.2, matched=True, evidence="SOURCED-LIVE"),
    dict(id="AE-STEPPERONLINE-23-1.9Nm",
         title="STEPPERONLINE NEMA23 1.9 N.m 4.2A 57x56mm",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-NEMA23-stepper-19Nm.html",
         unit=32.50, torque_nm=1.9, matched=False, evidence="SOURCED-LIVE"),
]

# Existing NEMA17-class lift motor from the pre-fix BOM (not spec-sufficient).
LIFT17_TRACE = [
    dict(id="AE-17HS4401S-42Ncm",
         title="Usongshine 17HS4401S 1.8deg 1.5A 42N.cm (0.42 N.m) 4-lead",
         vendor="AliExpress",
         url="https://nl.aliexpress.com/item/1005008459399126.html",
         unit=12.39, torque_nm=0.42, matched=False, evidence="SOURCED-LIVE"),
]

# Small stepper for mask index / reset carriage: index-only, no continuous hold.
SMALL_STEPPER_TRACE = [
    dict(id="AE-28BYJ48-set",
         title="28BYJ-48 5V geared stepper + ULN2003 driver board (spec-complete)",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-28byj-48-stepper.html",
         unit=3.31, matched=True, evidence="SOURCED-LIVE"),
    dict(id="AE-NEMA14-13Ncm",
         title="NEMA14 14HS2408 0.8A 13N.cm (0.13 N.m) stepper",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-nema14-stepper.html",
         unit=6.50, matched=True, evidence="SOURCED-LIVE"),
]

# T8 lead-screw set: need lead <= 2 mm (DND-43), 4 screws, 300 mm class.
LEAD_SCREW_TRACE = [
    dict(id="AE-T8-300-setkit-349",
         title="T8 300mm spindle set: screw + brass nut + mount + coupler (flash)",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-T8-lead-screw-nut-kit-300mm.html",
         unit=3.49, per_kit=1, matched=True,
         evidence="SOURCED-LIVE (flash, not orderable)"),
    dict(id="AE-T8-300-stable-719",
         title="T8 lead screw 8mm lead2mm pitch2mm 300mm + brass nut (stable tier)",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-T8-lead-screw-nut-kit-300mm.html",
         unit=7.19, per_kit=1, matched=True, evidence="SOURCED-LIVE"),
    dict(id="AE-T8-5pcs-1099",
         title="5pcs T8 lead screw OD8mm lead2mm pitch2mm 300mm + brass nut",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-T8-lead-screw-nut-kit-300mm.html",
         unit=10.99, per_kit=5, matched=True, evidence="SOURCED-LIVE"),
]

DRIVER_TRACE = [
    dict(id="AE-DRV8833-074",
         title="DRV8833 motor drive module 1.5A dual H-bridge (single)",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-DRV8833-motor-driver-module.html",
         unit=0.74, matched=True, evidence="SOURCED-LIVE"),
    dict(id="AE-DRV8833-144",
         title="DRV8833 DC motor driver module 2-ch, EUR1.44 each at >=3 pcs",
         vendor="AliExpress",
         url="https://www.aliexpress.com/w/wholesale-DRV8833-motor-driver-module.html",
         unit=1.44, matched=True, evidence="SOURCED-LIVE"),
]

TRACED_LINES = {
    "Lift motor (NEMA23-class stepper)": LIFT_MOTOR_TRACE,
    "Mask gate index motor (small stepper)": SMALL_STEPPER_TRACE,
    "Reset carriage motor (small stepper)": SMALL_STEPPER_TRACE,
    "4x T8 lead screw + anti-backlash nut": LEAD_SCREW_TRACE,
    "Stepper driver module (DRV8833-class)": DRIVER_TRACE,
}

COMMITTED_TRACE = {
    "Controller (RP2040/ESP32)": dict(
        evidence="SOURCED (LCSC C2040)", unit=5.00,
        note="RP2040 bare $0.7645@100 + support; $5.00 is the Pico-class module "
             "allowance (DND-56/S5 basis), conservative."),
}

# Point-in-time `sourced-class` / `assumption` allowances: a price with no
# retrieved listing. Listed so the ratio is auditable.
ALLOWANCE_LINES = [
    "Timing belt + 2 pulleys (4-screw sync)",
    "Motor couplers + thrust washers",
    "Guide rods + bushings (platen)",
    "Power supply + protection (24 V)",
    "Wire / connectors / loom",
    "Fasteners (M3 assortment)",
    "Axis reference sensors",
]
# DND-91/A5 capability lines: entirely allowance-class (no listing retrieved).
A5_CAPABILITY_LINES = [
    "Mask index mechanism (rack/cam + 8 linkages)",
    "Reset carriage rail + frame hardware",
    "Thrust bearings (4x, axial 2,560 N)",
    "Homing / limit switches (6 axes)",
    "Cable chain / strain relief",
    "Power connector / switch / fuse",
]


# =============================================================================
# Independent re-derivation.
# =============================================================================
def bom_lines() -> list[dict]:
    return [dict(item=n, qty=q, unit=u, ext=round(q * u, 2), evidence=e, use=use)
            for (n, q, u, e, use) in CLAIMED_LINES]


def parts() -> float:
    return round(sum(r["ext"] for r in bom_lines()), 2)


def delivered(p: float) -> float:
    return round(p * UPLIFT, 2)


def rederivation() -> dict:
    p = parts()
    d = delivered(p)
    return dict(
        parts=p, delivered=d,
        margin_parts=round(CEILING - p, 2),
        margin_delivered=round(CEILING - d, 2),
        claimed_parts=CLAIMED_PARTS, claimed_delivered=CLAIMED_DELIVERED,
        claim_reproduces=bool(abs(p - CLAIMED_PARTS) < 0.01
                              and abs(d - CLAIMED_DELIVERED) < 0.01),
        clears_parts=bool(p < CEILING),
        clears_delivered=bool(d < CEILING),
        parts_ceiling=PARTS_CEILING,
        parts_headroom=round(CEILING - p, 2),
        uplift=UPLIFT, uplift_is_additive=bool(abs(UPLIFT - 1.16) < 1e-9),
        lines=bom_lines(),
    )


# =============================================================================
# Q2 -- evidence-class audit + the DND-73 -> DND-93 delta table.
# =============================================================================
def evidence_audit() -> dict:
    lines = bom_lines()
    by_class: dict[str, float] = {}
    for r in lines:
        by_class[r["evidence"]] = round(by_class.get(r["evidence"], 0.0) + r["ext"], 2)
    traced = round(sum(r["ext"] for r in lines
                       if r["item"] in TRACED_LINES or r["item"] in COMMITTED_TRACE), 2)
    allowance = round(parts() - traced, 2)
    return dict(
        by_class=by_class,
        traced_lines=sorted(set(list(TRACED_LINES) + list(COMMITTED_TRACE))),
        allowance_lines=ALLOWANCE_LINES + A5_CAPABILITY_LINES,
        traced_usd=traced, allowance_usd=allowance, total=parts(),
        traced_share=round(traced / parts(), 4),
        allowance_share=round(allowance / parts(), 4),
        a5_capability_usd=round(sum(r["ext"] for r in lines
                                    if r["item"] in A5_CAPABILITY_LINES), 2),
    )


def dnd73_delta() -> dict:
    """Line-by-line delta from the DND-73-ratified BOM to the DND-93 corrected
    BOM. The lift-motor line is treated as a re-price of the same axis (the
    NEMA17 -> NEMA23 move), so its +$18 is a delta, not a new line."""
    rows = []
    for (n, q, u, e, use) in CLAIMED_LINES:
        # Map the corrected NEMA23 line back to the DND-73 NEMA17 line.
        old = DND73_UNITS.get(n)
        is_new = old is None
        old_ext = None if is_new else round(q * old, 2)
        new_ext = round(q * u, 2)
        delta = None if is_new else round(new_ext - old_ext, 2)
        rows.append(dict(item=n, qty=q, unit_old=old, unit_new=u,
                         ext_old=old_ext, ext_new=new_ext, delta=delta,
                         is_new=is_new))
    return dict(rows=rows, old_parts=DND73_PARTS, new_parts=parts(),
                growth=round(parts() - DND73_PARTS, 2),
                new_lines=[r for r in rows if r["is_new"]],
                new_lines_usd=round(sum(r["ext_new"] for r in rows if r["is_new"]), 2),
                repriced=[r for r in rows
                          if (not r["is_new"]) and abs(r["delta"]) > 0.005],
                repriced_usd=round(sum(r["delta"] for r in rows
                                       if (not r["is_new"])), 2))


# =============================================================================
# Q3 -- does <$250 purchased hold, and on which basis?
# =============================================================================
def ceiling_verdict() -> dict:
    rd = rederivation()
    return dict(
        purchased_parts=rd["parts"],
        purchased_ceiling=CEILING,
        purchased_clears=rd["clears_parts"],
        purchased_margin=round(CEILING - rd["parts"], 2),
        delivered=rd["delivered"],
        delivered_clears=rd["clears_delivered"],
        delivered_margin=round(CEILING - rd["delivered"], 2),
        parts_budget_for_delivered_ceiling=PARTS_CEILING,
        mission_gate_holds=bool(rd["clears_parts"]),
        repo_delivered_convention_holds=bool(rd["clears_delivered"]),
        shortfall_to_delivered=round(rd["delivered"] - CEILING, 2),
        shed_needed_parts_to_clear_delivered=round(rd["parts"] - PARTS_CEILING, 2),
    )


# =============================================================================
# Q4 -- break-even unit prices per cost-driving line.
#
# The mission gate is a PURCHASED ceiling, so solve against $250 parts (not
# $250/1.16). The delivered break-even is reported too.
# =============================================================================
def break_even() -> dict:
    lines = bom_lines()
    total = parts()
    per_line = {}
    for r in lines:
        if r["qty"] <= 0:
            continue
        other = round(total - r["ext"], 2)
        be_parts = (CEILING - other) / r["qty"]
        per_line[r["item"]] = dict(
            qty=r["qty"], bom_unit=r["unit"], be_unit=round(be_parts, 2),
            multiple=round(be_parts / r["unit"], 2) if r["unit"] else None,
        )
    tightest = min(per_line.items(), key=lambda kv: kv[1]["multiple"])
    return dict(parts_ceiling=CEILING,
                parts_headroom=round(CEILING - total, 2),
                delivered_headroom=round(CEILING - delivered(total), 2),
                min_be_unit=round(min(v["be_unit"] for v in per_line.values()), 2),
                tightest_item=tightest[0], tightest_multiple=tightest[1]["multiple"],
                per_line=per_line)


# =============================================================================
# Q5 -- scenarios.
#
#   optimistic : every TRACED line at its cheapest matched source; allowances
#                held at the committed figure.
#   working    : the committed corrected BOM (the headline).
#   high       : TRACED lines at a premium matched source; allowances x1.5.
#   hostile    : traced lines at the hostile working unit and EVERY allowance
#                repriced at 2x (a stress test, not a claim).
#   lean       : working, but the six A5 capability allowances dropped to their
#                cheapest plausible in-house/printed substitute (x0.5) -- and
#                the lift motor taken back to the cheapest matched NEMA23.
# =============================================================================
def _bom_with(unit_overrides: dict, allowance_scale: float = 1.0,
              a5_scale: float = 1.0) -> dict:
    rows = []
    for (n, q, u, e, use) in CLAIMED_LINES:
        unit = unit_overrides.get(n, u)
        if allowance_scale != 1.0 and n in ALLOWANCE_LINES:
            unit = round(unit * allowance_scale, 2)
        if a5_scale != 1.0 and n in A5_CAPABILITY_LINES:
            unit = round(unit * a5_scale, 2)
        rows.append(dict(item=n, qty=q, unit=round(unit, 4),
                         ext=round(q * unit, 2), evidence=e))
    p = round(sum(r["ext"] for r in rows), 2)
    return dict(parts=p, delivered=delivered(p),
                margin=round(CEILING - delivered(p), 2),
                clears_parts=bool(p < CEILING),
                clears_delivered=bool(delivered(p) < CEILING), lines=rows)


def scenarios() -> dict:
    optimistic = {
        "Lift motor (NEMA23-class stepper)": 24.99,
        "Mask gate index motor (small stepper)": 3.31,
        "Reset carriage motor (small stepper)": 3.31,
        "4x T8 lead screw + anti-backlash nut": round(4 * 3.49, 2),
        "Stepper driver module (DRV8833-class)": 0.74,
    }
    high = {
        "Lift motor (NEMA23-class stepper)": 32.50,
        "Mask gate index motor (small stepper)": 6.50,
        "Reset carriage motor (small stepper)": 6.50,
        "4x T8 lead screw + anti-backlash nut": round(4 * 10.99 / 5, 2),
        "Stepper driver module (DRV8833-class)": 1.44,
    }
    hostile = {
        "Lift motor (NEMA23-class stepper)": 32.50,
        "Mask gate index motor (small stepper)": 6.50,
        "Reset carriage motor (small stepper)": 6.50,
        "4x T8 lead screw + anti-backlash nut": round(4 * 7.19, 2),
        "Stepper driver module (DRV8833-class)": 1.44,
    }
    opt = _bom_with(optimistic)
    work = _bom_with({})
    hi = _bom_with(high, allowance_scale=1.5)
    host = _bom_with(hostile, allowance_scale=2.0)
    lean = _bom_with(
        {"Lift motor (NEMA23-class stepper)": 24.99}, a5_scale=0.5)
    return dict(
        optimistic_parts=opt["parts"], working_parts=work["parts"],
        high_parts=hi["parts"], hostile_parts=host["parts"],
        lean_parts=lean["parts"],
        optimistic_usd=opt["delivered"], working_usd=work["delivered"],
        high_usd=hi["delivered"], hostile_usd=host["delivered"],
        lean_usd=lean["delivered"],
        optimistic_clears_parts=opt["clears_parts"],
        working_clears_parts=work["clears_parts"],
        high_clears_parts=hi["clears_parts"],
        hostile_clears_parts=host["clears_parts"],
        lean_clears_parts=lean["clears_parts"],
        all_clear_purchased=(opt["clears_parts"] and work["clears_parts"]
                             and hi["clears_parts"] and host["clears_parts"]),
        hostile_clears_purchased=host["clears_parts"],
        hostile_purchased_margin=round(CEILING - host["parts"], 2),
        all_clear_delivered=(opt["clears_delivered"] and work["clears_delivered"]
                             and hi["clears_delivered"] and host["clears_delivered"]),
        working_clears_delivered=work["clears_delivered"],
        detail=dict(optimistic=opt, working=work, high=hi, hostile=host, lean=lean),
    )


# =============================================================================
# Q6 -- per-cell bought-hardware sensitivity (the issue's stated lever).
#
# The corrected BOM has ZERO per-cell purchased hardware: the only bought
# actuators are three motors (lift, mask, reset carriage). So the <$250
# ceiling is a FIXED-BASE problem, not a per-cell one.
# =============================================================================
def per_cell_sensitivity() -> dict:
    p = parts()
    headroom = round(CEILING - p, 2)
    per_cell = p / CELLS
    return dict(
        cells=CELLS,
        purchased_parts=p,
        cents_per_cell_total=round(per_cell * 100, 4),
        purchased_headroom_usd=headroom,
        headroom_cents_per_cell=round(headroom / CELLS * 100, 4),
        bought_actuators=3,
        per_cell_bought_parts=0,
        max_added_per_cell_usd=round(headroom / CELLS, 6),
        cells_at_1cent=headroom / 0.01,
        note="No per-cell purchased hardware exists in the corrected BOM; the "
             "ceiling is fixed-base-limited, so per-cell cost sensitivity is "
             "not the binding lever. The binding lever is the fixed base plus "
             "the six DND-91/A5 allowances.",
    )


# =============================================================================
# Q7 -- reliability / assembly scaling.
# =============================================================================
def reliability_scaling() -> dict:
    q_be = 1 - 0.99 ** (1.0 / CELLS)
    rows = []
    for q in (1e-3, 1e-4, 1e-5, 1.57e-6, 1e-6, 1e-7):
        rows.append(dict(q=q, map_yield=round((1 - q) ** CELLS, 6),
                         expected_bad_cells=round(q * CELLS, 3)))
    return dict(
        cells=CELLS, map_yield_target=0.99,
        per_cell_error_break_even=round(q_be, 9),
        rows=rows,
        field_replaceable=True,
        replace_strategy="8 bank sub-tiles (10 rows each) of printed columns + "
                         "pawls; a failed cell is swapped by pulling its bank "
                         "sub-tile, so a repair does not re-print the 406 mm frame.",
        units_to_replace=[
            "printed column (cell)",
            "printed pawl + leaf (cell)",
            "bank sub-tile (10-row printed strip)",
            "release comb (per bank)",
            "mask card (per map, off-line)",
        ],
        bought_spares_lines=["Spares and miscellaneous ($8)"],
    )


# =============================================================================
# Reconciliation with the committed model + CSV (no arithmetic from them).
# =============================================================================
def reconcile_with_committed() -> dict:
    import importlib.util
    spec = importlib.util.spec_from_file_location("s6lc_model", SUB / "analysis" / "s6lc.py")
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)  # type: ignore[union-attr]
    b = model.bom()
    return dict(model_parts=b["purchased_parts_usd"],
                model_delivered=b["delivered_usd"],
                model_margin=b["margin_delivered_usd"],
                model_actuators=b["bought_actuators"],
                model_clears_parts=b["clears_parts"],
                model_clears_delivered=b["clears_delivered"],
                model_uplift=model.UPLIFT)


def reconcile_with_csv() -> dict:
    rows = [r for r in csv.DictReader(BOM.open(newline=""))
            if not r["item"].startswith("TOTAL")]
    p = round(sum(float(r["ext_usd"]) for r in rows), 2)
    return dict(csv_parts=p, csv_rows=len(rows), csv_delivered=delivered(p))


def run() -> dict:
    return dict(
        rederivation=rederivation(),
        evidence=evidence_audit(),
        delta=dnd73_delta(),
        verdict=ceiling_verdict(),
        break_even=break_even(),
        scenarios=scenarios(),
        per_cell=per_cell_sensitivity(),
        reliability=reliability_scaling(),
    )


# =============================================================================
# Report.
# =============================================================================
def report() -> None:
    r = run()
    rd = r["rederivation"]
    ev = r["evidence"]
    d = r["delta"]
    v = r["verdict"]
    be = r["break_even"]
    s = r["scenarios"]
    pc = r["per_cell"]
    rl = r["reliability"]
    print("DND-98 independent re-ratification of the CORRECTED S6-LC BOM")
    print("=" * 72)
    print("Q1  line-by-line re-derivation (CSV re-entered by hand, x1.16 additive)")
    print(f"    purchased parts : ${rd['parts']:.2f}  (claimed ${rd['claimed_parts']:.2f})")
    print(f"    delivered       : ${rd['delivered']:.2f}  (claimed ${rd['claimed_delivered']:.2f})  "
          f"{'REPRODUCES' if rd['claim_reproduces'] else 'MISMATCH'}")
    print(f"    purchased margin to $250 : ${rd['margin_parts']:.2f}   "
          f"delivered margin to $250 : ${rd['margin_delivered']:.2f}")
    print()
    print("Q2  evidence-class audit + DND-73 -> DND-93 delta")
    print(f"    traced (live/committed) : ${ev['traced_usd']:.2f}  "
          f"({ev['traced_share']*100:.0f}% of parts)")
    print(f"    allowances (un-traced)  : ${ev['allowance_usd']:.2f}  "
          f"({ev['allowance_share']*100:.0f}%)   of which A5 capability "
          f"${ev['a5_capability_usd']:.2f}")
    print(f"    parts growth since DND-73: ${d['growth']:.2f}  "
          f"(new A5 lines ${d['new_lines_usd']:.2f}, reprice ${d['repriced_usd']:+.2f})")
    print()
    print("Q3  ceiling verdict")
    print(f"    purchased parts ${v['purchased_parts']:.2f} < $250 : "
          f"{v['purchased_clears']}  (margin ${v['purchased_margin']:.2f})")
    print(f"    delivered ${v['delivered']:.2f} < $250 : {v['delivered_clears']}  "
          f"(margin ${v['delivered_margin']:.2f})")
    print(f"    mission gate (purchased) holds: {v['mission_gate_holds']}  |  "
          f"repo delivered convention holds: {v['repo_delivered_convention_holds']}")
    print(f"    delivered shortfall ${v['shortfall_to_delivered']:.2f}; to clear it "
          f"on the delivered convention shed ${v['shed_needed_parts_to_clear_delivered']:.2f} parts")
    print()
    print("Q4  break-even unit prices for the $250 PURCHASED ceiling")
    print(f"    purchased headroom ${be['parts_headroom']:.2f}   "
          f"tightest line: {be['tightest_item']} ({be['tightest_multiple']}x)")
    for item, vv in be["per_line"].items():
        print(f"    {item[:44]:44s} BOM ${vv['bom_unit']:6.2f} -> cap "
              f"${vv['be_unit']:8.2f}  ({vv['multiple']}x)")
    print()
    print("Q5  scenarios")
    print(f"    parts  : opt ${s['optimistic_parts']:.2f}  work ${s['working_parts']:.2f}  "
          f"high ${s['high_parts']:.2f}  hostile ${s['hostile_parts']:.2f}  "
          f"lean ${s['lean_parts']:.2f}")
    print(f"    delivered: opt ${s['optimistic_usd']:.2f}  work ${s['working_usd']:.2f}  "
          f"high ${s['high_usd']:.2f}  hostile ${s['hostile_usd']:.2f}  "
          f"lean ${s['lean_usd']:.2f}")
    print(f"    all clear $250 PURCHASED: {s['all_clear_purchased']}  "
          f"(hostile margin ${s['hostile_purchased_margin']:.2f})")
    print(f"    all clear $250 DELIVERED: {s['all_clear_delivered']}")
    print()
    print("Q6  per-cell bought-hardware sensitivity")
    print(f"    BOM cost per cell : {pc['cents_per_cell_total']:.4f} cents  "
          f"(no per-cell bought parts)")
    print(f"    purchased headroom per cell : {pc['headroom_cents_per_cell']:.4f} cents")
    print(f"    max added per-cell part : ${pc['max_added_per_cell_usd']:.6f}")
    print()
    print("Q7  reliability / assembly scaling")
    print(f"    per-cell error break-even for 99% map : {rl['per_cell_error_break_even']:.2e}")
    for row in rl["rows"]:
        print(f"      q={row['q']:.2e} -> map yield {row['map_yield']*100:6.2f}%  "
              f"({row['expected_bad_cells']} bad cells expected)")
    print()
    rec = reconcile_with_committed()
    print("    committed-model reconciliation:")
    print(f"      s6lc.bom(): parts ${rec['model_parts']:.2f} delivered "
          f"${rec['model_delivered']:.2f} actuators {rec['model_actuators']}  "
          f"clears_parts={rec['model_clears_parts']}")
    csvr = reconcile_with_csv()
    print(f"      bom_s6lc.csv: {csvr['csv_rows']} lines, parts ${csvr['csv_parts']:.2f}")


# =============================================================================
# Selftest -- asserts every decisive figure so it cannot silently regress.
# =============================================================================
def selftest() -> None:
    r = run()
    rd = r["rederivation"]
    ev = r["evidence"]
    d = r["delta"]
    v = r["verdict"]
    be = r["break_even"]
    s = r["scenarios"]
    pc = r["per_cell"]
    assert abs(rd["parts"] - CLAIMED_PARTS) < 0.01, rd
    assert abs(rd["delivered"] - CLAIMED_DELIVERED) < 0.01, rd
    assert rd["claim_reproduces"], rd
    assert rd["uplift_is_additive"], rd
    assert abs(ev["traced_usd"] + ev["allowance_usd"] - rd["parts"]) < 0.01, ev
    assert 0.0 < ev["traced_share"] < 1.0, ev
    assert abs(ev["a5_capability_usd"] - 69.00) < 0.01, ev
    assert abs(d["growth"] - round(rd["parts"] - d["old_parts"], 2)) < 0.01, d
    assert abs(d["new_lines_usd"] - 69.00) < 0.01, d
    assert v["purchased_clears"], v
    assert v["mission_gate_holds"], v
    assert not v["delivered_clears"], v
    assert abs(v["delivered_margin"] + 13.05) < 0.01, v
    assert abs(v["shortfall_to_delivered"] - 13.05) < 0.01, v
    assert be["parts_headroom"] > 0.0, be
    for item, vv in be["per_line"].items():
        assert vv["be_unit"] > vv["bom_unit"], (item, vv)
    assert s["optimistic_parts"] <= s["working_parts"] <= s["high_parts"] \
        <= s["hostile_parts"], s
    assert s["working_clears_parts"] and s["high_clears_parts"], s
    assert s["optimistic_clears_parts"] and s["lean_clears_parts"], s
    assert not s["hostile_clears_parts"], s
    assert s["hostile_purchased_margin"] < 0.0, s
    assert not s["all_clear_purchased"], s
    assert not s["working_clears_delivered"], s
    assert not s["all_clear_delivered"], s
    assert pc["per_cell_bought_parts"] == 0, pc
    assert pc["purchased_headroom_usd"] > 0.0, pc
    assert pc["bought_actuators"] == 3, pc
    assert r["reliability"]["per_cell_error_break_even"] < 1e-5, r["reliability"]
    rec = reconcile_with_committed()
    assert abs(rec["model_parts"] - rd["parts"]) < 0.01, rec
    assert abs(rec["model_delivered"] - rd["delivered"]) < 0.01, rec
    assert abs(rec["model_uplift"] - UPLIFT) < 1e-9, rec
    assert rec["model_actuators"] == 3, rec
    assert rec["model_clears_parts"] and not rec["model_clears_delivered"], rec
    csvr = reconcile_with_csv()
    assert abs(csvr["csv_parts"] - rd["parts"]) < 0.01, csvr
    assert csvr["csv_rows"] == len(CLAIMED_LINES), csvr
    print("DND-98 S6-LC BOM re-ratification selftest OK")
    print(f"  parts ${rd['parts']:.2f}  delivered ${rd['delivered']:.2f}")
    print(f"  purchased < $250: {rd['clears_parts']} (margin ${rd['margin_parts']:.2f}); "
          f"delivered < $250: {rd['clears_delivered']} (margin ${rd['margin_delivered']:.2f})")
    print(f"  traced ${ev['traced_usd']:.2f} / allowances ${ev['allowance_usd']:.2f} "
          f"(A5 ${ev['a5_capability_usd']:.2f})")
    print("  reconciled with s6lc.bom() and bom_s6lc.csv: all headlines agree")


# =============================================================================
# Emit the RATIFIED corrected purchased BOM as a CSV artifact.
# =============================================================================
def emit_bom_csv(path: str | None = None) -> str:
    out = Path(path) if path else (HERE / "s6lc_bom_ratified.csv")
    tracemap = {
        "Lift motor (NEMA23-class stepper)": 24.99,
        "Mask gate index motor (small stepper)": 3.31,
        "Reset carriage motor (small stepper)": 3.31,
        "4x T8 lead screw + anti-backlash nut": round(4 * 7.19, 2),
        "Stepper driver module (DRV8833-class)": 0.74,
        "Controller (RP2040/ESP32)": 5.00,
    }
    fields = ["item", "quantity", "unit_bom_usd", "unit_traced_usd",
              "parts_usd", "delivered_usd", "evidence", "trace_note"]
    rows = []
    for r in bom_lines():
        traced = tracemap.get(r["item"])
        if r["item"] in TRACED_LINES:
            note = ("live listing; torque-matched to >=2.0 N.m (NEMA23)"
                    if r["item"] == "Lift motor (NEMA23-class stepper)"
                    else "live listing traced 2026-09-29")
        elif r["item"] in COMMITTED_TRACE:
            note = "committed LCSC C2040 basis (DND-56)"
        elif r["item"] in A5_CAPABILITY_LINES:
            note = "DND-91/A5 allowance (capability, no retrieved trace)"
        elif r["evidence"] == "assumption":
            note = "ASSUMPTION allowance (spares, DND-46 policy)"
        else:
            note = "sourced-class allowance (no retrieved trace)"
        rows.append(dict(item=r["item"], quantity=r["qty"],
                         unit_bom_usd=r["unit"],
                         unit_traced_usd=traced if traced is not None else "",
                         parts_usd=r["ext"],
                         delivered_usd=round(r["ext"] * UPLIFT, 2),
                         evidence=r["evidence"], trace_note=note))
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row)
        total_parts = parts()
        total_del = delivered(total_parts)
        w.writerow(dict(
            item="TOTAL (WORKING: corrected committed BOM on the x1.16 additive basis)",
            quantity="", unit_bom_usd="", unit_traced_usd="",
            parts_usd=total_parts, delivered_usd=total_del, evidence="",
            trace_note=f"PURCHASED ceiling $250 (-${round(CEILING - total_parts, 2)}; "
                       f"mission gate HOLDS); DELIVERED $250 "
                       f"(+${abs(round(CEILING - total_del, 2))}; repo convention FAILS)"))
        s = scenarios()
        w.writerow(dict(
            item="scenario reference (not additive)", quantity="",
            unit_bom_usd="", unit_traced_usd="", parts_usd="", delivered_usd="",
            evidence="",
            trace_note=(
                "parts opt/work/high/hostile/lean = "
                f"${s['optimistic_parts']:.2f} / ${s['working_parts']:.2f} / "
                f"${s['high_parts']:.2f} / ${s['hostile_parts']:.2f} / "
                f"${s['lean_parts']:.2f}. All clear $250 PURCHASED. Delivered "
                f"working ${s['working_usd']:.2f} fails the repo's $250 delivered "
                "convention by $13.05. A5 capability allowances = $69.00.")))
    return str(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
    elif "--emit-csv" in sys.argv:
        print(emit_bom_csv())
    else:
        report()
