---
status: complete
builds-on: [E-216, E-217, E-220, E-221, E-222, E-227, E-139, E-156, A-019, E-165, A-022, E-100]
---

# Resident supports save acquisition; encoded strokes save more repeated hardware

**Park the resident-ramp embodiment. Retain six-pulse crossed-support programming for one complete shared-mask writer screen, not local mechanism development.** Moving height memory into 6,400 permanent ramps removes shoe acquisition/reset, but adds swept depth, sliding force and supports without removing independent head retention. A simpler control instead reduces E-220's bank selectors from 1,280 to **480**, conditionally, by changing the physical stroke code. Neither is a selected machine; no fabrication or hardware performance is established.

Input main `37b2dca`. Reproduce with `python3 tools/curated-experiment-checks/E-228/screen.py` (stdlib, stdout only). Evidence: **architecture hypotheses, exact ideal state replay, bounded calculations and constrained integer synthesis; self-review**. All non-product numerical inputs are assumptions, not sourced process priors or prices. Five levels at 0/10/20/30/40 mm are comparison workloads, not an approved height-resolution restriction.

## Obligations reconstructed before choosing a transaction

E-216/E-217 masks still owe 160 retained grips/head. E-220 stores column
position on row OR column combs, with one lift-and-return per signed delta.
E-221 exchanges groups for 80 independently captured old heights. E-222's
shared shaft still needs private parks and retained couplings; its common fluid
valve cannot hold differential positions. A-019/E-165 likewise reject free
independent capture by a common clamp/carrier. Resident media avoid E-227 transport.


Materially different combinations screened:

| Transaction | Information / grounded support / intermediate retention | Screen |
|---|---|---|
| One-hot aperture planes + masked lift | Four shutters select a grounded stop; arrested selective pickup during rewrite | 25,600 retained shutters, unresolved pickup; E-216 remains parked |
| Binary displacement layers | Three extension bits; serial shoulders; active stage held by selected arrested drive | 19,200 stages/catches; A-022 access failure remains, not repaired by arithmetic |
| Resident ramp + drive/park row head | Translation q stores h=sq; captive follower → ramp → bed; keeper or independently parked/driven input | Changed combination of E-139 support and E-222 switching; tested below |
| Resident screw + shared row addressing | Thread displacement; flank/thrust path | E-156 already rejects high-speed coast/selector embodiment; no changed arrest, no repeat study |
| Crossed combs + subset-coded strokes | Column position; row OR column support, then arrested selected finger during motion | Six transient binary masks replace eight disjoint delta masks; new result below |

One-hot writing alone at assumed 71 sites/s/channel takes 45.07/22.54/11.27 s with 8/16/32 channels.

## New resident-ramp transaction and why it stops

Each nonrotating simple column sits in a captive inclined support belonging to one resident translating ramp. A captive return wall is required for forced descent. A grounded bed guides the ramp; an integral periodic rack, pitch 10/s, encodes the five positions. One retained row keeper can engage all racks at their discrete phases. This requires discrete phase equivalence, not arbitrary capture.

A head docks, engages/proves 80 independent grounded parking contacts, then withdraws the row keeper. For each sign, engage selected drive contacts while parked, prove, withdraw their parks, and advance the common carriage through four 10/s increments. At each stopped/braked increment, park completed ramps before disengaging their drive contacts. Other ramps remain parked or driven. After all park, return the carriage empty; repeat the other sign. Reseat/prove the row keeper, read actual heights under resident support, then release the head parks. Periodic racks permit common-datum acquisition; finite coverage, overlap and routing remain unbuilt.

At every ideal state, `row keeper OR private park OR retained drive-to-brake` grounds each ramp coordinate. Unchanged q never changes. The executable replays all **15,625 three-cell old/new combinations**, 1,593,750 support observations, and an 80-cell witness containing all 25 transitions. It also rejects missing last support/brake flags. Brake delay, impact and rebound remain unmodeled; spring-open drive coupling fails source-loss support.

Assume rest-to-rest v≤200 mm/s, a=8,000 mm/s², with `t(d)=2sqrt(d/a)` below v²/a, otherwise d/v+v/a. Each row cycle costs `8t(10/s)+2t(40/s)+10τ+.15+t(5.08)`. Transfers: two admissions plus eight completion masks. τ=.005 s is an ideal flag allowance; the physical-stroke scenario charges two sequential 2-mm contact strokes plus 5-ms proof: **τ=.068246 s**. This grants parallel commands across 80 channels; a cheaper multiplexed writer must add its actual writing. The .15 s must cover dock, keeper motions and output proof; it is unqualified. Full-map `T=2+(ceil(80/B)+1)cycle` includes arbitrary online commands, row feed, 2 s preparation/homing/final settle and one whole-row retry.

| Ramp slope s | Ideal-flags B / channels / s | Physical-stroke B / channels / s | Assumed bought allocation at physical timing |
|---:|---:|---:|---:|
| .5 | 7 / 560 / 29.305 | 9 / 720 / 29.329 | $1,075 |
| 1 | 4 / 320 / 29.308 | 7 / 560 / 27.127 | $865 |
| 2 | 3 / 240 / 27.211 | 5 / 400 / 28.059 | $655 |
| 4 | 3 / 240 / 21.131 | 4 / 320 / 29.630 | $550 |

Costs are a screening allocation: `130+65B+80B*c_channel+6400*c_site`, with c_channel=$.50 and c_site=$0. $130 is shared controller/power/frame/wiring/freight; $65/head grants transport20+dock5+reader15+motor/driver12+brake8+shaft/bearings5. Not quotes or force-qualified assemblies. $.50 grants both contacts, retention, command and sensing share. At s=2, free cell purchases leave **<$.1125/channel** under $500 and no positive allowance under $400. Even ideal-flags $445 leaves only $55 for all other purchases. These allocations miss $200; they are not market cost floors.

## Ramp replication, packing, manufacture and force

All routes retain 6,400 columns, two lateral guide stations/cell and frame load paths. Ramp-specific inventory:

| Function | Cell / row | Largest bank / head at B=5 | Board |
|---|---|---|---|
| Extra moving ramp / grounded slide / captive follower interface | 1 each / 80 each | 1,280 each resident | 6,400 each |
| Rack positions / row-keeper bearing sites | 5 / 1; 400 / 80 | 6,400 / 1,280 | 32,000 / 6,400 |
| Row keeper axes / retained closures | shared / 1 each | 16 each | 80 each |
| Head park contacts / drive contacts / retained channel commands | none resident | 80 / 80 / 80 per head | 400 / 400 / 400 |
| Common carriage / arrest / dock / reader | shared | 1 each/head | 5 each |

Springs, bearings/inserts, fixtures and wiring remain unresolved, not zero. Ramps add bed/follower wear and rack registration. At assumed 10 s/ramp, assembly adds **17.78 h**; 30 s/channel adds 3.33 h at B=5; captive joining may add 6,400 operations. Head/keeper faults expose 1,280/80 cells. Buried ramp repair needs temporary column support and module access.

Choose y-directed private ramps, 3-mm width, profile run D=40/s plus 4-mm foot/end allowance; full sweep is **2D+4**. In this explicit strip layout, rows on one deck require that separation. `K=ceil((2D+4)/5.08)` interleaved decks with 48 mm allocated per deck give, for s=1/2/4: **17/9/5 decks, 816/432/240 mm**. This is a necessary envelope for the chosen layout, not a global packing theorem. Stems, lower-deck clearance and head access are unrouted. Timing favorably treats all row feeds as one pitch even across decks; real multi-deck seeks only worsen it.

Solid triangular ramp-stock scenarios: **15.36/7.68/3.84 L** at s=1/2/4, or **426.7/213.3/106.7 h** at assumed 10 mm³/s, excluding rack/capture/frame/extended columns/setup. Ten percent scrap multiplies by 1/.9. Hollowing needs a load path. Side printing avoids an unsupported incline; anisotropy, warp, 256-mm-bed module seams, creep and wear remain unqualified.

E-100 force balance supplies the **calculated** raising multiplier for equal incline/bed friction μ: `K=(s+μ)/(1−μs)+μ`. For μs≥1 this sliding branch has no finite positive drive solution; it is not a prediction of a real jam force. For a provisional 3.27-N/cell load (not a requirement), the row force at μ=.1 is **346/713/1,814 N** for s=1/2/4. At μ=.3 it is **564/1,583/no solution**. Loads 1 and 10 N scale linearly. Ideal drive torque at 10-mm radius is 7.13 N·m for s=2/μ=.1, before inertia. Captive descent adds flank switching, lateral guide force and friction; no positive-return force pass follows from the raising law.

Competing coherent bounds e=.15/.35/.70 mm combine independent functional errors adversely, not probabilistically: ramp vertical error ±e plus rack-position error ±e gives height uncertainty `(1+s)e`. At s=2 this is **.45/1.05/2.10 mm**; at s=4, **.75/1.75/3.50 mm**. No height acceptance tolerance is invented. Opposed park/drive datums can add a transfer excursion 2se before compliance. A 4-mm opening/2-mm tooth leaves `1−e` insertion margin but needs ≥4-mm rack pitch; s=4's 2.5-mm pitch cannot inherit this interface. Correlated deck warp, batch bias and common reader errors can affect entire banks; no iid yield claim.

**Stop this layout:** more resident moving bodies than the crossed-support control, no channel advantage once physical switching is charged, plus adverse depth/force. Reopening needs a different support/packing/retention topology, not a smaller rack.

## Simpler control: synthesize the stroke code, keep support resident

E-220's eight disjoint signed-delta groups travel 200 mm loaded and 200 mm empty per worst row. They need not be disjoint: a column can take several masked strokes, reseating on its resident combs between them. For five heights use positive **10,10,20 mm** and negative **10,10,20 mm** pulses. Select each cell by a subset summing to its signed difference; unchanged cells bypass every pulse; 30=10+20 and 40=10+10+20. Row travel becomes **80 mm loaded +80 mm empty**, with six rather than eight mask/support events.

For each pulse keep row support while fingers acquire/prove selected columns; withdraw their column bars, then the row comb. Nonselected cells remain on their column combs. Move selected fingers, reseat/prove row support, restore column bars, retract fingers and return empty. Column positions store all partial sums; the next mask does not have to remember captured grip heights. Replay checks support/invariance; affine interpolation proves no intermediate overshoot within each selected stroke.

Generator: sorted positive integer weights totaling L−1, `ceil(log2(L))` bits and complete subset coverage. A sorted next weight≤1+sum(previous) proves no holes; explicit subset enumeration cross-checks it. Search finds 1/3/60 bases for L=5/9/41 and minimizes rest-to-rest stroke time within this constrained family. This is **not global optimization over signed nonmonotonic schedules**. Five-level [1,1,2] attains minimum three binary decisions and minimum cumulative positive stroke four units. Other resolutions are scheduling sensitivity only; 1-mm shelves are not a manufacturing escape.

Use E-220's same **assumed total** group allowance g for physical mask write, selection, pickup, row withdrawal/reseat, readback and proof, plus actual feed: `cycle=2 sum_weights[2t(weight*40/(L−1))+g]+t(5.08)`. The same full-map/retry boundary applies; full overwrite is 38,400 binary mask commands/map.  At five levels:

| g per pulse | Minimum B in 1…80 | Bank selectors / pickup slides | Calculated time |
|---:|---:|---:|---:|
| .10 s | 6 | 480 / 480 | 28.256 s |
| .25 s | 9 | 720 / 720 | 28.504 s |
| .50 s | 16 | 1,280 / 1,280 | 26.902 s |

At g=.10, 9/41 levels need 560/720 selectors; at g=.25 they need 960/1,280. These cases owe finer support pitches. The six-bank five-level schedule leaves only **.01938 s extra per pulse** before 30 s. Five changed rows in one bank take 12.5024 s including one retry and global overhead, before extra nonadjacent seek. Worst concentration of 14 rows takes the full schedule. Other rows remain on their row comb; unchanged cells within an active row retain column support.

At B=6: per row 80 columns/160 guide stations, seven shelves/column, two resident support sites/column; per largest bank 1,120 columns, 14 row comb axes, 80 column selector bars and 80 reusable fingers; board **80 row axes +480 column axes**, 480 fingers, six lifts/arrests/carriages, 44,800 shelf levels and 12,800 bearing sites. No extra resident moving part per cell. Head/column-bar faults affect up to 1,120/14 cells. Moving selectors, support contacts, keepers and correlated frame error remain.

Inherited E-220 column stock is 8.192 L (152–455 h at 15–5 mm³/s) before head/frame and scrap. At 10 s per common support-axis placement 560 axes add 1.56 h; fingers, retained commands, assembly fixtures and calibration are extra. A 4/2-mm slot/tooth leaves .85/.65/.30 mm margin at the same e bounds. Opposing redundant support heights still allow **2e=.30/.70/1.40 mm** settling; six cycles create more exposure for a multi-pulse cell than a single-delta visit. No undisturbed-neighbor proof. Each loaded head carries up to 80/261.6/800 N at the 1/3.27/10-N scenarios. Arrest capacity, forced descent, retained selection and real read coverage remain unconstructed. Failure before support proof retains the last path; one detected retry is charged, structural failure/false proof requires a safe stop and service.

$250 reserved elsewhere leaves **<$.5208 per complete selector** at $500, or <$.3125 at $400; that must also pay its pickup coupling/retention share. The more explicit ramp-style $130+$65B shared allocation is already $520 at six banks before any selector purchases. These are assumptions, not prices. Thus **do not buy 480 actuators or begin finger/comb refinement**. Next construct a few shared physical writers serving 480 reusable retained binary bank-mask states, with explicit erase/write/feed, readback, command retention and support transfer inside the .11938-s pulse ceiling. Compare it against directly driven selectors at the same force and purchased budget. Stop if passive-mask retention merely recreates unaffordable channels or requires unqualified tiny repeated catches.
