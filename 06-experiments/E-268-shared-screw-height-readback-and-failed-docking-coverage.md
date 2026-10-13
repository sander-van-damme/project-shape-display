---
status: complete
builds-on: [E-178, E-259, E-261, E-262, E-267]
---

# Actual-pin readback must preserve support and affordable shared machinery

**Stop detail on fine-grid slotted guides and direct row-end imaging.** Coarse metal optical
bays remain a conditional control. Looking through a hollow resident screw restores connected
guides in the ideal geometry, but moves risk into thousands of bores and unqualified ranging.
Do not hollow screws merely to solve sensing. No camera, mechanism, process, print or purchase
is selected; E-263's declined print offer remains retired.

Reproduce `tools/curated-experiment-checks/E-268/{readback,support,structure,intact_routes}.py`;
last accepts `--check`. Evidence: **rays, fault witnesses, elastic calculations and schedules**.
Self-review only; dimensions/loads/moduli/time/error scenarios are not measured priors or passes.

## What must be observed

10→20mm/lead2 witnesses: five motor turns with missed docking or five screw turns with stripped
threads leave10. Miniatures hide tops; detached marks can report20 while terrain stays10.
Require integral actual-pin targets, fresh frames and cell identity. Occluded/stale/wrong-target
means **unknown**. Correct height proves neither future retention nor a need for extra brakes.

51 integer-mm heights need≥6 code bits before redundancy; this is not continuous feedback.
Acceptance a with error e permits true error a+e. At850rpm/lead3,10/20ms delay adds.425/.850mm
before braking. Final inspection cannot prevent earlier overrun or establish power-loss hold.

## Slotted mirror route: geometric and structural limits

E-261 lower guide is2mm thick at z=S+5; upper guide is40mm higher. External pin scales at fixed
z=S+9 occupy local pin coordinates7…47/57 for S40/50 on86/96mm stock. A45° between-row mirror
redirects toward a centered16-site reader at z=−10. Inputs include4.4mm pins, .25mm pupil,
±.5° mirror tilt, backing and explicit correlated errors; no real image quality is established.

|Pitch / error e, mm|Backing clearance, mm|Envelope hits|Required slot, mm|Guide web per side, mm|
|---|---:|---:|---:|---:|
|5.08 /0|.068|0|.450|−.005|
|5.08 /.05|−.032|8192|.666|−.113|
|6.35 /0|.330|0|.454|.628|
|6.35 /.10|.130|0|.885|.412|
|6.35 /.20|−.070|0|1.400|.155|

All S40 samples reach the mirror; negative backing gaps still collide. Fine e=.10 has wrong-side
rays. Breakpoints≈.034/.165mm are not process capabilities; E-261 clearance permits.12mm play.
Coarse S50/e.10 needs.887mm slot/.411mm web; wider stems cannot inherit coverage.

Both opaque lower guide and thrust bed obstruct the view; occupied screw holes are not optical
windows. Required web is `(pitch−slot−4.64)/2`. Continuous slots disconnect transverse support;
terminate them at ribs between8/16-column bays. A1mm coarse rib in the1.71mm aperture gap leaves
.51mm after opposing.10mm edge errors; fine.44mm gap cannot accommodate it. An interior-rib ray
witness defeats freely sliding16-field coverage. Fixed aligned bays are one sufficient restricted
policy, not the only topology. Relays, extra cameras or independent reader travel require cost.

### Resident load path and frame

Path: pin thread→screw shoulder→thrust row→rail→frame→table, throughout docking/withdrawal.
Guides independently react lateral load/torque. Proposed4.4mm shoulder/3.6mm journal has5.03mm²
bearing area and.425mm coarse slot margin before play; wear/pull-through remain unqualified.
Upward docking needs shared axial capture, with keeper clearance, end collision and repair still
unconstructed. Count duties, not invented4096 clips. Neither guides nor optics prove retention.

Simply supported virtual work `delta=integral(M*m/EI,dx)`, `I=net_width*t³/12`, uses3.6mm holes
and discrete loads; solid/net controls bracket the beam calculation. [AWC figures1/7/8](https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf)
check constant sections, not material properties. Exclusions: local seat/hole effects, shear,
torsion, anisotropy, joints, creep and frame settlement. Large deflection invalidates linearity.

Allocate1.10mm coarse/.70mm fine optical slots, rather than spend every margin on fabrication.
E1000/3000/70000/200000MPa are competing scenarios, not qualified polymer/metal stock. At2mm
thickness and uniform .05N/site (a stress case, not typical play):

|Pitch / bay cells|Sag E1000, mm|E70000, mm|E200000, mm|
|---|---:|---:|---:|
|6.35 /16|5.555|.0794|.0278|
|6.35 /8|.349|.00498|.00174|
|5.08 /16|5.325|.0761|.0266|
|5.08 /8|.334|.00478|.00167|

Fine is structural comparison only. Coarse16 constant-net controls:9.947/.1421/.0497mm;
6mm polymer:.206mm. Deflection scales with load/t³. Board load.05N/site=204.8/320N. Interior
rail receives nF/row, n²F/segment; exterior half. Coarse16/1×10mm rail:12.8N,6.4N/end,
sag2.101/.0300/.0105mm, nominal stress9.754MPa. Eight-cell sag:.0660/.000942/.000330mm.
Coarse16 row+rail gives≈.109/.0383mm at E70000/200000 before joints. Thickening the polymer
row does not cure rail sag. Joint stiffness1/1000N/mm adds6.4/.0064mm/end; torsion is unmodelled.

The .05mm comparison budget is illustrative, not a requirement. A single.20N changed load near
center moves the unchanged center .0564mm in the E70000/2mm constant-net control: fixed screw
angle alone does not establish isolation.

### Lower-guide vulnerability

Lower reaction=H(S+3)/40, upper=−H−lower. S50/H.10 gives+.1325/−.2325N; μ=.3 drag.1095N
already exceeds the.05N axial scenario. Lower-guide torque.35Nmm adds.0795N/contact across4.4mm.

Coarse1.10mm slot leaves w=.305mm side ligaments. Treat a4.64mm edge as simply supported under
the full lower reaction, `I=2*w³/12`; fixed ends are a four-times-stiffer control, not a built joint.
For S50/H.10, excluding global movement:

|Combined inward edge loss, mm|w, mm|Sag E1000 /E70000, mm|Nominal stress, MPa|
|---|---:|---:|---:|
|0|.305|.0583 /.000833|4.96|
|.10|.205|.192 /.00274|10.97|
|.20|.105|1.429 /.02042|41.82|

Coherent edge shifts.05 each give.10 loss; .20 loss amplifies compliance24.5×. Torque.35 raises
contact to.2120N/stress7.93MPa before edge loss. Shorter bays do not fix local edges. No strength/
creep pass. Coherent H.10/site yields gross-solid lateral sag.0172mm versus uncoupled87.6mm
(outside linear validity): cross-tie shear transfer is unresolved, not proved metal failure.

Fine/.70mm gives w=−.130mm: disconnected even with perfect material; original.450mm already
gives−.005. A.20mm end rib leaves.04mm after opposing.10mm allowances, while the mirror collides
at e=.05. **Metal cannot restore absent geometry; stop before tiny inserts or guide fingers.**

### Manufacture and service ledger

At both pitches,8/16 bays,S40/S50,2/6mm thrust, sampled slots≤.89295/.68383mm; end margins
≥2.434/1.938mm. Centered rays clear10mm-deep rails. Mounts/keeper/body/transport are unconstructed.

|Whole board|64² /6.35mm|80² /5.08mm|
|---|---:|---:|
|Resident pairs / thrust-seat duties|4096|6400|
|Two guide-aperture sets / thin lower-guide ligaments|8192 /8192|12800 /12800|
|Two slotted layers' row spans,16 /8 bays|512 /1024|800 /1600|
|Two layers' square panels,16 /8 bays|32 /128|50 /200|
|Ground-grid nodes,16 /8 bays|25 /81|36 /121|

Four fasteners/panel adds128/200 at16 bays,512/800 at8. Ten seconds/pair costs11.38/17.78h.
Scales4096/6400; two mirrors/row=128/160 pieces,26.01/32.51m. Marking, seams, finishing and
alignment remain unqualified. Opening256/64-site panels does not prove single-pair repair.
Compare molded/cast/FDM with cut/machined metal or formed stiffeners, charging tooling/finishing.
Two full2mm sheets at density2700/7850 weigh1.78/5.19kg;6mm+2mm doubles it. Prices unquoted.

## Routes retaining intact guides

### Direct view from a row end

Camera20mm outside the row at y=pitch/2 sees +Y pin faces at the fixed read datum. All pins
occupy that datum throughout travel. For last target distance D and previous pin's downstream
edge d=pitch−2.2mm nearer, target recessed−e and neighbor protruding+e give clearance
`−2e+(g+e)*d/D`, `g=(pitch−4.4)/2`. Occlusion occurs at `e=g*d/(2D−d)`; common translation cancels,
differential play/warp does not. Exact slab intersections independently reproduce the witness.

|Pitch / viewed cells|Occluding face deviation, mm|Pixels across .16mm horizontal mark, f1200px|
|---|---:|---:|
|6.35 /64|.00484|.00106|
|6.35 /32, ideal opposite-end views|.00942|.00398|
|6.35 /16, internal access granted|.01788|.01409|
|5.08 /80|.00117|.000368|
|5.08 /40, ideal opposite-end views|.00226|.00137|
|5.08 /16, internal access granted|.00517|.00705|

Assumed angular projection requires≈2.26million focal pixels for two pixels/mark across the
coarse row. Opposing .05mm errors block even16-cell views. Internal access is not implemented.
**Park this grazing route**, not all side optics; no micro-mirror/tighter-guide rescue.

### Through the resident screw

An axial bore views the underside of the pin's integral closed top, unaffected by miniatures.
With54/64mm thread,86/96mm pin,2mm cap and reader z=−10, target range is96…136mm S40 and
106…156mm S50. Both guides and thrust-bed connections remain intact; passage through the seat
and drive end is also required. Optics carry no load. For .8mm bore, .1mm-radius pupil,
.2mm-radius centered target and **combined** .1mm radial alignment/straightness envelope, the
continuous ray envelope clears by≥.130mm. Target lean must fit that allocation; E-261's guides
do not establish it. Dirt, curvature, scattering, finite optics and reflectance remain unknown.
Wrong screw-tip/wall reflections must be rejected, not mistaken for cap position.

|Bore, mm|Wall at nominal1.4mm root, mm|Root inertia retained|S50 ideal Euler load, N|
|---|---:|---:|---:|
|.8|.30|89.34%|.512|
|1.0|.20|73.97%|.424|
|1.2|.10|46.02%|.264|

`I=pi*(root⁴−bore⁴)/64`; Euler uses E1000, pinned ends,57mm station, no defect/safety allowance;
K2 divides load by four. No safe RPM follows. Concurrent .1mm inward root and .1mm outward bore
surface errors leave only.10mm wall for the.8mm case. Do not enlarge the pin and inherit old
clearance/holding. E-262's support-limited modes remain relevant.

Clear rays are not accurate ranging. The.8mm bore/.1mm envelope admits a centered point-camera
cone of .537°/.465° S40/S50. Granting stereo baseline filling the entrance, `disparity=f*b/D` and
`depth_error≈D²*pixel_error/(f*b)`. At f1200/.1px error:1.15…2.38mm /1.41…3.16mm across travel;
longest S50 range needs≥7592 focal pixels for illustrative .5mm error before calibration/texture.
This sensitivity is not a universal precision bound or product requirement.

[ST VL53L4CD DS13812 Rev8, pp8/25](https://www.st.com/resource/en/datasheet/vl53l4cd.pdf), checked
2026-10-13, specifies25° collector exclusion and22°/18° detection volumes at100/1000mm under
stated white-target/dark conditions, with windows accommodating the exclusion zone and weak
signals reported as errors. Those conditions do not qualify this long sub-degree bore. Clipping
is not proof of total failure, but catalog rate/accuracy cannot transfer. No sensor selection.

Removes128/160 mirrors and4096/6400 scales; adds4096/6400 bores, targets and inspection duties.
Pairs/guides/capture remain. Intact web1.71/.44mm reconnects guides without qualifying the frame.
Molded cores, machining, outsourcing or supported FDM owe67.5/80 bore aspect ratio, extraction,
cleanout and straightness. Extra10s/site adds11.38/17.78h. No new print or per-cell cartridge.

## Complete waiting and cost comparisons

Use E-267's16-output writer, conditional850rpm/lead3, same physical river/ravine at both pitches,
S40/neutral20 or S50/neutral30. Charge seeks, return,4s common allowance and one immediate retry.
No safe speed, physical isolation or representative-play pass is claimed: three maps and133
nonempty four-square reveal windows/depth remain scenarios.

Slotted readout replaces20ms proof with100ms per field. At free16 coarse stations this gives
19.97/23.97s local maxima; fixed support bays incur extra stations:

|Pitch / stroke|Free16, s|Fixed16 bays, s|Fixed8 bays, s|
|---|---:|---:|---:|
|6.35 /40|19.97|31.75|31.50|
|6.35 /50|23.97|39.52|39.26|
|5.08 /40|37.11|50.58|64.44|
|5.08 /50|46.59|64.22|82.79|

Fine lacks feasible optics/support. Coarse fixed16 penalty≤12.28/16.05s; boundaries add visits.
Large scenes179.25/208.66s; cold-neutral196.06/256.53s separately. Two-row heads give17.94/21.94s
coarse,20.75/25.69s fine, but require128/160 drives and8/10 fields; body/transport unconstructed.

Axial ranging needs the driver out of the way. Grant100ms shared exchange,100ms/read group and
50ms between serial groups of q changed cells; optical paths/read-shuttle not constructed. A
hollow drive or beam splitter is not free. Replace the20ms proof slot and recompute worst full
station retry; do not add unrelated maxima. Only changed pins are observed: unchanged-neighbor
verification and persistent-fault recovery remain outside the successful single-retry scenario.

|Pitch / stroke|q16 local max, s|q4, s|q1, s|
|---|---:|---:|---:|
|6.35 /40|21.67|29.32|59.92|
|6.35 /50|25.67|33.32|63.92|
|5.08 /40|41.11|50.56|97.30|
|5.08 /50|50.69|60.14|106.94|

Free exchange/q16 recovers the free-field control: slotted-bay delay is not unavoidable, but
axial optics have not earned that access. Coarse S50 q16/q4/q1 large-scene maxima234.28/277.63/
505.89s; cold-neutral282.23/397.88/860.48s; separate dense50 stress403.17/518.82/981.42s. q16
means16 parallel reusable optical paths, not necessarily16 cameras or one free camera field.
These schedules require passive support while exchanging heads, not qualified by readback.

Coarse16 dated motor/driver subset plus **unquoted** reserve$497.68 leaves$2.32/$502.32/$1002.32
under$500/$1000/$1500; two-row control$984.64. Entire$1000 remainder permits$31.40/q16 channel
($62.65 under$1500), with fabrication/support/docking/transmission unpaid. Alternatively it gives
$15.70/$3.92 per32/128 slotted panels. These are allocations, not BOM/retail price/purchase authority.

**Next:** compare accessible actual-pin sensing retaining solid threads/intact guides; screen
manufacture/access before detail. Keep these controls. E-263 remains retired; no owner blocker.

Verification: original262144 rays/fault aliases,114688 supported-bay and196608 structural-extension
rays; slab/rib obstruction and end clearances. Independent beam closed forms, curvature
integration, force/moment balance, SI/load/E/t scaling and400→800 samples/cell (<.005% change).
1176 signed replays and proof-slot replacement. New12960 bore rays plus continuous convex bound,
exact face-error roots/slab witnesses, annular-area integration, disparity finite differences,
no-op and dense serial-read/retry identities. These verify models, not hardware.
