# DND-60 — S5-R complete printable fabrication package

## What changed

Closes the [DND-57](/DND/issues/DND-57) gap: `08-current-design/` was a machine
*definition*, not a *printable package*. This PR produces the board-usable
**printable S5-R package**, on the evidence classes [DND-27](/DND/issues/DND-27)
allows only: **CAD + sourced FDM limits + calculation; no print, no purchase, no
measurement**.

- **`08-current-design/fabrication/scad/s5r_parts_common.scad`** (new) — shared
  part constants (single source of truth; pinned to `s5r_register.py`).
- **`08-current-design/fabrication/scad/s5r_parts.scad`** (new) — **every
  distinct printed part** of S5-R (14 parts) with a `part=` selector: cell
  cartridge, rotor, drive pawl, keeper (DND-59 re-profile), detent leaf, rack
  strip, bank drive housing, reset comber, writer carriage, platen module, lift
  frame rail, guide bracket, solenoid mount, comber cam.
- **`08-current-design/fabrication/stl/`** (new) — 14 **real-OpenSCAD rendered,
  watertight, bed-fitting** STLs (CAD witnesses).
- **`08-current-design/fabrication/manifests/`** (new) — **print manifest**
  (qty / PLA / nozzle / layer / orientation / supports / sourced limit / est.
  mass+time) and **assembly manifest** (exploded ordering, fasteners, ratified
  **$404.60 delivered** BOM), plus the render record.
- **`08-current-design/fabrication/tools/`** (new) — `part_set.py`,
  `render_fab_parts.py`, `gen_manifests.py`, `fab_package_checks.py` (CI
  coherence gate C1–C6).
- **`08-current-design/README.md`** — new **§6a "How to print and build"** +
  DND-60 status update + measurement-only residue.
- **`tools/validate/analytic_printability.py`** — new `check_fab_parts` branch
  for the full part set; include-following `parse_scad_constants`.
- **`tools/validate/validate_geometry.py`** — renders the 14 fab parts.
- **`.github/workflows/ci.yml`** — new `fab-package` job (render + manifests +
  coherence + printability PASS).
- **`.github/open-pr-body.md`** — this body.

## Evidence

- Full-set printability: **PASS** (no FAIL, no RISK) against
  `tools/fdm-limits/fdm_process_limits.py`.
- Render: 14/14 parts **watertight + 256 mm bed fit** (real OpenSCAD 2023.09.11).
- Coherence gate: **C1–C6 PASS** (constants match the promoted model; quantities
  match the 80×80 / 3×3 layout).
- Existing engineering checks: unchanged and green.

## Honesty

- `cell_cartridge` / `platen_module` STLs are **reduced witness blocks** of a
  periodic tile (same precedent as `s5r_bank.scad`); the full footprint and cell
  count are carried analytically.
- Mass / print time are **estimates**, not a slicer preview.
- **No part has been printed or measured**; the board performs the first
  physical print. Measurement-only residue (as-printed μ, leaf creep, per-set
  reliability, loaded torque-speed) is named in
  `08-current-design/fabrication/README.md` §5.
