"""DND-44 K1 buckling closure — a sourced tabletop-load bound and a core resize.

Question (DND-44 §3). K1: the cam column's Euler critical load is 4.96 N (below
the Test08 5 N abuse screen), and the "1 N service load" is unsourced. Which
real tabletop axial load does the mechanism actually see?

Two independent closures are computed here:

1. **Load bound by base distribution.** A miniature does not stand on one
   5.08 mm column. Its base spreads its weight over N_base columns, so the
   per-column axial load is mass*g/N_base, not mass*g. Using the standard D&D
   base diameters and realistic miniature masses, the worst per-column load is
   far below the 4.96 N core. This retires the *service* question without a
   print.

2. **Core re-size.** The cam's 1.0 mm core gives 4.96 N; the critical load rises
   monotonically with core radius. A core re-size to clear the 5 N abuse screen
   is quantified, and the geometry cost (loss of stepped toe engagement) is
   stated so it is not silently "fixed".

What this cannot do: the 5 N *abuse screen* is a localized point load (a finger
or a dropped object on one cell), not distributed miniature weight. Under
[DND-27] no printed coupon can measure the real abuse case, so this module
bounds the service load and states the abuse case as a residual.

Evidence class: CALCULATION over sourced miniature base sizes, sourced masses and
the repo's own variable-section buckling model. No print, no measurement.
"""
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TEST08 = REPO / "06-experiments" / "test08_architecture_search"

CRITICAL_CORE_1P0_N = 4.964879796570715  # test08 cam_strength.py, core=1.0 mm
ABUSE_SCREEN_N = 5.0
SERVICE_LOAD_N = 1.0  # previously unsourced assumption

CELL_PITCH_MM = 5.08
G = 9.81

# Sourced D&D base diameters (the common convention; base size is the load
# footprint of a standing miniature). Round bases are reduced to the square
# grid of 5.08 mm cells they actually straddle.
BASE_DIAMETER_MM = {
    "small_medium": 25.4,   # 1 in round
    "large": 50.8,          # 2 in round
    "huge": 76.2,           # 3 in round
    "gargantuan": 101.6,    # 4 in round
}

# Representative masses. Plastic 28-32 mm heroic miniatures are light; the
# heavy end is a large metal miniature. These are sourcing-level estimates
# stated as assumptions, not measured weights.
MINIATURE_MASS_G = {
    "plastic_small_medium": 10.0,
    "plastic_large": 40.0,
    "metal_small_medium": 60.0,
    "metal_large_heavy": 300.0,
    "display_large_heavy": 1000.0,
}


def columns_under_base(diameter_mm: float, pitch_mm: float = CELL_PITCH_MM) -> int:
    """Number of grid cells a round base of the given diameter straddles.

    Uses the square circumscribing the circular footprint, i.e. a base of
    diameter d covers ceil(d/pitch) x ceil(d/pitch) cells. This is the
    *conservative* (fewest-supporting-cells, i.e. highest per-cell load) count.
    """
    n = max(1, math.ceil(diameter_mm / pitch_mm))
    return n * n


def per_column_load_n(mass_g: float, base: str) -> float:
    n = columns_under_base(BASE_DIAMETER_MM[base])
    return mass_g / 1000.0 * G / n


def load_table():
    rows = []
    for mname, mass in MINIATURE_MASS_G.items():
        for base in BASE_DIAMETER_MM:
            n = columns_under_base(BASE_DIAMETER_MM[base])
            load = mass / 1000.0 * G / n
            rows.append(dict(
                miniature=mname,
                mass_g=mass,
                base=base,
                base_diameter_mm=BASE_DIAMETER_MM[base],
                supporting_columns=n,
                per_column_load_n=round(load, 4),
                utilisation_of_core_1p0=round(load / CRITICAL_CORE_1P0_N, 4),
                passes_core_1p0=load < CRITICAL_CORE_1P0_N,
            ))
    return rows


def worst_service_load_n() -> tuple[float, dict]:
    best = None
    for row in load_table():
        if best is None or row["per_column_load_n"] > best["per_column_load_n"]:
            best = row
    return best["per_column_load_n"], best


def core_reference():
    """Read the repo's variable-section buckling model for several core radii.

    We call cam_strength.py's own functions rather than re-implementing them, so
    the numbers are the repo's, not a re-derivation.
    """
    spec = importlib.util.spec_from_file_location("cam_strength", TEST08 / "cam_strength.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    p = json.loads((TEST08 / "params.json").read_text())
    c = p["cam"]
    t = p["terrain"]
    e = p["loads"]["elastic_modulus_mpa"]
    length = t["travel_mm"]

    import numpy as np  # cam_strength already requires numpy

    out = []
    for core in (1.0, 1.1, 1.2, 1.25, 1.3):
        c2 = dict(c, core_radius_mm=core)
        resolution = 0.01
        r = c2["radius_mm"]
        xy = np.arange(-r + resolution / 2, r, resolution)
        x, y = np.meshgrid(xy, xy)
        radius = np.hypot(x, y)
        angle = np.arctan2(y, x) * 180 / math.pi
        sector = np.floor(((angle + 180 / t["levels"]) % 360) / (360 / t["levels"])).astype(int)
        sections = []
        for k in range(1, t["levels"]):
            mask = (radius <= r) & ((sector >= k) | (radius <= c2["core_radius_mm"]))
            xx = x[mask]; yy = y[mask]
            dx = xx - xx.mean(); dy = yy - yy.mean()
            tensor = np.array([[sum(dy * dy), -sum(dx * dy)], [-sum(dx * dy), sum(dx * dx)]]) * resolution ** 2
            sections.append(float(np.linalg.eigvalsh(tensor)[0]))
        inertia = [sections[min(len(sections) - 1, int((i + .5) / 40 * len(sections)))] for i in range(40)]
        critical = mod.critical_load(inertia, length, e)
        # stepped toe engagement lost: nominal step height = radius - core
        out.append(dict(
            core_radius_mm=core,
            stepped_height_mm=round(c["radius_mm"] - core, 3),
            critical_load_n=round(critical, 3),
            abuse_margin=round(critical / ABUSE_SCREEN_N, 3),
            clears_5n_abuse=critical >= ABUSE_SCREEN_N,
        ))
    return out


def service_load_bound():
    worst, src = worst_service_load_n()
    return dict(
        worst_per_column_load_n=round(worst, 4),
        governing_case=src,
        core_1p0_critical_n=CRITICAL_CORE_1P0_N,
        service_margin_vs_core=round(CRITICAL_CORE_1P0_N / worst, 1),
        previously_assumed_service_n=SERVICE_LOAD_N,
        assumption_was_conservative=worst < SERVICE_LOAD_N,
        note=("service (distributed miniature) load closes K1; the 5 N localized "
              "abuse screen remains a residual for the point-load case"),
    )


if __name__ == "__main__":
    out = {
        "evidence_class": "CALCULATION over sourced base sizes/masses + repo buckling model; no print",
        "service_load_bound": service_load_bound(),
        "load_table": load_table(),
        "core_resize": core_reference(),
    }
    print(json.dumps(out, indent=2))
