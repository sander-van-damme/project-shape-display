---
status: complete
builds-on: [E-236, E-229, E-231]
---

# Supported overwrite exposes a short clearance window and an unqualified drive

**Park the forced-return command-inhibit embodiment; do not refine its contacts.**
It can overlap writing without another active register only after resident support
is proved. Under inherited motion bounds, four banks need total command-release
latency **<13.343 ms**. A 3-ms release proof permits **<0.428 mm actual clearance
travel**, including engagement and adverse manufacturing/alignment errors. A
0.35-mm case calculates 29.917 s; 0.50 mm needs 30.070 s. These are conditional
schedules, not manufacturing capability or a selected machine. The old $441.40
allocation also owes a roughly 1.30-kN shared drive and local arrest.

Input main `12e3063`. Reproduce: `python3 tools/curated-experiment-checks/E-237/screen.py`.
Evidence: **architecture construction at state/kinematic level, exhaustive finite
mask replay and calculations with labelled assumptions; self-review**. No finite
CAD, measured friction, process priors, sourced prices, force-rated hardware or
physical qualification. Five 10-mm-spaced heights are a comparison workload.

## What can actually overlap

Three materially different command/support transactions are compared:

| Transaction | Retained state and overwrite opportunity | Outcome |
|---|---|---|
| E-236 direct control | One 80-bit command register/head; rewrite after pickup withdrawal | Four banks: 32.445 s |
| Forced home plus command inhibit | Same register; after resident reseating, common return constrains every pickup toward home and disables both command-to-output routes | Conditional overlap; sensitive clearance window below |
| Hold old outputs, disconnect writer | Old pickup/bar pattern remains mechanically retained while the command register is overwritten during loaded motion | Requires separate output-retention duties and physical isolation; not supplied by one global inhibit bit |

For the forced-home construction: finish stroke and arrest; seat/prove row AND
column supports; start a common pickup-return cam. After command lands physically
clear and isolation is proved, write/read the next 80-bit mask while common return
continues. The return cam must prevent new commands from inserting pickups or
withdrawing column bars. Reconnect only with pickups home and new mask proved;
then perform the next ordinary acquisition/withdrawal. Common cam geometry is
assumed to incorporate reconnect without an extra stage. Cross-row feed may
also overlap writing, granting an intact routed bridge during carriage motion.
These are explicit unconstructed interfaces, not consequences of logical gating.

All 256 four-bit old/new overwrite pairs preserve ideal support in 1,280 state
observations. The source checks resident support before the overlap and home
before next acquisition. It does not simulate contact transitions. E-236 supplies
the height codes; this experiment does not change their paths or shelf count.
A concrete unsafe control has row support out, selected column support out and
an erased pickup: all three load paths absent. A global home command during a
loaded stroke cannot preserve arbitrary selection. If outputs instead stay in
the old pattern, they store that pattern physically: 80 binary retention duties
per head, separate from writable commands, even if a single common rail locks
all outputs. Existing slides can carry this state; 80 new moving parts are not
claimed necessary. Their locks, isolation and proof still need construction.

Source loss before reseating needs the old retained command, retained pickup
engagement and independently arrested lift. During overwrite, mechanically retained
resident supports and the forced-home inhibit must remain safe without power;
partial commands are invalid. A spring-return bit reader or common motor brake
alone does not establish either condition. After source loss, restart only from
proved support and measured heights. A failed brake/contact or false support
proof requires a safe stop; no sub-30-s hardware repair is claimed.

## Causal schedule and manufacturing tipping point

Inherited **assumptions**: contact throw 2 mm, acceleration 8,000 mm/s²,
maximum speed 200 mm/s, per-contact proof 3 ms. Each contact stage and parallel
write takes `C=W=34.6228 ms`. The five lift strokes remain
[-20,-10,+30,-10,+10] mm. Each pulse still pays all four support stages.
Writing begins during the fourth stage only after release latency
`L=t_clear(g)+proof`, where g is actual required retreat from the fully engaged
command interface. The symmetric triangular 2-mm trajectory gives
`t_clear(g)=sqrt(2g/a)` for g≤1 mm, with the decelerating branch thereafter.
This is first passage during a running stroke, not an extra rest-to-rest stroke.

The event recurrence charges the first physical write after map receipt,
all strokes/contact stages, row feed, two seconds for common registration and
final settling, and a full causal retry. Retry discards speculative commands,
returns the empty datum up to 30 mm, measures/regenerates with the inherited
10-ms allowance and performs a fresh first write. Digital preparation does not
replace either first physical write. All rows can contain the 25 old/target pairs.

For four banks, 20 normal rows plus one retry on the critical bank, and the tested
range of L, row indexing hides cross-row writes. There are 84 within-row writes:

`T = 28.809966 + 2W + 84L`.

An independent closed form matches the event recurrence. Turning overlap off
recovers E-236's 32.445358 s exactly. Zero clearance and zero release-proof oracle
is **28.879212 s**, not 28.809966 s: startup and causal retry writes remain.

| Actual clearance g, mm | L with 3-ms proof, ms | Four-bank full map, s |
|---:|---:|---:|
| .15 | 9.124 | 29.646 |
| .35 | 12.354 | 29.917 |
| .50 | 14.180 | 30.070 |
| .65 | 15.748 | 30.202 |
| 1.00 | 18.811 | 30.459 |
| 1.35 | 21.875 | 30.717 |
| 2.00 | 34.623 | 31.788 |

A five-row contiguous regional patch in one bank is 10.158 s at g=.35; remote
banks remain supported and idle. Unchanged cells in a visited row retain column
supports; this preserves commanded height, not measured absence of settling.
Noncontiguous seeks, sensor coverage and additional recovery latency are not free.

With release proof 0/3/6 ms, actual-clearance tipping points are
.712/.428/.216 mm respectively. These are timing thresholds, **not tolerances**.
Write `g=b+e`, nominal command engagement b plus adverse combined error e.
Using the inherited competing e=.15/.35/.70-mm bounds, the 3-ms case leaves
b<.278/.078/no-positive-engagement mm. Even b=.50 with e=.15 misses 30 s.
Those error bounds are not calibrated X1C distributions. Cam phase, module warp,
engagement bias and deflection may be shared across 80 or 320 routes. No IID yield
calculation applies; common clearance proof can falsely accept many outputs.
A different cam topology might separate release distance from working engagement;
that would need a concrete new construction, not a narrower contact here.

For retained outputs, even granting writing fully hidden, zero added stages gives
28.879 s. Two added 2-mm/proof stages per pulse for lock/disconnect and reconnect/
release give **36.150 s**. These bracket a hypothesis, not an implemented buffered
scheduler. Overlapping those operations must preserve old output state and actual
support; calling the common lock an inhibit does not supply that mechanism.

## Whole-machine ledger, force, economics and service

Four banks each serve 20 rows/1,600 cells. The shared head is one per bank.
The forced-home topology adds no resident per-cell state:

| Function | Cell / row | Bank/head | Board |
|---|---|---|---|
| Moving columns / guide stations | 1/2; 80/160 | 1,600/3,200 | 6,400/12,800 |
| Shelf levels / resident bearing sites | 7/2; 560/160 | 11,200/3,200 | 44,800/12,800 |
| Row support axes | shared; 1 | 20 | 80 |
| Column bars / pickup slides | shared | 80/80 | 320/320 |
| Retained commands / endpoint lands | no private command | 80/160 | 320/640 |
| Command-to-output routes requiring inhibition | shared | 160 | 640 |
| Forced pickup-return follower duties | shared | 80 | 320 |
| Lift, local arrest, carriage, reader | shared | 1 each | 4 each |

The 640 routes already appear in E-236's routing ledger; making them disconnectable
adds a requirement, not automatically 640 new parts. Likewise a common return
may reuse pickup followers. Actual additional contacts, cam segments, springs,
sockets, inserts, bearings, fixtures and installation operations are **unresolved**.
The retained-output variant adds at least 320 output retention duties (640 if
pickup and bar cannot share a retained selector), separate from 320 commands.
It must isolate both routes: at least 640 isolation duties. Monolithic rails do
not remove those functional sites. No precision mechanism development is earned.

Inherited printed stock: 80-mm 4×4 column blanks total 8.192 L, about 152–455 h at
assumed effective 15–5 mm³/s before caps/frame/setup/scrap. Command blanks add
.0768 L; duplicate blanks for separate output storage would add another .0768 L
but are not a proposed layout. Five seconds per column insertion is 8.89 h;
10 seconds per 400 support axes adds 1.11 h, before pickups, retainers, wiring,
inhibit assembly and calibration. X1C bed segmentation, layer direction, creep,
roughness and wear remain unresolved. Five/10% scrap multiplies printed effort
by 1/.95 or 1/.90, without assigning either as a measured failure rate.

A bank fault affects 1,600 cells; one column bar serves 20 cells. Retire a head
only after resident support proof. Failed buried combs need temporary support
and module access. Inhibit access/replacement is unconstructed; a common return
jam is a multi-output fault. Opposing resident support errors still permit 2e
settling. Added register readback does not measure support or neighboring motion.

E-236's shared **assumed allocation**, unchanged for comparison: common $195,
$20/bank, $.50/channel and $.02/command retention, gives **$441.40 B4 / $503 B5**.
This leaves $58.60 at B4 for additional inhibit hardware AND any correction to
underallocated drive/arrest/readers. It is not a sourced cost floor or complete
BOM. In particular, the common $30 motor/driver and $20 supply are not force-rated.
At .3/1/3 N assumed lateral command resistance, 320 simultaneous command motions
sum to 96/320/960 N before inertia; whether this loads the writer or shared cam
depends on the unbuilt route. It is distinct from the terrain lift load.

For 320 lifted cells at assumed 3.27 N/cell, 20% friction allowance, .5-kg/head,
3-g columns and 8-m/s² acceleration: **1,298.98 N, 12.990 N·m at 10-mm radius,
371.14 W peak input at .7 efficiency**. A .4-m end-loaded 12-mm shaft at assumed
G=80 GPa twists by .319 mm height-equivalent. This is a conservative shaft-load
scenario, not routed-shaft FEA. At 1/10 N/cell the force is 427/3,883 N and input
122/1,110 W. Those loads are scenarios, not a product per-cell requirement.
Each local bank arrest must hold its own loaded row after branch failure and
control stopping displacement; the $3 allowance establishes no such capability.

Reducing only lift acceleration to 6/4/2 m/s² makes the g=.35 schedule
30.800/32.567/37.327 s. Force barely drops: at 2 m/s² still 1,281 N, since
payload dominates inertia. Gravity-only descent of a 3-g unloaded cell at 8 m/s²
allows only .00543 N opposing guide drag. Positive pull-down would add capture
and tolerance obligations. Fast motion cannot be qualified by timing arithmetic.

## Decision

The new result is a causal overwrite window, with startup/retry and correlated
clearance sensitivity, rather than another assumed free writer. It does not
justify shrinking 320 command engagements or adding an unconstructed output
register. Keep E-236's five-stroke synthesis as reusable knowledge; park these
inhibit/retained-output embodiments, with no print or contact refinement.

The next architectural screen should change the support transaction enough to
remove repeated transfer events or obtain substantially more timing slack while
keeping broad contacts. Compare a program held through an entire row operation
against a changed shared load path; reconstruct E-230's decoder failure before
reusing that principle. Start with event/state/replication bounds, not another
pocket, clutch or guide. Reopening this embodiment requires an explicit broad-
engagement release topology and a force/arrest-qualified allocation; a cheaper
hypothetical actuator or a faster proof flag is insufficient.
