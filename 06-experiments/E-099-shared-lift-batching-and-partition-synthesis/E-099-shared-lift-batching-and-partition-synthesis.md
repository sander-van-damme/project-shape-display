---
status: complete
builds-on: [E-098, E-094, A-013]
---

# Smaller shared-lift packets exchange pickup count for slower updates

**Park serial rack-dog writing as the active machine direction.** Splitting a
bank into lift packets does not rescue its full-map timing at unchanged writer
count. Resident parallel writers buy time almost entirely by multiplying data
channels. A moving row comb offers fewer pickup members, but no demonstrated
complete-system advantage over direct heads. Preserve that conditional tradeoff
and its reopening budget; do not refine or print another rack/deck interface.
This is an exploration-allocation decision, not an impossibility or priced
rejection of all shared lifting.

Input main `7998420`. Reproduce:
`python3 tools/curated-experiment-checks/E-099/grouping.py`.
Evidence: deterministic schedule synthesis, analytical partition bound and
self-review. No new generated dispatch geometry, manufacturing measurements,
priced components, qualified actuators or hardware. E-098's translational
contact box remains conditional on ideal guides and retention; it does not
qualify a moving comb passing between rows. Generated JSON is not retained.

## Mechanisms and search representation

The generator changes **energy/selection grouping**, not tooth dimensions:

| Layout | Shared motion and setting | Repeated burden / new missing mechanism |
|---|---|---|
| Full-bank deck | One deck; one 80-channel writer scans every old and target group | 6,400 deck pads and ground dogs; E-098 dual-plane writer and retainers missing |
| Moving packet, g rows | Finish pickup, all old releases, all target insertions, load proof and pad clearing for one packet; move packet and writer to next block at home | 80Bg carried pads, 6,400 ground dogs; retracted comb must pass stationary columns and engage next rows; packet guides, registration and safe dispatch ungenerated |
| Resident writers | W contiguous row subbanks each have 80 setting channels and a row axis; share one larger deck | 6,400 pads/dogs; deck reacts summed load, writers synchronize; more parallel wiring/readers |
| Direct heads | Independent home→old→target→home positioning, grounded supports, row scan and return | E-094 comparator; grip/release/readback and complete head price still unqualified |

B={1,2,4,8,16}; n=80/B. Enumerate all integer g=1…n, including a shorter last
packet: **155 grouping variants**, not 155 operating principles. g=1 is a row
comb whose pickup selection stays on the reusable head. g=n recovers E-098.
For intermediate g the budget charges an additional packet-dispatch axis;
for g=1 the writer/comb share row transport. No extra actuator is hidden in a
claim that splitting fixed decks is free: this embodiment uses moving packets.
A fixed segmented deck with shared drive would instead need positive coupling
and isolation, absent here and unable to improve the favorable serial bound.

Full workload repeats all 72 nonidentity old/new pairs across 80 columns of
every row. Thus each row needs all nine old releases and nine target insertions.
Local workload changes a flat 5×5 patch to five heights. All 76×76 positions
are covered using explicitly checked column symmetry: 80 independent setting
channels make every horizontal translation have the same active level sets;
all 76 vertical starts are evaluated. This symmetry does not establish physical
column packing or equal edge stiffness. These are adverse workloads, not a proof
of worst time over every sparse arbitrary map.

Each packet uses E-098's finite waypoints: −2 → increasing old+2 → 45 →
(descending target+2, target) → −2 mm. Return the within-packet writer to its
first row before packet dispatch. Charge stopped dispatch, internal serpentine
scans and final return to bank home. No overlap is credited. Pad/dog slots must
include setting, retention, approach/withdrawal and individual readback. Support
slots must prove pickup/deposition, not merely shared deck height. A failed
proof stops motion while supported; one in-situ dog-slot retry plus one
2.2-mm up/down support retry is budgeted. Persistent faults do not become a
successful update through a timing allowance.

Central assumptions: v=200 mm/s, a=5,000 mm/s², pad/dog/proof slots each .1 s,
2-s preparation/registration/final-settling reserve. Motion alternatives are
80/1,000 and 400/20,000; dog slots .02/.05/.1/.2/.5; support slots
0/.05/.1/.2 s (zero is a favorable bound). Unknown additional packet coupling
is initially free, with its remaining margin exposed below. These are competing
bounds, not calibrated rates or manufacturing distributions. Correlated slow
axes, registration errors and shared proof bias do not average away.

## Partition bound and calculated results

For k contiguous packets covering n fully active rows, internal scanning costs
`20(n−k) move(5.08)`, while each packet repeats the complete deck itinerary D
and 18 support proofs. Dog and pad slot counts remain **18n and 2n**. Relative
to one packet, excess time is

`(k−1)[D + 18 proof − 20 move(5.08)] + packet dispatch/return`.

The bracket remains positive even with **zero** support-proof time:
.396770/.177441/.088720 s for slow/central/fast motion. Consequently **every
contiguous serial partition** is slower under these motion laws, including
unequal groups and ideal free coupling. This bounds all 2^(n−1) partitions;
it is not a universal result for overlapping machines, different acceleration
laws, automatic rack release, or a materially changed support topology.
An exact dynamic program over arbitrary partitions and a separate 128-partition
eight-row enumeration agree. No stochastic seed or solver tolerance is involved.

| Banks | Full-bank deck s | Row comb s | Direct s |
|---:|---:|---:|---:|
| 1 | 266.261 | 429.561 | 67.403 |
| 2 | 135.261 | 215.898 | 35.037 |
| 4 | 69.761 | 109.066 | 18.854 |
| 8 | 37.011 | 55.651 | 10.762 |
| 16 | 20.636 | 28.943 | 6.717 |

The B=16 time/pickup-count frontier retains g=1/2/3/5, respectively
28.943/24.914/22.846/20.636 s and 1,280/2,560/3,840/6,400 pads. g=4 loses to
g=3 because both require two excursions. This is a two-axis **conditional**
frontier, not a whole-product or feasible-machine Pareto set. Ground dogs/racks
and their retention remain 6,400; reducing pads does not eliminate the supports.

B=16 row comb leaves **1.057343 s** total margin, or **.211469 s per packet**
for equal added work across its five rows. Raising map overhead from 2 to 6 s
makes it **32.943 s**. Its dog slot ceiling is **<.111619 s**, with other grants
fixed; B=8 fails even with instantaneous dog slots. At .1-s proof and .02/.05/
.1/.2/.5-s dogs, minimum passing tested central bank counts are respectively
8/8/16/16/none for full deck, 16/16/16/none/none for row comb. The slow row comb
fails through B=16 even at .02-s dogs; fast still needs B=16 for .1-s proofs
at the three smallest dog slots. Direct's tested minimum is B=8/4/2 under
slow/central/fast motion with .1-s proofs. None of these accelerations is a
qualified loaded-machine capability.

Central B=16 local times are **9.439–14.242 s row comb** versus
**7.216–9.836 s bank deck**; B=4 row comb is 9.439–15.044 s. Local tests also
cross all three motions and .02/.1/.2-s dog slots. Unchanged cells never receive
an intentional unlock/lift command. No vibration, comb sweep clearance,
miniature stability or physical non-target displacement is established.

Resident writers do not remove the 18 per-row writes. With BW=16 total writers,
full timing is 20.636 s under the same grants and channels total `81BW+B`:
1,297 for one shared deck versus 1,312 for 16 independent decks. Saving only
15 lift channels retains all 6,400 pads and concentrates load/common faults.
Sparse timings from independent subbank decks are only optimistic bounds for a
shared deck with the union of their old/target stops. No exact regional speed
claim is inherited from the full-map equality.

## Complete budgets, limits and disposition

A B=16 row comb needs at least **1,312 complete shared setting/transport/lift
channels** under the favorable dual-plane grant. With $250 elsewhere and no
bought cell items, the mean channel must cost **<$0.19055**; $0.02/cell reduces
this to **<$0.09299**. One deck/16 resident writers improves the free-cell
allowance only to **<$0.19275**. Separate pad and dog actuation, guides,
registration, wiring, reader, power and structure must be paid, not assigned
zero cost. Source crosses reserve $150/250/400 and cell purchases $0/.02/.05;
negative allowances are budget rejection. No quote or economic impossibility
is inferred. Central B=4 direct heads have <$0.78125 per complete head with
shared transport in their reserve; these are different functional bundles.

The row comb can remove 5,120 persistent pickup pads at B=16 and reduce moving
column count per lift to 80. It also needs repeated row entry at 5.08-mm pitch,
1,280 active pickup channels and the same 6,400 rack/dog supports. At least
38,400 individual proof opportunities remain for a full map (E-098's six per
changed cell), plus carriage clearance/registration. No independent readback or
retry credit is granted against a common offset. An unconditional per-proof
false-accept bound would still propagate through a union bound; none is known.
No print-time, lifetime, strength, mass or assembly yield is manufactured from
these operation counts. Dispatch cannot inherit E-098's stationary contact
clearance or 146-mm envelope without new swept geometry.

Stop partition optimization: it cannot remove this embodiment's time/channel
bottleneck. Retain the time/pad tradeoff as a reopening target, but it does not
justify another guide/retainer study ahead of a materially changed addressing
principle. Reopen with automatic/passively governed support release/capture
that removes visits, or a finite complete cheap writer with real dispatch,
retained isolation and proof/recovery meeting these recomputed budgets. Faster
unqualified motion or an assumed perfect reader is insufficient. No fabrication
or purchased hardware follows. The campaign's finite pickup/stop failures and
system grouping question now have scoped outcomes; the research program remains
open and direct heads remain a comparator, not a selected product.

Self-review: 60 full-map E-098 reference cases, independent row-comb leg sum,
zero-work limit, exact partition DP at three motions, 128 brute partitions,
5,776 patch placement checks, and full/local slot/motion sensitivities. Existing
E-098 geometry replay is retained as subsection evidence. Checks of these
models do not prove manufacturing or hardware performance.
