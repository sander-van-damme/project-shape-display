---
status: complete
builds-on: [E-145, E-144, E-139, E-079, E-142, E-129]
---

# Finite output packets need a nonrepeating reset and a real impact path

**Retain a conditional bilateral catch construction; stop output-refreshed release.**
Wider staggered pockets escape E-129's disjoint insertion windows. A seated selector
bounds free output travel, including reversal, without relying on motor restraint.
But shared cycling releases a failed head repeatedly: twenty refreshes permit 40 mm.
Output seating alone cannot authorize another packet. No complete machine, accepted
outage displacement, fabrication candidate or hardware reliability is established.

Input main `2eb573f`; LAB-246. Reproduce with Python 3 standard library:
`python3 tools/curated-experiment-checks/E-146/permission.py` (disposable JSON).
Evidence: generated rectangular solids, exact interval certificates, finite state
counterexamples and lumped elastic impact bounds; self-review, no external review,
calibrated process prior, assembly CAD, physical measurement or purchased BOM.

## Different encodings and their causal limits

All combinations retain spatial selection, independent reversible drives, 6,400
parked supports/returns and actual output/support proof. A catch must intercept the
column **beyond capture elasticity**. A slotted extension on a head upstream of its
pickup does not satisfy this. Direct column extensions repeat at 6,400 sites; fitting
this section there or reaching them from reusable heads remains unproved.

| Encoding | Closure / support cause | Stuck OPEN, signed motion and reset |
|---|---|---|
| Duration-held OPEN, E-144/E-145 control | Remove opening force; local spring closes | Persistent command defeats closure; no excursion bound from time alone |
| One-way output run-off | Output drives follower off a finite ledge | Reverse motion away from the edge never trips; periodic ledges reopen. E-079's command trip supplies neither load support nor a reset guard |
| Absolute-travel meter + one-shot trip | Mechanical rectifier spends a finite travel budget; trip disconnects opening linkage | Reversal cannot restore budget; zero-speed dwell does not spend it, but later motion does. Rectifier, latch, return, finite closure and loaded catch are additional, unbuilt parts |
| Captive finite-stroke shuttle | Output pulls a captured member between grounded end stops | Both signs bounded while connected. Recenter only under another grounded support; automatic recenter supplies unlimited packets. E-139 already exposes stop energy |
| Alternating long pockets, constructed below | At least one ground-guided bolt stays inside a finite bilateral pocket | No timed closure or speed threshold. Fixed selector bounds motion; repeated selection refreshes it. Arbitrary target heights still need separate parked support |

These are recombinations, not new physical principles. Two genuinely different
search moves: invert narrow indexed holes into **overlapping finite motion windows**;
and examine industrial single-cycle anti-repeat as a reset requirement. [OSHA's
press definitions](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.211)
separate anti-repeat, requiring release of the initiating control, from the brake
that stops/holds the shaft (accessed 2026-10-11). This is a functional analogy, not a
claim that press regulations apply to this product or that a press clutch scales.
No broad saturation claim. E-139/M-004 already cover escapement principles.

Executable meter witnesses use a 2-mm budget: −10-mm travel never exhausts the
positive-only counter; ±.1-mm oscillation over 20-mm total path never exhausts a
signed counter. An absolute counter trips after 2-mm path in either case. One hundred
zero-motion samples leave it armed; subsequent motion trips normally. This corrects
E-144's coarse treatment: stationary dwell is not by itself a displacement-bound
failure. A finite **two-sided** window tolerates indefinite oscillation inside its
window; a cumulative path budget additionally limits wear, but needs a rectifier.
These logical counters grant ideal trip detection only, not instantaneous arrest.

## Constructed pocket/yoke section and continuous certificate

Coordinates in mm: column extension has x=[0,6], y=[0,2], z=[−46,6]+h. A continuous
x=[2,4] spine joins left and right pocket rows, each 2 mm deep. Pockets have pitch
p=4 and height w=3.2, with right-row phase p/2=2. Ground-guided U-yoke noses are
.8 mm thick in z; their x intervals are [−3+q,.6+q] and [5.4+q,9+q]. Outer arms
connect to a bridge at y=[3,4], clear of the column. Selector q ranges −1…+1.
The source constructs every web, spine, nose, arm and bridge as finite boxes;
positive-volume intersections are rejected. Ground slides must carry vertical
load/moment while allowing q translation; their bearings/fasteners are obligations,
not generated or qualified geometry. This is a local 16-mm swept-width head section,
not an assembly fitting under each 5.08-mm top.

Insertion depths are `dA=.6+q`, `dB=.6−q`; therefore `max(dA,dB)>=.6` for every q.
At least one bolt is already inserted. With an intact rigid yoke and square pocket
flanks, a misaligned incoming nose hits a web before the old nose can leave: jam,
not a free output. Slot/bolt intervals give free span `W=w−b=2.4 mm` and adjacent
handoff overlap `W−p/2=.4 mm`. Unlike E-129's narrow holes, both bolts can coexist.
The z reaction is column web → nose → yoke → ground slide; flat contact has no
ideal frictionless q component. No driven shaft is frozen in this calculation.

The generated cycle traverses 40 mm in one direction in twenty packets, then returns using
**21 packets**, the last partial. Reversal changes the active pocket phase; twenty
reverse toggles alone miss the starting height by 1.6 mm. At an interior target the
motor must hold until the separate parked support is proved; the slotted catch
itself permits slack. 8/32/128 subdivisions per motion segment check
738/2,706/10,578 states with the same contact topology; a separate grid checks 1,305 feasible h,q states in one period.
A .05-mm excursion through the retained endpoint produces **.160 mm³** solid overlap,
so arrest is tied to an actual web. This overlap is a collision witness, not elastic
penetration being accepted as manufactured geometry.

For **seated q**, any failure phase, velocity sign, stationary dwell or reversal
stays inside a window of width ≤2.4 mm before deformation. This is a continuous
interval result, not just a phase sample. If a held command still completes **one
monotone selector transition**, union of adjacent windows gives ≤4.4 mm. No frozen
release input is assumed for that conditional bound. It requires a real finite
stroke/nonrepeat actuator: q inertia, rebound or further oscillation are not granted
away. The generated section does not establish that actuator. Repeated q switching
has no packet-count bound; neither number is an unconditional machine arrest claim.

## Dimensional uncertainty, catch energy and evidence limits

Explicit competing bounds, not X1C distributions: each row width and bolt thickness
varies independently ±e; relative row phase varies ±e. Common recession of both
noses is also e. Thirty-two corners per e give exact minimum handoff overlap
`.4−3e`, maximum single-pocket span `2.4+2e` and minimum guaranteed nose depth `.6−e`:

| e, mm | Worst overlap, mm | Negative-overlap corners / 32 | Max free span, mm |
|---:|---:|---:|---:|
| .025 | .325 | 0 | 2.45 |
| .05 | .25 | 0 | 2.50 |
| .10 | .10 | 0 | 2.60 |
| .15 | −.05 | 2 | 2.70 |

These interval corners do not establish varied-solid assembly yield. Coherent
shrink/warp, slot bias, layer steps, yoke bending and assembly recession can affect
whole banks. At e=.15 the sequence can jam; that is not proof of loss of retention.
Nose rounding, cam-out, layer strength, creep, fatigue and wear are unmodelled;
engagement depth is not a force rating. No calibrated spring or friction is assumed.

For actual output contact, grant an effective linear elastic grounded catch k and
all moving/reflected mass m free. Let d be remaining unobstructed travel, F an upper
bound on force toward the catch, v initial speed and Es additional stored drive/
capture energy that can reach the output. In SI:

`Ehit=.5*m*v²+F*d+Es; delta=(F+sqrt(F²+2*k*Ehit))/k`.

This follows `.5*k*delta²=Ehit+F*delta`, with peak force k*delta. It conservatively
places all Es into the approach; it does not model when the coupled motor releases
that energy. The contact is directly on the output, so fixing a rotor is unnecessary.
It is **recoverable elastic storage**, not a qualified dissipative brake. Without a
specified sink it rebounds and need not settle; no arbitrary restitution or perfect
latch is inserted. Structural failure can invalidate every excursion bound.

For m=1.1 kg, v=.1 m/s, F=10 N, d=2.4 mm, Es=0:

| k, N/m | Total excursion, mm | Peak force, N |
|---:|---:|---:|
| 10,000 | 6.027 | 36.27 |
| 100,000 | 3.275 | 87.46 |
| 1,000,000 | 2.653 | 253.10 |

At k=100,000, Es=.05/.5 J enlarges excursion to **3.765/5.756 mm**. A still-finishing
selector stroke needs d=4.4 mm instead: **5.500 mm**, 110 N at k=100,000, Es=0.
The executable crosses m=.05/1.1/4.1 kg, v=0/.1 m/s, F=.02/10 N,
d=2.4/2.6/4.4/4.7 mm (the last includes +3e at e=.1),
k=10⁴/10⁵/10⁶ N/m and Es=0/.05/.5 J: 432 scenarios, not reliability samples. F and
inertial mass are independent generalized scenarios; low F at high mass needs an
external balancing reaction, not a free supplied counterweight. Using .6-mm nose overlap as a conservative
bearing-area scenario, 2×.6=1.2 mm² gives 72.9 MPa demand at 87.46 N; bolt shear area
1.6 mm² gives 54.7 MPa, before stress concentration. No PLA allowable is asserted.
Large calculated compression cannot be credited without constructing the compliant
load path; rigid .8-mm webs do not magically provide millimetres of safe stroke.

Self-review: independent RK4 first-contact integration at 200/100/50 µs gives
.874375/.874513/.874582-mm compression versus exact .874597 mm. All energy-root
residuals are <1e−12 J; zero-force limit matches kinetic-to-spring energy. This
verifies the lumped equation, not strength, damping, nonlinear impact or hardware.
For physical height H above the lower end, downward signed excursion must stay
within `[H−40,H]`; finite motion may cross an end stop near a travel limit.
No outage drop has been accepted.

## Reset counterexample and complete-machine cost of packets

State `ready → moving → spent → supported` consumes one permission. If support or
output motion resets `supported → ready` while OPEN stays high, five repeated reset
attempts give five packets. Requiring **CLOSE edge plus proved support** admits one
packet until CLOSE occurs. This is an explicit logical obligation, not a built
one-shot. A stuck high signal cannot satisfy it; a healthy shared clock still can.

Actual pocket seats reproduce that second fault: a gravity-driven failed output
with zero motor effort reaches each next endpoint while the shared selector keeps
cycling for healthy heads. Twenty switches move **40 mm**. Correct output-seat
readback would accept every endpoint: the problem is insufficient reset authority,
not sensor noise. False acceptance/common reader bias creates further faults.
A stalled/misaligned head can instead jam the whole common yoke. Local inhibition,
independent bank abort or drive-authenticated rearm must be built and counted; stop
this topology before silently adding an unpriced local powered release.

Worst-phase 40-mm transport needs up to 21 packets/site: **134,400 packet actions/map**,
plus parked handback. For scenario sliding μ=.02/.1/.3 and 10-N bolt load maintained
through the entire 2-mm selector stroke, work is .4/2/6 mJ per withdrawal,
**53.76/268.8/806.4 J/map**. These conservative constant-load allocations exclude
springs/guides and are not minimum work: unloading the bolt by the powered drive
changes them and adds a proved load-transfer operation. This worst-phase map allocates 134,400
load/withdrawal events; service life remains unknown.

Optimistic schedule: `.4 s` motion at .1 m/s, `.05 s` local capture/parked proof,
21 times packet overhead tr; six seconds/map for preparation, registration,
transport, final proof, bounded retry and settling. `T=6+ceil(6400/H)*(.45+21tr)`.
No overlap or empty return is earned. Packet overhead includes selector stroke,
load transfer, reset proof and local settling. Exact required head counts are emitted
for tr=0/5/10/20/50 ms: **121/149/178/238/427 heads** respectively. Shared wave
scheduling couples independent target heights/signs; the formula is optimistic.

Count H drives, two H grounded nose/guide contacts, H rigid selector/catch assemblies,
selector actuation/returns/end stops, proof and recovery hardware, and 6,400 parked
supports/returns/guides plus direct output catch features. Resident 6-mm extensions
at 5.08-mm centers need staggering/routing; this is not an E-132 access pass. Common
frame motion and non-target disturbance remain unqualified. Joint bought hardware
must stay <$500, ideally <$200: a hypothetical $250 elsewhere leaves <250/H per
complete head with free cells. No supplier quote or joint BOM passes. Print time,
material, assembly and wear cost are unresolved; no print/purchase is warranted.

**Decision:** preserve overlapping-pocket feasibility and conditional travel/energy
bounds; retire automatic output reset and shared repeated release as loss-safe
architectures. Reopen with finite selector dynamics, actual beyond-capture support,
impact dissipation/strength and reset authority independent of the failed output.
Do not refine yoke dimensions. **Next discriminator:** compare mechanically
nonrepeating, local-drive-work-authorized reset against a physically isolated finite
energy packet (spring/electrical/fluid). Construct source-disconnection and grounded
load paths, not another nominal OPEN force. Test low-load coast, signed motion and
stuck replenishment; stop any option whose only reset evidence is output motion or
whose finite input energy ignores gravitational energy. This changes the reset and
energy causality axis; no principle is promoted merely by giving it a new name.
