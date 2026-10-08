---
status: complete
builds-on: [A-013, A-007, ADR-010, Q-012, E-015]
---

# Row memory: complete-machine necessary-condition screen

## Scope, source and decision

Retain A-013 for bounded complete-channel costing and contact synthesis, not
product selection. No architecture passes all uncertainty bounds. This is
within-topology enumeration, not hundreds of new mechanisms. No physical
measurements, calibrated priors, quotes or validated CAD are used.

Initial input `73ec9eb`, checkpoint `5f30a98`: adding acceleration, row-index
travel and support/section checks changes optimistic rack time from 24 to
29.350 s. Run Python 3 standard-library sources
`tools/curated-experiment-checks/E-050/row_screen.py` and `joint_envelope.py`.
They emit exhaustive cases as JSON; reproducible output is not retained. No
random seed, probabilistic yield or mesh-convergence claim applies.

## Complete comparators and original screen

| Family | Addressing, state, isolation and recovery | Burden / failure |
|---|---|---|
| Rack A-013 | Independent linear grippers unload individually released grounded pawls; only targets unlock; encoder/optical/support read and gripped retry | 6,400 racks/pawls/returns; ≥19,200 guide/latch/grip interfaces; complete channel cost and contact geometry unresolved |
| Screw A-007 | Independent rotary sockets; thread-angle memory; nut/base load path; height read and re-dock/retry | 6,400 screws/nuts; ≥12,800 thread/socket interfaces; timing-favored high leads need brake or proven retention |
| Trapped fluid | Shared pressure/return pump, independent metering heads; normally closed dock-opened valves; closed-valve dwell/read then re-meter or stop | 6,400 seals/valves; ≥19,200 contacts; leakage, common contamination and pressure hardware unresolved |

All reach arbitrary five-state maps only in the ideal state model. Fluid uses
a double-stroke refill proxy, not a pressure-network solution; screw omits
angular acceleration. Added mechanical locks/brakes change their accounting.
Magnetic writing, nested binary supports and mechanically latched pressure
cells were not searched and cannot be ranked by this generator.

Original schedule: 75 cases, three families × 8/16/40/80/160 lanes × three
scenarios, with 1/2/4-mm screw leads. Fast/central/slow bounds respectively:
v=400/200/80 mm/s, a=20,000/5,000/1,000 mm/s², spindle=6,000/3,000/1,000 rpm,
contact=0.04/0.08/0.16 s, read=0.01/0.02/0.04 s, minimum index=0.025/0.05/0.10 s,
map overhead=2/4/8 s, extra full-station cycles=0/1/8. Competing assumptions,
not confidence intervals. Overhead must cover homing, digital preparation,
final settling and registration; external preparation is not free.

Rest-to-rest travel is `2 sqrt(d/a)` below crossover, otherwise `d/v+v/a`.
Enumerate unequal old/new states 0/10/20/30/40 mm and home→old→new→home.
Worst rack path is 40→20 (or reverse), 80 mm with three stops. Index includes
physical lane-block travel. Stations = row groups × column groups; partial-width
row-wrap travel is omitted, so those failing schedules are optimistic bounds.
Jerk, elasticity and read latency remain model discrepancy. Fixed overhead is
not a no-op estimate; scattered changes can require every row.

64/75 timing cases fail; survivors: rack 2, screw 7, fluid proxy 2. Fast rack
80/160 heads: 29.350/16.216 s; central 160: 33.052 s (fails <30). Reducing
fast acceleration to 10,000 mm/s² makes 80 heads take 35.206 s. Initial aligned
160-head 5×5: 3.066/6.752/24.461 s. The extension below supersedes the original
limited head-count frontier and checks adverse alignment.

Square-thread self-locking requires `mu > lead/(pi*3)` for 3-mm mean diameter,
ignoring collar help: 0.106/0.212/0.424 for the three leads. None robustly
survives assumed mu=0.08–0.30; at 0.30 only leads 1/2 may hold. Retain A-007's
rejection without rejecting all screw machines.

Fluid at assumed 10 N on a 3-mm bore needs 1.415 MPa. Assumed ≤0.1-mm drift
in four hours needs leakage ≤4.91×10⁻⁵ mm³/s/cell; no prior supports it.
80 pistons at 400 mm/s require ideal 226,195 mm³/s flow and 320 W at that
load, before losses. Stop timing refinement until retention/sealing is credible.
These load/drift bounds are research assumptions, not product requirements.

## Manufacturing and support screen

243 rack sections enumerate overlap 0.6/0.9/1.2 mm, tooth thickness 1/1.5/2 mm,
three error bounds, E=500/1,500/3,000 N/mm² and loads 1/10/100 N. Geometry:
2.4-mm web, 0.8-mm support wall, 1-mm cantilever reach, 2.4-mm tooth width,
10-mm tooth spacing. Gates: residual overlap≥0.4 mm, width≤5.08 mm,
stress≤8 MPa, deflection≤0.1 mm. These are unqualified scenario bounds.

Relative error sums print-wide bias + regional warp/alignment + local fit:
tight 0.05+0.05+0.05=0.15 mm; middle 0.10+0.10+0.15=0.35;
wide 0.20+0.20+0.20=0.60. Shared terms affect all cells, not independent draws.
Hole shrinkage, wall variation, layer quantization and roughness are aggregated;
exclude first-layer interference from working faces. No fatigue/creep/wear
prior is invented; the elastic screen cannot establish long-term retention.

48/243 pass (tight 36, middle 12, wide zero). None passes every bound at 10 N;
none carries 100 N under the stress limit. Middle witness: overlap 0.9/tooth
2 mm at 10 N gives residual 0.55 mm, width 4.80 mm, 6.25 MPa and 0.00417-mm
deflection at E=500 MPa. Independently, overlap≥0.4+error and
≤1.88−2error imply error≤0.4933 mm for any overlap: the wide failure is not
a grid artifact. Staggered wider supports escape this section constraint.

This is a 2D section, not swept contact CAD. All 25 transitions check ideal
support order latch→latch+grip→grip→grip+latch→latch and ≤80-mm path, not
executable geometry. Grid deflection, seam preload, buckling, impact and neighbor
friction are excluded. E-015's 100 N is sensitivity, not a new cell requirement.

False accepts at assumed per-cell rates 10⁻³/10⁻⁴/10⁻⁵ give expected
6.4/0.64/0.064 missed cells per board by linearity, without independence.
Shared reader/registration error may misaccept a whole row. No board reliability
is claimed; retries cannot repair common bias, and persistent faults stop a bank.

## Whole-machine burden and self-review

Original 54 budget cases: reserves $150/250/350, 80/160 heads at assumed $1/3/6
and purchased cells $0/0.02/0.05; ten fit ≤$500. Exact joint ceilings below
replace that sparse price grid, not its missing supplier evidence.

Solid 2.4×2.4×60-mm columns alone allocate 2.212 litres for 6,400 cells.
Assumed deposition 5–15 mm³/s gives 41–123 print hours before tops/racks/pawls/
guides, waste or reprints. Assumed 10–30 s insertion/inspection per cell gives
18–53 assembly hours. Infill/orientation remain unresolved. All families need
X1C-compatible modules, underside access and 40-mm stroke plus support/head
depth; compactness is not established. Printed parts are not burden-free.

Self-review assertions check motion zero/crossover limits, a separately
hand-computed row schedule, station counts, all 25 transitions and no 100-N
section survivors. The independent overlap inequality explains wide-error
failure. No independent validation or demonstrated feasible Pareto set follows.
Do not print or refine FEA from these screens; resolve complete channel cost,
load-dependent motion and implemented support transitions first.

## Joint row-bank timing, recovery and purchased-cost extension

Input `dc19a58`, with the initial E-058 result from `ada308f` consolidated here; `python3 tools/curated-experiment-checks/E-050/joint_envelope.py`
couples the previously separate timing and budget screens. This is deterministic
system accounting within A-013, not a new mechanism or supplier BOM. It enumerates
1–80 complete rows of independent heads (80–6,400 channels), three inherited
motion scenarios and 0/1/8 additional full-station retries: 720 timing cases.
No probability or calibrated manufacturing prior is introduced. A retry repeats
motion, contact and read while remaining at the station; reacquisition after a
lost grip, fault diagnosis and re-indexing would add time. Persistent/common-mode
faults are outside successful-update timing, not cured by retry allowances.

For r rows of heads and k retries, retain the original allocation:
`T = overhead + ceil(80/r)*(cycle + index(r)) + k*cycle`, where cycle includes
worst unequal-state home→old→new→home motion, contact and read; index is the
larger of the inherited minimum and rest-to-rest travel of r row pitches.
This charges an index at every station, including the last, as E-050 does.
It is a conditional schedule allocation, **not a universal physical lower
bound**: exact last travel/return, banking geometry, simultaneous power, moving
bank mass and overhead may change it. Larger banks are granted the same
acceleration and reserve to expose their most favorable budget envelope;
that scaling is not established. Non-divisor banks need inactive heads at the
board edge. Their packaging and isolation are unimplemented.

Minimum timing-feasible head counts under this allocation:

| Motion scenario | Retries | Heads | Full map s | Channel ceiling at $500 total, $250 reserve, no cell purchases |
|---|---:|---:|---:|---:|
| Fast | 0 / 1 | 80 | 29.350 / 29.660 | $3.125 |
| Fast | 8 | 160 | 18.696 | $1.5625 |
| Central | 0 / 1 / 8 | 240 | 23.877 / 24.497 / 28.837 | $1.0417 |
| Slow | 0 / 1 | 640 | 28.280 / 29.720 | $0.3906 |
| Slow | 8 | 2,160 | 29.223 | $0.1157 |

Fast 80-head operation permits only two full-station retries before exceeding
30 s (29.970 s for two; 30.280 s for three). These counts are explicit fault
budgets, not predicted failure frequency or board reliability. Central timing
can be rescued algebraically by a third row of heads; E-050's 160-head failure
must not be generalized to all independent-head counts. The rescue tightens
rather than resolves the cost problem.

For complete-channel cost c, purchased-cell allocation p, shared reserve B and
ceiling C, `c <= (C-B-6400*p)/(80*r)`. All grip/position/release actuators,
drivers, links, sensing and connectors must be assigned exactly once between c
and B; printed returns have print/assembly burdens even when p=0. The script
reports exact rational channel ceilings for all 80 bank sizes: C=$200/$400/$500,
B=$150/$250/$350 and p=$0/$0.02/$0.05 (2,160 budget cases). C=$200 is
strict for the ideal tier; $400/$500 ceilings are inclusive. Negative allowances
reject even free channels; zero leaves no positive channel budget.
These are competing budget scenarios, not quotes or manufacturing distributions.
At C=$500, B=$250, p=$0.02, the 80/160/240-head channel ceilings fall to
$1.525/$0.7625/$0.5083. At C=$400, the 240-head ceiling is $0.625 with
p=0, or $0.0917 with p=$0.02. At B=$250, p=$0.05 already exhausts the
$500 cap before buying any channel. More generally p must be below
$0.0390625 to leave any positive channel budget in that scenario.

Positive c and fixed B,p make the smallest timing-feasible bank the largest
per-channel allowance; the search does not assume time is monotone in r.
Larger banks can buy timing margin, but cannot rescue a channel that exceeds
that maximum without changing assumptions. Fixed row partitions also make
regional work alignment-dependent: a contiguous five-row update occupies two
or three stations with a three-row bank, rather than always ceil(5/3)=2.
The script checks every legal start row for every bank size, and reports
aligned (start row zero) and adversarial (maximum over starts 0–75) 5×5 times
for all 720 cases. Column selection is still assumed independent; unchanged
channels remain latched. An adversarial scattered update can touch every bank
and require the full-map allocation despite few changed cells.

| Motion, retry budget | Minimum heads | Aligned / adversarial 5×5 seconds | Maximum full-map retries | Exact channel ceiling, $500 cap / $250 reserve / p=0; p=$0.02 |
|---|---:|---:|---:|---|
| Fast, 0 | 80 | 3.709374 / 3.709374 | 2 | $25/8; $61/40 |
| Fast, 8 | 160 | 5.546200 / 5.546200 | 44 | $25/16; $61/80 |
| Central, 1 | 240 | 6.092400 / 6.828600 | 9 | $25/24; $61/120 |
| Slow, 1 | 640 | 11.468000 / 13.496000 | 1 | $25/64; $61/320 |
| Slow, 8 | 2,160 | 22.754500 / 25.989000 | 8 | $25/216; $61/1080 |

Times are conditional arithmetic, rounded here; precision is not evidence of
motion accuracy. These regional times retain a bank-step index per station and
the fixed overhead. Initial dispatch from an arbitrary parked location and
return must fit that overhead or be added; no location-independent regional
hardware-time guarantee follows. No untouched-cell disturbance is proven.

For any workload with n stations, reject when
`overhead + n*(cycle + index) + k*cycle >= 30`.
The largest nonnegative retry count is `ceil((30-T0)/cycle)-1`; if T0≥30 no
retry count passes. The source checks the passing count and its failing
successor, reporting -1 for no feasible count. These are total serialized extra
station cycles per update, not retries per cell or per station. Independent
heads inside a station run concurrently. A single retained fault can exhaust
the entire allowance; increasing heads does not bound diagnosis or false accepts.

The simultaneous cost/timing rejection is explicit: for a given scenario and
retry budget choose the smallest passing bank r_min. At fixed B,p, any positive
complete-channel price above `(C-B-6400*p)/(80*r_min)` rejects **every** tested
bank, regardless of possible nonmonotonic time with r. A price at the ceiling
passes only an inclusive cost tier and still needs timing and all omitted
hardware evidence. Necessary purchased-cell threshold for any positive channel
budget is `p < (C-B)/6400`. At C=$500, B=$150/$250/$350 these thresholds are
exactly $7/128, $5/128 and $3/128 per cell. Thus p=$0.05 leaves only $30
for channels at B=$150 and already rejects B=$250/$350 before channel purchases.
All price ceilings assume the reserve actually covers the shared hardware;
scaling its load, power or guide cost upward can only shrink the envelope.

Self-review: reproduce both original 80/160-head timing cases in all scenarios;
verify the fast 80-head result using a separately written motion expression;
check retry increments, strict-limit neighbors, and exact rational cost recomposition; independently enumerate
row sets for all 6,080 bank-size/start combinations. Finite enumeration, no seed,
mesh or convergence claim. Reproducible JSON remains untracked.

**Decision:** retain 80/160 heads only under fast motion, with the stated retry
scope; add 240 heads as a conditional central-motion comparator. Do not grow
head count as an uncosted cure or continue local pawl/FEA refinement first.
The next discriminating result is one complete realizable drive channel with
cost allocation and load-dependent motion, compared against these ceilings.
If none fits, switch addressing/energy-sharing principle instead of tuning
another tolerance. Reopen envelopes with changed reserve, cell purchases,
implemented schedule or sourced complete-channel costs. No geometry gate,
physical calibration or product selection is granted by this extension.
