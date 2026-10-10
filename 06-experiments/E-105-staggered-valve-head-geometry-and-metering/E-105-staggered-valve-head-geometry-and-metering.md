---
status: complete
builds-on: [E-104, E-060]
---

# Finite dry valve heads expose metering and return constraints

**Retain spatial hydraulic addressing conditionally; do not advance to a seal or
hardware pass.** Three staggered actuator lanes escape the tested body packing;
a short valve tail produces an actual head/gland collision. A longer tail clears
that subset, but return springs, grounded guides and real actuators remain
unimplemented. Fine metering cannot inherit E-104's ideal 400-mm/s closure.
A specified two-speed controller misses 30 s at an illustrative .2-mm height
budget and 2-ms response; .3/.5-mm budgets survive this timing calculation.
None is a product accuracy requirement or qualified control capability.

Input main `d063b8f`. Replay:
`python3 tools/curated-experiment-checks/E-105/finite_head.py`.
Evidence: generated primitive solids, deterministic reduced physics/control
calculations and self-review. No CAD kernel/contact dynamics, purchased actuator,
calibrated fluid, manufacturing distribution, independent review or measurement.
This is parameter/placement synthesis within one addressing family.

## Finite interface and limitations

The source generates a coaxial flat poppet, stem, seat, gland, shell and dry head
tip. At 5.08-mm pitch the cartridge outer diameter is 4.4 mm; shell inner radius
1.4 mm; port/stem diameters 1.4/.8 mm; disk radius/thickness 1.1/.4 mm; commanded
lift .35 mm. Seat occupies z=−.5…0; gland −1.8…−1.3; disk 0….4 when closed.
The .8-mm side supply port enters the intervening plenum. Its shell subtraction
is omitted in collision checks, conservatively adding solid. Flow reaches the
chamber through the stem annulus and seat curtain; it reverses for lowering.
The closed disk bears on a finite annulus r=.7…1.1. Sealing is not established.

A 1.2-mm dry tip contacts the .8-mm stem. With a tail ending at z=−2, opening
lifts the wider head into the gland: the final state overlaps in radius .5….6
and height −1.8…−1.65 mm. Extending the tail to −2.5 clears all 101 tested
lift states. Closure retraces this geometry **only if** a return element keeps
contact; no spring force or dynamic return is inferred. A spring volume is
reserved above the disk, not a generated spring. The gland's .1-mm radial gap
is geometric clearance and **requires a stem seal**; it is not a sealing fit.
This adds a second dynamic seal per cell alongside the piston seal.

The bank withdraws 1 mm before indexing. Its top then remains below every
closed stem for the whole row translation; opposing .1-mm vertical errors leave
.8 mm. Full tip-face capture permits only .2-mm radial registration error.
These are deterministic allocations, not X1C priors. Radial seat overlap,
whole-bank bow, guide wear and pressure distortion remain unqualified.

Allocated actuator boxes are 12×10×20 mm. One and two lanes collide; three lanes
14 mm apart give 15.24-mm same-lane center spacing. Independently rotating
1.2×3-mm lever solids occupy each column's x strip and connect y=0 tips to
actuator lanes y=0/14/28. A 4-mm output arm rotates 4.922 degrees. Actual input
strokes are **.339/1.544/2.750 mm**, so staggering does not preserve a universal
.35-mm actuator stroke. The generated lever bounds clear actuator bodies and
each other at 101 and 201 states. Continuous x separation and body/lever z
separation also cover asynchronous opening. Nine columns cover the repeating
layout; boundary brackets, wiring, rod guides, pivots and bank frame are not
complete solids. These boxes are allocations, not catalog components or proof
of assembly/support continuity. No complete finite head survivor is declared.

For a .5-MPa supply/chamber gauge range, dry stem and .8-mm stem diameter, the
ideal pressure force is `p_chamber*A_port − p_supply*(A_port−A_stem)`.
A closing spring needs **>.518 N** against forward differential; opening at the
opposite extreme needs **>1.288 N** before spring rate, drag and dynamics.
A simply supported lever with 32-mm span, 4-mm load position, 1.2-mm width and
assumed E=1500 MPa loses **.409 mm** at 1.4-mm depth or **.0416 mm** at 3-mm
depth. This beam bound omits guide/frame/contact loss and is not a material
prior. A thin lever cannot transmit the nominal lift under this load scenario.
The .35-mm stem sweep changes chamber geometry by .1759 mm³, equivalent to
.056-mm piston travel at 2-mm bore; this must enter transient volume accounting,
not be counted as inevitable final error while the port remains open.

## Flow and manufacturing/model uncertainty

The three serial restrictions have areas 1.0367 mm² (stem annulus), 1.5394 mm²
(full curtain) and .50265 mm² (side port). Sum pressure losses rather than using
the smallest area alone: `Δp = ρ Q² Σ[1/(Cd Ai)²]/2`. The orifice model is sourced
from [MathWorks' hydraulic-cylinder equations](https://www.mathworks.com/help/simulink/slref/single-hydraulic-cylinder-simulation.html)
(accessed 2026-10-10); it supports the equation, not our coefficients or geometry.
Here density=1000 kg/m³ and Cd=.4/.6/.8 are **assumed scenarios**. Line, viscous,
entry, compressibility and acceleration losses are initially omitted. The
nominal .1-MPa/Cd=.6 open-port calculation gives 1172 mm/s at 2-mm bore; it
neither delivers nor regulates the assumed 400 mm/s.

Unloaded lowering uses `(bias−drag)/A − .01 MPa` as available valve differential.
Across 18 bore/net-force/Cd cases at each of .15/.35-mm lift (36 total), an
example with net .1 N, Cd=.4 and .15-mm lift reaches only **314 mm/s at 2-mm
bore, 61 mm/s at 3 mm**; .02 N cannot overcome backpressure at either bore.
Net .3 N gives 621/170 mm/s respectively. Shared net bias/drag and backpressure
can therefore invalidate the ideal timing case. There are no probabilities or
claims that these forces, viscosity or coefficients represent the printer.

At .1 MPa/Cd=.6, a 75-mm/s slow approach needs a **.00633-mm curtain gap** in
the inertial model. Combined opposing seat/actuator zero errors are added as
bounds, not RSS: ±.005 mm gives 15.7…133.7 mm/s; ±.01 mm gives 0…191.5 mm/s.
Common errors affect the whole row, not independently averaged cells.
This gap prediction is strongly model dependent: adding radial parallel-plate
seat loss `6 μ Q ln(1.1/.7)/(π h³)` moves the required gap to
**.0137/.0278/.0591 mm** for μ=.001/.01/.1 Pa·s. This is a competing loss model,
not calibrated CFD; inlet development and flow regime remain uncertain. It
prevents treating the 6-micrometre result as a universal physical exclusion.
No fixed fine gap is qualified; no fabrication is requested to chase it yet.

## Two-speed control and decision

Use E-104's overhead, two pressure directions and one conservative row recovery.
For diagnostic height budget e, read error r=.05 mm and response bound τ, define
slow speed `(e−r)/τ`, reserve terminal band `400τ+r`, and charge an additional
stopped transition of τ. Each uniform phase executes fast then slow travel,
with each segment bounded by both channel speed and total flow. The full-stroke
81 direction splits are evaluated, including both directions in the recovery.
This is one explicitly conservative controller, **not** a universal lower bound:
it reserves the entire band at slow speed and charges a stopped transition.
It does not solve heterogeneous arbitrary-stroke synchronization or pressure
control. The narrow 30.032-s miss alone does not reject the hydraulic family.

| Bore / flow | τ | e | Worst modeled time |
|---|---:|---:|---:|
| 2 mm / 8 L/min | 1 ms | .2 mm | 28.682 s |
| 2 mm / 8 L/min | 2 ms | .2 mm | **30.032 s** |
| 2 mm / 8 L/min | 3 ms | .2 mm | **32.246 s** |
| 3 mm / 12 L/min | 2 ms | .2 mm | **30.972 s** |
| 2 mm / 8 L/min | 2 ms | .3 mm | 29.298 s |
| 2 mm / 8 L/min | 2 ms | .5 mm | 28.808 s |

Checks reconstruct pressure independently in SI, verify zero-flow and
area/pressure/bore scaling, the zero-viscosity limit, exact lever surface lift,
short-tail collision, lane rejection, sampling refinement and the fast=slow
schedule limit against E-104. Reduced equations remain unvalidated physics.

**Decision:** stop assuming that a cheap dry head provides precise analog valve
lift. Preserve this geometry as a conditional packing route and its unique
short-tail failure. Before completing its mechanical return/guide design,
compare full-open binary actuation with shared coarse/fine pressure phases
against independently throttled heads, explicitly charging synchronization,
load-dependent lowering and extra cycles. A coarser diagnostic accuracy budget
must remain visible; do not silently adopt .2 mm as a hard requirement.
Continue only if that comparison leaves credible time/force/channel-cost space;
then implement finite preload/return, grounding and bidirectional closure.
E-104's coupled $500 budget remains unchanged and no bought-part price has been
established. The extra 6,400 stem seals weaken, rather than establish, economics.
No printing, purchase, architecture acceptance or physical qualification.
