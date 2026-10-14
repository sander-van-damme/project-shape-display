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
