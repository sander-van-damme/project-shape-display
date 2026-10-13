---
status: complete
builds-on: [E-266]
---

# Reusing fewer rotary channels on one XY head

Reproduce `python3 tools/curated-experiment-checks/E-267/screen.py` (`--check`
for controls). **Retain16 outputs/coarse pitch as a lower-cost demonstrator
comparator**, not a fast full-map product or qualified machine.

**Changed architecture:** one XY carriage reuses8/16/32 independent rotary tips.
Selected tips dock, drive signed moves, stop/prove/release; resident screw/thread/
thrust support continues throughout. Overlapping footprints must isolate unselected
or completed sockets. No resident clutches or tool takeover of axial load are added.
Finite carriage routing, docking, feedback, real support and moving-loss behavior
remain unbuilt. The full-pitch motor packaging still needs staggering:15-mm minimum
motor width exceeds6.35-mm pitch;16 tips span95.25mm. The board retains4096/6400
pairs/thrust/socket duties and8192/12800 guide apertures. Only shared channel count
falls, by112 against coarse B2. Two positioning axes plus approach replace one
positioning axis plus approach. More reused docking cycles increase wear exposure.

Greedy intervals minimize station count per row; each changed cell is commanded
once. Intervals slide toward prior X where possible. Compare row and column-major
serpentine routes through those jobs, including return; this is not a global
weighted-route optimum. Tips never overhang. Reuse E-266/E-255 signed spin, simultaneous
XY travel at200mm/s and5000mm/s²,50-ms minimum seek,100-ms dock/proof,4-s allowance and one longest immediate
station retry. Retry uses observed remaining delta; no indefinite jam or invisible
engagement proof is implied. Undocked tool clearance is granted, not finite CAD.

Local scenarios are4×4-D&D-square/101.6-mm windows into the existing three physical
relief maps, stepped by2 squares:49 windows/map,147/depth/pitch,133 nonempty.
These overlapping windows sample spatial coverage, **not typical play frequency,
room boundaries or fog concealment**. S40/N20/depth20 and S50/N30/depth30 retain
physical river and ravine. Neutral preparation is paid. Existing wall connectivity,
miniature-base and under-bridge limitations remain. Scene tests reuse all prior
E-266 transitions, including shallow/deep switching; no between-map reset is inserted.

At both pitches the board spans406.4mm:64×64 at6.35mm versus the80×80/5.08mm reference.
Seconds **S40 / S50**, conditional850rpm/lead3, all installed outputs admitted:

|Grid|Outputs|Partial USD|Local max|Scene max|Cold neutral|Dense stress|
|---|---:|---:|---|---|---|---|
|64|8|461.32|29.71 / 37.48|267.26 / 308.44|343.83 / 464.53|585.24 / 705.95|
|64|16|497.68|18.61 / 22.61|173.33 / 200.62|175.50 / 235.97|296.44 / 356.91|
|64|32|564.00|18.61 / 22.61|118.17 / 136.75|90.58 / 120.93|151.28 / 181.63|
|64|64|671.08|18.61 / 22.61|62.71 / 76.12|48.59 / 63.88|79.18 / 94.47|
|80|8|507.40|47.62 / 61.97|388.91 / 452.91|526.86 / 715.33|903.80 / 1092.27|
|80|16|543.76|33.91 / 43.32|251.04 / 291.04|267.55 / 361.90|456.26 / 550.61|
|80|32|610.08|21.10 / 26.04|159.35 / 188.53|164.73 / 221.44|278.14 / 334.85|
|80|80|788.20|21.10 / 26.04|75.91 / 92.62|58.50 / 77.56|96.62 / 115.67|

All133 coarse16 windows/depth finish within30s nominally; coarse8 deep gives122/133.
These are scenario counts, not gameplay/reliability passes. Coarse16 cold first-map
is291.57/360.17s. Its deep200.62-s scene maximum compares with43.29s for B2/K32.
Even the independent work-only relaxation, sum(each screw's rest-to-rest time)/16,
needs65.92s on the worst S50 work case before all overhead. Better routing cannot
restore universal30-s scenes within this topology/rate. Actual200.62s is a feasible
model schedule, not an optimum. Coarse32 buys no better worst local wait.

Coarse16/S50 local sensitivity: lead2/850rpm28.61s; lead3/600 or400rpm27.54/35.99s;
200rev/s² plus100ms extra/station at850rpm25.28s. Bounds, not safe speeds or process
priors. Known pre-positioning gives21.05s worst visible versus22.61s paid cycle.
Unknown reveals receive no credit; wrong pre-position then return to origin adds
at most2.041/2.047s on64/80. No terrain moves early and preparation is not free.

Partial dollars use the same dated supplier tiers, rechecked2026-10-13 at the
[motor](https://www.adafruit.com/product/711) and
[driver](https://www.adafruit.com/product/3297) pages, plus E-266 reserve and **$35 unquoted extra XY-axis
allocation** for short heads. No power/sensing reserve reduction. Eight channels
buy8×$1.95 motors/4×$5.95 drivers;16 buy16×$1.76/8×$5.95;32 buy32×$1.76/16×$5.36.
Coarse16 leaves only$2.32 total under$500, versus$502.32 under$1000 ($31.395/output)
and$1002.32 under$1500. B2 leaves$15.36 under$1000. Missing feedback, reduction,
docking, wiring and reserve corrections must fit collectively; no complete BOM.
16 motors weigh.28kg; rated-load/stall arithmetic4/8A is not measured machine power.
At1min/channel illustrative assembly is.27h versus2.13h for B2, excluding carriage,
calibration and all resident assembly. Few machined/outsourced shared couplers may
now be affordable; no quote/process is selected. E-260's batch/service limits remain.

**Stop routing/channel sweeps.** A premium demonstrator might buy better accessible
channels while accepting minutes for setup/large changes; no owner preference or
purchase is inferred. Next discriminator: a complete observable, supported rotary
channel within the residual, then packaging/service. Shared-reader coverage and
failed-engagement detection can be screened independently of optional printing;
motor turns alone do not prove terrain height. E-263 remains unchanged, with no
new print, fine-feature/coupler campaign or owner question.

Verification:1538 exhaustive interval covers,144 full-row anchors, exact dense
station/spin counts including80/32, signed cell replay/no duplicates, no-op/budget
controls and a narrow-window anti-zigzag control. These verify code, not hardware.
