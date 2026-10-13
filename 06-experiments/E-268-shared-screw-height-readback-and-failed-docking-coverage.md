---
status: complete
builds-on: [E-178, E-259, E-261, E-267]
---

# Screw-pin readback must preserve guides, thrust support and service

**Stop reader detail on the present slotted-guide layout.** Metal stiffens thrust rows but
cannot reconnect the fine-grid guide or qualify coarse guide/frame support. Retain coarse metal
bays as an analytical control; do not rescue the optics with thousands of narrow guide fingers,
inserts or retainers. The examined support boundaries increase coarse local S50
maximum23.97→39.52s: a tradeoff, not automatic product rejection. No camera, architecture,
manufacturing process, print or purchase is selected. E-263's owner print offer remains retired.

Reproduce `python3 tools/curated-experiment-checks/E-268/readback.py`, `python3
tools/curated-experiment-checks/E-268/support.py` and `python3
tools/curated-experiment-checks/E-268/structure.py`. Evidence: sampled ideal rays, fault
witnesses, elastic beam calculations and scheduling. Self-review with independent calculation
methods; **no hardware qualification**. Loads, moduli, acquisition times and error bounds are
scenarios, not measured miniature distributions, calibrated process priors or reliability.

## Observe actual pin position

Motor counts miss failed docking/transmission; screw angles miss stripped threads. A top camera
cannot see through a miniature covering a pin. Actual-pin scales need integral marks, fresh
frames and cell identity. Contact probes require access/travel and can disturb the measured pin.

Executable10→20mm/lead2 witnesses: five motor turns with zero screw turns leave10; five screw
turns with stripped thread also leave10. A detached mark can report20 while terrain remains10.
Occluded, stale or unreadable means **unknown**, never last-known success. Integral marking,
fresh-frame identity, contrast, registration and persistent-fault rejection remain necessary. No
detection probability follows. A correct height cannot establish future retention or moving-loss
arrest; it also does not automatically require4096/6400 extra brakes or support sensors.

## Finite route through the actual beds

E-261 lower guide z=S+5mm is2mm thick; upper guide40mm higher. Datum z=S+9
covers local pin coordinates7…47/57 for S40/50 on86/96mm stock, without added
tail. Marks face+Y on4.4mm pins; a45° between-row mirror redirects to a centered
camera at z=−10. readback.py retains the finite tracks, pupil.25mm, tilt±.5°,
mirror backing and correlated-error definitions. Sampling is not image-quality
or continuous-pose certification. Original S40 results:



|Pitch / e, mm|Backing gap, mm|Mirror misses|Incoming envelope hits|Required slot, mm|Guide web/side, mm|
|---|---:|---:|---:|---:|---:|
|5.08 /0|.068|0|0|.450|−.005|
|5.08 /.05|−.032|0|8192|.666|−.113|
|6.35 /0|.330|0|0|.454|.628|
|6.35 /.10|.130|0|0|.885|.412|
|6.35 /.20|−.070|0|0|1.400|.155|

Negative gap is collision even if rays clear; fine e=.10 also gives wrong-side rays. Breakpoints
e≈.034/.165 are not process tolerances. E-261's.24 guide clearance permits.12 lateral play;
e=.10 is unestablished. Wider5.6 stems and changed pupils/reflectors cannot inherit this result.

Opaque lower guide and thrust bed both obstruct the view; occupied screw holes are not optical
windows. Slots through **both** layers must encompass ray intersections plus plate registration.
Web=(pitch−slot−4.64)/2. Coarse S50/e.10 needs.887mm slot/.411mm webs. Continuous slots break
cross-row support. Terminate them at transverse ribs between8/16-column bays. A1mm coarse rib in
the1.71mm aperture gap leaves.51mm after opposing.10 edge errors; fine.44mm gap cannot fit it.
An interior rib has an explicit ray-intersection witness: a freely sliding16-field reader cannot
inherit unobstructed coverage across boundaries. Fixed aligned bays are one sufficient
restricted policy, not the only possible optical route; extra relays/cameras or separate reader
motion need costing.

## Supported load paths and structural screen

Intended path: terrain→pin thread→screw→resident shoulder seat→perforated row→ transverse
rail→grounded frame→table, throughout docking/withdrawal. A proposed 4.4mm shoulder/3.6mm
journal has5.03mm² area (.010/.040MPa at.05/.20N), with .425mm coarse slot margin before
eccentricity/play. Seat strength, edge contact, wear and pull-through remain unqualified. Upward
docking/friction also needs **shared axial capture**; keeper clearance, minimum-stroke collision
and assembly remain unconstructed. Count one capture duty per screw, not free support or
permission for4096 clips.

The pin's guides resist rotation and lateral force; the thread carries gravity. Upper/lower
guide reactions and their moment must reach the frame independently of the writer. E-256 hold
and E-262 moving-loss/speed limits remain unresolved.

### Thrust strips and end rails

Use simply supported, variable-section Euler–Bernoulli virtual work
`delta=integral(M*m/(E*I),dx)`, `I=net_width(x)*t³/12`, with discrete cell-center forces and
circular3.6mm holes. Solid and constant-minimum-section controls bracket this **beam
calculation**, not hardware compliance. The [AWC beam formulas,
figures1/7/8](https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf) supply
constant-section checks only; no wood properties are imported. Exclusions: local hole/seat
distortion, stress concentrations, shear, torsion, joints, anisotropy, creep, fatigue and frame
settlement. Large displacement flags linear model breakdown, not a precise shape.

**Supported-module extension:** allow1.10mm coarse / .70mm fine slots rather than spend the
whole ray margin on fabrication. E1000/3000MPa polymer and E70000/200000MPa metal-like values
are labelled scenarios, not stock ratings or calibrated printed properties. At2mm thickness/.05N
per site:

|Pitch / cells|E1000 deflection, mm|E70000, mm|E200000, mm|
|---|---:|---:|---:|
|6.35 /16|5.555|.0794|.0278|
|6.35 /8|.349|.00498|.00174|
|5.08 /16|5.325|.0761|.0266|
|5.08 /8|.334|.00478|.00167|

Fine is only a structural control: its guide/mirror fails geometrically. Coarse16 constant-net
controls are9.947/.1421/.0497mm at E1000/70000/200000. Coarse6mm polymer still gives.206mm.
Scaling: load linearly, thickness t⁻³. Multiply by.4/4 for.02/.20N per site. Load includes pin
weight; uniform loading is a stress scenario, not typical miniatures. Full-board.05N
totals204.8/320N before frame.

An interior transverse rail receives nF/2 from each neighboring n-cell bay, i.e. nF per row and
n²F per segment. At coarse16/F.05, a proposed1×10mm rail supported at both segment ends
carries12.8N,6.4N/end. Sag E1000/70000/200000: 2.101/.0300/.0105mm; nominal bending
stress9.754MPa. At8 cells: .0660/.000942/.000330mm. Exterior rails receive half. Coarse16/2mm
row plus same-material rail therefore sags approximately.109mm at E70000 or.0383mm at E200000,
**before joints/frame**. A6mm polymer row does not cure2.10mm polymer rail sag. Hypothetical
joint stiffness1/1000N/mm adds6.4/.0064mm per loaded end. Unequal adjacent-bay loads can twist
the rail; torsion is unmodelled.

The .05mm comparison budget is illustrative, not a product requirement. A single .20N changed
load near row center moves the unchanged center.0564mm in the E70000/2mm constant-net control.
Fixed screw angle does not establish isolation.

### Guide reactions and repeated edges

With40mm guide separation and maximum top overhang S+3 above upper center, side load H gives
lower reaction H(S+3)/40; upper=−H−lower. At S50/H.10: +.1325/−.2325N; S40:+.1075/−.2075N.
H=.02… .50 are scenarios, not measured player loads. Illustrative μ=.3 sliding friction
adds.1095N axial drag at S50/ H.10 before torque contacts; the.05N axial case does not cover
this combined state. Torque.35Nmm allocated wholly to the lower guide adds an opposed
.0795N/contact couple across4.4mm. Upper and lower beds need grounded moments.

Coarse1.10 slot leaves w=(6.35−1.10−4.64)/2=.305mm side ligaments. Screen a 4.64mm simply
supported edge under the full lower reaction at its center, I=2w³/12. Fixed ends give a
four-times-stiffer control, not assumed construction. At S50/H.10, excluding global row/frame
movement:

|Combined inward edge loss, mm|w, mm|Local deflection E1000 / E70000, mm|Nominal stress, MPa|
|---|---:|---:|---:|
|0|.305|.0583 / .000833|4.96|
|.10|.205|.192 / .00274|10.97|
|.20|.105|1.429 / .02042|41.82|

Loss.10 can mean each hole/slot edge shifting.05 inward, coherently across a panel; these are
**bounds, not process priors**. Loss.20 amplifies compliance24.5×. With torque.35, nominal
contact becomes.2120N/stress7.93MPa before edge loss. No notch, strength, creep or fatigue pass
follows. Shortening bays helps global bending but leaves this same per-aperture vulnerability.

For coherent H.10 at every site, gross-solid16-row lateral control gives.0172mm at E70000; an
uncoupled single-rail control gives87.6mm, beyond linear validity. The perforated ladder needs
cross-tie shear transfer; this wide interval does **not** prove metal guide failure, but forbids
treating thrust stiffness as lateral qualification. No rigid-joint or material-strength credit
closes it.

Fine/.70 slot gives w=−.130mm, disconnected even with perfect material. Even original.450 slot
gives−.005. A.20mm fine end rib leaves only.04 after opposing .10 edge allocations; the mirror
already collides at e=.05. **Metal cannot restore absent geometry. Stop this embodiment before
repeated micro-supports.**

## Reader envelope, manufacturing and service

Original support recheck covered114,688 rays; the structural extension covers 196,608 more
across both pitches,8/16 bays,S40/S50 and2/6mm thrust thickness. Maximum slots.89295/.68383mm
fit the1.10/.70 allocations; sampled end margins ≥2.434/1.938mm. A10mm-deep end rail's lower
segment approaches the centered camera in X, so it cannot add an end-rib crossing on these
straight outgoing rays. Mounts, keeper, camera body, writer retraction past deeper rails and
full-frame access remain unconstructed; additional time cannot be called zero. Upper guide stays
unslotted.

|Whole board|6.35mm /64²|5.08mm /80²|
|---|---:|---:|
|Resident pairs / thrust-seat duties|4096|6400|
|Two guide-aperture sets|8192|12800|
|Thin lower-guide side ligaments|8192|12800|
|Two slotted-layer row spans,16 /8 bays|512 /1024|800 /1600|
|Two layers of square panels,16 /8 bays|32 /128|50 /200|
|Ground-grid node locations,16 /8 bays|25 /81|36 /121|

Monolithic panels retain every edge; upper guides, keepers, spacers and mounting
are extra. Illustrative four fasteners/panel adds128/200 at16 bays or512/800 at8.
Ten seconds handling/pair costs11.38/17.78h. Marked faces4096/6400; two≤203.2mm
mirrors/row means128/160 pieces,26.01/32.51m strip. Batch registration, marking,
deburring, seams and flatness remain unqualified.

Compare FDM/molded/cast panels (creep, shrinkage, tooling/release) with cut or machined metal
and controlled finishing. Formed stiffeners owe footprint/joint accounting. Density
scenarios2700/7850kg/m³ give1.78/5.19kg for two full406.4mm square2mm sheets before
perforation;6mm thrust+2mm guide doubles stock mass. Finished mass, upper bed/frame and pricing
remain unknown.

Assembly must capture shoulders without bonding beds shut. Panel removal can affect256 sites
at16-square or64 at8-square; calling it removable proves no single-pair service route. Shared
openable access must preserve adjacent support. No per-cell cartridge, sensor or latch is added
or authorized by this screen.

## Read/stop/recovery and paid waiting

E-178's code is not continuous sensing:51 integer-mm positions need≥6 bits before redundancy.
With acceptance half-width a and error e, accepted true error can reach a+e (.5mm at a=.3/e=.2).
Pixel density is not accuracy. Retry uses fresh actual height; persistent faults/later drift
exceed the one-retry model.

Final imaging does not replace active control. At850rpm/lead3,10/20ms latency adds.425/.850mm
before braking; at2000rpm,1/2mm. Keep active stopping/end margins and feedback budgeted. Neither
image nor powered brake proves power-loss hold.

Replace E-267's20ms proof slot, never double-charge it. At100ms,16 coarse visits
plus retry adds1.36s. Two full-row heads give17.94/21.94s coarse and20.75/25.69s
fine, requiring128/160 drives and8/10 simultaneous fields rather than16 drives/
one field. Acquisition sensitivity remains in readback.py; no measured rates.

At850rpm/lead3/100ms,133 nonempty four-square windows per depth:

|Pitch / stroke mm|Free16, s|Fixed16 bays, s|Fixed8 bays, s|
|---|---:|---:|---:|
|6.35 /40|19.97|31.75|31.50|
|6.35 /50|23.97|39.52|39.26|
|5.08 /40|37.11|50.58|64.44|
|5.08 /50|46.59|64.22|82.79|

Seeks, return,4s common allowance and one immediate retry are paid; deeper-frame transport
remains unqualified. Fine schedules lack feasible support/optics. Coarse fixed16 gives128/126
windows≤30s; maximum individual penalty12.28/16.05s. A two-cell boundary reveal needs two
stations, not one; some travel heuristics improve. Coarse fixed16 large-scene
maxima179.25/208.66s; cold N20/N30 preparation 196.06/256.53s separately. These preserve real
downward travel,40/50 stroke and unchanged regions in the command schedule, not physical
isolation qualification. Three annotated maps are scenarios, not representative observed play;
dense stress remains separate. No safe850rpm or30s gameplay pass is claimed.

Coarse16 motor/driver subset plus **unquoted** reserve$497.68 leaves
$2.32/$502.32/$1002.32 at$500/$1000/$1500 for optics, structure, scales, docking,
feedback and transmission. Two-row-head control$984.64. At32/128 panels the$1000
remainder averages$15.70/$3.92 per panel if all other omissions were free.
Allowances are not quotes, a complete BOM or purchase authority. Longer waits
and premium cost remain product tradeoffs.

**Next discriminator:** compare a materially different actual-pin view preserving connected
guides and accessible resident thrust capture against this slotted-bay control. Include grounded
frame, service and acquisition cost before camera engineering. Stop fine and thin-polymer slots;
coarse metal remains conditional, not a complete module. No optical microdetail, print or owner
answer is required.

Checks: original262,144 ray samples/fault aliases and stock/error witnesses; 114,688
supported-bay rays plus196,608 extension rays; finite slabs/end ribs and interior obstruction.
Constant-section point-load closed forms agree with separate curvature integration/boundary
conditions for symmetric and asymmetric loads; dense point loads converge to uniform load. SI
reconstruction, force/moment balance, zero/load/E/t scaling, solid/net controls and400→800
samples/cell (<.005% circular-hole change) pass.1176 signed replays, boundary witness and
proof-slot replacement checks remain. These check calculations, not physical safety.
