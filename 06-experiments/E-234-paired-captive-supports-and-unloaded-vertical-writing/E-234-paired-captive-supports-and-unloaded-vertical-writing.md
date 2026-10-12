---
status: complete
builds-on: [E-233, E-218, E-221, E-226]
---

# Captive paired supports remove cassette handling but multiply resident hardware

**Park this paired-bar embodiment before pad, comb or finger refinement.**
Keeping both profiles under every column removes travelling cassettes, turnover,
old-height acquisition and independently loaded writer axes. It instead needs
**12,800 captive support bars and temporary friction sites**, plus 160 vertically
moving row bases. The cheapest sampled timing-feasible allocation uses nine
heads / 720 binary channels / **28.807 s / $999 assumed bought cost**. Even
reducing the shared-head allocation from $65 to $20 gives $594. No machine is
selected and no print is justified.

Input main `de15f3c`. Reproduce:
`python3 tools/curated-experiment-checks/E-234/screen.py` (stdlib, stdout only).
Evidence: **architecture hypotheses, ideal contact replay, dimensional bounds,
and assumed force/time/economic scenarios; self-review**. No CAD, quotes,
process distributions, physical measurements or independent validation.
Five heights 0/10/20/30/40 mm are a comparison alphabet, not a resolution choice.

## Changed transaction: keep both profiles captive under each row

Give every display column a foot spanning two 1.6-mm bearing lanes separated by
.8 mm, inherited from E-218. Each lane contains a vertical 64 × 3.4 × 1.6-mm
support bar, five broad height notches and two guide stations. A common row comb
holds all 80 bars in one lane; its carrier is one vertically moving row base.
There are **two resident bars per cell**, not one spare row carried by a head.
A base's final positions are 0 and −45 mm. Each position needs a retained frame
dock. Separate lateral lanes avoid E-233's homogeneous-section merge premise;
no foot must pass through a higher shelf in its own bearing lane.

At rest lane A carries the old profile at base 0; lane B is docked at −45. A
bank head visits a row, programs B in place, raises B, then lowers A. Next visit
reverses lane roles. The writer below the row only touches the inactive lane.
No 406-mm cassette extraction, inventory buffer, turnover or retained old-code
copy is needed. Lowered media remain in their own row; head transit through
resident frames is still unconstructed, not declared collision-free.

The inactive bars must remain independent while the common comb is open:

1. Prove the old dock, old keeper and actual heights; dock the head. Engage a
   **common pressure strip** against the 80 inactive bars, then open their comb.
   Friction here holds unloaded bar weight only, never terrain load.
2. Insert a common top platen into the inactive lane, reset all its bars to the
   lowest writer datum, and withdraw. The platen's reset/return is charged.
3. Use q equally spaced retractable bottom fingers on one vertical beam. For
   each of 80/q adjacent phases, preset the q outputs, retract target-zero
   fingers, rise through four stopped 10-mm increments and retire fingers at
   each target height. The strip holds retired bars while the others rise.
   Return the empty beam, index one 5.08-mm phase, repeat, then return x home.
   This requires q **physical** binary output channels per head. No free latches
   or independent vertical axes are assumed for the fingers.
4. All raw values are 1 mm above their intended seated heights. Close/prove the
   common comb, release the pressure strip, allow bars to seat downward onto
   their notch load flanks, and read actual seated tops. This explicitly removes
   nominal notch play from the intended datum; **successful gravity seating is
   a grant**, not a constructed or qualified result. A bad read keeps old support.
5. Withdraw writer intrusions. Arrested shared lifts raise incoming B by 45 mm;
   dock/prove it at zero. Then take A on the second lift, release its upper dock,
   lower it 45 mm and dock it. Reset both empty lift carriages, read/prove final
   heights, and feed to the next row. No media transport or offline programming.

Terrain follows E-218's `h=max(old+a,target+b)`: first a=0 and b=−45→0, then
b=0 and a=0→−45. Thus an ideal unchanged cell stays fixed, and changed cells
move monotonically; there is no all-changed apex excursion. All 80 cells in a
visited row nevertheless undergo support replacement. Other rows stay docked.
Finite contact area, gravity following, comb/dock strength and grounded arrest
are prerequisites, not supplied by the max equation.

The source checks 15,625 three-cell maps / 160,150 contact-event and midpoint
states, plus a 997-subdivision scalar holdout. It replays 6,250 stable retry/control
cases (5,000 actual wrong codes): deposit onto the actual safe profile, read it, rewrite the now inactive
lane and exchange again. Before transfer, a wrong code can simply be rewritten
under the unchanged old dock. The budget conservatively charges one complete
row retry in the critical bank. A failed read, missing support or hung/off-grid
column demands supported service; no under-30-s repair is promised. False
acceptance can disturb an originally unchanged cell; replay does not qualify
reader coverage. Resetting the **active** lane gives an explicit drop witness.

A shared lift needs a grounded arrest downstream of its drive; a powered motor
is insufficient. Without arrest, source loss during a 0→40 rise can lose 20 mm
at the mid-transfer example. The slower schedule charges 1-mm indexed arrest
and 1-ms proof per increment, with at least two interlocked catch functions per
lift; impact, engagement and support proof remain unbuilt. Keeper/dock/pad/read
interlocks are logical specifications, not sensing hardware.

## Finite envelope and manufacturing window

A support bar top is `base+h`; its bottom is `base+h−64`. At base −45, final
inactive tops lie −45…−5 and bottoms −109…−69 mm. During writing the +1-mm
seating offset makes the ranges −44…−4 and −108…−68. A 2-mm reset platen can
fit above the highest inactive top below a zero-height foot, with **2 mm nominal
vertical spare**. The highest bottom finger reaches −68, below the lowest
active bar bottom −64. These are necessary section clearances only; combs,
frames, guide walls, return linkages, pad release cams and docking are not finite
routed CAD. Bars occupy a 104-mm union and need underfloor writer space.

Use competing error bounds e=.15/.35/.70 mm **per mating component**, including
its local, batch, warp and assembly contribution; these are not X1C priors.

| Necessary function | Formula | e=.15 / .35 / .70 mm |
|---|---|---|
| 4-mm notch / 2-mm centered comb entry | 1−2e | .70 / .30 / −.40 mm |
| Separate 1.6-mm lanes, .8-mm gap | .8−2e | .50 / .10 / −.60 mm |
| Reset platen vertical spare | 2−2e | 1.70 / 1.30 / .60 mm |
| Possible unchanged-height shift on A/B takeover | 2e | .30 / .70 / 1.40 mm |

The lane gap is already fragile in the .35-mm scenario. Sharing a row base
correlates errors across 80 sites; opposing A/B batch bias does not cancel.
Final flank seating and actual readback are necessary because a 4/2-mm notch
has 2 mm axial play. No yield probability or manufacturing pass follows.

For an assumed solid-bar density 1.25 g/cm³, mass=.4352 g. Let strip friction
μ=.1… .4, mean normal force N=.3 N/bar with ±50% spatial/common variation,
and downward disturbance .005/.01/.05 N. Minimum holding margin is
`.1×.5N − mg − disturbance` = **+.005731 / +.000731 / −.039269 N**.
Worst upward writing force at 8 m/s² is `.4×1.5N+m(g+8)` = .18775 N/bar,
**15.02 N for 80**. These are unqualified bounded scenarios, not material data.
At .01 N disturbance, the common pressure loss tipping point is only about
2.4% of the nominal N beyond the assumed worst reduction. At .05 N disturbance,
required mean N exceeds 1.085 N/bar; stronger preload is not free force/wear.

After releasing the strip, guide drag must be **below .004269 N** even for
quasistatic gravity seating. The .005-N competing drag case already sticks.
A common platen cannot press all differing final bar heights simultaneously;
adding individual seating fingers or springs changes the ledger. This is an
unresolved mechanism obligation, not justification to refine 12,800 pads.
Terrain following is separately unqualified: a 3-g column descending at 8 m/s²
has only .00543 N gravity surplus for guide drag. No positive downward capture
is included.

## Whole-machine schedule and economics

Rest-to-rest motion uses `t(d)=2√(d/a)` below v²/a, otherwise d/v+v/a.
Assume v=200 mm/s and a=8,000 mm/s² unless varied. Let g=80/q, with q drawn
from divisors 1/2/4/5/8/10/16/20/40/80; enumerate B=1…80 disjoint banks.

- One q-output phase: `W=4t(10)+t(40)+6[t(3)+.003]`. Six selector events are
  initial preset and releases at all five heights, with 3-ms proof allocation.
- Whole-row reset: `R=2t(40)+2t(3)` for platen travel and insertion/withdrawal.
- Writer x feed/return: `X=(g−1)t(5.08)+t((g−1)5.08)`; q outputs span the row
  at g-pitch spacing. This grants routing but does not hide the phase return.
- Exchange: `2L(45)+2t(45)+2t(3)` including loaded lifts, empty resets and dock
  approach/clearance. L=t for the unbuilt continuous arrest; indexed L is
  `45[t(1)+.001]`. This conservatively charges all 45 mm as loaded.
- Row cycle `S=R+gW+X+exchange+u+t(5.08)`. u=.25/.50/1 s is an **assumed**
  combined read, keeper, pressure-strip release, seating, dock and proof allowance.
- Full map `T=2+(ceil(80/B)+1)S`: two seconds global command/homing/registration/
  settle allowance and a causal full-row retry. No overlap or prewritten target.

At q80 a fresh map writes 6,400 physical values, resets 80 inactive rows,
executes 320 writer height increments and 160 loaded base transfers before retry.
Readback owes 6,400 old, 6,400 seated-media and 6,400 final height observations;
shared cameras/scanners are possible but coverage, occlusion and latency are
unconstructed. The u and global allowances do not demonstrate those timings.

| Scenario, least assumed bought allocation under 30 s | B / q / channels | Seconds | Assumed dollars |
|---|---:|---:|---:|
| Fast, u=.25, continuous arrest granted | 9 / 80 / 720 | 28.807 | 999 |
| u=.50 | 10 / 80 / 800 | 28.376 | 1,092 |
| u=1 | 12 / 80 / 960 | 29.446 | 1,278 |
| a=2,000, u=.25 | 14 / 80 / 1,120 | 29.364 | 1,464 |
| Indexed arrest, fast, u=.25 | 16 / 80 / 1,280 | 27.699 | 1,650 |
| Fewest channels, then least allocation, fast u=.25 | 20 / 20 / 400 | 28.296 | 1,602 |

Dollar calculation is **$130 fixed +$32 resident hardware +$65B +$.35Bq**.
Illustrative per-bank $65 partitions into $14 lift drives, $10 reset/sweep,
$8 transport, $8 reader/electronics, $10 arrest/docking, $15 rails/wiring/mounts.
These are allocations, **not sourced purchases, a feasible BOM or a cost floor**;
$32 for 160 row assemblies is particularly unqualified. Reduce the bank allocation
to $20 and the lowest timed result is still B9/q80/$594. At B9/q80 the remaining
budget under $500 is **less than $9.56/head** for all shared hardware after these
other allocations. Granting entirely free heads gives a $302 timing-feasible
control; therefore this is explicitly not a universal economic impossibility.

A regional edit skips untouched rows. Critical time is two seconds plus visited
row services, one retry, and **actual seek distance**, replacing adjacent feed
where rows are skipped. A patch concentrated in the largest nine-row bank can
consume the full-map service count. One changed cell still rewrites 80 supports;
A/B seating error exposes unchanged cells in that row to the 2e bound.

Each loaded lift must carry up to 80F: 80/261.6/800 N for assumed cell loads
1/3.27/10 N, or .8/2.616/8 N m at 10-mm ideal drive radius, before carrier mass,
friction and efficiency. Nine simultaneous middle-load lifts imply 2.354 kN and
about 673 W input at .2 m/s and .7 efficiency, excluding writer load/inertia.
The illustrative drive and supply allocations are not force-qualified.

## Replication and decision

At the B9/q80 scenario, the largest bank contains nine rows:

| Functional item | Cell / row | Largest bank or head | Board |
|---|---|---|---|
| Columns / guide stations | 1/2; 80/160 | 720/1,440 | 6,400/12,800 |
| Captive support bars / guide stations | 2/4; 160/320 | 1,440/2,880 | 12,800/25,600 |
| Temporary friction sites / bar keeper contacts | 2/2; 160/160 | 1,440 each | 12,800 each |
| Notch load positions | 10; 800 | 7,200 | 64,000 |
| Moving bases / combs / pressure strips | 2 each/row | 18 each | 160 each |
| Upper and lower retained dock sites | 4/row | 36 | 320 |
| Base guide stations (at least two/base) | 4/row | 36 | 320 |
| Binary fingers / guides / drive outputs | shared | 80 each/head | 720 each |
| Shared loaded lifts / arrest sets | shared | 2/head | 18; ≥36 catch functions if indexed |
| Reset platen, sweep, x phase feed, y feed, reader | shared | one each/head | nine each (x fixed at q80) |

No resident individual springs, inserts, sockets or motors are proposed; pressure
strips still repeat **12,800 force-sensitive contacts**. Head springs, bearings,
fasteners, fixtures and sensor paths have no finished count. Comb and row-base
beams span 406.4 mm and need at least two printed modules on the 256-mm bed;
intermediate supports and stiffness are unresolved. Row-wide clamp/dock failures
affect 80 cells; a head outage blocks its bank. Both bars are buried below terrain,
so failure replacement requires temporary independent support and access.

Bar stock is **4.456 L**, before guides/frames/heads and after ignoring notch
removals. Assumed 5–15 mm³/s effective extrusion and 10% scrap give **275–92 h**
for bars alone. The inherited 4.608-L column allowance brings stock to 9.064 L.
Bars require 12,800 placements: **35.6–106.7 h at assumed 10–30 s each**, plus
6,400 columns, 720 head outputs, 160 base/comb/pad assemblies and dock alignment.
Orientation, buckling, wear, pressure-strip creep and joint stiffness remain
unqualified. Printing monolithic strips does not erase functional contact sites.

Compared with E-221's favorable stopped head (240 independently loaded axes,
26.511 s), this transaction removes independent load arrest from the writer,
but triples controlled outputs in its least-allocation case and adds 12,800
resident moving support bars. Compared with E-233's 32,000 shutters it reduces
moving media count, but restores friction retention, duplicated supports and
head multiplicity. Neither comparison earns deeper development.

Keep the distinct causal result: **captive duplicate profiles trade transport
for resident duplication; unloaded vertical writing trades load-rated arrest
for a small-force retention-and-seating problem, not zero retention**. Stop this
embodiment before finer pad or keeper work. Reopening needs a transaction that
removes duplicated moving supports or most writer strokes/head count, together
with a complete supported sequence; merely lowering an allocation or adding
individual springs is insufficient. Next architecture synthesis should address
state placement directly: can a common load support coexist with externally
rewritten height information without either two supports per cell or independently
loaded head outputs? Any proposal must exhibit its actual rewrite/hold/transfer
paths before a timing sweep. No current survivor or hardware pass is implied.
