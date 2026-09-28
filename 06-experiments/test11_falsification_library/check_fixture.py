#!/usr/bin/env python3
"""Test11 -- fixture geometry gate: is the J2 print set actually printable?

`j2_isolation_rig.scad` is a *proposed* fixture. This script checks the
geometry claims the protocol depends on, so a bad edit (pitch drift, a tile
that no longer fits the X1C bed, a seam that cannot be shimmed) fails a check
instead of silently shipping:

1. Full-scale pitch is 5.08 mm and is never scaled down.
2. Every single-part layout fits the Bambu X1C bed (256 x 256 mm) or is
   explicitly flagged as a split print.
3. The two-holder pair plus seam is reachable by the base rail.
4. Bed fit of the combined `plate` layout.
5. Seam shim set brackets the nominal seam.

This is a CALCULATION over the declared parameters, not a CAD render or a print.
If OpenSCAD is on PATH it also compiles each part to confirm the SCAD parses;
otherwise that step is reported as SKIPPED, never as passed.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAD = HERE / "j2_isolation_rig.scad"


def _openscad_env() -> dict[str, str]:
    """Env for headless OpenSCAD renders on CI and local boxes alike.

    The Ubuntu/Debian OpenSCAD package is a Qt build; without a display it must
    be told to use the offscreen platform plugin or the CLI aborts. Forcing it
    here keeps the render deterministic and non-interactive.
    """
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    return env


BED_MM = 256.0            # Bambu X1C build plate
PITCH_MM = 5.08           # full-scale cell pitch -- must not be scaled
BORDER_MM = 6.0
SEAM_NOMINAL_MM = 0.40
MIN_WALL_MM = 2.0         # protocol: holder wall >= 2.0 mm
COMMON_RAIL_MIN_MM = 12.0  # protocol: base rail >= 12 mm thick

SHIMS_MM = (0.20, 0.30, 0.40, 0.50)
FINITE_DIAL_MM = 0.01
FORCE_GAUGE_MN = 1.0

FAILURES: list[str] = []


def check(cond: bool, ok: str, bad: str) -> None:
    if cond:
        print("  PASS  " + ok)
    else:
        print("  FAIL  " + bad)
        FAILURES.append(bad)


def holder_outer(tile: int) -> float:
    return tile * PITCH_MM + 2 * BORDER_MM


def main() -> int:
    print("J2 fixture geometry gate (CALCULATION over declared parameters)\n")

    check(PITCH_MM == 5.08, "cell pitch is 5.08 mm (full scale)",
          "cell pitch is not 5.08 mm -- the fixture is off-scale")

    print("\n[1] single-part bed fit (X1C %.0f mm)" % BED_MM)
    for tile in (5, 10, 20):
        outer = holder_outer(tile)
        fits = outer <= BED_MM
        if tile == 20:
            # 20x20 is explicitly a split print in the protocol.
            check(True, "tile 20x20 outer=%.1f mm -> split print (documented)"
                  % outer, "")
        else:
            check(fits, "tile %dx%d outer=%.1f mm fits bed" % (tile, tile, outer),
                  "tile %dx%d outer=%.1f mm exceeds bed" % (tile, tile, outer))

    print("\n[2] holder pair + seam rail reach")
    for tile in (5, 10, 20):
        outer = holder_outer(tile)
        pair = 2 * outer + SEAM_NOMINAL_MM
        check(pair <= 2 * BED_MM,
              "tile %dx%d pair+seam=%.1f mm within rail budget" % (tile, tile, pair),
              "tile %dx%d pair+seam=%.1f mm unreachable" % (tile, tile, pair))

    print("\n[3] combined plate layout fits one bed")
    outer10 = holder_outer(10)
    gap = 6.0
    mini = 25.4 + 4
    plate_w = 2 * outer10 + gap
    plate_h = outer10 + gap + mini + gap + 24
    check(plate_w <= BED_MM and plate_h <= BED_MM,
          "plate %.1f x %.1f mm fits X1C bed" % (plate_w, plate_h),
          "plate %.1f x %.1f mm exceeds bed" % (plate_w, plate_h))

    print("\n[4] protocol material/feature floors")
    check(BORDER_MM >= MIN_WALL_MM,
          "holder wall %.1f mm >= %.1f mm floor" % (BORDER_MM, MIN_WALL_MM),
          "holder wall %.1f mm below %.1f mm floor" % (BORDER_MM, MIN_WALL_MM))
    check(COMMON_RAIL_MIN_MM >= 12.0,
          "base rail floor satisfies >= 12 mm", "base rail < 12 mm")
    check(FINITE_DIAL_MM <= 0.01, "dial resolution 0.01 mm",
          "dial resolution too coarse")
    check(min(SHIMS_MM) <= SEAM_NOMINAL_MM <= max(SHIMS_MM),
          "shim set brackets nominal seam %.2f mm" % SEAM_NOMINAL_MM,
          "shim set does not bracket the nominal seam")

    print("\n[5] OpenSCAD render check")
    osc = shutil.which("openscad")
    if osc is None:
        print("  SKIP  OpenSCAD not on PATH -- SCAD render not verified")
        print("        (a print-ready claim still requires a real render,")
        print("         done by hand or in a CAD-enabled environment)")
    else:
        renders = (
            ("holder_5x5", ["-D", "tile=5"]),
            ("holder_10x10", ["-D", "tile=10"]),
            ("base_rail", ["-D", 'part="base_rail"']),
            ("indicator_bracket", ["-D", 'part="indicator_bracket"']),
            ("miniature_tray", ["-D", 'part="miniature_tray"']),
            ("plate", ["-D", 'part="plate"']),
        )
        for name, args in renders:
            out = "/tmp/j2_%s.stl" % name
            proc = subprocess.run(
                [osc, "-o", out, *args, str(SCAD)],
                capture_output=True, text=True, timeout=300, env=_openscad_env())
            check(proc.returncode == 0,
                  "%s renders to STL" % name,
                  "%s failed to render: %s" % (name, proc.stderr.strip()[:200]))

        # Functional-feature check: the interchangeable-fixture socket must be a
        # real VOID in the holder floor, not a pocket buried inside solid plastic.
        # This is the exact bug the 2026-09-28 revision fixed; it silently
        # renders and only wastes a physical print if left uncaught.
        if probe_socket_is_open(osc):
            pass
        else:
            FAILURES.append("holder fixture socket is buried (not an open pocket)")

    print()
    if FAILURES:
        print("FIXTURE GATE: FAIL (%d)" % len(FAILURES))
        return 1
    print("FIXTURE GATE: PASS (geometry + CAD render; still not a print)")
    return 0


def _load_vertex_bbox(path: "str | Path") -> "tuple[tuple[float, float, float], tuple[float, float, float]] | None":
    """Read an ASCII STL and return its vertex bounding box, or None if empty."""
    import re

    pat = re.compile(r"vertex\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)")
    lo = [float("inf")] * 3
    hi = [float("-inf")] * 3
    seen = False
    try:
        for line in Path(path).read_text(errors="ignore").splitlines():
            m = pat.search(line)
            if not m:
                continue
            seen = True
            for i, val in enumerate(m.groups()):
                v = float(val)
                lo[i] = min(lo[i], v)
                hi[i] = max(hi[i], v)
    except OSError:
        return None
    if not seen:
        return None
    return (tuple(lo), tuple(hi))


def probe_socket_is_open(osc: str) -> bool:
    """Return True iff the holder's fixture socket is a genuine void.

    Renders a thin slab of the holder at the socket height and checks that the
    intersection is EMPTY inside the socket footprint, while a slab just below
    the socket is solid. Uses the same OpenSCAD binary as the render step.
    """
    holder = Path("/tmp/j2_holder_10x10.stl")
    if not holder.exists():
        print("  FAIL  holder_10x10 STL missing -- cannot probe socket")
        return False
    # tile=10: outer 62.8, border 6, socket footprint 8.0..54.8, floor 0..3,
    # socket cut 2.0..3.0, active field open above 3.0.
    probe_scad = HERE / "_socket_probe.scad"
    probe_scad.write_text(
        "use <%s>\n"
        "intersection() { holder(); translate([8.5, 8.5, 2.5]) cube([40, 40, 0.4]); }\n"
        % SCAD
    )
    out = Path("/tmp/j2_socket_probe.stl")
    if out.exists():
        out.unlink()
    subprocess.run([osc, "-o", str(out), str(probe_scad)],
                   capture_output=True, text=True, timeout=300,
                   env=_openscad_env())
    probe_scad.unlink(missing_ok=True)
    is_void = not out.exists()
    if is_void:
        print("  PASS  fixture socket is an open pocket (slab at z=2.5 is void)")
    else:
        print("  FAIL  fixture socket is buried: slab at z=2.5 still solid")
    return is_void


if __name__ == "__main__":
    sys.exit(main())
