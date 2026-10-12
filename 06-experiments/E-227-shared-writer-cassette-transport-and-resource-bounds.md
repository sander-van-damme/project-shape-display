---
status: complete
builds-on: [E-226, E-218, E-222]
---

# Shared writers trade selectors for cassette transport machinery

**End this full-row cassette-handling trajectory before local refinement.**
Moving E-226's unloaded writers outside the display removes bank-local turnover
collisions, but the explicit side-extraction/overflight topology needs at least
**7 writers, 21 shuttles and 7 transfer handlers** under its nominal timing
assumptions, before startup and queues. These are separate resource lower bounds,
not a feasible machine. A finite-buffer FIFO replay first meets 30 s at a
**sampled allocation of $3,012**, with 16 writers, 40 shuttles, 16 handlers and
80 spare cassettes. Doubling assumed linear speed/acceleration gives a $1,368
sampled allocation. No sourced BOM, complete routed assembly or hardware pass.

Input main `0145b15`. Reproduce:
`python3 tools/curated-experiment-checks/E-227/transport.py`.
Evidence: **constructed transport topology, finite interval calculations,
resource bounds and discrete-event simulation with explicitly assumed timings
and cost allocations**. No calibration, physical measurements or independent
review. The result rejects this allocation of full-row media; it does not prove
all shared programming or all possible cassette transport impossible.

## Concrete handling transaction and its favorable relaxation

Coordinates: x along an 80-column row (406.4 mm allocated length), y across rows,
z vertical. Retain E-226's locked 80-bar cassette: upright longitudinal bar union
104 mm; two bearing lanes; common comb retains each independently written offset.
Each bank has an x extraction carriage, y row indexing, and two z lift/arrest
sets. It carries target and outgoing cassettes in two nests. Other rows retain
their grounded cassettes. The new profile is raised before the old lowers, using
E-218's ideal `max(old+a,target+b)` support law. All 80 cells of a touched row
hand off; unchanged rows are neither reset nor deliberately moved.

Incoming and outgoing media travel upright. At the 113-mm lowered position,
extract the full cassette length in x: **414 mm** clears the 406.4-mm board
projection by 7.6 mm. The next target returns through that x corridor. Underboard
y indexing stays within the bank's assigned rows; it happens below resident bars.
Two loaded z strokes and two empty returns remain required. Exterior docks
receive incoming/outgoing cassettes, so writing can overlap other banks' motion.

One exterior y/z transfer gantry supplies all banks and writers. A parked
upright cassette occupies z=[-52,+52] around its comb. Lower a transported
cassette **112 mm** before crossing the parked cassette field: its top is now
-60, leaving 8 mm below the parked bottoms. Raise at the selected dock/writer.
Thus each delivery or collection owes **two 112-mm z strokes**, plus y travel.
The writer rotates unloaded media in a 112.012-mm bay, resets and writes the
horizontal bars, reads offsets, closes/proves the comb, seats/readbacks upright,
and presents it for collection. Its bay must remain outside resident media and
the transfer corridor. The transfer gantry positively retains the cassette;
pad friction is never credited during transport.

This is a finite conservative crossing route, **not a universal minimum**:
separated horizontal corridors could remove overflight, but need their own
routing, forks, occupancy and resource ledger. Here, a single gantry is already
excluded by its 189.54 s aggregate vertical handling work for 81 transactions,
even if all y moves take zero time. Multiple gantries require separated paths or
interlocks; no 7- or 16-gantry collision-free assembly is constructed.

The scheduler deliberately **grants** those parallel paths and all-to-all access,
zero nominal y displacement, instantly available dock identities and the stated
short capture/proof allowances. They favor the candidate. Actual dock-to-writer
routing, conveyor alternative, carrier/frame sweeps, staging transfers, drive
mounts and access remain unknown. The cheap resource/cost screen fails without
resolving them, so do not spend a geometry campaign making the gantries fit.

## Full cycle, buffer accounting and timing

Assumptions: rest-to-rest linear v=200 mm/s, a=8,000 mm/s²; E-226 .375-s unloaded
quarter-turn; no claim of gravity following at these accelerations. Let t(d) be
triangular/trapezoidal rest-to-rest time. Per row:

- Writer: E-226 horizontal writing 1.219379 + two turns .750 + .300 for
  capture/comb/registration/read/seating = **2.269379 s**.
- Bank shuttle: two t(414) + two [t(40)+t(73)] + two t(113) + two t(2.4) +
  t(5.08) + .200 for docking/proof = **6.919682 s**. Lateral lane and y moves
  are assumptions; arbitrary bank access can take longer than one row hop.
- Handler: two t(112) + t(y distance) = **1.170 s at y=0**, for each of delivery
  and collection. No additional gripper actuation/proof time is charged here.
- Global receive/referencing/final verification allowance: **2 s**.

The simulated map needs 80 row services plus one extra full service assigned to
the first bank. This is an **81-service capacity stress case**, not a proven
causal recovery bound: faults detected after a queue fills may incur more delay.
Arbitrary five-height data are written after receipt; no prewritten media credit.
The last outgoing cassette returns to storage inside the cycle. `playable_seconds`
also reports the earlier final exchange endpoint; storage cleanup cannot vanish
from sustained arbitrary-map throughput. Both remain conditional on proof time.

For B equal-size banks (B divides 80), S=1/2/3 spare cassettes per bank circulate:
write → handler delivery → bank shuttle/exchange → handler collection → write.
Resident outgoing media become the next blank. Allocate S incoming and S outgoing
staging slots per bank, plus one bed per writer. All initial spares are unprogrammed.
Each writer remains occupied after writing until a delivery handler picks up.
Each bank has only one shuttle; buffered targets wait. Media tokens are released
for another job only after collection. No infinite media inventory or free
simultaneous reuse. Common storage-to-bed transfers are granted within the writer
allowance; their mechanics and distributed locations are not constructed.

Independent **necessary** resource counts are
`floor(81 * service / 28) + 1` (strict <30 s), with two handler services/job.
They give W≥7, B≥21, H≥7. At 80 jobs without the extra service B≥20; neither
figure establishes sufficient parallelism. Seven writers already mean 560
binary selectors. For the simple S=1 policy, each bank's cycle is 11.529061 s;
B=40 plus its extra transaction needs at least three cycles, regardless of
unlimited other resources. Buffers can overlap phases but consume real media.

FIFO discrete-event grid: W=4/6/7/8/10/12/16/20,
B=10/16/20/40/80, H=1/7/8/12/16/20, S=1/2/3.
All 720 resource/buffer combinations per scenario are evaluated. This is a
specified scheduling policy, **not global scheduling optimization**. More buffers
can worsen FIFO order; selecting buffers or resources is not proof of monotonic
speedup. Counts below minimize only the explicit sampled cost allocation.

| Scenario | W / B / H / S | Selectors | Simulated complete s | Assumed allocation |
|---|---:|---:|---:|---:|
| Small shared pool control | 6 /20 /1 /1 | 480 | 193.809 | $1,302 |
| Near aggregate counts (B still below 21) | 7 /20 /7 /1 | 560 | 59.645 | $1,479 |
| Nominal sampled <30 s | 16 /40 /16 /2 | 1,280 | 29.708 | $3,012 |
| Each handler leg adds 100-mm y travel | 20 /40 /20 /2 | 1,600 | 28.418 | $3,320 |
| Each handler leg adds 200-mm y travel | 20 /40 /20 /2 | 1,600 | 29.418 | $3,320 |
| Loaded lift has 1-mm arrest/proof steps | 12 /80 /12 /1 | 960 | 28.705 | $4,384 |
| Linear v=400, a=16,000; rotation unchanged | 8 /16 /7 /2 | 640 | 28.848 | $1,368 |
| Rotation .750 s each | 16 /80 /16 /1 | 1,280 | 29.578 | $4,692 |

The nominal 29.708 s is **not a product pass**: routing, causal fault recovery,
physical readback and load following are granted. E-226's bank-owned control
has 1,600 selectors/26.995 s only with free routing; its separated bays need
85.001 s. This shared pool saves 320 selectors in the nominal sampled comparison,
but adds 40 transport carriages, 16 handlers and doubles the media to 12,800 bars.

## Whole-machine ledger and economic tipping points

At W=16, B=40, S=2 (two resident rows and two spares per bank):

| Function | Per cell / resident row | Bank or writer | Board |
|---|---|---|---:|
| Display columns / guide stations | 1,2 /80,160 | 160,320 per bank | 6,400 /12,800 |
| Support bars / positive comb contacts | 1,1 /80,80 | 320 each incl. spares/bank | 12,800 each |
| Bar guide stations / five notch sites | 2,5 /160,400 | 640 /1,600 per bank | 25,600 /64,000 |
| Common comb+keeper sets | shared /1 | 4 per bank | 160 |
| Alternative grounded row docks | shared /2 | 4 per bank | 160 |
| Writer binary fingers / guides / drag sites | writer-owned | 80 each/writer | 1,280 each |
| Shuttle x / y axes, two z/arrest sets | bank-owned | 4 axes +2 arrests | 160 axes +80 arrests |
| Writer reset / sweep / turnover axes | shared | 3/writer | 48 axes |
| Handler y/z axes + carrier grip/proof | shared | 2/handler +1 fixture | 32 axes +16 fixtures |
| Staging docks / writer beds | shared | 4/bank /1/writer | 160 /16 |

Thus **240 continuous motion axes** in addition to 1,280 binary selector
functions, before additional feed/clamp axes or motor sharing mechanisms. Axis
counts do not prescribe a motor each; linking them requires supported independent
parking and cannot inherit independent scheduler resources for free (E-222).
No resident individual springs, motors or inserts are proposed. Writer spring
returns, bearings, fasteners, fixture keepers, wiring and inaccessible interfaces
remain unspecified, not zero. 406-mm structures require joined printed modules.

Explicit deliberately low **assumed allocations, not supplier quotes or cost
floors**: $8 per complete continuous axis; $.35 per binary selector; writer
reader/comb/capture $5; shuttle two arrest sets $6 and fixtures/readback $4;
handler carrier/readback $4; shared frame/control/power/wiring $100. Therefore
`C=100 +57W +42B +20H`. Printed structures/material/labor are excluded.
At the nominal aggregate necessary counts alone C=$1,521; even the doubled
speed counts W=6/B=11/H=4 give $984 before scheduling. Lower component prices
could change this arithmetic, but no such complete procurement route is known.

Price-independent useful ceiling: with $100 reserved and 560 selectors at the
hypothetical $.35, **only $204 remains** under $500 for all 21 shuttles, seven
writers' shared axes, seven handlers, arrests and sensors. All of that divided
by 21 is **<$9.72 per shuttle**, granting the other systems free. This is a
budget tipping point, not an asserted minimum price. Reopening needs a changed
transaction that shares motion without restoring missing retention/transport.

Solid 64×3.4×1.6-mm bars total **4.456 L**, before the 4.608-L column-stock
comparator, frames, cassettes, beds and moving gantries. At assumed effective
5–15 mm³/s and 10% scrap they need **91.7–275.1 h**; 12,800 bar insertions at
10–30 s need **35.6–106.7 h**, plus columns, 1,280 selectors, 160 comb sets,
160 row docks, staging nests, axes and calibration. Not sliced or measured.
Each 406.4×112.012-mm writer bed allocates .0455 m²: sixteen sum to **.728 m²**
before motors and access. Stacking does not remove transport travel/occupancy.
At least one side needs 414-mm extraction reach beyond the board. Compactness
has not been demonstrated.

## Manufacturing, load support, faults and decision

The new transport clearances are broad *allocations*: 7.6 mm side clearance and
8 mm overflight. Opposing ±.35-mm rigid position bounds leave 6.9 and 7.3 mm,
respectively, but carrier protrusions, row-span bow and common frame error are
additional. These are scenarios, not X1C capability or full swept CAD. Transport
does not improve E-226's .8-mm bearing-lane gap (.1 mm under opposing ±.35),
4-mm notch/2-mm tooth axial play of 2 mm, actual seated-height readback or common
comb force distribution. Do not refine those repeated interfaces for this machine.

Load path during play remains column → bar → positive common comb → grounded
dock → frame. Loaded exchange needs grounded arrest on both z lifts at every
intermediate stop. At assumed 1/3.27/10 N per cell each row needs
80/261.6/800 N support, plus inertial/guide forces. Horizontal writer force and
pad-relaxation uncertainties remain E-226's bounds. No drive torque, print-layer
strength, fatigue, friction, bar buckling or creep has been qualified.

Before pickup, invalid profile/comb/seating proof leaves the existing row
supported. Transport loss must retain the common comb and carriage fixture;
loaded loss additionally needs both z arrests. A cassette cannot be released
based only on actuator position. Height, load support and dock engagement proofs
remain unbuilt. A writer fault affects served banks; a shared bus obstruction
can stop the full map. Positive support must remain during jam clearing and
module replacement. Common reader offset, bed/comb warp, frame deflection and
power loss are correlated row/bank faults, not 6,400 independent trials.
Unchanged cells in a touched row can still settle by opposing support-height
errors; no disturbance or recovery qualification follows from the ideal law.

**Stop this full-row travelling-cassette route.** Its shared-writer escape
replaces selectors with numerous independently supported transport resources,
extra media and large external workspaces. The simple common-gantry version
fails throughput; granting many parallel gantries still fails the explicit
allocation by a wide margin. This is enough to redirect research without proving
all layouts impossible. No printing or finger/pad/comb development is justified.
Reopen only through a concrete transport topology that removes full-row travel
or greatly reduces independent handling while retaining supported return,
arbitrary in-cycle writing and service access.

Next research should synthesize **resident support memory with shared addressing**,
using this transported-media control to price movement rather than silently
adding another cassette buffer. First reconstruct earlier resident-mask and
crossed-support failures; generate a changed causal combination before local
geometry. A new support law or addressing transaction is needed, not another
finer latch or an uncosted multi-gantry layout. No replacement architecture is
selected by this negative screen.

Verification: serial one-resource replay equals the independently summed 81
cycles; 80 fully independent resources without retry equal one complete chain;
all runs check processing counts, resource exclusivity, bank job counts, final
resource release and aggregate work bounds. Exact interval checks verify stated
side/overflight clearances. Sensitivities separately change travel, rotation and
loaded arrest. These checks establish internal model consistency only. No
collision-free multi-handler routing, gravity contact dynamics, causal recovery
proof, physical fabrication or independent validation is claimed.
