---
status: open
builds-on: [E-006, E-007, E-008, DES-003, Q-005]
---

# E-009: Coupon-B stiffness and regional-coupling protocol

## Purpose and scope

This is a bounded, pre-physical-test protocol for deciding whether the
`DES-003` baseline can satisfy the proposed **0.10 mm peak motion of an
untouched loaded neighbour** during 5×5, 10×10, and 20×20 regional updates,
without A-004 couplers. It does not redesign DES-003 and does not repeat the
E-006 sensitivity calculation.

Evidence in this record is either calculated or CAD-derived. No print,
purchase, material test, FEA, or physical validation has been performed.

## Coupon and boundary condition

Use `08-integrated-designs/DES-003-reliability-first/scad/a1_coupon_b_5x5.scad`
as the 5×5 CAD fixture. It is a 40 mm square tile with the existing A1 cells
at 5.08 mm pitch. The centre cell is the untouched-neighbour station and
receives the design-calculated 3.27 N service load plus the representative
miniature mass. The surrounding cells are the update region. Do not infer
stiffness from the 3.27 N load alone: stiffness is an output of the same
load/displacement trace.

For 10×10 and 20×20, retain the same cell pitch, load station, support
interface, actuator motion, and measurement reference. Use a tiled or
extended coupon fixture with the same local boundary detail; the larger cases
are regional boundary sweeps, not a claim that the existing 40 mm CAD tile is
large enough. Record the actual fixture extent and support condition.

At each size, run the same sequence:

1. Establish zero and record the loaded untouched neighbour without an update.
2. Apply the normal DES-003 update trajectory to the selected region, with no
   A-004 coupler or intentional isolation feature.
3. Capture vertical and lateral displacement of the untouched station at a
   rate sufficient to resolve the motion peak and after-settle residual.
4. Repeat for both update directions and the worst boundary orientation found
   in the first pass. Keep the fixture, load, trajectory, and reference frame
   unchanged between sizes.

The protocol is executable only when the measurement/logger setup, fixture
support condition, trajectory, and load mass are recorded. If any is missing,
the result is **unresolved**, not a pass.

## Variables and calculations

For each run, report:

- `d_peak_mm`: maximum absolute neighbour displacement during the update;
- `d_residual_mm`: displacement after the defined settle interval;
- `F_service_N = 3.27` (design-calculated input);
- `n_boundary = 4 × (side − 1)` for the square updated region;
- `alpha_eff = F_transferred / (F_service × n_boundary)` when transferred
  force is available from an instrumented trace;
- `k_eff_N_per_mm = F_transferred / d_peak_mm` when the displacement is
  non-zero and the force path is identified.

The cheapest pre-test screening bound uses the E-006 sensitivity assumption
`alpha_assumed` per boundary cell:

```text
F_equiv = F_service × n_boundary × alpha_assumed
k_required = F_equiv / 0.10 mm
alpha_max(k) = k × 0.10 mm / (F_service × n_boundary)
```

These are calculated sensitivities, not measured properties. The reproducible
check is:

```text
python3 08-integrated-designs/DES-003-reliability-first/analysis/coupon_b_gate.py
```

It prints the 1%, 5%, and 10% sensitivity rows and the maximum allowable
coupling at candidate stiffnesses 10, 32.7, and 50 N/mm. Candidate stiffness
values are deliberately labels for sensitivity only.

## Pre-test decision gate

The analytical check alone cannot promote DES-003. Before any physical work,
use these dispositions:

- **Reject/falsify regional claim:** a justified CAD/FEA model or later trace
  predicts `d_peak_mm > 0.10` mm for any required size, or requires an
  explicitly bounded stiffness/coupling combination that the design cannot
  provide.
- **Promote to physical coupon test:** all three cases have a reproducible,
  geometry/material-justified bound with `d_peak_mm ≤ 0.10` mm, and the model
  includes support compliance, actuator trajectory, contact/clearance, and
  worst boundary orientation. This is only promotion to a test; it is not
  product qualification.
- **Leave unresolved:** any stiffness, coupling, support condition, load path,
  or trajectory is assumed or omitted; or any required case is not modelled.

For eventual coupon evidence, pass requires both `d_peak_mm ≤ 0.10 mm` and
`|d_residual_mm| ≤ 0.10 mm` for every required run, with no miniature tip-over,
hinge stall, or fracture. A single failed required run fails that regional
case. These are proposed test gates derived from Q-005, not established
product limits.

## Current calculated disposition

The existing E-006 model gives, at 5% assumed coupling, required stiffness of
26.16, 58.86, and 124.26 N/mm for 5×5, 10×10, and 20×20 respectively. At 10%
it gives 52.32, 117.72, and 248.52 N/mm. Therefore the present evidence is
**NOT FALSIFIED, OPEN, and not qualified**. It is insufficient to promote
DES-003: effective coupling, support stiffness, trajectory, and residual
motion remain unresolved. The next concrete action is to freeze the fixture
and logger definition above, then run the same coupon sequence when physical
testing is authorized; alternatively, produce a validated FEA model covering
the same boundary conditions.

