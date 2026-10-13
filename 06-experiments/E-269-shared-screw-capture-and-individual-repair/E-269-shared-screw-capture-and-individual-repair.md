---
status: complete
builds-on: [E-268, E-261, E-260]
---

# A shared service keeper can release one pair without removing the thrust bed

**Retain the coarse construction as conditional; stop the fine embodiment.** A shared plate
can capture resident screw collars in operation and shift 1.2 mm to let one complete pair
leave upwards through intact guides. Neighboring downward load paths remain on the fixed bed.
The coarse geometry has connected retaining material; the fine optical cutouts isolate it.
Neither result qualifies manufacture, force, safe docking, or full-board repair.

Reproduce `python3 tools/curated-experiment-checks/E-269/capture.py` (`--check` for assertions;
Python + numpy). Evidence: **bounded planar geometry, ideal service-state replay and statics**,
self-reviewed. No new measured material/process data, print offer, purchase or selected head.
E-263 remains retired. Dimensions below are hypotheses, not reconstructed successful prints.

## Construction and repair sequence

Retain E-261's solid screw, 4.4-mm square pin, 4.64-mm intact guide openings, 54/64-mm usable
thread and 86/96-mm pin for S40/S50. In thread-origin coordinates, allocate:

- Fixed lower bed z−5…−3, circular 3.6-mm journal holes; the entire underside drive end is
  at most 3.2 mm diameter and ends at z−7. Actual drive-socket strength remains unconstructed.
- Integral 4.4-mm-diameter collar z−3…−1, seated on the bed. No separate retaining ring.
- Shared keeper z−.8…+.8: 1.6 mm thick, with .2-mm nominal axial float above the collar.
- Each keeper opening is a radius1.8 capsule along y0…1.2, union a radius2.4 circle centered
  at y1.2. The operating screw axis is y0. Shift the whole keeper −1.2y to align the service
  circle with the screw. The 3.2-mm neck stays inside the capsule throughout the shift.
- Keeper optical holes remain centered at interstitial corners **in the operating position**.
  They need not transmit a reading during maintenance. Restore registration before operation.

Downward support is pin→thread→screw→collar underside→fixed bed→frame, including during service.
Upward docking load is collar top→keeper→frame **only in the locked operating position**.
The keeper is not an added pin brake and does not establish passive thread holding. Its .2-mm
float permits up to .2 mm screw/pin rise before capture, before elastic deformation; unchanged
neighbors can also move if the shared structures bend. There is no disturbance qualification.

Service transaction, granting an intact or jammed-but-straight pair and existing passive hold:

1. Park and de-energize the writer; clear the target miniature. Keep the board horizontal and
   prevent accidental upward loads. Release the keeper's shared lock and shift to service.
2. Pull **the pin and its engaged screw together**. There is no need to drive a jammed thread
   to its end. The 4.4-mm collar passes the 4.8-mm service opening and both 4.64-mm square
   guides; the 3.2-mm drive end passes the fixed 3.6-mm bed hole. Neighboring screws stay seated.
3. Lift at least94/104 mm for S40/S50 so the z−7 drive tip clears the upper guide at z86/96,
   including1 mm allowance. At maximum initial extension the pin top reaches z222/252.
   This is real overhead service clearance, not available gameplay travel.
4. Lower a replacement assembled pair, seat its collar, restore/lock the keeper, and verify
   registration, target height and neighbors before play. A wrong-height replacement needs
   local correction; the model does not grant free homing or an automatic repair cycle.

All cells sharing that keeper temporarily lose **upward** capture. Their normal downward support
is not released, but this is a powered-off maintenance mode, not continued playable actuation.
A bent/fractured trapped part, stripped pin that separates from its screw, inaccessible grip,
wide terrain cap, or displaced guide is outside this extraction proof; module access remains
necessary for those faults. A 5.0-mm collar cannot pass the4.64-mm guides: widening the collar
is not a free escape from capture margins. Forcing parts through the guides is not a repair plan.

## Optical and material continuity checks

Reuse E-268's two .5-mm pupils at z−10, .2-mm bottom patch and independent ±.1-mm lateral optical
bounds. Baseline2 mm coarse/.5 mm fine. Recompute ray envelopes through the **new** bed and keeper
faces; do not reuse the old3.8-mm hole blindly. At S50:

|Pitch, mm|Keeper optical hole, mm|Bed optical hole, mm|Neighbor ray margin, mm|
|---|---:|---:|---:|
|6.35|3.8872|3.0889|+.2112|
|5.08|2.2661|1.9276|−.1190|

These envelopes include plate/ray alignment bounds; additional edge-loss scenarios below are
separate. The lower bed retains the full nominal collar footprint with .7457/.4283-mm ligament
before edge loss. Its positive remaining area is not a stiffness/strength certificate. The pupil
is only3 mm below the drive-end plane; actual shared driver/reader bodies, withdrawal and frame
clearance remain unconstructed. Extra3 mm to the bed reaction also changes screw support from
E-262; no operating RPM transfers.

Planar test: a3×3 keeper kernel plus2-mm external rim, nine screw openings and surrounding optical
holes. Expand each hole by the pixel half-diagonal; accept only whole solid squares and connect
by shared edges to the external rim. Count collar contact only where those squares lie entirely
inside the collar. This gives a **sufficient connected-material subset**, not a contact-pressure,
stress or finite plate-bending solution. Erosion is common across the entire kernel, so this is
not an independent-cell yield model.

At fine pitch, successive keyholes overlap vertically by `.32 mm = 4.2−(5.08−1.2)`.
An optical opening overlaps the neighboring service circles horizontally by .6613 mm. Those
open-hole chains form closed barriers around the retaining patches; e.g. collar points
(x,y)=(±2,−.5) are solid but isolated. The raster independently finds zero grounded collar area
and14.82 mm² of isolated whole-cell material. Removing optics restores connected strips in the
same model. This is a scoped combined-layout failure, not a ban on every fine-pitch keeper.
At coarse pitch the vertical chain has a .95-mm gap; a grounded path survives this test.

Let `a` enlarge keeper-hole edges and shrink the collar radially; let `r` independently bound
collar/keeper misregistration in each lateral axis. A guaranteed inscribed collar disk shrinks
by an additional `sqrt(2)*r`. These are deliberately competing bounds, **not X1C priors**.
S50/coarse results (S40 has the same capture geometry):

|a / r, mm|Grounded contact subset, mm²|Point-sampled area estimate, mm²|Grid step, mm|
|---|---:|---:|---:|
|0 /0|2.0347|2.4001|.040|
|0 /0|2.2249|~2.40|.020|
|.10 /0|.7740|1.1155|.040|
|.10 /.05|.5359|.6882|.020|
|.10 /.10|.1567|.2965|.020|
|.20 /0|0|0|.040|

The last loss is exact: an enlarged2.0-mm-radius neck opening contains the contracted2.0-mm
collar, leaving no retaining area regardless of optics. Sampling precision is not manufacturing
accuracy. At a=.10/r=.10 the thin guaranteed contact is a warning, not an earned tolerance.
Nominal neck and service radial clearances are both .20 mm; summed neck/collar growth, inward
hole error and registration must fit that budget independently. The material-loss cases above
do **not** prove insertability or a batch-wide assembly window.

Under **assumed uniform pressure on the nominal sufficient patch**, its y centroid is−1.343 mm.
An upward docking force F therefore introduces1.343F Nmm of eccentric moment and, if the2-mm
bed journal alone reacts it, roughly.671F N of opposite radial reactions. At F=.05/.20/1 N,
that is .0336/.134/ .671 N per journal edge. Actual pressure, journal compliance, binding,
friction, collar bending and keeper/frame reactions are unmodeled. The nominal patch area is
not an axial-force rating. Merely adding a keeper does not make powered docking harmless.

## Whole-machine consequence and stopping point

At4096/6400 cells this construction retains4096/6400 integral collars, journal seats, drive
interfaces and thread pairs, and8192/12800 intact guide apertures. It adds4096/6400 keeper
openings with eccentric bearing duties and4096/6400 keeper optical holes; the fixed bed retains
its separate4096/6400 optical holes. No per-cell clip, spring, cartridge or service fastener.

The **whole-sheet hypothesis** has one service translation and shared lock/stop duties, but its
frame support, distributed upward load path and reachable lock are not designed. A3×3 bordered
kernel is not a tileable module: repeating its2-mm rims inside the board would consume pitch.
Do not claim16×16 panels, interior fastener positions, full-board stiffness or cheap modular
replacement from this test. At406.4-mm square, gross keeper stock is .264 L at1.6-mm thickness,
before holes/rim; E-268's assumed2700/7850 kg/m³ gives .713/2.074 kg before cutouts. A single sheet
exceeds the X1C's256-mm bed. Cut/machined sheet is a candidate process; tiling, casting/molding
or FDM still owe tooling, flatness, deburring, seams and support, not thousands of hand-fit fixes.

Two-part assembly and inspection remain E-260 duties. Adding10 s of cleanup per keeper opening
alone adds11.38/17.78 h; keeper plus bed optical deburring could add more. A shared slide does
not eliminate4096/6400 fits or verify them automatically. Service adds positioning, lock access,
extraction, replacement and inspection; no repair-time measurement is claimed.

Keep E-268's conditional850rpm/lead3/q16 comparison: coarse S40/N20 versus S50/N30 local maxima
21.67/25.67 s against the~30-s reference; S50 scene234.28 s, paid neutral282.23 s and dense stress
403.17 s. These remain granted reader/body access and one-retry scenarios, not speeds earned by
this keeper. The16-output dated subset plus unquoted reserve is$497.68, leaving only$2.32 under
$500 and$502.32/$1002.32 under$1000/$1500 for **all** missing support, docking, transmission,
sensing and assembly. No complete BOM, finished price or purchase authority follows.

**Decision:** the coarse construction removes a nominal service-topology obstacle without adding
private moving retainers. Park the fine combined embodiment and reject blind collar enlargement.
Stop before polishing keeper pockets or requesting prints. The next useful screen is a complete
shared support/frame and reachable service-lock construction, compared with a simpler opaque
keeper/readback control, including the docking-force budget; if it needs fragile internal webs
or thousands of added mounts, stop this layout rather than refine it. Optional owner printing
is not the blocker. Global manufacture, actual holding, powered engagement and repair of broken
parts remain open.

Checks:294 ideal service/support states,35,329 neck boundary points, independent negative-y
capture/release witnesses, fixed-keeper and wide-collar failures, exact aperture-chain overlaps,
coarse .04→.02-mm connected-subset refinement and midpoint-area agreement within .04 mm².
These verify the stated model and its scoped failures; no hardware has been validated.
