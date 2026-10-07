---
status: candidate
builds-on: [A-001, A-002, A-003, A-004, A-005, A-006, A-007, A-010, A-011, DES-006, Q-005, Q-010, Q-011, E-005, E-007, E-010, E-015, E-017, E-041, E-047, E-048, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006, ADR-007, ADR-008]
---

# A-012: Q-011 stiffness escape-route comparison

## Purpose and boundary

This is an architecture screen for the **DES-006/Q-011 full-scale stiffness
failure**, not a design release or a switch decision. A-011 is a historical comparison boundary, not a required architecture. These routes explore load paths within that comparison; they do not cover the broader addressing and state-storage search. Enforce regional updates and the stage-02 purchased-cost ceiling (> $500 unacceptable). All numbers below are calculations or explicit
assumptions; none is physical validation.

## Three materially different escape routes

### R1 — segmented load-island cartridges (screened out)

Replace the continuous 406.4 mm load path and shaft with 16 independently
supported 20x20-cell structural islands. Each island has a local hard-stop
frame and A-011 mask cartridge; the travelling writer visits islands, while a
tile clamp isolates service and update reactions.

This is materially different from rejected A-004: it removes the shared power
shaft and its jam/torsion path rather than adding tile couplers to that shaft.
It also changes the disturbance boundary from a full-field frame to tile seams.
The price is 16 structural frames, 16 datums/clamps, 16 seam interfaces and
more assembly/service locations.

**Cheap bound:** with the E-017/E-005 rate anchor, writing 16 tiles still takes
`16 x (400/(8 x 71)) = 11.27 s`. Even a favorable 0.50 s per-tile clamp/reseat
allowance adds 8.0 s; adding the inherited 5.864 s full-field verification,
0.50 s settling and 1.0 s retry allowance gives about **26.6 s before gantry
index/reversal overhead**. A 1.50 s combined clamp/index allowance per tile (replacing the 0.50 s assumption) gives about
42.6 s. Thus the route has no robust <30 s margin unless clamp/index is near
zero or several tiles are serviced in parallel. It also multiplies precision
datums and seams and makes a failed island unavailable. The stiffness advantage
is plausible but unbounded until a tile frame and seam are modeled.

**Disposition: reject the sequential 16-island schedule under the stated overhead bounds.** Reopen with a changed parallel schedule or justified lower overhead and a bounded loaded-seam model; the segmented-load-path principle is not rejected.

### R2 — deep distributed backplane/grid with local selector strips (best escape)

Replace the single long rail and continuous 80-rotor torsion shaft with a deep
two-dimensional structural grid: purchased or laminated rails are supported at
approximately 8-pitch bays, and each bay carries a short selector strip or
passive A-011 mask interface. Service load closes through nearby grid ribs and
hard stops; the writer reaction closes locally into the grid. State is retained
in the reusable mask/selector, not in the structural member. The grid may be
assembled in serviceable 5x5 or 20x20 panels, but panels are not individually
transported during a full update.

This changes the load path without making every cell an independently purchased
mechanism, and it avoids A-004's shared-shaft couplers. It preserves A-011's
parallel full-map write and local clamp concept. A regional update can address a
panel/strip without global reset, subject to measured coupling.

**First-order bounds:** E-015's 25 mm rail at 406.4 mm and 100 N gives 0.0623
mm in its idealized beam model. If the same section is genuinely supported at
50.8 mm bays, the simple beam term scales as `(50.8/406.4)^3`, about 1/512,
or 0.000122 mm per bay. This is only a scaling bound: joint compliance,
torsion, local plate bending, load eccentricity and support settlement can
dominate. Similarly, the 0.0669 mm full-span torsion term in DES-006 cannot be
inherited; replacing it with short strips could reduce torsional span by about
8x, but only a defined strip reaction path can justify that reduction.

**Full-map/update screen:** no extra per-tile transport is required, so the
inherited A-011 analytical total remains approximately 20.18 s full-field,
0.72 s for a locally clamped 5x5, or 1.72 s with full transport. These are
unchanged calculations, not evidence that the grid is stiff or quiet.

**Cost/manufacture:** added grid rails, joints and panel datums are the main
increment; no 6,400 purchased axles and no 6,400 bought actuators are required.
Printed ribs/panels increase print volume and assembly, but service can replace
a panel rather than a buried full-width shaft. Main correlated risks are rail
joint slip, grid flatness, and writer reaction coupling; their count may be lower than 6,400 independent load stops, but observability and common-cause consequences are unmodelled.

**Disposition: retain for a computational load-path comparison.** It is not promoted and does not rescue
DES-006 until local contact/seam compliance is bounded.

### R3 — grounded load-bearing cell cartridges with force-free selectors

Give every visible post a local, broad hard-stop stack that reacts service load
directly into a nearby base plate. A low-force translating gate or four-plane
mask selects height while unloaded; it does not carry tabletop load. The
travelling writer unloads only the target post, changes its passive state, and
releases it. This is a load-path change from shared frame/shaft to 6,400 local
ground reactions, distinct from A-010's geometry because the defining claim is
that service force never enters the selector or long-span drive.

**Bound:** it can eliminate the DES-006 100 N full-span beam and 80-rotor shaft
terms from the cell datum only if the base plate and each stop/post interface
are demonstrably local. It does not eliminate local tilt, post buckling,
neighbor contact, plate bending, or writer reaction. The repeated precision
interfaces rise to roughly 6,400 stop/post paths plus 6,400 guides; this
directly conflicts with the repeated-mechanism qualification preference and
creates 6,400 wear/service faults. A single stuck selector is local and
observable, but a warped base or shared writer remains correlated.

**Throughput/cost:** it can retain A-011's ~20.18 s full-map calculation and
regional updates in principle, but every changed cell needs unload/change/
verify/release. The current 0.3124 s one-cell DES-003 local prediction is not a
validated per-cell allowance. Printed parts may avoid bought axles, but
6,400 guides/stops and assembly yield are a major hidden cost; replacing a
cartridge is attractive, replacing an inaccessible stop field is not.

**Disposition: conditional research direction only.** It is physically
different enough to model, but its repeated precision and service burden leave it
unranked against R2 until generated geometry and contact/load models bound force-free selection, clearance and neighbour motion.

## Compact trade table

| Route | Q-011 load-path change | Arbitrary-map/full-map update | Regional isolation | Repeated burden / service | Cost and manufacturability screen | Disposition |
|---|---|---|---|---|---|---|
| R1 segmented islands | 16 local frames; no long shaft | ~26.6 s best-case before index overhead; robust margin absent | Potentially strong, but 16 seams | 16 frames/datums; island replacement good | High assembly/joint count; shared writer still needed | **Reject stated schedule** |
| R2 distributed grid | Bay-supported grid; local strip reactions; no continuous torsion shaft | Retains A-011 analytical 20.18 s / 0.72 s local accounting | Potentially improves perimeter coupling; unmeasured | Grid joints/panels, but no per-cell bought load parts | Printed/stock grid and joint burden unresolved | **Retain for modelling** |
| R3 grounded cartridges | 6,400 local hard stops; selector force-free | Retains A-011 in principle; per-cell sequence unvalidated | Local by construction only if base is stiff | ~6,400 guides/stops; difficult field service | Bought cost may be low; yield/calibration risk high | **Conditional only** |

## Recommendation and dominant uncertainty

No route is promoted. Compare R2 joint/support compliance and reaction direction against R3's local contact and assembly burden using generated load paths, tolerance bounds and explicit shared/spatial variation. Carry R1's rejected sequential schedule as a negative comparator; evaluate changed parallel scheduling only if it can recover complete-system margin.

First bound supports, seam gaps/preload, local tilt and selector reaction over declared load cases; escalate informative survivors to contact/structural models. The ideal bay beam scaling alone cannot select R2. Include full-board supports, print/assembly effort, complete unload/write/verify/release timing and recovery. The inherited 0.10 mm displacement screen is provisional, not a stage-02 requirement. Print only if a specific unresolved contact parameter changes the comparison and cannot be bounded economically by computation; select article size from that parameter's spatial scale.

## Evidence boundary

The 20.18 s, 0.72 s, 1.72 s, 26.6 s and 42.6 s figures are first-order
calculations from E-005/E-017 assumptions. The 0.000122 mm bay value and 8x
torsion-span scaling are analytical bounds, not FEA or measurements. Existing
E-041/E-047/E-048 results still govern: Q-011 and regional isolation remain
unresolved, DES-006's combined idealized stack fails the 0.10 mm screen, and
no route here claims reliability, printability, wear life, or affordability
from these calculations. Ranking remains conditional on complete mechanisms, uncertainty bounds and drawing-level costs; hardware claims require physical qualification.
