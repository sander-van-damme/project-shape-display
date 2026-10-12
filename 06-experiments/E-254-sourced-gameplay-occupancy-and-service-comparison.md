---
status: complete
builds-on: [E-253, A-007, E-050, E-131, E-156]
---

# Sampled gameplay geometry: sparse walls still visit most rows

**Representation qualification is pending.** The historical schedules below apply
to their declared encodings, not a selected gameplay benchmark. The final section
compares explicit playable alternatives using the later E-255/E-256 rotary models.

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

| Conversion | Raised / 6,400 | Height counts, mm:cells | Rows / columns | Rows in 27/27/26-row banks | Raised components / largest |
|---|---:|---|---:|---|---:|
| Ruins | 867 / 13.55% | 0:5533, 10:295, 20:572 | 74 / 78 | 23 / 27 / 24 | 19 / 150 |
| Road relief | 4449 / 69.52% | 0:1951, 10:4272, 20:177 | 80 / 80 | 27 / 27 / 26 | 3 / 4037 |
| Ravine | 4575 / 71.48% | 0:1825, 30:4408, 40:167 | 80 / 80 | 27 / 27 / 26 | 1 / 4575 |
| Road, flattened water | 177 / 2.77% | 0:6223, 20:177 | 24 / 18 | 9 / 1 / 14 | 3 / 143 |

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

Historical screw model:80 reversible selectively docked spindles/head; resident
thrust-supported screws and antirotating columns. Rates200 mm/s,5000 mm/s²,3000 rpm;
assumed1000 rev/s² ramps,.08-s docking/release,.02-s read,≥.05-s index. Row service
=.10+spin(max|delta|/lead). Map=4+maximum bank seek/service/return+largest row service
(one retry). E-255 expands masks/signs with the same assumptions. No physical proof.
At.4-mm lead, initial maps require35,975/115,650/347,300 revolutions. Serial moving
writer:970/3300/7979 s; single-intersection AND oracle:898/3208/7867 s (free routing,
.05-s selection+.08-s dock+.02-s read/site). These are scoped schedules, not universal
bounds. Multiple selected rows/columns form a Cartesian product;160 address lines do
not establish arbitrary independent parallel motion, holding or half-select isolation.

## Historical manufacturing and lead screen

`analyze.py` preserves the initial .15/.4/1/3-mm-lead sweep:27/8/4/2 heads for
this sample. E-255/E-256 supersede its preliminary retention/drive investigation;
A-007/E-050/E-131/E-156 keep their scoped dense/friction/arrest failures. The old
.4-mm/3-mm-diameter threshold μ>.0424 becomes>.0512 at2.8/.45; not PLA priors.
Resident ledger:6,400 columns/screws/thread pairs/thrust supports/sockets/antirotation
duties and12,800 guide duties, plus80B shared rotary channels. Illustrative stock
~6 L and two10-s placements/site (~35.6 h) remain unqualified manufacturing warnings.
The old$250+$.02/site reserve was an allocation, not a BOM. Current costs below use
E-255. Research$1000–1500 does not authorize purchase or revise final<$500.

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
new visual workflow within4 s. They are not measured player waits; <30 s remains.

For each suite, three initial setups plus all six directed map pairs:

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
none meets the final <$500 goal. Detail selection is premature.

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
