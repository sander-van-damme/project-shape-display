---
status: complete
builds-on: [A-014]
---

# Hydraulic series-gate addressing does not guarantee regional isolation

Defer A-014's two-series-gate embodiment: a closed upstream gate does not
prevent chamber motion when the downstream gate connects a previously charged
intermediate cavity. This is a new architecture screen, not a rejection of
hydraulic actuation. Require a pressure-history/compliance bound or a true
chamber-side coincidence valve before geometry refinement. No fabrication.

Input main `3e1bc0c`. Reproduce with
`python3 tools/curated-experiment-checks/E-060/hydraulic_bound.py`.
Evidence is conservation and a linear compliance model; no CFD, generated
contact geometry, sourced fluid properties, calibrated manufacturing priors
or physical measurements. All numerical material/process inputs below are
explicit sensitivity bounds, not claims about PLA or a particular fluid.

## Mechanism and discriminating history

Source → row gate → intermediate cavity → column gate → piston chamber.
An active row with column closed charges the intermediate cavity. Later, with
row closed and column open, that cavity equilibrates with an unchanged cell.
For piston area A, intermediate volume Vi, effective incremental bulk modulus
K and pressure difference Δp, the constant-load quasistatic piston receives
`ΔV = Vi Δp/K`, hence `Δx = Vi Δp/(KA)`. Δp can have either sign. Chamber
pressure remains set by the load in this limiting case. A piston physically
blocked at a hard stop instead experiences a pressure transient, not this
motion; seal stiction can delay release and cannot be credited as reliable
isolation. Reversing gate order moves the half-select problem to the other axis.

With gate closure followed by intermediate recharge, successive pulses can
pump volume into/out of a cell. N equal refreshed pulses produce NΔx while
stroke, load and pressure conditions permit. Opening an already equilibrated
cavity repeatedly without recharge does **not** accumulate this effect. The
80-pulse case below is an adversarial repeated-operation diagnostic, not a
claim that every full-map schedule causes 80 pulses per cell. A future scheduler
must enumerate the real shared pressure history of all half-selected cells.

A sealed full-stroke chamber under incremental force F has rigid-wall fluid
compression `δ = FH/(KA)`. Additional manifold/wall compliance worsens this;
effective K may represent linearized combined compliance, but nonlinear gas
compression, cavitation and seal friction need separate models. Constant K is
an approximation; the largest Δp/K here is 0.1. These equations are screening
models, not validated upper bounds on real drift. Extra dead volume in the
chamber worsens load deflection and is omitted optimistically.

## Deterministic screen and full-board consequences

Enumerate 2/3/4-mm bores, K=10/100/1000 MPa, Vi=1/10/100 mm³,
Δp=0.1/1 MPa: 54 combinations. No probability or yield follows from the grid.
Bores are trial internal dimensions, not demonstrated pitch-compatible seals.
At 3-mm bore, Vi=10 mm³, Δp=1 MPa, H=40 mm:

| Effective K | One half-select pulse | 80 refreshed pulses | Incremental 10-N sag |
|---|---:|---:|---:|
| 10 MPa | 0.14147 mm | 11.3177 mm | 5.65884 mm |
| 100 MPa | 0.01415 mm | 1.13177 mm | 0.56588 mm |
| 1000 MPa | 0.00141 mm | 0.11318 mm | 0.05659 mm |

There is no stage-02 numerical disturbance limit. An **illustrative**, unapproved
0.1-mm budget over 80 refreshed pulses requires Vi≤0.88357 mm³ at K=100 MPa.
A 0.1-mm drift budget over four hours instead permits only 0.04909 nL/s net
leakage per cell at this bore. These are acceptance-envelope diagnostics, not
measured leakage or new requirements. Common manifold compliance, pressure
bias and batch seals cause correlated drift; independent-cell sampling would
miss them. No distribution is assigned without evidence.

6,400 cylinders require 1.8096 L for a 40-mm full upward stroke at 3-mm bore;
strictly <30 s needs >3.6191 L/min before gate/readback/settling/reset overhead.
Ten newtons per piston implies 1.4147 MPa chamber pressure and 85.33 W ideal
average lifting power at 30 s. This is an optional sustained-load scenario,
not a requirement to lift the stationary 10-N comparator load everywhere.
Fluid volume does not include manifolds, reservoir margin or packaging. Gates,
seals, supply/return, reader and recovery remain uncosted. Cell-level sealing
burden and pressure containment preclude calling this a cheap architecture.

## Decision and self-review

The relevant new failure is intermediate-volume charge transfer despite a
logically closed series path. Stop treating row/column address arithmetic as
isolation evidence. Retain A-014 as an exploratory family; next useful result
would be an explicit chamber-side coincidence valve or mechanical-lock hybrid
with support continuity, reset and full-system cost, not tighter fluid numbers.
A credible low-compliance bounded-pressure implementation can also reopen the
series-gate embodiment. A physical calibration is premature without that design.

Executable self-review checks SI volume conservation, force/compression identity,
zero-volume/zero-pressure limits, sign reversal, linear scaling and independent
litres-per-half-minute flow conversion. A unit conversion error found during
self-review was corrected before integration. No independent review claimed.
Finite motion/time integration, mesh convergence and yield estimates are not
applicable to this algebraic screen; unmodeled dynamics remain evidence limits.
