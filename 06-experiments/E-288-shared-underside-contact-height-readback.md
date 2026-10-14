---
status: complete
builds-on: [E-270, E-277, E-286]
---

# Shared underside contact height readback

**Park the fixed off-axis contact probe as final actual-surface verification.**
It reaches a different observable from screw angle and escapes miniature occlusion
in principle, but the complete proposed path cuts the keeper edge, lacks a
full-travel landing guarantee under inherited guide bounds, and can move the
object it purports to measure. Do not rescue it with another tip/port-clearance
sweep. Reopen through a materially different accessible observation path or
measured alignment/contact-force evidence, including post-release height.

Evidence: analytic rigid envelopes, quasi-static counterexamples and allocated
schedule/cost/operations, self-checked by
`python3 tools/curated-experiment-checks/E-288.py`. Not CAD/contact simulation,
sensor specifications, process capability or physical qualification. E-281 stays
optional and unperformed; no print, purchase, supplier contact or owner question.

## Construction and supported transaction

Retain E-277's half-square 12.7-mm grid, 10.3-mm constant-section body, 10-mm nut
and 136-mm total length; nut underside Z2…52 and top Z138…188. E-286 retains the
E-280 screw ends: driver/collar diameter4.4 at Z−10…−4, journal2.8 at Z−4…0.
The fixed 12×24-mm spine spans Z−34…−10; two locked keeper halves surround the
journal. All existing thread, guide, thrust and upward-capture obligations remain.

New shared tool: a vertical1-mm-diameter stylus, offset3.5mm in Y from the screw
axis, rising through2-mm passages in **both spine walls and the keeper** to touch
the nut underside. Its measured independent Z axis and force trigger travel with
the rotary head; four25.4-mm-spaced writers would require four separately stopping
probe channels to read unequal heights concurrently. A common rigid probe lift
cannot obtain four independent heights merely by counting four tips. No sensor
is resident in each column, but three access layers repeat at every site.

Stop rotation → withdraw socket → settle → raise the probe from Z−36 → detect
contact or return unknown → retract below Z−36 → settle. Thread→driver→spine→frame
remains the downward path; locked keeper remains the upward path. Probe force
adds an upward load and can unload the gravity thread flank. Unexpected force,
missing contact, blocked passage or uncertain identity is **unknown**, never a
height pass. Keepers must be closed while probing; no service opening or neighbor
reset is credited. Broken support requires service rather than repeated probing.

With an intact rigid body, nut height plus known body length estimates the terrain
top even under a miniature. This does not prove body length, a joined nut/cap,
straightness or integrity: equal nut locations with intact versus damaged tops
can produce identical readings. That limit also matters for the joined-body
manufacturing alternatives; do not call this direct cap observation.

## Access and landing discriminate before sensor selection

The centered nominal tip clears the2.2-mm collar radius and lands outside the
1.75-mm conservative thread-mouth radius. However, the selected keeper half has
4.5-mm outer reach: `4.5 − 3.5 − 1 = 0` nominal outer ligament around its port.
This would be an edge notch, **not a closed probe bore**. Its stiffness/capture
consequences are unconstructed. Spine passages leave1.1mm nominal separation from
the central2.8-mm tool hole and only.3mm from the driver footprint; local thrust
plate deformation, burrs and accumulated alignment are not qualified. Changing
keeper/spine support is a mechanical redesign, not free sensing access.

Assume the same guide opening maximum10.9, body minimum10.2, independent guide
placement±.1 and82-mm face span as E-277; lower guide face Z54. A relaxed yaw-free
one-coordinate nut-center bound at base z is
`d(z)=.1+(10.9−10.2)/2+(54−z)(10.9−10.2+.2)/82`.
Allocate probe/head placement±.2 and tip radius.5. A fully supported contact
footprint outside the bore and inside the square face along this axis requires
`1.75+d+.7 ≤ R ≤ 5.1−d−.7`.

|Nut base z, mm|Center bound d, mm|Allowed fixed offset R, mm|
|---|---:|---:|
|2|1.0207|3.4707…3.3793: empty|
|22|.8012|3.2512…3.5988|
|32|.6915|3.1415…3.7085|
|52|.4720|2.9220…3.9280|

At R3.5/z2, opposing axis witnesses give+.0293mm bore margin and−.1207mm outer
margin. The relaxed offset interval is empty by.0915mm; moving this one tip
cannot earn the stated full-footprint guarantee. Partial edge contact may happen,
but its force/height bias is not the assumed flat-face contact. Yaw, tip shape
and cross-axis effects have been omitted favorably, not verified away.
**These independent guide bounds need not all be physically reachable with a
straight engaged screw**: the thread may constrain the nut, or bind/bend instead.
This is a failure to establish robust readback from existing evidence, not proof
that every assembled pair misses, nor a measured failure rate. An actual coupled
alignment envelope could reopen the question; nominal centering cannot.

A2-mm port with−.1mm diameter error,±.2 placement and.2 bow leaves only.05mm radial
reserve around a1-mm stylus. These are explicit bounds, not X1C statistics. Reach
from Z−36 to the highest nut is88mm. Ideal E200GPa rod Euler bounds are12.51N
pinned/pinned and3.13N fixed/free: gross rod buckling is not the discriminator at
.05N, but those assumptions do not qualify tip straightness, port rubbing,
trigger force, metrology or crash behavior.

## Contact can create a false height pass

Consider frictionless axial lash as a limiting case, with the screw stationary.
If upward trigger force exceeds body weight, the probe can move the body from
its gravity-loaded thread flank to its opposite flank before triggering. With an
assumed3-g body and.05-N trigger, weight is.02943N. A body resting at30mm with zero
lash and one resting at29mm with1mm lash both trigger at30mm. After retraction,
the second returns to29mm. This is a constructive observation ambiguity, not a
prediction of lash/friction distributions. Sander's rough~1mm historical play
motivates considering the mode, but does not measure the new geometry's lash.

Reducing trigger to.02N distinguishes this particular3-g example; it does not
establish a universal safe setting. Assumed1/3/5/14-g bodies weigh
.00981/.02943/.04905/.13734N. A1-g body can lift even at.02N, while miniatures may
bridge other columns and supply no local preload. Force uncertainty, overshoot,
friction, compliance and damage remain additional variables. At.05N, effective
stiffness.1/1/10N/mm gives.5/.05/.005mm displacement before other errors. Common
calibration error does not average away over a row. Actual lowest weight, trigger
and post-release motion need evidence; neither motor counts nor another contact
at the same force resolves the alias. Later creep is also unobserved.

## Whole-machine consequence and decision

Assume50mm/s,500mm/s², .1s contact and.2s post-release settling. A complete
search/retract from Z−36 takes2.02…4.02s for bases2…52. Unknown actual height means
budgeting the full path; approaching only the commanded height can miss a fault.
Four independent channels give4.02s per occupied four-site group before XY seek,
socket withdrawal, retries or additional proof. One/four/eight/sixteen groups add
4.02/16.08/32.16/64.32s of read-only work. Eight groups already exceed the~30s
reference before terrain motion. This is a scenario count, not typical play or
a newly replayed map benchmark.

|Sites / comparison grid|Access passages in three layers|Four-channel dense read, s|If each passage needs10–30s finishing, h|
|---|---:|---:|---:|
|1024 /12.7mm|3072|1029.12|8.53–25.60|
|4096 /6.35mm|12288|4116.48|34.13–102.40|
|6400 /5.08mm|19200|6432.00|53.33–160.00|

Fine-grid rows are counts only: unchanged coarse bodies/keeper geometry do not fit.
Single-channel dense inspection takes4116.48/16465.92/25728s. Cutting passages in
registered sheet batches or machining a stack could avoid individual drilling,
but chip removal, deburring, alignment, wall support and rejection are unpaid;
no thousands-of-hand-operations route is accepted. The tool adds only1/4 measured
axes, force channels and replaceable styli, yet adds3N access/inspection sites.
Retain2N bodies/screws,2N guide apertures,N thrust contacts and existing keepers;
no resident function or assembly operation has been removed.

Explicit **unsourced cost allocations**, not quotations: per channel axis$15–50,
force$10–30, position read$5–20, stylus$5–10, mounting$5–10 = $40–120; shared
control/fixture$40–120. One/four channels add$80–240/$200–600 before support
refabrication and integration. Added to E-276's optimistic$798 allocation gives
$878–1038/$998–1398, not a complete demonstrator BOM. The~$500 reference is still
missed; a~$1000 finished device or$1000–1500 demonstrator remains a value question,
not authorization or an earned price. No automatic supplier quote is implied.

E-276's existing850rpm S40/S50 local26.84/31.07s, scene201/223s,
neutral271/332s and dense392/452s remain conditional reference calculations.
Do not simply add the above reads and claim a new map prediction: replace the old
unqualified proof, enumerate actual groups and charge routing/retries first.
Minimum rest versus elevated neutral does not remove readback: signed travel and
paid initial preparation remain real; the40-mm/reference dense case is separate
from the50-mm alternative. A slower diagnostic can still be valuable, but this
construction does not earn safe final verification beneath occupied terrain.

The new decision is to avoid adding three access layers and four probe axes on
this evidence. Preserve nut-side observation as a possible principle; a next
construction must change the observation/access or establish nondisturbing,
post-release measurement, not optimize this nominal hole pattern. No additional
service-cage, tip-margin, or repeat schedule sweep follows from this result.


## Top-contact control: two forces do not prove released height

**Retain force extrapolation only as a calibrated diagnostic, not general final
verification.** E-270 already screens top access, miniature occlusion and timing;
this extension tests a new correction hypothesis rather than repeating those
screens. Reproduce with the same E-288 source. All forces, stiffnesses, errors
and fault travel below are explicit analytical scenarios, not measured priors.

Move the shared force-limited measured-Z stylus above the exposed terrain cap.
Stop/undock the writer, settle, touch downward, record positions at added forces
F1=.02 and F2=.05 N, retract and settle. Existing thread/thrust/keeper support stays
engaged. Downward force does not unload the gravity-loaded thread flank as the
underside probe can; direct cap contact also avoids inferring top integrity from
nut position. It removes the proposed 3N underside passages (3072/12288/19200 at
1024/4096/6400 cells), adding no resident sensor or witness. But it requires an
upper carriage, independent Z/force channels, collision protection and registration.
No reduced complete-machine price follows: upper motion and guarding are uncosted.
E-270's top access and long read cycles still apply, as do its covered-pin aliases.
An unknown miniature/prop contact cannot be accepted as a terrain measurement.

For a reversible linear law `z(F)=h−F/k`, the zero-added-force estimate is
`h_hat=(F2*z1−F1*z2)/(F2−F1)`. This exactly removes unknown linear compliance:
48 finite cases span h0/20/30/50 mm, k.1/1/10 N/mm and two choices for each force.
It does not remove common height datum bias. Independent bounded position errors
±.05 mm amplify to ±.1167 mm at .02/.05 N. Independent actual-force errors ±.002 N
alone give bounds .04667/.004667/.000467 mm for k.1/1/10 N/mm; combined errors can
add. These are worst-case corner bounds, not statistical confidence or sensor specs.

A continuous, reversible fault defeats the correction without friction or lash:

- A: `zA(F)=30−F` (k1 N/mm), released top30 mm.
- B: `zB(F)=31−F−min(1,F/.01)`, released top31 mm. An initially soft,
  gravity-preloaded element compresses an additional1 mm by .01 N, then rests
  against a stop; an ordinary k1 element remains in series. This is a constructive
  compliance law, not a claim that an existing printed part has this response.

Both return29.98/29.95 mm at .02/.05 N and extrapolate to30 mm; after release B
returns31 mm. Additional readings or unloading repeats entirely above .01 N give
identical curves. A .005-N read distinguishes this witness, but without an earned
lower stiffness or upper travel bound a softer transition can lie below any finite minimum
read force. The source constructs three such cases. Continuous zero-force contact
tracking could change the observable; it owes qualified near-zero force resolution,
contact identity and the actual release event, and is not supplied by extrapolation.

This is not proof that every contact method fails or that ordinary intact columns
are soft. It identifies the missing qualification needed to call the corrected
reading a final height: a verified reversible force law down to release, a bound
on unobserved compliant travel, or an independent fresh released-cap observation.
A supported miniature can still hide the actual cap even with ideal force sensing.
Neither ramps restricted above the transition nor screw-angle agreement resolves
these witnesses.

E-270 already exceeds the ~30-s reference for its serial probe gameplay cases,
with separate dense stress, S40/S50 and paid neutral cases. The bounded accounting
below adds the missing 1024-site and independent four-channel controls; it does
not rerun those map schedules or grant free force acquisition.
The 5.08/6.35/12.7-mm comparisons, raised neutral and ~$500 versus premium cost
references remain open product trades; slower diagnostics may be useful off-table.
Do not select automatic verification from this correction alone. A bench force-displacement
measurement with independent released-height observation could calibrate a survivor;
no new owner print, sensor purchase or fragile stylus CAD is justified by this model.


## Top-contact access, faults and scale closure

**Keep top contact as an exposed-cap diagnostic; stop before probe CAD.** The
source now explicitly checks missed upward/downward moves, damaged tops at an
unchanged nut and post-undock slip. Under the qualified-linear-law *assumption*,
these change the direct cap intercept and are detectable, although the cause is
not identified. Underside nut readback cannot distinguish damaged tops. Neither
route observes later creep; the stopped-compliance witness above defeats top
contact even with perfect identity and no sensor error.

A rigid opaque 25.4-mm square base, supported by other cells at z30, has underside
30 and top32. Central caps at29 versus28 produce identical first contact32 at all
three pitches. The base covers the entire central cap, so moving the stylus within
that cap does not resolve it. The source grants perfectly rigid surrounding
supports and checks base/support overlap; this is an explicit obstruction witness,
not a miniature-load model or a claim about every base. Recognized obstruction
must return **unknown**; unrecognized prop contact can falsely pass a command32.
Higher parking clearance prevents traversal collisions only for obstacles inside
that assumed height envelope. It cannot reach through a miniature. Clearing and
replacing miniatures changes loading and interrupts play (E-270); do not grant it
as routine verification or retry by moving a hidden loaded pin.

For an empty vertical shaft, radius.5 + placement.2 + bow.2 = .9 mm. Nominal
centered cap widths10.3 at12.7 pitch and4.4 at6.35/5.08 pitch leave landing
margins4.25/1.30/1.30 mm and nearest-neighbor margins6.65/3.25/1.98 mm. These
relaxed bounds exclude cap lean/yaw, guide and manufacturing variation, tip
housing and actual force sensing; they demonstrate a nominal access route, not
full-travel qualification. The fine grids use E-270's narrower cap control;
E-277's10.3-mm body is not shrunk silently into those arrays. Shared precision
could be machined or purchased, but repeated cap finish and integrity remain
unqualified. No new per-cell holes, marks, sensors or manual finishing is selected.

**Calculated read-only scaling**, not typical gameplay or achieved speed: park
H60 mm above maximum terrain, search full S40 or S50 downward, retract, acquire
two force readings at.1 s each and settle after release for.2 s. Retain assumed
50 mm/s and500 mm/s². Cycle `2*t_move(S+H)+.4` is4.6/5.0 s. This favorable
allocation does not qualify the force ramp or release; two-force acquisition may
need more time. Four channels must each independently stop and measure Z/force.
A rigid four-tip crossbar sees the highest cap; lower unequal states alias in the
source witness. Four-channel timing grants perfect grouping and excludes XY
routing, initial deployment, writer undocking, reference checks and retries.

|Cells / pitch, mm|Single-channel S40 / S50, s|Four-channel S40 / S50, s|
|---|---:|---:|
|1024 /12.7|4710.4 /5120|1177.6 /1280|
|4096 /6.35|18841.6 /20480|4710.4 /5120|
|6400 /5.08|29440 /32000|7360 /8000|

These dense scan components are paid whenever full-board readback is required,
even if few cells moved. Changed-only inspection requires independently earned
unchanged-neighbor isolation. One/four/eight active groups cost4.6/18.4/36.8 s
at S40 and5/20/40 s at S50 before writing/routing; eight groups exceed the~30-s
reference already. They are scenario counts, not player-frequency estimates.
An empty-board H5 plane reduces cycles to2.4/2.8 s but cannot safely traverse
unbounded props. One retry pays another complete cycle for its group; persistent
obstruction has no finite scan-to-accept time. Minimum rest and elevated neutral
both owe actual-height search; elevated neutral also retains its paid preparation
and real downward headroom. A commanded-height shortcut can miss a low fault.

Compared with underside sensing, top contact removes3N access passages and the
nut-to-top integrity inference but adds upper-carriage access over the play area.
It retains all column/thread/support functions and repeatsN surface contacts per
full scan. One/four measured Z axes, force channels, replaceable tips, shared XY,
reference and collision protection are still necessary. Earlier$80–240/$200–600
channel allocations exclude the upper gantry/guarding and are **not** a top-system
quote or complete BOM; no demonstrated$500,$1000 finished or$1000–1500 prototype
price follows. More spend or a longer acceptable wait cannot resolve hidden-cap
identity or force-induced ambiguity. A slow empty-board/service diagnostic may
still have value. Reopen automatic acceptance only with earned release behavior
and cap access, or an independent fresh released-cap observable. No detailed CAD,
print, purchase or hardware qualification follows from this bounded screen.
