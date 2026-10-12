---
status: complete
builds-on: [E-240, E-239, E-074, E-183]
---

# Polarized commands remove powered hold, but the tested machine still misses

**Park the screened 90-degree permanent-magnet mask before detailed flag design.**
Single-winding signed torque and passive retention remove E-240's common keeper
strokes and allow serial groups without holding earlier groups electrically.
That is a real architectural improvement. It does not yet buy an affordable,
robust machine: the only sampled <$500 allocation needs four banks and a 5-ms
write; its prescribed motion fails even an optimistic barrier-free energy check
under the selected field/inertia bounds. Five banks relax writing but allocate
$531.59–573.35 for 50–200 turns before any qualified reader or power system.
No blanket rejection of polarized masks, no selected machine and no print.

Input main `9ba3669`. Reproduce with
`python3 tools/curated-experiment-checks/E-241/screen.py` (stdlib; stdout only;
imports E-240/E-239). **Evidence: calculations, ideal state enumeration, supplier
observations and explicitly chosen bounds; self-review.** No field/contact FEA,
CAD, process probability, winding transient, measured switching or hardware pass.

## Changed topology and complete transaction

An axially magnetized disc is fixed in a pivoted flag, with its magnetic axis
rotating through ±45 degrees about a perpendicular pivot. A transverse coil field
has signed torque `m B cos(theta)` throughout the sweep: reversing current really
reverses torque, unlike E-074's soft pole. Two stationary steel targets are proposed
to create endpoint retention; their actual potential is **unconstructed**. This
rotates a hard magnet instead of reversing an opening-gap soft magnet (E-183).

Compare three paths: E-240 monostable coil/common keeper; E-240 opposed-coil
bistable mask; one-winding polarized flag with local H bridge. The last removes
returns, second windings and keeper motion, but adds purchased magnets, signed
drivers, magnetic interaction and reader-reaction constraints. A single shared
H bridge plus one ordinary low-side transistor per flag is **not** a complete
bidirectional isolated circuit. The costed control therefore gives every flag
its own complete bridge; shared supply is not free shared selection.

At a stationary supported datum, withdraw the mechanical reader and leave both
resident support paths seated. Write selected groups with either sign, extinguish
current, retain each group, then prove the physical pattern. A bridge can write
both signs in the same group; no reset-all or second polarity phase is needed.
Engage/prove pickups, release only selected resident paths, execute the inherited
loaded stroke, reseat/prove supports and unload/withdraw pickups. Only then rewrite.
The flag is command memory, **not terrain support**. Its mechanical reader must
resist reaction throughout use or transfer it into a grounded stop; the latter
is an unresolved extra interface, not a free latch.

During interrupted writing, resident supports hold; rewrite and prove the mask
before motion. During motion, command retention plus local output arrest remain
necessary. A bit proof does not prove load support. Retry uses actual stable
heights, not blind replay. Persistent jam/false proof requires supported shutdown
and accessible head service. Other rows remain resident-supported; unchanged
active-row cells retain their column supports in the inherited ideal topology.
No regional-disturbance or dynamic-arrest qualification is added.

## Whole-machine timing and procurement

Keep E-239's five strokes/row, four 2-mm support transfers/stroke, .2-m/s speed,
8-m/s² acceleration, 3-ms support proofs, row feed, 2-s setup/readback, one full
causal row retry and 30-mm empty reset. Gravity following still limits that
acceleration. For q simultaneous bits/head and pulse P:
`write = ceil(80/q)*(P+1 ms decay) +3 ms mask proof +160B/1 MHz`.
P grants current rise and settling within the pulse; these allowances are
unqualified. Physical writing is charged on first use and retry, with no buffering.

| Calculated case | Banks / flags | Full map | Allocation |
|---|---:|---:|---:|
| P5 ms, q80, 50 or 100 turns | 4 / 320 | 29.822 s | $481.75 |
| P10 ms, q80, 100 turns | 5 / 400 | 24.997 s | $550.98 |
| P10 ms, q20, 100 turns | 5 / 400 | 27.802 s | $550.98 |
| P20 ms, q80, 200 turns | 5 / 400 | 25.847 s | $573.35 |

B4 requires P<6.694 ms even at q80. B5/P20/q20 instead needs 31.202 s.
Grouping exchanges peak power for time without adding E-240 group keepers.
Regional rows use the same supported transaction and seek allowances; no free
regional acceleration or relaxed verification is inferred.

Supplier observations, 2026-10-12, USD before freight/tax:

- [LCSC TI DRV8837DSGR C39159](https://www.lcsc.com/product-detail/_Texas-Instruments-DRV8837DSGR_C39159.html):
  $.1684 at 150+, $.1428 at 500+. 320/400 devices cost $53.888/$67.36;
  buying 500 costs $71.40. Search snippets had cheaper stale tiers; use this page.
- [K&J D21](https://www.kjmagnetics.com/d21-neodymium-disc-magnet):
  ten-pack $1.32, 50 packs $1.20/pack. 320/400 magnets cost $42.24/$52.80.
  Axial N42, 3.175×1.5875 mm nominal, ±.1-mm listed tolerance, .09-g listed
  mass and Br **maximum** 1.32 T. Neither steel pull rating nor surface field
  predicts this rotor's torque/retention.
- E-240's dated wire/74HC595 observations are reused, not re-quoted: B4 50/100
  turns fit one $22.37 spool; B5 100/200 turns cost $41.76/$64.13. Two input bits
  per bridge require 80/100 shift packages ($7.248/$9.06).

[TI's datasheet](https://www.ti.com/lit/ds/symlink/drv8837.pdf) supplies the full
bridge, bidirectional output, high-impedance coast and typical .280-ohm bridge
resistance. It does not supply regulated coil current or prove our pulse response.
Use fail-disabled startup, defined inputs, decay handling and supply decoupling;
thermal shutdown/retry is not terrain fault recovery. The 2×2-mm exposed-pad
package needs PCB/reflow assembly. No simpler transistor count is credited.

Reserve remains E-239's **assumed** $195 common+$20/bank, including its $20 shared
writer-drive allowance conservatively. Added allocations: PCB $25, pulse-power
upgrade $20, steel targets/pivots $.05/site, harness $10, passives $5 and winding
fixture $5. These are not quotations. B4 leaves $99.25 for extras versus $81
allocated; B5/100 turns leaves $34.02 versus $85. Reducing the whole reserve by
$50 changes the ranking; neither these allocations nor sampled suppliers prove
an absolute price floor. Current regulation, field shields and load-isolating
readers cannot silently consume zero of the remaining allowance.

## Retention, motion, broad error and interference bounds

Use a thin finite air-core solenoid, nominal radius 5 mm, length 10 mm, 30-mm mean
turn. On-axis field is integrated analytically; field factor .25/.5/1 represents
unresolved geometry/model error. Error .15/.35/.70 mm increases coil radius and
length and offsets the magnet axially. This is a competing manufacturing envelope,
not a precise X1C prior or an off-axis field solution. Assume working Br=1.2 T,
magnetic moment factor .85, current factor .85, complete rotor .2 g with 2-mm
radius of gyration (`J=8e-10 kg m²`), friction torque 6 µN m and a 2-µJ shock.
Coil/core batch, supply droop, frame warp and target spacing may vary coherently.

For an illustrative unpowered potential `U=E cos²(pi theta/(2a))`, a=pi/4,
±30% barrier variation and reader force f at 3-mm lever:

- Retention certificate: `E_low=(f*.003*a+2e-6)/.7`.
- Conservative prescribed-motion certificate:
  `E_high=[m B cos(a)−6e-6−4J(2a)/P²]*(2a/pi)/1.3`.

A nonempty interval certifies only these energy/torque inequalities. Empty
intervals are **not universal switching impossibility**: torque extrema do not
coincide, and other waveforms/potentials may work. The model does not construct
endpoint targets, damping, braking or repeat-pulse immunity. Field can vary over
the finite magnet; the lumped moment is only a screen.

256 timing/winding/current cases (P5/10/20/40 ms; q10/20/40/80; N50/100/200/400;
I .2/.4/.8/1.2 A) have no certificate at f=.010 N, middle error/factor, within a
5-V coil+typical-bridge voltage allowance. None meets that certificate and <$500.
At B4/100 turns/1.2 A/P5, minimum modeled drive torque is 30.50 µN m while
prescribed inertial torque is 201.06 µN m. Independently, magnetic work to the
midpoint is 30.50 µJ against 157.91 µJ required kinetic energy, **before** barrier
and drag. That prescribed trajectory fails under these assumptions even with
zero barrier; a smaller rotor/different stroke is a changed embodiment.

N200/.8 A/P20 gives E_high=8.50 µJ. A .010-N reader needs E_low=36.52 µJ;
zero reader needs 2.86 µJ. Maximum certified reader force is only **1.677 mN**
under this particular envelope. Consequently contact-free command sensing might
retain state, but transferring that sensed command to a load-isolated mechanical
selector still owes its own hardware. Do not turn this result into a tiny detent
or tighter magnetic-gap campaign.

Direct electrical isolation does not isolate fields. A dipole-norm sum for all
other magnets in one 80-site head gives the following **upper screening bounds**,
not actual fields or necessary failures. Use maximum listed Br and +.1-mm magnet
size; neighbor coils use 160 AT and 5-mm radius. No shield/core is granted.

| Packing | Center span | Permanent / energized-neighbor bound |
|---|---|---:|
| 40×2, 10.16-mm pitch | 396×10 mm | 12.60 / 10.60 mT |
| 20×4, 20.32-mm pitch | 386×61 mm | 2.461 / 2.071 mT |
| 10×8, 40.64-mm pitch | 366×284 mm | .344 / .290 mT |

Bounds may be loose, especially at the closest spacing; actual vectors, extended
magnets, steel targets and other heads are unsolved. Middle-scenario selected
field is only 5.638 mT at 160 AT. Thus even external spacing does not justify
zero cross-talk. The tight packing also overlaps a 10.7-mm adverse coil diameter;
use wider/staggered routing if reopened. Larger footprints add linkage length,
compliance, read force and service space, not just free spacing.

At N200/.8 A/P20, q20/B5 draws 80-A summed coil current, 328.5-W peak copper,
versus 320 A/1314 W at q80. All-site pulse allowance consumes 2234 J/map; this
sizes a conservative electrical workload, not the exact terrain-mask population.
Grouping leaves total copper work unchanged. A 5-V bound is 400/1600 W respectively;
PWM can reduce bus demand but needs regulation and qualified rise/decay/layout.
Unpowered retention removes hold energy, not switching energy or a real supply.

## Replication, service and decision

| Functional inventory | Per cell / row / bank-head / board at B5 |
|---|---|
| Resident support | 1 column, 2 guide stations, 7 shelves, 2 bearing sites/cell; 80 columns+1 row support/row; 1280 columns/bank; 6400 columns, 12800 guides, 44800 shelves, 80 row supports/board |
| Shared output | 80 bars+80 pickups/head; 400 each and 800 inherited routing contacts/board; local arrest still required |
| Mask | 80 rotors, magnets, windings/bobbins, pivots and two endpoint targets/head; 400 each except 800 targets/board; 400 pivot interfaces+800 endpoint contacts plus 400 reader sites |
| Electronics/assembly | 400 bridges, 100 shift ICs, 800 coil terminations; ≥5200 IC pad joints including bridge exposed pads, before passives; 5 head harnesses |

No mask spring, insert socket or independently moving keeper is assumed; steel
inserts/axles and magnet fixing still need construction. One printed strip does
not remove 80 retention/read failure sites. At 2/5/10 min per installed, wound,
polarized and terminated selector, added labor is 13.3/33.3/66.7 h. Assumed bobbins
.3–.6 cm³ add .12–.24 L, excluding rotors/housings; E-239's inherited 8.192-L
column stock and 152–455-h extrusion allocation remain. Modular flat bobbins
and split pivot housings could avoid support-intensive prints, but there is no
routed orientation/time/scrap estimate. Printed poles do not replace steel.
Correlated warp can spoil an entire head; wrong magnet orientation is an assembly
fault. Detachable head replacement must leave terrain resident-supported.

Keep the benefits of retained group programming as a comparator; stop local
polarized-mask refinement. Next compare a **shared traveling field writer** that
writes passive external flags without one winding/driver per flag against this
direct bridge control. First charge arbitrary-pattern writes, return/registration,
old-bit isolation, reader reaction, field spread and all necessary axes; determine
whether writer reuse saves enough hardware within the real map boundary. If even
that cheapest screen fails, redirect support/encoding, not magnetic gap tuning.

Checks: 768 four-bit overwrites, 1792 retained group observations, 10 ideal support
logic states and 18 independent schedule expansions. Ring-field quadrature at
32/128/512 intervals converges to the analytic field (relative error
1.22e-4/7.63e-6/4.77e-7); energy derivatives and field scaling/symmetry agree.
The independent midpoint work test checks the selected failed trajectory.
These are model-consistency checks, not independent validation or physical proof.
