---
status: complete
builds-on: [E-255, E-258, E-259]
---

# Threaded-column batch manufacture and service

**Prefer individually replaceable pairs in an openable shared guide/thrust bed;
do not commit to sealed, discard-on-fault tiles.** This changes the manufacturing
and service hypothesis, not the screw's load path. A batch fixture can reduce test
occupancy, but cannot erase thousands of loading, thread-start and inspection duties.
No fabrication route, fixture, pair yield or four-day complete build is qualified.

Evidence: **conditional calculations and primary process guidance**, self-reviewed;
no new CAD, physical measurements, supplier quotation, print job or purchase.
Reproduce `python3 tools/curated-experiment-checks/E-260/manufacture.py`;
`--check` verifies the model. All labor, defect and detection inputs below are
explicit scenarios, **not X1C/PLA priors**. E-255's positive owner holding observation
remains valid but unquantified; the historical trial5 dependency mismatch remains.

## Concrete manufacturing and service route

Keep two separate batch-made pieces/site: hollow internally threaded column and
resident screw. Load indexed trays into a shared fixture; establish thread start,
check signed travel and drift under a known individual load, then install accepted
pairs into an openable guide/thrust bed. Preserve lot identity and reject or correct
a problematic process before consuming replacement stock. No selective hand filing,
matched-pair sorting or automated feeding performance is granted.

The screw seat supports the column continuously; the writer supplies only torque.
Square guides react rotation. The proposed bed must locate that seat independently
of the removable writer. During repair, temporarily support the affected column
before screw removal. A shared cover may open only if other seats stay captured;
otherwise that bed requires unloading before service. Service access is a design
obligation, not a demonstrated assembled mechanism. No extra per-cell cartridge,
keeper or brake is introduced by this screen.

| Repeated duty | 64×64 / 6.35 mm | 80×80 / 5.08 mm |
|---|---:|---:|
| Columns + screws | 8192 parts | 12800 parts |
| Thread pairs / thrust seats / antirotation / drive interfaces | 4096 each | 6400 each |
| Two initial placements, before thread starts/tests | 8192 | 12800 |
| Illustrative 8×8 service beds | 64 | 100 |
| Two travelling heads' motor/feedback/dock duties | 128 each | 160 each |

An 8×8 bed spans50.8/40.64 mm at coarse/reference pitch, excluding its edges.
These are service accounting units, not finite layouts. Larger molded pieces do
not eliminate their internal failure sites. Pitch reduction removes36% of resident
pairs, not36% of E-259's update latency. For40/50-mm stroke and a10-mm full nut
engagement, threaded length must exceed50/60 mm once end/runout margins are added.
Deeper terrain therefore needs longer stock, guides and travel qualification.

## Maker-time and parallel inspection bounds

Illustrative maker allowance:16/32 hours represents two/four eight-hour days,
**not a new product gate**. Assume8 hours setup,2 minutes closing/checking each
64-site bed, and2 minutes replacing each first-pass defective pair. Assume mean
pair defect0.95% for this sensitivity calculation, replacements already qualified.
Fixture development, printing/cleanup, electronics, head assembly, whole-board
calibration and repeated replacement failures remain additional.

Manual touch scenario per pair: two5-s loads +2-s thread start +2-s inspection
+3-s installation =17 s. Tray/fixture-assisted hypothesis: two2-s loads +1-s
start +1-s inspection +2-s installation =8 s. These are task allocations to verify,
not measured rates or proof that a jig halves labor. Rejected pieces are replaced,
not tuned until they fit. The model excludes unseen defects from the labor success
claim; imperfect screening is considered separately below.

| Subtotal or breakpoint | 4096 pairs | 6400 pairs |
|---|---:|---:|
| 17-s touch scenario, maker hours | 30.77 | 43.58 |
| 8-s touch hypothesis, maker hours | 20.53 | 27.58 |
| Maximum touch seconds for16 /32 hours | 4.02 /18.08 | 1.48 /10.49 |
| One extra minute fitting every pair, added hours | 68.27 | 106.67 |
| Expected first-pass replacements in assumed case | 38.91 | 60.80 |

A **production screen scenario**, not endurance qualification: start at bottom,
move to top, return bottom, move to neutral, disconnect torque and observe a30-s
hold. At assumed300 rpm/3-mm lead and12-s batch overhead, fixture cycle is
`12 +30 +(2*stroke+neutral)/(3*300/60)` seconds. Acceleration, engagement delays
and longer required hold are absent; add them when measured. Each site needs a
known load and observable travel/hold; total tray force cannot prove every site.

For40-mm stroke/neutral20, one serial site occupies55.37/86.52 hours; a16-site
parallel fixture occupies3.46/5.41 hours. For50/neutral30:57.65/90.07 versus
**3.60/5.63 hours**. This grants16 driven, independently observable sites and
individual loading; tooling and automation cost are unpaid. Parallel hold alone
cannot accelerate a serial drive test by16. With no overlap, adding the deeper
fixture occupancy to8-s-touch maker time gives24.14/33.21 hours, still before
excluded work. Overlapping unattended testing is unqualified. Printing calendar
time remains separate from hands-on time; no new extrusion-time estimate is made.

## Correlation and why service access matters

Toy two-class model:90% of lots have independent conditional pair-defect probability
p=.005,10% p=.05; average.0095. Cells share their lot class, so they are correlated
unconditionally. These numbers deliberately illustrate sensitivity, not a fitted
process distribution. A perfect all-site test accepts an m-cell sealed module with
`q = .9*(1-.005)^m + .1*(1-.05)^m`.

| Cells per sealed module | Clean module probability | Attempts if each retry gets a fresh independent lot class | Attempts if retry class persists |
|---|---:|---:|---:|
|16|.87465|1.143|1.202|
|64|.65676|1.523|3.905|
|256|.24943|4.009|50441.15|

Fresh-class attempts are1/q; persistent-class attempts are
`sum(weight/(1-p)^m)`. The large last number is a **stop-and-diagnose witness**,
not predicted production: real operators should stop, salvage sound pairs and
correct the lot, not manufacture50,000 replacements. Independent random parts
at the same mean give64-site clean probability.54286, lower than the mixture.
Correlation can concentrate failures and *increase* the all-good fraction while
making persistent bad-lot rework much worse. A single iid yield scalar hides both.

With individually replaceable, perfectly screened parts drawn from refreshed lots,
expected supply factor is1/(1-.0095)=**1.00959** rather than1.523 for sealed64-site
modules. This comparison grants defect localization, accessible removal and
qualified spare supply; guide-bed faults, misalignment or damage during repair can
defeat it. A tray may be a batch unit without being a disposable service unit.

Inspection is not automatically perfect. At95% independent detection sensitivity
and perfect specificity, accepted64-site modules are only98.31% clean in this toy
model. Individual removal of detected faults still leaves expected hidden defects
**1.95/3.04 per initial board**, even granting perfect replacement parts. Repeating
the same blind test need not help. For illustration only, a union-bound guarantee
of≥95% probability of zero residual defects would require sensitivity≥99.8715% /
99.9178% at this mean; this is not a project reliability target or a measured tester.
Eight flawless sampled pairs still miss a5%-defect lot66.34% of the time;59 samples
reduce that conditional miss to4.85%, assuming random conditional independence.
Neither calculation qualifies drift, endurance or source-loss behavior.

## Process alternatives and cash breakpoints

Primary process sources checked2026-10-13; transfer to this geometry is unproven:

| Route | What it changes / decision-relevant limits |
|---|---|
| X1C FDM trays | Reuse available process and separate simple parts. Preserve orientation/lot identity; broad fit window and removal without hand cleanup remain to measure. Historical4.4-mm column is not automatically resized to fill6.35-mm terrain pitch. |
| Split tool or silicone casting | Many cavities can share pouring/curing, but core removal, degating and release still repeat. Formlabs' [molding guide](https://formlabs-media.formlabs.com/rs/060-UIG-504/images/WP-EN-Silicone-Molding-For-Product-Design.pdf), pp9–12, demonstrates master/tray replication and warns that surface detail transfers and repeated flexing affects mold life. Its wax/tile examples do not establish threaded engineering-polymer fit, wear or creep. No hot-metal-in-printed-mold assumption. |
| Injection molding | Covestro's [Joining Techniques](https://www.covestro.com/-/media/covestro/solution-center/brands/downloads/imported/1556890495.pdf?hash=789FC84A89B23E35811682A1C83B75A8&rev=b9342b910e604957994648aca3d4c88c), p6, identifies collapsible/unscrewing internal cores and split/unscrewing external tools as extra mold cost. Its joining guidance does not qualify a continuously driven lead screw. Multi-cavity ejection/unscrewing must be priced, not assumed free. |
| Machining/outsourced precision | [Protolabs](https://www.protolabs.com/resources/design-tips/mastering-complex-features-on-machined-parts/) documents thread/tool-access limits and alternative custom service. Its standard thread range does not establish our OD3.2/lead3 custom profile. A machined master or few shared spindle plates concentrates cost; thousands of custom screws need a real quote and compatible nut/seat evidence. |

An unscrewing core through10 mm at3-mm lead needs3⅓ turns. Sequential1-rev/s
release alone takes3.79/5.93 hours, before core reinsertion/handling. Parallel core
unscrewing can reduce this but adds tooling. Cast/molded material changes require
fresh friction/holding/creep checks; cheaper parts cannot inherit PLA behavior.

Use E-259's dated quoted motor/driver subset$4.24/output and unquoted$360 common
plus two-head reserve; **remove** its$.02/site allowance before computing the
maximum residual/site. This leaves, at purchased totals$500/$1000/$1500:

| Grid | $500 | $1000 | $1500 |
|---|---:|---:|---:|
|64×64|−$.09832|$.02375|$.14582|
|80×80|−$.08413|−$.00600|$.072125|

These are ceilings for **all remaining purchased resident work plus missing
feedback/transmission/docking, fixture/tooling and reserve corrections**, not a
screw price quotation. A$200 tool consumes$.04883/$.03125 per site before a part is
made. Every added$.05/site costs$204.80/$320.00. Material, outsourced processing,
scrap and paid labor belong in all-in economics; printed material is outside the
original purchased-hardware benchmark but never free. No retail-price or minimum
market-cost claim follows. The$1000 finished-value possibility remains an owner
preference, not proof this catalog route fits it or authorization to buy tooling.

## Disposition and checks

Carry forward **openable shared beds, accessible individual pairs and batch
screening** as the manufacturing hypothesis. Reject sealed whole-module disposal
as the default; no fine latch/fit redesign or mold is selected. The economic reason
for coarser pitch now includes maker-time and replacement burden, alongside E-258's
play geometry. It still needs playable walls, gaps and miniature support.

E-259's conditional64-grid/K32 deep-scene25.38-s maximum,32.58-s paid neutral setup
and45.78-s dense50 stress remain unchanged; the30-s gameplay reference has not been
relaxed or physically passed. Resident seat/guide failures still threaten support;
software inspection cannot supply it. The next discriminator remains the existing
pair's hold/drive/travel data. In any future justified batch calibration, also time
loading/thread start/removal, record lot identity and demonstrate individual repair
without unloading neighbors. Do not block independent research on optional printing.

Verification:32 exhaustive mixture/screen comparisons (up to8 cells), perfect/no
inspection and zero-defect limits, Jensen inequalities for both retry models,
serial/parallel occupancy anchors, touch-time differences and cash reconciliation.
No simulated yield is a production prediction; no manufacturing capability or
physical support is validated by these checks.
