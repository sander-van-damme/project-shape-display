---
status: complete
builds-on: [E-256, E-258]
---

# Sourced rotary channels and feedback budget

**Cheap rotary power remains plausible, but no complete channel or BOM is
qualified.** Two64-output heads leave about$4/output under a$1500 research
allocation after the sampled motors/drivers and an unquoted reserve. About$1000
leaves only$.12/output. The later2-mm-lead screen removes the prior30-s margin
at2000rpm; compare drive ratio before adding heads. No hardware selection,
physical test, print or purchase follows from these calculations.

Reproduce `python3 tools/curated-experiment-checks/E-259/channel_screen.py`,
`concurrency.py` and `lead_sensitivity.py` (same directory). JSON stdout is
reproducible output, not retained evidence. Supplier inputs were checked2026-10-12;
711/3297 were rechecked2026-10-13. These are catalog facts, deterministic
calculations and conditional E-258 schedules, not motor tests or production quotes.

## Catalog inputs and missing implementation

USD before tax/shipping; listed stock is not a quantity reservation.

| Part | Price at applicable quantity | Relevant rating / limitation |
|---|---:|---|
|[Adafruit711](https://www.adafruit.com/product/711)|$1.56 at100+|6V,10gf·cm rated load,4500±1500 loaded rpm,≤250mA loaded/≤500mA stall;27.5×20×15mm,17.5g; no encoder/gearbox|
|[Adafruit3297 dual DRV8833](https://www.adafruit.com/product/3297)|$5.36 at10–99 boards; $4.76 at100+|Two reversible channels; default1A limit,2.7–10.8V; quantity tier applies to boards, not outputs|
|[Pololu5180](https://www.pololu.com/product/5180)|$25.27 at100+|9.96:1 encoder gearmotor,12 counts/motor rev;3300 typical unloaded rpm at6V; cables extra|
|[Pololu3081 encoder pair](https://www.pololu.com/product/3081)|$8.42/pair at25+|Compatible extended rear shaft required; **not compatible with711** without a separately designed attachment|

[5180 specifications](https://www.pololu.com/product/5180/specs) list2300rpm at
.042kgf·cm/.51A maximum efficiency; no-load speed±20% is not a loaded curve.
3297's1A default limit is below5180's1.5A stall extrapolation. Basic711+3297
voltage/current ratings are compatible, not proof of thermals, regeneration,
layout or complete feedback. Leads are supplied; connectors/distribution remain.
3081 is only a feedback-price comparator, never a plug-in711 assembly.

Keep E-255's **unquoted** reserve:$250 common +$.02/resident site +$55/head,
including just$40 supply/protection and$20 controller allowance. At two heads:

| Duty / accounting |64×64,6.35mm|80×80,5.08mm|
|---|---:|---:|
|Resident pairs/seats/sockets/anti-rotation duties, each|4096|6400|
|Independent drive/feedback/dock duties, each|128|160|
|Dual driver boards|64|80|
|Reserve|$441.92|$488.00|
|711+3297 per output|$4.24|$4.24|
|Subset+reserve|$984.64|$1166.40|
|Remaining/output at$500/$1000/$1500|−$3.79/$.12/$4.026|−$4.17/−$1.04/$2.085|
|5180 motors alone|$3234.56|$4043.20|
|5180+3297+reserve|$4019.52|$4960.00|
|Basic subset plus incompatible3081 price comparator|$1523.52|$1840.00|

The$4 original complete-channel allowance cannot buy even the sampled711/3297
subset. Missing feedback, transmission, spindle/journals, retained/self-aligning
socket, docking, harness, actual-height proof and reserve corrections are not
zero. Custom assembled electronics might help; no quote or market-wide price
floor is established. Avoid hand-wiring64/80 breakouts without counting labor.
A one-minute/channel assembly assumption already adds2.13/2.67h, before resident
insertion, fixtures, calibration and rework. Molding or machined shared carriers
may improve alignment, but do not remove these duties or establish process yield.

Motor-only rated-load/stall arithmetic is32/64A for128 outputs,40/80A for160:
192/240W at rated load, **not** predicted screw consumption or a PSU rating.
PWM, startups, braking, regeneration and electronics need measured budgeting.
Motor mass is2.24/2.80kg;5m/s² carriage acceleration requires5.6/7N per half-board
for motors alone. The15-mm body needs at least three staggered lanes at either
pitch even without clearance. Off-board drives exchange carriage mass for routed
shafts/cables; neither arrangement has finite routing or service qualification.

## Torque, feedback and stopping

711's rated torque converts to.980665N·mm. A **hypothetical**1.5:1 reduction at
70% efficiency maps the lower loaded-speed endpoint to2000rpm/1.0297N·mm.
This is one operating-point transformation, not a motor curve or achievable ramp.
E-256's20-g/μ.3/drag.05-N·mm/lead3 scenario needs.2954N·mm accelerating at
1000rev/s² before rotating inertia, leaving effective screw-side J≤1.17e−7kg·m²;
J=1e−6 fails that bound. The earlier1e−8 is not a catalog specification.

Open-loop timing based on4500rpm gives6.67–13.33mm for a nominal10-mm move
at the listed3000–6000 range, even ignoring startup. PWM duty is not position.
5180's exact ratio1295/130 and12 counts/rev give.02510mm/count at lead3 and
3984.6edges/s/output at2000rpm:510031/637538edges/s across128/160 channels.
This is capture workload, not accuracy: gearbox backlash, coupling and missed
sockets lie downstream. A disengaged socket can produce all expected motor
counts and no pin motion. Preserve actual-height proof and local retry; the20-ms
proof allowance is unimplemented. At100mm/s,1/5/20ms latency alone adds.1/.5/2mm
before braking distance.

[TI DRV8833 Rev E §§7.3.2,7.3.5–7.4](https://www.ti.com/lit/ds/symlink/drv8833.pdf)
distinguishes powered short-circuit brake from coast; sleep/undervoltage turns
bridges off. Brake commands are not power-loss support. The resident screw
carries the pin, consistent with Sander's positive manual static-hold evidence.
Stop/prove/withdraw is the intended sequence; unexpected moving loss needs its
own caught-load test. Missing evidence does not justify6400 extra brakes.

## Scene timing and powered-output admission

`channel_screen.py` retains all E-258 physical/visual policies, both pitches,
neutral20/30 with40/50mm range,1500/2000rpm and200/1000rev/s². These remain three
convenience maps, not representative play. At64/N20/lead3/B2, mixed maxima are
22.08s at2000/1000,25.28s at1500/1000 and26.48s at2000/200.1500/200 gives28.57s
shallow but32.97s atN30/depth30.80/N20 at2000/200 needs31.50s. InitialN20 prep
at64 is18.28s for2000/1000 or23.51s for1500/200; dense±40 is24.88/32.31s.
Startup is separately paid; homing/manual/visual workflow remains unqualified.
All schedules retain seeks,80-ms docking/release,20-ms row proof, return, one
full-row retry and4s common allowance; none proves player-ready operation.

`concurrency.py` keeps every installed motor but admits at mostK powered
outputs/head. Each changed cell gets one signed rest-to-rest move. Longest-first
(LPT) starts waiting moves in the earliest free slot; a slot is electrical
permission, not a mechanical motor selector. Ideal passive screw hold covers
idle/finished cells. Row lower bound is max(total duration/K,ceil(j/K)*t_j) over
sorted durations. LPT need not be optimal: the source preserves a7-unit witness
with6-unit optimum. Bounds propagate through inherited4+slowest-bank+globally
longest-row-retry accounting; this conservative retry is not a tight adversarial
wall-clock optimum. Alternative routes, global token lending and preemption are
not bounded. A5-ms token-release scenario charges possible stop/current settling.

Owner-selected physical river/ravine at fixed ground30 and shallow20/deep30
produces6 initial commands and30 directed transitions; duplicates are not new
map evidence. Shallow deltas also apply to ground20/40-mm hardware. At lead3,
2000rpm/1000rev/s²:

| Grid / K | Shallow max s | All preset max s | Ravine20→30 s | ColdN30 s | Dense50 s | Motor loaded/stall A |
|---|---:|---:|---:|---:|---:|---:|
|64 /16|28.18|34.18|19.38|54.58|80.98|8/16|
|64 /24|23.95|28.62|16.98|43.58|63.38|12/24|
|64 /32|22.12|25.38|14.98|32.58|45.78|16/32|
|64 /64|22.08|25.38|14.98|21.58|28.18|32/64|
|80 /32|28.07|33.50|19.40|52.67|77.27|16/32|
|80 /48|26.07|30.13|17.13|39.00|55.40|24/48|
|80 /80|26.03|30.13|17.13|25.33|33.53|40/80|

64/K32 preserves scene25.38s with half as many powered outputs; dense50 needs
two waves/row, K24 three. At64, K22 first permits a lower bracket≤30; K23 first
has an LPT witness≤30 (28.92s). K22 is not disproved; K24 brackets28.18–28.62s.
At1500rpm/1000rev/s², K29 gives29.93s but5-ms release raises30.12; K32 gives
29.67/29.84s. At2000/200, K32 gives29.85/30.02s.1500/200 full gives32.97s deep;
K32 shallow28.70s. These are rate scenarios, not manufacturing priors.

Two K-slot banks imply.5K loaded/K stalled motor amperes using711's stated
conditions, not measured draw or supply sizing. Admission must wait for current
to stop; stationary active braking still consumes budget. An indefinite jam
is not covered by one retry. No powered-output reduction deletes installed
channels, motor mass or purchased cost; K24–32 is a control hypothesis only.

**Physical discriminator:** measure an intact retained pair's loaded signed lead,
torque, inertia/ramp, current, stop/withdrawal and missed engagement before
selecting a bank. Cheap motor torque justifies investigating this window, not
claiming a buildable head. Quote custom feedback/driver assembly only if the
window survives. No micro-thread or resident latch campaign is reopened.

Verification: quantity tiers, torque-unit/inertia limits, budget identities,
E-258 anchors,729 exhaustive small-row comparisons, nonoptimal-LPT witness,
all36 full-slot anchors at both pitches, signed/no-op and exact dense waves.
Self-review; no independent validation or physical qualification.

## Lead, gearing and head-count sensitivity — 2026-10-13

Reproduce: `python3 tools/curated-experiment-checks/E-259/lead_sensitivity.py`
(`--check` for verification). **Conditional calculations:** E-256's rough owner
estimate motivates 2 versus historical 3 mm/turn, not calibrated bounds or CAD
identification. The reported 1-mm play is not a lead correction. Retain the same
36 physical river/ravine preset commands, ground30, shallow20/deep30 and required
50-mm range. Ground20/40-mm travel remains the shallow control. Preserve all
prior overheads and unqualified proof/homing limitations. K is powered outputs
per head; default acceleration is1000 rev/s². No physical travel is established.

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

At64/B2/K32, lead3→2 raises the maximum **27%, not50%**. K64 cannot recover the
critical row duration. The30-s boundary is approximately2262rpm at1000rev/s²,
with no margin. At200rev/s², unlimited speed still needs32.04s with LPT/K32 or
31.69s at full concurrency. This is a schedule limit, not a hardware failure or
reason to reject an enjoyable32-s update. Cold ground30/dense50 at64/B2/K32/
lead2/2000rpm take42.48/62.28s, versus32.58/45.78s atlead3; K64 gives26.53/36.43s.
Same-ravine20→30 takes16.63s atK32 with unchanged ground retained ideally.

**Compare gearing before adding a head.** At the same hypothetical motor point
3000rpm/1500rev/s², lead3/1.5:1 reduction and lead2/1:1 both give100mm/s and
3000mm/s² axial motion: every move has identical duration, restoring25.38s at
64/B2/K32. Scaling RPM alone while retaining1000 output rev/s² gives25.93s.
The1:1 route still owes staggered-motor shaft routing, spindles and docking.
With assumed70% efficiency,20-g mass, μ=.3, .05-N·mm drag, d2.3 and no guide drag:

| Lead / ratio | Available N·mm | Accelerating demand excluding rotating J | Effective output J ceiling kg·m² | Motor J ceiling with zero output inertia |
|---|---:|---:|---:|---:|
|3 / 1.5|1.030|.295|1.17e−7|5.19e−8|
|2 / 1|.686|.239|4.74e−8|4.74e−8|

Motor ceilings use ideal ratio-squared reflection; real shaft/socket inertia
consumes allowance. These are necessary hypothetical-point bounds, not a measured
speed-torque curve, achievable ramp or motor selection. A changed lead also
changes friction; neither lead scenario establishes hold or moving-loss arrest.

[711](https://www.adafruit.com/product/711) and
[3297](https://www.adafruit.com/product/3297) tiers rechecked2026-10-13:

| Grid / heads | Outputs | Motor kg | Subset + unquoted reserve USD | Remaining/output at $500 / $1000 / $1500 |
|---|---:|---:|---:|---:|
|64 / 2|128|2.24|984.64|−3.79 / .12 / 4.03|
|64 / 3|192|3.36|1272.44|−4.02 / −1.42 / 1.19|
|80 / 2|160|2.80|1166.40|−4.17 / −1.04 / 2.09|
|80 / 3|240|4.20|1488.60|−4.12 / −2.04 / .05|

192 outputs:100 driver boards at$4.76 beat96 at$5.36; four spares counted.
240 outputs need120 boards. All prior missing-BOM/tax/shipping limitations remain.
The third head adds64/80 drive/transmission/feedback/dock paths, carriage and
wiring;4096/6400 resident pairs remain. At illustrative1min/channel it adds
1.07/1.33 maker hours before carriage build/calibration; K32 increases powered
outputs64→96. No electrical or assembly saving is booked.

**Decision:** retain selectable depth and the two-head/coarser comparison. Do
not add a third head merely to preserve30s under the uncalibrated2-mm estimate.
Measure loaded lead, torque, ramp/inertia and stop/withdrawal on an intact
supported pair with1:1/1.5:1 as hypotheses. Respect E-256's engagement/end-extension
failure; gearing cannot repair it or grant50-mm stroke. No new geometry, brake,
print, purchase or architecture selection.

Verification:288 inherited full-slot anchors across both leads/pitches and2/3
banks; exact dense-wave, signed/no-op, cache, frictionless-work, reflected-inertia,
trajectory-scaling and quantity-tier controls. Original729 admission checks and
E-256/E-259 regressions pass. Self-review, not independent or physical validation.
