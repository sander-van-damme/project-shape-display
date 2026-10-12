---
status: complete
builds-on: [E-253, A-007, E-050, E-131, E-156]
---

# Sampled gameplay geometry: sparse walls still visit most rows

**Representation qualification is pending.** The historical schedules below apply
to their declared encodings, not a selected gameplay benchmark. The final section
compares explicit playable alternatives using the later E-255/E-256 rotary models.
Owner guidance at `64ee4f9` makes pitch, neutral, timing and cost reference variables;
the 80×80 schedules below are comparators, not automatic product gates.

Evidence: manual annotations, assumed conversion/play sequences, calculations and
conditional schedules; self-review, no observed play or hardware qualification.
Input `92aa01c`, owner guidance `e5308d0`. Reproduce historical results with
`python3 tools/curated-experiment-checks/E-254/analyze.py`. `sample.json` retains
provenance/hashes/crops/polygons; `heightmaps.json` retains four80×80 arrays with
10-mm digit units. `--write-maps` deliberately refreshes them; stdout is disposable.

## Provenance and conversion limits

Convenience sample selected for distinct visible terrain: ruined enclosures, a river
ford with islands, and a bridged ravine. All are by **Ross McConnell, 2-Minute
Tabletop**, accessed 2026-10-12:

- [Desert Ruins](https://2minutetabletop.com/product/desert-ruins/): standing walls and slabs.
- [Riverside Road](https://2minutetabletop.com/riverside-road/): river/ford/islands/rocks. Flattened-water variant loses bank relief; it is not an independent sample.
- [Mountain Ravine](https://2minutetabletop.com/product/mountain-ravine/): plateau/bridge/ravine/boulders; [published D&D use](https://2minutetabletop.com/mountain-ravine-encounters/), not observed play.

Trace only major terrain; omit small rubble, furniture, foliage and texture. Heights are
assigned representations, not recovered elevations. No functioning projection is assumed. The bridge has a solid underside; slopes are stepped.

Normalized800×555 previews are cropped to ~16×16 game squares at five pins/square,
not squeezed: ruins/ravine `(102,-3,560,560)`, road `(104.25,0,556,556)`. Outside edge
pixels continue traced boundary/base. Thick west ruins perimeter and some eastern
rooms are excluded. Three windows, one author/annotator, no indoor/cave or observed
sessions: not representative. Offline annotation and arbitrary-art conversion are
not implemented in the update timing, which starts from submitted height fields.

## Measured annotations and calculated occupancy

Historical occupancy/level/component outputs remain reproducible in `analyze.py`;
updated comparison below retains the original shapes alongside alternatives.

Four-neighbor components are pin geometry, not room counts. Ruins: 572 wall cells,
15 wall components; traced centerline 56.3 grid squares (1.43 m on the display).
Length within 15° of horizontal/vertical: **25.75/18.03 squares**; other: 12.49.
Thus 77.8% of this hand trace is near-axis, not a population statistic. Curved
walls were traced as chords; classification depends on tracing and angle cutoff.
Raised boundaries total 838/754/496/98 pin edges, including board edges, not wall lengths.

One-pin erosion/dilation gives fractions 3.81–27.05% /61.94–76.89% / 67.75–75.09%
/1.61–4.20%: **annotation sensitivities**, not confidence/FDM bounds. Horizontal crop
shifts ±one square give ruins 12.56–13.31%, road 67.98–71.17%, ravine 71.48%. Flattening
water changes more than these shifts. Even flattened road spans 14 rows/bank; transposing
also fails E-253's three-row envelope.

## Historical transition and service model

`analyze.py` retains all initial setups, six directed map pairs, east reveals
(x≥40) and local reveals(40≤x<60,20≤y<40), plus dense flat→40 stress. These are
hypothetical sequences, not observed play. All unchanged cells may carry miniatures.
Local relief reveals leave1324/789/1308 unchanged cells in serviced rows for
ruins/road/ravine. No whole-board homing or load transfer is credited to screws.

E-253 B3 includes physical neutral-code writing, two color phases, resets, seek,
return, proof and retry. Initial ruins require47,360 decisions despite867 changed
cells; dense needs51,200, plus640 for a retried row. Updated visual comparisons below
still reject its row-writing overhead. This does not reject all shared programming.

Historical serial moving writer:970/3300/7979 s for initial ruins/road/ravine at
.4-mm lead; single-intersection AND oracle:898/3208/7867 s. Source retains all
rates, ramps, docking, proof, retry, support and manufacturing assumptions. These
are scoped schedules, not universal bounds. Multiple selected rows/columns form
a Cartesian product;160 lines do not establish independent parallel selection.

Historical lead/manufacturing calculations remain reproducible; E-255/E-256 now
supersede that preliminary investigation. Existing dense/friction/arrest failures
remain scoped. Bought allocations are not quotes or purchase authority; current
~$500,~30-s and pitch/travel figures are transparent reference comparisons.

## Physical versus visual terrain: representation sensitivity

**Retain physical cliffs as a meaningful case; do not require raised land for every
river.** Proposed starting policy: walls and substantial rock/ground forms physical,
ordinary water and loose rubble visual, deep ravine physical. This is a recommendation
for owner evaluation, not an adopted product requirement. Flattening both depressions
changes the shared-drive head count, so the decision cannot be inferred from occupancy.

Reproduce `python3 tools/curated-experiment-checks/E-254/playable_variants.py`.
Optional `--figure /path/terrain-choices.png` requires matplotlib and generates the
four player-view schematics. Source annotations and historical stored arrays remain
byte-unchanged. New arrays derive from semantic labels, not additional map samples.
Evidence: sourced gameplay context, explicit encoding hypotheses, geometric counts,
conditional schedules and self-review; no user play test or physical qualification.

### Gameplay semantics and limits

The [official D&D rules](https://www.dndbeyond.com/sources/dnd/br-2024/playing-the-game)
distinguish difficult terrain from cover, use five-foot grid squares, and assign
Small/Medium creatures one square. These rules do not require mechanically elevated
water or rubble. Our inference: mark movement costs visually; give physical form to
substantial obstacles and useful elevation, with the DM determining actual cover.
Trees can provide cover, so omitting foliage from pins must not erase a relevant tree
trunk from the game: use a marked footprint or removable prop when needed.

| Map feature | Physical role / alternative | Player and GM consequence |
|---|---|---|
| Ruins: standing walls | Keep 20-mm wall bands | Legible enclosure and cover; simplified top heights do not adjudicate sightlines |
| Ruins: large fallen slabs | Historical 10-mm masses, or flat marked rubble | Retain a slab physically if climbable/solid; loose difficult terrain need not become a barrier |
| Road: ground, islands, ford | 10-mm continuous land, or flat ground/water | Relief shows banks but creates base-straddling edges; visual water keeps placement flat and still needs water/ford rules |
| Road/ravine: major rock masses | Keep 10 mm above local ground | Preserve obstacle function when changing datum; a label “rock” alone does not justify elevation |
| Ravine: plateaux and chasm | 30-mm physical drop, or flat marked hazard | Physical drop communicates separation; visual version needs explicit no-walk/depth marking |
| Ravine: bridge | 30-mm pin-built deck, or flat marked crossing | Pin-built deck fills its underside; cannot represent two simultaneous vertical play layers |
| All: trees, small stones, texture | Visuals or optional removable props | Do not turn vegetation into continuous pin walls; props/visual placement and visibility remain unqualified |

The map author's [river description](https://2minutetabletop.com/riverside-road/)
emphasizes a hazardous water crossing, not a specified bank height. The
[ravine encounters](https://2minutetabletop.com/mountain-ravine-encounters/) use a
bridge over a dangerous drop, with climbing and even activity beneath the bridge.
**New incompatibility with that published use:** the existing solid pin-built bridge
cannot host under-bridge play. A separate bridge prop above lowered channel pins is
an option, but requires real span support, placement time and owner choice; it is not
included in the schedules or a free pass. The rendered 30-mm drop compresses narrative
depth; physical millimetres are not the rules' distance scale.

No thin raised shoreline/ravine rim is introduced: it would create an unsupported
wall-shaped obstruction where the source shows an edge, changing movement/cover.
Colors in the schematics explain semantics; **no functioning projection or overlay
is assumed**. Flat variants require some visible marking solution. Its setup/reveal
time, registration, occlusion, cost and legibility are still unmeasured.

### Counts, placement and conditional timing

The new visual variants retain **10-mm local rock relief**, instead of keeping
absolute 20/40-mm rock tops after lowering their surroundings. The legacy flattened
road, with 20-mm rocks, remains a separate reproducible control.

| Initial physical setup | Raised cells | Rows / columns | Independent B2, 2000 rpm s | Independent B2, 3000 rpm s | Shared mask B3, 3000 rpm s | Four 16-tip heads, 3000 rpm s |
|---|---:|---:|---:|---:|---:|---:|
| Ruins, walls + slabs (historical) | 867 (13.55%) | 74 / 78 | 20.19 | 18.31 | 16.43 | 40.62 |
| Ruins, walls only | 572 (8.94%) | 72 / 70 | 19.74 | 17.89 | 16.02 | 40.62 |
| River, physical banks (historical) | 4449 (69.52%) | 80 / 80 | 18.63 | 17.45 | 15.99 | 65.31 |
| River, visual water / 10-mm rocks | 177 (2.77%) | 24 / 18 | 9.50 | 9.25 | 9.44 | 13.53 |
| Ravine, physical drop (historical) | 4575 (71.48%) | 80 / 80 | 26.93 | 22.98 | 19.80 | 87.36 |
| Ravine, visual drop / 10-mm rocks | 167 (2.61%) | 28 / 28 | 10.23 | 9.96 | 9.06 | 16.98 |
| **Separate dense stress**, flat→40 mm | **6400** | **80 / 80** | **29.43** | **24.65** | **19.75** | **93.70** |

E-255 timing includes seeks, docks, ramps, proof, return, one retry and common4 s;
lead3 mm,1000 rev/s²,20-ms row proof are assumed. Masks pay signed groups/rewrites.
These **physical-subsystem estimates** do not establish manual conversion, props or
new visual workflow within4 s. They are not measured player waits; ~30 s is a reference.

For each suite, three initial setups plus six directed map pairs; head minima below
use the historical <30-s comparator, not a product rejection rule:

| Suite | Fewest independent heads, 2000 rpm / maximum s | Fewest mask heads, 2000 rpm / maximum s | Fewest mask heads, 3000 rpm / maximum s |
|---|---:|---:|---:|
| Historical relief | B2 / 26.93 | B3 / 29.19 | B3 / 26.18 |
| Walls only + visual river + physical ravine | B2 / 26.93 | B3 / 27.96 | B3 / 24.56 |
| Walls only + visual river + visual ravine | B2 / 20.51 | B2 / 24.91 | B2 / 23.10 |

Within the inherited uniform-bank scheduler (not a global optimum), visual depressions
reduce mask channels **240→160**, mask bought allocation
**$1608→$1198**, and increase the complete-channel allowance under $1500 from
**$3.55→$5.8875**. Independent B2 retains its $1128 allocation/$6.325 allowance.
All numbers use E-255's favorable assumed $4/channel and reserves, not supplier quotes;
all exceed the $500 comparator. Premium value is possible, not established.

Four 16-tip heads improve flat-depression setups but still need 40.62 s for initial
ruins. The inherited turning 80-tip oracle needs 31.30 s for walls-only ruins, despite
13.84/15.37 s for visual river/ravine. E-253 B3 remains 97.05/84.54 s for those visual
maps and 178.14 s for walls-only ruins: removing broad ground does not rescue its
row-writing overhead. No parked crank/clamp campaign reopens.

Placement check: among the 164 grid squares centered on road land, **136** have all
25 pin tops coplanar with relief versus **160** when flat. Ravine plateau/deck squares:
**155/173→164/173**. This conservative square-footprint geometry does not measure
round-base stability, friction, pin gaps or miniature loads; real bases vary and may
bridge unequal tops. Schematics show illustrative 25.4-mm bases at identical safe
locations in each alternative. Walking on marked water/chasm is still a rules decision.

The same local four-by-four-square reveal changes 171 river / 292 ravine pins with
relief (B2 at 2000 rpm:9.11/15.89 s), but **zero** with the visual-depression variants
because that patch contains no retained rock masses. Walls-only ruins still change
36 pins /17 rows /12.67 s. Separately, a visual reveal over already deployed geometry
has zero **mechanical** moves for every variant; it does not have proven zero latency
or concealment. A loaded region must never be raised just to uncover its artwork.
All unchanged cells remain potential miniature locations; ideal selective screw
commands do not prove zero disturbance through a common frame.

**Decision:** compare mixed, both-relief and both-visual policies with Sander using
the schematics. Keep them conditional pending feedback and a workable marking/prop
flow; published rules do not establish owner preference or representative play.
Source invariance, semantic counts, signed reversal, no-op and bank-boundary checks
pass; historical E-254/E-255/E-256 checks remain unchanged. No hardware qualification
or corpus expansion is claimed.

### Paid raised-neutral control (owner update at integration)

Source now tests initial **physical** flats at10/20/30 mm against the unchanged
0..40-mm targets. These are reversible screw positions, not free negative travel.
Road from10-mm neutral: **1951 lower,4272 stay,177 rise**;2128 changed/51 rows,
versus4449/80 from minimum. B2/2000 rpm:**13.586 s** versus18.633 s. Cold minimum→
neutral preparation costs**17.133 s**: two paid updates total**30.720 s**, slower
than direct cold setup. Persistent neutral can help, but preparation is not free.

Ravine from30-mm neutral:1825 lower,4408 stay,167 rise;1992 changed/78 rows,
**25.333 s** versus26.933 s from minimum. Fewer pins barely helps because30-mm
row maxima remain. Preparation costs25.333 s; two-update cold total50.667 s.
A common20-mm neutral gives21.233-s ravine service, with plateaux10 mm above it.
Map-dependent flats need preparation and cannot be swapped beneath loaded terrain.

Map-pair deltas are exactly invariant to relabeling both endpoints by the same datum.
These targets fit assumed0..40 range;20-mm neutral cannot offer both30-mm depth and
20-mm wall rise without changing range/representation. Guide engagement, stops,
shaft/column clearance, loaded reverse and retained neutral remain unqualified.
The schematics show final relief, not a required start state. The following same-area64×64 comparison now tests these geometry and schedule
questions without rescaling80×80 timing.

### Same-area quarter-square and fixed-ground screen

**6.35 mm deserves further comparison; fewer cells do not establish playable walls
or a purchasable machine.** The connected-wall alternative below retains the inspected
one-square passage and bridge width, reduces B2 channels160→128 and its favorable
bought allocation$1128→$953.92. Ordinary ground fixed across physical maps requires
**50-mm total travel**, and changes map-pair deltas. This is distinct from the earlier
paid initial flat, which leaves all target heights unchanged.

Reproduce with `python3 tools/curated-experiment-checks/E-254/pitch_neutral.py`;
optional `--figure /path/comparison.svg` produces a zoomable standalone vector sheet.
JSON and figure are disposable outputs. This extends the same canonical annotations
and E-255 scheduler; no new map, CAD, physical trial or owner policy is inferred.
Evidence: independent rerasterization, deterministic geometry/schedules, labelled
uncertainty bounds and self-review. No timing is scaled by cell fraction.

**Geometry construction.** Both grids cover406.4×406.4 mm, exactly16×16 game squares.
Rasterize original semantic polygons directly at cell centers:80×80 at5.08 versus
64×64 at6.35. Keep all seven historical/current variants, local4×4-square reveals,
three physical/visual suites, all six directed map pairs and all six three-map orders.
The historical stored80×80 arrays remain unchanged. Heights retain their declared
roles: ruins walls20/slabs10; river ground10/rocks20; ravine ground/bridge30/rocks40;
visual depressions retain10-mm rocks; walls-only ruins and legacy20-mm flat-water
rocks remain separate controls. Visual policy does not erase water/chasm semantics.

Raw wall-center sampling is insufficient:572→298 wall cells,15→24 four-neighbor
components. A **connected-centerline alternative** keeps the polygon fill and traces
each existing wall polyline into a four-neighbor stair path; diagonal crossings add
an x-first bridge cell. It adds17/45 cells (589/343 wall cells total), producing9/8
components. Separate polylines are never intentionally connected, but adjacent cell
fills can merge: connectivity still differs between pitches. This deterministic
conversion is a hypothesis, not a topology or player-validation pass. Do not count
raw missing walls as useful sparsity. All timing results below use connected walls
unless explicitly labelled raw; these repairs do not change the principal B2 maxima.

| Inspectable feature / geometric check | 5.08 mm | 6.35 mm |
|---|---:|---:|
| Thin vertical wall section, source x530..575,y100 | 5.08 mm | 6.35 mm |
| Southern ruin opening, x420..510,y382, raw | 30.48 mm | 31.75 mm |
| Same opening with connected walls | **25.40 mm** | **25.40 mm** |
| Ravine bridge section x380,y180..300 | 50.80 mm | 50.80 mm |
| River ford section x515..640,y250 | 40.64 mm | 38.10 mm |
| Coplanar25.4-mm squares /234 ground-centered ruins squares, connected | 144 | 163 |
| Coplanar squares /164 land-centered river squares, relief / visual | 136 /160 | 137 /160 |
| Coplanar squares /173 plateau/deck-centered ravine squares, relief / visual | 155 /164 | 155 /164 |

Coordinates refer to retained normalized source polygons. Widths are exact raster
cross-sections at the named locations, **not minimum widths along entire passages**.
The northern probe is also emitted but passes beside the upper thin wall; its41.37-mm
open run must not be called a doorway width. Both pitches have4/5 cells per game
square. Eligibility uses the **same continuous semantic square centers**, avoiding an
even-grid center bias. Coplanarity of the whole square is sufficient geometry only:
no pin-gap, round-base rocking, friction, force, tall-miniature or load-sharing pass.
One-square clearance has no allowance for wider bases or assembly error. The greater
coarse ruins support count partly reflects changed boundaries, not proof of better play.
Solid bridge pins still preclude under-bridge play; separate props/markings remain unpaid
and unqualified options.

A coherent annotation/registration displacement±3.175 mm in X/Y (nine cases, not
printer priors) gives raw wall component counts10–15 at80 and19–24 at64. This changes
whole outlines together, not independent random pixels. The figure overlays original
polygons on raw and connected variants so losses/mergers remain inspectable. A chosen
wall conversion must explicitly protect openings and intended separations.

**Layouts and paid timing.** Same lead3,2000 loaded rpm,1000rev/s²,200mm/s travel,
5000mm/s²,80-ms dock/release,20-ms row proof, one immediate station retry and4-s
common allowance as E-255/E-256. B2 owns40/40 versus32/32 full-width rows; B3 owns
27/27/26 versus22/22/20. Actual pitches enter every seek/return. Independent outputs
can reverse separately; stopped masks serialize signs and pay threshold rewrites.
Four16 heads own40×40 quadrants with16/16/8 strips versus32×32 with16/16 strips;
XY seeks, return and retry are charged. No adjacent/crossing head collision clearance
is proved. Full-row span changes401.32→400.05 mm: quarter pitch barely shrinks its
rotation sweep, despite fewer outputs. Turning schedules still pay parking/yaw.

| Submitted scenario, seconds | 80×80 | 64×64 |
|---|---:|---:|
| Connected ruins from minimum, independent B2 / four16 / turning full row | 20.19 /43.87 /35.59 | 17.21 /30.73 /30.05 |
| Physical river from minimum, independent B2 / four16 | 18.63 /67.56 | 16.18 /39.03 |
| Physical ravine from minimum, independent B2 / four16 | 26.93 /98.31 | 22.98 /54.79 |
| Separate dense0→40, independent B2 | 29.43 | 24.88 |
| Extra-stroke dense0→50, independent B2 | 33.53 | 28.18 |
| Separate dense±40, stopped-mask B2 | 50.89 | 42.15 |

These are **conditional complete physical-subsystem budgets**, not measured player
waits. The4 s does not establish art preparation, miniature relocation, prop placement,
visual reveal/registration or sensing under occlusion. Add their real times and costs
when implemented; power-on homing is also unmeasured. No-op mechanical reveal costs0
in the model, not0 player wait. Retention, selective docking and reliable proof remain
unqualified. Unchanged pins keep resident screw support ideally; frame motion and
accidental coupling can still disturb them. Extra proof time/running drag must rerun
the model, rather than consume unreported margin.

**Fixed initial flats, unchanged0..40 targets:**

| Physical preparation and first-map service, B2 seconds | 80×80 | 64×64 |
|---|---:|---:|
| Minimum→neutral10 | 17.13 | 14.98 |
| Neutral10→river; lower /stay /rise cells | 13.59;1951 /4272 /177 | 11.96;1256 /2730 /110 |
| Same river changed rows | 51 | 40 |
| Cold two-update total, compared with direct cold river | 30.72 vs18.63 | 26.94 vs16.18 |
| Minimum→neutral20; neutral20→ravine | 21.23;21.23 | 18.28;18.28 |
| Minimum→neutral30; neutral30→ravine | 25.33;25.33 | 21.58;21.58 |
| Neutral30→ravine; lower /stay /rise cells | 1825 /4408 /167 | 1166 /2823 /107 |

The ravine still visits78/63 rows from neutral30. Persistent prepared surfaces can
shorten a reveal; they do not remove first preparation or subsequent signed moves.
The source reports10/20/30 initial flats for every policy, including unfavorable ones.

**A fixed ordinary-ground plane is a different physical workload.** Set ordinary
ground to30 across maps: ruins wall50/slab40, river water20/ground30/rock40, ravine
bottom0/plateau30/rock40. Mixed policy flattens river at30; fully visual depressions
need only30..50 once prepared. Keeping30-mm ravine depth and20-mm wall rise therefore
needs50 usable stroke (neutral30,−30/+20). Neutral20 within a40-mm range cannot do
both. Changing coordinate names on two unchanged endpoints cannot alter deltas;
changing each map's **physical** placement to align ordinary ground can.

| Nine-transition suite maximum, seconds | Independent B2,80 /64 | Mask B2,80 /64 | Mask B3,80 /64 |
|---|---:|---:|---:|
| Original absolute targets, both depressions physical | 26.93 /22.98 | 39.21 /32.61 | 29.19 /23.71 |
| Original targets, visual river /physical ravine | 26.93 /22.98 | 37.92 /31.40 | 27.96 /22.63 |
| Original targets, both depressions visual | 20.51 /17.70 | 24.91 /21.66 | 20.05 /17.31 |
| Ground aligned at30, physical or mixed | **30.13 /25.38** | as corresponding row above | as corresponding row above |
| Ground aligned at30, both visual | 20.51 /17.70 | 24.91 /21.66 | 20.05 /17.31 |

The aligned80 B2 case misses the30-s reference by0.13 s; that alone is no reason to
buy a third head. Its64 counterpart retains128 channels in this model. Cold preparation
is reported separately from these three neutral→map plus six map→map maxima.
Aligned ruins→ravine has lower/stay/rise2461/3862/77 cells at80 versus1568/2470/58
at64, yet visits all80/64 rows. Its50-mm wall→chasm deltas set the30.13/25.38-s maximum.
The script emits signed counts, unchanged cells in serviced rows, turns and schedules
for every directed pair. Reverse independent timing is symmetric under the assumed
rates; actual signed force/torque need not be.

For the explicit **ruins→river→ravine** sequence, absolute targets from minimum take
64.56/55.38 s total. Preparing neutral30 first takes95.03/81.33 s including prep;
returning to that flat between each map costs149.20/127.30 s. With ordinary ground
aligned physically at30, direct cold first map plus transitions costs80.20/68.12 s;
paid neutral preparation plus those maps costs92.79/79.33 s; inter-map flattening
costs118.22/101.50 s. All six orders are emitted. This constructed sequence is not
observed session behavior. Resetting a loaded scene is not an acceptable local reveal.

**Replication and cost, actual proposed counts:**

| Duty / component | 80×80 | 64×64 |
|---|---:|---:|
| Each of pins, resident screws, thread pairs, thrust seats, screw sockets, antirotation duties | 6400 | 4096 |
| Moving resident parts (pin+screw); two spaced guide duties | 12800;12800 | 8192;8192 |
| Independent B2 motors/drive-feedback/docking duties | 160 | 128 |
| Mask B3 outputs/mask states/writers/couplings | 240 each | 192 each |
| Row-column AND hypothesis: address lines /serial interruption contacts | 160 /12800 | 128 /8192 |
| Two placements/site at5 /10 /20 seconds each, maker hours | 17.8 /35.6 /71.1 | 11.4 /22.8 /45.5 |

There are two/three full heads, or four16-output heads/64 output duties at either pitch.
Masks add one shaft/motor/brake set per head. AND still needs4096/6400 output paths;
logical lines do not implement clutches. Springs, inserts, selective docking, bearings,
end-stop features, hidden service access and wiring are unresolved counts, **not zero**.
At least one nut interface, seat interface and guide duty per site remains tolerance/
wear-sensitive; molding a module does not delete those functional sites.

Reuse the explicit E-255 allocation: common$250, resident$.02/site, $55 per independent
head, extra$35 per mask head, $4 per complete channel. This is a conditional whole-machine
**bought allocation**, not a quote or all-in delivered price:

| Layout | 80 allocation | 64 allocation | 64 complete-channel allowance under$500 /$1000 /$1500 |
|---|---:|---:|---:|
| Independent B2 | $1128 | **$953.92** | $.454 /$4.36 /$8.266 |
| Mask B2 | $1198 | $1023.92 | negative /$3.813 /$7.719 |
| Mask B3 | $1608 | $1369.92 | negative /$2.073 /$4.678 |

64 independent B2 at$2–8/channel instead gives$697.92–1465.92; no probability is
assigned. Four16 needs four XY transports: extending the same allocations with an
extra$35 XY axis/head gives$994/$947.92 at80/64, before routing extras; its relief
waits remain slower. Turning full-row allocation is at least the one-head duties
($753/$642.92) **plus uncosted yaw/parking hardware**; do not call it cheaper complete
hardware. These are neither sourced floors nor purchase authority.50-mm stroke adds
unknown longer-stock/guide/frame costs; optical/prop workflows, tooling, outsourced
parts, printed material/time, scrap, assembly/calibration labor and repair are extra.
A ~$1000 enjoyable product or$1000–1500 demonstrator remains possible, not established.

**Travel, manufacture and retention:** fixed10/20/30 initial planes within0..40 do
not inherently demand longer parts than the same40-mm machine. The aligned50-mm
case does: full10-mm nut overlap requires screw threaded length≥60 mm **before**
runout/end-stop margins, versus≥50 for40-mm stroke. For two fixed guide stations
separated by g, a translating guide surface needs length≥stroke+g+end margins;
a50.8-mm historical tube leaves at most10.8/0.8 mm for g at40/50 stroke, before
margins. The old55.8-mm grid height is not proof of engagement through that travel.
Underside thrust retention, cap/screw clearance, torque reaction, end stops and safe
loaded reverse remain real obligations. E-255's dependency mismatch and positive
unquantified owner holding observation both remain intact.

Coarser pitch does not automatically relax the thread fit. Keeping the4.4-mm stem
and screw can preserve the core interface, but needs wider supported caps for a
near-continuous6.35-mm surface. Bare4.4-mm square tops cover75.0% versus48.0% of each
cell area at the two pitches. Widening the whole tube instead changes guide/friction,
cap mass and dynamics; requalification is needed. Shared guide/frame bias and batch
thread variation correlate many sites. Do not multiply invented cell-yield priors.

Repeated core production falls36% only if core geometry/process stay comparable;
cap material need not. No new sliced volume or print-time claim is made. Compare
batch FDM with unscrewing-core/split molds, machined/rolled screw stock and accessible
machined shared sockets; mold release, shrinkage, burrs, run-in, tray fixtures and
module rejection must be costed. Two10-s placements already consume22.8 h at64 before
inspection/calibration; per-cell hand fitting still risks exceeding the owner's
few-day assembly preference. Modular guides/replaceable seats and batch tests are
necessary investigation topics, not an implemented manufacture/repair route.

**Next technical decision:** settle a constrained wall-conversion rule that preserves
intended connectivity, one-square openings and base placement at6.35 mm, then decide
whether the **common-ground50-mm** case earns its extra travel over the0..40 reference.
Keep all three physical/visual policies conditional while owner feedback is pending.
This screen supports carrying64×64 forward as a comparator; it selects neither
architecture nor actuator. The next physical discriminator remains E-256's proposed
hold/drive/travel characterization of the existing pair, with stroke informed by the
representation choice. No detailed head CAD, print or purchase follows automatically.

Verification: legacy E-254/analyze, playable_variants, E-255 and E-256 stdout byte-identical;
new independent dense timing arithmetic, no-op, signed reversal, actual bank partitions,
common-datum invariance, exact one-square passage control and connected-wall geometry
checks. SVG is generated from the same labels/probes as the JSON. Self-review only;
no independent physical validation or representative-play claim.
