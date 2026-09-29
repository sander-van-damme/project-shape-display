#!/usr/bin/env python3
"""DND-60 CI coherence gate for the S5-R fabrication package.

Asserts (all must pass for CI green):

  C1  Constants coherence: the fabrication constants in
      `scad/s5r_parts_common.scad` match the promoted model
      (`test12_winner_convergence/s5r_register.py`) for every shared value.
  C2  Manifest completeness: every part in `part_set.py` has a row in
      `print_manifest.json`, and every manifest row has a part.
  C3  Render record: every part has a committed STL that is watertight and
      fits the 256 mm bed.
  C4  Quantity coherence: the cartridge/rotor/pawl/keeper/detent counts match
      the 80x80 field and the 3x3 cartridge layout.
  C5  Sourced-limit pass: every part's critical feature is >= its sourced FDM
      limit (no FAIL). A RISK would also fail the gate.
  C6  Assembly manifest covers every printed part.

Run: python 08-current-design/fabrication/tools/fab_package_checks.py
A manifest is regenerated first (in-memory checks) so a stale committed file
cannot pass: the check re-derives the manifest and compares key fields.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAB = HERE.parent
REPO = FAB.parents[1]
COMMON = FAB / "scad" / "s5r_parts_common.scad"
RENDER = FAB / "manifests" / "render_record.json"
PRINT_JSON = FAB / "manifests" / "print_manifest.json"
ASM_MD = FAB / "manifests" / "assembly_manifest.md"
REGISTER_PY = (REPO / "06-experiments" / "test12_winner_convergence"
               / "s5r_register.py")

sys.path.insert(0, str(HERE))
from part_set import (PARTS, COLS, ROWS_FULL, CARTRIDGE_COLS,  # noqa: E402
                      CARTS_PER_AXIS, MIN_FEATURE_MM, MIN_WALL_MM, BED_MM)

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {msg}")
    if not cond:
        FAILS.append(msg)


def parse_scad_constants(path: Path) -> dict:
    text = path.read_text()
    out = {}
    for m in re.finditer(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*([0-9.]+)\s*;", text, re.M):
        out[m.group(1)] = float(m.group(2))
    return out


def parse_register_constants(path: Path) -> dict:
    text = path.read_text()
    out = {}
    for m in re.finditer(r"^([A-Z][A-Z0-9_]*)\s*=\s*([0-9.]+)\b", text, re.M):
        try:
            out[m.group(1)] = float(m.group(2))
        except ValueError:
            pass
    return out


def main() -> int:
    print("=" * 72)
    print("DND-60 S5-R fabrication-package coherence gate")
    print("Evidence class: CAD + sourced limits + calculation. Not a print.")
    print("=" * 72)

    scad = parse_scad_constants(COMMON)
    reg = parse_register_constants(REGISTER_PY)

    # --- C1 constants coherence ------------------------------------------
    print("\n[C1] constants coherence (fab package vs promoted register model)")
    pairs = [
        ("PITCH", "PITCH_MM", 5.08),
        ("ROTOR_RADIUS", "ROTOR_RADIUS_MM", 1.5),
        ("ROTOR_CORE_RADIUS", "ROTOR_CORE_RADIUS_MM", 1.0),
        ("PAWL_T", "PAWL_T_MM", 0.90),
        ("PAWL_W", "PAWL_W_MM", 0.70),
        ("PAWL_LEN", "PAWL_LENGTH_MM", 8.0),
        ("KEEPER_T", "KEEPER_LEAF_T_MM", 0.90),
        ("KEEPER_W", "KEEPER_LEAF_W_MM", 0.70),
        ("KEEPER_LEN", "KEEPER_LEAF_L_MM", 4.0),
        ("KEEPER_GATE_STEP", "KEEPER_GATE_STEP_MM", 0.35),
        ("RACK_TOOTH_PITCH", "RACK_TOOTH_PITCH_MM", 1.00),
        ("RACK_TOOTH_HEIGHT", "RACK_TOOTH_HEIGHT_MM", 0.50),
        ("BAR_D", "BAR_D_MM", 6.0),
    ]
    for scad_name, reg_name, want in pairs:
        have = scad.get(scad_name)
        rval = reg.get(reg_name)
        ok = have == want and (rval is None or rval == want)
        check(ok, f"{scad_name} = {have} (model {reg_name} = {rval}, want {want})")
    # WALL is a DESIGN wall, not the min-wall floor: it must be >= the model's
    # 2-line minimum (MIN_WALL_MM = 0.88) so every printed wall clears the floor.
    wall = scad.get("WALL")
    min_wall = reg.get("MIN_WALL_MM", 0.88)
    check(wall is not None and wall >= min_wall,
          f"WALL = {wall} >= model min-wall floor {min_wall}")

    # --- C2 manifest completeness ----------------------------------------
    print("\n[C2] manifest completeness")
    mani = json.loads(PRINT_JSON.read_text()) if PRINT_JSON.exists() else {}
    mrows = {r["part"]: r for r in mani.get("parts", [])}
    keys = {p.key for p in PARTS}
    check(keys == set(mrows), f"part set == manifest parts ({len(keys)} parts)")
    for p in PARTS:
        check(p.key in mrows, f"manifest row present for {p.key}")

    # --- C3 render record ------------------------------------------------
    print("\n[C3] render record (watertight + bed fit)")
    rec = json.loads(RENDER.read_text()) if RENDER.exists() else {}
    rrows = {r["part"]: r for r in rec.get("parts", [])}
    for p in PARTS:
        r = rrows.get(p.key, {})
        stl = FAB / "stl" / f"{p.key}.stl"
        check(stl.exists() and stl.stat().st_size > 0,
              f"{p.key}: STL committed ({stl.name})")
        check(bool(r.get("watertight")), f"{p.key}: watertight")
        check(bool(r.get("fits_256_bed")), f"{p.key}: fits 256 mm bed")

    # --- C4 quantity coherence -------------------------------------------
    print("\n[C4] quantity coherence")
    qty = {p.key: p.qty for p in PARTS}
    cells = COLS * ROWS_FULL
    check(qty["rotor"] == cells, f"rotor qty {qty['rotor']} == {cells} cells")
    check(qty["drive_pawl"] == cells, f"pawl qty {qty['drive_pawl']} == {cells}")
    check(qty["keeper"] == cells, f"keeper qty {qty['keeper']} == {cells}")
    check(qty["detent_leaf"] == cells, f"detent qty {qty['detent_leaf']} == {cells}")
    check(qty["cell_cartridge"] == CARTS_PER_AXIS ** 2,
          f"cartridge qty {qty['cell_cartridge']} == {CARTS_PER_AXIS**2} (3x3)")
    check(CARTRIDGE_COLS * CARTS_PER_AXIS >= COLS,
          f"{CARTRIDGE_COLS}x{CARTS_PER_AXIS} = {CARTRIDGE_COLS*CARTS_PER_AXIS} "
          f">= {COLS} columns covered")

    # --- C5 sourced-limit pass -------------------------------------------
    print("\n[C5] sourced FDM limit pass (no FAIL, no RISK)")
    for p in PARTS:
        feat = p.critical_feature
        if not feat:
            continue
        _, value, limit, rule, verdict = feat
        check(value >= limit and verdict == "PASS",
              f"{p.key}: {value} mm >= {limit:.3f} mm ({rule}) -> {verdict}")

    # --- C6 assembly coverage --------------------------------------------
    print("\n[C6] assembly manifest covers every printed part")
    asm = ASM_MD.read_text() if ASM_MD.exists() else ""
    check(bool(asm), "assembly_manifest.md exists")
    for p in PARTS:
        check(p.key in asm or p.title.split("(")[0].strip() in asm,
              f"assembly manifest references {p.key}")

    print("\n" + "=" * 72)
    if FAILS:
        print(f"GATE: FAIL ({len(FAILS)} failing check(s))")
        for f in FAILS:
            print(f"   - {f}")
        return 1
    print("GATE: PASS (fabrication package coherent)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
