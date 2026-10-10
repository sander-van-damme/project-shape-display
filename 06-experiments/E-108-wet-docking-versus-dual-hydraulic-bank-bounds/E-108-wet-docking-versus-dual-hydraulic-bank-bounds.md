---
status: complete
builds-on: [E-107, E-060, ADR-017]
---

# Two zoned banks retain a timing window after a pump-starvation counterexample

**Retain two independently supplied dry-head banks, limited to 40 open channels
per pressure phase, for finite three-state valve/return investigation. Park the
single wet bank under the inherited controller bounds.** This is an exploration
allocation, not architecture, cost, reliability or hardware acceptance. A new
79-easy/1-hard load witness defeats unrestricted shared-pump opening even with
two banks. Chunking avoids that modeled failure and gives a conservative
**23.387-s full-map bound** within the specified load/fluid/error model. No new
passage optimization is performed; E-107's .6-mm × 40-mm round passage is fixed.

Input main `301aa30`. Replay:
`python3 tools/curated-experiment-checks/E-108/bank_docking.py` (`--all` includes
216 pressure-volume scenarios). Evidence: analytical bounds, deterministic event
simulation, logical sequencing and self-review. No geometry/contact/CFD,
process calibration, sourced prices, measurement or independent review.

## Changed arrangement and complete schedule

Two 80-head banks each own a disjoint 40-row zone, starting at opposite outside
edges and reversing scans on successive maps. Each has an independent regulated
8-L/min supply/return capacity; a single 8-L/min source is **not** credited twice.
The banks may run different pressure directions concurrently. Their moving
frames/hoses must clear at the zone boundary. No row is shared and unchanged
chamber valves remain shut. Total displacement volume stays **.804 L**, not twice
that; at .5-MPa circuit differential two simultaneous 8-L/min sources imply
**133.3 W ideal hydraulic power**, before losses. Reservoir, containment,
electronics and actual bidirectional pressure capability remain unresolved.

Use E-107's tight explicit bounds: ±.025-mm restriction diameter, ±2% length,
.008….012-Pa·s viscosity, entry K=0…2, ±1-kPa common pressure error. Retain
2-mm piston bore, .3-N bias, .05-N drag, payload anywhere in 0….1 N, 40-mm travel,
.5-mm **diagnostic** positioning budget, .05-mm read error and 2-ms response.
These are assumptions, not product accuracy or X1C capabilities. Restrictions
remain cell-resident, closed/restricted/full-open; E-105 does not implement the
extra bypass seat or complete return.

Schedule: .5-s map preparation; E-104 rest-to-rest travel; 40-ms acquisition/
withdrawal and 20-ms read/settle per visited row; 10-ms pressure/open/close and
2-ms stopped coarse-to-fine transition per nonempty chunk. Coarse, stop, fine,
independent chamber closure and proof precede withdrawal. Chunk at most 40
requested columns for each direction; completed and non-target cells remain
closed. Proof/read overheads are allocations, not demonstrated sensing.

Append the largest complete changed-row recovery **after both banks finish**.
Recovery permits all changed cells to traverse the full stroke in both directions,
up to four chunks, then proof/withdrawal. This conservatively covers one detected,
arrested error; persistent valve faults or further failed rows stop the update.
No perfect readback, false-accept rate or persistent-fault recovery is established.
Empty maps take zero; local maps visit only affected rows. Per-map reset is not
hidden by prebuffering or one-time setup.

### The new adversary and its escape

The inherited eight evenly repeated load levels conceal pump starvation.
At raising thresholds `b = (.3 + payload + .05)/π`, set 79 cells to zero payload
and one to .1 N. At the pressure needed to move the hard cell at 400 mm/s,
the easier channels consume too much flow. Even at the hard cell's stall pressure,
the 79 easy channels exceed 8 L/min. The event law rejects this as
`pump-induced stall/reverse-risk`; doubling banks alone cannot repair it.

For at most 40 open channels, define
`u_floor = b_min + loss(Q/(40 A))`. At this pressure each channel draws at most
Q/40, so pump saturation cannot force a lower pressure. Combining that floor
with the controller pressure and return limit leaves **≥400 mm/s** coarse speed
for any payload assignment in the stated range. Worst fast-corner terminal band
is 1.629171 mm; slow fine-corner speed is **49.844359 mm/s**. Generously traverse
all 40 mm coarsely **and** the whole terminal band finely: each chunk is bounded
by `40/400 + 1.629171/49.844359 + .012 = .144685 s`.

For 80 changed cells, `ceil(n_up/40)+ceil(n_down/40) ≤ 3`; the separate recovery
uses four. Thus preparation + 39 adjacent moves + 40×(.06+3×.144685) +
(.06+4×.144685) = **23.387191 s**. This bounds arbitrary heights/directions and
payload placement **only within this reduced model**, rather than extrapolating
a favorable workload. It leaves <**161.288 ms extra per visited/recovery row**
before 30 s. The inherited full-open port law and static thresholds are necessary
conditions; transients, stem displacement, return losses and real proof may
consume the margin. Additional .22-N common drag still prevents unloaded
lowering, irrespective of bank count.

Executable event examples with the original eight-level load pattern give
**20.957 s for 79/1 with chunking**, versus 16.104 s without it. The latter is a
conditional comparison only. Enumeration retains 1,296 direction-cut/load-offset
cases for unrestricted control; the analytical chunk bound is what covers changed
load correlations. Local 10×10 tests cover 71 row placements, 16 distinct
load/direction offsets and two zone-end starts (2,272 cases), taking **2.593…5.355 s**. These test command
isolation and schedule only, not adjacent displacement. Common speed factors
.8/.5 and added row overheads are diagnostic schedule sensitivities, not an
independent physical friction model or measured tails.

## Wet acquisition: repeated volume is not free metering

Proposed wet circuit: source → reusable head metering/isolation → sealed docking
cavity → selectively opened normally closed chamber check → piston. Unlike the
dry route, supply plumbing and restrictions travel with 80 heads. Reusing a
fixed restriction does **not** change E-107's pressure/load law. Independently
regulated flow remains an unimplemented, unpriced comparator.

Required sequence: seal face with chamber closed; fill/bleed/condition cavity;
isolate head source; selectively open target chamber check; equalize; enable
metered bidirectional flow; close chamber; proof while still sealed; close head;
dump trapped cavity to contained return; undock/reset. Checks on unselected
cells must never open even if all 80 faces dock. A coupling that automatically
opens every check when docked fails this regional-isolation requirement. The
logical state audit rejects early check opening and early undocking; it does
not implement individual check actuation, contact or proof. If the chamber
check sticks open, keep the head sealed and stop: undocking is not recovery.

For an isolated cavity with volume V at initial gauge pressure pi, gas fraction
f **at pi**, liquid bulk modulus K, wall compliance V/Kw and constant-load final
pressure pf, expelled volume is

`ΔV = V(1−f)[exp((pi−pf)/K)−1] + Vf[((pi+patm)/(pf+patm))^(1/n)−1] + V(pi−pf)/Kw`.

`Δx=ΔV/A` is a quasistatic motion witness; a piston at a stop instead experiences
pressure change. It is not a dynamic overshoot bound. [MathWorks' hydraulic
chamber model](https://www.mathworks.com/help/simscape/ref/constantvolumehydraulicchamber.html)
supports liquid/gas compressibility modeling; it does not qualify these chosen
parameters or printed walls. No gas dissolution/cavitation prediction is made.

Explicit scenario grid: V=1/10/100 mm³, f=0/.01/.1, Kw=10/100/1000 MPa,
pi=.01/.5 MPa, pf=.08/.14 MPa, n=1/1.4, K=1500 MPa and patm=.101325 MPa.
These are competing bounds, not process/fluid priors or yield. The 216 cases
span **−2.131…+8.718 mm**. At V=10, f=.01, Kw=100 and isothermal gas,
.5→.08 MPa gives **+.08798 mm**; .01→.14 gives **−.02156 mm**. Common pressure,
air or wall bias affects an entire bank; no independent-cell averaging. Source
replenishment while opening would invalidate this isolated-cavity bound.

Closure/disconnection swept volume must also go somewhere: just **.314159 mm³**
uncompensated volume moves a 2-mm piston .1 mm. Post-closure readback/calibration
or a trapped-volume compensation design needs its own accuracy/time allowance.
A full 80-face bank with 2-mm effective sealing diameters at .5 MPa sees
**125.664 N** separating force, before preload, seals, springs and geometry.
For V=1…100 mm³, one complete liquid flush per head takes ≥.6…60 ms per row at
8 L/min, before purging effectiveness, valving and proof. Repeating .01 mm³ loss
or air inclusion at each of 6,400 dockings gives .064 mL/map, 64 mL/1,000 maps;
this is an accumulation scenario, not measured leakage or a retained-air model.
[Parker's non-spill coupling description](https://discover.parker.com/non-spill-couplings)
confirms that air inclusion, fluid loss and residual-pressure connection require
dedicated hardware. Its commercial products are not pitch, price or PLA evidence.
Sources accessed 2026-10-10.

With unchanged fixed restrictions the single wet bank inherits the >31-s
examples **before extra docking work**. Even ideal independent throttling leaves
only **14.717 ms/row** additional to inherited acquisition/read allocations:
28.808 s becomes **30.428 s** with 20-ms extra per visit/recovery. This does not
prove wet docking impossible; changed shared metering, pressure sensing,
calibration or larger overhead overlap could reopen it. No such affordable
mechanism is established here. Do not elaborate wet solids now.

## Coupled economics and next gate

| Arrangement | Repeated interfaces and actuation | Joint economic constraint |
|---|---|---|
| Two dry banks | 160 complete head drives/returns/controllers; 6,400 piston seals, ≥6,400 stem glands, 6,400 chamber seats plus 6,400 bypass seats/passages; two motions/supply capacities | With $250 shared and $.01 bought per cell, ≤$1.1625 per complete head |
| One wet bank | 80 metering/check-opening heads with head shutoff and face sealing; 6,400 chamber checks, piston seals and mating ports; bleed/containment; ≥6,400 docking cycles/full map | Same reserves allow ≤$2.325/head, but different head/shared functions invalidate equal-price comparisons |
| Direct rack, ADR-017 | Four-bank comparison has 320 complete positioning heads and positive support without fluid state | 18.854-s prior allocation; sourced servo route over budget; cheap complete drives unresolved |

All satisfy `Cshared + Nhead Chead + 6400 Ccell ≤ $500` jointly, not separately.
With two banks, raising shared reserve to $350 leaves **$.5375/head** at $.01/cell;
$250 shared and $.04/cell already fail with free heads. These are inverse targets,
not invented prices. Printed parts have no formal ceiling but retain substantial
printing, assembly, leak-test and service burden. Geometry is insufficient for
print-time estimates; none are fabricated here.

Continue one bounded finite dry three-state valve/head design with positive
return, grounded force path and complete actuator stroke/force/envelope. It must
fit the **chunked** time margin and show a credible complete bought-channel path;
cheap bare actuators do not satisfy the budget. Resolve pressure-sign closure,
stem-volume exchange and unloaded lowering before full-board reliability. Reject
or conclude if that gate produces only nominal slots/affordable imaginary parts.
Wet reopening requires a complete changed acquisition/metering sequence with
bounded pressure/volume and joint time/cost; further fixed-passage tuning remains
stopped. No printing or purchase is justified.

Self-review checks volume/pressure limits and scaling, an independent midpoint
integration of nonlinear compliance at 100/200/400 subdivisions, inherited
single-bank replay, monotonic schedule sensitivities, unsafe sequence injection,
pump-starvation witness and its 40-channel escape. No hardware pass follows.
Reproducible JSON is omitted; executable source and unique failures are retained.
