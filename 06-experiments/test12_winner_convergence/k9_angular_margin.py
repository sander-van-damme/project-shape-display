"""DND-45 K9 - Monte-Carlo angular-error stack-up for the S5 stepped rotor.

K9 (08-current-design, Test12 killer list): the 5-level stepped cam gives a
nominal angular margin of 180/5 - toe_angle = 12.50 deg, reduced to 6.50 deg
after a 6.00 deg worst-case seating error. The +/-0.05 mm FDM positional print
tolerance on the 1.5 mm-radius rotor was NOT propagated. This module does that
propagation.

Geometry (Test08 params.json, the winner CAD's own cam):
    toe_angle(theta) = atan2(toe_width/2, toe_x - center_x)
    angular_margin   = 180/levels - toe_angle - seating_error
The quantity that +/-0.05 mm print error perturbs is the toe lever arm
    arm = toe_x - center_x = 0.85 - (-0.30) = 1.15 mm
and the toe half-width = toe_width/2 = 0.50 mm. The nominal toe_angle is
atan2(0.50, 1.15) = 23.50 deg (reproduces Test09's "23.50 deg toe envelope").

Monte-Carlo terms (all sourced or stated):
    toe_x          : positional tolerance  +/- 0.05 mm  (sourced FDM positional)
    center_x       : positional tolerance  +/- 0.05 mm  (sourced FDM positional)
    toe_width      : extruded feature      +/- 0.05 mm  (sourced FDM dimensional)
    rotor_radius   : profiled feature      +/- 0.05 mm  (sourced FDM dimensional)
    seating_error  : 0..6.00 deg  (Test09 seating gate; modelled uniform and
                     half-normal, both reported)
The rotor-radius term does not enter toe_angle directly (toe_angle is a planar
arm ratio), so it is carried as a correlated shift on the flank contact point
and reported separately; the dominant terms are the two positional offsets on
the lever arm.

Evidence class: CALCULATION / MONTE-CARLO over stated tolerances. No print, no
measurement (DND-27). The +/-0.05 mm tolerance is a sourced FDM capability
claim, not a measured distribution on these parts.
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# --- Parameters (Test08 params.json cam block; Test09 seating gate) ---------
TOE_X_MM = 0.85
CENTER_X_MM = -0.30
TOE_WIDTH_MM = 1.00
CAM_RADIUS_MM = 1.50
CAM_CORE_RADIUS_MM = 1.00

# Sourced FDM positional tolerance used across the repo (DND-28/41 T11-A gate
# and Test08 uncertainty block: body_width +/-0.10, local_pitch +/-0.05).
TOL_XY_MM = 0.05

# Test09 seating gate: residual angular seating error <= 6 deg (gate angle_deg).
SEATING_GATE_DEG = 6.0

# Level counts to test (Test09 levels.csv sweep).
LEVEL_COUNTS = (3, 4, 5, 6, 8, 9, 10)

# DND-19 / Test09 gate: permitted level-height error 0.25 mm; a toe that crosses
# into the neighbouring sector changes level. The angular margin is the pass
# quantity here; the height gate is a separate check.

DEFAULT_DRAWS = 200_000
DEFAULT_SEED = 20260928


def toe_angle_deg(toe_x_mm: float, center_x_mm: float, toe_width_mm: float) -> float:
    """Angular half-envelope of the toe (Test08 analysis.geometry)."""
    return math.degrees(math.atan2(toe_width_mm / 2.0, toe_x_mm - center_x_mm))


def nominal_margin_deg(levels: int) -> float:
    return 180.0 / levels - toe_angle_deg(TOE_X_MM, CENTER_X_MM, TOE_WIDTH_MM)


@dataclass(frozen=True)
class MarginResult:
    levels: int
    draws: int
    mean_deg: float
    std_deg: float
    p05_deg: float
    p50_deg: float
    p95_deg: float
    min_deg: float
    max_deg: float
    p_negative: float
    nominal_deg: float
    seating_is_random: bool


def sample_margin(levels: int, draws: int, seating_is_random: bool,
                  seed: int = DEFAULT_SEED, distribution: str = "uniform",
                  rng: random.Random | None = None) -> list[float]:
    """Draw angular margins for one level count.

    distribution:
      "uniform"  - each dimension is uniform in +/-TOL_XY_MM. This treats the
                   stated "+/-0.05 mm tolerance" as a bounded capability limit,
                   the most common reading, and is minimax-honest.
      "gaussian" - each dimension is N(0, TOL_XY_MM). This treats +/-0.05 mm as
                   1 sigma, giving a heavier tail; reported as the conservative
                   case. A 3-sigma draw reaches +/-0.15 mm.
    seating_is_random False holds the seating error at its worst-case 6.00 deg
    gate; True draws a half-normal |N(0, 2)| truncated at 6 deg.
    """
    rng = rng or random.Random(seed)
    if distribution == "uniform":
        def dim() -> float:
            return rng.uniform(-TOL_XY_MM, TOL_XY_MM)
    elif distribution == "gaussian":
        def dim() -> float:
            return rng.gauss(0.0, TOL_XY_MM)
    else:
        raise ValueError(distribution)
    out = []
    for _ in range(draws):
        dx = dim()                            # toe_x positional
        dc = dim()                            # center_x positional
        dw = dim()                            # toe_width feature size
        d_rotor = dim()                       # rotor radius feature size
        toe = toe_angle_deg(TOE_X_MM + dx, CENTER_X_MM + dc, TOE_WIDTH_MM + dw)
        # A rotor printed off-radius shifts the flank contact; carry the 1-sigma
        # shift as a small angular penalty ~ |d_rotor| / r radians.
        rotor_penalty_deg = math.degrees(abs(d_rotor) / CAM_RADIUS_MM)
        if seating_is_random:
            seat = min(SEATING_GATE_DEG, abs(rng.gauss(0.0, SEATING_GATE_DEG / 3.0)))
        else:
            seat = SEATING_GATE_DEG
        out.append(180.0 / levels - toe - rotor_penalty_deg - seat)
    return out


def summarise(levels: int, vals: list[float], seating_is_random: bool) -> MarginResult:
    n = len(vals)
    s = sorted(vals)
    mean = sum(vals) / n
    var = sum((v - mean) ** 2 for v in vals) / n
    neg = sum(1 for v in vals if v < 0.0)
    return MarginResult(
        levels=levels, draws=n,
        mean_deg=mean, std_deg=math.sqrt(var),
        p05_deg=s[int(0.05 * n)], p50_deg=s[int(0.50 * n)], p95_deg=s[int(0.95 * n)],
        min_deg=s[0], max_deg=s[-1],
        p_negative=neg / n,
        nominal_deg=nominal_margin_deg(levels),
        seating_is_random=seating_is_random,
    )


def run(draws: int = DEFAULT_DRAWS, seed: int = DEFAULT_SEED) -> dict:
    """Full K9 stack-up over all level counts, seating models and tolerance shapes."""
    results = []
    for distribution in ("uniform", "gaussian"):
        for approach in (False, True):   # adversarial-worst-case seat, then random seat
            rng = random.Random(seed)
            for levels in LEVEL_COUNTS:
                vals = sample_margin(levels, draws, approach, rng=rng,
                                     distribution=distribution)
                r = summarise(levels, vals, approach)
                d = r.__dict__
                d["distribution"] = distribution
                results.append(d)
    # Primary = uniform (bounded tolerance) + worst-case seat.
    primary = [r for r in results
               if r["distribution"] == "uniform" and not r["seating_is_random"]]
    gauss = [r for r in results
             if r["distribution"] == "gaussian" and not r["seating_is_random"]]
    random_uni = [r for r in results
                  if r["distribution"] == "uniform" and r["seating_is_random"]]

    def safe(rows: list[dict]) -> list[int]:
        return [r["levels"] for r in rows if r["p_negative"] == 0.0]

    return {
        "evidence_class": "CALCULATION/MONTE-CARLO; no print, no measurement (DND-27)",
        "model": {
            "toe_angle_deg": toe_angle_deg(TOE_X_MM, CENTER_X_MM, TOE_WIDTH_MM),
            "nominal_5_level_margin_deg": nominal_margin_deg(5),
            "nominal_6_level_margin_deg": nominal_margin_deg(6),
            "tol_xy_mm": TOL_XY_MM,
            "tol_distribution": "uniform +/-0.05 (primary) and gaussian sigma=0.05 (conservative)",
            "seating_gate_deg": SEATING_GATE_DEG,
            "rotor_radius_mm": CAM_RADIUS_MM,
            "core_radius_mm": CAM_CORE_RADIUS_MM,
        },
        "draws": draws,
        "seed": seed,
        "results": results,
        "primary_model": "uniform tolerance, worst-case 6 deg seat",
        "max_safe_levels_primary": max(safe(primary)) if safe(primary) else None,
        "max_safe_levels_gaussian_conservative": max(safe(gauss)) if safe(gauss) else None,
        "max_safe_levels_random_seat_uniform": max(safe(random_uni)) if safe(random_uni) else None,
        "five_level_primary": next(r for r in primary if r["levels"] == 5),
        "six_level_primary": next(r for r in primary if r["levels"] == 6),
    }


def main() -> None:
    print(json.dumps(run(), indent=2))


if __name__ == "__main__":
    main()
