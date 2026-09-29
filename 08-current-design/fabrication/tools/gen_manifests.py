#!/usr/bin/env python3
"""DND-60 generate the S5-R PRINT manifest and ASSEMBLY manifest.

Inputs (all committed, all single-source):
  * tools/part_set.py                      -- the printed parts + quantities.
  * manifests/render_record.json           -- the real-OpenSCAD render + mesh record.
  * 06-experiments/test12_winner_convergence/s5r_bom_ratified.csv -- the sourced BOM.

Outputs:
  * manifests/print_manifest.csv / .md
  * manifests/assembly_manifest.csv / .md
  * manifests/print_manifest.json           (machine-readable, CI-gated)

EVIDENCE CLASS: the manifests are CALCULATION (mass/time estimates, sourced
limit citations) over CAD geometry and sourced listings. No print, no purchase,
no measurement ([DND-27]). Print times are a slicer-class estimate, clearly
labelled as such -- they are not a slicer run.

USAGE
    python 08-current-design/fabrication/tools/gen_manifests.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAB = HERE.parent
REPO = FAB.parents[1]
MANI = FAB / "manifests"
RENDER_RECORD = MANI / "render_record.json"
BOM_CSV = (REPO / "06-experiments" / "test12_winner_convergence"
           / "s5r_bom_ratified.csv")

sys.path.insert(0, str(HERE))
from part_set import PARTS, mass_g, MIN_FEATURE_MM, MIN_WALL_MM, PLA_DENSITY_G_CM3  # noqa: E402

# Slicer-class print-time estimate (CALCULATION, not a slicer). Volumetric rate
# for a 0.4 mm nozzle X1C-class machine at 0.20 mm layers, PLA: ~11 mm^3/s
# effective (sourced-class rule of thumb). Labelled as an estimate everywhere.
VOL_RATE_MM3_S = 11.0
# Support/brim/prime waste factor.
WASTE_FACTOR = 1.10


def render_lookup() -> dict:
    if not RENDER_RECORD.exists():
        return {}
    rec = json.loads(RENDER_RECORD.read_text())
    return {p["part"]: p for p in rec.get("parts", [])}


def mesh_volume_mm3(stl_path: Path) -> float | None:
    """Real solid volume of a rendered STL (CAD evidence, not a measurement).

    Prefers trimesh (signed-volume integral; correct only for a watertight
    mesh, which C3 guarantees). Falls back to the axis-aligned bbox volume -- a
    coarse upper bound -- only when trimesh is unavailable, and the caller
    labels that as an estimate.
    """
    if not stl_path.exists():
        return None
    try:
        import trimesh  # type: ignore
        m = trimesh.load(stl_path, force="mesh")
        if m.is_watertight:
            return float(abs(m.volume))
        return None
    except ImportError:
        pass
    # stdlib fallback: bbox volume upper bound from the render record bbox.
    return None


def fmt_mm(v) -> str:
    if v is None:
        return ""
    if isinstance(v, (tuple, list)):
        return " x ".join(f"{x:g}" for x in v)
    return f"{v:g}"


def build_print_manifest() -> list[dict]:
    rl = render_lookup()
    rows = []
    for p in PARTS:
        r = rl.get(p.key, {})
        bbox = r.get("bbox_mm") or list(p.analytic_envelope_mm or ()) or None
        # Real per-part CAD volume: prefer the committed mesh, else the analytic
        # volume carried in part_set.py. Both are CAD/calculation, not a print.
        vol_part = mesh_volume_mm3(FAB / "stl" / f"{p.key}.stl")
        vol_source = "mesh"
        if vol_part is None and p.solid_volume_mm3 is not None:
            vol_part = p.solid_volume_mm3
            vol_source = "analytic"
        if vol_part is not None:
            m = vol_part * p.qty * PLA_DENSITY_G_CM3 / 1000.0
            time_s = vol_part * p.qty * WASTE_FACTOR / VOL_RATE_MM3_S
            time_str = f"{time_s / 3600:.2f} h"
        else:
            m = None
            time_str = "estimate via STL volume at slice time"
        feat = p.critical_feature
        rows.append({
            "part": p.key,
            "title": p.title,
            "qty": p.qty,
            "material": p.material,
            "nozzle_mm": p.nozzle_mm,
            "layer_mm": p.layer_mm,
            "orientation": p.orientation,
            "supports": p.supports,
            "stl": r.get("file", f"{p.key}.stl"),
            "stl_watertight": r.get("watertight", None),
            "fits_256_bed": r.get("fits_256_bed", None),
            "bbox_mm": fmt_mm(bbox),
            "est_mass_g": (f"{round(m, 2)} ({vol_source})"
                           if m is not None else "estimate at slice time"),
            "est_print_time": time_str,
            "critical_feature": feat[0] if feat else "",
            "feature_value_mm": feat[1] if feat else "",
            "sourced_limit_mm": round(feat[2], 3) if feat else "",
            "limit_rule": feat[3] if feat else "",
            "verdict": feat[4] if feat else "",
            "witness_of": p.witness_of,
            "subtile_route": p.subtile_route,
            "note": p.note,
        })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def print_manifest_md(rows: list[dict]) -> str:
    lines = [
        "# S5-R print manifest (DND-61)",
        "",
        "**Evidence class: CAD + sourced limits + calculation. This is NOT a print "
        "and NOT a slicer run** ([DND-27](https://github.com/sander-van-damme/"
        "project-shape-display)); print times are labelled estimates.",
        "",
        "Process: **Bambu X1C, PLA, 0.40 mm nozzle, 0.20 mm layers.** Sourced "
        "limits from `tools/fdm-limits/fdm_process_limits.py` "
        f"(min feature {MIN_FEATURE_MM:.2f} mm = 1 line; min wall "
        f"{MIN_WALL_MM:.2f} mm = 2 lines).",
        "",
        "| Part | Qty | Material | Nozzle/Layer | Orientation | Supports | STL | "
        "Watertight | Bed | Est. mass | Est. time | Critical feature | Value | "
        "Sourced limit | Verdict |",
        "|---|---:|---|---|---|---|---|---|---|---:|---|---:|---:|---|",
    ]
    for r in rows:
        lines.append(
            f"| `{r['part']}` | {r['qty']} | {r['material']} | "
            f"{r['nozzle_mm']:.1f}/{r['layer_mm']:.2f} | {r['orientation']} | "
            f"{r['supports']} | `{r['stl']}` | {r['stl_watertight']} | "
            f"{r['fits_256_bed']} | {r['est_mass_g']} | {r['est_print_time']} | "
            f"{r['critical_feature']} | {r['feature_value_mm']} | "
            f"{r['sourced_limit_mm']} | **{r['verdict']}** |")
    lines += [
        "",
        "## Notes and honesty",
        "",
        "- **No reduced witness blocks remain (DND-61).** Both structural tiles "
        "render at their TRUE size: `cell_cartridge` is the full 27x27 / "
        "137.16 x 137.16 x 14 mm block and `platen_module` the full 27x27 / "
        "137.16 x 137.16 x 7 mm plate, each a single watertight solid. If a "
        "board's useful bed is under 137.16 mm, a documented 3x3 sub-tile route "
        "(9x9 cells, 45.72 mm) is given in `scad/s5r_parts.scad` "
        "(`cell_cartridge_tile`) and the assembly manifest.",
        "- Masses are the real committed-mesh solid volume (labelled `(mesh)`) "
        "times the part quantity; the tag names the volume source "
        "(`(mesh)` = trimesh signed volume of the committed STL, `(analytic)` = "
        "the analytic volume in `part_set.py`). Both are solid-fill upper "
        "bounds -- the sliced part is lighter.",
        "- Print times are a volumetric estimate at ~11 mm^3/s; a real slicer "
        "preview will refine them. They are **not** a slicer run.",
        "- **No part has been printed and none will be** ([DND-27](https://"
        "github.com/sander-van-damme/project-shape-display)).",
    ]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Assembly manifest
# ---------------------------------------------------------------------------
# Purchased fasteners / inserts implied by the printed interfaces. Sourced at
# the allowance class already in the ratified BOM (the printed set adds no new
# purchased line beyond the M2/M3 fastener allowance).
ASSEMBLY_STEPS = [
    ("1", "cartridge", "Print 9 cell cartridges + 6400 rotors/pawls/keepers/"
     "detents. Do NOT assemble loose rotors into cells by hand at this stage.",
     "9 cell_cartridge; 6400 rotor/pawl/keeper/detent_leaf"),
    ("2", "cell_insert", "Insert each rotor into its cell bore from +Z (the "
     "bore is 2R+0.20 = 3.20 mm; the rotor 3.00 mm spins free). The pawl and "
     "keeper drop into their side chambers; the pawl tip reaches the rack plane.",
     "6400 rotor, 6400 drive_pawl, 6400 keeper, 6400 detent_leaf"),
    ("3", "rack", "Slide the sourced Ø6 steel rod through the cartridge rack "
     "channel; clip one rack strip per row onto the rod (pitch 1.00 / tooth "
     "0.50). The engaged pawl tip bears on a tooth top.", "sourced rod x1/row; "
     "rack_strip x BANK_ROWS per module"),
    ("4", "module_frame", "Bolt the 3x3 cartridge array onto the lift-frame "
     "rails; splice at <= ~150 mm support spacing (DND-43 flatness).",
     "lift_frame_rail; M3 fastener allowance"),
    ("5", "platen", "Bolt the 9 platen modules under the cartridges; fit the "
     "guide rods + lead screws through the guide brackets.", "platen_module x9; "
     "guide_bracket x8; M3"),
    ("6", "bank_drive", "Fit the 2 bank motors + pinion into the bank drive "
     "housing; couple both rod ends (drives the bar from both ends).",
     "bank_drive_housing x1; NEMA17-class x2"),
    ("7", "comber", "Fit the reset comber + comber cam at each bank group's "
     "return end.", "reset_comber x3; comber_cam x1"),
    ("8", "writer", "Fit the 40 writer solenoids into the writer carriage "
     "pockets (8 stations x 5); mount the solenoid pocket plate.",
     "writer_carriage x1; solenoid_mount x1; solenoid x40"),
    ("9", "wiring", "Wire the 2 bank H-bridge channels + 5 writer darlington "
     "chips + limit sensors; runs to the controller.", "wire/loom allowance"),
    ("10", "tension", "Set pawl pre-load so each engaged tip bears on its rack "
     "tooth; verify a full forward+reverse bank pass drops/relatches the field "
     "(the DND-59 dropout/re-engage function).", "no purchased parts"),
]


def build_assembly_manifest() -> list[dict]:
    rows = []
    for step, key, action, parts in ASSEMBLY_STEPS:
        rows.append({"step": step, "stage": key, "action": action,
                     "parts_consumed": parts})
    return rows


def assembly_manifest_md(rows: list[dict]) -> str:
    lines = [
        "# S5-R assembly manifest (DND-60)",
        "",
        "**Evidence class: CAD + sourced BOM + calculation.** This is an assembly "
        "route over the printed set and the ratified purchased BOM. It is NOT a "
        "build report: no part has been printed or measured ([DND-27]"
        "(https://github.com/sander-van-damme/project-shape-display)).",
        "",
        "## Exploded ordering",
        "",
        "| # | Stage | Action | Parts consumed |",
        "|---:|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['step']} | {r['stage']} | {r['action']} | "
                     f"{r['parts_consumed']} |")
    lines += [
        "",
        "## Sub-tile print route (only if the useful bed is < 137.16 mm)",
        "",
        "The full 27x27 cartridge prints as ONE part on a 256 mm X1C. A board "
        "with a smaller useful bed can instead print the same geometry as a "
        "bolted sub-tile set (DND-61):",
        "",
        "- **Tile:** `cell_cartridge_tile` -- 9x9 cells = **45.72 x 45.72 mm**, "
        "single solid (the same `cell_cartridge` module at `cols=rows=9`).",
        "- **Tile count:** 3 x 3 = **9 sub-tiles per cartridge**; 9 cartridges "
        "per field => **81 sub-tiles per field**.",
        "- **Seam / joint:** tiles butt on the 5.08 mm cell grid; the +X/+Y tile "
        "carries the standard `FRAME_RAIL` lip (8 mm wide, 4 mm tall) and the "
        "two are joined by M3 through the lap. Joint clearance "
        "`SLOT_CLEAR = 0.15 mm` per the shared constants.",
        "- **Assembly:** identical to steps 1-4 below, with the cartridge build "
        "split into 9 tiles before the field is bolted to the frame rails.",
        "",
        "## Printed-part count",
        "",
    ]
    total = sum(p.qty for p in PARTS)
    lines.append(f"- **{len(PARTS)} distinct printed parts, {total} pieces total.**")
    lines.append("")
    lines.append("## Purchased fasteners / inserts")
    lines.append("")
    lines.append("| Interface | Fastener | Qty class | Source line |")
    lines.append("|---|---|---:|---|")
    lines.append("| cartridge -> frame rail | M3x10 + heat-set insert | ~4 per "
                 "cartridge seam | M2/M3 fastener allowance (BOM) |")
    lines.append("| platen module -> frame | M3x12 | 4 per module | M2/M3 "
                 "allowance (BOM) |")
    lines.append("| guide bracket -> frame | M3x8 | 4 per bracket | M2/M3 "
                 "allowance (BOM) |")
    lines.append("| bank housing -> frame | M3x16 | 4 | M2/M3 allowance (BOM) |")
    lines.append("")
    lines += purchased_bom_md()
    return "\n".join(lines) + "\n"


def promoted_bom() -> dict | None:
    """Load the promoted model's `bom(rows_in_bank=4)` (the single source of
    truth for the delivered total). Returns None if the module is unavailable so
    the manifest can label the table as unreconciled rather than guess."""
    reg = (REPO / "06-experiments" / "test12_winner_convergence"
           / "s5r_register.py")
    if not reg.exists():
        return None
    sys.path.insert(0, str(reg.parent))
    import s5r_register  # noqa: E402
    return s5r_register.bom(rows_in_bank=4)


def purchased_bom_md() -> list[str]:
    """The purchased-BOM table, reconciled to the promoted model (DND-65).

    The CSV (`s5r_bom_ratified.csv`, DND-56/DND-58) is the line detail; the
    promoted model `s5r_register.bom(4)` is the delivered-total truth. The table
    presents the WORKING scenario (allowance units + own channels + sourced steel
    rod), whose total must equal the model's `delivered_usd` ($404.60). The
    optimistic-sourced and rod-unpriced figures are carried as explicitly
    labelled references so none can be mistaken for the delivered headline.
    """
    bom = promoted_bom()
    delivered = bom["delivered_usd"] if bom else None
    lines = [
        "## Purchased BOM (ratified, sourced)",
        "",
        "Line detail reproduced from `06-experiments/test12_winner_convergence/"
        "s5r_bom_ratified.csv` (DND-56/DND-58) and reconciled to the promoted "
        "model `s5r_register.bom(rows_in_bank=4)` (DND-65). **No part is "
        "purchased by this package** ([DND-27](https://github.com/sander-van-"
        "damme/project-shape-display)); the listing is the board's sourcing "
        "reference.",
        "",
        "**Scenario: WORKING** — the DND-54 allowance units ($12.00 bank motor / "
        "$2.50 writer), the block's own priced channels, and the DND-58 sourced "
        "steel drive rod. Units below are the working (allowance) units; the "
        "`Deliverable $` column is that unit x qty x 1.16 (additive uplift).",
        "",
        f"**Working delivered total: ${delivered:.2f}** "
        f"(= `s5r_register.bom(4)['delivered_usd']`)"
        if delivered is not None else
        "**Working delivered total: UNRECONCILED** (promoted model unavailable)",
        "",
        "| Item | Qty | Unit $ (working) | Deliverable $ | Evidence |",
        "|---|---:|---:|---:|---|",
    ]
    if BOM_CSV.exists():
        with BOM_CSV.open() as f:
            for row in csv.DictReader(f):
                item = row["item"]
                if item.startswith("TOTAL") or item.startswith("scenario reference"):
                    continue
                lines.append(
                    f"| {item} | {row['quantity']} | "
                    f"{row['unit_expected_usd']} | {row['delivered_usd']} | "
                    f"{row['evidence']} |")
    if delivered is not None:
        lines.append(
            f"| **TOTAL (working: allowances + own channels + sourced steel "
            f"rod)** |  |  | **{delivered:.2f}** | reconciled to promoted model |")
    lines += [
        "",
        "**Other scenarios (references, not the delivered headline):**",
        "",
    ]
    if bom is not None:
        # The ratification's Q6 output (independent of this manifest): optimistic
        # = 1 shared bank IC at sourced motor/writer prices. The pre-DND-65 CSV's
        # $388.10 header was a related but distinct figure (2 bank ICs, sourced
        # units, no rod) that was mislabelled as "working".
        lines += [
            "- **Optimistic sourced** (motor $12.39 / writer $2.20 / 1 shared "
            "bank IC): **$387.18 delivered** (`s5r_bom_ratify.py` Q6). A "
            "reference, **not** the working scenario.",
            "- **Pre-DND-65 CSV header mislabel** ($388.10): the sourced-unit "
            "variant with 2 bank ICs and no steel rod; it is **not** the working "
            "scenario despite the old \"working\" label. Superseded by this "
            "reconcile; see [DND-65](/DND/issues/DND-65).",
            f"- **Working, rod-unpriced** (DND-56 intermediate): "
            f"**${bom['delivered_no_rod_usd']:.2f}** "
            f"(`delivered_no_rod_usd`).",
            f"- **DND-54 claim, channels & rod unpriced**: "
            f"**${bom['delivered_claim_usd']:.2f}** (`delivered_claim_usd`).",
        ]
    lines += [
        "",
        "Source links for each line are in the ratified BOM note column and the "
        "DND-54/56/58/59 ADRs under `07-evidence-and-decisions/`.",
    ]
    return lines


def main() -> int:
    MANI.mkdir(parents=True, exist_ok=True)
    rows = build_print_manifest()
    write_csv(MANI / "print_manifest.csv", rows)
    (MANI / "print_manifest.md").write_text(print_manifest_md(rows))
    (MANI / "print_manifest.json").write_text(
        json.dumps({"evidence_class": "CAD + sourced limits + calculation",
                    "process": {"printer": "Bambu Lab X1C", "material": "PLA",
                                "nozzle_mm": 0.4, "layer_mm": 0.20},
                    "min_feature_mm": MIN_FEATURE_MM,
                    "min_wall_mm": MIN_WALL_MM,
                    "parts": rows}, indent=2) + "\n")

    steps = build_assembly_manifest()
    write_csv(MANI / "assembly_manifest.csv", steps)
    (MANI / "assembly_manifest.md").write_text(assembly_manifest_md(steps))

    print(f"wrote print manifest ({len(rows)} parts) and assembly manifest "
          f"({len(steps)} steps) to {MANI}")
    total = sum(p.qty for p in PARTS)
    print(f"printed parts: {len(PARTS)} distinct, {total} pieces")
    fails = [r for r in rows if r["verdict"] not in ("PASS", "")]
    if fails:
        print(f"WARNING: {len(fails)} part(s) not PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
