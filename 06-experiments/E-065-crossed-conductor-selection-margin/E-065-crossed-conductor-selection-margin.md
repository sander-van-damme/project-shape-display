---
status: complete
builds-on: [E-063, A-016]
---

# Crossed-conductor selection margin

**Disposition:** retain only the 2-mm-return air-core cases as tight-scenario
point-field survivors. All nine geometries fail the middle/wide scenarios;
stop their refinement under those bounds. The original guided-flux A-016
remains conditional, not rejected by this air-core mutation. No architecture
selection, affordable strip qualification or fabrication release follows.

Input main `a3e33fa`. This is an air-core conductor-geometry discriminator for
A-016, not a ferromagnetic field solution or a working magnetic flag. Evidence:
analytical magnetostatics, generated finite loop geometry and bounded scenario
calculations; no measurements, manufactured tolerance priors or validated CAD.

Run `OPENBLAS_NUM_THREADS=1 python3 tools/curated-experiment-checks/E-065/field_margin.py`
(Python + NumPy; checked with NumPy 1.26.4). `--check` runs the independent
numerical and limiting-case checks. Output JSON is reproducible, not retained.
Deterministic grid, no seed, random population or probability/yield claim.

## Representation and scope

Generate two orthogonal arrays of 80 rectangular single-turn wire loops on
5.08-mm pitch over 80×80 observation sites. The forward row wire runs +x and
the column wire +y; each has a return and two end connections. End connections
are 10 mm beyond the first/last site. Rows are h below the site plane; columns
are h+0.2 mm below it. h=0.4/0.8/1.2 mm; returns are 1/2 mm sideways or at a
common remote edge 20 mm beyond the final site. These are nine parameter
cases within one air-core topology, not nine new architectures. Removing local
pole pieces is the cost/assembly mutation tested; the original guided-flux
A-016 geometry remains unresolved. The remote-edge case is a
field reference: overlapping return routing still needs physical separation.
No supply/harness field outside these closed loops is included. The second
selector layer, its unpowered magnets and elevator-dependent separation are
not included; concurrent programming cannot assume mutual field isolation.

Integrate the finite straight-segment Biot–Savart law around every loop. The
[Caltech/Feynman derivation](https://www.feynmanlectures.caltech.edu/II_14.html#Ch14-S7)
provides the governing thin-wire law, not a device specification. Units are
metres, amperes, tesla internally; fields are reported in mT per nominal ampere.
An ideal scalar flag responds to the projection along (x−y)/√2. Two crossed
wire fields do **not** add as magnitudes: their directions are orthogonal.
The chosen easy axis makes both projections positive at their own sites.
Actual vector switching, distributed magnet volume, mechanical torque,
remanence, hysteresis, pulse width and neighboring flag magnets are omitted.
Thus a scalar interval is only a necessary conditional discriminator.

A write energizes one row and any subset of same-polarity columns. Separate
positive/negative phases set/reset; mixing column polarities within a phase
is excluded. Calculate the minimum selected projection and maximum absolute
unwanted projection over all 80 row choices and every column bitmask. Affinity
in the independent column bits permits exact extrema by summing negative or
positive coefficients; enumeration of 2^80 masks is unnecessary. This includes
selected-row/off-column sites, unselected-row/on-column sites and unselected
intersections affected by leakage. Reverse all currents for the opposite
write polarity. Current errors are independent bounded line errors; a common
supply error lies inside that envelope. No cancellation is credited as perfect.

For selected minimum S, unwanted maximum U and fractional threshold spread d,
a common nominal scalar threshold must satisfy **U/(1−d) < T < S/(1+d)**.
Negative or empty intervals reject the tested point-threshold embodiment.
Increasing every current scales both endpoints; it cannot fix overlap.

## Manufacturing and model uncertainty

Four scenarios: nominal zero errors; tight ±0.05-mm site/loop registration,
±5% current, ±5% threshold; middle ±0.15 mm, ±15%, ±15%; wide ±0.30 mm,
±15%, ±30%. Registration uses the centre and eight xyz corner offsets, common
across the whole sheet. These are labelled stress scenarios, **not** measured
X1C accuracy or a proof over the continuous placement box. Both worst spatial
fields and line-current boxes enter the shared threshold interval. Threshold
spread includes a possible batch shift as well as local spread.

Independent wire bow, spatially varying warp, local magnet offset, easy-axis
rotation, magnet dimensions, thermal drift, conductor cross section and finite
flag travel are not certified by nine placements. A negative sampled interval
is a counterexample within the scenario; a positive interval is not guaranteed
robustness. In particular the minimum 0.1-mm centreline standoff in the widest
case may not accommodate a real flag plus conductor/insulation. Printed PLA
would support/locate conductors and flags, not provide magnetic pole material;
layer quantization, creep and assembly alignment remain downstream gates.

## Calculated selection windows

36 geometry/scenario combinations, 252 full-board geometry evaluations:
7/9 nominal, 3/9 tight, 0/9 middle and 0/9 wide cases retain a sampled scalar
window. Ten of 36 combinations survive this necessary screen; 26 fail.
Counts describe this deterministic parameter grid, not production yield.

The table gives upper-minus-lower threshold interval in **mT/A**; a positive
number is sampled survival and a negative number is overlap/failure.

| Row standoff mm | Return spacing mm | Nominal | Tight | Middle | Wide |
|---:|---:|---:|---:|---:|---:|
| 0.4 | 1.0 | +0.1700 | -0.0348 | -0.3381 | -0.4310 |
| 0.4 | 2.0 | +0.2080 | +0.0090 | -0.2858 | -0.4058 |
| 0.4 | edge | +0.0942 | -0.1109 | -0.4170 | -0.5913 |
| 0.8 | 1.0 | +0.0654 | -0.0049 | -0.1373 | -0.2568 |
| 0.8 | 2.0 | +0.1003 | +0.0242 | -0.1201 | -0.2389 |
| 0.8 | edge | -0.0926 | -0.1839 | -0.3594 | -0.4807 |
| 1.2 | 1.0 | +0.0272 | -0.0050 | -0.0675 | -0.1416 |
| 1.2 | 2.0 | +0.0514 | +0.0093 | -0.0723 | -0.1568 |
| 1.2 | edge | -0.2232 | -0.2900 | -0.4262 | -0.5517 |

The best tight-scenario interval is h=0.8 mm, return=2 mm:
**0.186397 < T < 0.210566 mT per nominal ampere**. Its midpoint is about
0.1985 mT/A with only ±6.1% remaining interval half-width after the stated
5% threshold spread is already charged. The same geometry's middle interval
is reversed: lower 0.258880, upper 0.138815 mT/A. More current does not change
that ratio. At h=0.4/1.2 mm with 2-mm returns, tight intervals narrow to
0.427105–0.436070 / 0.107908–0.117192 mT/A respectively.

Remote returns at h=0.8/1.2 mm fail even nominally: summing many active column
fields defeats a local 2:1 intuition. Every 1-mm-return case fails tight bounds.
A local return reduces accumulated fields but also cancels useful field;
closer return is therefore not uniformly better. This rules out blindly
shrinking the loops as an isolation fix. Empty intervals reject a **single
uncalibrated common threshold over the sampled scenario**, not every possible
per-site calibrated magnetic writer or flux-guided mechanism.

## Full-machine consequences and stopping rule

Two selectors per site retain 12,800 flags, local memory/detents, moving
collets, pawl-release dogs, 6,400 ground pawls and guides. The field model does
not erase E-063's force, support-transfer or 100-mm tail-track burden. A false
unselected flag command can cause an unchanged pin to unlock at the next cam
stroke. Proof and height/flag readback must inhibit motion; unverified flag
state is not a safe state. Persistent correlated faults stop an isolated module.
No reliability estimate follows from field-window counts.

A direct implementation has 320 reversible lines for two arrays, or 160 dual
H-bridge ICs before logic, sensing, copper, supply, connector and flag costs.
At a $250 **non-selector** reserve and $500 total ceiling, the entire selector
has $250: at most $1.5625/dual driver if every other selector item cost zero. This
reserve explicitly excludes selector drivers; it is not a priced E-063 BOM.
At $150/$350 reserve this ceiling is $2.1875/$0.9375. The full ledger is
`C = reserve + 160*Cdriver + 12800*Cflag + Cboards/harness + Creader-extra`;
allocate reader costs once. These are budget ceilings, not market prices.
[TI's DRV8835](https://www.ti.com/product/DRV8835) is a concrete dual reversible
channel comparator (up to 1.5 A per bridge, 0–11 V motor supply), not a selected
part. Its [ordering page](https://www.ti.com/product/DRV8835/part-details/DRV8835DSSR)
did not expose a numerical price on 2026-10-08; an affordable complete strip BOM
remains unestablished. Multiplexing H bridges may reduce IC count, but requires
bidirectional isolation for inactive inductive lines, current decay and added
switching time; it is a different circuit, not a free saving.

A 1-mm-return loop is 0.84464 m; all 320 loops total 270.285 m. An explicit
0.2-mm × 35-µm copper trace scenario at assumed resistivity 1.72e−8 Ω m gives
2.075 Ω/loop. With both arrays concurrently writing one row and 80 columns,
162 energized loops dissipate about 336 W at 1 A or 756 W at 1.5 A during the
pulse, excluding drivers. These are Joule-loss scenarios, not average machine
power or thermal qualification. Duty cycle, rise/decay, inductance, wider copper,
current regulation and peak supply sizing must be resolved. Larger current
cannot rescue a closed selection interval and incurs quadratic loss.

E-063 allows about 21.14 s for nine complete contact events after its assumed
motion and overhead. With 80 rows, two sequential selector arrays and two
polarity phases/event, at most **7.34 ms per row phase** remains even before cam
motion, grip proof and settling. Parallel arrays permit 14.68 ms only if mutual
field isolation is established, and raise peak power; a one-polarity/reset
strategy must establish its alternate state sequence.
These allocations are not demonstrated switching times. Positive pawls remain
the service load path; neither masks nor racks need magnetic coincidence, but
they retain their own cost, geometry and preparation failures from E-063.

For a hypothetical guided-flux design, normalize each intended row/column
contribution to one. Let L bound total parasitic projection from all other
lines, normalized to one intended contribution, and e bound intended field
error. The conservative window needs
`1+e+L < (1−d)/(1+d) * (2*(1−e)−L)`.
Hence `L < (1−3e−3d+e*d)/2`: tight e=d=0.05 allows L<0.35125;
middle e=d=0.15 allows only **L<0.06125**; e=0.25,d=0.30 admits no window
even at L=0. This bound cannot establish that a local flux return achieves L,
or that local steel, magnets and windings fit the budget/pitch. It specifies
what a materially changed guided circuit must demonstrate before reopening
an overlapping air-core case. Shared steel may also introduce saturation and
nonlinear interactions that invalidate superposition.

Stop air-core refinement when the bounded scalar gate fails. A surviving
point window warrants only a later finite-flag torque/field study with an
actual low-work detent and an affordable strip circuit; no printing or purchase.
Complete the pressure and electroadhesive discriminators before choosing a
product architecture. No new hardware winner or complete Pareto ordering follows.

## Numerical verification

Self-review, not independent external validation: finite-segment closed form
agrees with independent midpoint Biot–Savart quadrature; 200/400/800 segments
give relative errors 2.14e−6/5.35e−7/1.34e−7, consistent with second-order
convergence. Check infinite-wire limit, reversal, zero current, ideal isolated
2:1 coefficients and exhaustive four-column masks/current corners against the
extrema method.
The field solution itself has no mesh/time step. Mechanical and magnetic
material-model discrepancy remains unbounded; numerical checks do not validate
physical switching or service reliability.
