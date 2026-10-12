---
status: complete
builds-on: [E-236, E-238, E-222]
---

# Concentrated loading changes the drive question, not the selector-cost failure

**Retain E-236's supported transaction as a comparator; park catalog direct
selectors and the sampled distributed motor/brake procurement.** The old uniform
3.27-N/cell scenario is not a miniature-load requirement. Separate payload,
concentration, moving hardware and drag: five active rows calculate **68–157 N**
across the bounds below, versus E-236's 1,624 N. This removes that force figure as
a general reason to reject shared actuation. It does not establish a working
motor, retained selector, gravity-following column or safe brake.

The direct comparator still needs **400 complete command channels**. Its lean
$295 non-channel allocation leaves **$0.5125/channel** at the $500 ceiling,
including actuator, electronics, retention, readback interfaces and installation
hardware. Sampled catalog bare actuators already cost **$1,584–3,160**. No local
finger, brake tooth, smaller contact or print is justified.

Input main `329e94e`. Reproduce:
`python3 tools/curated-experiment-checks/E-239/screen.py` (stdlib, stdout only;
imports E-236). Evidence: **calculations and bounded scenarios, dated supplier
observations, self-review**. No measured loads/process priors, CAD/contact model,
qualified BOM or physical performance. Product requirements remain unchanged;
0/10/20/30/40-mm terrain is the inherited comparison workload.

## Load is a distribution, not one force repeated 6,400 times

Assume B=5 heads of .5 kg, 3-g columns, all 80 columns/head moving, peak lift
speed .2 m/s, acceleration 8 m/s². Let P be total external payload, α its fraction
on moving columns, and f the upward guide-drag bound per moving column:

`M = B(.5 + 80×.003) + αP; F_up = M(9.81+a) + 80Bf`.

This explicitly includes payload inertia and column weight. E-236's legacy
formula used a uniform per-cell force and a fractional friction allowance;
these are different scenarios, not a numerical correction to its arithmetic.
3.27 N on every cell corresponds to **2,133 kg across the board**, or 133.3 kg
on five complete active rows. A local concentrated load need not occur everywhere.

The following are **competing bounds, not measured D&D usage**. Uniform α=5/80
is a reference only; α=1 is a conservative concentration envelope. All-on motion
is granted for load sizing even when an individual map uses fewer pickups.
No miniature size/mass or board-load limit is being imposed.

| External payload P | Uniform board F_up | All payload in active rows F_up | Concentrated input power at assumed 70% efficiency |
|---:|---:|---:|---:|
| 0 kg | 67.90 N | 67.90 N | 19.40 W |
| .5 kg | 68.45 N | 76.80 N | 21.94 W |
| 2 kg | 70.12 N | 103.52 N | 29.58 W |
| 5 kg | 73.46 N | 156.95 N | 44.84 W |

Table uses f=.005 N. Source sweeps .001/.005/.02/.05 N, a=2/4/8 m/s²;
these have no assigned probability. Guide drag shared by a warped/bias-affected
module adds coherently; it does not average down. Raising drag .005→.05 adds
18 N to the five-head demand. Moving-head mass uncertainty matters: +.5 kg/head adds
44.5 N at a=8. The .5-kg assumption is not a packaging estimate; any actuator
bodies carried by the lift must be added, or stationary mounting/routing shown. A rigid miniature bridging unequal moving tops may transfer its
whole weight to fewer contacts; equal sharing is not a local contact rating.
No tip, impact, side-force or user-hand-load qualification follows.

At r=10 mm, concentrated output torque is .679–1.569 N·m. The inherited .4-m,
12-mm steel shaft calculation (assumed G=80 GPa, end-loaded) gives .0167–.0385-mm
height-equivalent twist, versus .399 mm in the old scenario. This excludes
joints, bending, gearbox backlash and module misalignment; it is not a clearance
or shaft-design pass. Static load on all columns plus 5 kg is 237.4 N under the
same mass assumption, carried by resident supports rather than the lift.

## Gravity following ties drag to parallelism

A push-only pickup descending at a requires each **unloaded** 3-g column to
satisfy `f < .003(9.81-a)` for positive contact force. Heavy miniatures cannot
qualify empty cells. Correlated drag, binding and unequal tilt remain possible.
The source changes lift acceleration only; the four 2-mm contact stages,
writing and row feed retain E-236's fast assumptions.

| Drag bound/cell | Necessary acceleration boundary | First bank count / channels | Calculated map time |
|---:|---:|---:|---:|
| .005 N | 8 m/s² used | 5 / 400 | 26.681 s |
| .010 N | 6.477 m/s² | 5 / 400 | 27.187 s |
| .020 N | 3.143 m/s² | 5 / 400 | 29.962 s |
| .025 N | 1.477 m/s² | 7 / 560 | 27.358 s |
| .030 N | No nonnegative acceleration | — | Cannot descend even quasistatically |

Boundary equality supplies **zero contact preload**, not acceptable operation.
B5's exact 30-s acceleration boundary is 3.119807 m/s², equivalent to
.0200706-N drag with zero contact margin. The .020-N row therefore has almost
no additional allowance. Positive capture would change the mechanism and must
pay for routing, backlash, wear and loaded interfaces; it is not a free fix.

Timing retains all five physical writes, four support-transfer stages/pulse,
registration/settling, row feed, one complete causal row retry and a 30-mm empty
recovery return. B5 takes 26.681 s; B4 takes 32.445 s. Maximum additional writer
transaction at B5 is 73.664 ms/pulse, compared with the assumed 34.623 ms.
A five-row regional visit takes 10.831 s under inherited local-seek assumptions.
Power-loss/jam repair is a safe-stop obligation, not a bounded successful retry.
All 80 bank counts reproduce the predecessor scheduler; 48 mass/drag/acceleration
cases check force additivity independently. No unchanged support replay was rerun.

## Purchasable shared actuation and arrest: conditional, not selected

Supplier observations on 2026-10-12, USD before tax/freight:
[StepperOnline 17HS19-2004D-B070](https://www.omc-stepperonline.com/nema-17-stepper-motor-0-52nm-73-64oz-in-with-24v-3-7w-electromagnetic-brake-17hs19-2004d-b070)
lists $28.05 at five, .52-N·m motor **holding** torque and .7-N·m power-off
brake, 24 V/3.7 W. Its [datasheet](https://files.omc-stepperonline.com/17HS19-2004D-B070_Full_Datasheet.pdf)
is not a qualified response/energy test for this load.
[DM542T](https://www.omc-stepperonline.com/digital-stepper-driver-1-0-4-2a-20-50vdc-for-nema-17-23-24-stepper-motor-dm542t)
lists $19.02 at five; it is open-loop and has no brake output. Five motor/brakes
plus drivers cost **$235.35**, before supply, brake switching and transmission.

Compare one shared geared source with five independently stopped belt/capstan
heads. Both keep the E-236 support transaction. For a bank radius r=.01 m,
ratio R, assumed efficiency η=.8 and input-equivalent rotary inertia J,
`τ = F r/(ηR) + J aR/r`. At R=1, J=10⁻⁵ kg·m², a=8 and f=.005:

| Payload on one moving row | Required motor torque at 191 rpm | Static brake torque |
|---:|---:|---:|
| 0 kg | .178 N·m | .073 N·m |
| .4 kg | .267 N·m | .112 N·m |
| 1 kg | .400 N·m | .171 N·m |
| 2 kg | .623 N·m | .269 N·m |
| 5 kg | 1.291 N·m | .563 N·m |

A hypothetical available .30 N·m **at 191 rpm** allows only .549 kg payload/bank;
.45 allows 1.223 kg. These are tipping points, not this motor's measured curve.
J=5×10⁻⁵ adds .032 N·m at R1. R2 halves load torque but doubles rotor acceleration
and speed to 382 rpm; it cannot inherit a low-speed torque figure. A common
source sees summed load and needs its own reduction/speed curve. Holding torque
cannot establish the advertised motion profile; driver voltage/current, inertia,
resonance, brake release and thermal duty remain unresolved.

Power-off sequence: preserve selected pickups mechanically, arrest lift, then
read actual supported heights before resetting. A motor brake stops only an
intact downstream transmission. Retain a local arrest/support obligation for
belt/shaft disconnect; counting the motor brake must not delete it.

Even granting .7 N·m as instantaneous constant **dynamic** brake torque after a
10-ms delay, zero reflected inertia and no helpful friction, a bank carrying
1 kg drops **3.951 mm** from .2 m/s downward; 5 kg drops **21.119 mm**. Delay alone
contributes 2.491 mm. At 20 ms these become 8.542/38.869 mm. These are conditional
physics calculations, not sourced response times or measured stops. Rotor/load
energy, holding-vs-dynamic torque and structural interception need qualification.
Static torque margin alone cannot substantiate continuous safe support.

## Direct selectors and complete-machine ledger

| Catalog actuator | Observed bare unit price | 400 units | Extra channel obligations |
|---|---:|---:|---|
| [Adafruit 2776](https://www.adafruit.com/product/2776) spring-return solenoid | $3.96 at 100+ | $1,584 | Transistor, suppression, retained selection, proof, harness, mount |
| [Adafruit 858](https://www.adafruit.com/product/858) geared stepper | $3.96 at 100+ | $1,584 | Multiple drive outputs, endpoint proof, unpowered retention, coupling |
| [Pololu 2818 FS90](https://www.pololu.com/product/2818) servo | $7.90 at 5+ | $3,160 | PWM distribution, power, external state proof, unpowered retention |

These observed offerings reject these procurement routes **before** completing
an optimistic BOM; they are not global price floors or confirmed 400-unit quotes.
The solenoid lists 3-mm travel, 1.1 A at 5 V and spring return: 400 energized
continuously would draw 440 A/2.2 kW and weigh 5.04 kg bare. A pulse-driven latch
can change duty, but adds retention and still owes write/read timing. Power loss
must not retract a selected support. The geared stepper supplier recommends
under 6 rpm at 5 V; a 2-mm arc at 10-mm radius alone takes >.318 s, versus the
73.7-ms budget. A larger arm changes force, footprint and retention. FS90 lists
.10 s/60° at 6 V, not a loaded switch-and-proof time; internal position control
does not prove the linked support or promise unpowered holding.

E-236 replication remains: **6,400 columns, 12,800 guide stations, 44,800 shelf
levels and 12,800 resident bearing sites**; 80 row supports. Each 16-row bank
contains 1,280 columns and 80 shared column bars, pickups and retained commands.
Board totals: 400 bars/400 pickups/400 bits, 800 command endpoints and 800 routing
contacts. Catalog drives add 400 actuator assemblies, harness connections,
mounts and proof/retention interfaces, not fewer column features. Solenoids add
400 returns; servos/geared steppers add hundreds of gear trains. Fewer purchased
lift motors do not erase these failure sites.

Inherited 8.192-L gross column stock, 152–455-h assumed extrusion and ≥8.89-h
column insertion remain comparison allocations; these are not sliced estimates.
Five catalog bank lifts add five motor-brakes, drivers and local transmissions;
a common source needs five enable/retention branches instead. Both owe segment
joints, wiring, inaccessible-guide service and temporary supported repair. Reader
coverage, finite bridges, interfaces and force-rated hardware remain unbuilt.
Common comb height bias can move unchanged terrain by up to 2e in the inherited
±e scenarios (.15/.35/.70 mm); neither lighter loading nor catalog actuators
qualify FDM margin, creep, wear, column alignment or correlated error.

Source itemizes the lean non-channel $295 reserve: $195 common plus $20/bank,
including power, frame, controller, wiring, freight, motion, readers, mounts,
enables and local arrest. These remain **allocations**. Replacing only its $40
common motor/driver/brake with the quoted five-axis $235.35 set gives **$490.35**
before channels. Local downstream arrest stays counted. The remaining complete
channel cap is $.024125; the same ledger with $3.96 bare selectors is already
$2,074.35, excluding their channel extras. Shared common-drive allocation plus
those bare selectors is $1,879. No power-supply adequacy is claimed.

With non-channel reserves $0/$150/$250/$295, a 400-channel machine permits
$1.25/$.875/$.625/$.5125 per **complete** channel at $500. Even free shared
hardware does not save the three sampled catalog routes. This is a sharper
stop condition than refining motor power from an assumed $30 line item.

## Decision and next discriminator

Lighter, concentrated load scenarios improve shared-lift plausibility and shaft
stiffness. Catalog selector multiplicity, unpowered retention, gravity drag and
local arrest still prevent choosing a machine. Stop catalog direct-channel
procurement and fine mechanical refinement; retain the parametric load model
and supported five-stroke sequence. No print or product-load restriction follows.

A bounded next investigation may compare **bulk electrical writing of a reusable
external binary mask** (matrix-addressed magnetic state with shared read/actuation)
against the parked mechanical writers. Before any coil, latch or contact detail,
construct complete write/retain/read/isolate phases and a 400-site copper,
driver, power, routing and assembly ledger against the $.5125/channel and
73.664-ms write ceilings. Count half-selection, return/retention, common-cause
faults and actual support isolation. This is an unselected changed programming
route, not a claim that printed coils, cheap relays or matrix addressing supply
free motion/state. Stop if cost, retained-force margins or another serial
transfer erase its system benefit; return to different support/encoding principles.
