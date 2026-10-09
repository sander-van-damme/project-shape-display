---
status: complete
builds-on: [E-089, E-081]
---

# Finite trip faces trade compactness for discrimination

**Stop the alpha=0.5 single-slot embodiment under the adverse dimensional box;
retain alpha=1 only for the next finite-package investigation.** Adding independent
±0.1-mm slot/probe width bounds consumes E-089's entire 0.1-mm reserve. No change
of slot width can restore simultaneous guaranteed target insertion and exclusion
of the nearest wrong state in that box. This rejects an embodiment under explicit
uncertainty, not retained multilevel commands or measured X1C capability.

A second constraint is architectural: a finite short slotted tab lets a distant
probe pass outside its ends, producing a false selection. A simple uninterrupted
blocking strip sufficient for every signed command/reader pairing needs about
**161–162 mm body length and 241–242 mm swept length at alpha=1** without sign
isolation. A working phase-sign gate reduces the sufficient envelope to
**77–78 mm body / 157–158 mm sweep**, before guides and installation allowance. An array of rigid probes on one common
insertion bar also fails mixed matches: one blocked neighbor arrests the selected
probe. Independent probe travel is required in this implementation.

Input main `4ff89e9`. Reproduce:
`python3 tools/curated-experiment-checks/E-090/finite_trip.py`.
The retained source generates finite convex contact sections and enumerates
**645,504 state/width/error corner cases across 24 bounded scenarios**, with 198
independent polygon-contact holdouts and 19,848 finite-face state/error checks. No random seed, physical measurements,
calibrated probability, material model, CAD qualification or complete machine
survivor. This is the decoder subsection of E-089's open finite-package gate;
detents, setting, sign selection and load-support transfer remain unproved.

## Geometry and uncertainty

Use H=21 over 40-mm column travel, as a workload comparison rather than a product
resolution requirement. State pitch is `p=2 alpha` mm; cursor and reader each
range over −20p…20p. The reader is a convex 3-mm-long pin with nominal 0.4-mm
shank width, 0.2-mm tip and 0.4-mm chamfer length. It enters normal to a 1-mm-thick
flat cursor plate containing one rectangular slot, nominal width `W=0.4+p`.
Insertion stroke is 1.5 mm. These are generated two-dimensional rigid sections,
not a full 3D package: lateral guides, rotation and neighboring support parts are
not granted clearance. Plate lands and pin polygons are explicit in the source.

Competing epistemic boxes use relative datum error E0=0.1/0.2/0.4 mm, independent
slot and shank width deviations s=0.05/0.1 mm each, and reader-to-cursor gain
error r=0/1%. The datum bounds inherit E-089's common/spatial/local decomposition;
all components can align coherently. Width corners permit common slot growth
and probe shrinkage across an entire bank, not independent lucky cells. The
fixed gain error accumulates with reader coordinate. At the extreme,
`E=E0+40 alpha r`. No distributions or manufacturing yield are inferred. These
are bounds to discriminate mechanisms, **not sourced fabrication statistics**.

Tip width/chamfer/plate thickness are fixed geometry hypotheses in this screen;
burrs, shape error, pin yaw, wear, elastic penetration and dynamics can worsen
it. Overshoot belongs in E or an additional error term, not free margin. The
±0.1-mm width scenario is added uncertainty absent from E-089, not a correction
to its arithmetic or a measured printer error.

Full shank insertion requires `2|dx|+w <= W_actual`. Hence a tunable nominal slot
must satisfy both:

- target containment: `W >= 0.4 + 2E + 2s`;
- exclusion of a wrong neighbor: `W < 0.4 + 2(p-E) - 2s`.

A strict feasible interval exists only when `p > 2E+2s`. At alpha=0.5,
E0=0.4, s=0.1 and r=0, both limits equal 1.4 mm: a wrong neighbor can enter fully
at its boundary. Tightening the slot loses intended insertion; widening it admits
wrong states. At r=1%, the lower/upper bounds become 1.8/1.0 mm. Do not spend a
nominal slot-width sweep trying to repair this contradiction.

| alpha | E0 / size bound each / gain | Nominal slot | Guaranteed capture / rejection reserve | Sufficient body / swept length |
|---|---|---:|---:|---:|
| 0.5 | 0.4 mm / 0.1 mm / 0 | 1.4 mm | 0 / 0 mm | 81.3 / 121.3 mm |
| 0.5 | 0.4 mm / 0.1 mm / 1% | 1.4 mm | −0.2 / −0.2 mm | 81.7 / 121.7 mm |
| 1 | 0.4 mm / 0.1 mm / 0 | 2.4 mm | 0.5 / 0.5 mm | 161.3 / 241.3 mm |
| 1 | 0.4 mm / 0.1 mm / 1% | 2.4 mm | 0.1 / 0.1 mm | 162.1 / 242.1 mm |

For the adverse 1% scenario, the independent inversion gives **alpha>5/6**.
Twenty of the 24 scenario combinations retain strictly positive margins; this
fraction is not a probability. Alpha=0.5 can reopen with a defensible smaller
combined error bound or changed encoding/reader geometry; alpha=1 does not
inherit a detent, writer, time, cost or support pass.

## False entry, finite ends and withdrawal

The reduced contact law obtains the available aperture width at displacement dx
and finds where the widening chamfer first meets a land. A wrong state can enter
partway even without full shank containment. In the ideal section all such stops
occur by 0.4-mm insertion. A proposed output gate that opens at 0.8±0.1 mm separates
partial insertion plus a bounded 0.1-mm depth error (at most 0.5 mm) from a fully
inserted probe (at least 1.4 mm). This is a **gate-interface envelope**, not a
constructed cam/follower. Any force path that uses initial probe motion as the
selection signal fails this partial-entry witness. Nor can a depth gate reject
the fully admitted wrong neighbor in the failed alpha=0.5 scenario.

Finite end coverage is checked separately. A 2-mm-long tab with a 1.4-mm slot
lets a reader displaced 3 mm from its slot pass entirely outside the tab; the
polygon checker returns full 1.5-mm insertion while the infinite-land formula
returns zero. For the long-strip implementation, the maximum relative center
excursion is `40p+E`. Choose half-body length at least that plus half the widest
probe; this conservatively keeps the full probe over blocking material away
from the slot. The table uses `L=80p+2E+0.4+s`, then adds cursor stroke `40p` for
the swept envelope. Outer-edge shortening requires additional stock allowance.
This is sufficient, not a universal lower bound. In particular, E-089 already
hypothesizes phase-specific sign gating. If it positively inhibits opposite-sign
and neutral outputs throughout deposition (not just acquisition), admissible
pairs have q,r both in 1…20 or both in −20…−1. Maximum difference then falls
from 40p to 19p. A sufficient sign-gated face has
`L_sign=38p+2E+0.4+s`, with sweep `L_sign+40p`: at alpha=1 this is
77.3/157.3 mm without gain error and 78.1/158.1 mm with 1% gain error. At alpha=0.5
the adverse 1% values are 39.7/79.7 mm, but discrimination still fails.
All same-sign state pairs and datum/gain corners are checked against the finite
plate polygons. This is a conditional packaging improvement, **not proof that
the sign gate exists**. Its failure exposes the shorter plate's ends: q=−20,
r=+20 at alpha=1 passes outside the face and falsely inserts fully. A telescoping
cover, normally closed local gate or linked position comparator may reduce the
face further, but needs a different finite selection and reset proof.

The generated pin hits a slot land if translated by one state pitch while still
inserted. Withdrawal to −0.1 mm clears the ideal plate before either reading
coordinate or command setting moves. A jammed probe therefore prohibits both
motions; commanding withdrawal is not evidence that it occurred. Positive
pullback, local proof, acceptable pull force and a recovery path remain required.
A global RETURN stop limiting insertion to 0.3±0.1 mm is below the earliest
0.7-mm gate opening in this envelope. Its strength, retention and individual
probe response are unproved; a common failed stop remains a correlated fault.

## Shared insertion and force accounting

With one selected and one solid-face neighbor, the available depths are 1.5 and
0 mm. A rigid common carrier reaches only their minimum, so the selected output
never enables. This rejects **rigid shared-depth insertion**, not shared energy.
Independent sliding probes with compliant push and positive pullback are one
possible repair; their force and repeated parts cannot be omitted.

For an illustrative spring isolator, blocked-pin force is `F0+k*1.5`, with k in
N/mm. These are competing force scenarios, not sourced spring/friction priors:

| k / preload | Blocked probe | 800-cell bank upper envelope | 6,400-cell upper envelope |
|---|---:|---:|---:|
| 0.05 / 0.02 N | 0.095 N | 76 N | 608 N |
| 0.2 / 0.1 N | 0.4 N | 320 N | 2,560 N |
| 0.8 / 0.1 N | 1.3 N | 1,040 N | 8,320 N |

These all-blocked bounds can overestimate scheduled active banks; they expose
fanout without claiming a necessary force floor. Incremental spring energy is
0.36/1.44/5.76 J across 6,400 blocked probes per query, excluding preload work,
friction, drive inertia and losses. Softer springs reduce reaction but must still
overcome guide friction and seat within the transfer dwell; no settling time is
established. Sequential bank queries reduce peak reaction while adding time.

If every cell has such a query module, there are 6,400 independently sliding
probes and compliant push paths, plus pullback and depth-gating interfaces.
Carrier-position sensing alone can falsely accept a selected probe jammed at
zero while the carrier compresses its spring and reaches 1.5 mm. Individual
probe/depth proof or another independently justified observation remains inside
the product time and cost boundary. The probe only selects a separate energy
cam; it must not be credited as a service-load brake. Unloading the output cam
before gate retraction and preserving ground/grip support on a failed proof
remain finite-mechanism gates from E-081.

## Decision and verification limits

Continue the existing retained-command campaign with alpha=1 as a **conditional
geometric comparator**, carrying its strip and independently moving probe
burden. Prioritize a finite sign gate because it can reduce required face coverage
as well as implement acquisition; require inhibition during every query. Stop the alpha=0.5 adverse-box embodiment, short exposed slot tags and
rigid common probe bars. Preserve the selective stepped-deck and direct-position
controls; no physical principle or complete architecture wins this subsection.
Next discriminate finite retention/positive setting and sign gating, then the
independent probe's output-cam coupling and loaded support transfer. Reject or
change principle if the long face, return path or fanout cannot be packaged;
do not treat the previous mask-count advantage as an obligation to rescue it.

Self-review only: exhaustive 41×41 state pairs at dimensional/datum/gain corners;
strict analytic slot-width interval and alpha inversion; 198 separate SAT
polygon/bisection comparisons including interior chamfer contacts; short-face
bypass, rigid-bank obstruction, movement-before-withdrawal and carrier-readback
fault witnesses. Polygon bisection resolution is <6e−12 mm, much smaller than
the stated 1e−7-mm comparison tolerance; no physical precision follows. Contact
is monotone over the tested insertion stroke and sections are piecewise linear,
so no time discretization is involved. No test covers compliance, fatigue,
creep, loaded-release friction, complete lateral packing or actual false-accept
probability. No printing or purchased parts are justified by this result alone.
