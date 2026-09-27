# R01: a separate travelling-head screen

`analyze.py` writes 60 cases to `results/multirow.csv`: 1–5 rows × 20/40/80
parallel columns × 150/300 mm/s stroke speeds × two mechanisms. Pitch stays
5.08 mm and stroke 40 mm. Last partial groups are counted with ceil; a 3-row
head needs 27 stops across 80 rows. Column groups use serpentine scanning with
accelerated diagonal transitions, then return to origin. No scanning overlap
is credited. Motor/body fan-out is necessary: adjacent 8 mm motors cannot sit
on a 5.08 mm grid. At least two ranks along a row are needed, with additional
routing space for adjacent rows, boards and compliant output shafts.

The full-width subset at **150 mm/s**, **4000 mm/s²** stroke acceleration:

| Rows | Stops | Available dwell at 27 s | Direct full stroke total | Shared stroke total | Direct head kg / axes | Shared head kg / selectors+drive |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 80 | 0.209 s | 66.97 s | 87.17 s | 1.70 / 80 | 0.94 / 81 |
| 2 | 40 | 0.461 s | 36.91 s | 47.01 s | 2.90 / 160 | 1.18 / 161 |
| 3 | 27 | 0.709 s | 26.98 s | 33.80 s | 4.10 / 240 | 1.42 / 241 |
| 4 | 20 | 0.983 s | 21.51 s | 26.56 s | 5.30 / 320 | 1.66 / 321 |
| 5 | 16 | 1.247 s | 18.38 s | 22.42 s | 6.50 / 400 | 1.90 / 401 |

All times and masses above are **calculated from assumed inputs**, not measured.
The 300 mm/s sweep retains stroke acceleration rather than simply halving times.
It gives two-row direct 29.25 s (no 27 s reserve), three-row direct 21.81 s,
four-row shared 24.31 s and five-row shared 20.62 s. Narrower 20/40-column heads
pay for extra stations; five×40 direct at 300 mm/s reaches 26.21 s but its
200 independent drives fail screened cost. No 20/40-column shared case meets 27 s.

## Transactions, reset and selection independence

**Independent:** all r×c axes raise through up to 40 mm and retract through
40 mm each stop, plus 100 ms assumed contact/settling/control overhead. A
passive per-cell latch must preserve independently chosen positions as rods
retract. Motor axes have 4 conductors each (320–1600 for full-width heads).
There is no evidence for a complete $2 full-stroke axis at 15 g; these are
optimistic costing and mass assumptions, not PM-motor specifications.

**Shared:** one common actuator advances 10 mm at each of four height planes,
rest-to-rest, with local selectors deciding which columns remain coupled; each
plane adds 20 ms selection and 15 ms settling. It then retracts 40 mm, plus
100 ms transaction overhead. The local selector travels only an assumed **1 mm**;
the shared mechanism still performs the **full 40 mm**. Each of r×c selectors
needs two conductors in this screen, plus four for the shared drive. This is
644/804 wires at four/five full rows before buses and sensors. Remote shared
power and fan-out can lower carriage motor mass but cannot eliminate independent
state selection. A fixed mask does not count as arbitrary-map programmability.

Both start from a **globally released low map**. The fixed 3 s allowance consists
of 0.5 s reference, 1.5 s release/down-reset, 0.5 s final settling and 0.5 s
inspection. None is measured; each must be timed, including gravity return and
release of the previous high map. A reset jam invalidates readiness. With only
3 s fixed overhead this is an optimistic screening bound. Extra reset/detection
time adds directly, and all selected cells reaching every level is adversarial.
The shared case must selectively disengage without dropping already held cells;
Test06/07's whole-row moving comb is unsuitable for this independence requirement.

## Mass, acceleration, force and cost

Scan v=250 mm/s and a=4 m/s² are assumed. Force `m*a` ranges from **6.8–26 N**
for 1–5-row direct heads and **3.76–7.6 N** for shared heads. Rail friction,
cable drag and motor torque/speed must be added. Minimum triangular acceleration
to move a distance d in a slot t is `4*d/t²`; keeping a five-row 25.4 mm hop
inside 160 ms requires about **3.97 m/s²**, before vibration settling. Bolting
more actuators onto a carriage does not establish this acceleration.

Head mass model is 0.5 kg frame/loom plus 15 g per direct axis; shared is
0.5 kg +0.2 kg drive +3 g/selector. Weigh actual hardware; these figures exclude
any later heavy reinforcement. At 400 columns and 10 mN drag the moving columns
alone need about 12.12 N (weight plus drag), plus shared tooling inertia and
latch forces. The large shared stroke and force remain real even though local
selector stroke is short. A jam can bend multiple outputs or stall the whole
head; force limiting and individual fault detection must be costed.

The $220 fixed hardware allowance is decomposed in `multirow_bom.csv`; it covers
scan axes/rails, power/control, reset and inspection. Direct local axes are
$2/$5/$10; local selectors $0.40/$1.50/$4.46 plus $25 shared drive. For large
banks the last value combines the sourced $3.96 solenoid tier with a $0.50
driver allowance. Its actual 12.6 g mass is greater than the custom-selector
3 g hypothesis, and 320 simultaneously powered solenoids would draw 1760 W.
That retail case needs a much larger supply, loom and head than the lean base
allowance; its shown cost is therefore already-failing lower-bound costing.
Add 20%
contingency. These are allowances, not purchasable matched assemblies. The
screen's base is deliberately leaner than Test08's lift/rotor programmer.

| Full-width choice | Optimistic / realistic allowance / conservative incl 20% | Maximum delivered local hardware price to fit $500 |
|---|---:|---:|
| 3-row direct | $840 / $1704 / $3144 | $0.819 per complete axis |
| 4-row shared | $447.60 / $870 / $2006.64 | $0.536 per selector including its driver |
| 5-row shared | $486 / $1014 / $2434.80 | $0.429 per selector including its driver |

Sourced commercial solenoids do not fit this budget. A $0.40 custom selector
is **speculative**, and five-row optimistic cost has only $14 left below the
ceiling. No measured region jointly satisfies timing, price and packaging.

## Later test decision

**Retain a dedicated shared-motion selector experiment**, contingent on a
credible <$0.54 delivered selector/driver route. Four rows offer more cost room;
five offer more time. This is a newly quantified research window, not grounds
to build a 320/400-channel head. Direct full-stroke arrays have timing regions
but fail even optimistic cost in those regions.

The smallest later prototype is a **2×4 full-pitch array** of individually held
columns, eight dynamically controlled selectors, one common four-increment
40 mm stroke and shared down-reset. First test all 256 binary masks and then
mixed five-level maps, measuring loaded selection ≤20 ms, no neighbor release,
reset reliability and selector/driver price. A manually swapped mask can test
passive mechanics only; it cannot pass dynamic programming. This experiment
belongs after the present process coupons and is not silently implemented as
an improved Test08. It can also test backlog R02/R03/R09 building blocks.
