---
status: complete
builds-on: [E-179, E-178, E-176, E-173]
---

# Underside access separates pickup positions but retains the channel burden

**Stop further pickup-reader refinement as the primary architecture search.**
Direct underside viewing escapes E-179's depth alias, but the tested shared camera
is blocked at 19/20 cells. A scanning mechanical probe can cover actual pickup
clearance without 6,400 extra relays; its common endpoint still aliases a missing
probe, and clearance proof does not establish the next armed selection. Neither
route removes the setters or supplies ground support, keeper retention or arrest.
Keep both as conditional verification functions, not a selected machine.

Input main `d9367eb`; LAB-295. Reproduce:
`python3 tools/curated-experiment-checks/E-180/clearance.py` (standard library;
imports E-178 segment/box and motion routines). Evidence: finite rays and swept
boxes, interval bounds, counterexamples, ideal elastic stability and conditional
timing. Self-review only; no fabricated parts, optical rendering, contact dynamics,
measured process distributions, priced components or hardware qualification.

## Two different routes to actual output

Retain E-173's five-level rack, pickup lip and pad at deck home. The pad is
X=−2.2…−1.2, Y=q±.5, Z=−3…−2 mm, with q=0 active and 1.7 clear. Grounded
columns span heights 0…40.4. E-176's reset comb is parked. No failed keeper or
lane guide is reinstated by granting its output position here.

| Route | Complete functional boundary and result |
|---|---|
| Writer-carried underside optical reader | Existing setters select pad/ground state; deck transports; dogs retain terrain. Read the actual pad from below before ascent, retaining grounded support on ambiguity. Two Y viewpoints test access; one known-plane view already separates endpoints. Needs per-column optical access or slower XY scanning. |
| Writer-carried clearance rake | Existing reset clears pads; a shared Z axis raises 80 fingers under one row's potential pickup footprint. A blocked finger should inhibit permission; retract and index to the next row. Grounded dogs carry terrain throughout. Needs intact/stiff probes, actual endpoint gate, scan-completion memory and subsequent armed-mask proof. |
| Existing direct-head control | Heads address and move columns independently with positive retention; E-176 B4 timing 19.469 s. Capture, actual retained-support proof, lost-input arrest and bought cost remain open. It does not need this shared-deck pickup-clear function, but is not qualified. |

These are two independent verification moves: rotate observation into the plane
of output motion; replace observation with attempted occupation of forbidden
space. Neither is a new actuation principle. E-179 provides the comparison;
this result does not claim broad architecture-search saturation.

## Optical access: local success is not a shared camera

Camera centers lie at X=−1.7, Y=±2, Z=−50; pupil/registration X excursion is
±(.15+e), Y/Z registration ±e. Four pad-bottom sample points span X=−1.7±(.4+e),
Y=q±(.4+e), Z=−3±e. At e=0/.05/.1, **0/256 rays per scenario** intersect the
modeled obstacles. Neighbor spines, lips, all teeth, all ground-dog lanes, pads
and parked reset tooth/post/rail are included over all five heights and both pad
states in the surrounding 3×3 neighborhood. Inflated boxes permit coherent and
opposed local errors. Segment subdivision 1/4/16 agrees at e=.05.

The local X corridor is the reason: rays stay away from the spine and reset rail;
neighbor pads are above most of the ray and laterally separated at its endpoint.
This is access to sampled bottom points, not a full silhouette/contrast test.
An actual deck, pickup guide, keeper, reader housing, illumination and cables
remain unconstructed and may obstruct it. No transparency is granted to them.

For a single camera at Y=.85, Z=−50, projection to the nominal pad plane gives
`y_image=.85+47*(y−.85)/(z+50)`. Allow independent center/plane errors ±e and an
additional ±.1-mm aggregate image-registration/read error. The active and clear
center intervals have gaps **1.398/1.297/1.094 mm** for e=.05/.1/.2. Thus the
E-179 single-view alias is specific to its geometry; stereo is not intrinsically
required when displacement lies across the image and depth is bounded. This
endpoint calculation does not classify partially retracted or broken pads. A
clearance classifier must observe the near edge and include actual lip extent,
shape and localization error; command-center classification is insufficient.

Trying one direct camera at (46.56,.85,−50) for 20 columns blocks **19/20 center
rays in each state**, using actual h=0 spines. Only column 10 is visible. This
rejects that finite pose, not every shared optical arrangement. An 80-column row
writer could instead carry 80 local optical stations (320 at B4, 640 views if
stereo), with pitch/housing/controller cost still owed. No sensor was selected.

Reducing to 4/8/16 cameras and scanning assigned full rows in XY gives serpentine
path lengths 8,122.92/4,058.92/2,026.92 mm per camera. At the inherited hypothetical
200 mm/s, **40.615/20.295/10.135 s** are scan-only lower bounds, before acceleration,
exposure, return, verification or retries. Four cameras already miss 30 s alone;
faster travel, wider useful fields or overlap need new evidence. Do not append
these floors to a machine total and call them complete schedules.

## Mechanical coverage and what its endpoint cannot prove

A narrow finger spanning Y=±.2 misses a pad at q=.99, whose lower Y edge is .49.
That pad still overlaps the lip (Y up to .5) by **.01 mm** on ascent. This is a
concrete false-clear state even for perfectly rigid parts.

The broader finger spans X=−2.3…−1.1 and Y=±.7. Its 43.5-mm shaft rises 2 mm,
from tip Z=−3.5 to −1.5; the root remains below the deepest spine. A crossbar would
connect roots below Z=−45; its real drive, guide, stiffness and permission latch
are not constructed. The full shaft swept box and retracted row-scan envelope
avoid the known neighboring solids even after each body expands by .05 mm.
The nearest reset-post/rail X reserve is **.10 mm** under those expansions.
The swept shaft includes its lower root motion to Z=−47. All columns remain
on grounded dogs; the probe never reaches their lip at Z≥.95.

Independent edge errors ±e give continuous Y coverage reserve `.2−2e` beyond
the lip, and clear-pad gap `.5−2e`. 16 edge-sign combinations ×401 q positions produce
6,416 cases per scenario: **0 false clears at e=0/.05/.1**, but **188 at e=.2**.
These are deterministic test counts, not rates. At .1 the coverage guard is zero;
only .05 is checked for complete surrounding-body clearance. Coherent print,
assembly and local errors can oppose each other; no iid averaging is used.
Roughness, tilt, bow, wear and first-layer distortion must fit the declared edge
box. Layer quantization and actual X1C capability are not calibrated.

The proof depends on an intact physical chain. A missing finger plus an active
pad gives exactly the same **shared bar endpoint** as a clear pad. Reaching that
endpoint cannot diagnose the missing finger. Likewise, bar/finger compliance,
a displaced root, fractured pad fragment or lost permission linkage can defeat
a rigid collision argument. Individual integrity evidence or a different causal
interlock is still needed; a drive-position sensor is not that evidence.

For a 1.2×1.4-mm unbraced finger, L=43.5 mm, weak-axis I=.2016 mm⁴, the ideal
fixed-free Euler bound `π²EI/(4L²)` is **.131/.394/.789 N** for E=500/1,500/3,000
MPa. These E values are epistemic scenarios, **not sourced PLA/X1C properties**.
[MIT's column derivation](https://live.ocw.mit.edu/courses/16-001-unified-engineering-materials-and-structures-fall-2021/mit16_001_f21_pset12_sol.pdf)
supplies the ideal fixed-free formula; no printed-part capacity transfers from it.
An independent Rayleigh-energy integral for the first mode agrees at 16/64/256
subdivisions. Width sensitivity 1.0/1.2/1.4 mm is executable. Euler onset is not a
computed postbuckling escape or proof of false acceptance; contact may brace the
finger. It does deny a free rigid stop at arbitrary shared drive force. Under a
hypothetical factor-two reserve at low E, a **single blocked probe** permits less
than .066 N before that ideal bound is consumed, irrespective of 79 free probes.
Friction, moving weight/inertia, geometric imperfection, creep and drive limiting
remain unresolved. No detailed contact optimization is warranted by this screen.

Even perfect clear proof cannot certify the next selection: request pickups
(1,0), prove (0,0), then a wrong-address write produces (0,1). E-173's next deck
position d=3 lifts the unchanged column by **2 mm**. Keeping all probes inserted
would also obstruct intentionally active pads. Retracting them restores the
obligation to prove the armed mask and its retention; selective permissive gates
would be another mechanism. The rake is a home-clear checker, not a constructed
continuous travel inhibitor or a substitute for grounded-support proof.

## Full-machine disposition

Replacing E-176's .02-s row read with 2-mm probe approach/retract plus the same
.02-s completion allowance adds **1.680/.880/.480 s** at B4/B8/B16, including one
additional probe cycle for retry. Conditional dense totals are **23.174/14.007/
9.424 s**, versus broadcast optical allocations 21.494/13.127/8.944 s. Motion still
assumes 200 mm/s and 5,000 mm/s²; compliance/force limiting may invalidate it.
All existing preparation, return, support proofs and bounded retry remain in the
baseline; persistent jams halt acceptance. Regional scans retain E-176's touched-
bank penalty and add probe cycles per visited row. No disturbance claim follows.

B4 rake inventory is 320 reusable contact fingers, four added Z drives/guides,
shared bars and real permission/scan-state mechanisms. It can replace 320 clear-
reader functions **only if** integrity and transfer are solved. It leaves 6,400
pickup selectors, 6,400 ground selectors, 320 setters, support proofs and bank
arrest. Bought cost must include the complete original machine plus these parts;
there is no demonstrated <$500 BOM, print-time, assembly or durability advantage.
Broken probes are local hazards; bar bias, drive failure and lost scan association
are correlated hazards. Neither optical ray counts nor rigid-probe counts provide
a false-accept probability or board yield.

**Stop** this sparse-camera pose, narrow-finger checking, and common-endpoint-only
clearance certification. Retain underside observation and guarded broad probing
as conditional reusable functions. Reopen detailed work only if an architecture
supplies accessible outputs and removes enough repeated hardware to justify it.
No print or purchase: the present conclusions are geometric/causal, not missing
material calibration. The next research axis should eliminate temporary pickup
selection or merge it with permanent retention, comparing complete load and
addressing paths across existing direct, field-release and laminate controls.
Cross-check their prior failures before claiming a new topology; another mirror,
keeper or probe stiffness sweep would not change the current architecture ranking.
