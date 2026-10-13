---
status: complete
builds-on: [E-255, E-256, E-258, E-260]
---

# Resident-screw travel and shared-guide support envelope

**Keep resident screw support, but do not reuse the short historical pin as a
40/50-mm-travel guided assembly.** Two shared guide planes can react side loads
without adding moving parts per cell. Sustained guide overlap, lateral play and
screw restraint must be budgeted together; an unspecified enclosure is no cure.

Evidence: **axial interval geometry, small-angle rigid-guide calculations and
ideal elastic-column sensitivity**, self-reviewed. No new CAD, measurements,
process qualification, print request or purchase. Reproduce with
`python3 tools/curated-experiment-checks/E-261/support_envelope.py`; `--check`
tests independent interval, statics, linear-program and elastic-column anchors.
All new dimensions/material/load inputs below are explicit scenarios, not
X1C/PLA priors or selected production dimensions.

## Support and travel closure

Reinspected trial3 actuator and trial5 actuator/frame/both calibration sources
at41484f96999847c139b9010e73009d73e9459c89. E-255's dependency mismatch remains:
trial5 is not a proven mating pair or Sander's identified successful variant.
Its pin is50.8 mm, screw50 mm, nut10 mm; the external thread's nominal radial
depth.9 mm implies root diameter3.2−2×.9=**1.4 mm**, not a solid3.2-mm shaft.
The recovered screw was roughly40 mm; internal engagement remains unmeasured.
The reported near-extension break in E-256 is real; its cause is still unresolved.

Proposed support graph: pin→engaged thread→resident screw→shared thrust bed→frame.
Two square guide planes react pin torque and transverse loads; a resident radial
seat locates the screw. The travelling writer adds torque only. Retention after
withdrawal still requires the observed holding behavior to transfer to the built
assembly. Neither a guide nor a thrust collar is an added axial pin brake.

Let usable screw thread occupy z=[0,L], nut occupy[q,q+n], q=m+u, and commanded
displacement u=[0,S]. Full overlap needs `L≥S+n+m+end_margin`. Illustrative n10
and2-mm margins at each end give26/36-mm usable travel from40/50-mm threaded
length, respectively. These are **not** measurements of either printed specimen.
Full40/50-mm stroke instead needs54/64-mm usable thread, plus seat/drive stock.
Ten millimetres of engagement is inherited CAD, not a proven adequate minimum.

Let the pin have projected axial length P, two2-mm-thick guide slabs have center
spacing b, and reserve2 mm at each pin end outside the bearing section. For both
slabs to stay fully inside that section throughout travel:
`P≥S+b+2+2+2`. The common bearing interval is[S+m+2,m+P−2]. The optimal axial
placement below minimizes stock; it is a geometry construction, not toleranced CAD.

| Stroke S / guide center span b, mm | Pin P, mm | Usable thread L, mm | Minimum / maximum pin top above thread origin, mm |
|---|---:|---:|---:|
|40 /20|66|54|68 /108|
|40 /40|86|54|88 /128|
|40 /60|106|54|108 /148|
|50 /20|76|64|78 /128|
|50 /40|96|64|98 /148|
|50 /60|116|64|118 /168|

For50.8-mm stock and40-mm travel, b≤**4.8 mm** under these allowances;50-mm
travel cannot preserve them at all. A continuous sleeve can move its effective
contact region, but its high-extension overlap is still limited by pin length
minus travel when the sleeve must stay below the lowest terrain surface. The
historical55.8-mm-tall grid has no specified assembled placement; do not count
its full height as simultaneous bearing separation or let it protrude into play.

At b40, moving fromS40/neutral20 toS50/neutral30 raises the neutral top from108
to128 mm above the thread origin. This excludes the seat, writer and enclosure:
**20 mm added stack**, not merely10, for this topology. Transport height is a
tradeoff, not rejection. The cavity also needs screw-tip clearance at retraction;
these constructions leave12/32/52 mm at b20/40/60 with a2-mm cap reserved, but it must
be checked again if stock, cap or end margins change.

## Guides alone do not eliminate lateral contact

Use trial5's nominal4.64-mm aperture minus4.4-mm pin width as a **.24-mm total
clearance scenario**, not actual print capability. At maximum extension the top
is S+2 above the upper slab face. A rigid centerline can lean across the two outer
faces separated by b+2. Its worst top displacement is
`U=C/2+C*(S+2)/(b+2)`. Opposing neighboring play leaves `gap=p−w−2U−d`, where
d is differential axis error. Common bed translation cancels for equal-height
neighbors; opposite play, local distortion and module seams do not.

| S / b, mm | U, mm | Gap at p5.08 /w4.4 | Gap at p6.35 /w4.4 | Gap at p6.35 /w5.6 |
|---|---:|---:|---:|---:|
|40 /20|.578|−.476|.794|−.406|
|40 /40|.360|−.040|1.230|.030|
|40 /60|.283|.115|1.385|.185|
|50 /20|.687|−.695|.575|−.625|
|50 /40|.417|−.154|1.116|−.084|
|50 /60|.321|.037|1.307|.107|

All gaps are mm with d=0 and no elastic bending. A.2-mm differential error
subtracts.2 from each. The.030/.037-mm results are fragile, **not acceptable
manufacturing margins established by this screen**. Coarser pitch helps while
the pin remains narrow, but a4.4-mm top at6.35 pitch leaves1.95-mm surface seams;
miniature support/appearance remain to assess. A5.6-mm top largely spends that
space. Wider caps cannot borrow the narrow-shaft clearance result.

This is a small-angle straight-strip relaxation. Slab-face constraint extrema
are independently enumerated; the neglected rotated-section width correction
is<.00034 mm in this table. Real pin bending, yaw, cap-edge geometry and contact
are absent. Negative gap means **guides alone permit a conflicting envelope**,
not proven contact in the assembled mechanism: a radially stiff screw/nut could
limit tilt, but then carries the missing side reaction. Positive gap only passes
this model. No tighter fit or extra per-cell bearing is selected to rescue it.

A separate force balance illustrates the duty. With assumed H=.1 N at the top,
S50/b20 yields guide reactions+.265/−.365 N; b40 reduces them to+.1325/−.2325 N.
At illustrative sliding μ=.3, their absolute sums imply.189/.1095 N guide drag,
before misalignment/preload and torque reactions. This is comparable to.196 N
weight for the **20-g total moving-load scenario**, not evidence of typical play.
An enclosure can relieve screw bending while increasing drive force. Its side
contacts and motor torque must be tested together; no free speed pass follows.

## Screw stability is a separate requirement

[Nook's miniature screw engineering catalog](https://www.nookindustries.com/media/2427/pmbs-miniatures-catalog.pdf),
PDFp8, checked2026-10-13, gives Euler column strength using root-section inertia
and end restraint. It distinguishes axial restraint from a moment-fixed bearing
and treats screw speed separately. Its steel values and product ratings do not
transfer to printed PLA. Here use `Pcr=π²EI/(Kℓ)²`, `I=πd_root⁴/64`, with
E=1000/3000 N/mm² as deliberately competing stiffness scenarios, not measured
material properties; K1 pinned/pinned and K2 clamped/free are ideal controls.

AtS50, the compressed segment is52–62 mm depending on where the nut transfers
load, taking the bearing at the thread origin. Mid-nut ℓ57 gives:

| Root diameter, mm | E1000, K1 /K2 critical load N | E3000, K1 /K2 critical load N |
|---|---:|---:|
|1.4 historical nominal|.573 /.143|1.719 /.430|
|2.0 comparison|2.386 /.596|7.157 /1.789|
|2.5 comparison|5.825 /1.456|17.474 /4.369|

These are ideal instability values **without safety, defect or creep allowance**,
not permissible loads. For core1.4/E1000/K1, uncertain thread load station alone
changes.484–.688 N. S40/mid-nut instead gives.843 N. At20-g static load.196 N,
the adverse K2/S50/core1.4 scenario is already below load. Neither a threaded
flank nor the loose historical collar has demonstrated either end condition:
K2 is not a guaranteed conservative bound on a poorly located assembly.

Using OD3.2 as a solid section instead of root1.4 would multiply this estimate
by**27.30**. Actual helical ribs can add stiffness, but a constant isotropic
root-cylinder model omits that, anisotropy, imperfect alignment, bending stress,
thread stripping, fatigue, bearing compliance and residual curvature. Changing
root diameter changes the thread and holding behavior; it is not a free CAD fix.
The unknown broken specimen cannot be diagnosed or rated from this table, nor
does the reported ~9.81-N scale reaction establish an operating load. Powered
rotation also owes critical-speed/whirl and moving-loss checks; buckling is not
the last mechanical criterion.

## Machine consequence and next discriminator

The resident ledger remains4096/6400 each pins, screws, thread pairs, thrust
seats, radial locating duties and underside drive interfaces, plus8192/12800
guide apertures in two shared layers. These are functional sites, not that many
purchased bearings. Guides can be openable molded, machined or printed modules;
frame bow, plate registration and service access remain unqualified. No private
cartridge, latch, additional axis or individual alignment operation is granted.
E-260's two-part placements, batch handling and local replacement obligations
remain. Independently driven B2 still installs128/160 channels.

Ten more millimetres in every4.4/.44-wall pin adds.285/.446 L of ideal tube stock
at4096/6400 sites. The extra screw length lies between core and OD cylinder
volumes.063–.329 /.099–.515 L; actual thread and end geometry needs slicing.
Thus even the added material is nonzero; print time, scrap and outsourced price
are unquoted. Adding guide separation also lengthens every pin. Do not promise
the existing resident allowance buys the longer seat/guide/thread construction.

Preserve E-259's comparisons rather than claim a new faster machine: at64 pitch
6.35/B2/K32, assumed lead3/2000rpm/1000rev/s² gives25.38-s deepest-sample maximum,
32.58-s paid neutral preparation and45.78-s dense50 stress; lead2 instead makes
the deep maximum32.23 s. These remain conditional against the~30-s reference,
not qualified play. The dated motor/driver subset plus unquoted reserve is
$984.64/$1166.40 at64/80, already above$500; $1000/$1500 comparisons still owe
feedback, docking, physical support, power and these stock corrections. No price
floor, complete BOM, finished retail price or purchase authorization is inferred.

**Decision:** carry the longer-stock/shared-guide construction as a comparator;
stop short-stock reuse and do not optimize microscopic guide fits. It makes
physical support explicit without adding thousands of moving parts, but has not
earned detailed head design or a print. Before choosing a supported test article,
the next independent discriminator is whether a practicable screw/seat stiffness
and alignment envelope can support the required rotary speed across its moving
nut positions, including the unloaded screw overhang. Then a small intact article
can measure axial hold, side-load/drive interaction, reversal and limited travel.
Mechanical overtravel prevention, actual nut engagement and end margins must be
defined in that article; software limits alone do not establish physical stops.
No new owner question or test of the damaged pair is needed for this result.

Checks:1212 all-position axial states;12 independently enumerated four-face
guide-play optima; limiting zero-clearance and differential-error cases; force
and moment equilibrium; SI-unit reconstruction, fourth-power/inverse-square
Euler scaling and inverse roots; stock-shortening failure witnesses. These
verify the calculations, not manufactured support or simulated contact.
