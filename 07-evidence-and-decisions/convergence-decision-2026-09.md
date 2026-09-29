# ADR-001 — Convergence decision after the first invention + falsification generation

- **Status:** Accepted (CTO), for board awareness.
- **Date:** 2026-09-28.
- **Owner:** CTO.
- **Scope:** Shape Display Lab, `sander-van-damme/project-shape-display`.
- **Supersedes:** the "five co-equal survivors" posture in
  [`04-architecture-candidates/`](../04-architecture-candidates/README.md). The candidate list is
  preserved as the search record, not as a commitment.

## 1. Decision

**No architecture is promoted to [`08-current-design/`](../08-integrated-designs/s5r-shared-drive-register/README.md).**

The surviving field S1–S5 is **one bet in five shapes**, not five independent architectures:

> a passive, printable, final-pitch state/selection element can be (a) written by a small shared
> programmer and (b) hold terrain load without powered holding.

Every survivor is unsupported or rejected on at least one binding conjunct (pitch/printability,
release force, regional isolation, reliability, or matched delivered cost). **Nothing in the field
has printed or measured evidence.** Promotion was previously gated on repo write access; that gate
is now closed and merge authority is delegated to agents (§4). Under board directive
[DND-27](/DND/issues/DND-27) the programme will **not** produce printed/measured evidence, so the
critical path is analytic/simulation/CAD plus a set of explicitly qualitative residual risks (§5),
not physical experimentation.

## 2. Factors considered

| Factor | Finding | Evidence level |
|---|---|---|
| Per-cell bought actuation | 6,400 selectors even at $0.50 = $3,200 → dead | calculated (Test10) |
| Cell-serial visible writing | needs >213 completed cells/s; modelled writer ≈76 min → dead | calculated (Test10) |
| S1 pull-density | gate+pawl fit in 2.28 mm beside a 2.0 mm shaft at 5.08 mm → **not** the killer | calculated (Test11, InventorAlpha) |
| S1 worst-case stroke force | all-high map arms 6,400 pawls → ≈2.37 kN at 0.37 N/cell; break-even 0.234 N/cell → **fails** | calculated |
| S1/S2 mask writing | 12,800 ops: serial 2,560 s, 80-channel 56 s → needs ≥500 channels or off-line pre-write | calculated |
| S2 read timing | ≈2.0 s full / ≈1.8 s per tile → passes 30 s cap | calculated |
| Print-force variation | safe release window collapses at ≈9% force sd; no per-cell calibration; **permanently qualitative** under DND-27 | calculated (risk) |
| Regional isolation | S1/S2/S4 all *assume* it; no disturbance limit exists; now bounded analytically only | assumption → simulation (§5.2 residual) |
| Reliability | at 0.01% per-cell error P(all 6,400 correct) ≈ 52.7%; 6-cell coupon is not evidence; **no coupon will be built** | calculated (Test11 reliability.py) |
| Return margin | solid column: 20.29 mN weight vs 5 mN drag = 4.06×, only 15.29 mN headroom; hollow is <2× | calculated |
| Cost | best-defended BOMs $432–$518 with contingency; no *matched delivered* BOM <$500 | calculated (DND-6/DND-11) |

## 3. Consequences

- **S1** is downgraded: survives only as **S1-B banked broadcast** (8 banks × 10 rows → ≈296 N/stroke,
  ≈17.6 s, <30 s) and only with pre-written media — i.e. S1 collapses into S2 unless disposable
  media are accepted.
- **S2** survives as a **system** (double-buffered, off-line writer), conditional on two unproven
  product properties: **surprise maps** (writer is the bottleneck if the next map is not known
  ~1 min ahead) and **exchange disturbance** (frame stiffness assumed 100 N/mm, now bounded by
  simulation only — a permanent qualitative risk under §5.2).
- **S3/S4** remain candidates but are unbuilt and will not be built; their gates are fan-out dwell
  (S3) and loaded clutch independence + jam containment (S4), both now analytic/simulation gates.
- **S5** is the most specified (Test08/Test09) but the 5 N cam-buckling abuse gate is **not passed**
  even in the ideal model (≈4.96 N); this is an analytic result and cannot be improved by testing.
- A requirements re-scope (pitch, level count, surprise-map support, or cost ceiling) is a **product
  decision for the CEO** if the §5 bet fails; it is not an engineering workaround.

## 4. Integration status (administrative gate closed; merge authority delegated)

- SSH deploy-key **push** works; **PR creation works with no PAT** via the reusable
  `.github/workflows/open-pr.yml` (workflow-scoped `GITHUB_TOKEN`, `pull-requests: write`).
- **Merge authority is delegated to agents**, superseding the earlier "merge remains
  board-authorized" rule. Board directive [DND-19](/DND/issues/DND-19) (2026-09-28) states that
  agents may merge repository PRs themselves once the change is reviewed and the checks/evidence
  support it. Agents do **not** need board approval to merge.
- **Merge status of the first-generation PRs (#12–#17), reconciled against `origin/main`
  (head `1a9926e`, 2026-09-28):** all are merged. PRs #12–#17 were integrated through the
  `integrate/test11-all` branch and are ancestors of `origin/main`; the cross-cutting DND-28
  analytic-gate re-scope was then applied directly on `main`. There are **no open PRs** against
  `main` as of this revision.

  | PR | Content | Status vs `origin/main` |
  |---|---|---|
  | #12 | cost/printability CI checks | merged |
  | #13 | S3/S4 selector fan-out | merged |
  | #14 | reusable credential-free PR opener | merged |
  | #15 | shared-drive invention | merged |
  | #16 | S1/S2 rejection screen + coupon | merged |
  | #17 | falsification library + J2 isolation rig | merged |

  Verification: the deliverable commits `8ea9c5f` (S1/S2 rejection screen) and `452206f`
  (J2 CAD render + socket gate) are each ancestors of `origin/main`.

## 5. Binding next tests (ranked, cheapest first)

**Program policy [DND-27](/DND/issues/DND-27) forbids physical print tests.** Physical
measurement is not an available evidence class. The gates below are therefore ranked as
**analytic / simulation / CAD-mesh** gates, preserving the same elimination order and the same
kill logic as the original plan, but each is now executable from a calculation, a mesh/kinematic
model, or a CAD render — none requires printing or measurement.

Each gate carries a **binding assumption** that cannot be retired analytically. Where a physical
coupon was the only way to close a risk, the risk becomes a **permanently qualitative risk** and is
flagged as such in §5.2.

### 5.1 Ranked analytic/simulation/CAD gates

1. **Step 0 — isolation disturbance bound (Q5/J2), analytic.** Replace the two-tile physical rig
   with a **beam/FEA-coupled kinematic model**: clamped/simply-supported rail-beam bound for
   target→neighbour coupling, plus a Coulomb-stiction bound for release. Deliverable:
   `06-experiments/test11_falsification_library/analytic/` run record + `check_fixture.py` mesh
   gate. Kills: no candidate directly — supplies the shared disturbance baseline against which the
   S2/S4 isolation claims are judged. Evidence level: **SIMULATION/CALCULATION**.
2. **Step 1 — passive pitch/backlash capability, CAD + sourced process limits.** Replace the
   printed coupon with a **CAD/mesh validation** of the final-pitch geometry against *sourced* FDM
   process limits (minimum wall, minimum slot, overhang, clearance) plus a **worst-case and Monte
   Carlo tolerance/interference stack-up**. Closes only if the geometry fits inside the sourced
   process envelope with positive margin. Kills: any survivor whose fit, web, gate or detent needs
   a feature outside the envelope. Evidence level: **CAD + CALCULATION**.
3. **Step 2 — passive memory cell capability, analytic stack-up + kinematic model.** Replace the
   printed one-bit cell with a **force/kinematics model**: hold force, toggle force, vibration
   release threshold and cycle-life bounds derived from geometry and material properties, with the
   tolerance stack-up on the detent/ratchet interface. Kills: **S5** (detent cannot correct a
   slipped step), **S1** (gate/ratchet cannot hold or repeat), **S4** (no local memory) — and the
   whole shared-power/passive-memory bet if the stack-up is negative. Evidence level:
   **CALCULATION/SIMULATION**, with the central hold/repeat behaviour a **permanently qualitative
   risk** (§5.2).
4. **Step 3 — isolation of a 2×2 tile arrangement, simulation with representative load.** Model
   regional reset of one tile while a neighbour carries a representative miniature mass; report
   coupling and jam propagation. Kills: **S2** (registration seizes the follower) and **S4**
   (coupling/jam propagates). Evidence level: **SIMULATION**.
5. **Step 4 — selector/register fan-out, analytic gate (DND-28).** One common stroke selectively
   engages 2×4 outputs at final pitch without neighbour release; use the existing
   `t11a_fit_check.py` engine on the analytic run record. Kills: **S1** (threshold gates), **S3**
   (fan-out register), **S4** (tile clutch). Evidence level: **CALCULATION**.
6. **Step 5 — writer path, modelled timing.** Complete receive→write→install→register→settle for
   one tile in a kinematic/timing model. Kills: **S2** for surprise reveals; bounds S1's mask
   install. Evidence level: **CALCULATION/SIMULATION**.
7. **Step 6 — load, structure and power, analytic + FEA.** Spliced full-span beam model + dummy
   platen at modelled column mass; lift torque-speed margin, flatness and power-cut behaviour.
   Kills: any survivor whose lift/structure cannot maintain the unload gap or hold position on
   power loss. Evidence level: **CALCULATION/SIMULATION**.

### 5.2 Gates that remain physically unverifiable (permanently qualitative risks)

Under DND-27 the following cannot be closed by any available evidence class. They stay on the risk
register as **qualitative**, not as pending physical tests:

| Risk | Why it cannot be closed analytically | Where it binds |
|---|---|---|
| Print realisation: fusion, stringing, layer adhesion, elephant-foot, warp | depends on actual toolpath/hardware, not geometry | Step 1 |
| Measured release-force spread across many identical passive elements (≈9 % sd break-even) | statistical property of real printed parts | Step 2, central bet |
| Detent/ratchet hold and repeat behaviour after a slipped step | contact/creep/fatigue of printed interfaces | Step 2 |
| Rig noise floor and cumulative regional creep | physical rig + time-dependent creep | Steps 0, 3 |
| Stiction release force under real surface finish | surface roughness of printed faces | Steps 0, 3 |
| Miniature-height compliance / real miniature loads | physical figures and operator handling | Steps 3, 6 |

These are the risks that a printed or measured coupon would have retired. They are recorded here
so no later reader mistakes an analytic pass for a physical one.

## 6. What would change the decision

- Step 2 analytic stack-up **passes** with positive margin → the field is real **on paper**; race
  moves to modelled timing/cost, subject to the §5.2 qualitative risks.
- Step 2 analytic stack-up **fails** → escalate a requirements re-scope to the CEO **before** any
  further candidate invention (this is the single most important rule of the plan).
- Step 1 CAD/mesh check shows the final-pitch geometry cannot fit the *sourced* FDM process
  envelope → escalate a fabrication-baseline change (e.g. resin/SLA memory layer) to the CEO; do
  not silently relax criteria. A process change can only be verified by sourced process limits, not
  by printing.
- **No physical test can be added as a decision gate** while DND-27 is in force. If a gate cannot
  be expressed analytically, it is parked as a qualitative risk (§5.2), not scheduled.

## 7. Honesty statement

Every figure above is **sourced fact, stated assumption, calculation, simulation, or CAD** — never
physical validation. **No printed or measured shape-display evidence exists, and under
[DND-27](/DND/issues/DND-27) none will be produced.** This ADR records a decision made on
analytical evidence and names the analytic/simulation/CAD gates that can overturn it, while
explicitly marking the assumptions that are now permanently qualitative (§5.2).
