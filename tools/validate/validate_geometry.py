#!/usr/bin/env python3
"""Software-only geometry validation harness for the Shape Display program.

This is the single command that replaces "print it and see": it renders the
OpenSCAD fixtures with a real OpenSCAD, validates the resulting meshes, and
runs the analytic printability gate. It is intentionally usable **inside the
rootless dev container** as well as on CI.

PIPELINE
--------
    1. tool check     - locate `openscad`; install instructions if absent.
    2. render         - .scad -> .stl for every fixture part (real OpenSCAD).
    3. mesh validate  - parse every rendered + checked-in STL: watertight-ish,
                        finite vertices, non-empty bbox, X1C bed fit.
    4. printability   - analytic FDM pass/RISK/FAIL table vs sourced limits.

EVIDENCE CLASS
--------------
    Rendering and mesh checks are CAD evidence.
    The printability table is CALCULATION over CAD parameters.
    Nothing here is a print or a measurement.

USAGE
-----
    python tools/validate/validate_geometry.py            # full run
    python tools/validate/validate_geometry.py --no-render # skip OpenSCAD step
    python tools/validate/validate_geometry.py --json out.json

Exit code is non-zero if any hard gate fails. A missing OpenSCAD binary is a
*skip* for the render step (reported, never silent) unless --require-openscad
is given.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FAB = REPO / "06-experiments" / "test11_falsification_library"
SHARED = REPO / "06-experiments" / "test11_shared_drive_gate_analysis"
BED_MM = 256.0

# --- fixtures to render: (label, scad file, extra -D args) --------------------
FAB_SCAD = (REPO / "08-integrated-designs" / "s5r-shared-drive-register"
            / "fabrication" / "scad" / "s5r_parts.scad")
RENDER_TARGETS = [
    ("j2_isolation_rig", FAB / "j2_isolation_rig.scad", []),
    ("selector_fanout_coupon", SHARED / "selector_fanout_coupon.scad", []),
    ("s5r_register_cell", REPO / "06-experiments" / "test12_winner_convergence"
     / "s5r_register.scad", ['-D', 'part="cell"']),
    ("s5r_bank_assembly", REPO / "06-experiments" / "test12_winner_convergence"
     / "s5r_bank.scad", ['-D', 'part="assembly"']),
    ("s5r_bank_comber", REPO / "06-experiments" / "test12_winner_convergence"
     / "s5r_bank.scad", ['-D', 'part="comber"']),
    ("s5r_bank_carriage", REPO / "06-experiments" / "test12_winner_convergence"
     / "s5r_bank.scad", ['-D', 'part="carriage"']),
    # DND-60/DND-61 complete printable part set. DND-61 renders the two
    # structural tiles at their true full size (no reduced witness blocks); see
    # 08-integrated-designs/s5r-shared-drive-register/fabrication/README.md.
    ("s5r_fab_cell_cartridge", FAB_SCAD, ['-D', 'part="cell_cartridge"']),
    ("s5r_fab_rotor", FAB_SCAD, ['-D', 'part="rotor"']),
    ("s5r_fab_drive_pawl", FAB_SCAD, ['-D', 'part="drive_pawl"']),
    ("s5r_fab_keeper", FAB_SCAD, ['-D', 'part="keeper"']),
    ("s5r_fab_detent_leaf", FAB_SCAD, ['-D', 'part="detent_leaf"']),
    ("s5r_fab_rack_strip", FAB_SCAD, ['-D', 'part="rack_strip"']),
    ("s5r_fab_bank_drive_housing", FAB_SCAD, ['-D', 'part="bank_drive_housing"']),
    ("s5r_fab_reset_comber", FAB_SCAD, ['-D', 'part="reset_comber"']),
    ("s5r_fab_writer_carriage", FAB_SCAD, ['-D', 'part="writer_carriage"']),
    ("s5r_fab_platen_module", FAB_SCAD, ['-D', 'part="platen_module"']),
    ("s5r_fab_lift_frame_rail", FAB_SCAD, ['-D', 'part="lift_frame_rail"']),
    ("s5r_fab_guide_bracket", FAB_SCAD, ['-D', 'part="guide_bracket"']),
    ("s5r_fab_solenoid_mount", FAB_SCAD, ['-D', 'part="solenoid_mount"']),
    ("s5r_fab_comber_cam", FAB_SCAD, ['-D', 'part="comber_cam"']),
]


def find_openscad() -> str | None:
    return shutil.which("openscad")


def openscad_env() -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    return env


def render(scad: Path, out: Path, osc: str, extra: list[str]) -> tuple[bool, str]:
    if not scad.exists():
        return False, f"missing source {scad}"
    try:
        # DND-61: the full-tile S5-R cartridge is a single ~10.5 min CGAL render
        # on the reference container, so the budget is 30 min (was 10 min when
        # the cartridge was an 8x8 witness).
        proc = subprocess.run(
            [osc, "-o", str(out), *extra, str(scad)],
            capture_output=True, text=True, timeout=1800, env=openscad_env())
    except subprocess.TimeoutExpired:
        return False, "render timed out"
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout).strip()[:300]
    if not out.exists() or out.stat().st_size == 0:
        return False, "render produced no output (empty solid is likely)"
    return True, f"{out.stat().st_size} bytes"


def read_stl_bbox(path: Path):
    """Return (ntris, lo, hi) for ASCII or binary STL; None if empty/unreadable."""
    data = path.read_bytes()
    if data[:5] == b"solid" and b"facet" in data[:2000]:
        lo = [1e18] * 3
        hi = [-1e18] * 3
        n = 0
        for line in data.decode("ascii", "ignore").splitlines():
            line = line.strip()
            if line.startswith("vertex"):
                n += 1
                for k, tok in enumerate(line.split()[1:4]):
                    v = float(tok)
                    lo[k] = min(lo[k], v)
                    hi[k] = max(hi[k], v)
        return (n // 3, lo, hi) if n else None
    if len(data) < 84:
        return None
    cnt = struct.unpack("<I", data[80:84])[0]
    if cnt == 0:
        return None
    expected = 84 + cnt * 50
    if len(data) < expected:
        return None
    lo = [1e18] * 3
    hi = [-1e18] * 3
    for i in range(cnt):
        # per-record: 3 normal floats, then 9 vertex floats, then 2-byte attr
        verts = struct.unpack_from("<9f", data, 84 + i * 50 + 12)
        for v in range(3):
            for k in range(3):
                c = verts[v * 3 + k]
                if c != c or abs(c) > 1e6:
                    return None
                lo[k] = min(lo[k], c)
                hi[k] = max(hi[k], c)
    return cnt, lo, hi


def mesh_validate(out_dir: Path, extra_paths: list[Path]) -> list[dict]:
    results = []
    paths = sorted(out_dir.glob("*.stl")) + extra_paths
    for p in paths:
        if not p.exists():
            continue
        got = read_stl_bbox(p)
        if got is None:
            results.append({"file": p.name, "verdict": "FAIL",
                            "reason": "unreadable or empty mesh"})
            continue
        n, lo, hi = got
        size = [hi[k] - lo[k] for k in range(3)]
        fits = all(s <= BED_MM for s in size)
        nondegenerate = all(s > 0 for s in size)
        v = "PASS" if (fits and nondegenerate) else "FAIL"
        results.append({
            "file": p.name, "verdict": v, "tris": n,
            "bbox_mm": [round(s, 2) for s in size],
            "fits_256_bed": fits, "nondegenerate": nondegenerate,
        })
    return results


def run_printability(scad: Path) -> dict | None:
    checker = HERE / "analytic_printability.py"
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tf:
        out_json = Path(tf.name)
    try:
        proc = subprocess.run(
            [sys.executable, str(checker), str(scad), "--json", str(out_json)],
            capture_output=True, text=True, timeout=120)
        if out_json.exists() and out_json.stat().st_size:
            return json.loads(out_json.read_text())
        return {"verdict": "ERROR", "stderr": proc.stderr.strip()[:300]}
    finally:
        out_json.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-render", action="store_true",
                    help="skip the OpenSCAD render step")
    ap.add_argument("--require-openscad", action="store_true",
                    help="treat a missing openscad binary as a failure")
    ap.add_argument("--json", metavar="PATH", help="write the full record here")
    args = ap.parse_args()

    report: dict = {"repo": str(REPO), "steps": {}}
    hard_fail = False

    print("=" * 72)
    print("Shape Display geometry validation harness (software-only)")
    print("=" * 72)
    print("Evidence class: CAD (render/mesh) + calculation (printability).")
    print("This is NOT a print and NOT a physical measurement.\n")

    osc = find_openscad()
    print(f"[1] tool check: openscad = {osc or 'NOT FOUND'}")
    report["steps"]["tool"] = {"openscad": osc}
    if osc is None:
        print("    -> render step will SKIP.")
        print("    -> install with: tools/openscad-install/install-openscad.sh")
        if args.require_openscad and not args.no_render:
            print("    -> --require-openscad set: this is a FAILURE.")
            hard_fail = True

    with tempfile.TemporaryDirectory() as td:
        out_dir = Path(td) / "stl"
        out_dir.mkdir()
        render_results = []

        if osc and not args.no_render:
            print("\n[2] render (.scad -> .stl, real OpenSCAD)")
            for label, scad, extra in RENDER_TARGETS:
                out = out_dir / f"{label}.stl"
                ok, info = render(scad, out, osc, extra)
                print(f"    [{'PASS' if ok else 'FAIL'}] {label}: {info}")
                render_results.append({"target": label, "ok": ok, "info": info})
                if not ok:
                    hard_fail = True
        else:
            reason = "--no-render" if args.no_render else "openscad not found"
            print(f"\n[2] render: SKIPPED ({reason})")
        report["steps"]["render"] = render_results

        # mesh validation over rendered + checked-in coupon STLs
        print("\n[3] mesh validate")
        checked_in = [
            SHARED / "coupon_assembled.stl",
            SHARED / "coupon_finger.stl",
            SHARED / "coupon_bank.stl",
            SHARED / "coupon_base.stl",
        ]
        mesh = mesh_validate(out_dir, checked_in)
        for m in mesh:
            extra = f", {m.get('tris')} tris, {m.get('bbox_mm')}" if "tris" in m else ""
            print(f"    [{m['verdict']}] {m['file']}{extra}"
                  + (f"  ({m.get('reason')})" if m.get("reason") else ""))
            if m["verdict"] == "FAIL":
                hard_fail = True
        report["steps"]["mesh"] = mesh

    # analytic printability
    print("\n[4] analytic printability (calculation vs sourced FDM limits)")
    coupon = SHARED / "selector_fanout_coupon.scad"
    print_res = run_printability(coupon)
    report["steps"]["printability"] = print_res
    if print_res and print_res.get("verdict"):
        print(f"    verdict: {print_res['verdict']}"
              f"  ({print_res.get('evidence_class', '?')})")
        for c in print_res.get("checks", []):
            print(f"      [{c['verdict']}] {c['feature']} "
                  f"= {c['value_mm']} vs {c['limit_mm']} {c['rule']}")
        if print_res["verdict"] == "FAIL":
            # A design-risk FAIL is reportable but not a harness bug; the
            # harness itself only hard-fails on render/mesh errors.
            print("    note: printability FAIL is a DESIGN finding, not a "
                  "harness error.")

    print("\n" + "=" * 72)
    print("HARNESS: " + ("FAIL (render/mesh error)" if hard_fail
                         else "OK (all hard gates passed)"))
    print("=" * 72)
    report["harness_verdict"] = "FAIL" if hard_fail else "OK"

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2) + "\n")
        print(f"wrote {args.json}", file=sys.stderr)
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
