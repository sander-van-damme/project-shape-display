---
status: complete
builds-on: [E-254, E-255, E-256]
---

# Same-area quarter-square terrain and paid neutral comparison

**6.35 mm deserves further comparison; fewer cells do not establish playable walls
or a purchasable machine.** The connected-wall alternative below retains the inspected
one-square passage and bridge width, reduces B2 channels160→128 and its favorable
bought allocation$1128→$953.92. Ordinary ground fixed across physical maps requires
**50-mm total travel**, and changes map-pair deltas. This is distinct from the earlier
paid initial flat, which leaves all target heights unchanged.

Reproduce with `python3 tools/curated-experiment-checks/E-257/screen.py`;
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
