---
status: complete
builds-on: [E-256, E-258]
---

# Sourced rotary channels and feedback budget

**Cheap rotary power remains plausible; the $4 complete-channel allocation is not
supported by the sampled catalog assembly.** The 64×64 research case leaves about
$4/output for feedback, transmission, docking and reserve corrections after buying
basic motors/drivers. The approximately $1,000 case leaves only $0.12/output.
An encoder-equipped catalog gearmotor exceeds $1,500 on motors alone.
These are scoped catalog comparisons, not a market price floor or a selected machine.
The later 2-mm-lead sensitivity below removes the apparent 30-s margin at the
old 2000-rpm setting; measure the pair and compare drive ratio before adding heads.

Reproduce: `python3 tools/curated-experiment-checks/E-259/channel_screen.py`.
Evidence: supplier listings checked **2026-10-12**, deterministic calculations and
unchanged E-258 conditional map schedules. No motor tests, production quotes,
finite head layout, physical qualification, print or purchase. The original screen
preserved alternative terrain policies. The extension below uses the subsequent
owner preference for physical river/ravine relief and selectable depth (E-258).

## Purchased inputs and compatibility

Prices are USD before applicable tax/shipping; stock listings are not quantity
reservations. Supplier ratings are not measurements of our assembled system.

| Supplier part | Observed price at actual quantity | Useful specification / unresolved duty |
|---|---:|---|
| [Adafruit 711 motor](https://www.adafruit.com/product/711) | $1.56 at 100+ | 6 V; 10 gf·cm rated load; 4500±1500 loaded rpm; ≤250 mA loaded, ≤500 mA stall; 27.5×20×15 mm, 17.5 g. No encoder or gearbox. |
| [Adafruit 3297 dual DRV8833 board](https://www.adafruit.com/product/3297) | $5.36 at 10–99 **boards**, $2.68/output | Two reversible channels, default 1-A current limit, 2.7–10.8 V supply. 64/80 boards, not 128/160, are needed. The $4.76 tier requires buying 100 boards and costs more overall. |
| [Pololu 5180 integrated encoder gearmotor](https://www.pololu.com/product/5180) | $25.27 at 100+ | 9.96:1, 12 encoder counts/motor revolution, 3300 typical unloaded rpm at 6 V. Cables excluded. [Specs](https://www.pololu.com/product/5180/specs) give 2300 rpm at 0.042 kgf·cm/0.51 A at maximum efficiency; no-load speed is ±20%, not a guaranteed loaded curve. |
| [Pololu 3081 encoder pair](https://www.pololu.com/product/3081) | $8.42/pair at 25+, $4.21/output | Requires compatible extended rear shaft. **Not a plug-in encoder for motor 711.** A custom attachment would need its own geometry and price. Used only as a feedback-price comparator. |

The compatible motor/driver subset is 711+3297: voltage and catalog current are
within the board's stated range, without proving thermal performance, PCB layout,
regeneration handling or a complete feedback channel. The motor has preattached
leads; connector, power distribution and control wiring still require assembly.
5180+3297 is another electrical subset, but the board's default 1-A limit is below
5180's 1.5-A stall extrapolation: do not claim that stall performance is available.

## Board accounting before unknowns

Preserve E-255's **unquoted** reserve: $250 common, $.02/resident site, $55/head.
This includes only $40 for power/protection and $20 for controller hardware;
those allowances are not ratified by the electrical counts below. Two heads have
128/160 outputs at 64/80 columns. Table totals mix quoted subsets with that reserve;
**none is a complete BOM or finished selling price**.

| Two-head board | 64×64 / 6.35 mm | 80×80 / 5.08 mm |
|---|---:|---:|
| Resident pairs/seats/sockets/antirotation duties | 4096 each | 6400 each |
| Independent motor/dock/feedback/output duties | 128 each | 160 each |
| Unquoted non-channel reserve | $441.92 | $488.00 |
| 711 motors + 3297 drivers per output | $4.24 | $4.24 |
| Reserve + motor/driver subset | **$984.64** | **$1166.40** |
| Remaining/output under $500 / $1000 / $1500 | −$3.79 / $0.12 / **$4.026** | −$4.17 / −$1.04 / **$2.085** |
| 5180 encoder motors alone | $3234.56 | $4043.20 |
| Reserve + 5180 motors + 3297 drivers | $4019.52 | $4960.00 |
| Add 3081 price comparator to basic subset (not compatible assembly) | $1523.52 | $1840.00 |

No missing duty is zero: each basic output still needs feedback or an equivalent
observable control route, output spindle/journals, transmission, retained/self-aligning
socket, docking accommodation and cable service. Shared actual-height proof,
controller/encoder capture, current distribution and transport must also fit.
The original $4 allowance cannot buy even these sampled motors/drivers. Custom
assembled electronics, cheaper sensing or another vendor could change that result;
no price is assigned without a quotation. Automated PCB assembly is a credible
route to investigate rather than hand-wiring 64/80 breakout boards. It is not yet
a costed solution, and Sander's willingness to consider premium value is no purchase
authority.

At supplier rated-load current, simultaneous motors alone require **32/40 A at 6 V
(192/240 W)**; simultaneous stall is 64/80 A. Actual screw loads/PWM may use less.
Neither number is a predicted map average or a required continuous supply rating;
current limits, simultaneous startup and bank staggering must be designed together.
Staggering outputs changes the parallel schedule. Driver, encoder and controller
power is additional. Motor-only mass is **2.24/2.80 kg**; at inherited 5 m/s² carriage
acceleration each half-board needs 5.6/7.0 N just for those motors. Guide, carrier,
transmission and cable loads remain additional.

The 15-mm narrow body dimension requires at least **three staggered motor lanes**
at either pitch, even granting zero mounting clearance. Motors cannot all be
coaxial in one pitch-spaced row. Three lanes establish no collision-free shaft
routing; placing motors off-board exchanges mass for shafts/cables and compliance.
At least 128/160 torque paths and dock interfaces remain. An illustrative single
minute assembling/testing each shared channel adds 2.13/2.67 maker hours, before
resident E-255 insertion labor, jigs and rework; it is not a measured assembly rate.
Printed/cast shared carriers or machined spindle plates may help alignment, but
molding does not remove the purchased drive and feedback duties.

## Torque, feedback and useful speed bounds

The basic motor's rated torque is **0.980665 N·mm**. A **hypothetical** 1.5:1 reduction
at .7 efficiency converts its lower listed loaded-speed endpoint to 2000 output rpm
and 1.0297 N·mm. This is an operating-point transformation, **not a rated transmission
or acceleration prediction**. E-256's illustrative 20-g/.3-friction/.05-N·mm-drag
case needs .2954 N·mm at 1000 rev/s² before rotating inertia. Available excess would
permit effective screw-side J only up to about **1.17e−7 kg·m²** in that model.
Motor rotor, gear, shaft and socket inertia/loss are unmeasured; 1e−6 fails the same
necessary bound. The favorable earlier J=1e−8 is not a catalog motor specification.
Neither high free speed nor a stall torque establishes the required ramp.

At fixed rated load and voltage, using a duration based on 4500 rpm for a nominal
10-mm move gives **6.67–13.33 mm** across the stated 3000–6000-rpm range (constant-speed
illustration; startup adds error). PWM duty is not position feedback. With the exact
5180 ratio1295/130 and12 counts/rev, nominal screw motion is .02510 mm/count and
2000 output rpm produces3984.6 edges/s/output: **510,031/637,538 edges/s** across
128/160 outputs. This is a controller capture workload, not an accuracy claim.
Encoder position is upstream of gearbox backlash, coupling and screw engagement.
A missed socket can produce all expected motor counts with no pin motion. Preserve
shared actual-height verification and local retry; do not substitute encoder ticks
for E-258's unqualified20-ms proof allowance. At100 mm/s pin speed, 1/5/20-ms latency
alone adds .1/.5/2 mm before stopping distance.

[TI DRV8833 Rev E, §§7.3.2 and7.3.5–7.4](https://www.ti.com/lit/ds/symlink/drv8833.pdf)
distinguishes powered short-circuit braking from coast; sleep and undervoltage
switch the bridge off. A command to brake is not a power-loss holding mechanism.
Resident threaded support remains the pin load path, consistent with Sander's
positive static-hold observation. Stop, prove, withdraw; unexpected moving loss
remains a separate caught-load test. Do not add thousands of brakes merely because
that test has not yet been measured.

## Timing and next discriminator

E-258's three scene policies are retained, with real neutral20/30 and respective
40/50-mm required ranges, both pitches, 1500/2000 output rpm and200/1000 rev/s².
Startup is separately charged; homing and manual/visual workflow remain unknown.
All comparisons retain transport, docking, one row retry and the4-s common budget;
none demonstrates a complete player-ready update.

At **64×64 / neutral20 / depth20**, mixed-policy B2 maxima are **22.08 s** at
2000rpm/1000rev/s², **25.28 s** at1500/1000 and **26.48 s** at2000/200. Thus the
original dense-grid fast ramp is not automatically required by the coarser comparison.
At1500rpm/200rev/s² the same mixed case is28.57 s, while neutral30/depth30
needs32.97 s; the added physical depth matters to this trade. At80×80/neutral20,
2000rpm/200rev/s² needs31.50 s. Initial neutral20 preparation at64 is18.28 s
for2000/1000 versus23.51 s for1500/200, before homing. Separate dense±40-mm
stress is24.88 versus32.31 s for those two settings. The executable reports all
physical/visual policies and depths, plus±50-mm full-range stress for neutral30. The~30-s comparison
is not an automatic product rejection gate.

**Next useful discriminator remains one actual retained screw pair driven and
observed under realistic load**, including inertia, ramp, bidirectional torque,
stop/withdrawal and missed engagement. Measure before selecting an entire motor
bank. Cheap bare motors have sufficient catalog-scale torque to justify that
investigation; neither the timing nor the cost screen establishes a buildable head.
Custom feedback/driver assembly deserves a bounded quotation only if that test
preserves the operating window. No new micro-thread CAD or resident latch campaign.

Verification: independently reconciled quantity tiers/residual budgets, gf·cm
conversion, inertia tipping point, E-258 timing anchor, no-op and signed controls.
Self-review; no independent validation or physical test.


## Concurrent-output admission — 2026-10-13

Reproduce: `python3 tools/curated-experiment-checks/E-259/concurrency.py`;
`--check` runs only verification. **Deterministic simulation, no physical test.**
Keep all64/80 independent motors/head but allow at mostK powered simultaneously.
Each changed cell gets one signed rest-to-rest move on its own motor. An admission
slot is electrical permission, not a mechanical multiplexor. Idle/finished outputs
retain E-255's assumed screw hold; feedback, docks and all installed motors remain.

Longest-duration waiting moves start in the earliest available slots (LPT).
Each row has a feasible schedule; its lower bound is the larger of total duration/K
and `ceil(j/K)*t_j` for each descending duration. LPT need not be optimal: the source
includes a7-unit schedule with a6-unit exact optimum. Bounds propagate through the
**inherited accounting**:4 s + slowest bank + globally longest full-row retry.
That retry charge is conservative, not the tight adversarial wall-clock optimum;
the lower bracket does not bound different routes, globally shared slots or retries.
Preserve80-ms dock/release,20-ms row proof, actual seeks and empty return. Moves
include individual acceleration/deceleration; waiting adds no partial stops.
Base token release is instantaneous after the modelled stop; an additional5-ms
per-move occupancy probes unmeasured stop/current-settling delay.

Workload: E-258 physical river/ravine, ground30 and shallow20/deep30 presets at both
pitches:6 initial commands and30 directed state transitions. Duplicates/no-ops do
not add map evidence; these remain three convenience maps, not representative play.
Ground20/40-mm-travel control has identical shallow deltas; fixed ground30 requires
the unqualified50-mm range. Preparation, same-ravine switching and dense50-mm
stress are separately charged. Homing/manual/visual workflow remain unqualified.

**At64×64, K32 preserves the25.38-s scene maximum while halving powered outputs
from128 to64. K24 takes28.62 s.** At2000 output rpm/1000 rev/s², seconds are:

| Grid / K per head | Shallow scene max | All preset/scene max | Ravine20→30 | Cold ground30 prep | Dense50 stress | Loaded / stall motor A |
|---|---:|---:|---:|---:|---:|---:|
|64 /16|28.18|34.18|19.38|54.58|80.98|8 /16|
|64 /24|23.95|28.62|16.98|43.58|63.38|12 /24|
|64 /32|22.12|25.38|14.98|32.58|45.78|16 /32|
|64 /64 full|22.08|25.38|14.98|21.58|28.18|32 /64|
|80 /32|28.07|33.50|19.40|52.67|77.27|16 /32|
|80 /48|26.07|30.13|17.13|39.00|55.40|24 /48|
|80 /80 full|26.03|30.13|17.13|25.33|33.53|40 /80|

Scene sparsity/unequal moves absorb staggering atK32; uniform dense moves cannot.
At64/K32 dense50 needs two waves/row;K24 needs three. Initial neutral is paid.
The64/base sweep first has a lower bracket≤30 atK22 and an LPT witness≤30 atK23
(28.92 s); K22 is **not** proved impossible. K24's bracket is28.18–28.62 s.
At1500 rpm/1000 rev/s²,K29 gives29.93 s but5-ms release raises it to30.12;
K32 gives29.67/29.84 s. At2000/200,K32 gives29.85/30.02 s: a fragile boundary.
At1500/200,full concurrency gives32.97 s deep;K32 shallow gives28.70 s.
These are correlated machine-rate scenarios, not calibrated motor/process priors.

[Adafruit711](https://www.adafruit.com/product/711), rechecked2026-10-13, lists6 V,
250-mA loaded and500-mA stall maxima under its stated conditions. Two K-slot banks
yield **0.5K A loaded / K A stalled**, motor-only arithmetic, not measured screw
consumption or a validated startup/supply rating. PWM, regeneration, controller,
driver losses, current-limit tolerance and fault isolation remain unresolved.
Admission must wait until the prior output ceases drawing power; stationary active
braking also uses budget. An indefinite jam cannot be covered by the one retry.
Stop/hold/current confirmation is unimplemented, bounded only by stated delays.

**Decision:** retainK24–32 as a64-grid control option; compare a future measured
current trace withK32. Installed count alone does not require simultaneous starts.
An8-A loaded-current arithmetic case(K16) takes34.18 s deep, not<30. Slower dense
and setup operation may be worthwhile;30 s remains a reference, not a safety gate.
All4096/6400 resident pairs,128/160 drive/feedback/dock duties,2.24/2.80-kg motor
mass and$984.64/$1166.40 quoted-subset-plus-reserve remain unchanged. No supply,
assembly, print or bought-cost saving is booked; the$500 case and$1000/$1500
missing-channel/reserve qualifications remain. No hardware or purchase selected.

Verification:729 exhaustive small-row comparisons; no-overlap/one-visit witnesses;
nonoptimal-LPT counterexample; both pitches/all36 full-slot E-255 anchors; signed,
no-op and exact dense-wave controls. Self-review. Pair hold/drive/current/stop
measurements remain the physical discriminator; this screen does not replace them.

## Lead, gearing and head-count sensitivity — 2026-10-13

Reproduce: `python3 tools/curated-experiment-checks/E-259/lead_sensitivity.py`;
`--check` runs verification only. **Conditional calculations**, responding to
E-256's rough owner estimate of 2 mm/turn. Compare 2 and historical 3 mm/turn;
neither is a calibrated uncertainty bound or identification of the successful CAD.
Reported 1-mm free play is not silently converted into a lead correction.
No geometry, engagement, friction or physical qualification is inferred.

Retain the same 36 scene/preset commands, physical river/ravine, ground 30,
shallow 20/deep 30, 50-mm required range, and 64/80 grids at 6.35/5.08-mm pitch.
The ground 20/40-mm control has the shallow deltas. All times include inherited
docking, proof, seeks, return, conservative row retry and 4-s common allowance;
unknown homing and actual proof remain unpaid qualifications. Default acceleration
is 1000 rev/s²; K denotes simultaneously powered outputs **per head**.

| Grid / heads / K | Lead mm | Output rpm | Shallow max s | All preset max s |
|---|---:|---:|---:|---:|
|64 / 2 / 32|3|2000|22.12|25.38|
|64 / 2 / 32|2|2000|27.32|32.23|
|64 / 2 / 64|2|2000|27.28|32.23|
|64 / 2 / 32|2|3000|22.68|25.93|
|64 / 3 / 32|2|2000|20.28|23.40|
|80 / 2 / 80|2|2000|32.53|38.68|
|80 / 3 / 32|2|2000|27.62|33.74|
|80 / 3 / 64|2|2000|24.92|28.97|

At 64/B2/K32, changing lead 3→2 raises the maximum by **27%, not 50%**; unchanged
overheads and motion ramps remain. Increasing K32→64 does not fix the critical
row-duration limit. The calculated 30-s boundary is approximately 2262 rpm at
1000 rev/s², with no operating margin. At 200 rev/s², even unbounded speed gives
32.04 s for this LPT schedule; full concurrency still needs 31.69 s, so merely
raising top speed cannot reach 30 s in that acceleration scenario. These are
schedule limits, not hardware failures or reasons to reject a 32-s enjoyable update.

Setup and dense stress worsen separately. At 64/B2/K32/2000 rpm, cold ground 30
preparation is 42.48 s and dense 50-mm motion 62.28 s, versus 32.58/45.78 s at lead 3.
With K64 these become 26.53/36.43 s. Same-ravine 20→30 takes 16.63 s at K32;
the unchanged ground stays supported in the model. None proves actual travel.

**Compare gearing before buying a third head.** Holding the hypothetical motor
point at 3000 rpm/1500 rev/s², lead 3 with 1.5:1 reduction and lead 2 with 1:1 both give
100 mm/s and 3000 mm/s² axial motion. Every ideal move then has exactly the same
duration: 64/B2/K32 returns to 25.38 s. At fixed 1000 output rev/s², increasing only
RPM gives 25.93 s instead; speed scaling alone is not trajectory equivalence.
The 1:1 case still needs staggered-motor shaft routing, spindles and docking.

Using the same assumed 70% transmission efficiency, 20-g moving mass, μ=.3,
.05-N·mm running drag, d2.3 and zero guide drag, the rated-point available torque
changes 1.030→.686 N·mm; accelerating demand excluding rotating inertia changes
.295→.239 N·mm. Effective output-inertia ceiling is 1.17e−7→4.74e−8 kg·m².
After ideal ratio-squared reflection, the motor-only ceilings with **zero output
inertia** are 5.19e−8→4.74e−8; do not mistake output-reference numbers for a measured
motor-inertia penalty. Real shafts/gears/socket inertia consume this allowance.
These are necessary bounds at a hypothetical point, not a speed-torque curve,
achievable ramp or motor selection. Changed lead also changes the friction model;
it does not establish holding or moving-loss arrest in the observed pair.

Supplier [711](https://www.adafruit.com/product/711) and
[3297](https://www.adafruit.com/product/3297) tiers rechecked 2026-10-13. Preserve
the unquoted reserve and count all installed motor/feedback/dock duties:

| Grid / heads | Outputs | Motor kg | Quoted subset + reserve USD | Remaining/output at $500 / $1000 / $1500 |
|---|---:|---:|---:|---:|
|64 / 2|128|2.24|984.64|−3.79 / .12 / 4.03|
|64 / 3|192|3.36|1272.44|−4.02 / −1.42 / 1.19|
|80 / 2|160|2.80|1166.40|−4.17 / −1.04 / 2.09|
|80 / 3|240|4.20|1488.60|−4.12 / −2.04 / .05|

For 192 outputs, buying 100 dual-driver boards at $4.76 costs less than 96 at $5.36;
four spare boards are counted. At 240 outputs buy 120 boards. Taxes/shipping,
feedback/transmission/docking and reserve corrections remain unresolved; these
are not finished BOMs or selling prices. A third head adds 64/80 motor/transmission/
feedback/dock paths, one carriage, wiring and proof duties without reducing 4096/
6400 resident pairs. At the illustrative 1 min/channel it adds 1.07/1.33 maker hours
before carriage build, calibration or repair. At K32 it also raises simultaneous
outputs 64→96; no electrical or assembly saving follows from the faster schedule.

**Decision:** retain shallow/deep software choice and the two-head, coarser-grid
comparison. Do not add a third head merely to preserve 30 s under the uncalibrated
2-mm estimate. Keep 1:1 versus 1.5:1 as explicit measurement hypotheses; first
establish loaded lead, torque, inertia/ramp and stop/withdrawal on an intact
supported pair. Minimum engagement/end margins must respect E-256's extension
failure; changing drive ratio does not repair that failure or grant 50-mm stroke.
No new thread geometry, brake, print, purchase or architecture selection.

Verification: 288 full-concurrency anchors against the existing E-255 scheduler,
both leads/pitches and 2/3 banks; exact dense-wave, signed/no-op, cache-isolation,
frictionless work, reflected translation inertia, trajectory-scaling and quantity
tier controls. Original 729 admission checks and E-256/E-259 regressions pass.
Self-review; no independent or physical validation.
