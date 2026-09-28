#!/usr/bin/env python3
"""Test11 J2 -- analytic/simulation gate replacing the J2 physical isolation rig.

Policy: board directive DND-27 "No physical print tests will be performed".
The J2 protocol (isolation_rig_protocol.md) measures how much a target-tile
reset disturbs a loaded, untouched neighbour tile. That physical measurement is
no longer available, so this module replaces it with the strongest *analytic*
proxies that can still reject the isolation claim:

  B1. Kinematic / force analysis at the intended load. The neighbour is coupled
      to the target only through (i) the shared rigid base rail and (ii) the
      seam. We compute, with explicit units and assumptions:
        * the neighbour vertical/lateral motion induced by the target stroke
          through a clamped-beam rail model (a *bound*, not a measurement);
        * the stiction/friction force that must be exceeded before a loaded
          neighbour column can creep, and the isolation ratio that follows.
  B2. Fixture fit stack-up: holder outer size, seam, X1C bed fit and the
      interchangeable-fixture socket, worst-case and Monte Carlo. Mesh
      validation of the SCAD fixture (OpenSCAD render if installable, else
      stdlib STL parse).
  B3. An explicit statement of which protocol claims now rest on analysis and
      which would still require measurement, and an *analytic run record* row
      set in the exact `measurements/isolation.csv` schema the CI-tested gate
      engine `isolation_rig_runner.py` consumes, with an `evidence` column that
      is never `MEASURED`.

Evidence labels (DND-27): sourced fact, assumption, calculation, simulation,
CAD. This module emits only analytic classes. It is NOT a print and NOT a
measurement.

Usage:
    python j2_analytic_gate.py --report
    python j2_analytic_gate.py --emit-record
    python j2_analytic_gate.py --selftest
    python j2_analytic_gate.py --json

Exit codes: 0 = analysis ran; 1 = analytic KILL (a bound exceeds a fail gate);
2 = usage error.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL_MAP_SECONDS = 26.251  # modelled full-map time; test09/test11

# ---------------------------------------------------------------------------
# Sourced / assumed inputs. Every number carries its class.
# ---------------------------------------------------------------------------
# Column mass: Test09 analyse.py solid 2.069 g, hollow 0.997 g (CALCULATED).
COLUMN_MASS_G = 2.069
COLUMN_MASS_HOLLOW_G = 0.997
DRAG_MN_PER_CELL = 5.0        # Test09 lower drag assumption
DRAG_MN_PER_CELL_HI = 10.0    # Test09 mid drag assumption

# Cell geometry
PITCH_MM = 5.08

# J2 fixture / protocol constants
TILE_SIZES = (5, 10, 20)
BORDER_MM = 6.0
SEAM_NOMINAL_MM = 0.40
BED_MM = 256.0
HOLDER_WALL_MIN_MM = 2.0
RAIL_THICKNESS_MM = 12.0

# Material: printed PLA (isotropic approximation; FDM is anisotropic -- an
# explicitly stated limitation).
PLA_E_MPA = 2500.0            # Test09 material modulus upper bound
PLA_DENSITY_G_CM3 = 1.24

# Gates (from isolation_rig_protocol.md / measurement_plan.md)
GATE_PEAK_MM = 0.10
FAIL_PEAK_MM = 0.25
GATE_MINI_MOVE_MM = 0.50
GATE_SEAM_MM = 0.25
GATE_DRIFT_MM = 0.20

# Static friction coefficient (assumption): PLA-on-PLA printed surfaces.
MU_STATIC = 0.35              # assumption, dry PLA-PLA; range 0.2-0.5
NEIGHBOUR_LOAD_N = 1.0        # protocol J2-2 seam load + miniature+20 g ~ 1 N


@dataclass(frozen=True)
class Input:
    key: str
    value: float
    units: str
    kind: str
    source: str


INPUTS = [
    Input("column_mass_solid", COLUMN_MASS_G, "g", "calculation",
          "Test09 analyse.py solid column mass."),
    Input("column_mass_hollow", COLUMN_MASS_HOLLOW_G, "g", "calculation",
          "Test09 analyse.py hollow column mass."),
    Input("drag_per_cell", DRAG_MN_PER_CELL, "mN", "assumption",
          "Test09 lower-bound drag per cell; the model output, not measured."),
    Input("pla_modulus", PLA_E_MPA, "MPa", "assumption",
          "Test09 material modulus upper bound; FDM is anisotropic."),
    Input("mu_static_pla", MU_STATIC, "-", "assumption",
          "Dry PLA-on-PLA static friction; textbook 0.2-0.5, midpoint 0.35."),
]


# ---------------------------------------------------------------------------
# B1a. Structural coupling through the shared rail (clamped beam bound).
# ---------------------------------------------------------------------------
def rail_coupling(
    tile: int,
    actuator_force_n: float,
    rail_thickness_mm: float = RAIL_THICKNESS_MM,
    rail_width_mm: float = 40.0,
    span_mm: float | None = None,
    e_mpa: float = PLA_E_MPA,
) -> dict:
    """Vertical deflection the target stroke puts into the neighbour rail point.

    Model (stated assumptions):
      * The rail is a clamped-clamped beam of rectangular section, span L, that
        carries the two holders. Length along the rail is set so both holders
        fit: L = 2*holder_outer + seam.
      * The actuator applies a vertical force F at the target holder centre.
      * The neighbour is at the far holder centre.
    The induced neighbour deflection is bounded by the simply-supported
    point-load deflection at the load point, which is *larger* than the
    clamped case -- deliberately conservative.

    Returned values are a CALCULATION/BOUND, not a measurement.
    """
    if span_mm is None:
        span_mm = 2 * (tile * PITCH_MM + 2 * BORDER_MM) + SEAM_NOMINAL_MM
    L = span_mm
    b = rail_width_mm
    h = rail_thickness_mm
    I = b * h ** 3 / 12.0                     # mm^4
    E = e_mpa                                # N/mm^2
    # Simply-supported centre point load: delta = F L^3 / (48 E I).
    delta_ss = actuator_force_n * L ** 3 / (48.0 * E * I)  # mm
    # Clamped-clamped centre point load: delta = F L^3 / (192 E I).
    delta_cc = actuator_force_n * L ** 3 / (192.0 * E * I)
    return {
        "tile": tile,
        "span_mm": round(L, 2),
        "actuator_force_n": actuator_force_n,
        "delta_simply_supported_mm": delta_ss,
        "delta_clamped_mm": delta_cc,
        "gate_mm": GATE_PEAK_MM,
        "conservative_bound_passes": delta_ss <= GATE_PEAK_MM,
        "evidence": "CALCULATION/BOUND (assumes rigid holders, isotropic PLA)",
    }


# ---------------------------------------------------------------------------
# B1b. Stiction / friction bound and the isolation ratio.
# ---------------------------------------------------------------------------
def stiction_bound(tile: int, mass_g: float = COLUMN_MASS_G,
                   mu: float = MU_STATIC, cells: int | None = None) -> dict:
    """Force needed to start a loaded neighbour cell sliding laterally.

    The neighbour's loaded columns are held by static friction against their
    guides. Peak-neighbour-lateral gate is 0.10 mm; the seal is: if the force
    the target can transmit through the rail is below the stiction threshold,
    the neighbour cannot creep at all (isolation ratio -> large).

    F_stiction = mu * N, with N = m g (the column's own weight plus the
    miniature's share). This is an UPPER bound on transmitted lateral force
    the neighbour can tolerate; it is not a measured release force.
    """
    if cells is None:
        cells = tile * tile
    total_mass_g = cells * mass_g
    weight_n = total_mass_g * 1e-3 * 9.80665
    f_stiction_n = mu * weight_n
    return {
        "tile": tile,
        "cells": cells,
        "total_mass_g": round(total_mass_g, 3),
        "weight_n": round(weight_n, 4),
        "mu_static": mu,
        "f_stiction_n": round(f_stiction_n, 5),
        "evidence": "CALCULATION (Coulomb friction model)",
    }


def isolation_ratio(target_motion_mm: float, neighbour_motion_mm: float) -> float:
    """Ratio of intended target motion to induced neighbour motion.

    Returns +inf when the neighbour bound is exactly zero (perfect isolation in
    the model), which the report renders as '>1e6'.
    """
    if neighbour_motion_mm <= 0.0:
        return float("inf")
    return target_motion_mm / neighbour_motion_mm


# ---------------------------------------------------------------------------
# B2. Fixture fit stack-up (worst-case + Monte Carlo).
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FitTol:
    name: str
    nominal_mm: float
    half_range_mm: float
    sigma_mm: float
    kind: str
    source: str


FIT_TOLS = [
    FitTol("holder_outer", 0.0, 0.10, 0.10 / math.sqrt(3), "sourced fact",
           "FDM XY dimensional tolerance ~+/-0.1 mm published class, applied "
           "to the holder outer footprint."),
    FitTol("socket_width", 2.0, 0.08, 0.08 / math.sqrt(3), "assumption",
           "Interchangeable-fixture socket width deviation, +/-0.08 mm."),
    FitTol("seam_gap", SEAM_NOMINAL_MM, 0.05, 0.05 / math.sqrt(3),
           "assumption", "Seam shim + print tolerance +/-0.05 mm."),
]


def fit_monte_carlo(n: int = 200_000, seed: int = 22222) -> dict:
    """Check the fixture dims stay in-spec under tolerance sampling."""
    rng = random.Random(seed)
    sig = {t.name: t.sigma_mm for t in FIT_TOLS}
    wc = {t.name: t.half_range_mm for t in FIT_TOLS}

    def gauss():
        u1 = max(rng.random(), 1e-12)
        u2 = rng.random()
        return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)

    pass_bed = pass_pair = pass_socket = pass_wall = 0
    max_outer = 0.0
    for _ in range(n):
        d = {k: gauss() * s for k, s in sig.items()}
        outer = 10 * PITCH_MM + 2 * BORDER_MM + d["holder_outer"]
        pair = 2 * outer + (SEAM_NOMINAL_MM + d["seam_gap"])
        # Bed fit: a single 10x10 holder must fit the X1C.
        pass_bed += outer <= BED_MM
        # Two holders + seam must be reachable by the rail.
        pass_pair += pair <= 2 * BED_MM
        # Socket stays positive and >= a fixture plate thickness.
        pass_socket += (2.0 + d["socket_width"]) > 0.0
        # Holder wall >= 2.0 mm after the outer tolerance (border is 6 mm).
        pass_wall += (BORDER_MM + d["holder_outer"]) >= HOLDER_WALL_MIN_MM
        max_outer = max(max_outer, outer)

    outer_nom = 10 * PITCH_MM + 2 * BORDER_MM
    return {
        "n": n,
        "seed": seed,
        "nominal_holder_outer_mm": outer_nom,
        "worst_case_holder_outer_mm": round(outer_nom + wc["holder_outer"], 3),
        "bed_mm": BED_MM,
        "mc_pass_bed_fraction": pass_bed / n,
        "mc_pass_pair_fraction": pass_pair / n,
        "mc_pass_socket_fraction": pass_socket / n,
        "mc_pass_wall_fraction": pass_wall / n,
        "max_sampled_outer_mm": round(max_outer, 3),
        "worst_case_bed_ok": (outer_nom + wc["holder_outer"]) <= BED_MM,
        "evidence": "SIMULATION (Monte Carlo over declared fit tolerances)",
    }


# ---------------------------------------------------------------------------
# B3. Analytic run record + claims statement.
# ---------------------------------------------------------------------------
# Analytic proxies for each J2 measured quantity. Each proxy is derived from the
# bounds above, then expressed in the isolation.csv schema. Values are the
# analytic *bound*, which is deliberately conservative (worst side).
def analytic_proxies(tile: int = 10, actuator_force_n: float = 1.0) -> dict:
    rail = rail_coupling(tile, actuator_force_n)
    stic = stiction_bound(tile)
    # Peak vertical proxy = conservative simply-supported rail deflection for a
    # 1 N actuation force (protocol J2-2 applies 1 N).
    peak_vertical = rail["delta_simply_supported_mm"]
    # Peak lateral proxy = the same rail flexibility projected laterally with a
    # 0.1 factor (lateral bending is stiffer with the rail on edge, assumption).
    peak_lateral = 0.1 * peak_vertical
    # Miniature move/tip: rail-induced rotation of the neighbour holder.
    # Slope at the neighbour end of a clamped-clamped beam under centre load is
    # zero; bound it by the simply-supported end rotation theta ~ F L^2/(16 E I).
    b, h = 40.0, RAIL_THICKNESS_MM
    I = b * h ** 3 / 12.0
    theta = actuator_force_n * rail["span_mm"] ** 2 / (16.0 * PLA_E_MPA * I)
    mini_tip = theta * (tile * PITCH_MM) / 2.0   # edge lift across half a tile
    mini_move = mini_tip
    # Seam step: with a 0.40 mm nominal seam and no shared feature above the
    # base, the seam step is a fit, not a motion, quantity. Bound = seam
    # tolerance + rail-induced relative displacement.
    seam_step = SEAM_NOMINAL_MM / 2.0 + peak_vertical
    # Cumulative drift: no mechanism shares a wear surface across the seam in
    # the fixture itself; analytic bound = 0 plus the rail deflection.
    drift = peak_vertical
    # Rig noise: a property of the BUILT fixture (bench, clamps, dial mounts).
    # It cannot be bounded analytically, so the analytic record leaves it blank
    # (the engine returns MISSING -> INCONCLUSIVE) rather than claim zero.
    rig_noise = None
    return {
        "tile": tile,
        "actuator_force_n": actuator_force_n,
        "rig_noise_mm": rig_noise,
        "peak_vertical_mm": peak_vertical,
        "peak_lateral_mm": peak_lateral,
        "miniature_move_mm": mini_move,
        "miniature_tip_mm": mini_tip,
        "seam_step_mm": seam_step,
        "cumulative_drift_mm": drift,
        "cycles": 100,
        "stiction_n": stic["f_stiction_n"],
        "isolation_ratio": isolation_ratio(40.0, peak_vertical),
        "evidence": "CALCULATION/BOUND",
    }


# Regional timing proxy: the gate engine applies the same 26.251 s fail line to
# regional timing. Use the screening model with perfect scaling (benefit of the
# doubt), so the analytic row reflects the best case, not a guess.
def regional_time_proxy(tile: int) -> float:
    fixed = 0.5   # reference/home overhead, Test09 timing model
    fraction = (tile * tile) / (80 * 80)
    return fixed + (FULL_MAP_SECONDS - fixed) * fraction


ANALYTIC_FIELDS = [
    "run_id", "date", "fixture_id", "survivor", "tile_size", "part_revision",
    "slicer_project", "nozzle_mm", "layer_mm", "pla_lot", "operator",
    "instrument_ids", "neighbour_state", "miniature_id", "miniature_mass_g",
    "rig_noise_mm", "peak_vertical_mm", "peak_lateral_mm", "miniature_move_mm",
    "miniature_tip_mm", "seam_step_mm", "seam_load_n", "cumulative_drift_mm",
    "cycles", "regional_clear_settle_s", "notes", "trace_path", "evidence",
]

RECORD_PATH = HERE / "runs" / "isolation_analytic.csv"


def analytic_rows() -> list:
    rows = []
    for tile, survivor, fixture in ((5, "S5", "FX-S5"),
                                    (10, "S5", "FX-S5"),
                                    (20, "S5", "FX-S5")):
        p = analytic_proxies(tile=tile, actuator_force_n=1.0)
        rows.append({
            "run_id": "ANALYTIC-%dx%d" % (tile, tile),
            "date": "2026-09-28",
            "fixture_id": fixture,
            "survivor": survivor,
            "tile_size": "%dx%d" % (tile, tile),
            "part_revision": "analytic/dnd28",
            "slicer_project": "analytic/j2_analytic_gate.py",
            "nozzle_mm": 0.4,
            "layer_mm": 0.2,
            "pla_lot": "",
            "operator": "CTO (analytic gate, DND-28)",
            "instrument_ids": "none (analytic)",
            "neighbour_state": "loaded-nonflat (modelled)",
            "miniature_id": "none (analytic)",
            "miniature_mass_g": 20.0,
            "rig_noise_mm": "" if p["rig_noise_mm"] is None
            else round(p["rig_noise_mm"], 4),
            "peak_vertical_mm": round(p["peak_vertical_mm"], 6),
            "peak_lateral_mm": round(p["peak_lateral_mm"], 6),
            "miniature_move_mm": round(p["miniature_move_mm"], 6),
            "miniature_tip_mm": round(p["miniature_tip_mm"], 6),
            "seam_step_mm": round(p["seam_step_mm"], 6),
            "seam_load_n": 1.0,
            "cumulative_drift_mm": round(p["cumulative_drift_mm"], 6),
            "cycles": 100,
            "regional_clear_settle_s": round(regional_time_proxy(tile), 4),
            "notes": ("analytic bound: rail-beam deflection + Coulomb stiction; "
                      "NOT a measurement (DND-28)"),
            "trace_path": "",
            "evidence": "CALCULATION",
        })
    return rows


def emit_record(path: Path = RECORD_PATH) -> Path:
    rows = analytic_rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ANALYTIC_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return path


# Which J2 protocol claims are retired analytically vs still need measurement.
CLAIMS = [
    ("rig_noise", "J2-0", "analysis",
     "Rig noise is a property of the built fixture (bench, clamps, dial "
     "mounts). NOT retireable analytically -- requires the built rig."),
    ("peak_vertical", "J2-1", "analysis",
     "Boundable: target stroke couples to the neighbour only through the rail; "
     "a clamped-beam bound with 1 N actuation gives << 0.10 mm. Retired as a "
     "BOUND, not a measurement."),
    ("peak_lateral", "J2-1", "analysis",
     "Boundable the same way, plus stiction: Coulomb friction on the loaded "
     "neighbour columns dominates any rail-transmitted shear."),
    ("miniature_move", "J2-1", "analysis",
     "Boundable from rail end-rotation; the miniature is inertia-dominated and "
     "the target stroke does not accelerate the neighbour (no shared drive)."),
    ("miniature_tip", "J2-1", "analysis",
     "Same as miniature_move; an upper bound on holder tilt across half a "
     "tile."),
    ("seam_step", "J2-2", "analysis",
     "The seam step at max adjacent height is a *geometry* quantity (seam + "
     "height fit), so it is analytically computable; the load-dependence is "
     "boundable."),
    ("cumulative_drift", "J2-3", "measurement-required",
     "Creep over 100 cycles depends on wear, dust and print tribology. An "
     "unloaded fixture has no shared wear surface, so the analytic bound is the "
     "rail deflection; real creep CANNOT be retired analytically."),
    ("regional_clear_settle_s", "J2-4", "analysis",
     "Timing is model-derived (reliability.py screening model). Retired as a "
     "screening bound with perfect-scaling benefit of the doubt."),
    ("stiction_release", "J2-1", "measurement-required",
     "The actual force that releases a loaded cell (stiction, contamination) "
     "is tribology and cannot be bounded tightly from first principles."),
]


def report(tile: int = 10) -> str:
    lines = []
    lines.append("J2 analytic isolation gate (DND-28)")
    lines.append("Evidence: sourced fact / assumption / calculation / simulation.")
    lines.append("No MEASURED input. This is NOT a print or a measurement.")
    lines.append("")
    lines.append("[B1a] Shared-rail coupling (CALCULATION/BOUND)")
    for t in TILE_SIZES:
        r = rail_coupling(t, 1.0)
        lines.append("  tile %2dx%-2d span=%.1f mm  delta_ss=%.6f mm  "
                     "delta_cc=%.6f mm  bound_passes(<=%.2f)=%s"
                     % (t, t, r["span_mm"], r["delta_simply_supported_mm"],
                        r["delta_clamped_mm"], GATE_PEAK_MM,
                        r["conservative_bound_passes"]))
    lines.append("")
    lines.append("[B1b] Stiction / friction bound (CALCULATION)")
    for t in TILE_SIZES:
        s = stiction_bound(t)
        lines.append("  tile %2dx%-2d cells=%d weight=%.3f N  "
                     "F_stiction=%.5f N" % (t, t, s["cells"], s["weight_n"],
                                            s["f_stiction_n"]))
    p = analytic_proxies(tile, 1.0)
    lines.append("  isolation ratio (40 mm target stroke / rail-bound neigh) = 1e6+"
                 if p["isolation_ratio"] == float("inf")
                 else "  isolation ratio = %.1f" % p["isolation_ratio"])
    lines.append("")
    lines.append("[B2] Fixture fit stack-up (SIMULATION)")
    f = fit_monte_carlo()
    lines.append("  nominal holder outer = %.2f mm; WC = %.2f mm; bed = %.0f mm"
                 % (f["nominal_holder_outer_mm"],
                    f["worst_case_holder_outer_mm"], f["bed_mm"]))
    lines.append("  MC pass: bed=%.4f pair=%.4f socket=%.4f wall=%.4f"
                 % (f["mc_pass_bed_fraction"], f["mc_pass_pair_fraction"],
                    f["mc_pass_socket_fraction"], f["mc_pass_wall_fraction"]))
    lines.append("")
    lines.append("[B3] Claim dispositions")
    for _key, step, kind, note in CLAIMS:
        lines.append("  [%-20s] %-5s %s" % (kind, step, note))
    return "\n".join(lines)


def verdict() -> dict:
    """Analytic gate verdict for the isolation concept."""
    fails = []
    for t in TILE_SIZES:
        r = rail_coupling(t, 1.0)
        if not r["conservative_bound_passes"]:
            fails.append("rail bound tile %dx%d = %.4f mm > %.2f mm"
                         % (t, t, r["delta_simply_supported_mm"], GATE_PEAK_MM))
    f = fit_monte_carlo()
    if not f["worst_case_bed_ok"]:
        fails.append("worst-case holder exceeds X1C bed")
    if fails:
        return {
            "verdict": "ANALYTIC_KILL_OR_REVISE",
            "reason": "; ".join(fails),
            "residual_uncertainty": "bound is conservative; a real test may be "
                                   "better, but the analytic gate forbids the "
                                   "current geometry.",
        }
    return {
        "verdict": "ANALYTIC_PASS_BOUND_POSITIVE",
        "reason": "rail-coupled neighbour bound is << the 0.10 mm peak gate for "
                  "all tile sizes; fixture fit passes worst-case",
        "residual_uncertainty":
            "This is NOT a measurement. It cannot see stiction release, wear, "
            "dust, creep (J2-3) or the real rig noise floor (J2-0). Those "
            "claims remain measurement-required and are listed in CLAIMS.",
    }


def selftest() -> int:
    failures = 0

    def check(name, cond, detail=""):
        nonlocal failures
        print("[%s] %s %s" % ("PASS" if cond else "FAIL", name, detail))
        failures += 0 if cond else 1

    # Rail bound must shrink with smaller tiles and pass the gate for 1 N.
    big = rail_coupling(20, 1.0)
    small = rail_coupling(5, 1.0)
    check("rail bound decreases with tile size",
          small["delta_simply_supported_mm"] < big["delta_simply_supported_mm"])
    check("rail bound passes peak gate at 1 N",
          big["conservative_bound_passes"], big["delta_simply_supported_mm"])
    check("clamped < simply-supported (conservative ordering)",
          big["delta_clamped_mm"] < big["delta_simply_supported_mm"])

    # Stiction scales with cell count.
    s5, s20 = stiction_bound(5), stiction_bound(20)
    check("stiction scales with cells", s20["f_stiction_n"] > s5["f_stiction_n"])

    # Isolation ratio is finite and positive for a real bound (40 mm stroke).
    ratio = isolation_ratio(40.0, big["delta_simply_supported_mm"])
    check("isolation ratio large", ratio > 100, ratio)

    # Fit Monte Carlo must pass and be deterministic.
    f1 = fit_monte_carlo(n=50_000, seed=999)
    f2 = fit_monte_carlo(n=50_000, seed=999)
    check("fit MC deterministic",
          f1["mc_pass_bed_fraction"] == f2["mc_pass_bed_fraction"])
    check("fit MC bed pass = 1", f1["mc_pass_bed_fraction"] == 1.0)
    check("fit both holders + seam reachable",
          f1["mc_pass_pair_fraction"] == 1.0)
    check("worst-case bed ok", f1["worst_case_bed_ok"])

    # Record schema and evidence discipline.
    rows = analytic_rows()
    check("record has three tile sizes",
          {r["tile_size"] for r in rows} == {"5x5", "10x10", "20x20"})
    check("record evidence never MEASURED",
          all(r["evidence"] != "MEASURED" for r in rows))
    check("record leaves rig noise (J2-0) unmeasured",
          all(r["rig_noise_mm"] == "" for r in rows))
    check("verdict disclaims measurement",
          "NOT a measurement" in verdict()["residual_uncertainty"])

    print()
    print("SELFTEST %s" % ("PASS" if failures == 0 else "FAIL"))
    return 0 if failures == 0 else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--emit-record", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.emit_record:
        p = emit_record()
        print("wrote %s (%d rows)" % (p, len(analytic_rows())))

    if args.json:
        out = {
            "rail_coupling": [rail_coupling(t, 1.0) for t in TILE_SIZES],
            "stiction": [stiction_bound(t) for t in TILE_SIZES],
            "fit_stackup": fit_monte_carlo(),
            "claims": [{"quantity": k, "step": s, "kind": kind, "note": note}
                       for k, s, kind, note in CLAIMS],
            "verdict": verdict(),
            "evidence": "CALCULATION/BOUND/SIMULATION; NOT MEASURED",
        }
        print(json.dumps(out, indent=2))
    elif args.report or not args.emit_record:
        print(report())

    if verdict()["verdict"].startswith("ANALYTIC_KILL"):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
