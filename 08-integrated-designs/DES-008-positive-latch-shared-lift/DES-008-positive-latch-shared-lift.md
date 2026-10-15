---
status: candidate
builds-on: [DES-007, E-281, E-258, E-228]
---

# DES-008 — positive latches, resident mechanical memory, and shared bank lifts

**Recommendation: build the small positive-latch support-transfer article; do not build a full display yet.** The strongest surviving full-machine hypothesis is two stationary bank lifts, addressed through reusable column setters and mechanically enabled row memories. It avoids both the DES-007 selector-per-head-lane expense and the repeated travel of a narrow mask writer. Its timing is conditionally promising. A guide revision removes the sampled planar jam, but leaves no guaranteed unloading margin; the priced construction exceeds budget and playable walls remain unresolved. This is an engineering handoff at a physical and manufacturing boundary, **not digital product success**.

## Baseline and evidence preserved

Work started from current `main`, **b23ed12**, fetched on 14 October 2026. That commit already merges `codex/des007-radial-pinch` and includes the newer owner observations. The requested `1c622b0` is in that history. Development takes place on `codex/des008-multiplexed-lift`; no historical experiment was rewritten or branch blindly merged.

Independent calculation reproduced DES-007's 64² four-head finite-strip case: **68.93 s** worst sampled transition. Its eight-head endless-loop comparator is **29.38 s**, with **512 selectors** and a historical allocation of **$9,072–$16,257**. The latter is not the fabricated strip mechanism. Its nominal isolation test repeats a fixed geometric gap and does not establish elastic-strip isolation under tolerance, preload or wear. Preserve DES-007 as an untested friction-drive experiment; it is not the preferred full-display architecture.

The owner reported five hand-driven short-thread pairs, each completing five forward/reverse cycles without damage or postprocessing. The 0.20-mm-relief pair felt best; nominal 0.15-mm pairs varied. Those nuts are **10.3 mm wide**. The historical narrow Trial 5 family has positive owner recollection, but its exact successful parameters are unknown. Supports obstructed the new narrow replica, so it has **no functional fit result**, rather than a demonstrated thread failure. None of these observations measures powered torque, array yield, holding load or neighboring-pin independence. No duplicate short-thread test is requested here.

## Architecture comparison and engineering iterations

| Candidate | Power, selection and retained support | Decision-changing result | Disposition |
|---|---|---|---|
| DES-007 radial strip | Shared friction drive; individually selected pressure shoes; thread retention | Constructed-strip schedule 68.93 s; favorable fast comparator retains 512 costly selectors; strip strength/friction unresolved | Preserve evidence; stop full-display development |
| Scanned independent rack/screw drives | Independently reversible drives across each visited row; local passive supports | Four 64-output heads have a favorable 23.96 s linear-motion comparison, but require 256 moving drive channels; access, packaging and full drive cost remain | Performance control, not low-cost winner |
| Crossed rigid row/column support combs | Either comb holds an output; releasing both selects an intersection | Unchanged pins transfer between independent bearing datums. Biasing one comb merely moves the disturbance to other rows | Reject this support topology |
| Shared row lift, binary displacement pulses | One grounded pawl per pin; captured dogs; mask rewritten for each signed pulse | Even favorable 0.20 s *complete* mask writes yield 38.00 s at eight banks in the 40-mm/5-mm-step case; physical writer travel is additional | Reject as 30 s solution at this bank count |
| Retained row grips, stopped retirement | Keep unfinished dogs engaged; separately restore support and release completed outputs | Eight writers per head give 48–62 s in optimistic comparison models; actual reader/keeper sequencing remains slower. Sixteen heads with 32 writers regain 26 s by restoring **512 active writers** | Reject the apparent selector saving |
| Prewritten target memories | One signed target per lane; local comparator/cam retires it; double-buffer next row | Five bits needed for 17 signed 5-mm deltas. Even favorable overlapping programming leaves approximately 37–39 s with eight heads and stopped retirement | Park; memory alone does not remove support-transfer time |
| **Stationary resident masks, two bank lifts** | Reused column setters write a mechanically enabled row; resident state gates captured dogs and fixed pawl releases; global signed subset strokes | No row-head travel or repeated 64-bit lateral scans. Full-row-scan sampled times **24.83 / 25.08 s** for 40 / 50 mm at 80 ms per complete row write | **Conditional topology; revised guide still lacks qualified seating margin** |

These are embodiment-specific rejections, not an impossibility theorem. A different local retirement, combined cam or fabrication process must replace the failed transaction before its benefit can be credited.

Jacquard, knitting and fluidic-matrix research informed the mechanisms; none establishes compatible cost, sealing, retention or selector speed. See [sources and dispositions](research.md).

## Construction and operation

Use a normally engaged, rigidly backed ground pawl at every site, a separate captured dog for forced bidirectional motion, and a resident memory gating two separately sequenced common frames. Unchanged terrain keeps its original ground support. The ordered sequence is **dog capture → take up load → ground release → signed movement → ground restore → seat → dog withdrawal**. One row of mechanical memories is written by aligning column setters to OLD bits, raising only that row into channels, setting NEW bits, and lowering it into fixed pockets.

The [construction principles](construction.md) and [dimensioned resident-cell study](resident-integration.md) make the load paths explicit. The latter uses two captured T-feet in each stored C-guide, separate A/B frames, paired end registers and paired programming bars. It occupies about 293 mm vertically and requires tiny metal sliding interfaces. The [bounded guide revision](guide-escape.md) preserves the original failure and its remaining limits. Full-frame manufacture and tolerance remain unqualified; this is not released full-machine fabrication CAD.

## Timing: conditional arithmetic, unmeasured rates

Use the sequential decoder comparison, which scans **every row for each mask**. At an assumed **80 ms per complete OLD → row-up → NEW → row-down/index/check transaction**, two stationary banks give:

| Field | 40-mm stroke | 50-mm stroke | Complete row-cycle limit for 30 s |
|---|---:|---:|---:|
| 64², 6.35-mm pitch | 24.83 s | 25.08 s | 107 / 106 ms |
| 80², 5.08-mm pitch | 28.67 s | 28.92 s | 86 / 85 ms |

All four fail at 120 ms/row. The models include mask clearing, five 80-ms support/check events per pulse, 0.4-mm take-up, then post-ground 0.7-mm seating and 0.3-mm centring, loaded and empty moves at 80 mm/s and 800 mm/s², a one-mask-plus-pulse **time reserve**, and four seconds of common work. That reserve does not qualify recovery from uncertain OLD memory, whose supported reset remains missing.

The [corrected workload and timing ledger](timing-evidence.md) distinguishes cold starts, neutral preparation, sustained updates, local reveals and dense stress. At 64², the full-scan model takes **31.89 / 38.99 s** for neutral-plus-first-scene and **38.76 / 39.52 s** for dense levels (40 / 50 mm). These cases are not covered by the favorable scene maximum.

The inherited E-254/E-258 maps are hand-annotated examples, not measured gameplay frequencies. Their full-pitch walls fail the separate corridor test. The 40-mm encoding explicitly sacrifices 10 mm of ravine depth. Mechanical timing and settling remain assumptions: these are **not measured 30-second playable-display results**. The [independent system audit](review/revised-system.md) reproduces the final sequence; the older traveling-head audit preserves its rejected schedules.

## Cost: fewer active selectors does not yet mean an affordable machine

The 64² stationary hypothesis uses **128 shared data actuators**, at least two lift axes, two row-enable/index mechanisms and two independent A/B sequencing duties. The machine still contains **4,096 each of terrain pins, ground pawls, lifting dogs and memories**, plus guides and release/read followers. A common actuator is not a free mechanical distribution network.

Current catalog references put 128 small solenoids at **$506.88**, sixteen driver boards at **$215.36**, and eight low-cost motor/driver accounting pairs at **$167.60**: **$889.84 before** frame, rails, supply, wiring, printed columns, fabricated memories, latches or suitable high-force lift drives. This anchor alone exceeds the original $500 bought-parts benchmark. The [supported bank-drive comparison](bank-drive.md) adds $903–1,424 for two banks, replacing two unqualified lift motor/driver entries. **This conventional construction exceeds $1,500 before the remaining terrain mechanism.** A cheaper transmission is unqualified.


Resident-mask affordability remains **unresolved and currently unsupported**, not passed. A production quotation for complete comb/flag/follower modules and a tested drive-force budget are decisive dependencies. Injection molding is a later option; hypothetical volume savings do not finance the first machine. No purchase was made or authorized by this analysis.

The integrated solid columns weigh **14.93 kg**, replacing the earlier 7.06-kg estimate. At the same $20/kg polymer input, the minimal electronics/common-hardware allocation leaves only **$51.56, or 1.26 cents/site**, under $1,500 before resident mechanisms and suitable lifts. With the conventional lift provisions, the allocation is approximately **$2,310–2,830 before custom resident parts**. These are allowances, not quotes. At the reference coil rating, simultaneous selection requires **704 W / 140.8 A at 5 V**; supply, duty and sequencing remain unqualified.

## D&D geometry is a separate unresolved product constraint

For two equal walls centered on grid lines 25.4 mm apart, the inner-face gap is **25.4 − wall thickness**. Full-pitch walls leave 20.32 mm at 5.08-mm pitch and 19.05 mm at 6.35-mm pitch. Even a 0.8-mm panel leaves only 24.6 mm and excludes a real 25-mm base. A 25.4-mm base cannot fit between any positive-thickness centered walls, even with zero placement allowance. Finer terrain resolution does not change this result.

The package therefore does not claim automatic playable thin walls. Smaller bases, widened physical grid spacing, widened passages, displaced walls or selectively supported elevated wall panels are explicit product alternatives, each with consequences. Raised panels require a complete traversable base-height opening and supports outside the walking envelope; a drawing that fits a stationary base but blocks passage is not a solution. A separate automatic wall subsystem could require up to 544 grid-edge segments for sixteen-by-sixteen squares and is not included as free hardware. Actual owner base dimensions and an accepted wall interface remain necessary.

6.35 mm is a useful **mechanical comparison pitch**, giving four terrain samples per square and fewer repeated parts. 5.08 mm provides five samples and remains a comparator. The cap/guide/tilt trade-off, stable miniature support at cliffs, and useful wall/door geometry must all pass before either is a selected product resolution.

## Build boundary and qualification

The small positive-latch article asks a new question: can neighboring captured racks move up and **positively down**, transfer onto their original grounded latches, and leave witness pins stationary? The separate short-flag memory article is **DEFERRED**: its verified files are preserved, but it does not qualify the resident design’s tall channels and paired pocketed writers. The support-transfer article tests a new question without repeating short-thread fit or claiming an automatic selector.

The [P1 print handoff](../../owner-print-tests/positive-rack-handoff/test.md) and [verification record](verification.md) identify released files, orientation, estimated material/time, assembly and tests. A READY mesh is a fabrication handoff, not a physical pass. Stop on forced fit, skipped support, damaged fingers, changed witness height or incomplete latch seating. A successful coupon permits measured tolerance/force/timing work; it does not justify ordering a full array.

| Requirement | Classification at handoff | Evidence / remaining boundary |
|---|---|---|
| DES-007 baseline accounting | **Computationally demonstrated** | Independently reproduced; historical physical limits preserved |
| Manual short-thread engagement | **Supported by physical observations** | Owner-reported five pairs; wrong width for a compact-array qualification |
| Independent signed selection logic | **Computationally demonstrated in stated ideal models** | Actual pawl/dog and matrix hardware still untested |
| Positive retained load, forced descent, no neighbor motion | **Unresolved physically** | Small CAD articles and adversarial test sequence; no physical measurements here |
| Stationary two-bank timing | **Computationally demonstrated conditionally** | Complete row write and mechanical event rates unmeasured; stress cases separate |
| Traveling low-writer-count architecture within 30 s | **Failed in screened embodiments** | Multiple independent schedules and explicit transaction ledgers |
| Integrated guide and full-machine construction | **Original guide failed; bounded revision unresolved** | Planar jam repaired in sampled poses; vertical play consumes unload margin; bank junction unbuilt |
| $500 affordability | **Failed for catalog electronics anchor** | $889.84 before major hardware |
| $1,000–1,500 complete demonstrator | **Failed for priced construction; cheaper alternatives unresolved** | About $2,310–2,830 before custom resident parts |
| Common-base thin-wall one-square corridors | **Failed for centered walls considered** | Exact clearance inequality; alternative interface not accepted or built |
| Manufacturing repeatability and physical prototype success | **Unresolved** | No claim of array yield or performed tests |

**Do not continue by optimizing the discarded traveling mask head.** The useful next evidence is mixed-drag positive support transfer, then a quoteable resident module with controlled guide play and measured row-write timing. If those fail the available margins, the remaining honest choices are a higher-cost direct-drive architecture, slower scene updates, reduced field size, or a changed playable wall/base interface. Each is an explicit product trade-off, not a silent relaxation.
