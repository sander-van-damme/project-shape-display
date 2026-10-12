---
status: complete
builds-on: [E-166, E-054, E-056, E-131]
---

# Bayonet columns trade separate pawls for interlevel rotation and alignment

**Preserve the coarse-grid principle; park this architecture before local detail.**
A lugged round stem passes a fixed slot, turns 90° and seats in a grounded pocket:
the column is the moving lock. A 4.8-square cap with .6-mm release hits a neighbor;
2.3-mm lift between 10-mm levels escapes nominally without a swivel. The resolution
extension below shows why this does not establish finer-height feasibility.
No machine, physical qualification, print or procurement is selected.

Original input main `1a3cb2e`; reproduce with standard Python:
`python3 tools/curated-experiment-checks/E-167/probe.py`.
Evidence: **generated rigid geometry, analytical bounds and self-review**; no CAD,
contact dynamics, calibrated process priors, measurements or independent review.
JSON is disposable. All dimensions, forces and speeds below are scenarios.

## Mechanism and controls

E-054/E-056 side-wing pawls are the nonrotating control. [Southco's D2 guide](https://southco.com/en_any_int/fasteners/emdzusemreg-quarter-turn-fasteners/emdzusemreg-turn-to-close-turn-to-open-quarter-turn-fasteners/d2-dzus-rapier-quarter-turn-fasteners)
(accessed 2026-10-11) supplies an insert-turn-seat analogy, not dimensions or
qualified gravity-pocket retention. E-131/A-007 screws retain their own
friction/throughput constraints; a released quarter-turn is not a 40-mm screw lead.
A swivel top avoids rotation but adds 6,400 captured thrust/retention interfaces.
Interlevel turning changes the path without that added joint.

Units mm, z up, pitch 5.08. Shaft radius .6; five rectangular lugs x=[−2,2],
y=[−.45,.45], thickness 1.2, spaced 10. A 4.8-square/2-thick cap has top 44 above
the lowest lug bottom. Stem shift −10k for k=0…4 gives tops 44/34/24/14/4.
Round exposed stems are essential; full-width square skirts invalidate clearance.

Gate base z=[−1.2,0]; aperture is full-width x slot |y|<.65 union central square
|x|,|y|<.8. Ten boxes form base rails, shoulders and raised pocket rails at
z=[0,.4], |y|≥.8, |x|≥.65. At theta=0 lugs pass; at 90 wings bear in a 1.3-wide
pocket. Its walls constrain seated yaw; lift above .4 permits turning.

Captured seat → lift → turn 90→0 → translate → turn 0→90 → lower → prove → detach.
Twenty unequal transitions/five lugs give 8,500/32,500/128,500 poses at 16/64/256
subdivisions with no gate intersection at .6 lift; 2.3 lift also clears at 64.
Seated 45° rotation and axial translation while locked deliberately collide.
Continuous separation: aligned lugs fit the slot; turning lug clears .4 and the
next lower lug stays below −1.2 (its top is −6.5 at 2.3 lift). These are nominal
path results, not supported contact, capture, angular-error or hardware passes.

All variants need bilateral loaded capture before release and retained axial/
rotary reaction until actual height and seating are proved. A false seat can drop
the column. Retry while captured, then stop the module, is an intended policy;
no sensor or input-loss arrest implements it. Slot-aligned gravity does not hold.

## Distinct geometric and manufacturing failures

Equal overlapping caps first touch when `(d/2)(cos(theta)+sin(theta))=p−d/2`:
**7.1484°** at d=4.8. Polygon grids converge through 8.4375/7.3828/7.2070°;
45° intrusion is .7141. Isolated coplanar turning requires d≤4.2084; arbitrary
simultaneous neighboring turns need d≤3.5921. Threshold holdouts check these
geometry limits, not miniature usability.

At .6 lift, 25 old/neighbor pairs give **4,300 intersections/25,700 poses**.
At 2.3 lift: zero, including neighboring lugs. The active cap bottom clears a
same-height top by .3 and its top clears the next higher cap bottom by 5.7.
It occupies z=4.3…6.3 above a 10-mm lug datum, missing neighboring 1.2-thick lugs.
Aligned vertical travel has .28 cap/cap and ≥.68 cap/lug horizontal gaps.
A turning-cap envelope clears a radius-1.4 neighboring stem by .2859, but that
larger shaft does not fit the original .8 aperture. Adjacent active caps still
collide; checkerboard centers leave .396 circumcircle separation. This supplies
neither a head route nor an automatic timing factor. Miniatures on changed caps
rotate and return; their slipping/handling and exposed-stem appearance are open.

Let e bound in-plane moving/gate edges and relative center offset. Shared size/
registration bias can put many sites at the same adverse corner; rigid common
translation cancels. Slot/pocket/shaft margins are .2−3e; wing land 1.2−3e;
short-lift axial margin .2−2e. These are bounds, not printer priors or yield.

| e mm | Slot/pocket margin | Wing land | Slot/pocket failures, 64 corners |
|---:|---:|---:|---:|
| .025 | .125 | 1.125 | 0 / 0 |
| .050 | .050 | 1.050 | 0 / 0 |
| .100 | −.100 | .900 | 16 / 16 |
| .150 | −.250 | .750 | 16 / 16 |

Corners rebuild offset, lug dimensions, aperture and slot/pocket edges. A wide
slot holdout omits vanished shoulders, avoiding inverted solids. At e=.05,
angular error delta leaves `.55−.50 cos(delta)−2.05 abs(sin(delta))` clearance:
.0143 at 1°, −.0212 at 2°. Pocket uses swapped axes. Cap gap budget .3−4e is .1
at e=.05 and fails at .10; widening needs changed geometry.

Nominal bearing area 2.16 mm² gives 4.63 MPa average at an assumed 10 N, not a PLA
allowable or peak pressure. Root stress, eccentric load, guide moments, plate
bending and distributed frame grounding remain unsolved. Ideal straight-shaft
Euler diagnostic `Pcr=pi² E (pi r⁴/4)/(K*44)²` at E=2000 MPa gives:

| Radius | Pcr N, K=1 / K=2 | Wing land with aperture r+.2 |
|---:|---:|---:|
| .6 | 1.038 / .259 | 1.2 |
| 1.2 | 16.605 / 4.151 | .6 |
| 1.4 | 30.763 / 7.691 | .4 |

Source also sweeps E=1000/3000. Neither restraint is established; this is not a
lugged-column eigenmode, creep or strength qualification. Larger stems consume
bearing; extra guides must allow every lug/cap transition. No thick-stem pass.
Ten grams lifted .4 stores only .03924 mJ; this is not shock retention. Stiction,
upward release, warp, layer/first-layer error, roughness, anisotropy, creep, wear
and fatigue remain uncalibrated. False acceptance p gives 6,400p expected misses
without independence; neither p nor product reliability is known.

## Board burden and service bound

Resident burden: 6,400 rotating columns, 32,000 fixed lug stations and 6,400
precision pocket/slot sites, plus guides and cap attachments. Fixed forms are not
moving latches. Modular printed rails still need attachments, alignment, repair
access and assembly. At assumed $250 shared spend, resident bought allowance is
<$.0391/cell under $500, before head extras; no priced BOM or fabrication pass.

Optimistic service grants 40-mm travel at 300 mm/s, 3000 mm/s²; two lift/reseat
strokes; two 90° turns at 7200°/s²; .05 s capture/proof/release; and 6 s/map for
preparation, registration, other travel, settling, verification and bounded retry.
Strict `6+ceil(6400/H)*service<30` gives:

| Rotary ceiling °/s | .6 lift: service s / heads | 2.3 lift: service s / heads |
|---:|---:|---:|
| 360 | .93990 / 256 | .99409 / 267 |
| 720 | .78990 / 214 | .84409 / 229 |
| 1440 | .78712 / 214 | .84130 / 229 |

Acceleration limits the fastest cases. Transport, checkerboard conflicts,
retained output routing and recovery are unbuilt. E-166's .45/.50/.55-s service
controls need 121/137/149 heads under the same optimistic overhead. No timing
advantage is earned. U pockets remain grounded, but frame deflection/vibration
and actual disturbance are unknown. E-168–E-171 subsequently examined guidance,
bearing and shared pickup without establishing a competitive complete machine.
No rotary-head detail follows from this historical nominal path.

## Resolution extension: tops and gate consume the same height gap

On input main `a2025e3`, run
`python3 tools/curated-experiment-checks/E-167/resolution.py`.
**Calculation and reduced rigid geometry, self-review; no physical measurement.**
Stage 02 specifies 40-mm travel, not a height increment. The five-level result
cannot silently establish feasibility at finer resolution.

Keep the original 4.8-square/2-thick tops, 1.2-thick lugs/base and .4-deep pocket.
Change vertical station spacing to D. At an interior height h, put unchanged
neighbors at h and h+D. At 45 degrees the active cap overlaps both neighboring
footprints. Turning in the first interlevel gap requires lift L satisfying

`max(2+Ec, .4+Eg) < L < D - max(2+Ec, 1.2+1.2+Eg)`.

Ec/Eg are **total adverse axial gap allowances** for cap/gate separation, not
per-part errors, distributions, X1C priors or the original in-plane e. The next
lower lug rising into the base underside sets the upper gate limit. With equal
Ec=Eg=E, positive clearance needs **D > 4.4+2E mm**. Equality leaves touching.
This is a first-gap, fixed-axis integral-cap bound, not a universal yaw limit.

| Spacing / levels over 40 mm | Nominal L-window width | E=.15 | E=.35 | E=.70 | Board lug stations |
|---|---:|---:|---:|---:|---:|
| 10 mm / 5 | 5.60 mm | 5.30 | 4.90 | 4.20 | 32,000 |
| 5 mm / 9 | .60 mm | .30 | **−.10** | −.80 | 57,600 |
| 2.5 mm / 17 | **−1.90 mm** | −2.20 | −2.60 | −3.30 | 108,800 |

Window width is a range of commanded lifts, not a fit margin or complete-geometry
pass. At D=5, centered L=2.3 leaves .30 mm to each nominal boundary; the error
tipping point is E=.30. The independent in-plane slot restriction still applies.

**Finite witness:** D=5; thicken the lower neighbor cap upward by .35, move the
upper neighbor down .35, and thicken the base downward .35. At L=2.3/theta=45°,
the active cap and next lower lug each penetrate their obstacles by **.05 mm**.
Cap clearance needs L>2.35; gate clearance needs L<2.25. Thus no first-gap midturn
height works in this coherent scenario. Original polygon SAT independently checks
both intersections, 2,001 heights across 0…5, and ±1-micrometre boundary holdouts.
The contradictory intervals, not sampling, establish continuous exclusion.
Positive windows also clear reduced cap/own-gate solids at 16/64/256 turn samples;
neighbor lugs, guides, loaded deformation, active-neighbor turns and heads are
outside this extension. No three-dimensional machine pass follows.

Common cap/base bias can consume many windows together. Seating, pitch errors,
wear, debris and deflection spend the same budget; none is measured. A 1-mm cap
changes the bound to D>3.4+2E (4.1 mm at E=.35), an escape condition rather than
permission for a thin-top campaign. Stiffness and manufacture remain unpaid.

The ledger above still has 6,400 columns/gates and at least 12,800 guide duties;
each row has 80/80/160. Nine levels raise fixed lug forms from 400 to 720 per row,
not moving latch count. No spring, swivel, sensor, insert, or assembly saving is
created. Print time, orientation, attachment, fits and service remain unqualified.
Granting the earlier direct-head allowances still needs **229 retained rotary/
axial output pairs**, .84409 s/service and 29.63447 s/map. An assumed $295 shared
reserve leaves **$.8952/complete pair** under $500 before resident extras. This
is a spending bound, not a priced BOM; the six-second overhead has no constructed
programmer, transport/conflict schedule, readback, arrest or recovery inside it.

E-236's shared five-stroke control uses 400 command channels/seven shelves; its
unchanged columns transfer support. Integral rotation could keep U rails fixed
but owes loaded capture and this spacing restriction. E-249 pitch tilt avoids
yaw but owes compatible guidance/320 retained output pairs in its allocation.
These are functional comparisons, not equal-assumption timing rankings. A U-cap
collision directly defeats isolation; installed rails do not prevent it. Head
support through release, source-loss arrest, actual height/seating proof and
safe captured recovery remain unbuilt as described above.

**Park the fine-spacing first-gap embodiment.** Preserve the coarse-grid principle
with its limits. Reopening requires a changed full-machine support/motion route
that reduces retained loaded outputs while preserving U support, with height
resolution explicit. No thin-cap, pocket, cam or guide repair and no print is
justified. The next discriminator remains shared loaded motion and arrest.
