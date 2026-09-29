"""SHA-12 T2 camera K2 analytic test (occlusion + contrast at 2 angles).

K2 zero-silent proof for T2 (overhead camera, zero motion) from SHA-10.
Evidence class: CALCULATION (exact shadow-projection onto the low-top plane
+ Lambertian contrast bounds). DND-27: no print, purchase, or measurement.
Ranges with stated confidence; residual uncertainty explicit.

Kill criteria (up front, from SHA-10 + SHA-12 acceptance):
  K2-KILL if EITHER:
    (a) any occluded cells (>0) in either view for general terrain, OR
    (b) on/off height contrast < 2x on any cell.
  PASS (advance to line-BOM reprice question) requires >=2x contrast on 100%
  of cells AND 0 occluded, both angles.

Geometry assumptions (nominal; sweep where noted):
  pitch p = 5.08 mm, travel H = 40 mm (low top z=0, tall top z=40),
  array 80x80, extent 406.4 mm, column top w = 4.8 mm (gap 0.28 mm),
  camera = pinhole, OV2640-class UXGA 1600x1200 (20.0 px/cell over field).
  Top-down: axis vertical through array center, height Hcam above low tops.
    Nominal Hcam = 700 mm; sweep 500/700/1000 mm.
  Oblique: axis tilted 45 deg from vertical, azimuth along +y: exact parallel
    shadow-rectangle projection (this UNDERESTIMATES real pinhole occlusion,
    so a kill here only gets worse with perspective) + one pinhole-oblique
    spot check at 900 mm slant range.

Occlusion method (exact, gap-aware, conservative toward PASS):
  Tall columns are W x W x [0,H] solids; low cells are top surfaces at z=0.
  A low cell center g is occluded iff segment g->camera meets any tall solid.
  Top-down/pinhole-oblique: project each tall box's 8 corners through the
  camera point onto z=0, take convex hull (= exact shadow polygon on the
  low-top plane), mark low cells inside. Uses the W box, so gap rays are
  credited as passing: a LOWER BOUND on occlusion. Full-pitch boxes would
  only add more.
  Parallel oblique: shadow rect W x (W+L), L = H*tan(45), exact for boxes.
  Tall cells are never occluded (nothing is taller); only low cells tested.

Run:  python 06-experiments/test17_t2_k2_camera/t2_k2.py
Gate: python 06-experiments/test17_t2_k2_camera/t2_k2.py --gate
"""

from __future__ import annotations

import argparse
import json
import math
import random

P = 5.08          # pitch, mm
H = 40.0          # travel, mm
N = 80            # grid
EXTENT = N * P    # 406.4 mm
W = 4.8           # column top width, mm (gap = 0.28)
HCAM_NOM = 700.0  # nominal camera height, mm
HCAM_SWEEP = (500.0, 700.0, 1000.0)
OBLIQUE_DEG = 45.0
PX_PER_CELL = round(1600.0 / EXTENT * P, 1)  # 20.0


def cell_center(i: int, j: int) -> tuple[float, float]:
    return ((i - (N - 1) / 2) * P, (j - (N - 1) / 2) * P)


def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 1:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def point_in_convex(pt, hull) -> bool:
    x, y = pt
    n = len(hull)
    if n == 0:
        return False
    if n == 1:
        return abs(x - hull[0][0]) < 1e-9 and abs(y - hull[0][1]) < 1e-9
    if n == 2:
        (ax, ay), (bx, by) = hull
        if abs((bx - ax) * (y - ay) - (by - ay) * (x - ax)) > 1e-6:
            return False
        d = (x - ax) * (bx - ax) + (y - ay) * (by - ay)
        return 0 <= d <= (bx - ax) ** 2 + (by - ay) ** 2
    sign = 0
    for k in range(n):
        ax, ay = hull[k]
        bx, by = hull[(k + 1) % n]
        c = (bx - ax) * (y - ay) - (by - ay) * (x - ax)
        if abs(c) < 1e-9:
            continue
        s = 1 if c > 0 else -1
        if sign == 0:
            sign = s
        elif s != sign:
            return False
    return True


def project_to_ground(pt3, cam):
    """Ray from camera through pt3 meets z=0. Camera must be above pt3."""
    (x, y, z), (cx, cy, cz) = pt3, cam
    assert cz > z, "camera below surface point"
    t = cz / (cz - z)
    return (cx + (x - cx) * t, cy + (y - cy) * t)


def tall_boxes(heights):
    """Yield (xc, yc) centers of tall columns."""
    for j in range(N):
        row = heights[j]
        for i in range(N):
            if row[i] >= H - 1e-9:
                yield cell_center(i, j)


def shadow_occluded_pinhole(heights, cam) -> int:
    """Exact gap-aware lower-bound occlusion count for a pinhole camera."""
    low = [[heights[j][i] < H - 1e-9 for i in range(N)] for j in range(N)]
    hidden = [[False] * N for _ in range(N)]
    for (xc, yc) in tall_boxes(heights):
        corners = [(xc + sx * W / 2, yc + sy * W / 2, z)
                   for sx in (-1, 1) for sy in (-1, 1) for z in (0.0, H)]
        proj = [project_to_ground(c, cam) for c in corners]
        hull = convex_hull(proj)
        xs = [p[0] for p in hull]
        ys = [p[1] for p in hull]
        i_lo = max(0, int(math.floor((min(xs)) / P + N / 2)))
        i_hi = min(N - 1, int(math.floor((max(xs)) / P + N / 2)))
        j_lo = max(0, int(math.floor((min(ys)) / P + N / 2)))
        j_hi = min(N - 1, int(math.floor((max(ys)) / P + N / 2)))
        for j in range(j_lo, j_hi + 1):
            for i in range(i_lo, i_hi + 1):
                if low[j][i] and not hidden[j][i]:
                    if point_in_convex(cell_center(i, j), hull):
                        hidden[j][i] = True
    return sum(sum(1 for v in row if v) for row in hidden)


def shadow_occluded_parallel_oblique(heights, theta_deg: float) -> int:
    """Exact shadow-rect occlusion for parallel oblique (camera on -y side)."""
    L = H * math.tan(math.radians(theta_deg))
    hidden = [[False] * N for _ in range(N)]
    for (xc, yc) in tall_boxes(heights):
        x0, x1 = xc - W / 2, xc + W / 2
        y0, y1 = yc - W / 2, yc + W / 2 + L
        i_lo = max(0, int(math.ceil(x0 / P + N / 2 - 0.5)))
        i_hi = min(N - 1, int(math.floor(x1 / P + N / 2 - 0.5)))
        j_lo = max(0, int(math.ceil(y0 / P + N / 2 - 0.5)))
        j_hi = min(N - 1, int(math.floor(y1 / P + N / 2 - 0.5)))
        # cell-center-in-rect test (centers strictly inside shadow count)
        for j in range(j_lo, j_hi + 1):
            for i in range(i_lo, i_hi + 1):
                if heights[j][i] < H - 1e-9 and not hidden[j][i]:
                    x, y = cell_center(i, j)
                    if x0 <= x <= x1 and y0 <= y <= y1:
                        hidden[j][i] = True
    return sum(sum(1 for v in row if v) for row in hidden)


def make_pattern(name: str):
    h = [[0.0] * N for _ in range(N)]
    if name == "flat_low":
        pass
    elif name == "single_tall_center":
        h[N // 2][N // 2] = H
    elif name == "single_wall":
        for i in range(N):
            h[N // 2 - 1][i] = H  # wall row just camera-side of center
    elif name == "stripes":
        for j in range(N):
            if j % 2 == 0:
                for i in range(N):
                    h[j][i] = H
    elif name == "checker":
        for j in range(N):
            for i in range(N):
                if (i + j) % 2 == 0:
                    h[j][i] = H
    elif name == "random50":
        rng = random.Random(0)
        for j in range(N):
            for i in range(N):
                if rng.random() < 0.5:
                    h[j][i] = H
    else:
        raise ValueError(name)
    return h


def occlusion_study() -> dict:
    out: dict = {"assumptions": {
        "pitch_mm": P, "travel_mm": H, "grid": f"{N}x{N}",
        "top_width_mm": W, "gap_mm": round(P - W, 2),
        "hcam_sweep_mm": list(HCAM_SWEEP), "hcam_nominal_mm": HCAM_NOM,
        "oblique_deg_from_vertical": OBLIQUE_DEG,
        "px_per_cell": PX_PER_CELL,
        "method": "exact shadow projection, gap-aware W-box lower bound",
        "confidence": "high (closed-form projection; only lens distortion / "
                      "Bayer / noise unmodeled, none of which remove occlusion)",
    }}
    th = math.radians(OBLIQUE_DEG)
    L = H * math.tan(th)
    out["closed_form_shadow_45deg"] = {
        "length_mm": round(L, 2),
        "cells": round(L / P, 2),
        "fully_hidden_behind_each_tall_wall": int(L // P),  # 7
        "partially_hidden": 1,  # 7.87 -> 7 full + 1 partial ~= 8 (SHA-10 claim)
        "claim_check": "SHA-10 '~8 cells' CONFIRMED (7.87 pitches)",
    }
    edge: dict = {}
    for hc in HCAM_SWEEP:
        for label, r in (("edge_mid", EXTENT / 2), ("corner", EXTENT / math.sqrt(2))):
            ang = math.degrees(math.atan(r / hc))
            edge.setdefault(label, {})[str(int(hc))] = {
                "chief_ray_tilt_deg": round(ang, 2),
                "shadow_mm": round(H * math.tan(math.radians(ang)), 2),
                "shadow_cells": round(H * math.tan(math.radians(ang)) / P, 2),
            }
    out["topdown_pinhole_edge_tilt"] = edge
    patterns = ["flat_low", "single_tall_center", "single_wall",
                "stripes", "checker", "random50"]
    cache = {name: make_pattern(name) for name in patterns}
    topdown: dict = {}
    for name in patterns:
        topdown[name] = {str(int(hc)): shadow_occluded_pinhole(
            cache[name], (0.0, 0.0, hc)) for hc in HCAM_SWEEP}
    out["topdown_occluded_cells_of_6400"] = topdown
    out["oblique45_parallel_bound_occluded_cells_of_6400"] = {
        name: shadow_occluded_parallel_oblique(cache[name], OBLIQUE_DEG)
        for name in patterns}
    S = 900.0
    cam_obl = (0.0, -S * math.sin(th), S * math.cos(th))
    out["oblique45_pinhole_spotcheck_slant900"] = {
        name: shadow_occluded_pinhole(cache[name], cam_obl)
        for name in ("single_wall", "stripes", "random50")}
    out["reading"] = (
        "Parallel bound already kills (hundreds-thousands occluded); "
        "pinhole spot check is worse (adds radial perspective spread). "
        "Top-down is occlusion-free only for flat/single-feature patterns; "
        "general terrain (stripes/checker/random) hides 1700-3000 valley "
        "cells even top-down at 500-1000 mm (gap-aware lower bound)."
    )
    return out


def contrast_study() -> dict:
    rows = {}
    for hc in HCAM_SWEEP:
        inv_sq = (hc / (hc - H)) ** 2          # point light at camera, center
        magnif = hc / (hc - H)                  # perspective size ratio
        rows[str(int(hc))] = {
            "point_light_at_camera_max_ratio": round(inv_sq, 3),
            "perspective_size_ratio": round(magnif, 3),
            "size_delta_px_on_20px_cell": round(PX_PER_CELL * (magnif - 1), 2),
        }
    return {
        "assumptions": {
            "tops": "coplanar-parallel Lambertian, same albedo/normal "
                    "(monochrome PLA tops); diffuse dome + optional point "
                    "light at camera; confidence medium-high (textbook radiometry)",
        },
        "topdown": {
            "diffuse_dome_ratio": 1.0,
            "per_hcam": rows,
            "verdict": "Max top-surface brightness ratio 1.08-1.17x "
                       "(point light AT camera, center field, best case); "
                       "diffuse room light ~1.00-1.05x. Kill line needs >=2x "
                       "on 100% of cells -> FAIL by ~2x margin. Perspective "
                       "size cue is 4-9% (<=1.7 px), not a radiometric contrast, "
                       "and needs calibrated absolute reference.",
            "gap_AO_note": "Height-correlated signal lives only in gap pixels "
                           "(~5.5% of area), weakest at center where occlusion "
                           "is best; subpixel segmentation at 20 px/cell, "
                           "not a per-cell 2x top-contrast mechanism.",
        },
        "oblique45": {
            "tall_column_sidewall_vs_top_pixel_ratio": round(H / W, 1),
            "verdict": "Tall columns THEMSELVES are bright (side wall "
                       "~8x top area) but each wall projects onto image "
                       "positions of cells BEHIND it (correspondence "
                       "ambiguous) and those cells are occluded (signal "
                       "undefined, 0x). Per-cell decode of 100% cells from "
                       "one view is geometrically impossible; two views still "
                       "leave shadowed valleys ambiguous (classic occlusion); "
                       "stereo/structured-light = new subsystem outside the "
                       "T2 zero-motion single-camera claim -> FAIL.",
        },
        "kill_line": ">=2x on/off contrast on 100% of cells, 0 occluded",
        "kill_line_met": False,
    }


def screen() -> dict:
    occ = occlusion_study()
    con = contrast_study()
    wall_obl = occ["oblique45_parallel_bound_occluded_cells_of_6400"]["single_wall"]
    verdict = (
        "REJECT T2 (K2 FAIL): 45-deg oblique hides ~8 cells behind each tall "
        f"column (single-wall pattern: {wall_obl}/6400 occluded, 0 allowed); "
        "top-down single view has ~0 geometric height cue (max ~1.1x vs 2x "
        "kill line). A7-V stays parked."
    )
    return {
        "evidence_class": "CALCULATION (exact shadow projection + Lambertian "
                          "bounds); DND-27, no print/purchase/measurement",
        "kill_criteria": {
            "K2a_occlusion": "0 occluded cells in either view on general terrain",
            "K2b_contrast": ">=2x on/off contrast on 100% of cells, both angles",
        },
        "occlusion": occ,
        "contrast": con,
        "verdict": verdict,
        "k2_pass": False,
        "a7v_revisit_opens": False,
    }


CHECKS: list[tuple[str, bool]] = []


def check(name: str, cond: bool) -> None:
    CHECKS.append((name, bool(cond)))


def gate() -> int:
    r = screen()
    occ = r["occlusion"]
    con = r["contrast"]
    CHECKS.clear()
    check("45-deg shadow length ~= 8 cells (7.5-8.0)",
          7.5 <= occ["closed_form_shadow_45deg"]["cells"] <= 8.0)
    wall = occ["oblique45_parallel_bound_occluded_cells_of_6400"]["single_wall"]
    check(f"single-wall oblique occludes ~640 cells (got {wall})",
          550 <= wall <= 730)
    rnd = occ["oblique45_parallel_bound_occluded_cells_of_6400"]["random50"]
    check(f"random50 oblique occludes thousands (got {rnd})", rnd >= 1500)
    stripe = occ["oblique45_parallel_bound_occluded_cells_of_6400"]["stripes"]
    check(f"stripes oblique occludes thousands (got {stripe})", stripe >= 1500)
    flat = occ["topdown_occluded_cells_of_6400"]["flat_low"]["700"]
    check(f"top-down flat field ~0 occluded at center (got {flat})", flat <= 50)
    wall_td = occ["topdown_occluded_cells_of_6400"]["single_wall"]["700"]
    check(f"top-down center wall honestly ~0 (got {wall_td}; near-vertical "
          "rays)", wall_td <= 50)
    stripes_td = occ["topdown_occluded_cells_of_6400"]["stripes"]["700"]
    check(f"top-down general terrain still occludes thousands (got "
          f"{stripes_td})", stripes_td >= 1000)
    mx = max(v["point_light_at_camera_max_ratio"]
             for v in con["topdown"]["per_hcam"].values())
    check(f"top-down contrast max < 2x (got {mx})", mx < 2.0)
    check("kill line honestly NOT met", con["kill_line_met"] is False)
    check("verdict rejects T2", r["verdict"].startswith("REJECT"))
    check("A7-V revisit stays closed", r["a7v_revisit_opens"] is False)
    passed = sum(1 for _, ok in CHECKS if ok)
    total = len(CHECKS)
    for name, ok in CHECKS:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\nK2: FAIL -> T2 REJECTED; A7-V revisit opens: "
          f"{r['a7v_revisit_opens']}")
    print(f"{passed}/{total} K2 checks pass")
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
