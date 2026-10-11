---
status: complete
builds-on: [E-172, E-098, E-095, E-097, E-089, E-054, E-056, E-148, E-170, E-171, E-090, E-146]
---

# Lateral tooth addressing removes height-group writes, at a narrow-lane cost

**Retain the lane-addressed rack for a bounded guide/retention discriminator.**
Separating the five rack teeth into different lateral lanes lets one grounded
dog remain inserted during pickup and deposition. A top-of-stroke scan selects
its new lane. Three programming scans replace E-172's matched separate-contact
control's twelve; a second independently selected pickup remains. This is a new
combination here, not a new rack principle or a selected machine. The finite
rigid section supports arbitrary old/new pairs under declared bounds, but dog
indexing, guides, readback and bank arrest are unbuilt. No printing or purchase.

Input main `5bc2c23`; LAB-283. Reproduce with
`python3 tools/curated-experiment-checks/E-173/lanes.py` (standard library; imports
E-172's unchanged scheduling source). Evidence: generated boxes, unilateral
quasistatic contact, deterministic uncertainty bounds and conditional timing/cost;
self-review only. No measured process prior, reliability probability, complete
assembly CAD, priced components or independent/hardware qualification. Output
JSON is reproducible and discarded.

## Exploration: change the sequence or remove its need

| Combination | Causal support/selection route and screen |
|---|---|
| Push-push latch | Binary pickup selects changed cells; deck overtravel powers heart-cam release/reseat of a grounded dog, with follower and return spring. Same-old cells given identical arm/history cannot finish at independent targets 10.1/40.4. Phase is not target storage; add memory/comparison, different exposure or writer intervention. Read phase/support; stop the supported deck on disagreement. |
| Displacement/countdown trip | Row writer stores signed travel; shared motion moves a reader or spends a count; a powered transfer closes ground before releasing grip. Phase inhibit isolates unchanged cells and return. Duplicates E-089/E-090; counting does not construct support, and E-146 forbids free automatic rearm. |
| Overrunning pawl | Selected pad lifts against ramped teeth; spring returns pawl onto grounded flat faces. On reversal it catches the first available tooth, so arbitrary lowering still needs target gating. E-054/E-056 prove neither ramps, return nor dynamic capture. Keep as control; faults require retained pad support and a real clearance/reseat route. |
| Lane-addressed rack | Ground dog stores target as transverse position; each tooth has its own lane. Selective pad lifts, unloaded scan changes lane, gravity deposits on the unique tooth, final pad clear isolates the next cycle. Probe below: removes the repeated release/capture action but retains two selectors and a bank brake. |

Three genuinely different search moves: push-push cyclic sequencing by analogy,
retained output-travel programming, and transposing time-separated tooth access
into spatial lanes. The pawl is a comparison within sequencing, not a fourth
independent discovery. [US4636601A](https://patents.google.com/patent/US4636601A)
describes a heart-cam push-push switch with successive lock/release actions and a
recovery spring (accessed 2026-10-11); it supplies an analogy, no load/scale claim.
The lateral-rack patent query found no useful close match; no novelty clearance.
Repository cross-checks include
E-089/E-095's passive deck separation, E-097's moving upright staircase and
E-098's single-lane rack. Here the upright steps become column-carried teeth
in separate lanes; only a small grounded dog traverses, so E-097's tall moving
stop/neighbor collision is not inherited. E-170/E-172 remain distinct controls.
E-148 integrates jaw release energy,
not target information. No saturation claim.

## Finite support cycle

Five levels `j*10.1`, j=0…4, give 40.4-mm nominal travel. Dimensions in mm:
column spine X=−.6….6, Y=−2.3…2.3, Z=h−41.4…h+50. Tooth j has
X=.2…1.8, Y centered at `.9*(j−2)` with width .5, bottom h−10.1j+epsilon_j,
thickness 1.2. The grounded dog is X=1.2…2.2, width .5 in Y, top g,
thickness 1; it translates 3.6 mm between extreme lanes. Column/tooth root
volumes overlap by .4 nominal (≥.2 in the .05 box). The dog is ground-guided.

Opposite-side pickup lip: X=−1.8…−.2, Y=±.5, underside h+delta, thickness .9.
Deck pad: X=−2.2…−1.2, thickness 1 below deck coordinate d, Y=±.5 when active
or 1.2…2.2 when clear. Its 1.7-mm Y stroke fits inside the cell. A 4.6-mm-square,
1-mm cap begins at h+50, above the +45.4-mm deck even on unchanged low columns.
That standoff is necessary for this layout, not hidden compactness credit.
Nominal full swept extent is 136.8 mm before guides/frame/brake/service room.

1. At d=−2, write changed pads active; unchanged pads stay clear and dogs stay
   at their old lanes. No unsupported latch release occurs.
2. Raise to 45.4, stopping at each used old level +2 for pickup proof. A tooth
   already on its dog simply lifts away. All lower teeth are in different Y
   lanes and pass the dog; no ramp, reversible pawl or return spring is needed.
3. With all selected columns on pads, scan their dogs once from old to target
   lane. Every tooth is above the dog throughout this transverse sweep. Retain
   and prove the actual lane before descent; no actuator stays to hold it.
4. Descend through target+2 and target proof stops. The chosen tooth lands on
   the dog while the open pad separates and continues downward. Other teeth
   bypass it. At d=−2, clear/prove changed pads in one final scan.

For fixed selected lane j, seated h is `10.1j+g−epsilon_j`. With an active pad,
`h=max(seated,d−delta)`; a clear pad leaves h=seated. Contact follows actual
face overlap and equality; ground/pad reactions are nonnegative and sum to
.1/1/10-N scenario loads. Ideal prismatic joints carry moments. E-056 warns
that this does not establish real guide equilibrium under eccentric pressure.
The lateral index is also an explicit retained-coordinate boundary.

Independent epsilon_j and g=±.05 and delta=.95/1.05 are bounded scenarios,
not X1C priors. Top-setting clearance is at least **3.85 mm**; target proof
separates the pad by at least **.85 mm**. Endpoint travel remains ≥40.3 mm.
The source replays all 25 pairs under 128 vertical-error patterns (**249,600
poses**), all 625 two-cell maps (**56,210 poses**) and nonsymmetric 1/4/16
subdivision holdouts (**1,950/4,725/15,825 poses**). Contact breakpoints and
interval midpoints are explicit. Between them
motion is affine; lane disjointness prevents intermediate tooth collisions.
Continuous top-sweep vertical separation is stronger than its sampled poses.
Every generated solid stays inside a 4.6-mm-square XY envelope, proving both
lattice directions clear at arbitrary neighbor heights/pad states. Bounded
XY separation below extends that certificate to dimensional error.

## Manufacturing sensitivity and failures

Each relevant body center and facing edge independently ranges ±e. Four adverse
terms give minimum selected Y overlap `.5−4e`, wrong-lane gap `.4−4e`, X bearing
`.6−4e` and nearest cell-envelope gap `.48−4e`. Actual interval corner enumeration
checks the first three; full coordinate envelopes give the last. Pad/lip capture
and spine clearance
are also ≥.6−4e; inactive pad/lip Y gap is ≥.7−4e. Coherent
bank registration, opposing local shifts and common tooth-width bias are allowed;
there is no independent-cell averaging or invented yield distribution.

| e mm | Selected Y overlap | Wrong-lane gap | Conservative X×Y bearing mm² |
|---:|---:|---:|---:|
| .025 | .40 | .30 | .200 |
| .050 | .30 | .20 | .120 |
| .075 | .20 | .10 | .060 |
| .100 | .10 | 0 | .020 |
| .125 | 0 | −.10 | 0 |

The .05 box survives this section; .10 loses strict lane separation, and .125
admits wrong-tooth contact (**.003 mm³** at .05-mm penetration).
At .05, .1/1/10 N require mean bearing
pressure at least .833/8.33/83.3 MPa at the minimum patch; no PLA allowable or
strength pass. A 0.5-mm tooth breadth/dog nose is a repeated process risk on the
specified .4-mm-nozzle PLA process. Vertical thickness can grow independently,
but wider lanes consume address range; dimensions alone do not fix indexing.
At e=.05, .5-mm dog/tooth widths and .05-mm wrong-lane reserve need lane pitch
≥.75 mm. Within the same 3.6-mm center span this permits at most five lanes;
nine heights require changed packaging/width/error, not just more tooth levels.

A **+.41-mm dog misindex** from target lane 2 overlaps lane 3 by .01 mm and
captures h=30.3 rather than 20.2. Lowering .05 mm through that first contact
produces **.0003 mm³** actual tooth/dog overlap. Support-only proof can therefore
accept a firm wrong-height state; measure height and retained lane. With .05-mm
face recession on both parts, a dog halfway between lanes overlaps neither
tooth. The pad must not clear without ground proof.
A missed pad clear lifts an unchanged zero-height cell by **2 mm** on the next
pass at d=3. A setting-time misindex must keep the deck carrying at the top
for rewrite/proof. A late height fault must stop on existing support; its
recovery is unbuilt. The short retry below covers bounded seating errors only.

Warp, tilt, hole shrinkage, first layer, layer quantization, roughness, friction,
anisotropy, tooth/root bending, guide play, elastic bank deflection, creep,
fatigue and wear are uncalibrated. Extra errors must fit these margins or rerun
an enlarged bound. Common lateral/height reader bias can affect a whole bank;
zero replay failures supply no reliability estimate or reader false-accept rate.

## Matched complete-machine allocations

Use E-172's five-height dense workload (all 20 unequal pairs repeated in every
row), 80×80 sites and B equal parallel row banks. Each bank has n=80/B rows.
Three scans write pad-on, five-position dog and pad-off, with scan directions
forward/backward/forward plus the final full row-axis home return. Target
programming is allocated **.5 s/row**, versus .1 s for binary pad setting; all
include approach, retention, actual readback and withdrawal. Do not treat a
five-position setter as a free binary stroke.

The deck retains the matched separate-contact itinerary and all ten .1-s
pickup/ground proof stops; only dog writing disappears from those stops.
Central motion is 200 mm/s, 5,000 mm/s², stopped at every waypoint. Charge 2 s
preparation/registration/final settling, one complete .5-s repeat write, one
.1-s proof retry and 2×2.2-mm reseat motion. Proofs require parallel bank sensing;
false acceptance, persistent jams or late misindex are outside this successful
completion allocation. No overlapped motion or hidden preparation is credited.

| Banks | Lane rack s | E-172 crossbolt s | Separate contacts s | Direct heads s |
|---:|---:|---:|---:|---:|
| 1 | 77.918 | 265.347 | 160.797 | 69.776 |
| 2 | 41.252 | 134.347 | 82.197 | 36.238 |
| 4 | **22.919** | 68.847 | 42.897 | **19.469** |
| 8 | 13.752 | 36.098 | **23.247** | 11.085 |
| 16 | 9.169 | **19.723** | 13.422 | 6.892 |

This changes minimum passing tested banks from eight to four against separate
contacts; it does **not** beat direct heads at .5-s word setting. At .1/.2/.5/1-s
word slots, first passing central B is 2/2/4/8. At B4 the word slot must be
**<.83720 s** under the other allocations. Four extra overhead seconds give
26.919 s/B4. Slow/central/fast motion and word-slot sensitivity are executable;
none is a measured actuator capability. The 5×5 initially flat patch (20 changed
cells), all 76 vertical placements, takes **6.660–9.257 s/B4**. Unchanged cells
remain grounded in the model; vibration and miniature stability are unmeasured.

The favorable shared writer boundary is **82B bundles** (80 complete setting
channels, row drive, lift drive), with access to home pads and fixed ground dogs
granted as in E-098. This arrangement still needs real two-plane/opposite-side
engagement, guides, reader, power and bank brake, paid inside bundles or reserve.
Independent pad/dog writers instead need **163B**, including two row axes.
At B4, $500 ceiling/$250 reserve/free bought sites allow **<$0.76220** per
328 shared bundle, or **<$0.38344** per 652 split bundle. Split writers almost
erase the channel-count advantage over the 656-bundle B8 separate-contact
control. Direct B4 uses 324 richer head bundles with <$0.77160 allowance;
these functions are not interchangeable motors or current quotes.

One $.02 bought part/site consumes $128 and reduces B4 shared allowance to
**<$0.37195**; $.05/site plus reserve already exceeds $500. Target retention,
column/pad/dog guides, wiring, sensors and fasteners cannot be omitted. Lane
routing retains 6,400 pickup selectors and 6,400 ground selectors, with 32,000
narrow tooth faces and five stable dog positions/site. It avoids crossbolt's
second ladder and long command tongues but does not eliminate repeated precision
support. One ten-second assembly operation/site costs 17.8 h; sliced material,
print time/scrap, calibration, wear and service remain unpriced.

At least **32,000 individual proof opportunities/map** cover pad-on, pickup,
retained lane, ground support and pad-clear; no false-accept bound is known.
Shared motion still carries up to 1,600 selected cells/B4, demanding grounded
arrest of **160/1,600/16,000 N** at .1/1/10 N/site, plus deck weight. Dog commands
do not arrest the free deck while pads carry columns. With uniform downward
loads and the dense map's mean old/target height 20.2, nominal lift to h=44.4
requires **15.488/154.88/1,548.8 J** board work; descent must absorb the same
load energy. At .2 m/s simultaneous loaded lift would demand 128/1,280/12,800 W
instantaneous useful power at those loads, excluding inertia/friction. Loads,
rate and ideal unilateral descent are scenarios, not required or qualified
machine capacities. Gravity supplies lowering contact only for positive net
downward force; bounce, zero load and signed external loads need other evidence.

## Disposition and next discriminator

This is a supported **contact/schedule candidate**, not a complete-machine pass.
Stop further binary push-push/countdown elaboration without target encoding or a
changed transfer. Keep the lane topology because it removes height-group writes
causally and changes the bank-count tradeoff; do not reopen E-172 guide refinement.

Next construct **grounded Y guidance plus five-state retention and unloaded
writer access**, testing finite loaded contact/pressure position, withdrawal,
misindex and neighbor clearance. Compare amplified or remotely retained indexing
against narrow local detents; surface pitch is not an internal-component mandate.
Carry the actual extra axes/channel costs and write time. Stop this embodiment if
it cannot retain the .05-box lane/guide margin under explicit loads, or if access
restores the control's bank/channel burden. Do not treat another nominal box pose
as that evidence. Bank input-loss arrest remains an independent shared-drive
obligation; no free brake was introduced. No physical experiment is yet justified.
