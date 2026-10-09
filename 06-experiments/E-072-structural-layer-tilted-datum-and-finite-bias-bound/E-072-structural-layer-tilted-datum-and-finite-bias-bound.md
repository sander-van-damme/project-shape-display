---
status: complete
builds-on: [E-071, E-070, A-022]
---

# Longer local datums fail by stroke-amplified tilt

**Reject the tested 12/20-mm local two-pad retrofit under the bounded mismatch
below, even granting ideal preload.** A carriage following mismatched pads
translates along a tilted axis; its dog housing eventually intersects the
vertical fork. This is a new finite-geometry counterexample, not another
assertion that manufacturing evidence is absent. It does not reject structural
memory or every possible datum arrangement. Stop refining these local guides;
no FEA or print is justified for them.

Input main `33cef17`. Reproduce with
`python3 tools/curated-experiment-checks/E-072/tilted_datum.py`; `--all` emits
48 scenarios and collision pairs. Standard library, deterministic rigid geometry
and beam calculations; units mm and N. No physical measurements, process priors,
random sampling, yield estimate or hardware acceptance.

## Finite geometry and error allocation

Import E-070's connected carriage, bore, T guide and fork, and add E-071's two
0.4-mm-tall datum pads. Pad face errors are −a and +a, separated by L−0.4 mm.
Both finite pads touch the straight flange at corresponding bottom corners for
positive tilt (top corners for negative tilt). Thus

`tan(theta) = 2a / (L−0.4)`.

Rotate every carriage solid, including the bore. To remain on both pads the
carriage must translate along its own tilted axis. Check the whole stroke against
a vertically translating fork, and the failed-proof/overtravel interval against
the fixed mount. Convex hulls of endpoint polygons give exact continuous sweeps
for this fixed-angle translational model; separating-axis tests in x-z, with
finite y overlap, find actual prism intersections. Merely using a rotated
axis-aligned bounding box would overreport collision and is not used.

**Partition** the old e=0.15-mm relative-error scenario: pad error consumes a;
opposing common rail registration consumes e−a. Do not add a fresh ±e expansion.
At either datum contact the worst relative x error is still at most e. The
extra error at the dog comes from extrapolation and stroke, rather than double
counting process error. Nominal flange width and all other dimensions remain
unchanged; this is an admissible counterexample within a larger unknown error
set. A common rigid shift of carriage and rail cancels. Equal pad offsets give
no tilt; opposite pad offsets are the adverse differential case. These are
competing correlation cases, not assigned probabilities.

Enumerate L=12/20 mm, a=0/0.01/0.025/0.05 mm, both tilt signs and all three
10/20/40-mm layers: **12/48 cases collide**. The others pass only this narrow
collision test; no dog engagement, latch proof, elasticity or full-machine pass
is inferred. The decisive upper-layer positive-tilt cases remain clear of their
own fixed guide throughout travel, but their bore floor/roof intersect the lower/
upper fork. This is permitted guide motion, not an imposed pose the mount blocks.

| L | a | Tilt | Rail shift | Roof-to-fork x gap at 40 mm |
|---|---:|---:|---:|---:|
| 12 mm | 0 | 0° | −0.150 mm | +0.0500 mm |
| 12 mm | 0.010 mm | 0.0988° | −0.140 mm | −0.0253 mm |
| 12 mm | 0.025 mm | 0.2470° | −0.125 mm | −0.1381 mm |
| 20 mm | 0.010 mm | 0.0585° | −0.140 mm | +0.0055 mm |
| 20 mm | 0.025 mm | 0.1462° | −0.125 mm | −0.0613 mm |

Negative gap denotes penetration in x; the polygon test independently confirms
z/y intersection for the negative cases above. Analytically, for the roof's
upper right corner at local (c,z_r), its lateral excursion is

`−a + (cos(theta)−1)(c−x_d) + sin(theta)(z_r+stroke−z_lower)`.

Subtract this from the nominal gap plus rail bias. Bisection on this exact corner
expression gives zero-gap a=0.00664/0.01123 mm for L=12/20. These are **necessary
corner-clearance limits for this error allocation**, not qualified tolerance
specifications; positive running margin, pad deformation, wear and other errors
make them insufficient for acceptance. Increasing force cannot make two
mismatched rigid pads collinear with a vertical rail.

## Finite bias skeleton and model uncertainty

Construct a paired leaf arrangement inside the former right guide wall: two
0.4-mm-thick vertical leaves, 0.4-mm end anchors and a 0.4-mm-tall central shoe.
Release slots of 0.20 mm separate each leaf from the existing front lip and rear
wall, leaving only **0.40 mm leaf width**. Using the entire 1.6-mm wall depth as
a free cantilever would wrongly include material attached to those walls. The
installed straight skeleton is connected and clears the nominal carriage
through stroke/proof/overtravel. This construction checks available material
and release space; its free shape, prestrain, assembly and compliant motion are
not qualified. It remains a repeated submillimetre flexure at 19,200 sites.

For a bending-only clamped-guided pair, `F=2 E b t^3 delta / ell^3`, with
ell=(L−1.2)/2. Explicit exploratory assumptions E=3,000 MPa and delta=0.6 mm
are **not sourced X1C PLA properties or safe strain bounds**. They give
0.585/0.111 N for L=12/20, versus E-071's marginal ideal requirements
1.476/0.607 N at W≤1 N, |H|≤0.2 N, mu≤0.6.

Do not promote that linear shortfall to a universal spring rejection. At
delta/t=1.5, an initially straight beam with constrained axial stretch adds
`1.44 E b t delta^3 / ell^3` for the pair, giving 1.533/0.291 N. That comparison
can reverse the 12-mm force result. It is an alternative beam assumption, **not
an established packed preload configuration**: a precurved spring straightening
in the same envelope can instead experience compression; axial release and
assembly prestrain change the force. A nonlinear model would be needed to
select such a spring. It has low decision value now because ideal bias already
fails the independent rigid tilt screen. No strength, creep, fatigue or bought
spring saving is claimed.

## Decision and next discriminating mechanism

The failure is local but can be correlated across a printed bank. It needs no
6,400-cell independence assumption and no reliability probability. No additional
machine cost/time claim follows. E-069's support path cannot be combined with
these ideal-centered guides to claim a supported assembly. Contact compliance
could redistribute pad reactions/tilt, but would need an explicit position
bound under load; it cannot simply be called perfect alignment.

Retire this local two-pad retrofit within the existing campaign. The remaining
bounded test is a **vertically displaced shared-frame guide with a through-slot
for the dog/bore**, which may place the guide span around the drive instead of
below it. Generate the finite slot, retained load faces, latch connector and
neighbor layout through all strokes/lower offsets. A shared moving guide cannot
merge independent cell coordinates. Count stationary channels, depth and repeated
contacts; carry this differential-datum model into any survivor. If that changed
topology has no finite supported witness, close the campaign with scoped
rejection rather than extending another local-pad parameter sweep. Reopening
local datums requires a materially changed alignment mechanism or evidence
supporting a complete, sufficiently smaller error budget.

Self-review: axis-aligned box limit, exact touching, rigid length preservation,
two-pad contact slope, both tilt signs, coherent translation cancellation,
off-grid L=17.137 mm, and containment of 4/17/64-step sampled intersections in
the continuous sweeps pass. An independent strain-energy integral checks the
linear leaf coefficient with two quadrature resolutions. These verify models,
not hardware. Reproducible JSON is not retained.
