---
status: complete
builds-on: [E-120, E-121, E-126, E-163, E-234, E-243]
---

# Moving height memory into cords removes shelves, not independent support

**Park the screened external cord/clamp machine before termination, spool or grip
refinement.** Straight tails remove shelves but add 6,400 cords, 12,800 bends and
6,400 independently adequate grip sites.
A favorable direct writer still needs 240 independently loaded outputs:
**24.552 s / $623 allocated**, with unqualified gravity following and arrest.
A common actuator can close many grips; a common continuous cord cannot replace
those independent constraints. No machine is selected.

Input main `3345b91`. Reproduce:
`python3 tools/curated-experiment-checks/E-244/screen.py`.
Evidence: **architecture hypotheses, exact linear-constraint calculations, ideal
handoff replay and bounded geometry/time/force allocations; self-review**.
No measurements, finite CAD, calibrated priors or quotes. All numerical inputs
are assumptions. Five heights 0/10/20/30/40 are a comparison alphabet, not a
product resolution. JSON output is disposable.

## What changes, and what earlier work already settled

E-120 already established that two-edge tendon routing is not topologically
excluded, and counted 740–881 m before moving legs, ends and storage. E-121's winding collision and loop slack witness remain. The changed embodiment has **straight externally gripped tails,
no drums or local rotary locks**, and accounts for the moving lower column anchor.
E-163 already rejects a free-tail capstan as memory; no claim that it self-locks
is reopened. E-126's serial particle shuttle and E-234's paired rigid supports
remain compression controls, not presumed viable machines.

| Complete-machine hypothesis | Retention and rewriting | Principal burden / disposition |
|---|---|---|
| Separate straight cords, common row clamp | One captured cord per column; row platen closes 80 distinct friction sites. An external head takes all 80 tails, proves load, opens the clamp, independently changes lengths, reclamps/proves, then releases. | 6,400 grip sites, loaded independent head outputs, long tensile transmission; screened below and parked. |
| One frictionless continuous cord per row, or crossed row/column cords | End clamps fix total row/column lengths; a shared draw adjusts sums. | Fails independent height retention; differential modes remain even with perfect material. |
| Paired independently clamped cords | Inactive lengths are written unloaded, incoming common datum rises, outgoing datum lowers; separate slack pockets prevent tangling. | Conditional max-envelope support, but 12,800 cords/anchors/grips, ≥25,600 bends and 160 movable row datums. No packing or writer advantage over E-234 established. |
| Direct compression controls | E-243 common comb/shelves; E-234 paired bars; E-126 confined solids | Respectively repeated shelf sites, duplicate moving media, or serial particle rate. Avoid long tensile elasticity and string routing. All remain unqualified. |

Single-cord head sequence preserves unchanged tail coordinates while the common
row clamp is open. This is a **grant of 80 independent grounded head constraints**,
not a claim that one rigid moving grip bar can do it. Direct 40-mm opposed tail
motions require separate positional outputs or a real selectable transmission.
Every output needs arrest while released from the resident clamp. Length readback
cannot establish column height under cord stretch, slip, routing friction or a
hung column; actual terrain readback and load proof are required before departure.

A bad write with intact support can reclamp at the actual measured profile and
retry once. A broken cord, failed anchor, clamp creep or failed head arrest has
no automatic rescue path; quarantine and temporary underside support are needed.
Mechanical resident keeper closure can hold through electrical source loss only
if all individual grips remain adequate. Loss during open-clamp motion is not
safe without independently grounded head retention. Unvisited rows stay clamped;
all 80 visited cells undergo a load transfer even for one changed cell. Opposing
capture/seat errors ±e can cause up to 2e unchanged-cell motion, before elasticity.
All these interfaces remain unconstructed.

## Shared length is not independent state

For frictionless inextensible row strands with equal path coefficients,
`sum(h[row,:]) = constant`. Eighty rows leave 6,320 unconstrained coordinates.
Adding eighty column strands gives rank `80+80−1=159`, leaving **6,241**.
The 2×2 transition `(20,20;20,20) -> (30,10;10,30)` preserves every row and
column length. Unequal loads can drive this mode; equal loads do not restore
independent stiffness. Exact rational elimination checks n=2…6 against rank
2n−1, and the explicit checkerboard witness checks every constraint.
This excludes this simple crossed routing, not every nonlinear cable network.

Separate cords closed by one platen instead impose 80 separate no-slip
constraints: one actuator does not mean one contact or one constraint. Crediting
friction at intersections of the continuous strand similarly restores distributed
retention sites; it does not evade their force, release and wear obligations.
The paired-cord ideal `h=max(old+a,target+b)` reproduces supported transfer in
56,875 two-cell observations. Slack capture, return tension, rounded routes and
load equilibrium are **not** represented by that max equation.

## Under-cap routing and manufacturing bounds

Allocate 40 paths toward each x edge per row, 80 rows. Separate the incoming
vertical legs from outgoing horizontal legs with a lateral lane; two quarter-turn
guides connect them. Stack outgoing lanes at spacing `s=d+2e+.4` mm, where d is
cord diameter and e is each route's total size/position error bound. Common
translation cancels; opposite local or module offsets consume 2e. No yield is inferred. Two bent corridors, a 1.4-mm-wide stem and
.4-mm separating allowance need transverse width `2r+d+2e+1.4+.4`, where
r=kd/2 and k is assumed bend-diameter/cord-diameter ratio.

Highest redirect is 5 mm below the lowest surface. With 39s deck spread and a
moving anchor that must remain at least r+2 below its redirect, identical stem
length must be `40+5+39s+r+2`. The sampled k=2/5/10 are **geometrical alternatives,
not allowable cord bends**. Nine of 27 d/e/k boxes meet this one lane-width
inequality. Rounded guide solids, cable sag, end fanout, pin/guide sweeps and
continuous collision checks remain absent; these are necessary allocations only.

| d mm, e=.35, k=5 | Transverse spare mm | Routing depth mm | Stem mm | Sharp-skeleton cord stock m |
|---|---:|---:|---:|---:|
| .3 | .78 | 55.6 | 102.35 | 1,492.16 |
| .5 | −.42 | 63.6 | 110.65 | 1,526.72 |
| 1 | −3.42 | 83.6 | 131.40 | 1,613.12 |

Stock includes moving leg at zero height, lateral 2r, actual half-board horizontal
run and **60 mm per tail** for 40-mm movement plus an assumed 20-mm engagement.
Actual rounded length, tie/termination stock and external fanout can change it.
No spool slack is required on the taut single-cord branch, but external ends
sweep 40 mm in separate lanes. Paired cords require real slack storage as well.
The .3-mm case's external outputs occupy roughly 406×56 mm per edge before clamps
and structures; arbitrary output-to-channel fanout and head movement are unbuilt.
The new information beyond E-120 is moving-anchor/tail accounting, not a
cable-routing proof.

At e=.15/.35/.70, d=.3/k5 transverse spare is 1.18/.78/.08 mm. The last has little unmodelled allowance. Shared printed datum warp affects many routes;
cord diameter/length batch error, knot seating, tension history, creep and reader
bias correlate errors. Smooth guide finish, layer strength, wear and small bend
behavior have no X1C/PLA or cord-specific evidence. Replaceable open routing trays
would improve access but need covers and temporary loaded support during service.

The .3-mm route's assumed 2×1.4-mm solid stems total **1.834 L**. At assumed
5–15 mm³/s extrusion and 10% scrap that alone takes **113–38 h**, excluding caps,
guides, frames and travel. At assumed density 1.25 g/cm³, stem plus 1-mm cap is
only **.386 g**. It supplies .00378 N weight, below an assumed .005-N guide drag
before routing loss. The timing model's 3-g moving column would require a changed
section or about **16.7 kg total added ballast**; it is not a consequence of this
light section. Gravity return is therefore an architectural gate, not a later
cord-selection detail.

## Force, load sensitivity and economics

The [Harvard rope-friction demonstration](https://sciencedemonstrations.fas.harvard.edu/presentations/rope-friction-around-pole)
(accessed 2026-10-12) supports the capstan relation and warns that small-radius
bending adds loss; its nylon/steel friction does not transfer to this design.
For the two stationary quarter turns, assumed μ=.05/.15/.3 gives raising tension
multipliers `exp(μπ)`=1.17/1.60/2.57, excluding bending hysteresis. With 3-g
columns and .005-N guide drag, gravity permits only **20.9/15.2/9.52 mN** tail
drag quasistatically. During assumed 8 m/s² descent these become
**.367/.268/.168 mN**. A .386-g column fails even with a freely paid-out tail
under that guide-drag assumption. Pulleys or pull-pull drive alter this bound
but restore repeated bearings, preload or additional paths; none is granted.

For straight grips let N be the **sum of both face normals**, μ=.1… .4 and
minimum delivered force be half nominal under coherent platen/cord variation.
Required nominal N is F/(.5μ): at μ=.1 and F=.2/1/10 N per tail,
**4/20/200 N per site**, or 320/1,600/16,000 N if all 80 sites have that load.
These are force sensitivities, not expected simultaneous D&D loads. Concentrated
loads demand adequate local force even when total row load is small; a stiff
common platen does not imply uniform grip on variable-diameter cords. No springs,
pressure equalizer, qualified clamping stress or clamp-release mechanics exist.

At μ=.15, .2/1/10-N load on each of 80 rising cells requires about
25.6/128.2/1,281.6 N tail force before acceleration; at 200 mm/s this is
5.1/25.6/256.3 W mechanical per head. For actual maps sum actual cell loads,
not 6,400 copies of a maximum. An assumed 300-mm loaded length with EA=20/200/2000 N
changes height by `.15/1.5/15 mm` for ΔF=1 N when ordered stiffest→softest.
A whole-length/common-temperature change adds correlated drift. This simple
linear bound omits unequal tension across bends, creep and seating; it is not
a material selection or output-accuracy requirement.

## Complete schedule and replication

Favorably grant 80 independent bidirectional positioned outputs/head, gravity
following, an arrested loaded stroke and complete sensor coverage. No physical
mask or prewritten inventory is used: commands directly drive those 80 outputs.
Each head serves both edges (40 outputs each), requiring a spanning carrier or
synchronized pair; that access structure is unbuilt. At v=200 mm/s,
a=8,000 mm/s², rest-to-rest time is t(d).
Row service is `S=2t(40)+8[t(2)+.003]+t(5.08)+.020=.797382 s`.
Eight stages pay for capture approach/close, takeover, resident release/restore,
proof transfer and head release/clear; geometry could require more. Two 10-ms
reads and 3-ms stage dwells are allocations, not sensor results. Both loaded
motion and empty 40-mm head reset are included.

`T=2+(ceil(80/B)+1)S+t(40)` includes ingestion/initial registration/final settling
allocation, one causal whole-row retry and its extra empty recovery stroke.
Three banks/240 outputs give **24.552 s**. At loaded/reset acceleration 2 m/s²
it is **28.827 s**, still granting successful gravity following. Formula agrees
with an independently expanded event list; the 8-m/s² case has only .1946 s extra
per service before reaching 30. Regional changes pay visited-row service plus
actual seek and retry; skipping distant rows does not make transport free.

| Functional item | Per cell / row | Largest B3 bank / reusable head | Board |
|---|---|---|---|
| Column / guide stations | 1/2; 80/160 | 2,160/4,320 per bank | 6,400/12,800 |
| Cord / anchor / retained tail grip | 1 each; 80 each | 2,160 each | 6,400 each |
| Fixed bends / grip face contacts | 2 each; 160 each | 4,320 each | 12,800 each |
| Row clamp actuator/keeper duty | shared; 1 each | 27 each per bank | 80 each |
| Loaded positioned output, head grip, downstream arrest | shared | 80 each/head | 240 each |
| Output guide duties (minimum two) | shared | 160/head | 480 |
| Head transport, reader and registration systems | shared | one set/head | three sets |

No resident per-cell spring, motor, spool or insert is proposed. Force equalization
may require compliance at every grip; calling it one strip would still repeat
6,400 critical contacts. Fasteners, clamp bearings, structural fixtures and
per-output control wiring are unresolved, not zero. Cutting, routing, anchoring
and tail loading give **25,600 operations**, 71–213 h at assumed 10–30 s each,
before columns, head build, calibration or maintenance. A failed common row clamp
threatens 80 heights; replacing a buried cord requires access and temporary support.

Illustrative allocation: **$195 common +$20B +$1×80B outputs +$.02×6,400 sites**.
This is an aggressive allowance, not a bought BOM or price floor. B3 costs $623;
$.50/output still costs $503. With entirely free resident bought parts, the
$1/output case is $495; thus no universal cost impossibility is claimed.
At $.02/site the complete channel ceiling is **$.4875** below $500. Allocating
that entire resident $128 to 1,492 m of cord leaves only **$.0858/m**, with no
money for anchors, clamps or guides. No rated BOM fits these allocations yet.

## Decision and next discriminator

This topology removes E-243's 32,000 shelves but substitutes many loaded tensile
interfaces and hundreds of independent head outputs, with added gravity, drift
and assembly risks. Paired cords duplicate the support route; shared continuous
cords lose independent retention. Neither earns a drum, tiny grip or bend-design
campaign. This does not reject all tensile mechanisms or establish process capability.

Next compare **direct smooth rigid pins held by replaceable, collectively loaded
row strips** with the positive-comb control. Remove the long cord transmission;
count all contact sites and retained head functions before any strip detail.
Reconstruct E-148/E-165/E-216 and E-236 first: changing resident holding physics
must not smuggle back their expensive independent writer or repeated mask traffic.
The first discriminator is a complete supported moving-datum transaction and
force-distribution bound under coherent pin-size/platen error. Stop if it merely
restores the old independent-axis budget or needs thousands of tiny springs.
No print: the present rejection does not depend on choosing a precise cord prior.
