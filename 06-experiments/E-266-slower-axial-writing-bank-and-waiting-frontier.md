---
status: complete
builds-on: [E-259, E-262, E-265]
---

# Slower axial writers: added banks buy time, not a simpler machine

**Keep longer waits as the simpler control.** A third coarse-grid axial bank
has a conditional timing benefit, but its value depends strongly on paying for
more simultaneous power as well as 64 more installed channels. At 850 rpm,
3-mm lead and K32/head, it reduces the deep-scene maximum 43.29→31.27 s for
$287.80 more motor/driver subset plus allocated reserve. With roughly the same
64 total power slots, the result is 39.57 s and cold preparation gets worse.
No sampled configuration establishes a complete $500/$1000/$1500 machine.
Stop bank escalation after the four-bank control: its incomplete allocation
already exceeds $1500 at both pitches. This is an economic stopping choice
within the sampled architecture, not a universal cost floor or a 30-s rejection.

Reproduce `python3 tools/curated-experiment-checks/E-266/frontier.py`; `--check`
runs controls only. Standard library; JSON stdout is disposable. Evidence is
**conditional scheduling, catalog facts and allocated costs**, not physical
qualification, safe operating RPM, a finished-product price or owner preference.
E-263's optional manual article is unchanged; no print, purchase or head design.

## Inherited anchors and bounded search

- E-259 `concurrency.py` supplies the unchanged E-258/E-257 physical river,
  ravine and ruin arrays. S40/N20 uses nine shallow initial/directed commands;
  S50/N30 uses six preset states and 36 initial/directed commands, including
  shallow/deep ravine switching at fixed ground. Duplicates are not new map
  evidence. Both 64×64/6.35-mm and 80×80/5.08-mm cover 406.4 mm. Existing wall,
  miniature-base and under-bridge representation limitations still apply.
- E-255 supplies rest-to-rest spin, 200-mm/s and 5000-mm/s² seek, 50-ms minimum
  row seek, 80-ms dock/release plus 20-ms proof, bank return, one globally longest
  full-row retry and 4-s common allowance. The retry sum is conservative, not
  a tight adversarial completion bound. Failed moves must be remeasured before
  retry; an indefinite jam is not covered. Homing and actual visual/prop workflow
  have no measured duration; reported waits are model totals with these limits.
- B=1/2/3/4 full-width independent rotary heads serve fixed contiguous bands of
  ceil(n/B) rows; three banks have unequal last bands. Every head installs n
  motors/drive paths even if only K are powered. Sweep K=16/24/32/n plus
  min(n,floor(64/B)); the three-bank fixed-total case admits 63, not 64 outputs.
  LPT queues one signed rest-to-rest job per changed output. Unchanged and
  completed outputs rely on resident passive hold. No motor multiplexor,
  collision-free head routing or qualified reader is invented.
- Screw speed 400/600/850 rpm, lead 2/3 mm, nominal acceleration 1000 rev/s².
  E-262 motivates slowing down but establishes **no safe positive speed for
  unspecified support**; static instability cannot be cured by slower rotation.
  Lead2 is motivated by the rough owner observation, not a measured interval.
  A 200-rev/s² plus 5-ms output-token-release control tests correlated schedule
  optimism. No fitted manufacturing priors or independent-cell yield are used.
- Cold neutral is a full-board 0→20/30-mm command. Cold first-map time is paid
  neutral plus the worst initial map command, not neutral plus the worst
  inter-map transition. Dense 0→40/50 is separate stress (signed equal-magnitude
  motion has the same schedule). Neither is called a typical gameplay update.

This gives 420 configurations. Pareto dominance is evaluated **within each
pitch/lead/RPM/stroke scenario**, minimizing installed outputs, partial dollars,
powered-output ceiling, scene maximum, cold neutral and dense time. Do not let
an unqualified speed, shallower ravine or coarser representation dominate a
physically different option. 414 are nondominated because electrical capacity,
setup and waiting genuinely trade off; Pareto membership is not endorsement.
The six dominated points are coarse B4/K24/S50 (both leads, all speeds), dominated
by B3/K32: same 96 power slots, fewer outputs, lower dollars and shorter times.

## Installed burden and dated allocation

[Adafruit 711](https://www.adafruit.com/product/711) and
[3297](https://www.adafruit.com/product/3297), rechecked 2026-10-13: motor
$1.76 at10–99/$1.56 at100+; dual driver $5.36 at10–99 boards/$4.76 at100+.
Orders may include surplus to reach a cheaper tier. 192 outputs buy100 driver
boards with four spare boards. One-bank motors correctly use the smaller tier.
Before tax/shipping, add the **unquoted** E-255 reserve
`$250 + $.02*n² + $55*B`. Its supply/protection $40 and controller $20 remain
unverified; neither shrinks with K. This is a dated subset plus allocation,
not a BOM or complete channel cost.

| Grid | B | Installed outputs | Driver boards bought | Motor kg | Subset + reserve USD | Missing bundle allowance/output at $500 / $1000 / $1500 |
|---|---:|---:|---:|---:|---:|---|
|64|1|64|32|1.12|671.08|−2.67 / 5.14 / 12.95|
|64|2|128|64|2.24|984.64|−3.79 / .12 / 4.03|
|64|3|192|100|3.36|1272.44|−4.02 / −1.42 / 1.19|
|64|4|256|128|4.48|1560.56|−4.14 / −2.19 / −.24|
|80|1|80|40|1.40|788.20|−3.60 / 2.65 / 8.90|
|80|2|160|80|2.80|1166.40|−4.17 / −1.04 / 2.09|
|80|3|240|120|4.20|1488.60|−4.12 / −2.04 / .05|
|80|4|320|160|5.60|1858.80|−4.25 / −2.68 / −1.12|

Every missing feedback, transmission/reduction, spindle, dock, harness, reader
and reserve correction must fit that residual **collectively**. For coarse B3,
just $1/$2/$4 added per output gives $1464.44/$1656.44/$2040.44. Fine B3 leaves
only $11.40 total before those duties. Coarse B2's $1000 case leaves $15.36.
One bank preserves more room for a complete channel under $1000 at longer waits.
No sampled subset meets $500. Changing suppliers/custom PCB manufacture might
change these amounts, but no quote establishes that escape.

Resident burden is unchanged by B: 4096/6400 each pins, screws, thread pairs,
thrust seats, base radial locating and underside socket duties; two pin guide
planes repeat 8192/12800 apertures. S40/S50 retain E-261/E-262's proposed
54/64-mm useful thread and 86/96-mm pin stock, engagement/end margins and
full-travel support uncertainty. Longer stroke's added stock and bed cost are
not quoted; equal reserve does not make S50 equally cheap or reliable.
Head burden is B*n rotary/feedback/transmission/dock paths, B seek and B common
docking axes, bridges, control and cable routing. No side-drive selective radial
slides are added. Finite motor packaging and mutual clearance are still unbuilt.

At an illustrative one minute/output, B2→B3 adds 1.07/1.33 maker hours, before
carriage assembly, calibration or rework. It adds 1.12/1.40 kg of motors.
The 4096/6400 resident fitting burden remains: an extra minute per pair costs
68.27/106.67 hours. Openable shared beds and individual replacement remain the
service hypothesis. Batch molding/casting or machined shared carriers could
reduce touches, but no tooling, shrinkage/yield or assembly quote is supplied;
adding banks does not repair a hand-fitted production route.

## Waiting versus bank count

Seconds, **S40/N20 / S50/N30**, K32 per head. Thus B1/2/3/4 admit 32/64/96/128
outputs, not a common electrical budget. Every number retains the overhead above.

| Grid | Lead mm | rpm | B1 | B2 | B3 | B4 |
|---|---:|---:|---|---|---|---|
|64|3|400|112.54 / 141.01|62.81 / 79.30|46.29 / 56.79|37.46 / 45.95|
|64|3|600|81.10 / 100.06|45.59 / 56.58|33.70 / 40.69|27.52 / 33.17|
|64|3|850|62.76 / 76.12|35.54 / 43.29|26.34 / 31.27|21.71 / 25.69|
|64|2|400|160.04 / 202.76|88.81 / 113.55|65.29 / 81.04|52.46 / 65.20|
|64|2|600|112.77 / 141.23|62.92 / 79.41|46.37 / 56.86|37.52 / 46.01|
|64|2|850|85.12 / 105.18|47.77 / 59.40|35.28 / 42.68|28.77 / 34.75|
|80|3|400|144.95 / 187.42|84.07 / 111.55|66.32 / 86.81|53.14 / 70.64|
|80|3|600|103.65 / 131.93|60.27 / 78.58|47.47 / 61.13|38.27 / 49.93|
|80|3|850|79.59 / 99.52|46.40 / 59.31|36.48 / 46.11|29.61 / 37.83|
|80|2|400|207.45 / 271.17|120.07 / 161.30|94.82 / 125.56|75.64 / 101.89|
|80|2|600|145.31 / 187.76|84.27 / 111.75|66.47 / 86.96|53.27 / 70.76|
|80|2|850|109.00 / 138.93|63.34 / 82.72|49.89 / 64.35|40.20 / 52.54|

At coarse B2→B3/lead3/850, $287.80 buys 9.20/12.02 s less worst-scene waiting
(about $31/$24 per second saved **for this allocation**, not lifetime value).
At fine pitch the increment is $322.20 for 9.92/13.20 s; its missing-hardware
allowance makes it a weak $1500 proposition. At coarse B3/lead2, even850rpm
still gives35.28/42.68s. At400/600rpm, a third bank cannot restore30s for either
coarse depth. Slower operation does not alone reject a usable display.

Allowing full K=n improves coarse deep maxima by **zero** at this speed; coarse
shallow changes by at most .06s. It does improve cold/dense time. At fine pitch,
full K gives deep B1/2/3/4 maxima92.62/52.48/39.28/31.00s at850/lead3, but powers
80/160/240/320 outputs. This is not free capacity. The coarser board removes2304
resident pairs, but E-257/E-258's representation caveats remain a product choice.

## Electrical admission and cold/session waits

K is permission to power an installed motor, not a removed driver. Supplier
711 arithmetic is .25 A at its rated-load condition and .50 A stall per motor;
these are **not measured screw currents or a PSU rating**. B2/K32 gives16/32 A,
B3/K32 gives24/48 A, B4/K32 gives32/64 A. At6 V the rated-load arithmetic is
96/144/192 W. Slow screw RPM does not imply a proportional current reduction:
PWM, gear ratio, startup, low-speed control, thermal duty and torque are unqualified.
Braking or a jam retains its token until current is actually safe; power-loss
holding still relies on the resident mechanism, not the powered bridge.

Fixed-total control, at850rpm/lead3: B1/K64, B2/K32, B3/K21, B4/K16 admit
64/64/63/64 motors. About16/32 A rated-load/stall arithmetic applies throughout.
Entries again give S40 / S50 seconds.

| Grid | B/K | Scene maximum | Cold neutral | Dense full stroke |
|---|---|---|---|---|
|64|1/64|62.71 / 76.12|48.59 / 63.88|79.18 / 94.47|
|64|2/32|35.54 / 43.29|42.58 / 58.11|73.64 / 89.17|
|64|3/21|30.87 / 39.57|53.15 / 74.80|96.45 / 118.09|
|64|4/16|28.36 / 35.39|40.30 / 56.30|72.30 / 88.30|
|80|1/64|75.91 / 92.62|97.76 / 135.88|174.00 / 212.12|
|80|2/32|46.40 / 59.31|71.29 / 100.23|129.17 / 158.12|
|80|3/21|41.03 / 53.09|63.50 / 89.85|116.21 / 142.56|
|80|4/16|41.94 / 54.89|58.78 / 83.49|108.19 / 132.90|

Three coarse banks need four waves for64 cells atK21, versus two atK32, so cold
preparation gets slower despite a shorter band. Fine B4 loses to B3 on scene
waiting and cost at this fixed capacity, while improving preparation/stress;
it is not globally dominated. No global token lending, preemption or bank-boundary
optimization is claimed. They could shift the frontier without deleting channels.
The fixed-total coarse B3 deep row bracket39.03–39.57s and fine B3 52.61–53.09s
show that LPT suboptimality alone cannot restore the B3/K32 times.

For K32/head,850rpm/lead3:

| Grid/B | Cold neutral S40 / S50 | Dense S40 / S50 | Cold first-map S40 / S50 |
|---|---|---|---|
|64/2|42.58 / 58.11|73.64 / 89.17|69.24 / 92.45|
|64/3|30.85 / 41.68|52.50 / 63.32|50.57 / 66.79|
|80/2|71.29 / 100.23|129.17 / 158.12|111.07 / 153.66|
|80/3|49.93 / 69.69|89.46 / 109.22|80.28 / 110.39|

An illustrative ground→road→ruins→shallow ravine→deep ravine sequence totals
101.30→83.48 s of command waits for coarse B2→B3/K32, excluding separately paid
58.11→41.68 s initial neutral. At fixed-total admission, B3's command sum is
96.87 s and preparation74.80 s: **171.67 s versus B2's159.41 s combined**.
This is one illustrative sequence, not observed play frequency or a prediction
of subjective enjoyment. Cold setup may happen before players arrive, but it
still occupies the machine. No between-map full-neutral reset is inserted.

## Sensitivity, comparator and disposition

At850rpm/lead3, reducing acceleration1000→200rev/s² and charging5ms token
release jointly changes coarse B2 scenes35.54/43.29→37.63/45.32s and B3
26.34/31.27→27.70/32.56s. Fine B3 changes36.48/46.11→39.25/48.83s. These are
correlated bounds, not measured distributions. Whole-board support/fit bias can
invalidate all speeds together; none of this scheduling qualifies manufacturing.

E-265 side-friction remains a **conditional** comparator: at coarse B2/K32,
lead3 and unqualified2000 nut rpm it gives27.67/30.93s, cold31.53/38.13s and
dense44.73/51.33s. Coarse axial B3/K32 at850rpm gives26.34/31.27s, cold30.85/41.68s,
dense52.50/63.32s. Comparable scene times exchange side contact/reaction and128
selective radial slides for64 extra axial rotary channels and another bank.
The roller's force, neck, support and control issues remain unresolved; the
axial writer's rotary stability, retention, docking and routing also remain
unqualified. Neither earns local head/rotor/selector development from this table.

**Decision:** retain one-/two-bank coarse axial writing with honest longer waits
as the simpler cost/service controls. Preserve coarse B3 only as a conditional
premium timing option if the real channel bundle and increased admitted power
fit; do not add it merely to force30s. Fine B3 and either B4 do not justify
further bank escalation under the present allocations. The strong Pareto trade
is real, but no preference winner or purchase is selected. Reopen added-bank
engineering only with a credible complete channel/power/assembly allocation and
an earned loaded-speed/support window. E-263 remains optional and unchanged;
no new owner question or new physical job follows from this bounded comparison.

Verification:1728 full-concurrency anchors against the inherited scheduler,
420 independent exact dense-wave calculations (including uneven bands), E-262
850-rpm anchors, brute-force supplier quantity tiers, budget identities,
fixed-total quotas, physical reach/shallow-neutral delta identity and Pareto
controls. E-259's729 small-row oracle and288 lead anchors also pass. This is
self-review of executable models, not independent or physical validation.
