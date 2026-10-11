---
status: complete
builds-on: [E-170, E-153, E-101]
---

# Direct rotary release trades cap clearance for steep sliding contact

**Stop the tested integral-cap sliding-cam repair of E-170.** A finite grounded
helical shoe can lift and retrace without an independent axial input, but the
adverse cap-clearance case requires a steepness incompatible with the .2-friction
scenario even under a generous cell-wide contact bound. The generated shoe also
cannot continue rotating at the proposed 2.3-mm lift: its trailing contact forces
additional rise. Its fixed crest intersects the lowest parked cap. These are
scoped necessary-condition failures, not rejection of rolling cams, smaller caps,
relative rotary collars or all shared power. No machine survivor or print follows.

Input main `214ff9e`; LAB-280. Reproduce:
`python3 tools/curated-experiment-checks/E-171/cam.py`.
Evidence: finite rigid cap prisms, parametric finite helical contact surfaces,
exact separating-axis translation intervals and quasistatic Coulomb balances;
self-review only. No fabrication CAD, contact deformation/dynamics, calibrated
X1C/friction prior, priced components, physical measurement or independent review.
JSON is reproducible and discarded. All dimensions/friction/loads are scenarios.

## Functional comparison

| Combination | Selection / motion / support / recovery | Result and repeated burden |
|---|---|---|
| Direct column cam | Torque-selected column climbs two grounded ramps; periodic lugs then acquire E-170's shared lift; reverse cam motion reseats. | Removes the asserted independent release lift only during generated ramp engagement. Tested clearance/friction, continuation and parked geometry fail below. Shared plate pickup, angular capture, power-loss support and readback remain unbuilt. |
| Relative collar cam | A grounded rotating collar lifts an antirotating column before a separate pickup engages; collars remain parked at unchanged cells. | Avoids cap rotation, allowing a larger cam angle. Adds a resident rotor/thrust/column coupling and still needs pickup and a retaining state; not the integral-column simplification. No finite collar witness or cost pass. |
| Nonrotating periodic pickup | A fork acquires repeated rack stations at a common datum while a ground dog releases/reseats; shared deck supplies travel. | Avoids this cap/ramp constraint but restores separate pickup and ground selection. E-098/E-099 are controls, not newly discovered principles. |
| Direct head / screw | Captured rotary-linear head supplies the release explicitly; screw converts sustained torque to height. | E-167/E-131 controls retain their channel, throughput, support and cost obligations. |

This probes E-170's explicit escape, not a new cam principle. E-101 addressed
crossed shared-support packaging; E-153 addressed corrugated wells and energy.
Neither established this integral-cap short-angle transfer. No new external
search or global saturation claim. Repeated local repairs now have diminishing
value without a comparative complete-machine benefit; broaden the next search.

## Finite cap clearance bounds the available rise

Pitch 5.08; cap side 4.6, thickness 2. Active cap stays vertically guided while
rotating by theta. Neighbor remains at the same height, tilting toward it by
`alpha=atan(2c/25)`, with center drift `c(1+2*43/25)` at z=43. A coherent adverse
case expands each cap half-dimension by e and shifts the neighbor center inward
by e. Thus thickness also grows by 2e, unlike E-170's fixed-thickness section.
These are admissible correlated bounds, not distributions or measured errors.

Generate both oriented rectangular prisms. Fifteen separating axes give their
collision interval under axial translation exactly; an actual overlap at one
angle supplies a necessary lower bound on rise. For a constant lead h=k theta:

| e / c mm | First overlap at zero lift, degrees | Necessary k witness, mm/rad | Sufficient k envelope, mm/rad |
|---|---:|---:|---:|
| 0 / 0 | 13.72406 | 8.34968 | 8.34969 |
| .025 / 0 | 11.12753 | 10.55547 | 10.55547 |
| .050 / 0 | 8.74593 | 13.75738 | 13.75738 |
| .025 / .025 | 7.74030 | 15.14021 | 15.20906 |
| .050 / .025 | 5.56743 | 21.56321 | 21.65995 |

Sufficiency here concerns only these cap prisms: reach the exact neighbor-top
clearance before the first zero-lift collision. It does not validate a cam.
The adverse witness at 5.56743187° needs 2.09529791 mm lift. It penetrates at
1 micrometre less lift and clears at 1 micrometre more. A full-prism witness
supersedes neither E-170's different section conditions nor its conclusions.
The same-height neighbor is enough to reject robustness; no favorable averaging
across 6,400 sites is valid. Other heights, lugs and simultaneous active neighbors
need further checks for any repaired machine.

## Torque, friction and signed motion

At contact radius r, a helical surface has slope m=k/r. Its unit uphill tangent
and normal in tangential/axial coordinates are `(1,m)/sqrt(1+m²)` and
`(-m,1)/sqrt(1+m²)`. For total downward force F, friction coefficient mu, and
symmetric opposed contacts with ideal guidance:

`N_up = F sqrt(1+m²)/(1-mu*m)`

`tau_up = F r (m+mu)/(1-mu*m)`

`tau_hold_on_descent = F r (m-mu)/(1+mu*m)`.

N is the aggregate normal magnitude at a representative radius, not peak
contact pressure. Positive compressive sliding support during raising requires
**mu*m<1**. If every available contact violates it, more torque cannot supply a
positive vertical reaction; deformation, another contact or another energy path
would change the model. Ideal frictionless guides favor the mechanism.

This also bounds a variable-lead sliding cam: with no initial axial lift or
stored-energy boost and contact radius at most R, each raisable increment needs
`dh/dtheta<R/mu`, hence `h(theta)<R theta/mu`. Grant even the square cell's corner
radius **R=5.08/sqrt(2)=3.5921 mm**, ignoring swept interference. The adverse
witness requires **mu<.166585**; a circular in-cell bound R=2.54 tightens this to
**.117793**. At mu=.2 the favorable square-radius path still intersects the
actual cap. An off-threshold 6° holdout at 1.88082044-mm lift contains a
point strictly inside both prisms, independently checked in their local frames.
Thus nonlinear reshaping alone cannot escape this bounded sliding
case. Contacts extending outside the cell, rolling, stored energy, smaller caps
or decoupled cap rotation change its scope.

Representative-radius r=2, F=1-N calculations (scale linearly for .1/10 N):

| k mm/rad | mu | Raising torque Nmm | Aggregate normal N | Descent holding torque Nmm |
|---:|---:|---:|---:|---:|
| 10 | 0 | 10 | 5.099 | 10 |
| 10 | .1 | 20.4 | 10.198 | 6.533 |
| 10 | .2 | no positive sliding equilibrium | — | 4.8 |
| 24 | .05 | 60.25 | 30.104 | 14.938 |
| 24 | .1 | no positive sliding equilibrium | — | 10.818 |

The actual finite shoe spans r=1.75…2.25; r=2 is a diagnostic, not a solved
pressure distribution. At k=24 and mu=.1 even its outer radius fails; at .05
all those radii satisfy the necessary friction condition. Mu=0/.05/.1/.2/.4
are competing bounds, not a claim about printed PLA or rolling resistance.
The uncertain friction choice reverses the local disposition; no yield follows.

Both steep cams backdrive when torque is removed: positive descent holding
torque is required for the tested friction range. Retrace can bring a loaded
column toward its old seat (which still needs a terminal stop), but releases F*2.3 = .23/2.3/23 Nmm for
F=.1/1/10 N. A stop without damping has not established benign impact/rebound.
At zero total downward load this unilateral cam supplies no seating preload.
A captured return adds contact; it is not silently granted. This is local
release/reseat only: once detached onto the moving plate, neither fixed ramp
arrests shared-drive power loss. E-153's energy distinction still applies.

## Finite shoe defeats the point-follower plateau

Construct two opposed annular sectors with r=1.75…2.25, shoe angle u=0….2 rad,
flat shoe top at h+1.2 and underside `h+k(u-.2)`. The grounded track occupies
phi=0…(.2+2.3/k), with top `k(phi-.2)` and material below. During selected
rotation phi=u+theta, h=k theta, the finite surfaces coincide exactly; reverse
motion retraces them. Opposed sectors remain disjoint. This constructs local
contact surfaces, not roots, a frame, dwell blend, complete gate or strength.

For k=10/24, shoe maximum thickness is **3.2/6.0 mm**, leaving **6.8/4.0 mm**
between 10-mm stations. Two sectors have .4 mm² projected contact area.
The selected release reaches 2.3 at **13.1780/5.49085°**; the desired capped
height path clears nominal/adverse cap prisms, respectively, but is **not**
realized by these finite cams.

After release, try theta=2.3/k+.1 while holding h=2.3. An interior shoe point
u=.05 is still over the fixed rising track and penetrates it by **1.0/2.4 mm**.
For every remaining overlap, support requires h≥k theta; at the last edge
contact, h reaches **4.3/7.1 mm**, then that track ends. A point follower would
miss this overrun. A flat dwell extension also requires a compatible follower
profile; it cannot be asserted from a commanded plateau. Changed profile,
extra axial travel or earlier load transfer requires new geometry.

Also, the fixed crest at z=2.3 lies strictly inside the lowest parked 4.6-square
cap, which occupies z=2…4. Crest points are (2.0452,.9380,2.3) and
(2.1523,.6560,2.3); neighboring interior ramp points give positive volume.
An extra cap standoff can repair this .3-mm nominal intrusion, but changes the
column envelope and does not repair friction or follower overrun.

## Board consequence and next decision

E-170's full-stroke separated-plate proposal already needs ten stations/cell.
Replacing each station's wings with two shoes means **128,000 shoe surfaces**
and **12,800 fixed ramp tracks**, plus existing guides and moving pickups;
these are features, not necessarily separate parts. No reduction in its 640
rotary channels at the conditional .1-s slot / 22.937-s allocation is earned.
Its <$0.391/channel ceiling with $250 elsewhere and free bought cells remains
an obligation, not a quote. More lift, maintained torque, ramps, standoff,
readback, false acceptance, retries and settling cannot be omitted from a new
schedule. Unchanged sites are stationary in the cap calculation; the parked
crest collision already prevents granting regional isolation to this geometry.

Stop detailed direct sliding-cam optimization and printing. Reopen only with
changed contact physics, cap geometry/decoupling, an actual finite handoff, or
process evidence that changes a comparative decision. Low friction alone does
not cure the two geometric failures; another friction sweep has low value.
Keep periodic common-datum pickup as a functional insight, not a selected
architecture. Broaden next toward **nonrotating columns with shared motion and
independently grounded retention**, comparing materially distinct contact routing
and physical addressing against E-098/E-099 and direct-head/screw controls.
Reject duplicates that merely restore the same two resident selectors; probe
only a new causal load/selection path. No new purchase, fabrication or CEO
permission is needed.

Self-review: independent nominal projection limit; continuous axial SAT intervals
against bisection and ±1-micrometre holdouts; 64/256/1024 angular grids including
near-onset samples; 16/64/256 finite-contact paths (maximum residual
3.45e−14 mm); force balance, zero-friction torque-work equality, frictional work
balance and a low-slope self-hold control. These verify reduced calculations,
not hardware. Warp, layer quantization, roughness, bias, anisotropy, root strength,
creep, wear and frame/guide compliance remain uncalibrated; no simulated
probability, reliability, force-tail or manufactured-fit claim is made.
