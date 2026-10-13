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


## Concurrent-output admission — 2026-10-13 extension

Reproduce: `python3 tools/curated-experiment-checks/E-259/concurrency.py`.
**Deterministic scheduling simulation, not electrical or physical qualification.**
This adds a software control option to the independent B2 reference: keep all
64/80 motors on each head, but allow at most K to operate simultaneously. Each
changed cell gets one complete signed rest-to-rest move. A motor remains assigned
to its own screw; a free admission slot lets the next waiting motor start. No
mechanical drive multiplexor, extra clutch or replacement of feedback is implied.
Idle/finished outputs rely on the same resident screw holding assumption as E-255.

The longest-duration waiting move starts in the earliest available slot (LPT).
Each row has an explicit feasible slot witness. The lower bound is the larger of
sum of move durations/K and `ceil(j/K)*t_j` for every duration sorted descending.
This bounds row service without assuming LPT is optimal. The source includes an
exact exhaustive small-case comparison and a case where LPT takes 7 units while
an optimal partition takes 6. Bounds propagate through **the inherited accounting**:
4 s + slowest fixed-bank route + globally longest row retry. That retry charge is
conservative; the reported lower bracket is not a universal lower bound on actual
wall-clock latency across different routes, globally lent slots or retry policies.

Preserve 80-ms docking/release, 20-ms row proof, actual pitch-dependent seeks,
empty return, a full row retry and the common 4 s. One continuous move includes
its own acceleration/deceleration; waiting adds no extra partial-stop cycles.
The base assumes current can cease at the predicted stop. A separate 5-ms
per-output token-release allowance probes current settling/stop qualification;
it is a labelled bound, not measured overhead. No-op rows remain skipped.

Workload: unchanged E-258 physical river and ravine, fixed ground30, shallow20/deep30,
both pitches. Six scene/preset states give six ground-to-map commands and all30
directed state transitions; duplicates and no-ops are retained as checks, not
additional real map evidence. This remains three annotated convenience maps,
not representative session statistics. The ground20/40-mm-travel control has
identical shallow-mode deltas; fixed ground30 pays separate initial preparation
and needs the previously unqualified50-mm hardware range. Dense50-mm stress and
same-ravine preset change are separate from the scene maxima.

**New result: at64×64, K32 preserves the25.38-s scene maximum while halving
simultaneously powered outputs from128 to64. K24 takes28.62 s.** This is a useful
software-controlled power/latency hypothesis, not an installed-motor reduction.
At2000 output rpm/1000 rev/s², times in seconds are:

| Grid / K per head | Shallow scene max | All preset/scene max | Same ravine20→30 | Cold ground30 prep | Dense50 stress | Loaded / stall motor A |
|---|---:|---:|---:|---:|---:|---:|
|64 /16|28.18|34.18|19.38|54.58|80.98|8 /16|
|64 /24|23.95|28.62|16.98|43.58|63.38|12 /24|
|64 /32|22.12|25.38|14.98|32.58|45.78|16 /32|
|64 /64 full|22.08|25.38|14.98|21.58|28.18|32 /64|
|80 /32|28.07|33.50|19.40|52.67|77.27|16 /32|
|80 /48|26.07|30.13|17.13|39.00|55.40|24 /48|
|80 /80 full|26.03|30.13|17.13|25.33|33.53|40 /80|

The scene bottleneck has enough idle capacity/unequal move lengths to absorb
staggering atK32; a cold flat or dense uniform move does not. At64/K32 the
50-mm dense case takes exactly two waves per row; atK24 it needs three.
Cold preparation is separately paid, never erased by a raised software zero.
No new homing or manual/visual workflow qualification is added to these times.

The64/base sweep first has a lower bracket≤30 s atK22 and an LPT witness≤30 s
atK23 (28.92 s); it does **not** prove K22 impossible. K24's bracket is
28.18–28.62 s. At1500 rpm/1000 rev/s², K29 gives29.93 s but adding5 ms per
finished move raises that to30.12; K32 gives29.67/29.84 s without/with that delay.
At2000 rpm/200 rev/s², K32 gives29.85/30.02 s: the boundary is fragile.
At1500/200, even full concurrency gives32.97 s for deep relief, whileK32 shallow
is28.70 s. The80-grid base deep result is30.13 s even at full concurrency.
These are whole-machine rate scenarios, not independently sampled motor errors
or manufacturing yield predictions.

**Decision:** keep K24–32 as a conditional64-grid operating option and useK32 as
the comparison for a future measured current trace. Do not design a128-motor
simultaneous-start supply merely from the installed count. Equally, do not claim
an8-A loaded-current case keeps deep relief below30 s: K16 takes34.18 s under
these rates. Retain slower dense/setup operation explicitly. No motor bank,
supply, driver PCB, print job or architecture is selected by this screen.

The supplier [711 listing](https://www.adafruit.com/product/711), rechecked2026-10-13,
still gives6 V,250-mA loaded and500-mA stall maxima under its specified conditions.
For two reserved K-slot banks these yield **0.5K A loaded / K A stalled** motor-only
arithmetic. They are not measured screw-drive consumption, a validated startup
bound, a rail/protection design or permission to buy a supply. PWM, regeneration,
driver/controller power, current-limit tolerance and fault isolation still matter.
Admission must prevent a new start while the preceding output remains powered;
otherwise counting moving shafts alone understates simultaneous electrical demand.
A stalled output must time out or release its slot safely; one retry does not
cover indefinite jams. Stationary active braking would also consume part of the
budget. Stop/hold/current confirmation remains unimplemented and timed only by
the stated bounds.

All4096/6400 resident pairs,128/160 installed drive/feedback/dock duties,2.24/2.80-kg
motor mass and the quoted-subset-plus-reserve$984.64/$1166.40 remain unchanged.
No reduction in bought cost, assembly, print burden or supply size is booked.
The$500 reference remains unresolved; the$1000/$1500 cases retain their missing
feedback/transmission/docking and reserve qualifications. Slower schedules can
still be useful D&D tradeoffs; crossing30 s is reported, not declared unsafe.

Verification:729 exhaustive small scheduling comparisons, explicit no-overlap and
one-visit witnesses, a nonoptimal-LPT counterexample, both pitches/all36 full-slot
anchors against E-255, signed symmetry, no-op and analytically exact equal-move
wave counts. Self-review only. This changes the power/latency trade study; it does
not substitute for the existing pair's loaded speed, stop, hold and current tests.
