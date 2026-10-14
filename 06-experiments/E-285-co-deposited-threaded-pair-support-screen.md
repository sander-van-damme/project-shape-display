---
status: complete
builds-on: [E-277, E-279, E-280]
---

# Co-deposited threaded pair: support and assembly screen

**Printing an already engaged screw inside the integral column does not inherit
its separate components' bed support.** Park this unchanged-geometry production
proposal before a new fit/support campaign. A removable pedestal could make it
possible, but it substitutes release and inspection for threading rather than
establishing an assembly saving. This is an analytical screen, not CAD contact
validation, slicing, a printability rejection of every orientation, or a print job.

Construction: E-277's 136×10.3-mm upright integral closed/U column with its
10-mm, 90°-profile nut; E-280's completed 64-mm threaded screw with lower
journal and 4.4-mm collar/driver extending to screw-local Z=-10. Place the nut
bottom at Z=2 (engaged low position), with matching screw phase. The torque path,
passive threaded load path, shared thrust/anti-rotation guides and direct moving
writer remain unchanged. Co-deposition does not construct those shared supports,
qualify retention, or provide height verification. Screw phase/contact and
finite-clearance deposition would still need checking before manufacture.

`tools/curated-experiment-checks/E-285.py` calculates exact support-plane extrema
of the retained body corner and circular collar rim for a tilt toward the U's
retained wall. The collar is below the journal and thread envelopes throughout
0–90°; its socket does not remove the extremal rim. Thus these extrema do not
require a guessed thread friction, shrinkage distribution or slicer model.

|Pose, axis from vertical|Body above bed|Screw above bed|Consequence|
|---|---:|---:|---|
|0° upright|12 mm|0|Column starts in air; needs a pedestal/support or changed construction|
|90° horizontal, U open upward|0|2.95 mm|Screw starts in air within body; needs internal support|
|76.1887° tilted|0|0|Both touch at extremities, but longitudinal lower surfaces are shallow|

For the tilted pose, successive longitudinal boundary tracks shift 0.814 mm
at the comparison's 0.2-mm layer versus 0.45-mm extrusion width. They have no
same-track overlap. At 0.1-mm layer the shift is 0.407 mm, leaving only 0.043 mm
nominal overlap; neither value proves printable or unprintable material.
Interior infill/bridging may support a perimeter; no slicer paths were generated
for this assembly. The zero-overlap threshold is 0.1106-mm layer. This is a
geometric deposition diagnostic, **not** a new process tolerance or permission
to start a fine-layer sweep. Projected body length is 134.53 mm, so the upright
289-up assumption cannot simply carry over to tilted packing.

An upright annular pedestal could support the column without deliberately
supporting the working screw thread. It would add a release interface under
every nut and requires access around each finished screw; exact material,
removal force, clean separation and bed adhesion are unknown. The open U gives
better cavity access than the closed body but does not remove the nut's threaded
engagement. Simultaneously deposited internal/external threads must remain
separable; E-281's separately printed fit test cannot qualify that. Binding may
scrap both parts, and removal/repair must preserve the screw's accessible head
and thrust surfaces. No guessed failure probability is assigned; a common
first-layer/process bias may affect an entire plate.

## Whole-machine consequence and stop rule

At N cells this removes **at most N initial pair-threading operations** versus
separately printed integral columns and screws. It removes no resident part:
N bodies, N screws, N mating threads, 2N guide apertures and N shared-structure
thrust/capture sites remain. No column end joins existed in the integral control
to remove again. Pedestals add N release sites; screw/column inspection,
installation, height commissioning and individual repair remain. One printing
job is not one manufactured mechanism or one finishing operation.

For explicitly assumed 5/15/30 seconds of saved threading per pair:

|Replication|Potential saved maker hours before any added work|
|---:|---:|
|1024 (12.7-mm pitch)|1.42 / 4.27 / 8.53|
|4096 (6.35-mm reference count)|5.69 / 17.07 / 34.13|
|6400 (5.08-mm reference)|8.89 / 26.67 / 53.33|

Fine-grid rows are replication controls only: this 10.3-mm column does not fit
those pitches. Break-even requires added release, separation/gauging, reject
rework and allocated setup per accepted pair to be less than the saved threading
time. These are scenarios, not measured assembly savings. Do not deduct them
from a prior aggregate installation budget without identifying its threading
allowance. Supports, finer layers, scrap and packing can add machine time;
E-279's separate completed-pair figures (676.31 h integral U or 794.07 h closed
at1024, comparison repetition) are controls, not co-deposition forecasts.

No actuator/RPM, safe support, readback or purchased-cost improvement is earned.
E-276's conditional S40/S50 four-spindle local26.84/31.07s, scene201/223s,
neutral271/332s and dense392/452s remain comparison scenarios against ~30s;
N20/N30 is actual prepared neutral, not free negative travel. Its bought
$798–1768 allocation remains unqualified against ~$500, ~$1000 finished-value
and $1000–1500 demonstrator references. Co-deposition neither resolves nor
worsens those timings by calculation; no machine has been selected.

**Decision:** retain separate integral components as the simpler release control.
Reopen co-deposition only with a materially simpler support/release construction
or actual process evidence showing net whole-pair labor benefit and working
clearances. Do not pursue another tilt, thread-gap or pedestal-detail sweep from
this screen. The next useful independent direction is a shared assembly tool
that threads separately fabricated pairs and gauges them in the same operation:
it can attack this operation without joining the parts during fabrication.
That tool is not constructed or costed here. No new owner print or purchase;
E-281 remains optional.

Verification: standard-library executable; closed-form contact angle independently
checked by bisection, endpoint gaps, 91-angle collar-dominance check and two-layer
boundary-shift checks. Source dimensions inspected in E-277/upright.scad and
E-280/release.scad. Self-review only; no mesh intersection, actual assembly slice,
physical measurement, process yield or manufacturing qualification.
