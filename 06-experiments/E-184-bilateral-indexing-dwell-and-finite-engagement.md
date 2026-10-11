---
status: complete
builds-on: [M-006, E-139, E-146, E-147, E-154]
---

# Bilateral dwell locks need finite handover clearance and input arrest

**Retain Geneva indexing as conditional bilateral parked memory; stop treating it
as a one-step outage limiter.** The new result is an exact full-pin handover window
and its clearance/backlash tradeoff. Nominal geometry admits overlap; coherent
errors can erase it. Even a perfect dwell lock grounds output torque without
stopping the input from initiating another index. No machine or fabrication selected.

Input main `465513f`. Reproduce: `python3 tools/curated-experiment-checks/E-184/indexing.py`.
Evidence: finite circular-pin/straight-slot sections, parked contact normals,
analytical energy bounds and deterministic synthesis. Self-review only. No complete
relieved locking-disk geometry, contact dynamics, process calibration, physical
measurement, purchased BOM or reliability claim. Generated JSON is disposable.

## Comparison and changed question

The compass suggested rack escapement versus captured indexing. E-146 already
constructs bilateral rack pockets: fixed selector bounds a packet, repeated
selection renews travel. E-139 constructs a finite captive cam and shows dwell
coast-through; E-154 already tests passive damping. Repeating those models would
add no evidence. This probe instead tests **finite engagement before releasing a
bilateral rotary dwell lock**, then uses the earlier energy result as a control.

| Combination | Selection / energy / retention / load / recovery |
|---|---|
| Bilateral rack pockets, E-146 | Independent drive and selected alternating bolts; column webs return force to grounded bolts. Fixed selector limits travel; repeated switching defeats nonrepeat. Needs separate accurate parked support, actual top/support proof and supported retry. No new pass. |
| Captive cam, E-139 | Selected translating plate, bilateral roller groove and grounded slide. Dwells hold vertical load; free input traverses dwell. Shared versions need retained pickup and service support. No new pass. |
| Resident Geneva + rack | Reusable reversible rotary head selects a resident driver; its pin indexes a slotted wheel rigidly coupled to a rack pinion. Lock disk/pads ground either output torque sign in dwell. Actual height, resident driver phase and loaded seating must be proved before undocking; failed proof retains the head. Passive input arrest, retained dock and the reader remain counted obligations. |

A resident drive disk is essential to this version's parked support: withdrawing a
head carrying the only lock disk would remove retention. Replacing 6,400 disks with
shared ones therefore needs another parked lock. A stuck powered head can cycle the
indexer indefinitely; phase readback is not a physical stop. Unchanged resident pairs
can stay locked, but head access, rack layout and shared-frame disturbance are unsolved.

Source-domain search: machine-tool Geneva detents, separate from the prior energy
packet search. [US4317385A](https://patents.google.com/patent/US4317385A/en) describes
paired abutments, concentric locking surfaces and continued restraint during finite
pin entry; it also identifies backlash and an uncontrolled interval in earlier
arrangements. [US3546958A](https://patents.google.com/patent/US3546958A) uses rollers
and a precision groove for dwell locking. Accessed 2026-10-11. These motivate the
handover test, not miniature manufacturing or performance. This is a recombination
of M-006, not a new indexing principle. One new search axis; no saturation claim.

## Constructed pin/slot geometry and bilateral parked reaction

All dimensions are assumed millimetres. Output axis O=(0,0), driver D=(C,0), n slots,
crank radius `r=C sin(pi/n)`, half-index input angle `alpha=pi/2-pi/n`.
The pin center and active zero-clearance output angle are

```
P(theta)=(C-r cos(theta), r sin(theta)); phi=atan2(Py,Px)
phi'=(Cr cos(theta)-r²)/(C²+r²-2Cr cos(theta))
-alpha <= theta <= alpha; output step=2pi/n
```

Nominal n=4, C=6, pin radius a=.5, side clearance g=.1. Each radial slot has
straight inner side faces at ±(a+g), mouth radius `rho_e=C cos(pi/n)` and bottom
radius `C-r-a-.2`; material outside the sides is solid. Disk/finite-face separation
is checked at 1,001 held-output handover poses. Nominal centered active poses are
also checked at 1,001 phases; partially inserted entry/exit poses are **not**
credited as full-pin support. Slot webs, teeth, hubs and surrounding solids are
not constructed. This is a finite contact section, not assembly CAD.

An independent parked section uses driver disk radius 2 and two radius-.5 circular
pads attached to the output, at `D+2.5*(-cos30°, ±sin30°)`. Each disk contact normal
passes through D: **zero input moment**, output moment arms **±3 mm**. Compressive
contact on the appropriate pad can oppose either output torque; the grounded driver
bearing returns the force. At 10 N and the 1.27324-mm rack radius below, one pad
needs 4.244 N. No down-bias spring is needed for this ideal bilateral dwell.
The driver phase is neutral: support persists only inside its dwell sector;
vibration-induced phase drift and a resident phase detent are not qualified.

These pads occupy a separate axial plane from the drive pin. A relieved disk must
remove them during indexing and restore contact at exit. Its complete contour,
bridges, engagement edges, lock clearance and manufactured preload are **unbuilt**.
The pad witness proves a possible parked reaction, not compatible swept geometry.
Failure of the following full-pin gate rejects only a held-output, full-insertion
handover with these straight sides. Partial-pin tip support, compliant/preloaded
locks or altered cam profiles require different contact models; they are not ruled out.

## Exact handover synthesis and manufacturing bounds

Hold the output at entry angle `phi=-pi/n`. Advance input by delta. Project the actual
pin center onto the held slot axes. Inward insertion and lateral displacement are
exactly `d=r sin(delta)` and `t=r(1-cos(delta))`. Full disk entry requires `d>=a`;
nonpenetration against the held side wall requires `t<=g`. Finite disk size matters:
point-pin tangency at delta=0 does not establish supported handover.

Explicit uncertainty box: pin radius grows e, slot half-width shrinks e, tangential
registration may shift e, and radial mouth registration may shift e. Use the
adverse common bounds `a_eff=a+2e`, `g_eff=g-3e`. Timing error is independently ±1°.
A robust release command exists for this stipulated handover only if

```
asin(a_eff/r) + 1° <= min(acos(1-g_eff/r), alpha) - 1°
```

Negative g_eff means no robust side fit; it is not an inverse-cosine input.
The calculation is a conservative coherent box, not an inferred X1C distribution.
The same geometry applies to exit and reverse operation by reflection.

| g (mm) | e (mm) | Full-entry angle | Side-limit angle | Command-window width |
|---:|---:|---:|---:|---:|
| .10 | 0 | 6.768° | 12.465° | 3.696° |
| .10 | .025 | 7.449° | 6.223° | −3.226° |
| .20 | .025 | 7.449° | 13.943° | 4.494° |
| .20 | .050 | 8.130° | 8.805° | −1.325° |

For e=.05 at g=.1, or e=.1 at either gap, robust side clearance already fails.
These signs are design discriminators, not failure probabilities. Timing at zero
error is more favorable; no supplied actuator/edge manufacturing establishes ±1°.

Enumerate n={4,6,8}, C={4,6,10}, a={.3,.5,.8}, g={.025,.05,.1,.2}: **108 geometries**
per error bound. Full-pin-window survivors at e=0/.025/.05/.1 are **61/21/6/0**.
These are necessary-condition survivors for this handover specification, not
assemblies. They do not check all slot bottoms, web strength or relieved contours.
The short script is an evaluator, not a broad architecture search or optimizer.

A nominal 2-mm rack step requires pinion radius `R=s*n/(2pi)`. With n=4, slot-only
angular freedom at fixed input is `±asin(g/rho)` and rack span is twice that times R.
At entry/mid-index, g=.1 gives **.0600/.1450 mm**; g=.2 gives **.1201/.2904 mm**.
These spans exclude rack backlash and lock clearance; at entry the pin is only
partially inserted, so the figures describe side-angle freedom, not qualified
support. A signed load change can exchange flanks. No height-error acceptance is
invented. More clearance repairs entry tolerance while worsening motion/readback.

Common pin/slot shrink, warp, shaft spacing, layer quantization, hole bias and
assembly registration can affect a whole printed bank. Local scatter is unknown;
no averaging or independent-cell yield is used. Roughness, friction, compliant
cam-out, orientation strength, creep, fatigue, wear and contact stress remain
unmodelled. The .4/.2-mm nozzle process is not qualified by these ideal sections.

## Ideal free-input counterexample, separate from finite-clearance geometry

Grant perfect zero-clearance bilateral engagement and locking, positive input
inertia J, output inertia I, and no damping. This is a favorable separate model:
`K=.5*(J+I*phi'^2)*theta_dot²`. During index, signed work adds `F*R*dphi` in the
load-assisted direction. At both index boundaries phi'=0, so output speed becomes
zero while **all remaining kinetic energy resides in the input**. Lock engagement
need not dissipate energy in this ideal limit. During dwell the lock reaction does
zero input work, and the input coasts to the next entry.

From a cut at mid-index, rest, F=1 N, s=2 mm, the remaining 1-mm descent gives
**1 mJ** at the next dwell. With J=1e-6 kg m² and n=4 the input crosses its 3pi/2-rad
dwell in **.10537 s**. At 10 N this is 10 mJ and .03332 s. Each subsequent complete
load-assisted index adds F*s: no one-step geometric outage bound follows. At F=0,
1.25 mJ crosses the dwell in .09425 s; at zero force and zero velocity it stays put.
Exactly stationary entry is also not credited with spontaneous initiation.

Reversing input and load sign reflects the trajectory. Against a 1-N load, initial
1.25 mJ at midpoint leaves .25 mJ at the first dwell; later uphill steps may be
unreachable. Negative calculated endpoint energy means a turning point, **not**
a continued trajectory. The executable checks these distinctions at signed
F=−10/−1/0/.02/1/10 N and K0=0/1.25/12.5 mJ. Finite backlash creates impacts and
possible losses, but no measured minimum dissipated work is available to credit
as arrest. A brake, nonrepeat stop or qualified sink changes the mechanism;
E-147/E-154 retain those obligations. No acceptable outage travel is asserted.

## Full-machine screen and disposition

At C=6, s=2, F=10 N, n=4/6/8 give peak quasi-static pin forces
**7.245/6.366/6.875 N** and peak input torques **30.739/19.099/15.786 N mm**.
These omit acceleration, wear and friction. All require **20 input turns/40 mm**;
more output slots do not reduce input cycles at fixed height step. Increasing n
also enlarges the rack-pinion radius: 1.273/1.910/2.546 mm, before teeth/housing.
C=6 already exceeds top pitch internally; tiers/routing are allowed but unsolved.

Assume .10 s/site dock/read/seat-proof/withdraw plus 6 s/map preparation, transport,
registration, final proof, settling and bounded retry. Grant constant input speed,
no acceleration or extra reset. For all 6,400 sites changing 40 mm:
`T=6+ceil(6400/H)*(.10+1200/rpm)`.

| rpm | T with 80 heads | Minimum heads for strict <30 s | $250/head-pool allocation |
|---:|---:|---:|---:|
| 600 | 174 s | 582 | $.430/head |
| 1,200 | 94 s | 305 | $.820/head |
| 2,400 | 54 s | 165 | $1.515/head |

The allocation assumes free resident parts and $250 for everything else under the
$500 ceiling; it is not a priced BOM. At $400 only $150 remains jointly for heads
and resident purchases; the $200 ideal is already exceeded by the assumed reserve.
Count at least **12,800 resident rotary axes**, 6,400 pin/slot pairs of members,
6,400 lock interfaces, rack meshes/guides, head docks, drives, arrest and sensing.
Two discrete pads per site add 12,800 pad elements; integral pads avoid assembly
parts but retain wearing precision surfaces. Four-slot wheels repeat 25,600 slots.
Shared versions reduce indexer count only by restoring separate cell retention.
Printed volume/time and life are unknown without full geometry; even one 10-s
site assembly operation totals 17.8 hours. Bought resident content alone has
<$.03906/site with the assumed reserve and free heads.

Raising uniform 1/10-N loads needs at least 256/2,560 J per field; lowering needs
absorption. The quoted time is conditional, not a performance pass. A reader must
observe actual height and support, not infer both from input turn count. False
acceptance, common registration errors, jam detection and supported retry remain
unspecified; no map reliability follows. Persistent failed proof keeps the head
captured and requires supported service, outside a successful-map timing claim.

Self-review: transformed Cartesian centers agree with the exact insertion identities
to 1.8e−15 mm; finite-face tests include interval endpoints; parked moments are
reconstructed from normals. Independent trapezoidal phi' integration errors at
64/256/1,024 intervals are 1.004e−4/6.275e−6/3.922e−7 rad. Finite-difference
phi' error is <6.7e−11; signed work and integer scheduling checks pass. There is
no time integrator or claimed impact simulation requiring time-step convergence.

**Decision:** close this screen. Do not detail a nominal four-slot lock or print.
Reopen with a swept relief/lock geometry surviving a justified error box, actual
input arrest and a complete cost/schedule advantage. Keep the finite handover model
as reusable negative/conditional knowledge; reject neither all Geneva mechanisms
nor the broader escapement principle.

**Next discriminator:** compare motion-profile/ratio synthesis across continuous
screw, intermittent indexer and direct linear setter controls. Prior screens use
constant rpm despite very different output velocity/acceleration ratios. Bound
motor torque-speed, reflected inertia, regeneration/lowering and readback overhead
together; ask whether physically admissible nonuniform profiles change required
head count enough to justify any finite lock/capture construction. Read E-131,
E-154 and E-181 source first. Stop if improvement requires free acceleration,
braking, perfect readback or an unpriced transmission. This changes the comparison
method, not the selected architecture; no CEO-owned boundary arose.
