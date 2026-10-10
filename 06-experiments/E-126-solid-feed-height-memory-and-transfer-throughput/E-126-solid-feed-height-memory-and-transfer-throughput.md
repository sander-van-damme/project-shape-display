---
status: complete
builds-on: [E-125, A-013, A-024, A-025]
---

# Common-datum storage avoids variable-height capture but serial particle exchange fails

**Reject the four-stroke particle feeder at the tested motion bounds. Retain
continuous feed and fixed-datum pinion docking as different unproven routes.**
A clearance section is available; throughput rejects the specified loose-particle
transaction before detailed load/contact design. A-025 is the cheaper next
finite-mechanism question because it avoids both loose-particle recirculation and
the extra linked-chain inventory. This is an investigation priority, not a selected
machine. Input main `723b71a`; no physical measurements or hardware qualification.

Reproduce with Python standard library:

```
python3 tools/curated-experiment-checks/E-126/solid_feed.py
```

Evidence: analytical bounds, generated sphere/blade swept-section checks and an
abstract unit-transfer scheduler. No complete CAD, dynamic granular simulation,
validated timing, sourced process distribution, material allowable or price quote.
JSON is reproducible output, not retained evidence.

## Search and complete-machine comparisons

Three different exploratory moves, cross-checked with repository mechanism and
architecture names/content (particle/granular, chain, screw):

- **Bulk feeding analogy:** store height as counted solid length in a tube
  (A-024). Common-datum bottom access removes the 40-mm acquisition search.
  Source-domain search found US6155403's golf-ball conveyor: pushing a confined
  ball column is an existing mechanism, not evidence for precision height storage,
  arbitrary addressing or loaded reversible exchange. The patent search excerpt
  was accessible; full text fetch failed. No patent novelty claim is made.
- **Deployable structural members:** linked/zip chains exchange flexible stored
  length for a compression column. Tsubaki describes two interlocking chains;
  this supports the operating principle only, with no transfer of industrial
  speed, size or lifetime to our pitch. The proposed display would dock reusable
  drives to fixed feed wheels, retain each wheel with a positive arrest, and
  guide each output. It still needs local lock transfer and readback; interlocking
  links alone do not establish anti-backdrive at the base. At assumed 4-mm link
  pitch and 40-mm stroke, two strands require at least 20 links/site, or 128,000
  links before stored slack, pins and end joints. $250 residual permits at most
  $0.00195/bought link before all those other parts; no supplier meets that here.
  Linked feed avoids stop/start for every separate sphere, but adds hinge wear,
  storage routing and assembly. Keep as a continuous-feed control, no detailed
  chain optimization yet.
- **Invert the moving interface:** leave the pinion/docking shaft fixed and move
  only the rack (A-025). This merges continuous feed with an existing rigid
  column instead of producing a new segmented column. It is a material topology
  change from E-125's acquired foot, not a new physical principle. It retains
  repeated gears/bearings/arrests and the costly reusable selector channels.

A-013/E-125 remains the direct-head control: fewer permanent gears, but the tested
compact acquired-foot layout failed finite retention and loaded contact. A-007's
screw failure is preserved; a pinion's circumference is a different displacement
ratio. None of these alternatives inherits a qualified actuator, sensor or lock.
A-024/A-025 specify selection, energy, retention, load, verification and recovery
causally; unresolved implementations receive no free mechanism credit.

Primary references accessed 2026-10-10:
[US6155403, patent search excerpt](https://patents.justia.com/patent/6155403),
[Tsubaki operating principle](https://en.tt-net.tsubakimoto.co.jp/tecs/pdct/sad/pdct_sad_3zca.asp).
These are analogy evidence, not procurement or manufacturing priors. The search
is not saturated; three distinct moves gave two useful new topologies and a
linked-feed comparison, with no claim of exhaustive landscape coverage.

## Particle geometry and correlated dimensional bounds

Enumerate d={2,3,4} mm sphere diameter, nominal diametral bore clearance
c={.1,.2,.4}, wall={.3,.4}, and error e={.025,.05,.1} mm. These are **explicit
uncertainty scenarios**, not X1C or purchased-ball capability. Actual bead diameter
is d±e, bore diameter d+c±2e, outer envelope d+c+2wall±2e. Require positive
minimum running gap c−3e and maximum outer envelope ≤5.08 mm. A .3-mm printed
wall is experimental, even where arithmetic clears; no strength is granted.

For a local transfer section, generate two .4-mm-thick × .4-mm-wide blades at
x=[a,a+.4] and its mirror, z=d/2±.2, swept along y through the tube. Enumerate
a=.40…2.20 mm in .05-mm steps, with an outer wall allowance inside half-pitch.
Use exact sphere-to-swept-box distance in x-z. Test common bead diameter extremes,
bore extremes, blade growth ±e, and same/opposing sphere-center wall positions.
The lower sphere centre at z=0 is a **fixture assumption**; the model does not
build that fixture. Upper centre separation follows actual sphere contact.
Thirty parameter sections have a nonintersecting blade sample. For d=4,c=.2,
wall=.3,e=.05,a=1.30, minimum sampled clearance is .02326 mm. These are finite
section results at discrete corners, **not an all-errors guarantee**, a retained
fork assembly, tube-slot strength, or a supported exchange trajectory. Tube slots,
blade bridges, end stops, removal pocket and every actual support handover remain
unbuilt. Do not call this a mechanical-gate pass.

A sphere chain in a straight tube can zigzag. For n equal rigid spheres,

`Hmin = d + (n−1) sqrt(d²−c²)`; `Hmax = nd`.

This is an attainable alternating-wall geometry, before compression. Use d−e
and c+3e for the low bound and n(d+e) for the high bound. It conservatively bounds
unequal spheres within these diameter limits too, but says nothing about frictional
bridging or compliant walls. Common lot/bore error affects every contact and may
affect an entire module: no 1/sqrt(n) averaging or independent-cell yield is used.
For d=4,c=.2,e=.05, ten beads reach only 39.3602 mm at the low corner. Eleven
reach 43.2946–44.55 mm across these bounds, requiring 70,400 spheres at full scale.
The 44-mm nominal state is allowable excess travel, not an exact 40-mm height.
No product height-accuracy tolerance is invented; calibration of count alone
cannot remove load-dependent seating, wear, creep or rearrangement.

$250 remaining after an **assumed**, unsourced shared-machine reserve permits
$0.00355 per sphere at the $500 ceiling, before forks, springs, fasteners or any
other bought cell hardware. Printing spheres trades this threshold for ~70k
surfaces/support-removal/assembly operations; it establishes no saving. The stack
also needs containment and storage for an all-low map, replenishment for all-high,
and bounded recirculation for repeated maps. None is included as free volume.
Service compression/contact stress, friction, layer anisotropy, fatigue and wear
are unresolved; do not extrapolate this rigid geometry into 10-N load capacity.

## Transaction-rate discriminator and continuous controls

Worst mixed map: each bank contains cells going 0→11 particles and 11→0.
With independently enabled channels but one shared feed direction, a batch needs
`max(positive changes)+max(negative changes)=22` particle cycles; independently
reversible channels need 11. A serial particle-cycle assumption is distinct from
cell-level indexing. Unchanged sites take zero transfers and retain their forks.

Test a **hypothetical four-stroke shuttle**, four sequential rest-to-rest travels
of 4 mm per particle (lift/lower and pocket out/return). This is a defined timing
embodiment, not a universal lower bound on every feeder. Every stroke obeys
`2 sqrt(L/a)` if triangular, otherwise `L/v+v/a`. v={100,300} mm/s and
acceleration={1000,10000} mm/s² are optimistic unloaded scenarios. No jerk,
load/force derating or extra per-particle fork/readback dwell is charged.

At the fastest corner, one particle takes .160 s. Allow six seconds per map for
registration, indexing, verification, settling and a bounded retry; this is an
**unallocated screening allowance**, not a constructed completion schedule.

| Heads | Shared-direction mixed map | Independent-direction control | Required particle cycle, shared |
|---:|---:|---:|---:|
| 80 | 287.6 s | 146.8 s | <13.64 ms |
| 160 | 146.8 s | 76.4 s | <27.27 ms |
| 320 | 76.4 s | 41.2 s | <54.55 ms |

Even zero overhead leaves the best shared case at 70.4 s and independent case
at 35.2 s. Therefore uncertainty about the six-second allowance cannot rescue
this tested embodiment. Higher acceleration, more heads or overlapping/continuous
feeding changes the case and requires a new mechanism, not a timing assertion.

Continuous linked feed or a fixed pinion avoids four stopped strokes per particle.
At the same v=300,a=10000 bounds, one 40-mm stroke takes .16333 s. Ideal selectable
couplings let one shared-direction batch do positive and negative strokes:

| Heads | Two shared-direction strokes + 6-s allowance | Independent-direction + allowance |
|---:|---:|---:|
| 80 | 32.13 s | 19.07 s |
| 160 | 19.07 s | 12.53 s |
| 320 | 12.53 s | 9.27 s |

These are necessary-condition controls, **no admitted machine timing**. Couplings
must engage/stop each channel at its own target without disturbing parked cells;
phasing, clamp reset, load arrest, docking and proof may exceed the reserve. With
$250 reserved, 160 complete bought head channels have at most $1.5625 each before
all repeated cell parts. A-025's 3-mm pinion needs 4.244 turns over 40 mm and
1,910 rpm at the speed bound; torque, tooth strength and coupler dynamics are open.

Reader false acceptance can miss a supported-height error or an open lock.
No failure probabilities are assigned. Count/drive encoders need independent
height and support evidence; a common reader bias can invalidate a whole bank.
No support loss on power failure, local-disturbance or reliability acceptance
follows from these schedules. Printing would not resolve the fatal shuttle-rate
bound; a finite common-datum pinion/docking/lock transfer is the next useful test.

Self-review: zero-clearance and zero-count limits; independently assembled sphere
coordinates/contact distances reproduce stack height; exact box-distance limits;
all 81 two-site signed delta schedules in −4…4 reach their target with conserved
unit transfers; zero-change/local-update cases; triangular/trapezoidal continuity.
No independent external validation. Stop loose-shuttle refinement and detailed
chain work; retain their unique failure/part-count evidence and probe A-025 before
any complete-channel timing/BOM or fabrication claim.
