# DND-115: CAD-design + validate the A1 state-encoding shutter

## What changed

[DND-114](/DND/issues/DND-114) gave A1 a CAD-validated **common-height read
target** (CH-A frame-fixed vane, `Δz = 0`), but left it **state-invariant**: a
plain post returns the same light in both latch states, so the read could not
actually distinguish up from down — and A1's readback/retry advantage (its whole
reliability case) stayed unproven. DND-115 dimensions and CAD-validates the
**state-encoding shutter** that closes this, the last agent-reachable read-axis
artifact.

- **Mechanism (CAD).** A **matte-dark flap** on a **shutter crank** that shares
  the frame-fixed latch hinge axis with the toe arm. The crank has two hard-stop
  positions: **HIDDEN** (flap flat over the vane, plane normal +Z → the beam is
  blocked) and **VISIBLE** (flap edge-on, normal ≈ +X → the beam reaches the
  frame-fixed vane). The flap pivot **is** the hinge axis, placed directly over
  the vane, so a 90° crank swing moves the flap only ~2.87 mm laterally — inside
  the own lane. The flap is an **absorber** (ρ ≈ 0.05), so the reflective
  **target stays the frame-fixed vane top** (`Δz = 0`); only the *shadow* is
  state-dependent. No state-dependent target z is reintroduced.

- **Cell CAD** (`10-reliability-mask/scad/a1_binary_latch_cell.scad`):
  `shutter_crank()` + `shutter_flap(state)`, a `part="shutter"` printable
  selector, and shutter self-checks (vane gap, aperture clearance, neighbour
  envelope, own-column clearance, min feature, spot coverage).

- **Reader CAD** (`10-reliability-mask/scad/a1_reader_head.scad`): the flag-read
  standoff/aperture are revised to the DND-115 values (see below).

- **Model** (`10-reliability-mask/analysis/a1_writer_rate.py`): new
  `shutter_read_contrast()` (shadow fraction, on/off ratio, envelope clearances,
  absorber Δz) and `shutter_tolerance_mc()` (worst-case + 200k-draw Monte
  Carlo); `flag_read_contrast()` re-baselined; `OUTCOME_STATEMENT` updated.

- **Render** (`10-reliability-mask/analysis/render_a1_cad.py`): renders +
  mesh-validates the `shutter` part and **fails hard** if any shutter self-check
  does not pass.

- **Docs:** new ADR
  [`07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md`](https://github.com/sander-van-damme/project-shape-display/blob/main/07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md);
  the DND-114 ADR gets a "resolved by DND-115" note and a standoff-supersession
  note; README §4.2a / §4.7 / §6 / §9 / §10 and the evidence index updated from
  "residual" to "closed".

- **Gate/CI:** new
  [`falsifier_dnd115_checks.py`](https://github.com/sander-van-damme/project-shape-display/blob/main/07-evidence-and-decisions/falsifier_dnd115_checks.py)
  (9 attacks, default-deny, `--gate` exits 0), CI-wired as a hard gate. The
  DND-114 companion is re-baselined to the revised reader.

## Engineering question

Can the frame-fixed CH-A vane's return be made **unambiguously state-dependent**
at one fixed standoff, without reintroducing a state-dependent target z?

## Evidence produced

- Hidden state covers **100%** of the read spot; visible state **0%**.
- **On/off return ratio 7.72×** (gate 2×).
- Reflective target Δz = **0.000 mm**; absorber Δz = **0.55 mm** (inside ±1 mm DoF).
- Swept flap clears the neighbour body by **0.28 mm**, the own column by **3.41 mm**.
- Monte Carlo (200k draws): **zero failures** on every margin at realistic
  (±0.10 mm) frame pitch tolerance.

## Standoff revision (important)

The DND-114 **1.0 mm standoff / 0.60 mm aperture is infeasible** for a 0.44 mm
flap under printed placing tolerances — the aperture-clearance check fails in
~0.5 %, rising to ~32 % for a tight gap split (`shutter_tolerance_mc()`). DND-115
therefore adopts a **1.8 mm standoff / 0.44 mm aperture**: spot 1.405 mm, which
still clears the neighbour body by 0.353 mm and fits the flag Y-width. The
frame-fixed target and `Δz = 0` are unchanged — only the standoff distance moves.

## Verification run

| Gate | Result |
|---|---|
| `reliability_mask_checks.py` | **75/75 PASS** |
| `falsifier_dnd115_checks.py --gate` | **CLEAN 9/9** (new) |
| `falsifier_dnd114_checks.py --gate` | **CLEAN 7/7** (re-baselined) |
| `falsifier_dnd112_checks.py --gate` | **exit 0** |
| `falsifier_dnd104_checks.py` | **26/26 PASS** |
| `render_a1_cad.py` (OpenSCAD + trimesh) | column / latch / cradle / flag / **shutter (watertight, 1.55×1.60×2.75 mm)** / reader all pass |

## Assumptions / residual uncertainty

- **Assumption-class (unmeasured):** flap matte reflectance (0.05), standoff
  (1.8 mm) and aperture (0.44 mm), printed placing tolerances, all optical
  constants.
- **Measurement-only (DND-27):** flap/hinge wear across 6,400 cycles, as-printed
  snap force, as-built pitch over 406 mm.
- The shutter crank linkage is drawn schematic (shared hinge axis); the flap and
  its swept envelope are the validated quantities.

## Most informative next test

An independent Falsifier audit of the decisive DND-115 number (the 7.72× on/off
return ratio and the swept-envelope clearances) against the placed CAD, and — if
the Falsifier finds it clean — the DND-110 terminal gate can consider A1's
read/verify axis closed at CAD + calculation.

## Evidence class / governance

**CALCULATION + CAD only.** No print, no purchase, no measurement
([DND-27](/DND/issues/DND-27)). No board contact ([DND-32](/DND/issues/DND-32)).
`08-current-design/` and `09-low-cost-variant/` untouched. No direct pushes to
`main`.
