---
status: complete
builds-on: [E-081, E-082, E-080, E-059, A-016]
---

# Mask clearing and independent banks trade scan time for many complete drives

**Differential writing does not rescue the demanding map, and banking is not
free addressing.** E-081's favorable cyclic direct-displacement map needs 240
physical row transactions, but its 21-height all-displacements map needs
**3,440**, including final clear. The representative force-limited row-clutch
scenario first meets a 30-s allocation at B=16 among the tested bank counts:
**27.410 s, 1,280 data drives and 80 row channels**. Their residual mean bought
allowance is **<$0.184/channel** with $250 elsewhere and free repeated keys.
This is a conditional time/cost intersection, not an available drive or a
qualified machine. No product architecture is selected.

Input main `407e41e`. Reproduce:
`python3 tools/curated-experiment-checks/E-083/bank_schedule.py`.
Standard-library deterministic state replay, force bounds and accounting; no
random seed, empirical manufacturing distribution, field/contact solver, CAD
assembly or measurement. All force, strength, mass, acceleration and cost
reserve values below are **epistemic scenarios**. E-082's finite joint section
and its geometric limitations are inherited unchanged.

## Actual mask state and banking topology

Use one transient command array with independently retained grip and pawl
outputs. At every acquire/deposit event in either E-081 controller, park the
cam, change the old command mask to the required set, prove the actual mask,
then apply the appropriate phased output cam. All writers withdraw before the
cam moves. Reuse an identical mask without rewriting it; no credit is taken for
skipping the output action or its support proof. At the end clear the command
array to zero, even though the final columns are already grounded. This is
command reset, not resetting column heights. Initial unknown states require
homing/readback and are not silently accepted as zeros.

Write every row where the **entire old and next binary vectors differ**, with
both set and reset bits; keep unchanged bits unchanged. A row absent from the
next selected set may still need clearing. Example: `{(row0,col0)}` followed by
`{(row1,col0)}` takes 1+2+1=4 row transactions including final clear, rather
than two selected-row visits. Conversely, two identical one-row masks require
only initial write and final clear. Cam motion during a partial rewrite is
forbidden; stale commands otherwise actuate the wrong cells.

Split the 80 rows into B contiguous independently programmed banks, with
B in {1,2,4,5,8,10,16,20,40,80}. Each bank has **80 independent push/pull data
drives and 80/B key feet per data bar**. It may process one local row at a time;
banks operate concurrently and synchronize before each global output event.
For each mask transition, rounds equal the maximum dirty-row count among
banks. This is an explicit barrier schedule, not an optimal pipeline. It
requires physically separate bars/drives; broadcasting one 80-bit vector to
several rows cannot write arbitrary independent row vectors. No shared-drive
or external row decoder is credited without a mechanism and timing model.

| Workload/controller | E-081 selected-row count | Physical transactions with differential writes and final clear | Rounds at B=8 |
|---|---:|---:|---:|
| Five-height cyclic, direct displacement | 320 | 240 | 30 |
| Five-height cyclic reset or all-displacements under either controller | 800 | 880 | 110 |
| 21-height cyclic, direct displacement | 320 | 240 | 30 |
| 21-height cyclic reset or all-displacements under either controller | 3,360 | 3,440 | 430 |
| Uniform zero to positive height | 160 | 160 | 20 |
| 5×5 patch, five target states, 21-height workload | 30 | 35 | 35 |

The patch is entirely within one eight-bank strip and gains no parallel speedup.
For all-displacements, all 80 rows contain the same height-pair coverage,
forcing 2H nonidentical command sets; initial write plus 2H−1 changes plus final
clear gives `80(2H+1)`. For cyclic direct movement the acquire/deposit sets are
identical within each sign, giving only initial negative write, change to
positive, final clear: `3*80`. These are workload proofs, not an arbitrary-map
worst-case theorem. Height states remain workload choices, not a new product
requirement. Unchanged maps do nothing.

## Force-compatible timing screen

Retain E-082's d=1.2-mm dog, S=1.85-mm socket, 1.0-mm pin and ±0.10-mm box.
The 0.025/0.030-mm insertion/neighbor reserves and missing y/rail/detent geometry
remain; banking does not relax these fits. At assumed sigma=10 MPa, minimum
pin width 0.9 mm and 1-mm bending lever, `Fcap=sigma*b³/(6L)=1.215 N`.

With common drag f per foot and 0.3-N required dog force, shortened bars give
`Freq=(80/B)f+0.3`. For series stiffness k N/mm and the inherited 0.8-mm contact
uncertainty span, `Fpeak=Freq+0.8k`. Reject Fpeak≥Fcap. Use half the remaining
static margin for inertia, retaining half for unspecified limiter/overshoot
error: `a_x=min(a_requested,0.5(Fcap−Fpeak)/m)`. This conservative scalar screen
still does **not** solve elastic bar/spring dynamics or establish a jam limiter.
Actual dynamic amplification can defeat it. No independent-cell averaging
reduces common drag or geometric error.

A chosen row cycle has three horizontal rest-to-rest legs: prepare 1.2 mm,
drive `1.2+0.825+Freq/k`, unload `0.825+Freq/k`; plus two 1-mm vertical legs.
Each takes `2 sqrt(D/a)`, D in metres. Vertical acceleration is an independent
scenario; its rail load, force limiting and extraction interlock remain unproved.
No speed cap is imposed. Add assumed **6 s** for elevator motion, all output cams,
support proofs, non-row settling/recovery and overhead. Per-round address,
readback and extra settling must fit the remaining allowance. The 6 s is not a
measured or proven sufficient value and is not added to elevator time a second
time. Flexible resonance, electrical duty and support-contact dwell remain gates.

Representative f=0.005 N, k=0.5 N/mm, m=20 g **per data drive**, sigma=10 MPa,
requested horizontal/vertical a=20 m/s², adverse 21-height map:

| B | Parallel rounds | Row-cycle motion | Total with 6-s reserve | Data drives | Mean allowance across data+row channels, $250 elsewhere |
|---:|---:|---:|---:|---:|---:|
| 1 | 3,440 | 193.814 ms | 672.719 s | 80 | <$1.5625 |
| 4 | 860 | 107.826 ms | 98.730 s | 320 | <$0.6250 |
| 8 | 430 | 102.132 ms | 49.917 s | 640 | <$0.3472 |
| 16 | 215 | 99.580 ms | 27.410 s | 1,280 | <$0.1838 |
| 20 | 172 | 99.090 ms | 23.043 s | 1,600 | <$0.1488 |
| 80 | 43 | 97.657 ms | 10.199 s | 6,400 | <$0.0386 |

At B=16, Freq=0.325 N, Fpeak=0.725 N, a_x=12.25 m/s² and model peak including
inertia is 0.970 N. Remaining force allowance is 0.245 N. The 215 rounds have
**<12.048 ms each** for all row overhead beyond model motion with that fixed
six-second allocation. This is a fragile conditional survivor, not a speed
claim. A single-bank failure stops the shared cam barrier; nominal parallelism
does not remove common-cause faults or permit bypassing support proof.

Cross B above, f={0.005,0.010,0.030} N, k={0.1,0.5,1.0} N/mm,
m={5,20,50} g, requested horizontal/vertical a={20,100} m/s² and
sigma={5,10,20} MPa: **1,620 deterministic scenarios**, 552 fail static force,
610 fail the deadline after static acceptance, 458 retain positive nominal
time allowance. None includes a demonstrated drive, reader or complete BOM.
For each drag/mass/acceleration/strength tuple, allowing the best of the three
stiffnesses yields minimum sampled bank counts from 8 to 80. At m=20 g,
a_requested=20 m/s² and low drag, reducing sigma from 10 to 5 MPa raises that
minimum from 16 to 40. At sigma=10 MPa, raising drag to 0.030 N raises it to 20.
Do not interpret scenario fractions as yield, or the chosen k grid as global
optimization. Mass is held as alternative bounds across B; no unmodelled motor,
gearbox or frame mass is assumed to disappear with shorter bars.

## Complete-system ledger and comparison

One mechanical command array repeats 6,400 dogs, endpoint retention sites,
captive keys and sliding feet, plus 80 row rails, 80B data bars and force-limited
bidirectional drives. The **active** bar span is 406.4/B mm; total active bar
length stays 32.512 m before supports, overhangs and module joints. B=16 has
25.4-mm active spans but 1,280 transmissions to pack and service. At 20 g per
drive the equivalent translating masses sum to 25.6 kg if all data axes move;
this is a model consequence, not weighed material or a proposed layout.
Dog guides, bar bearings, retention springs/stops, extraction verification,
output cams, two persistent output functions per column, grounded support,
elevator, controller, wiring, power, height/command readers and replacement
access all remain inside the product boundary. There is no full packing or
assembly-time estimate. Replicated fits and assembly are explicitly counted,
not assigned zero labor because printed material has no formal cost ceiling.

With free keys and $250 for everything besides channels, B=16 allows
<$0.1953 per data drive **before any row drive**, or <$0.1838 averaged over all
1,360 channels. A hypothetical $0.02 bought key uses $128 and reduces those
allowances to <$0.0953/<$0.0897. At $400 elsewhere and free keys the all-channel
allowance is <$0.07353. These are inequalities, not quotes. They cover the
complete actuator/transmission/limiter/control channel, not a bare driver IC.
E-059's dated catalog-servo prices already exceed even the B=1 whole purchased
cap; they cannot implement this banked escape. No inference that all possible
custom drives exceed these allowances follows. Two fully duplicated arrays
repeat the keys/dogs and data/row channels; independent parallel writers can
retain the same rounds but halve free-key channel allowances. Serial duplicated
programming adds corresponding transactions. An optimized persistent two-array
controller needs its own state replay; it is not credited here.

Magnetic selection needs 160 reversible row/column lines per unbanked array,
320 for two arrays; row banking with independent data buses gives `80(B+1)`
lines per array. A guided soft-pole implementation also requires **distinct set
and reset force paths**; reversing current alone cannot reset attraction.
Permanent magnets support signed torque but need a finite return-circuit,
detent and cam route passing E-080's pulse-history gate. One/two arrays repeat
6,400/12,800 flags and retention/return sites; magnets, pole pieces, coils or
shared threaded conductors must have a real manufactured routing and service
path. Reused command storage still needs separately persistent mechanical
outputs. Under the adverse transient-mask schedule, an unbanked magnetic
writer would need <24/3440=**6.977 ms per complete row transaction** with the
same six-second reserve, including both polarities as needed and readback.
E-080's dimensionless saddle times cannot establish that time.

No resistance, inductance, physical current pulse or cooling path is available
for an accepted magnetic package. Copper loss must be integrated as
`sum_lines integral I_line(t)^2 R_line dt`, including row and every active data
line, reset/retry pulses and simultaneous banks; stored gap energy is not that
loss. During dense scans one row line per bank has at most 1/(80/B) selection
duty under equal visits, but data-line duty can approach unity, and half-selected
flags still receive pulses. Neither guaranteed duty nor temperature can be
inferred from sparse maps. Banking increases active electrical concurrency as
well as line count. Unknown electrical/thermal cost prevents a magnetic win;
unknown mechanical motor efficiency prevents a claimed mechanical thermal win.

A bank reader must inspect the complete vector or equivalently prove stale bits
are absent; reading only newly selected dogs misses the injected failure. In
the 3,440-transaction case, a full 80-bit read after each row supplies 275,200
flag-state decisions, plus at least 12,800 grip/pawl support observations in the
direct controller. If genuine per-opportunity unsafe-accept bounds p_flag and
p_support existed, a union bound is
`P(any unsafe acceptance) <= min(1,275200*p_flag+12800*p_support)` without
independence. Neither bound is measured. Common optical bias or a stuck row
rail can defeat all repeated reads; retries do not repair undetected faults.
Each additional 1 ms per parallel round costs 0.215 s at B=16; retrying one
complete 80-row mask takes at least 5*99.580=0.498 s there. A persistent fault
holds the cam parked with ground/grip support and requires bank repair. Exact
repair access and acceptable detection/recovery limits remain unqualified.
Regional command state is preserved logically, but shared reaction, vibration,
and actual unchanged-column displacement are not simulated.

## Disposition and verification

Stop treating banking or differential masks as a demonstrated low-cost escape
for the tested row-clutch implementation. Preserve B≥8 algebraic survivors
only as **bounded reserves requiring an affordable complete drive and finite
retention/rail package**; do not spend another pass optimizing socket width or
assumed damping. The magnetic family remains a conditional reserve requiring
a realizable blocking/field package and admissible signed schedule, not more
threshold-only tuning. These conclusions support ADR-014's scoped campaign
closure; no broad physical-principle impossibility or fabrication release.

Self-review, not external validation: independently counted binary row-vector
changes match replay across all **4,096** three-mask histories on 2×2 sites;
an injected stale-row omission fails. All 81 two-cell old/new maps under both
controllers match E-081 command counts and selected-site counts. Full-board
and local mask counts match E-081 before physical differences/clear are added.
Closed-form adverse/cyclic counts provide independent checks of the large
workloads. B=1 force arithmetic reproduces E-082; an increased-drag failure
and half-strength failure are retained. This analytical/discrete model has no
time step, so discretization convergence is inapplicable. Model correctness
does not establish material properties, dynamic force limiting, complete
geometry, production yield, contact durability, readback or hardware timing.
