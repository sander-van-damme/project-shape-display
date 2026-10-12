---
status: complete
builds-on: [E-239, E-236, E-065, E-074, E-075, E-183]
---

# Cheap electrical channels do not supply retained mechanical commands

**Park the tested wound soft-armature masks; retain inexpensive direct electronics
as a comparator.** Diode-isolated coils remove electrical half-selection, but a
scanned monostable mask forgets earlier bits unless each group is retained.
Writing all bits concurrently permits one keeper per bank, trading matrix
hardware for peak current. This is a new retention/power trade, not a restoration
of the 6,400-site magnetic architecture.

In the coupled bounded screen, no case simultaneously meets the force condition,
<30 s and the assumed <$500 ledger. The least-allocated force survivor is
**$519.62 / 29.274 s**, with 400 coils, five common keepers, 200 turns/coil and
.4 A per selected coil. This is **not a sourced cost floor**: changing unquoted
hardware allocations could cross $500. Nor is it a force-qualified survivor:
it has only 6% calculated force margin in the chosen scenario and an unqualified
160-A pulse rail. Stop before shrinking gaps, keeper teeth or return springs.
No print, architecture selection or general rejection of electrically written
physical masks follows.

Input main `1a2129b`. Reproduce:
`python3 tools/curated-experiment-checks/E-240/screen.py` (stdlib, stdout only;
imports E-239/E-236). Evidence: **calculations, discrete state enumeration,
labelled competing bounds and dated supplier observations; self-review**.
No CAD, circuit transient solution, measured process distribution, assembled
selector, reader, qualified BOM or physical performance.

## Architectures and supported transaction

All alternatives retain E-236's five loaded strokes, seven-level column shelves,
row/column resident supports, lift, local arrest, proof and causal retry. Mask
hardware serves 80 columns per head; B5 uses 400 sites, reused across 6,400 cells.
The coils move unloaded command flags; they cannot lift columns or release
loaded support by themselves.

| Command mechanism | Write/retain/read path | Distinct burden |
|---|---|---|
| Crossed magnetic coincidence | Sum row/column fields switches local bistable state; then mechanical read | E-065's threshold/leakage bounds and E-075's repeated-pulse energy remain. Larger external spacing is not a field solution. No reopening of failed air-core cases |
| Diode matrix, opposed coils and bistable armature | Reset/set phases for every addressed group; local state survives while next group writes; read all flags before motion | Two windings, two isolated branches and one mechanical bistable site per bit. Reversing a soft pole's current does **not** reverse attraction (E-074). E-183's opening-gap remanence is not granted |
| Diode matrix, spring-return flags and group keepers | Release/reset groups while resident supports hold; pulse one group, close its keeper before current removal; repeat; read | One winding/return per site; independently retained keeper per group. A single end-of-scan clamp loses early bits |
| Direct vector, spring-return flags and common keeper | Unlock/reset all flags; energize target vector together; close keeper; remove current, wait decay and read | One winding/return per bit; one keeper/bank; full-vector peak current |

At the stationary supported datum, both resident support systems are seated and
pickups are unloaded. Withdraw the reader before changing the mask. Unlock/reset,
write, retain and prove the **physical** pattern. Only then engage selected
pickups, prove takeover, release the corresponding resident paths, execute the
stroke, reseat/prove resident support and withdraw pickups. The mask stays locked
through this entire loaded interval. Programming the next command is sequential;
no E-237 narrow overwrite overlap is credited. Mask reset is not terrain reset.
Other rows retain row supports; unchanged active-row columns retain column
supports in the inherited ideal topology.

During interrupted writing, resident supports hold; re-home and rewrite the mask.
During motion, retained commands and local arrest must hold until reseating.
Wrong proof inhibits takeover; retry regenerates from actual stable heights.
Persistent faults require supported stop/service, not a successful <30-s recovery.
A jammed keeper/false shared proof affects up to 80 sites. Output linkage,
keeper engagement, read isolation, proof and arrest remain unconstructed.

Proposed matrix circuit: selected high-side row → series isolation diode →
winding → selected low-side column. Local flyback and defined inactive-line bias
are required. Isolation blocks ideal DC reverse paths, not field leakage or
switching transients. Current decay, disable and fault detection are unresolved.
Direct channels remove row sources and series diodes.

## Complete timing, with writing inside every map

Use E-239's v=.2 m/s, a=8 m/s², 2-mm support transfers, four stages/pulse,
3-ms proof allowances, five strokes/row, row feed, 2-s aggregate setup/readback,
one complete causal row retry and 30-mm empty recovery. These are unqualified
motion/read allowances. A shared 1-MHz serial chain adds .4 ms for B5 direct data;
serial output readback alone cannot prove flag position. No free buffering.

Let K=keeper stroke time+3-ms proof, P=coil motion allowance, D=1-ms decay,
R=3-ms physical mask proof, G=ceil(80/q). Writer time is:

- Direct: `2K + P + D + R + serial`.
- Group keeper: `K + G(P+K+D) + R + serial`, granting simultaneous group reset.
- Opposed bistable coils: `2G(P+D) + R + serial`; no keeper motion but the
  bistable mechanism, set/reset energy and read isolation remain unknown.

P includes electrical rise and mechanical travel optimistically. Spring OFF
return must finish during K; slow return adds time. Current stays on while its
keeper closes. D is an assumption, not a diode or winding response specification.

| Scenario, P=10 ms | First feasible banks / sites | Calculated full map | Allocated bought cost, 100 turns/winding |
|---|---:|---:|---:|
| Direct, 1-mm keeper | 5 / 400 | 29.274 s | $497.25 |
| Direct, 2-mm keeper | 6 / 480 | 27.482 s | $532.40 |
| Matrix/group keeper, q20, 2 mm | 8 / 640 | 28.273 s | $646.59 |
| Matrix/opposed bistable, q20 | 6 / 480 | 28.100 s | $556.30 |

B5 direct with 2/4-mm keeper gives 30.848/33.075 s. The 1-mm case leaves only
.726 s total, or 8.54 ms per write transaction. Keeper travel is a sensitivity,
not a recommendation to shrink engagement. Regional visits use the same safe
transaction for each changed row and inherited seeks; no reduced force/read
latency is inferred from fewer changed bits.

## Copper, electronics and manufacturing ledger

Supplier observations on 2026-10-12, USD before freight/tax; order rounding included:

| Item | Observation / B5 direct procurement |
|---|---|
| [AOS AO3400A, LCSC C20917](https://www.lcsc.com/product-detail/MOSFETs_Alpha-Omega-Semicon_C20917.html) | $.0634 at 150+, $.056 at 500+; 400 cost $25.36 |
| [Nexperia 74HC595D,118, C5947](https://www.lcsc.com/product-detail/C5947.html) | $.0906 at 50+; 50 cost $4.53 |
| [MDD SS14, C2480](https://www.lcsc.com/product-detail/Schottky-Barrier-Diodes-SBD_Jiangsu-Yutai-Elec-SS14_C2480.html) | Undiscounted $.019 at 50+, $.0152 at 500+, $.0134 at 1500+; buy 500 for $7.60 |
| [Remington 34-AWG wire](https://www.remingtonindustries.com/magnet-wire/magnet-wire-34-awg-enameled-copper-6-spool-sizes/) | 4043/8086/20215 ft spools, $22.37/$41.76/$85.82. Variant 367/368/369 prices obtained from supplier's read-only `remote/v1/product-attributes/978?attribute%5B100%5D=…` endpoint |

[AOS's datasheet](https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf)
specifies 30 V and ≤48 mΩ at 2.5-V gate drive; this is not a transient/layout
pass. Shift registers drive transistor gates, not windings. Gate pulldowns,
decoupling, fail-disabled startup, boards and assembly remain required.

Assume 100 turns, 30-mm mean turn and 15% leads/scrap: 400 coils need 1,380 m
procured, one 8086-ft spool. At 200 turns buy one such spool plus one 4043-ft
spool for $64.13. This is whole-spool optimization, not a price per consumed gram.
Using .160-mm bare copper, resistivity 1.72e−8 Ωm (assumed room-temperature value),
100/200 turns give 2.566/5.133 Ω per winding. Supplier finished diameter is
.0070 inch (.1778 mm); insulation diameter is not the conducting diameter.

B5 direct's sourced subtotal is $79.25 at 100 turns, plus E-239's **assumed $295**
non-channel reserve. The remaining **$125.75** must buy all selector implementation
extras. Explicit allocation: boards $25, extra pulse regulation $20, pole/armature
stock $40, returns $8, keeper hardware $10, extra harness $10, passives/suppression
$5 and winding fixture $5. Total $497.25. These $123 extras are not quotations.
At 200 turns the same allocation becomes $519.62, with only $103.38 available
for extras under $500. Matrix high-side circuits add an assumed $.30/source;
independent group keepers add $2/group. A $50 increase in boards/supply/retention
changes every listed total by $50; no procurement-wide impossibility is proven.

| Functional replication | Per cell / row / B5 bank or head / board |
|---|---|
| Inherited resident hardware | 1 column, 2 guide stations, 7 shelves, 2 bearing sites per cell; 80 columns and 1 row support/row; 1280 columns/bank; 6400 columns, 12800 guides, 44800 shelves, 80 row supports/board |
| Shared support | 80 column bars +80 pickups/head; 400 of each/board, 800 inherited routing contacts; retained output/support function remains |
| Direct mask | 80 armatures, coils/bobbins, returns, keeper contacts and two-endpoint guides/head; 400 of each/board and ≥800 guide/end contacts; 5 keeper mechanisms, each with 80 failure sites |
| Electrical assembly | 800 coil terminations, 400 FETs, 400 flyback diodes and 50 shift ICs; ≥2800 SMD pin joints before passives; 5 power/data/proof module harnesses |
| q20 bistable B6 | 480 armatures/detents, 960 coils, 120 sinks, 48 source channels, 960 series +960 flyback diodes, ≥1920 coil terminations; no free reset pole |

External coils can occupy two staggered 40-site rows at 10.16-mm pitch; each
surface-pitch pair then owes two output routes. Module joints must respect the
256-mm printer. A 25-mm² pole, 30-mm mean turn and 10-mm winding length imply
about four .1778-mm wire layers at 200 turns. These are envelope assumptions,
not routed CAD; bobbin, steel return and moving clearance remain unconstructed.

B5 direct adds 400 winding/termination/core/return/flag installation operations.
At an assumed 2/5/10 min per complete selector module, this alone is 13.3/33.3/66.7 h.
A reusable winding fixture is counted; its cycle/reject rate is unknown. Assumed
.3/.6-cm³ bobbins add .12/.24 L, before mask guides; E-239's inherited 8.192-L
column stock and 152–455-h extrusion allocation remain. Reprint/rework of failed
sites, not merely filament price, matters. Accessible detachable heads improve
service but need resident support and safe writer extraction before replacement.

## Force, error and peak supply must be coupled to the cheap ledger

Ideal one-gap attraction is `F=k μ0 A (NI)²/(2g²)`. k=.25/.5/1 is a **force
model factor**, not measured efficiency; gap errors ±.15/.35/.70 mm and current
factor .85 are competing bounds, not X1C distributions. Shared voltage droop,
core batch and keeper warp can affect all sites coherently. Magnet leakage,
saturation, fringing, cross-talk, bearing friction, heating, remanent sticking,
return fatigue and creep are not solved. Positive worst-corner force is only a
necessary screen under this model.

A selected rest-to-rest 1-mm flag motion with .2-g armature and .002-N drag
uses a prescribed triangular-speed demand `.002 + 4ms/P²`: .034/.010/.004 N at P=5/10/20 ms. This grants
instant current rise and ideal acceleration/braking; it does not construct a
spring or establish settling. Comparing initial-gap force to that demand tests
this motion profile; it is not a universal pull-in bound. Initial gap 1.5 mm leaves .5 mm nominal final gap.
At +.35-mm gap error, k=.5 and −15% current, .010 N requires **77.66 ampere-turns**.
At +.70 mm it requires 92.35. A 100-turn/.4-A device yields only .002653 N in
the middle scenario; 200 turns/.4 A yields .010611 N. Even ideal k=1 needs
54.92 nominal ampere-turns there. Required load/drag is not measured.

57 timing/topology scenarios × four winding/current cases = 228 combinations.
None meets the middle force condition, assumed cost ceiling and <30 s. The
$519.62 best force survivor loses its 6% margin in the wider gap case. Do not
refine winding, keeper or gap geometry on this basis.

At .4 A ×400 the rail must carry **160 A while the keeper closes**, not merely
for the 10-ms free-motion allowance. The 1-mm keeper case keeps power on for
35.36 ms per write. At 200 turns, peak copper loss is 328.5 W; 85 all-on writes
would consume 987 J in copper alone. This all-on electrical envelope sizes the
hardware; it is not asserted to be the exact E-236 mask workload. A 5-V bus with
ballast/linear limiting would supply 800 W peak. A hypothetical 40-A source
would need ≥5.66 F to cover the current deficit over this interval at .75-V
droop (constant-current approximation). No such capacitor or regulator fits the
ledger by assertion. Higher-voltage switching regulation may reduce bus current
but adds power electronics; PWM without controlled per-coil current is not
voltage-independent force. Sequential energizing still needs all selected
monostable flags held until their common keeper closes. Matrix group retention
reduces peak concurrency by paying its extra retain/transfer phases.

## Checks and next discriminator

768 four-bit old/new command overwrites pass for the three retained abstractions;
an unretained matrix loses an explicit early selected bit. Ten allowed support
logic states check the stated inhibit rules, **not physical interlocks**. Twelve
scheduler comparisons agree with an independently expanded equation. Magnetic
pressure and ampere-turn inversion cross-check units and scaling. No unchanged
E-236 full-map replay or field integration was repeated; their scoped limitations
remain. No statistical yield or product reliability follows.

The next changed topology worth a whole-machine screen is a **single-winding
polarized retained command mask** with shared reversible power and direct
selection. Count magnets, polarity routing, read reaction, unpowered stability
and support isolation. It must remove second windings, serial keepers and powered
hold without importing E-074's soft-pole reversal error or E-183's variable-gap
EPM retention failure. No detailed flag work before a credible affordable,
broad-margin command interface; otherwise redirect support/encoding principles.
