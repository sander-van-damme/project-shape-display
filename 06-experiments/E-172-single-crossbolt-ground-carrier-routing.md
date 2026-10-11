---
status: complete
builds-on: [E-098, E-099, E-170, E-125, E-156]
---

# Single-crossbolt support routing survives contact but loses the matched schedule

**Park this embodiment; preserve its conditional support topology.** A travelling
crossbolt replaces separately selected pickup and ground sliders. Co-scheduling
cuts 32→20 scans, giving **19.723 s at 16 banks** with fixed-height transmission.
Matched five-height separate contacts take **13.422 s**, direct heads **6.892 s**.
A point writer reaching the keys through shared-Z motion takes **52.412 s**.
One fewer selector has not established a complete-machine advantage. No further
crossbolt guides/brake geometry, printing, purchases or machine selection.

Inputs `6af327f` / LAB-281 and extension `75b842d` / LAB-282. Reproduce:
`python3 tools/curated-experiment-checks/E-172/routing.py` and
`python3 tools/curated-experiment-checks/E-172/scheduling.py` (standard library).
Evidence: finite rectangular solids, quasistatic contact, deterministic bounds,
event/state replay and conditional timing/cost calculations; self-review only.
No physical measurements, process priors, sourced prices, qualified forces/rates,
complete fabrication CAD or independent validation. Generated output is omitted.

## Discovery and finite mechanism

Three distinct recombinations were screened against E-098/E-099/E-125/E-139/
E-150/E-156/E-166 and repository crossbolt/transfer-key/shuttle/make-before terms:

- Inverting selector ownership produced the new-here column-carried transfer key.
- Always-coupled traction plus a ground dog removes pickup selection but repeats
  E-150/E-156 preload/wear/drag: equal slip traction F across 6,400 locked sites
  dissipates `6400 F L` = 51.2/512/5,120 J over 80 mm at .1/1/10 N. Different
  static/kinetic traction changes this scenario; it is not a thermal limit.
- Common pressure plus ground latch repeats A-020/E-064 seals, returns and
  selectors. One-pitch piston area ≤25.8064 mm² requires ideal pressure
  ≥3.88/38.8/387.5 kPa at those loads, before walls/seals.

Only the ownership inversion produced a new combination here; no literature
novelty or saturation claim. Loads are scenarios, not product requirements.
Existing screws, pawls and direct heads remain controls/other leads; embodiment
failures do not reject whole principles.

Five levels are `j*10.1 mm`, j=0…4: 40.4-mm nominal travel, ≥40.3 mm after
independent ±.05-mm endpoint errors. Periodic seats retain E-170's common-datum
pickup. A 3.4×1.6×.8-mm key shifts laterally between q=−.7/0/+.7 mm (G/B/C).
Fixed shelves occupy x=−2.3…−1.4, carrier shelves x=1.4…2.3; both y=±.8,
1-mm thickness below planes `j*10.1+g_j` and `j*10.1+c_j+d`. Key horizontal
prismatic joint and moment-reacting column guides are ideal. No cap rotates.

Ladder spines, key guides, retained three-state selection, writer access and bank
arrest are unbuilt. Disjoint shelf footprints do not prove connected-ladder
clearance. Key sweep is 4.8 mm on 5.08-mm pitch; 4.6-mm cap is only an envelope.
Carrier shelves sweep **122.6 mm vertically** over ±40.4-mm displacement plus
preload, before frame/caps/brakes/service space. Two-position actuation does not
supply three retained states.

For errors `g_j,c_j ∈ [−e,e]`, e=.05, choose `a=2e+.1=.2 mm`. With old=o,
target=t and Δ=(t−o)*10.1, the complete isolated route is:

1. At d=−a shift G→B, carrier below the grounded key.
2. Raise d to +a: key height is `max(o*10.1+g_o,o*10.1+c_o+d)`; shift B→C
   only after carrier acquisition and ground unloading.
3. Move d to Δ+a, entirely clear of fixed shelves; shift C→B.
4. Lower d to Δ−a: height is `max(t*10.1+g_t,o*10.1+c_o+d)`; prove ground,
   shift B→G and return d to −a. G keys remain x-disjoint from carrier shelves.

`routing.py` covers **1,024 height-error sign patterns × 20 ordered pairs =
20,480 routes / 983,040 poses**, positive contact and reaction sums at .1/1/10 N,
plus nonsymmetric 4/16/64-subdivision holdouts. Every contact/lateral-overlap
breakpoint and interval midpoint is included. Affine geometry, x separation and
**7.8-mm upper-shelf clearance** bound intervals. Ideal guides react moments;
this is quasistatic downward support, not dynamic lowering or signed-load proof.

## Manufacturing bounds and irreplaceable failures

Independent key registration, key half-width and facing shelf-edge errors ±e
give bridge overlap `.3−3e`, off-clearance `.4−3e`, neighbor-key gap `.28−4e`.
Corner enumeration confirms these, including opposing local/coherent bank errors:

| e mm | Bridge overlap mm | Off-clearance mm | Neighbor key gap mm |
|---:|---:|---:|---:|
| .025 | .225 | .325 | .180 |
| .050 | .150 | .250 | .080 |
| .075 | .075 | .175 | −.020 |
| .100 | 0 | .100 | −.120 |

At e=.075, opposed selected key solids actually overlap **.0256 mm³**. At .05,
bearing area ≥.225 mm² implies mean pressure .444/4.44/44.4 MPa at .1/1/10 N;
no material allowable or strength pass. Breadth includes ±e face errors with
ideal alignment. Warp, tilt, hole shrinkage, first layer, roughness/friction,
layer anisotropy, guide play, creep, fatigue, wear and coupled bending remain
unmodelled. These are bounds, not calibrated X1C priors or yield distributions.

A flat d=0 handoff fails both mismatch signs: +.05 gives **.024 mm³** bridge
penetration; −.05 leaves a .05-mm fall after donor release. Bridge/unload is
functional for this rigid section. Ramps/compliance require different physics.
Missed B→C leaves the next fixed shelf in the key path: at d=9.5 intersection
is **.288 mm³**. An unchanged key falsely accepted as G while actually B rises
**.5 mm** at d=.5. These failures are preserved in executable source.

## Co-scheduled event/state comparison

All families use the same five heights. Every row repeats all 20 unequal pairs
four times. Membership logic accepts arbitrary maps, including empty groups and
identities; the dense workload is not a universal optimum/worst-time proof.

For each sign, acquire all its changed cells together at home through G→B,
`−a→+a`, B→C. Visit nonempty signed differences in increasing magnitude. At Δ,
move to Δ+a, shift only that group C→B, lower to Δ−a, prove ground and shift
B→G. Remaining C cells follow every microstroke. All are grounded before return
to −a and the opposite sign. Positive-going cells awaiting later targets descend
.4 mm at earlier depositions before rising again; no support is replaced by a
command bit. Two acquisition plus eight deposition writes per sign give
**20 scans / ten group proofs**, versus the former 32 scans / 16 proofs.

`scheduling.py` replays **64 coherent/anticorrelated level-error patterns /
674,825 key poses**, nonsymmetric 1/4/16-subdivision holdouts (11,775/17,775/
41,775 poses), all 625 two-cell maps, every shared return and identity support.
Shift and shared-motion checks include finite shelf/key contact/collision
breakpoints. Prior isolated-route coverage and affine bounds apply per cell;
different cells may have different admissible errors. This does not model elastic
bank coupling. No identical-independent-cell or reliability inference follows.

Matched separate-contact control: E-098's pad set, five ascending old-dog
releases, five descending target-dog insertions, pad clear = **12 scans**.
Deck path is −2→old+2→45.4→(target+2,target)→−2 mm. New contact-interval replay
uses five 10.1-mm-spaced teeth, all 32 tooth-error patterns × two dog errors ×
two lip errors: **374,400 poses** of all carried/grounded cells. Tooth/dog bounds
are ±.05 mm; lip=.95/1.05 mm. Separate Y lanes and unloaded slider sweeps retain
E-098's section assumptions. This does not supersede its broader error study.

Direct control grants a bilateral head: home→old, grip, lift .2 mm to unload
ground, move to target+.2, reinsert ground, descend .2, release and return home.
Eighty independent heads serve each row; its slowest path governs. Both transfers
and one full adverse-row retry are charged. This is a load-path/trajectory grant,
**not new head geometry**; E-123/E-125 capture failures remain applicable.

## Addressing, complete time and cost

Two causal routes prevent arbitrary-height access being silently free:

- **Shared-Z point forks:** an 80-finger bar traverses rows/height tiers, approaches
  a y-facing key feature from a service aisle, shifts q, reads and withdraws
  before any row/Z/carrier motion. Even granting aisle/fork clearance and error
  capture, settings number `2[2×4+2(4+3+2+1)] = 56` per row. Source charges
  height-major serpentine moves, stopped Z travel and final row/Z home. This
  counts this point-height schedule, not a bound on every writer topology.
- **Fixed-height tongues:** extend each key downward with a vertical command
  slot spanning ≥40.4 mm plus engagement/error reserve. A fork at one fixed
  service datum engages lateral slot walls to shift q, then withdraws; the
  tongue travels vertically with its column. No second retained selector or
  independent Z actuator is logically required. But 6,400 long transmissions,
  guidance, compliance, forces, retention and shelf/spine clearance are unbuilt.
  The favorable 20-scan result grants this access inside each write slot.

A full-height fork similarly buys extended transmission structure, not free
point access. Separate contacts retain E-098's favorable home-pad/fixed-dog
writer grant. Missing interfaces must fit each family's allowances.

Central allocations: 200 mm/s, 5,000 mm/s²; .1 s per complete row write and
bank proof; 2 s preparation/registration/final settlement. Writing includes
approach, retention, reading and withdrawal; motion does not overlap it. Recovery
budgets one write repeat plus up/down reseat (.4 mm key, 2.2 mm separate) and
proof; direct repeats an adverse row. Parallel bank proof remains unqualified.
Persistent/false-read faults or loss of arrest are not successful completion.

| Banks | Fixed-height key s | Shared-Z key s | Separate contacts s | Direct heads s |
|---:|---:|---:|---:|---:|
| 1 | 265.347 | 740.160 | 160.797 | 69.776 |
| 2 | 134.347 | 373.361 | 82.197 | 36.238 |
| 4 | 68.847 | 189.962 | 42.897 | 19.469 |
| 8 | 36.098 | 98.262 | 23.247 | 11.085 |
| 16 | 19.723 | 52.412 | 13.422 | 6.892 |

Independent hand sums reproduce both shared-family dense times. The original
independent-group **30.942-s/B16** result remains in `routing.py`, superseded as
a constructive schedule failure, not an architecture lower bound. Across slow
80/1,000, central and fast 400/20,000 motion with matched .02/.05/.1/.2-s
write/proof slots, fixed-height keys never need fewer tested banks than separate
contacts; some tie. Shared-Z passes only central .02-s or fast .02/.05-s at B16.
Four extra overhead seconds preserve the central key pass, not the ranking.
No global optimality: held-contact writers or overlapped motions are not optimized.

Local test: five rows × five columns, old zero, targets 0…4 (20 changed cells).
All 76 vertical placements at B16 give **7.710–10.985 s key**, **8.380–11.655 s
shared-Z**, **6.732–9.075 s separate**, **5.055–6.652 s direct**. Column-location
symmetry assumes 80 healthy independent channels. Unchanged supports stay
engaged through common motion/return; vibration and actual displacement are unproved.

Common purchased boundary: <$500, with $250 reserve and bought cell items charged
additionally. Key/separate count 82B complete setting/row/lift bundles; shared-Z
83B; direct 81B complete head/row bundles. Different functions must be paid: a
head includes drive/capture/ground handling/sensing, not merely a motor. Brakes,
guides, power, wiring/readers must fit reserve or bundle/site costs. At smallest
central passing B=16/8/4, key/separate/direct need 1,312/656/324 bundles and
mean ceilings **<$0.19055/$0.38110/$0.77160** with free bought sites.

Key removes 6,400 independent pickup selectors but adds long transmissions and
retains **12,800 five-seat ladders / 64,000 shelves**, guides and three-state
retention. At equal complete-bundle cost c it must save **>0.1025c per cell**
against separate contacts to offset its extra 656 bundles, before other costs.
At key B16, $.02 bought/cell reduces its allowance to **<$0.09299**;
$.05/cell plus the reserve already exceeds $500. These are tradeoff thresholds,
not prices or whole-product domination. One 10-s assembly operation/site takes
17.8 h; print material/time/scrap, calibration, service and life remain unpriced.

## Support limits and technical disposition

Four retained-setting observations and two support proofs per changed key still
mean **38,400 individual proof opportunities** on a dense map. Common reader
bias can defeat many cells; no false-accept probability or independent retry is
known. With ±.05-mm shelf errors, unload clearance has only .1-mm reserve.
An adverse **+.11-mm common carrier-position error** leaves carrier contact
**.01 mm above ground** at the deposition proof; finite pose checks reject G
release. Applied throughout, that bias already collides at initial bridge entry.
False acceptance would release support. Increasing a for drive uncertainty requires new clearance/time accounting.

Carrier-only input loss leaves a free collective coordinate. A 400-cell bank
requires arrest of **40/400/4,000 N** at .1/1/10 N/site plus carrier weight.
Retained key commands cannot brake it. Grounded arrest, excursion/energy, dynamic
lowering, force tails, creep and wear remain unqualified; retry time supplies none.

Stop guide/retainer/brake refinement for this crossbolt embodiment. Preserve the
supported topology and negative evidence; co-scheduling helps the old protocol
but has not shown an advantage over matched controls. Reopen on an executable
access/schedule removing visits or evidenced complete-bundle/site costs crossing
the threshold. A second resident selector is not inevitable: the tongue is a
causal alternative with unresolved repeated structure. No printing or purchases.
Redirect sharing exploration toward **passively sequenced grounded release/capture
that removes writer visits**, comparing both controls and cross-checking existing
pawl/cam families. A renamed latch or faster assumed writer is insufficient;
the broader sharing axis remains unsaturated.
