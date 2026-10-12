---
status: complete
builds-on: [E-253, A-007, E-050, E-131, E-156]
---

# Sampled gameplay geometry: sparse walls still visit most rows

**Defer E-253 detailing; test shared rotary programming before selecting screws.** Ruins
raise 13.55% but visit 74/80 rows. River/ravine relief raises 69.52/71.48%: upward-only
columns elevate surrounding ground to depict depressions. A serial addressed screw is
slow; parallel screws trade lead/retention against head cost.

Input `92aa01c`, reconciled with owner guidance at `e5308d0`. Evidence: **manual published-map annotations, assumed conversion/play
sequences, calculations, conditional schedules; self-review**. No observed play
frequencies, physical qualification, typical fraction or tail statistic. Reproduce
`python3 tools/curated-experiment-checks/E-254/analyze.py` (stdlib). `sample.json`:
provenance/hashes, crop transforms, polygons/centerlines/assumptions. `heightmaps.json`:
four retained 80×80 arrays, digits ×10 mm; checked against source. `--write-maps`
intentionally refreshes these. stdout results are disposable.

## Provenance and conversion limits

Convenience sample selected for distinct visible terrain: ruined enclosures, a river
ford with islands, and a bridged ravine. All are by **Ross McConnell, 2-Minute
Tabletop**, accessed 2026-10-12:

- [Desert Ruins](https://2minutetabletop.com/product/desert-ruins/): standing walls and slabs.
- [Riverside Road](https://2minutetabletop.com/riverside-road/): river/ford/islands/rocks. Flattened-water variant loses bank relief; it is not an independent sample.
- [Mountain Ravine](https://2minutetabletop.com/product/mountain-ravine/): plateau/bridge/ravine/boulders; [published D&D use](https://2minutetabletop.com/mountain-ravine-encounters/), not observed play.

Trace only major terrain; omit small rubble, furniture, foliage and texture. Heights are
assigned representations, not recovered elevations. No functioning projection is assumed. The bridge has a solid underside; slopes are stepped.

Normalize previews to 800×555 pixels. Their ~23×16-square grids are cropped to central
~16×16-square windows at five pins/square, not squeezed onto the display. Ruins/ravine
use `(102,-3,560,560)`; road `(104.25,0,556,556)`. A few outside edge pixels continue
the traced boundary/base (sub-pin assumption). Cropping excludes the thick west ruins
perimeter and parts of eastern rooms. Results characterize these windows, not entire
source maps.

Three windows, one author/style/annotator, no indoor/cave sample, no observed sessions
or independent tracing assessment: deliberately varied, not random or representative.
Manual annotation constructs benchmark inputs offline. Schedules start with submitted
height fields; arbitrary artwork conversion is unimplemented.

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

## Transition assumptions and full service counts

Initial setup: flat→map. All six directed map pairs hold crops fixed; these are
**hypothetical**, not observed campaign sequences. Reverse transitions have equal
absolute travel but different raising/lowering forces. East reveal restores x≥40 from
flat while x<40 is already set. Local reveal restores `40≤x<60,20≤y<40` from flat (four
D&D squares/side). Visual fog-of-war could need no motion; mechanically revealing raised
ground may be unsuitable under miniatures.

| Transition | Changed | Rows / max bank rows | Unchanged raised cells | E-253 s | Screw B3, lead .4 s |
|---|---:|---:|---:|---:|---:|
| Flat→ruins | 13.55% | 74 / 27 | 0 | 178.14 | 38.61 |
| Flat→road | 69.52% | 80 / 27 | 0 | 178.01 | 31.37 |
| Flat→ravine | 71.48% | 80 / 27 | 0 | 178.01 | 59.11 |
| Flat→flattened road | 2.77% | 24 / 14 | 0 | 97.05 | 22.54 |
| Ruins↔road | 69.66% | 80 / 27 | 210 | 178.01 | 34.11 |
| Ruins↔ravine | 74.67% | 80 / 27 | 0 | 178.01 | 59.11 |
| Road↔ravine | 91.55% | 80 / 27 | 0 | 178.01 | 57.11 |
| East reveal: ruins | 5.73% | 63 / 27 | 500 | 178.36 | 38.61 |
| East reveal: road | 37.69% | 80 / 27 | 2037 | 178.01 | 31.37 |
| East reveal: ravine | 33.70% | 80 / 27 | 2418 | 178.01 | 59.11 |
| Local reveal: ruins | 0.56% | 17 / 13 | 831 | 90.91 | 21.26 |
| Local reveal: road | 2.67% | 12 / 7 | 4278 | 53.25 | 10.83 |
| Local reveal: ravine | 4.56% | 20 / 13 | 4283 | 90.83 | 28.26 |
| **Separate dense stress**, flat→40 mm | **100%** | 80 / 27 | 0 | **178.01** | **66.61** |

No observed miniature locations/loads; all unchanged cells are potentially loaded. Local reveals preserve 6364/6229/6108 cells, including
**1324/789/1308 in serviced rows**. E-253 ideally retains their primary seats; screw
control never turns them. Neither proves physical non-disturbance. Whole-row
release/homing is not credited; readback occlusion, common bias and frame flexure remain
unresolved.

**E-253:** import its actual geometry, physical writer and synchronous sparse scheduler.
B3 has 240 writers/outputs, 2.548 s physical writing per row, two color phases, all
empty resets, monotonic stopped seek, return to bank zero, 2.010-s common allocation and
one immediate full-row retry. Main programming is **640 decisions/visited row**,
including neutral codes: 47,360 decisions for initial ruins versus only 867 changed
cells (5,920 row output slots, 6.83× inflation); dense maps need 51,200. A single
retried row adds 640 decisions. Sparse exact dense time is slightly above the old
177.424-s station formula because it now includes explicit final return. No free radius
writing or inherited physical capture pass.

**Idea 9 screw rows:** grounded screws/thrust supports, antirotating translating
nuts/columns, underside sockets; 80 independent reversible spindles per head. Changed
sockets alone dock. Screw angle stores height; actual top/hold proof precedes release. B
heads serve disjoint banks without homing unchanged columns. Selective docking is
unbuilt; touching every socket owes unwanted-torque proof.

Reconstruct E-050 central rates: translation 200 mm/s, 5,000 mm/s², 3,000 rpm, .08 s
dock/release, .02 s row read, ≥.05 s index, 4 s common overhead. Add assumed rotary
acceleration 60,000 rpm/s (not torque-qualified). For D revolutions, `v=50 rev/s,a=1000
rev/s²`, spin time is `2sqrt(D/a)` if `D≤v²/a`, otherwise `D/v+v/a`. Row time is
`.10+spin(max|delta|/lead)`. Sum actual seeks/services and empty return within each
bank; map time is `4+max(bank totals)+largest row service`, including one immediate
supported retry. The 4 s owes decoding, registration, final/unchanged-region checking,
diagnosis and settling. None has a qualified deadline. Independent signs, parallel row
read and the ramps are assumptions. Persistent jams require a supported stop; they are
outside successful bounded-retry timing.

Screw programming requires **35,975 / 115,650 / 347,300 revolutions** and
867/4449/4575 dock/read transactions for initial maps at .4-mm lead. Parallelism
reduces time, not wear; row maxima prevent free packing into other idle spindles.

**Changed-cell single writer / Idea 10 serial AND oracle:** same .4-mm lead, rates and
per-site contact/read. Moving writer uses a row-serpentine route, rest-to-rest
simultaneous XY seek and final return. Stationary matrix grants free power routing but
charges .05 s to write/settle the row/column selection and .08 s
engagement/disengagement plus .02 s read at each intersection. Initial ruins/road/ravine
take **970/3300/7979 s** moving, **898/3208/7867 s** stationary; these are scoped
scenarios, not universal lower bounds. A real matrix needs torque-qualified
bidirectional AND, half-selection isolation, source-loss behavior and readback.
Selecting several rows/columns activates their Cartesian product unless additional
masks/state prevent ghost selection; 160 address lines and one motor do not implement
arbitrary parallel subsets.

## Replication, manufacturing and joint economics

A-007's old dense rejection stays scoped. E-050's 1/2/4-mm leads require ideal
square-thread μ>.106/.212/.424 at 3-mm mean diameter. E-131's zero-margin lead at μ=.05
is .471 mm. E-156 shows static holding does not establish moving arrest; its rotating-nut
coast results do not qualify this rotating-screw control. Stopping before undocking
still owes power-loss/downstream-failure safety.

Leads .15/.4/1 mm require μ>**.0159/.0424/.1061** at diameter 3 mm. A common diameter/lead
corner 2.8/.45 mm raises the middle threshold to **.0512**, defeating μ=.05. Bounds, not
PLA priors: layer profile, wear, friction, backlash and grid bias can correlate across
modules. Fine .4-mm repeated flanks remain unqualified; a coarse lead may require added
retention, changing the ledger.

| Repeated duty | Per cell / row | Per B-bank head | Whole board |
|---|---|---|---|
| Translating column, rotating screw, thread pair, thrust support, socket | 1 each / 80 each | none extra resident | 6,400 each |
| Antirotation load path / lateral guide stations | 1 / 2; 80 / 160 | head alignment additional | 6,400 / 12,800 |
| Rotary spindle, selectable dock, driver, coupling | none resident | 80 each | 80B each |
| Seek, docking carrier, shared optical proof / torque limiting | shared | ≥1 duty each | B duties; implementation unknown |
| Springs/inserts/individual brakes | not granted | not specified | unknown, not zero proven |

Threads, sockets, thrust contacts and guides wear. Underside replacement of a loaded
seized cell needs access/props. Grid bias, head registration and reader faults can
correlate across banks. Idea 11 can improve few shared interfaces, not 6,400 threads.
Sander's manually successful translation supplies no measured travel/load/torque/wear,
process settings or specimen count.

Illustrative stock: 4.6-mm square column, 3.6-mm square bore, 60-mm stem/1-mm top: 3.284
L; 3-mm solid ×60-mm screw envelopes: 2.714 L. **~6 L before guides, thrust retention,
sockets and heads**, not CAD. At assumed 5–15 mm³/s: 111–333 extrusion hours before
waste. Two 10-s placements/cell: 35.6 assembly hours before inspection. Captive thrust
support, screw whirl, thread engagement, calibration and correlated reprints remain
uncosted/unqualified.

For the three initial setups and six directed map pairs, the tested uniform-bank
schedule needs the following smallest B (strict <30; no population percentile):

| Lead | B / independent spindles | Maximum sample s | Complete channel allowance at $500 / $1000 / $1500 |
|---|---:|---:|---:|
| .15 mm | 27 / 2160 | 26.20 | $.056 / $.288 / $.519 |
| .4 mm | 8 / 640 | 28.04 | $.191 / $.972 / $1.753 |
| 1 mm | 4 / 320 | 23.53 | $.381 / $1.944 / $3.506 |
| 3 mm, conditional historical pitch | 2 / 160 | 22.98 | $.763 / $3.888 / $7.013 |

Allowances assume **$250 shared + $.02×6400 resident purchases**, not a priced BOM. Any
bought thread/nut/thrust cartridge exceeding the resident allocation shrinks them. More
heads are granted the same translation rates; their packaging, force and cost are
unresolved. Thread heat/drive power is not free: ideal 3-mm/.4-mm square-thread raising
at μ=.05–.30 and 1 N gives .139–.520 mN m and .044–.163 W at 3,000 rpm per engaged
output, before bearings/motor loss. At 10 N these scale tenfold; such uniform loads are
sensitivities, not a D&D payload specification. No force-qualified drive or thermal duty
is selected.

**$1,000–$1,500 may justify a credible demonstrator; allocations alone do not.** Final
purchased goal remains <$500. Replacing independent motors with a few shared reversible
drives/reusable selectors is a testable cost-reduction path, provided it preserves
retention/timing/isolation without 6,400 added clutches. No purchase or fabrication.

## Decision and next discriminator

Do not detail E-253: sparse ruins and flattened-water geometry already defeat its
hoped-for few-row case. Screws improve conditional timing, not product qualification.
Ideas 9–11 remain comparators/manufacturing advice. The E-244-cutoff external review's
friction/isolation concerns remain relevant; no clamp campaign reopens. Serial resident
AND is not the next build.

**Next discriminator:** reconstruct the recovered screw mechanism and test whether its
coarse lead can retain load safely while a shared rotary writer meets this workload.
Read-only inspection of `41484f9699:trial-5-grid-and-cubes-and-rod/actuator.scad`
confirms pitch 3, screw OD 3.2/length 50, rod OD 4.4/wall .44, nut length 10 and BOSL2
trapezoidal calls. These are CAD settings, not the successful physical print.
If single-start, 3-mm lead gives 13.3 turns/40 mm and the B2 timing row above, but
ideal square-thread μ threshold is .318 at mean diameter 3 mm. Actual thread profile,
BOSL2 version/defaults, guide/thrust path and loaded hold remain to reconstruct.
Compare stopped reusable-mask rotary heads, orthogonal/reorientable heads and smaller
parallel heads against independent spindles; charge programming, docking, turns,
deceleration, support proof, seek/pre-positioning, retry and manufacturing labor.
Show visible reveal versus sustained cost if pre-positioned; unknown reveals get no
free preparation. Stop before CAD/printing if support or research economics fails.
A survivor may justify targeted actual-process calibration. Prioritize this recovered
family; defer resin microchannels/inflatable pins per new advice. Broaden maps only
when missing coverage could change a survivor's ranking.

Verification: exact raster/stored-map equality; dense/no-op/bank-boundary controls;
independent spin/travel arithmetic; visual source/derived-map comparison; all six
directed pairs; crop/boundary/orientation sensitivity; minimum-bank/cost recomposition.
Internal checks, not independent or hardware validation.
