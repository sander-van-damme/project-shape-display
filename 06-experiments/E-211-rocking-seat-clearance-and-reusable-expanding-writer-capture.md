---
status: complete
builds-on: [E-210, E-209, E-208, E-206, E-056]
---

# Wider rocking seats clear; miniature writers expose force and construction limits

**Retain the uncut toe with explicit rack-web contact as the simpler conditional
control. Stop developing this shortened toe and do not promote the four-shoe
writer into a machine design.** A chamfer retains support but does not eliminate
web contact; its freer released pose conflicts with the inherited rack jaw.
Wider sockets, a bowed registration move and a shorter withdrawal produce a
finite planar sequence. Positive tool capture with clearance is geometrically
possible, but this construction moves four precision sliders into every writer
head. Its thin stem demands 302 MPa nominal bending stress and up to 4.12 GPa
in bounded stock/root holdouts under the elastic model. It does not establish
an affordable, durable writer or select rocking.

Input main `aaf3417`; LAB-338. Evidence: deterministic finite convex prisms,
frictionless local elastic/contact calculations and self-review. No physical
measurements, process distribution, independent reviewer, purchases or fabrication.
Run `OPENBLAS_NUM_THREADS=1 python tools/curated-experiment-checks/E-211/fit.py`
with NumPy/SciPy; `--suite released|sequence|fit|verify|holdouts` runs a subset.
Tested NumPy 2.5.4/SciPy 1.18.1, installed in disposable run scratch. JSON is
reproducible output, not retained evidence. E-210 gains only a default-compatible
finite-body reconstruction hook; its original verification still passes.

## Seat synthesis and released equilibrium

Retain E-210's released y/z/pitch and rack-height coordinates, unbiased root
registration, nominal (L,a,t)=(12,.3,.4)-mm return and assumed E=2200 MPa.
Retain its rack guide force/couple obligation, rod energy and finite contact
reaction reconstruction. No toe guide, friction or extra keeper is supplied.
Compare three convex toe bodies: original y≤1.6; shortened y≤1.35; and chamfer
`y+.15z≤1.6`. The chamfer removes .3 mm at the upper front corner while preserving
the bottom front bearing. Pad, keys and return attachment remain fixed.

Socket end play changes from .07–.13 to **.17–.23 mm**, with coherent translation
±.05 and key depth .15–.25. These are assumed geometry bounds, not X1C capability.
The exact front-key excursion `hypot(2.15,.25)−2.15=.014486 mm` leaves
**.105514 mm** worst release reserve, versus E-208's .005514 mm. The rear key
edge moves inward until clear. Sixteen shape/fit combinations check 2,080 finite
rock/withdraw poses independently of the released optimizer. Increasing play
reduces front bearing: at the worst corner the uncut/chamfered toe has .17 mm
of seated overlap; shortening leaves an .08-mm gap instead of that bearing.

The 54-case released screen combines three shapes, two coherent fit corners
(.17,−.05,.15)/(.23,+.05,.25), root offsets (−.1,+.1)/(+.1,−.1)/(0,0), and
W=0/.1/10 N. These loads are comparison scenarios, not new requirements. This
is a sampled local branch, not a full Cartesian manufacturing distribution.
Root and seat biases may repeat across a 40-finger comb or bank; no independent
cell error or board-yield model is implied. These uncalibrated bounds and the
rigid contact/elastic-rod assumptions remain separate sources of uncertainty.

| Shape | Reconstructed equilibria / attempted | Minimum key embedding | Consequential finding |
|---|---:|---:|---|
| Original web-contact toe | 18/18 | .0500 mm | Two light-load cases use the web |
| Shortened toe | 14/18 | .0500 mm among solved states | Four 10-N cases reach the −.12-rad search bound; no reaction credited to that bound |
| Chamfer | 18/18 | .0500 mm | Two light-load states still touch web at the lower front corner |

Web/chamfer rack rise spans approximately 0–.1000 mm; released strain reaches
.6748%. No height-error acceptance limit is inferred. One chamfer solve reaches
its iteration limit: its actual finite contacts balance within 5.21e−6 N/N mm
and sampled feasible energy perturbations find no descent. This is labelled
an independently reconstructed local certificate, **not optimizer convergence**.
Other accepted cases converge. Maximum accepted balance residual is 5.21e−6;
penetration tolerance is 2e−7 mm. Shortened-toe bound hits remain unresolved
outside this local branch, rather than proof that every shortened design fails.

At nominal seat fit and root (−.1,+.1), W=.1 N, n=32, original/chamfered toes
have rack rise .023712/.024195 mm, key embedding .185594/.185275 mm and web
reaction .004230/.000240 N. For load y=.8/1.2, rack-guide couples are
−.020518/+.019482 and −.021908/+.018092 N mm. Chamfering greatly reduces this
small normal reaction but cannot remove the guide or web from the model.

## Writer alternatives and bounded fit

Replace the .3×.4-mm exact-fit blade pocket by a nominal .8×.8-mm cavity at
y=−.85…−.05, z=.6…1.4, x=−1.5…−.9. Its .4-mm-high mouth has .2-mm axial lips.
A collapsed tool enters from −x, then expands behind those lips. The blind back
blocks inward escape; expanded shoulders block outward escape after .05 mm of
axial free play. Finite tests distinguish free motion at .04 from interference
at .08 mm. This is axial retention with lost motion, not a rigid six-axis clamp.
The rear pocket wall is only .15 mm nominal, **.10–.20 mm** under the stated
y-wall errors, and the mouth lips are .2 mm thick. These occur at all 6,400
toes, not only in the shared tool. Stage 02 does not qualify such features with
either nozzle; no wall strength, printability or wear pass is claimed.

| Tool | Actual frictionless planar reaction span | Disposition |
|---|---|---|
| Undersized fixed blade | Rank 0 while clear of all walls | Clearance gives no prescribed toe control |
| Opposed z shoes | Rank 2: vertical force and pitch | No y reaction; cannot impose the withdrawal path |
| Four independent y/z shoes | Rank 3; all six signed unit wrenches have nonnegative reactions | Conditional geometric capture; four driven slides and their force control are owed |

The four-shoe model has .1-mm-thick z shoes, .5-mm y bearing span and a
.4×.12-mm stem. Explicit telescoping **envelopes** connect each shoe to the stem;
these are space allocations for independently guided drives, not constructed
actuators, bearings or locks. Finite contacts furnish the actual rod wrench at
all tested states. No friction or load capacity is assigned to the envelopes.

Sixteen combinations of independently bounded ±.05-mm pocket-wall errors require z strokes .25–.35 and
y strokes .15–.25 mm. All insert, expand and retain in the tested released pose.
All 128 additional collapsed-insertion pose corners (y/z ±.05 mm, pitch ±.02 rad)
clear. The initial .6-mm shoe span failed combined pocket/pose errors; narrowing
to .5 mm fixes that control and increases pitch-reaction demand. The source
preserves a failing .6-mm witness. Mouth and x-depth errors, angular wall errors,
roughness, warp and actual closure from a misregistered head are not covered.

Closure travel is computed to each actual wall; it therefore requires individual
contact-seeking/force-limited drives. The sequence follows the computed toe pose;
pose acquisition and readback are not implemented. It does not silently replace
the original exact blade fit by manufactured exact dimensions, nor establish
six-axis closure. Roll/yaw and one-sided load transfer remain unmodeled.

## Supported sequence and newly exposed failures

The sequence holds the released toe, acquires the rack with a C-jaw, lifts it
1.5 mm, registers the toe, rocks .22 rad, withdraws, changes rack height, reverses,
restores the released equilibrium, lowers the rack onto its pad and contracts/
withdraws the toe tool. Rack load stays on the jaw while the toe is unseated;
final released equilibrium supplies the support-transfer certificate. Reverse
insertion/contraction is a quasistatic geometric witness, not passive reseating,
power-loss arrest or dynamic proof. C-jaw closure still inherits E-207's exact
rack-thickness grant and is explicitly outside the solved toe-tool fit.

Three inherited/simple choices fail:

- Straight interpolation from the released pose to the seated datum cuts into a
  ledge. Add `z=.02 sin(pi f)` to that interpolation and its reversal.
- The 1.4-mm withdrawal puts the rear top toe corner **.006459 mm into the
  preceding rack web** at row spacing 5.03 mm. E-208's nominal spacing check
  and E-209's leaf-only row-error check did not cover this combination. Retain
  the failure. Withdrawal 1.2 mm restores .193541-mm rear-web separation.
- Shortened/chamfered light-load poses move the rack pad into the inherited
  y=1.35…1.65 C-jaw. Moving/narrowing it to y=1.45…1.68 clears the sampled case,
  but increases its required opposing reactions.

Original and chamfered toes have **.262667 mm** open rack projection clearance
at 1.2-mm withdrawal. Exact vertical swept prisms cover all twenty unequal
five-height transitions across 40 mm, including jaw travel. Stationary neighboring
rows at −5.03/+5.13 and columns at ±5.08 remain in the collision comparison.
The original toe can retain the old jaw with the .02-mm bow and 1.2-mm withdrawal;
this is the preferred comparison construction. The chamfer needs the shifted jaw.

For a 10-N load at y=.8, using contact points inset .05 mm from each jaw end,
original/shifted jaws need **40/30 versus 63.846/53.846 N** upward/downward
reactions. At most .75×.30/.23 mm² of gross contact area gives mean lower-jaw
pressure **177.8/370.1 MPa** for those chosen reactions. Actual pressure can be
higher; these are conditional calculations, not material allowables or hardware
failure measurements. Crediting a rack-guide couple could reduce jaw forces but
would transfer the requirement into a finite qualified guide instead.

At n=32, the nominal return with root (−.1,+.1) on the changed path reaches
1.96274% fiber strain, .51397 N return force and 2.08285 N at a tool contact
(E=2200). Reducing withdrawal does not remove the rocking strain peak. E-209's
broader ±.1-mm root tails remain 2.247/3.188% for nominal/short-thick stock; its
−.2-mm tensile edge remains 3.44/4.31% and 2.41–7.56/4.71–14.80 N across modulus
bounds. Those old-path numbers are controls, not newly bounded maxima for every
modified path. Tensile bias is not reinstated.

For both retained shapes, 32→64 rod segments and phase subdivisions increase
sampled poses 259→515 and change peak strain 1.96274→1.96495%, return force
.51397→.51725 N and tool contact peak 2.08285→2.08784 N. Released-coordinate
changes are ≤2.00e−5 mm/rad; both refined paths clear. Feasible released-pose
perturbations find no descent. This refines these cases, not all fit corners.

The actual .4×.12-mm stem has section moduli .4×.12²/6 and .12×.4²/6.
Taking a favorable .55-mm force arm from shank to the nearest shoe edge gives
`sigma=.55*(|Fz_local|/(.4*.12²/6)+|Fy_local|/(.12*.4²/6))`.
The nominal refined path demands **302.4 MPa** peak gross-section bending stress.
This force-only beam calculation omits pitch-torque transfer as stem torsion,
drive cutouts, stress concentrations, compliance and the shoe/lip pressures;
it neither establishes a material failure nor qualifies a metal replacement.
The rigid finite-clearance witness cannot be promoted without constructing and
checking this load path. Larger sections compete with collapsed insertion fit.

Three n=32 chamfer/shifted-jaw stock holdouts also clear the sampled sequence,
but increase the demands. All use E=2200 MPa and W=.1 N:

| Return (L,a,t), root offset (mm) | Peak strain | Return force | Stem bending demand |
|---|---:|---:|---:|
| (12,.3,.4), (+.1,−.1) | 1.964% | 2.410 N | 1,420 MPa |
| (11.5,.25,.45), (−.1,+.1) | 2.222% | .879 N | 515 MPa |
| (11.5,.25,.45), (+.1,−.1) | 2.893% | 7.001 N | 4,119 MPa |

These are linear-elastic return/beam demands, not achievable stresses or measured
forces after yielding. They expose sensitivity hidden by nominal fit. A new
writer must address force tails and compliance, not merely replace its material.
The 1,420/4,119-MPa cases peak at full withdrawal, where the toe has ≥.25096 mm
frame separation and the rack is clear; no seated bearing shares that demand.

## Verification, limits and decision

Self-review includes independent key-excursion algebra, actual convex geometry,
nonnegative contact-wrench reconstruction, failed blade bases, failed wide-shoe
insertion, the rear-rack collision control, and E-209's straight-bar, energy/work,
Jacobian and extensible/inextensible limits. The 2,080 finite release checks pass;
energy/work error is 3.85e−10 and residual-Jacobian error 2.32e−9 in their model
units. Rod/phase refinement and stock holdouts are reported above.
No continuous whole-path certificate, calibrated material law, contact pressure
solution, creep/fatigue, manufacturing yield or board reliability follows.

The wider seat is useful geometric progress. It retains 6,400 returns, toes and
pockets, 12,800 keys/socket interfaces and the assumed 160 comb placements.
The four-shoe tool adds 4H guided outputs for H heads: 160/320/640 at H=40/80/160,
besides y/z/pitch motion, insertion, rack takeover, height drive, readback and
recovery. It has not demonstrated a cost advantage over E-054/E-056's 6,400
separate slider fits, nor over E-206's longer torsion lead with yaw retention
still owed. No new motor, sensor, controller or assembly operation is free.
With $250 spent elsewhere, a $500 ceiling leaves <$6.25/$3.125/$1.5625 per head
at H=40/80/160 even before residual resident purchases. These are allocation
bounds, not quotations. With the inherited illustrative 6-s map overhead, the
same heads must complete each selected cell in strictly <.15/.30/.60 s including
acquisition, motion, settling, proof and retry. No timing or regional-disturbance
pass is claimed.

**Redirect from incremental pocket refinement to the complete reusable writer
load path and construction burden.** Compare an accessible larger external
capture/tool with the miniature expander and slider/longer-torsion controls.
Retain the uncut/wider-seat/1.2-mm-stroke construction as an input, not a selected
machine. Reopen the chamfer only if another acquisition topology removes its
jaw penalty; reopen shortening only with restored finite support. Stop a writer
embodiment if its six-axis restraint, stress or drive packing requires resident
precision guidance or cannot plausibly fit head cost/time allocations. Do not
request printing: those missing functions are more consequential than another
nominal leaf calibration. No new fundamental principle or search saturation is
claimed.
