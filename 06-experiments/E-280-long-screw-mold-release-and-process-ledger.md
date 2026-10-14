---
status: complete
builds-on: [E-279, E-277, E-276]
---

# Long-screw mold release and process ledger

## Decision and scope

**Reject exact rigid longitudinal splitting; park screw-only mold detail.**
Reusable tooling was screened before local mold CAD. E-279's 64-mm, lead-3,
3.2-mm-major/1.4-mm-core screw is the control, with 30° and 90° included
profiles. Finished ends below are **new CAD assumptions**, not recovered owner
hardware: lower journal Ø2.8×4 mm at z=-4..0, Ø4.4×2 collar at -6..-4,
Ø4.4×4 driver at -10..-6, blind 2-mm-across-flats hex socket 2 mm deep from
z=-10, and upper journal Ø1.4×4 at 64..68. Overall length 78 mm. No bearing, torque, capture or frame qualification follows.

Load path: column→nut→screw→collar→stationary keeper/frame; journals constrain
rotation. Population holding, moving power-loss arrest and writer release remain
unqualified.

## Finite release reconstruction

`tools/curated-experiment-checks/E-280/release.py` and `release.scad` construct
actual finite solids, subtract exact cavities, and calculate solid intersections.
Use the E-277 pinned BOSL2 revision, OpenSCAD, numpy, trimesh and manifold3d:

```sh
python tools/curated-experiment-checks/E-280/release.py \
  --bosl2 /path/to/BOSL2 --output /path/to/scratch
```

Generated meshes and JSON are scratch. No mold or STL is a fabrication handoff.
Two angular resolutions check whether a collision persists with refinement;
zero sampled intersection is not continuous-path, friction or elastic release
proof. Socket core retracts axially before side opening. A smooth stepped-shaft
control isolates thread undercuts from journals/collar. A separate threaded
sleeve tests downward synchronized rotation/translation after lower tooling and
socket core removal; upward withdrawal brings the collar into the threaded bore.

At 0.1-mm lateral opening, interference persists under mesh refinement:

|Profile|64 facets, +/− half overlap mm³|128 facets, +/− half overlap mm³|
|---|---:|---:|
|30°|.898574 / .878519|.895044 / .874989|
|90°|.298100 / .291868|.297901 / .291656|

Both halves collide already at .02 mm. At 4.4 mm they are clear, but that final
position does not make the intervening path feasible. Smooth stepped controls
stay below 1e-5 mm³ across the same sampled pulls. Axial socket-pin withdrawal
clears; lateral .1-mm motion instead intersects .400 mm³. Finished 128-facet CAD volumes
are 417.622/405.703 mm³ for 30°/90°; these are solids, not deposited resin volumes.

Downward sleeve extraction samples 72/136 steps at 64/128 facets, 416 total.
Maximum residual overlap is .003605→.003497 mm³ (30°) and
.004497→.003248 mm³ (90°); fully withdrawn at 68 mm gives zero. **No exact sleeve
clearance pass:** the residual persists with refinement and its origin is not
resolved. Do not reclassify it as harmless mesh noise or permitted compliance.
Wrong-sign rotation at .375-mm
retreat intersects 101.66–103.39 mm³ at 128 facets; upward 5-mm travel brings the
collar into the sleeve with 31.30–32.44 mm³ overlap.

Verification: eight manifold meshes; two resolutions; smooth/no-motion controls;
axial-versus-lateral socket pull and wrong-rotation/direction controls; scenario
capacity and cure accounting checks. Self-review, not independent validation.
OpenSCAD 2023.09.11; BOSL2 `136e6367e65d52196a3ea51d03156f8b622c60fc`;
numpy 2.5.4, trimesh 5.1.1, manifold3d 3.5.4. No force, wear, thermal, casting or
physical-print qualification.

## Process alternatives and finished-end duties

|Route|Release and end-production path|Unpaid obligations / consequence|
|---|---|---|
|Exact two rigid longitudinal halves|Axial hex pin first, halves move laterally; journals/collar divided on axis|Helical undercut is tested directly; milling accessibility and flash add further constraints. |
|Rigid sleeve plus removable lower tooling|Remove socket pin and lower journal/collar/driver blocks; unscrew downward through open sleeve|68 mm total retreat, 22.67 turns at lead 3. Sleeve fabrication and finish remain unpaid. Adhesion, shrink-on-tool, torque and slender-part damage unknown.|
|Flexible longitudinal silicone mold with rigid backing|Withdraw socket pin, open backing, peel rubber locally away from thread and collar; release part supported along length|Plausible avoidance of rigid interference, not proof of acceptable strain, force, life, straightness or finish. Individual peel, gate/seam cleanup and gauging remain. Do not compare 300% tensile break strain with local release fatigue.|
|Outsourced injection molding / machining|Vendor-defined side actions, unscrewing tooling or thread/end machining with supported stock|Potential automated whole batches and journals/socket finishing, but no qualified small-thread vendor, quote, cycle or tolerance. |

A closed flexible sleeve stripped axially must stretch over crests and the
collar; a split peel mold avoids imposing that entire simultaneous deformation.
Sacrificial tooling escapes rigid release but consumes a tool per casting; it
is not reusable molding. Modifying/removing thread near the split can change
release, contact area and torque ripple; this screen does not grant a modified
thread a load or mating pass. Stop before another local profile optimization.

[Sourced Protolabs guidance](https://www.protolabs.com/resources/design-tips/molded-threads-and-how-to-design-them/)
places external-thread parting along the axis and discusses undercuts, altered
thread forms or side actions, plus flash and extra tooling cost. Its 7.6-mm
minimum applies to its **internal** thread service, not proof of a 3.2-mm
external-screw process. 

[Smooth-Cast 300 manufacturer data](https://www.smooth-on.com/products/smooth-cast-300/)
reports 3-minute pot life, nominal 10-minute cure, density 1.05 g/cm³ and linear
shrinkage .01 in/in. It explicitly says low-mass/thin castings cure more slowly
and recommends pressure casting for best results. These are process cautions,
not 10-minute production or bubble-free thread evidence. Maximum-property
post-cure is 4–6 h at 65°C after initial cure; equipment, cooling and batch
capacity must be paid. Resin is a process example, not a selected bearing polymer.

[Mold Max 30 manufacturer data](https://www.smooth-on.com/products/mold-max-30/)
reports 24-hour room-temperature cure, .002 in/in shrinkage and 1.18 g/cm³;
recommends vacuum degassing and at least 13-mm rubber above the model.
Actual mold life depends on use; no guaranteed casting count is supplied.
Nominal combined uniform scale factor .998×.99 gives 1.198% shrinkage: a
64-mm shank loses .767 mm and lead 3 loses .03594 mm if uncompensated.
This is a calculation, **not a tolerance distribution or validated compensation**.


## Whole-pair ledger and uncertainty

Illustrative flexible casting: usable fraction 1, 16 cavities, 30-minute cure,
100-shot tool life. These favorable assumptions still include batch and individual
release time. Values exclude mold fabrication and final physical qualification.

|Cells|Unchanged channel+nut print h / L|Finished screw net L|Mold occupancy h|Print + mold serial h|Maker h, including inherited base|
|---:|---:|---:|---:|---:|---:|
|1024|533.62 / 4.284|0.415|39.82–54.40|573.44–588.02|40.90–104.67|
|4096|2134.47 / 17.135|1.662|159.29–217.60|2293.76–2352.07|151.44–382.53|
|6400|3335.11 / 26.773|2.597|248.89–340.00|3584.00–3675.11|234.32–590.90|

Resin including waste is .623/2.493/3.895 L, plus rubber tooling
.563/1.688/2.250 L at this assumed life. Incremental screw-process allocations
are $146–605/$258–869/$329–1040, **before** unpaid work/equipment below.
The source evaluates 18 cure/life/yield combinations per cell count (54 total);
no favorable point is a validated production estimate.

The channel/nut values reproduce E-279 actual three-copy slicer totals:
4057+1571 seconds and 9.41+3.14 cm³ per three. Bare upright shank adds
640–650 seconds/.76 cm³ per three; finished ends were not sliced in E-279.
The bare screw contributes **10.21%** of the lower bare-pair print-time
control. This is **not an upper bound for a finished printed pair**: journals,
collar/socket and their supports add unknown deposition/finishing time. No
usable PrusaSlicer was available in this execution; a finished-end slice is not
claimed. Cast-vs-finished-FDM speed superiority therefore remains unresolved. Casting does not eliminate channel printing
or the nut/channel join. No end-volume-to-time conversion is used as a slicer
forecast. Casting occupancy and printing can overlap on independent equipment;
serial sums are resource accounting, not calendar delivery promises.

A 16-cavity flexible-tool scenario grants 10-mm cavity spacing, 13-mm peripheral
cover and backing outside a 180×104×30.4-mm rubber block; cavity volume is
subtracted. This is a material allocation, not gate/vent/backing/tool CAD.
Life 25/100/250 shots, usable fraction .8/1, and cure occupancy 10/30/60 minutes are
**explicit bounds, not priors**. Ten minutes is an optimistic borrowed headline,
not qualified for this thin screw. No automated gang ejection, mixing or
finishing is assumed. At nominal yield, 1024/4096/6400 cells need 64/256/400 shots;
life 25 means 3/11/16 mold sets, life 100 means 1/3/4, life 250 means 1/2/2.
Mold occupancy also includes 2–5 min batch handling and 16 individual
10–30 s socket-core withdraw/reset operations plus 16 releases per shot; the headline cure time is not the complete cycle.
Finishing/gauging occurs outside the mold but consumes maker time. Tool
fabrication/cure is additional; parallel tools require more molds/fixtures.

For all alternatives retain N channels, N nuts, N screws, N column joins, 2N
stationary guide apertures, two screw journal surfaces per cell, one collar load
seat and one socket. Five screw checks per cell mean thread, two journals, collar/end location
and socket. A 16-cavity tool needs 16 socket cores plus two cavity halves
and backing; pins are reusable, but each casting still owes core withdrawal/reset. Two longitudinal seam lines traverse each molded screw; they intersect
functional thread/journal surfaces. Gauges must check both dimensional and loaded
functional behavior; a cosmetic inspection cannot establish holding yield.

Labor scenarios retain channel/nut handling: three 10–30 s operations/cell plus
5 min per assumed 24-channel/289-nut plate. Add E-276's scaled installation base
10.94–23.69 h/1024. Casting adds 2–5 min mix/pour/open/reset per 16-cavity shot,
four 10–30 s individual operations (socket-core withdraw/reset; peel/eject;
gate/seam finish; gauge), and
4–12 h initial setup. This is deliberately not a measured rate; mold replacement,
post-cure handling, failed-gauge diagnosis, PPE/cleanup, tooling manufacture and
commissioning remain additional. Manual unscrewing alone at assumed 60 rpm is
22.67 s/screw (6.45/25.79/40.30 h), before grip, reset and inspection. A synchronized
16-output unscrewer could divide machine occupancy but adds an unbuilt shared
fixture; it does not erase N releases, torque failures or checks.

Casting material includes assumed 50% runner/mixing waste, resin $30–80/kg,
rubber $40–80/kg and fixtures $100–500. These are allocation sensitivities,
not current prices or quotes. They are incremental screw-process spending;
channel/nut material, machine wear, maker labor and complete electronics/frame/
heads remain outside them. No finished product ~$500 or ~$1000 price pass follows.
The $1000–1500 demonstrator reference does not authorize purchases.

Tool cavity/master bias, mix/cure conditions and tool wear are shared errors.
A bad 16-cavity shot creates up to 16 correlated rejects; one biased master can
spoil every mold made from it. Sensitivities use yield/life bounds without
invented failure probabilities. Differential lead strain .2/.5/1/2% accumulates
.02/.05/.10/.20 mm over a 10-mm nut engagement. Shared shrinkage might preserve
pair lead only if both parts use the same calibrated process; this hybrid keeps
an FDM nut. Uniform master compensation does not remove warp, batch variation,
flash or local journal eccentricity. A sourced bulk modulus/strength does not
qualify thread wear, creep, thrust friction or loaded speed.

Individual service access remains required: replace the screw/pair, preserve
unaffected support and re-home/verify that cell. No potting or sealed bank is
credited. A hypothetical 1% replacement event means 11/41/64 pairs and
22–55/82–205/128–320 minutes at an assumed 2–5 min/pair; this is a consequence
scenario, not a predicted failure rate. A shared lot defect can require much
more. Tool replacement needs requalification of journal/lead/straightness.

## Product implication and stopping rule

This is a manufacturing comparison for E-277's 12.7-mm/1024-cell control with
S40/S50 and paid N20/N30. Replication to 4096/6400 is a burden comparison, **not
compatibility of its 10.3-mm columns with 6.35/5.08-mm pitch**. Original references
remain ~40 mm travel, ~30 s gameplay waits and ~$500 bought parts. E-276's
four-spindle S40/S50 local 26.84/31.07 s, scenes~201/223 s, initial neutral 271/332 s
and dense 392/452 s remain conditional assumed 850-rpm schedules. Casting supplies
no new motor, docking, retention, isolation or readback evidence and cannot
improve those waits by itself. No resolution or neutral choice is selected.

**Decision: reject exact rigid two-half straight opening for the tested screw;
park screw-only molding before mold-detail work.** Downward unscrewing and
supported flexible peeling remain process hypotheses, not qualified routes.
Even the favorable scenario retains 534 print-hours/1024 pairs and 41–105 maker
hours before exclusions, above the illustrative 2–4-day maker preference. Reopen
with whole-pair process advantage or measured low-touch finished-screw production
including column joining, release, checks and service. No gates/vents, local mold
refinement, purchases or owner prints follow. This does not reject all casting;
short actual-process fit qualification is a more informative next discriminator.
