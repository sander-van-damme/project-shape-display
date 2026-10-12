---
status: complete
builds-on: [E-221, E-156, E-194, E-126, E-130, E-109]
---

# Shared drive saves motors, but supported switching consumes channels and budget

**Stop these drive/feeder embodiments before local refinement.** Stopped shared
shaft: **400 channels / five heads / 27.269 s / assumed $807**. Catalog independent
actuators alone: **$950.40 at 240 channels**. A common hydraulic shutoff cannot
retain individual positions. Flat-spacer exchange: **640 forks + 640 shuttles +
25,600 tokens**. No selected machine, physical qualification, print or purchase.

Input main `45bb21f`. Reproduce:
`python3 tools/curated-experiment-checks/E-222/screen.py` (stdlib, stdout).
Evidence: **mechanism hypotheses, ideal state replay, necessary-condition
calculations, labelled bounds and supplier listings**. Self-review; no finite
assembly/contact CAD, calibrated process data or measurements. Five comparison
heights 0/10/20/30/40 mm are not a product resolution decision.

## Complete transactions before component detail

Common to the first three routes: E-221's resident row comb holds 80 simple
shelved columns. With comb still grounded, shoes rise from −5 mm to **measured
old heights**, prove contact and retention individually, then the comb withdraws.
Shoes carry the mixed old→target move; unchanged shoes stay at old height.
The comb reseats at all targets; actual height and supported deposit are checked
before empty shoes reset to −5 and the head indexes. A failed acquisition keeps
the comb; failed deposit keeps the arrested head. A jam is a safe service stop,
not an invented successful recovery. Every visited row transfers all 80 columns,
even for one changed cell. Other rows remain mechanically supported.

Complete routes, all with the common transaction above:
- **Independent screws:** private motor→screw/nut→shoe, with grounded thrust
  reaction, guide and brake. Catalog motors fail cost before local development.
  Static self-locking does not establish moving arrest (E-156/E-194).
- **Shared shaft:** one reversible motor/head; independent retained coupling
  and parking dog per axis. A common normally applied shaft brake holds coupled
  shoes; parking dogs hold disconnected shoes. Sequence below.
- **Shared pressure:** head-owned piston shoes, each with normally closed fill
  and exhaust paths. Closed valves trap fluid against cylinder/head; gravity
  lowers. Independent valves, seals and closure response remain necessary.
- **Flat stacks:** replace shelves/comb/absolute axes with follower→0…4 identical
  10-mm spacers→fixed floor. Selected fork plus arrested common lift supports
  upper stack during bottom-block exchange; parked state needs no moving latch.

**Shared-shaft sequence:** with shaft stopped/braked and parking dog engaged,
engage/prove coupling, retract dog, move; stop/brake shaft, insert/prove dog,
release coupling. Other coupled axes remain grounded through the shaft brake.
Power loss during motion requires **mechanically retained coupling state**: a
spring-open clutch would sever support before braking. Shaft fracture is outside
that protection. Brake, coupling phasing, overlap interlock, reader, torsion and
docking assembly remain unconstructed.

All 15,625 three-cell old/target replays maintain parking dog OR retained coupling
to brake through acquisition, signed moves, deposit and reset. This is a
**conditional support-graph invariant**, not brake/contact qualification; a
false reader or disconnected shoe defeats it. A continuous-shaft alternative
needs controlled friction clutch/brake transfer per axis. Two counter-rotating
sources recover mixed-direction concurrency only with ≥480 drive couplings plus
240 parking functions at 240 axes; neither inherits the stopped-dog proof.

**Hydraulic counterexample:** two equal-area cylinders behind one closed supply
valve can move (−1,+1) mm without changing fluid volume. Loads (10,1) N release
.009 J along this mode. Independent isolation is essential. Head-owned circuits
avoid E-109's 6,400 resident wet circuits but retain valves/seals. Assumed 50-mm²
pistons at 200 mm/s require **48 L/min/head** peak for 80 rising shoes, at ideal
20/65.4/200 kPa for 1/3.27/10 N loads. Smaller area trades flow for pressure.
Leakage .01/.1/1 mm³/s gives .006/.06/.6-mm drift in 30 s: diagnostic bounds,
not measured leaks or acceptance limits. Pump, accumulator, seals and shutdown
response are unresolved. [Clippard's pilot-check explanation](https://www.clippard.com/cms/wiki/how-do-pilot-operated-check-valves-work)
supports separate check/pilot functions in pneumatics, not liquid compatibility,
miniature-channel price or display qualification.

**Spacer transaction:** unlike E-126's eleven spheres, use four flat 10-mm
blocks. Unlike E-130's rolling wedge, a separate fork on a braked common lift
supports the stack. At the fixed bottom station, select/retain the fork, lift
the upper stack, exchange the bottom block with a selected shuttle, lower onto
floor/new block, prove actual height and support, then retract. Insertion
reverses the sequence. Zero-height followers need the same pickup shoulder as a
block. Unchanged lanes stay on their floors. Midstroke source loss requires lift
brake AND retained fork selection. Fork slots, feed past neighboring stacks,
empty storage, singulation and return are unconstructed; the schedule cannot
re-admit E-130's failed routing by assuming these away.

## Full-scale replication and service ledger

Counts are functions, including those printed monolithically. For absolute routes,
B heads each visit at most ceil(80/B) rows; a row has 80 cells. Hydraulic counts
below optimistically use E-221's B=3 timing, not a flow-qualified schedule.

| Function | Per cell | Per row | Per head / largest bank | Board |
|---|---:|---:|---:|---:|
| Absolute-route moving columns / guide stations | 1 / 2 | 80 / 160 | 80ceil(80/B) / twice that | 6,400 / 12,800 |
| Shelf positions / active comb bearing contacts | 5 / 1 | 400 / 80 | 400ceil(80/B) / 80ceil(80/B) | 32,000 / 6,400 |
| Resident comb / keeper / frame seat | shared | 1 each | ceil(80/B) each | 80 each |
| Independent screw axes / nuts / brakes / motor channels, B=3 | shared | 80 each during visit | 80 each / 2,160 resident cells | 240 each |
| Shaft route axes / nuts / couplings / parking dogs / command selectors, B=5 | shared | 80 each during visit | 80 each / 1,280 resident cells | 400 each |
| Shaft route motor / shaft brake / distributed drive train | shared | shared | 1 each | 5 each |
| Shoe linear bearing stations / thrust reactions, screw routes | shared | 160 / 80 active | 160 / 80 | 480 / 240 independent; 800 / 400 shaft |
| Hydraulic pistons / sliding seals / fill+exhaust seats, B=3 | shared | 80 / ≥80 / 160 active | 80 / ≥80 / 160 | 240 / ≥240 / 480 |
| Flat tokens / follower / guide stations | ≤4 / 1 / 2 | ≤320 / 80 / 160 | ≤3,200 / 800 / 1,600 at B=8 | 25,600 tokens total / 6,400 / 12,800 |
| Spacer grounded floor sites / maximum stack interfaces | 1 / 5 | 80 / 400 | 800 / 4,000 | 6,400 / 32,000 |
| Spacer retained selection forks / token shuttles, B=8 | shared | 80 / 80 active | 80 / 80 | 640 / 640 |

Add transport, retained dock, comb operator or spacer lift, reader and energy
routing/head. Shaft route has ≥400 selector return/retention assemblies, ≥800
switched support interfaces, ≥400 screw wear pairs and 800 linear bearing
stations. Extra journals, meshes, fixtures, springs and fasteners are unknown,
not zero. Linked clutch/dog operation still has two contacts. Hydraulic seats
need 480 closure functions even if one actuator sequences a pair. Spacer forks
and shuttles remain 1,280 conditional moving functions despite shared commands.

Assembly: 6,400 column insertions; shaft route adds ≥400 axis placements,
≥400 coupling/dog assemblies and calibrations, 80 combs and five heads. Spacer
route adds 25,600 inspected/loaded tokens, 640 forks and 640 shuttles. An all-low
map requires storage for every token. Head outage immobilizes its bank; comb
failure exposes 80 cells. Buried guides/media require temporary supported access.
The 406.4-mm frame needs modules on the 256-mm bed.

Printed allocation: retain E-221's **4.608-L column-stock control**, plus shelves,
12,800 guide stations, 80 combs/keepers and frames. An assumed 1–3 cm³ per
shoe/nut/coupler/dog bundle adds .4–1.2 L at 400 channels, excluding head frames.
Spacer allowance 3.4×3.4×10 mm gives **2.959 L**, plus follower stock, sleeves,
feeders and storage. At assumed effective 5–15 mm³/s and 10% scrap, column stock
alone takes **94.8–284.4 h**; column+token stock takes **155.7–467.1 h** before
other parts, finishing or assembly. Slots/hollowing change strength/volume, not
piece count. Bearing faces, sliding surfaces and fork layer orientation need
constructed geometry; these are neither slicer estimates nor total print times.

## Timing: count the supported transactions

Use E-221's optimistic v=200 mm/s, a=8,000 mm/s² and rest-to-rest t(d).
Two global seconds allocate map reception/processing, initial registration,
per-map reference checking and final proof/settling. u=.10/.25/.50 s per row
allocates command loading, contact/height scan, comb withdrawal/reseat and proof.
These are **assumptions**, not measured electronics/mechanics times. Add a feed
stroke t(5.08) for every visit and one full row retry in the critical bank:
`T=2+(ceil(80/B)+1)[S+t(5.08)]`. All preparations start after receipt.

| Route | Row service S, before feed | First B at u=.10 / axes or lanes | T / three-bank T |
|---|---|---|---|
| Independent ideal arrest | 2t(45)+t(40)+u | 3 / 240 | 26.511 / 26.511 s |
| One-direction-at-a-time continuous couplings | 2t(45)+2t(40)+u | 4 / 320 | 25.108 / 32.811 s |
| Stopped dog transfers | 2t(5)+16t(10)+18(.002)+u | 5 / 400 | 27.269 / 43.619 s |
| Flat-spacer four-stroke feeder | 8[2t(10)+2t(5.08)+.020]+u | 8 / 640 | 27.485 / 66.870 s |

Stopped shaft: five acquisition stops, four per rewrite direction and five
reset stops. The 2-ms engagement/proof/release allocation is unqualified. A row
with 0→10/20/30/40, 10/20/30/40→0 and unchanged 20 demands all distances.
u=.25 gives 29.819 s at five heads; u=.50 needs seven / 560 axes / 26.523 s.
Friction switching might remove stops but needs per-axis moving support transfer.

Spacers require four insert plus four remove cycles in a worst mixed row, each
with 20-ms proof. Two vertical and two lateral strokes/unit favorably omit extra
fork/inventory motions. This rejects the **defined feeder**, not all continuous
or independently reversible feeding. Worst-map token transfers remain 25,600.

Absolute routes require 12,800 old/target words, 6,400 acquisitions and target
checks, 80 comb release/deposits and 6,400 returns. Motor position does not prove
support; camera occlusion and underside support-reader coverage remain unsolved.
Regional time uses the maximum visited rows in one bank plus actual seek.
Unchanged cells in a visited absolute-head row experience takeover; spacer lanes
ideally bypass it, subject to feed routing. One recoverable row retry is budgeted;
source loss, jam or false acceptance has **no <30-s recovery guarantee**.

## Bought allocation and functional uncertainty

Supplier observations, 2026-10-12, USD before tax/freight:
[Adafruit 858 stepper](https://www.adafruit.com/product/858) and
[2776 spring-return solenoid](https://www.adafruit.com/product/2776) list **$3.96
at 100+**: **$950.40 for 240 bare motors OR selector solenoids**. Stop these
procurement routes; listings neither prove lowest market price nor qualify
speed, clutch force, brake or complete channel.

Make E-221's reserve explicit using **optimistic allocations, not quotes**:
controller15 + supply/protection25 + frame/datum35 + comb/keeper hardware16 +
common harness14 + freight/spares25 = **$130**. Per head: transport motor/driver/
belts/bearings20 + dock/operator5 + reader/light15 = **$40**. Shared shaft adds
motor/driver12 + brake8 + shaft/journals5 = **$25/head**.

Per channel: hypothetical motor or selector **$.35**, drive/wire **$.12**,
screw/thrust stock **$.18**, brake/return hardware **$.10**, sensing share **$.08**,
fasteners **$.05** = **$.88**. Printed nuts/dogs/couplings and stock are additional.
These exceptionally low placeholders buy no demonstrated speed/force/support.

| Allocation | Independent 240 | Continuous signed 320 | Stopped dogs 400 |
|---|---:|---:|---:|
| Non-channel reserve | $250 | $390 | $455 |
| Remaining complete-channel cap under $500 | <$1.042 | <$.344 | <$.113 |
| Custom $.88/channel total | $461.20 | $671.60 | $807.00 |
| Even with free motor/selector, $.53 remainder | $377.20 | $559.60 | $667.00 |
| Catalog actuator + same $.53 remainder | $1,327.60 | $1,826.80 | $2,251.00 |

Only the hypothetical independent route fits the last-resort tier, without a
qualified cheap actuator/arrest. Shaft allocations fail before local engineering.
They are not universal price floors: halving every stopped-route allowance gives
$403.50; keeping its $455 reserve needs <$.1125/complete channel. Reopen with a
credible sourced/manufactured allocation, not free printed mechanisms. No invented
favorable hydraulic/media BOM follows their earlier support/handling failures.

Manufacturing scenarios: E-221's combined e=.15/.35/.70-mm bounds leave shoe
lateral margins .55/.35/0 mm and permit .30/.70/1.40-mm takeover motion.
These are not X1C statistics. Shaft twist, sag, batch bias and reader zeros
correlate errors; more heads multiply alignment jobs. An ideal 4-mm mean-diameter
square screw self-locks statically only if lead <πdμ: .628/1.257/2.513 mm at
μ=.05/.1/.2. Leads 1/2/8 mm need 12,000/6,000/1,500 rpm at 200 mm/s. These
calculations are not PLA priors or moving-arrest evidence; E-156/E-194's source
inertia failures still apply. A 1/5/20-ms brake delay alone adds .2/1/4 mm before
deceleration/backlash. The head carries 80/261.6/800 N at 1/3.27/10 N per cell;
40-mm rise requires 3.2/10.464/32 J ideal work. Shaft transmission losses and
gravity following retain E-221's unresolved limits.

Spacer common height bias e=.05/.15/.35 mm accumulates to **4e=.2/.6/1.4 mm**,
without independent-error averaging. Wear, creep, bow, debris and first-layer
growth also affect bearing faces and feed slots. No process yield follows.

## Decision

Shared motors raise this favorable stopped-channel count from 240 to 400 while
retaining two support interfaces/channel. Do not start clutch/dog/shoe refinement.
Keep the supported-shaft sequence as a comparator, not a selected machine.
Independent hydraulic isolation and mid-transfer spacer support are also mandatory.

Next invention target: **fixed-datum, continuously supported solid-media exchange
with fewer stopped transfers**. It must escape E-130's upstream-stack routing and
free-input support failures and this result's 640-lane/25,600-token burden. A
reusable encoded support carrier may beat loose tokens, but must include arbitrary
rewriting, return and storage. Stop at the first missing path or failed full-scale
bound; no survivor has earned printing.
