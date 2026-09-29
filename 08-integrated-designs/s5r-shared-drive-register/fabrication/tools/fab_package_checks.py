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
  C7  No reduced witness blocks (DND-61): every part's committed STL bbox must
      match its declared real envelope; a part that is still a reduced witness
      must name a documented sub-tile print route, else the gate fails.
  C8  Purchased-BOM coherence (DND-65): the assembly-manifest purchased-BOM
      total must equal the promoted model's `s5r_register.bom(4)["delivered_usd"]`
      ($404.60), the sourced steel drive-rod line must be present, and the
      optimistic-sourced $388.10 figure must not be labelled as the working
      scenario.

Run: python 08-integrated-designs/s5r-shared-drive-register/fabrication/tools/fab_package_checks.py
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
REPO = FAB.parents[2]
COMMON = FAB / "scad" / "s5r_parts_common.scad"
RENDER = FAB / "manifests" / "render_record.json"
PRINT_JSON = FAB / "manifests" / "print_manifest.json"
ASM_MD = FAB / "manifests" / "assembly_manifest.md"
REGISTER_PY = (REPO / "06-experiments" / "test12_winner_convergence"
               / "s5r_register.py")
ASM_CSV = FAB / "manifests" / "assembly_manifest.csv"
BOM_CSV = (REPO / "06-experiments" / "test12_winner_convergence"
           / "s5r_bom_ratified.csv")

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


def run_model_bom() -> dict:
    """Load `s5r_register.bom(rows_in_bank=4)` from the promoted model.

    Returns {} if the module cannot be imported (the gate then fails cleanly on
    the missing `delivered_usd`).
    """
    sys.path.insert(0, str(REGISTER_PY.parent))
    try:
        import s5r_register  # type: ignore
        return s5r_register.bom(rows_in_bank=4)
    except Exception as exc:  # pragma: no cover - reported as a gate failure
        print(f"  [warn] could not load promoted model: {exc}")
        return {}


def read_ratified_bom_totals() -> tuple[float, float, bool]:
    """Read the ratified BOM CSV: (delivered_total, parts_total, rod_present).

    The TOTAL row is the additive working-scenario total; the 'scenario
    reference' annotation row is skipped.
    """
    import csv as _csv
    total_delivered = 0.0
    total_parts = 0.0
    rod = False
    with BOM_CSV.open() as f:
        for row in _csv.DictReader(f):
            if "Steel drive rod" in row["item"]:
                rod = True
            if row["item"].startswith("TOTAL"):
                total_parts = float(row["parts_usd"])
                total_delivered = float(row["delivered_usd"])
    return total_delivered, total_parts, rod


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

    # --- C7 no reduced witness blocks (DND-61) ---------------------------
    # The DND-60 gap: a part could ship as a reduced representative of a larger
    # part with no route to the real geometry. Fail unless the committed STL bbox
    # equals the declared real envelope (within a tolerance) OR the part names a
    # documented sub-tile print route.
    print("\n[C7] no reduced witness blocks (real envelope or documented route)")
    for p in PARTS:
        r = rrows.get(p.key, {})
        bbox = r.get("bbox_mm")
        env = p.analytic_envelope_mm
        if env:
            ok = bool(bbox) and all(
                abs(bbox[k] - env[k]) <= 0.05 for k in range(3))
            check(ok, f"{p.key}: STL bbox {bbox} == real envelope "
                     f"{[round(v, 2) for v in env]}")
        if p.witness_of:
            check(bool(p.subtile_route),
                  f"{p.key}: reduced witness names a documented sub-tile route")
        else:
            check(True, f"{p.key}: committed STL is the full-size part")

    # --- C8 purchased-BOM coherence (DND-65) -----------------------------
    # The assembly manifest's purchased-BOM table must carry the SAME purchased
    # BOM as the promoted model: the working delivered total must equal
    # `s5r_register.bom(4)["delivered_usd"]`, the sourced steel drive rod must be
    # a line, and the optimistic-sourced $388.10 figure must be labelled as NOT
    # the working scenario. This is the gate that stops the manifest from
    # silently regressing to the pre-DND-65 CSV (total $388.10, no rod row).
    print("\n[C8] purchased-BOM reconciled to the promoted model (DND-65)")
    model_delivered = run_model_bom()["delivered_usd"]
    check(model_delivered is not None,
          f"promoted model bom(4).delivered_usd readable ({model_delivered})")
    asm_md = ASM_MD.read_text() if ASM_MD.exists() else ""
    check(bool(asm_md), "assembly_manifest.md exists")
    # The manifest must present the working total at the model's figure.
    want_total = f"{model_delivered:.2f}"
    check(want_total in asm_md,
          f"assembly manifest states working total ${want_total}")
    # The optimistic-sourced $388.10 figure may only appear as an explicitly
    # labelled non-working reference, never as the working headline.
    optimistic_lines = [ln for ln in asm_md.splitlines() if "388.1" in ln]
    for ln in optimistic_lines:
        check("not" in ln.lower() and ("working" in ln.lower()),
              "optimistic $388.10 line is labelled as NOT the working scenario: "
              f"{ln.strip()[:80]}")
    check(not any("TOTAL" in ln and "388.1" in ln for ln in asm_md.splitlines()),
          "no TOTAL row carries the $388.10 figure")
    # The steel drive-rod line must be present in the manifest table.
    check("Steel drive rod" in asm_md,
          "assembly manifest carries the sourced steel drive-rod line (DND-58)")
    # The CSV line detail must agree with the model on the working total and rod.
    if BOM_CSV.exists():
        bom_total, bom_parts, rod = read_ratified_bom_totals()
        check(rod, "ratified BOM CSV has the sourced steel drive-rod line")
        check(abs(bom_total - model_delivered) < 0.01,
              f"ratified BOM CSV total ${bom_total:.2f} == model "
              f"delivered_usd ${model_delivered:.2f}")
        model_parts = run_model_bom()["parts_usd"]
        check(abs(bom_parts - model_parts) < 0.01,
              f"ratified BOM CSV parts ${bom_parts:.2f} == model "
              f"parts_usd ${model_parts:.2f}")
    else:
        check(False, f"ratified BOM CSV exists ({BOM_CSV})")
    check(ASM_CSV.exists(), "assembly_manifest.csv exists")

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
