---
status: complete
builds-on: [E-028, DES-004, DES-005, ADR-007, E-016, E-014, E-012]
---

# E-029: independent falsification review of E-028

## Scope and verdict

This is a repository-only review of the E-028 loaded rotor/readback coupon
package. Evidence below is sourced text, CAD inspection, or calculation. No
physical test, supplier confirmation, or hardware-performance result exists.

**Verdict: blocked for fabrication handoff.** The article dimensions can be
used as a candidate analytical baseline, but the package is not yet a
falsifiable implementation of its stated gates. Minimum corrections are
required before a fabricator can be asked to produce a comparable coupon.

## Reproducible decisive checks

### 1. The 10,000-transition schedule is not a transition schedule — FAIL

E-028 says that for transition index `k`, cell `(k mod 25)` receives state
`(k mod 5)`. Since `k mod 25` fixes `k mod 5` for each cell, each cell is
assigned one state for all 400 appearances:

```text
cell 0 -> state 0 (400 times), cell 1 -> state 1 (400 times), ...,
cell 24 -> state 4 (400 times)
```

The proposed reverse pass similarly assigns each cell one complementary
state. Thus the schedule has at most an initial move to a state followed by
repeated same-state commands; it does not exercise all 20 directed stop
changes per rotor, or balanced motion across the five stops. The repository
geometry script's `logical_smoke()` is also only an ideal state assignment and
cannot detect this defect.

**Required correction:** define a deterministic schedule whose emitted record
contains `(cell, from_state, to_state)` and prove by a small checker that all
20 directed pairs per witness cell occur, with declared counts and no
same-state records counted as transitions. The exact 10,000 records must be
generated from that schedule and checked before fabrication handoff.

### 2. Claimed hard stops/detents are absent from the coupon CAD — FAIL

`des004_rotor_coupon_5x5.scad` defines a circular rotor, bore, and integral
vane. It does not define five stop lands, detent pockets, a follower, a
return element, or a hard-stop datum. The frame is only a plate with circular
pockets. Therefore the 0/10/20/30/40 mm levels and 22.5-degree stops in E-028
are interface claims, not geometry in the source article. A writer cannot
reach or return to a reproducible stop in this CAD definition.

**Required correction:** either add the actual stop/detent/follower geometry
to the frozen coupon CAD, or explicitly identify the external fixture that
provides those functions and include its datums, travel, clearance, force,
and return path in the configuration and drawing. A prose stop count is not
enough for fabrication equivalence.

### 3. Load path and writer/reader assemblies are not defined — BLOCKED

The SCAD `assembly()` contains only the frame and rotors. The writer, reader,
axle, retainer, and load fixture are separate sample solids or prose values;
there is no assembled datum or collision/engagement geometry. E-028's
`stack = 3 + 3 + 2*1 = 8 mm` calculation assumes two 1 mm retainers, but no
retainers are present in the CAD or article bill of definition. The 10 mm pin
therefore has a calculated 2 mm margin only against an unmodelled stack.

The 3.27 N centre-cell load has no force application area, direction, contact
height, fixture stiffness, or reaction path. “Force instrument active” does
not make load transfer reproducible. Likewise, a 1.80 mm reader standoff is a
nominal number, not a defined target-to-aperture datum: the reader sample has
no coded target, registration feature, optical model, or neighbour occlusion
definition.

**Required correction:** freeze an assembly/fixture drawing or explicit CAD
subassemblies for axle retainers, writer, reader target, and load application,
including coordinate datums and tolerance stack. The load gate remains
blocked until the force trace is tied to that defined path.

### 4. Acceptance margins are not operationally falsifiable — BLOCKED

The gates require `reader_margin_mm >= 0.20` and writer clearance of at least
0.20 mm in both axes, but E-028 does not define how either quantity is
computed. Reader “margin” could mean aperture overlap, optical contrast,
registration error, or an instrument-specific confidence value; these are not
interchangeable. Writer clearance has no measurement planes or pose datum.
The source geometry script reports nominal aperture width difference and
nominal writer pocket clearances, but does not calculate reader discrimination
or writer engagement force.

**Required correction:** define each margin mathematically, state the measured
surfaces/coordinates and uncertainty, and include a deterministic result
checker that rejects missing or inferred values. Preserve the existing
physical-only boundary: CAD overlap is not reader discrimination.

### 5. Boundary and neighbour evidence is underspecified — BLOCKED

E-028 calls the four corners “edge/corner witness cells” but only explicitly
loads C3. It does not state which untouched neighbours are loaded, their
preload magnitude, or the sensor datum/uncertainty for peak and residual
displacement. The acceptance row says “every loaded directed transition” but
the run sheet only says edge/corner tests are “unloaded but mechanically
coupled,” which cannot falsify disturbance into a loaded neighbour.

**Required correction:** name the target and each untouched loaded neighbour,
fixture load and direction, sensor locations, resolution/uncertainty, and the
exact transition subset. A zero/absent trace must be rejection, not a pass.

## Gate disposition

| Gate | Disposition | Reason |
|---|---|---|
| load transfer/3.27 N | blocked | no reproducible load path or fixture datum |
| stop/return | fail as defined | stop/detent geometry absent from source CAD |
| writer engagement | blocked | separate sample only; no assembled stroke/force/pose definition |
| reader standoff/discrimination | blocked | target, optical margin definition, registration and occlusion absent |
| neighbour isolation | blocked | boundary load/sensor protocol does not exercise loaded neighbours |
| transition count | fail | proposed 10,000 schedule repeats fixed states per cell |
| evidence capture | blocked | raw-log schema lacks defined fixture/configuration and margin semantics |

The nominal arithmetic that remains reproducible is limited to 25.40 mm field
span, 7.30 mm nominal frame margin per side, 0.70 mm pocket-to-body radial
allowance, 0.40 mm nominal bore clearance, and 8.00 mm assumed pin stack.
The latter is not a validated assembly result. The existing tolerance screen
also reports 0.0546 mm worst-case vane margin; it does not establish process
capability or assembly success.

## Minimum release corrections and next owner

The Design Engineer owning E-028/LAB-107 must:

1. correct and machine-check the balanced `(cell, from, to)` transition
   schedule;
2. freeze stop/detent and writer geometry, or freeze the external fixture
   drawing that supplies them;
3. add the reader target/registration and load/retainer assembly datums and
   tolerance stack;
4. define measurable writer and reader margins, plus loaded-neighbour
   fixtures and sensor evidence; and
5. rerun `./repo check` and the relevant CAD/contract checks, retaining this
   adverse review as a prerequisite record.

Until those corrections exist, do not fabricate, procure, promote DES-004 or
DES-005, or call the E-028 package analytically ready. The next action is a
document/CAD repair by that owner, followed by a fresh independent review;
there is no physical-testing result to close this issue.
status: active
builds-on: [E-012]
---
