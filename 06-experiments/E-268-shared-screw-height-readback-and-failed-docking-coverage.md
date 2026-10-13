---
status: complete
builds-on: [E-178, E-259, E-261, E-262, E-267]
---

# Actual-pin readback must preserve support and affordable shared machinery

**Stop detail on fine-grid slotted guides and direct row-end imaging.** Coarse metal optical
bays remain a conditional control. Looking through a hollow resident screw restores connected
guides in the ideal geometry, but moves risk into thousands of bores and unqualified ranging.
Discrete thrust-bed apertures can instead view integral pin-bottom corners while retaining solid
screws and both intact guides; coarse access survives the tested bounds, fine access is fragile.
Do not hollow screws merely to solve sensing. No camera, mechanism, process, print or purchase
is selected; E-263's declined print offer remains retired.

Reproduce `tools/curated-experiment-checks/E-268/{readback,support,structure,intact_routes,interstitial}.py`;
last two accept `--check`. Evidence: **rays, fault witnesses, elastic calculations and schedules**.
Self-review only; dimensions/loads/moduli/time/error scenarios are not measured priors or passes.

## What must be observed

10→20mm/lead2 witnesses: five motor turns with missed docking or five screw turns with stripped
threads leave10. Miniatures hide tops; detached marks can report20 while terrain stays10.
Require integral actual-pin targets, fresh frames and cell identity. Occluded/stale/wrong-target
means **unknown**. Correct height proves neither future retention nor a need for extra brakes.

51 integer-mm heights need≥6 code bits before redundancy; this is not continuous feedback.
Acceptance a with error e permits true error a+e. At850rpm/lead3,10/20ms delay adds.425/.850mm
before braking. Final inspection cannot prevent earlier overrun or establish power-loss hold.

## Earlier route controls and scoped failures

Executable sources retain the full sweeps and structural models; the following are the durable
boundaries. All errors, loads, moduli and timings are labelled scenarios, not measured priors.

**Slotted mirror route (`readback.py`, `support.py`, `structure.py`).** Lower guide2mm thick at
z=S+5, upper40mm higher; fixed reading datum S+9 sees scale coordinates7…47/57 on86/96mm pins.
A45° inter-row mirror faces a centered16-site reader at z−10. With4.4mm pins/.25mm pupil/±.5°
mirror tilt, nominal fine pitch needs .450mm slot and leaves−.005mm side web; e=.05 requires
.666mm/−.113mm and gives−.032mm backing clearance. Coarse e=.10 needs .885mm slot/.412mm web
and .130mm backing clearance; e=.20 backing gap becomes−.070mm. S50 coarse slot.887mm.
The guide and thrust bed both obstruct the view. Web=`(pitch−slot−4.64)/2`; metal cannot replace
absent material. No tiny inserts/fingers repair. Finite supporting ribs obstruct some freely
sliding16-field rays, so fixed8/16-cell bays are a sufficient restricted policy, not universal.
Coarse1mm rib leaves .51mm aperture-gap margin after opposing .10 errors; fine cannot fit it.

The load path remains pin→thread→screw shoulder→thrust bed→rail→frame→table. A4.4mm shoulder/
3.6mm journal gives5.03mm² bearing area, not qualified wear/pull-through. Upward docking still
requires shared axial capture; optics cannot substitute for a keeper or unchanged-neighbor support.

Virtual-work beam calculation `delta=integral(M*m/EI,dx)`, `I=net_width*t³/12`, uses3.6mm holes,
discrete loads and solid/net controls; [AWC figures1/7/8](https://engineering.purdue.edu/~ce474/Docs/DA6-BeamFormulas.pdf)
check constant-section limits. Slots1.10mm coarse/.70mm fine, bed2mm, uniform.05N/site:

|Pitch / bay cells|Sag E1000 /E70000 /E200000MPa, mm|
|---|---:|
|6.35 /16|5.555 /.0794 /.0278|
|6.35 /8|.349 /.00498 /.00174|
|5.08 /16|5.325 /.0761 /.0266|
|5.08 /8|.334 /.00478 /.00167|

Fine is structural comparison only. Coarse16 constant-net bound9.947/.1421/.0497mm;6mm polymer
bed.206mm. Interior1×10mm rail adds2.101/.0300/.0105mm,12.8N per segment/6.4N per end; joint
stiffness1/1000N/mm adds6.4/.0064mm per end. A changed.20N load moves unchanged center.0564mm
in the E70000 constant-net control. No shear/torsion/creep/joint/strength qualification; large
linear deflections are invalid. The.05mm comparison allowance is not a product requirement.

Lower guide reaction=H(S+3)/40, upper=−H−lower. S50/H.10 yields+.1325/−.2325N; μ.3 gives.1095N
sliding drag. Torque.35Nmm adds.0795N/contact. Coarse1.10slot leaves .305mm ligaments;
combined inward edge loss0/.10/.20 gives E1000 local sag.0583/.192/1.429mm, E70000 .000833/
.00274/.02042, nominal stress4.96/10.97/41.82MPa. Shorter bays do not cure local edge weakness.
Gross-solid versus uncoupled lateral rails differ.0172 vs87.6mm (latter invalid): actual ladder
shear transfer is unresolved. Fine.70slot disconnects the guide (−.130mm). Stop local detail.

Board burden:4096/6400 pairs and seats,8192/12800 guide apertures and thin lower-guide ligaments;
two slotted layers have512/800 row spans in32/50 sixteen-square panels, or1024/1600 spans in
128/200 eight-square panels. Four fasteners/panel adds128/200 or512/800. Scales4096/6400,
mirrors128/160 totaling26.01/32.51m. Two full2mm sheets weigh1.78/5.19kg at assumed2700/7850kg/m³,
before cutouts. Panel opening is not demonstrated pair replacement. Tooling/finishing unquoted.

**Grazing row-end imaging (`intact_routes.py`).** Last target distance D, preceding downstream
edge d=pitch−2.2, corridor half-gap g=(pitch−4.4)/2: adverse recessed target/protruding neighbor
occludes at `e=g*d/(2D−d)`. Exact slabs confirm it. Full64/80 rows fail at.00484/.00117mm face
deviation; ideal opposite-end views at.00942/.00226; internal16 views at.01788/.00517. At f1200,
.16mm marks span only.00106/.000368px over full rows. Shared translation cancels, differential
play does not. Park this grazing route, not all side optics.

**Axial hollow screw (`intact_routes.py`).** A.8mm bore views the integral cap through both intact
guides.54/64mm thread,86/96mm pin and camera z−10 give range96…136/106…156mm. With.1mm-radius
pupil,.2mm target and combined.1mm radial straightness/alignment bound, convex rays clear≥.130mm.
Bores.8/1.0/1.2 in1.4mm root leave.30/.20/.10mm walls and89.34/73.97/46.02% inertia. Concurrent
.1mm adverse bore/root surface errors leave only.10mm wall for.8mm bore. E1000 pinned57mm Euler
loads.512/.424/.264N are ideal bounds; K2 divides by four. No safe RPM follows.

The.8mm bore admits only.537°/.465° centered point-camera cone. Even optimistic stereo baseline
filling its entrance with f1200/.1px gives S50 depth error1.41…3.16mm; longest range needs≥7592
focal pixels for illustrative.5mm error. [ST VL53L4CD DS13812 Rev8 pp8/25](https://www.st.com/resource/en/datasheet/vl53l4cd.pdf)
(checked2026-10-13) specifies25° exclusion and22°/18° detection volumes in stated conditions;
these do not qualify a sub-degree bore. Wrong-wall returns must remain unknown. This route
removes scales/mirrors but adds4096/6400 bores/targets/inspection duties with67.5/80 aspect ratio.
No bore/reader/printing selection; casting, machining or FDM still owe extraction and straightness.

## Discrete apertures: solid screws and intact guides

**Coarse geometric comparator only.** A circular thrust-bed opening at `(pitch/2,pitch/2)`
lets two shared pupils at z−10, separated along `(1,−1)`, view a .2×.2mm patch centered at `(2,2)`
on the integral bottom of each4.4mm pin. That surface moves z2→42/52, staying2mm below the intact
lower guide. No bore, mirror, scale or attached flag. Reader/projector/relay bodies remain unbuilt.

`interstitial.py` gives each pupil, target and plate independent ±e lateral bounds and expands
neighbor faces by e. These are **not process priors**. Convex rays at both bed faces bound the
opening; a rectangle above z2 excludes neighbors at every height when its margin is positive.
Exact slabs confirm clearance and an actual low-neighbor/high-target collision. Infinite cylinders
also bound screw/shoulder interference. Full-seat ligament subtracts adverse shoulder growth e
and aperture-edge loss e, in addition to the optical alignment envelope; no strength claim.

S50 results; both strokes checked. Pupil diameter is an optical entrance, not camera size:

|Pitch / baseline / pupil diameter, mm|e|Opening, mm|Neighbor margin, mm|Full-seat ligament, mm|Ideal depth error, mm|
|---|---:|---:|---:|---:|---:|
|6.35 /2 /.10|.10|3.610|.373|.285|.160|
|6.35 /2 /.50|.10|3.704|.211|.238|.160|
|6.35 /2 /.50|.20|4.268|.011|−.244|.160|
|5.08 /.5 /.10|.10|2.099|.042|.142|.641|
|5.08 /.5 /.50|.10|2.194|−.119|.095|.641|
|5.08 /.08 /.50|.10|2.192|.0007|.096|4.004|

Last row is a fragility witness, not a precision requirement; its pupils also overlap and need
an additional beamsplitter. Coarse e=.20 cuts the allocated full shoulder support, not proof that
every partially supported seat fails. Rounded3.8mm coarse opening at e=.10 leaves.190mm outside
full shoulder/.590mm to the expanded journal. No tightening or seat-cutout rescue is selected.

Range is12…52/62mm. With **assumed** f1200px and .1px disparity error, `sigma_z=D²*sigma_px/(f*b)`
gives .113/.160mm maxima at b2. No texture, focus, reflectance, exposure, spot steering or
calibration is demonstrated. Using [Edmund Optics' Airy relation](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/limitations-on-resolution-and-contrast-the-airy-disk/)
(checked2026-10-13), first-zero object-space radius≈`1.22*lambda*D/d`: at550nm/D62, .10/.50mm
pupils give.416/.0832mm. Tiny-pupil illumination spills beyond the.2mm patch; larger pupils change
access. Airy radius is not a centroid-error floor. Defocus, aberrations, stray returns and signal
remain unknown; no catalog rate/accuracy transfers. An integral nut target assumes an intact pin;
it cannot prove a separated cap's position or future retention. Occluded/stale returns stay unknown.

Board ledger: replace4096/6400 long bores with4096/6400 short bed openings/underside targets,
one designated corner per pin including a half-pitch border. All resident pairs/seats/two guides
remain; intact guide webs1.71/.44mm. Coarse3.6mm journal+3.8mm optical holes leave≈46.6% gross
planar area, not a stiffness pass. Old slotted-beam numbers do not transfer. Every opaque keeper
must clear the rays while capturing upward docking load; no keeper/mount/frame route is supplied.
Cut/machined sheet, casting or FDM owe flatness, finishing and load transfer. No resident optical
inserts;10s additional finishing/site still adds11.38/17.78h. Local pair repair remains unbuilt.

A16-output shared reader needs32 pupil/relay duties, not necessarily32 cameras. It must shift
half a pitch in both axes from the screw grid or use a separately cleared carrier. Retain below's
100ms exchange/q16 timings only as **granted-access controls**; no fixed bays are geometrically
required by discrete holes, but frame/keeper/body constraints may add them. No speed improvement
or complete optical BOM follows. **Stop fine-grid underside optics and further tiny-lens sweeps.**
E-269 now constructs a conditional shared service keeper and single-pair extraction route.
Coarse access survives its planar screen; whole-sheet support/manufacture still govern reader work.

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

**Next:** E-269 adds conditional coarse axial capture and pair extraction, and rejects the fine
combined keeper/optical layout. Resolve shared frame support, service-lock access and docking
force before reader detail; keep all timing/cost controls. E-263 remains retired; no owner blocker.

Verification: original262144 rays/fault aliases,114688 supported-bay and196608 structural-extension
rays; slab/rib obstruction and end clearances. Independent beam closed forms, curvature
integration, force/moment balance, SI/load/E/t scaling and400→800 samples/cell (<.005% change).
1176 signed replays and proof-slot replacement. New12960 bore rays plus continuous convex bound,
exact face-error roots/slab witnesses, annular-area integration, disparity finite differences,
no-op and dense serial-read/retry identities. These verify models, not hardware.

Interstitial verification:36864 exact neighbor-slab checks, continuous convex plate envelopes,
explicit occlusion witness and finite-difference triangulation sensitivity; both strokes/pitches,
two pupil sizes and three independent/coherent error bounds. Model verification only.
