---
status: complete
builds-on: [E-085, E-083]
---

# A compliant stopped fork trades rigid overdrive for recoil and routing conflicts

**Reject a single coplanar row of bidirectional forks; retain the staggered
section only as a conditional comparator, not a complete writer.** Two stations
remove adjacent-fork interference, but their flush stop collides with a parked
neighboring bank during regional operation. The generated spring embodiments
also fail the declared broad stiffness/load/stress box. Compliance changes the
rigid-completion mechanism; it does not establish safe capture, settling or
withdrawal. No architecture, material property or fabrication is qualified.

Input main `6a8842c`. Reproduce with
`python3 tools/curated-experiment-checks/E-086/compliant_fork.py`;
optional `--svg PATH` exports nominal fork solids in x–z. Standard-library finite
box intersections, deterministic map replay, interval corners, beam-energy
calculations and itinerary accounting. All dimensions, uncertainties, mechanical
properties, force limits, acceleration and overhead here are **explicit assumed
scenarios**, not measurements, sourced X1C priors or inferred distributions.
The spring model is analytical; no finite-element or dynamic-contact solver ran.

## Changed mechanism and finite transitions

E-085 supplied energy by scanning a one-sided cam past a dog. This comparator
stops an accessible reusable head at each row, lowers an open-bottom fork around
the dog, then moves the fork left/right through one bidirectional data channel.
A series flexure between drive and fork accommodates endpoint overrun. Return
the drive to neutral, prove settling and dog state, lift the fork, prove actual
clearance, then index. Retained dog endpoints and separately retained column
supports remain boundary conditions; the fork never carries tabletop load.
All support/output cams remain parked during partial-mask rewriting.

The 1.2-mm dog stroke and 0.8 × 0.6 × 1-mm boss are inherited comparison
geometry. Reference fork neutral center x=0.6 mm, inner gap g=2.6 mm, jaw wall
w=0.6 mm, y depth=1.2 mm. Its legs occupy z=[0.2,2.4] mm and its connecting
bridge z=[2.4,3.2] mm. A 1.2-mm lift clears the dog nominally by 0.4 mm.
Actual fork displacement to either endpoint is
`q0=d/2+(g−boss_width)/2=1.5 mm`, before spring drive overrun.

Generated boxes replay six old-state/set/reset/bypass paths through descent,
drive, neutral unload and lift, checking target and neighboring bosses. Bypass
leaves a generous neutral opening in the nominal section. In quasi-static
unloading, the pushing jaw separates and the other jaw remains clear. A
retention failure, adhesion or dynamic recoil is not concealed by this result.
No complete slide, drive, spring attachment, retention or readback geometry is
accepted from these boxes.

Two adjacent same-row forks with opposite commands have a **1.6512-mm³**
solid-intersection witness. This is not a tolerance problem. Put even-column
forks at longitudinal station 0 and odd-column forks one pitch behind:
same-station pitch becomes 10.16 mm and adjacent-column solids become disjoint
in y. This is one packing variant, not another architecture. A two-row bank
needs three stopped positions to flush both parities. All **256** two-by-two
old/new maps replay correctly through this staggered schedule. Nominal paths
alone do not include the complete spring or machine.

## Error corners and failure-safe travel envelope

Bound head x offset b, dog-stop offset t, full boss-width error dw, and inner
jaw-face error j independently by ±e. Terminal contact demand is
`q=q0+t−b−dw/2−j`, hence ±3.5e. Jaw thickness and fork mechanical-stop position
each have their own ±e bound. These are alternative uncertainty boxes; a shared
rail/batch can make their adverse corners coherent across a bank. No cell-count
averaging or production yield is inferred.

To avoid relying on a dog to arrest the fork, include a mechanical fork stop
at nominal `q0+3.5e+e`. This admits the farthest endpoint even with the stop
error −e. Test the largest stop position against the neighboring zero-state dog
when the target boss is missing or retention has failed. Actual outer-wall and
neighbor boxes supply collision witnesses; this is more restrictive than
checking only normal dog-limited motion.

| Reference fork error bound e | Neutral insertion gap | Neighbor gap at failed-dog stop | Same-lane fork gap | Raised dog gap |
|---|---:|---:|---:|---:|
| 0 mm | 0.300 mm | 0.680 mm | 3.360 mm | 0.400 mm |
| 0.05 mm | 0.125 mm | 0.180 mm | 2.510 mm | 0.300 mm |
| 0.10 mm | **−0.050 mm** | **−0.320 mm** | 1.660 mm | 0.200 mm |
| 0.20 mm | **−0.400 mm** | **−1.320 mm** | **−0.040 mm** | 0 mm |

Generate g={2.4,2.6,2.8}, w={0.6,0.8} mm and those four error boxes: six section
variants, 24 scenarios. Three sections retain all positive reserves at e=0.05;
none does at e≥0.10. A wider opening improves insertion while worsening the
outer-jaw sweep. These bounds do not establish that ±0.05 mm can be manufactured
or maintained. Orientation, tilt, wear and guide bending remain additional
errors. Stop wider-box development of these sections; tighter calibrated errors
or changed boss/withdrawal topology would be reopening evidence.

This conflict also has a continuous bound: positive insertion requires
`g>d+W+7e`, while neighbor clearance requires `g<P−d−w−10e`.
Thus any gap with w≥0.6 mm requires **e<0.07529 mm** at P=5.08 mm under this
stop/error contract. At e=0.10, the two constraints require g>2.70 and g<2.28 mm.
An internal pitch greater than 5.50 mm could remove this particular conflict;
it needs a changed internal layout, not permission to coarsen the top surface.

## Flexure force, capture and recoil

Screen two rectangular clamped-guided beams, with length L along z, x thickness
t and y width b=0.6 mm, connecting the moving drive to the fork. They are an
analytical compliance hypothesis, **not a generated/qualified spring assembly**.
For lateral endpoint separation δ and shape `φ(u)=3u²−2u³`, two beams give
`k=2Ebt³/L³`. A guide permitting axial relief gives the linear estimate `F=kδ`.
If guide separation in z is fixed, approximate elongation is `3δ²/(5L)`, adding
`cδ³` with `c=36Ebt/(25L³)`. Stored energy is `kδ²/2+cδ⁴/4` N·mm, and maximum
bending-plus-axial stress estimate is `E(3tδ/L²+0.6δ²/L²)` MPa.
These competing guide models express model uncertainty, not proved bounds on
all nonlinear behavior. Use δ/L≤0.1 as a declared reduced-model domain.

Cross L={12,16.8,24} mm, t={0.8,1.0} mm, e={0.05,0.10} mm and required force
{0.1,0.3} N: **24 scenarios**. Modulus interval [1,000,3,000] MPa, force cap
1 N and stress cap 20 MPa are screening assumptions, not generic PLA allowables.
Choose drive overrun `o=3.5e+Freq/k(Emin)` to reach the endpoint in the softer
axially relieved model. Then test maximum compression `o+3.5e` in the stiff,
fixed-z model, plus the swept drive crossbar against 10.16-mm lane spacing.
Fourteen scenarios remain within the reduced-model domain; all fourteen exceed
the assumed stress cap, twelve exceed force and one exceeds drive packing.
The other ten require a different model before interpreting their extrapolated
forces. No spring survives this uncertainty contract; this is not an
impossibility proof for PLA flexures, metal springs or force-limited drives.

For L=16.8,t=1,e=0.05 mm, Freq=0.1 N, required overrun=0.570136 mm;
maximum deflection=0.745136 mm, peak=0.79189 N and stress=27.302 MPa.
At Freq=0.3 N these become 1.360408 mm, 1.535408 mm, 3.1444 N and 63.996 MPa.
Even the lower-load case fails the declared stress limit. Creep/fatigue,
interlayer weakness, print orientation and attachment concentration are absent;
they cannot be treated as remaining positive margin.

Capture remains a separate gate. For known E=2,000 MPa, the fixed-z spring is
**1.72 times** its linear force at δ=1 mm. An illustrative 5-g follower against
0.1-N resistance, with the drive held fixed during arrest, has only 0.318 mJ
between its equilibrium and the 1-N force limit after subtracting resistance
work. That corresponds to 0.3566 m/s kinetic speed, but reaches 27.82 MPa.
Applying the assumed 20-MPa cap reduces the energy-based speed to 0.2314 m/s.
Neither is an allowable operating speed: continued drive work, contact impact,
effective modal mass, damping and settling were not solved.

At neutral drive, residual oscillation can bring the opposite jaw back into
the retained dog. The reference e=0.05 neutral reserve is 0.125 mm. For the
lower-load example, its spring-energy capacity before that contact is only
**2.36%** of the maximum-compression energy. This is an unloading requirement,
not a claim that all terminal energy becomes rebound. A nominal −0.4-mm fork
excursion actually intersects the set dog by **0.048 mm³**. No assumed damping
or 2-ms read/proof slot proves that recoil stays within the reserve.

## Full and regional routing, time and cost

Staggered stopped forks can write in either direction, allowing serpentine
mask scans without E-085's empty return. At B banks with n=80/B rows each, the
43-mask adverse workload needs `43(n+1)` stopped transactions and `43n`
pitch indexes per parallel bank. Include lower/raise, drive out/back, read/proof,
the extra flush stop, and E-083's still-unproved six-second allowance for other
machine operations. Every move uses rest-to-rest `2√(distance/acceleration)`;
drive travel is an assumed 2.5 mm and proof=2 ms per stop. No velocity cap,
moving-mass/drive-force feasibility or settling solution is credited.

| B / assumed acceleration | Full-map accounting | Bought channels counted | Mean residual/channel, $250 elsewhere |
|---|---:|---:|---:|
| 8 / 20 m/s² | 56.461 s | 656 | <$0.3811 |
| 8 / 100 m/s² | 29.090 s | 656 | <$0.3811 |
| 16 / 20 m/s² | 32.901 s | 1,312 | <$0.1905 |
| 16 / 100 m/s² | 18.316 s | 1,312 | <$0.1905 |
| 20 / 20 m/s² | 28.189 s | 1,640 | <$0.1524 |

These are itinerary scenarios of an unaccepted package, not deadline passes.
Channels are 80B bidirectional data axes plus B common lifts and B index drives;
reader, controller, transmission, limiter and wiring costs must still fit the
strict bought ceiling. No prices were researched or assigned zero. Against
E-083, the architecture removes 6,400 captive keys/feet and long data bars,
but retains 6,400 dogs/retentions and persistent outputs, adding 80B forks,
160B spring beams, their guides, drive couplings and shared moving heads.
No full BOM, total print time, weighed mass, assembly time or Pareto win exists.

**Regional routing fails before claiming these times.** At one bank's final
flush stop, its even-column forks occupy the same row as a neighboring bank's
parked initial even-column forks. A parked lift of 1.2 mm gives a **0.720-mm³**
fork/fork collision. Clearing a dog is not clearing a head. Raising by 3.2 mm
clears only these fork boxes, not the taller spring/drive/guide assembly; it is
not a complete parking solution. Synchronized full-bank scans avoid this fork
collision for n≥2; n=1 (B=80) reproduces adjacent opposite-fork interference.
Moving every bank in lockstep to support a local edit would change regional
disturbance and preparation accounting and has not been accepted as a product
tradeoff. The source's ideal 35-transaction patch arithmetic deliberately has
no regional feasibility credit.

At B=8,a=100, a whole-mask retry costs another 0.537 s in the itinerary; the
nominal 0.910-s deadline margin cannot hide arbitrary retries. A stuck extended
fork intersects a bypassed zero dog by 0.096 mm³. Indexing must remain disabled
until individual fork clearance is proved; common lift position is insufficient.
At least 275,200 dog decisions and 275,200 active-fork clearance decisions occur
in the adverse workload, before inactive-station checks and output-support
observations. Without independence, a hypothetical union bound is
`Punsafe ≤ min(1,Ndog*pDog + Nfork*pFork + Nsupport*pSupport)`.
None of these per-opportunity error bounds is measured; repeated reads cannot
be given independent-error credit. A jam leaves output cams parked and requires
repair under retained support. Extraction load and access remain unqualified.

## Decision and verification

Stop the coplanar fork and this broad-box printed-flexure embodiment. Keep the
staggered finite section as a simple stopped-head reference with explicit regional
collision, recoil and force failures. Do not refine its nominal timing to select
hardware. Reopening requires a changed route/packing mechanism and a force and
recoil envelope that survives declared uncertainty, not just narrower guessed
material/tolerance numbers. A bounded-rotation coupling or isolated retained
carrier return can change lateral sweep and bank-boundary behavior; neither is
supplied or rejected here. A stationary setter using this same fork at the output
inherits its local interference and completion requirements. Campaign completion
still requires that materially different coupling/route comparison. No printing,
purchase or staffing is justified by this result.

Self-review only: six nominal paths, 256 map compositions, finite collision
negative controls and exact interval-corner limits; disjoint interval envelopes
bound between sampled nominal poses. Independent quadrature of beam shape
curvature converges fourfold at 20/40/80/160 intervals (integral errors
0.060/0.015/0.00375/0.0009375). Energy differentiation recovers force and inverse
force solves recover displacement, including zero. These verify calculations,
not printed-material properties or a continuous 3D contact assembly. No dynamic
time-step convergence is claimed because there is no dynamic integrator.
