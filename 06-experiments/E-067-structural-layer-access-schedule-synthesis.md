---
status: complete
builds-on: [A-022, E-063]
---

# Structural-layer drive-access schedule synthesis

**Retain fixed-reference drives for a geometry test.** A-022's need for
lower-offset-following drives is conditional on its update protocol. Clear
all bits of **changed columns only**, least-significant layer first; then set
target bits most-significant first. Every commanded layer now has zero lower
binary displacement while it is driven. Unchanged columns keep their complete
state. This removes one access obstruction without proving dog clearance,
selection, load support or an affordable machine.

Input main `b07fb0d`. Reproduce:
`python3 tools/curated-experiment-checks/E-067/access_schedule.py` (standard
library); `--all` emits all protocols and first rejection witnesses. Evidence
is exhaustive discrete synthesis and a motion-budget calculation, not CAD,
contact simulation, physical measurement or manufacturing yield. No random seed.

## Generator and counterexamples

Three structural stages have 10/20/40-mm binary strokes. A layer-i drive
acquires its output carriage at one of two reference positions, 0 or its
stroke, relative to its nominal collapsed base. A shared rail then traverses
that layer's stroke. Any active lower bit adds an offset outside those
reference positions. Generated access guard: `state & ((1<<i)−1) == 0`.
A fixed-*reference* drive still moves through its working stroke; it is not a
stationary point actuator. This guard is a chosen sufficient access protocol,
not a claim that other positions cannot be reached by a more capable drive.

Enumerate all 3! clear orders × 3! set orders × two policies = **72 protocols**.
Policy one clears only old bits absent from the target and sets newly required
bits (E-063's minimal-change idea). Policy two clears every old bit on changed
columns and rebuilds the target. Neither touches old==new columns. Each clear
phase precedes every set phase. This excludes interleaved/adaptive schedules;
72 is a bounded protocol search, not a complete mechanism search.

For the required research workload 0/10/20/30/40 mm, enumerate all 25 ordered
pairs. **Nine normalized protocols survive; no changed-bit-only protocol does**.
The best changed-bit protocol still fails two pairs. Example 10→30 retains
lower bit 0 while setting layer 1, so that carriage starts 10 mm above its
reference. Normalization gives **10→0→20→30**, with zero lower displacement at
every operation. Clearing bottom-up and setting top-down is one witness.
The other eight survivors exploit the restricted five-code alphabet: the
40-mm bit never coexists with either smaller bit in an endpoint.

Hold out the complete eight-code alphabet, 0–70 mm: all 64 pairs leave only
**one** of the 72 protocols, bottom-up clear / top-down set with normalization.
This is an out-of-workload logic check, not a proposed 70-mm product requirement.
An independent normal-form check over one through six bits confirms the
invariant: before clearing bit i all smaller set bits have been cleared;
before setting bit i no smaller target bits have yet been set. At the end the
word equals the target. The same global sequence therefore works for arbitrary
mixtures of endpoint pairs across the board in the discrete model. Shared
mechanical interference is not included in that composition argument.

All paths stay between zero and the larger endpoint; they can descend below
both endpoints. This preserves E-063's local-reset tradeoff, not miniature
stability on a changed cell. The product forbids deliberate resetting of
*unchanged* regions, which these logical masks leave alone.

## Complete-machine costs of the changed protocol

Across all 25 pairs, normalized operation count is **40 versus 32** for
changed-bit-only control: +25% contact cycles under a uniform-pair workload.
Across the eight-code holdout it is 168 versus 96: +75%. These are counts, not
operating probabilities. Common bits may be unnecessarily released/reseated;
wear and failed proof exposure increase even if the six global phases remain.
An unchanged site contributes zero operations. A 10→30 edit uses three
transfers instead of one. Actual workloads must be retained in later comparisons.

For a worst full-map workload activating all six phases, their loaded travel
sums to 140 mm. There is another **140 mm** of unloaded shared-rail positioning
and return: each rail first reaches its extended acquisition endpoint before
clearing, and returns after setting. At assumed 100 mm/s and 500 mm/s², six
loaded passes alone take 2.5657 s; serially charging all twelve traversals gives
**5.1314 s**. With an explicit assumed 6-s preparation/read/settle/recovery
reserve, each of six complete contact events must take **<3.1448 s** for <30 s.
Unloaded overlap may improve this only after a collision-free concurrent path
is generated. These allocations omit no intended contact step: acquisition,
unload/catch release, reseat/proof and drive-dog withdrawal belong in dwell.
They are not achieved times or independently priced overhead.

19,200 load-bearing stages/dogs/catches/guides remain. Every active drive carries
the full column payload through its layer; dividing load by three is wrong.
Crossed magnetic addressing is still subject to E-065's gates. The schedule
neither fixes selector cost nor qualifies frame stiffness or support proof.

## Geometry gate and uncertainty

The next discriminator is **nonselected bypass and support-transfer geometry**.
An unchanged upper stage may sit at any lower offset; its retracted dog and
catch must stay clear during the entire shared-rail stroke and unloaded return.
Conversely, when a lower selected layer moves, an already-set upper stage moves
through space with its drive disengaged. Check both motions, neighbors, finite
walls and all support contacts. Logical zero offset is not swept-volume clearance.
Compare a laterally withdrawn fixed-reference rail/dog, a co-moving drive and
a travelling head; charge each extra moving link and load-bearing contact.

Normalization removes variable *binary* lower displacement, not dimensional
error. If each collapsed lower stage contributes bounded reference error e and
bank registration contributes b, layer i still needs at least `b+i*e` acquisition
allowance before dog/catch errors and warp. A common print/material bias adds
coherently rather than decreasing with cell count. No X1C tolerance, friction,
strength, creep or fatigue prior is assigned here. Finite geometry must use
labelled error bounds or sourced process evidence; a wider acquisition mouth
must preserve positive locking and pitch. The model contains no stochastic
cell variation, dynamic load or reader false-acceptance estimate.

Do not print or claim an implemented decoder from this result. Continue with
actual drive/dog/catch sweeps and supported transfer; reject a geometry on
collision or an unsupported interval even though its schedule passes. Reopen
co-moving/offset-following drives if no fixed-reference bypass fits; neither
kind is eliminated by this logical result.
