# ADR-001 — Convergence decision after the first invention + falsification generation

- **Status:** Accepted (CTO), for board awareness.
- **Date:** 2026-09-28.
- **Owner:** CTO.
- **Scope:** Shape Display Lab, `sander-van-damme/project-shape-display`.
- **Supersedes:** the "five co-equal survivors" posture in
  [`04-architecture-candidates/`](../04-architecture-candidates/README.md). The candidate list is
  preserved as the search record, not as a commitment.

## 1. Decision

**No architecture is promoted to [`08-current-design/`](../08-current-design/README.md).**

The surviving field S1–S5 is **one bet in five shapes**, not five independent architectures:

> a passive, printable, final-pitch state/selection element can be (a) written by a small shared
> programmer and (b) hold terrain load without powered holding.

Every survivor is unsupported or rejected on at least one binding conjunct (pitch/printability,
release force, regional isolation, reliability, or matched delivered cost). **Nothing in the field
has printed or measured evidence.** Promotion was previously gated on repo write access; that gate
is now closed (§4), so the programme's critical path is physical, not administrative.

## 2. Factors considered

| Factor | Finding | Evidence level |
|---|---|---|
| Per-cell bought actuation | 6,400 selectors even at $0.50 = $3,200 → dead | calculated (Test10) |
| Cell-serial visible writing | needs >213 completed cells/s; modelled writer ≈76 min → dead | calculated (Test10) |
| S1 pull-density | gate+pawl fit in 2.28 mm beside a 2.0 mm shaft at 5.08 mm → **not** the killer | calculated (Test11, InventorAlpha) |
| S1 worst-case stroke force | all-high map arms 6,400 pawls → ≈2.37 kN at 0.37 N/cell; break-even 0.234 N/cell → **fails** | calculated |
| S1/S2 mask writing | 12,800 ops: serial 2,560 s, 80-channel 56 s → needs ≥500 channels or off-line pre-write | calculated |
| S2 read timing | ≈2.0 s full / ≈1.8 s per tile → passes 30 s cap | calculated |
| Print-force variation | safe release window collapses at ≈9% force sd; no per-cell calibration | calculated |
| Regional isolation | S1/S2/S4 all *assume* it; no disturbance limit exists; unmeasured | assumption |
| Reliability | at 0.01% per-cell error P(all 6,400 correct) ≈ 52.7%; 6-cell coupon is not evidence | calculated (Test11 reliability.py) |
| Return margin | solid column: 20.29 mN weight vs 5 mN drag = 4.06×, only 15.29 mN headroom; hollow is <2× | calculated |
| Cost | best-defended BOMs $432–$518 with contingency; no *matched delivered* BOM <$500 | calculated (DND-6/DND-11) |

## 3. Consequences

- **S1** is downgraded: survives only as **S1-B banked broadcast** (8 banks × 10 rows → ≈296 N/stroke,
  ≈17.6 s, <30 s) and only with pre-written media — i.e. S1 collapses into S2 unless disposable
  media are accepted.
- **S2** survives as a **system** (double-buffered, off-line writer), conditional on two unproven
  product properties: **surprise maps** (writer is the bottleneck if the next map is not known
  ~1 min ahead) and **exchange disturbance** (frame stiffness assumed 100 N/mm; must be measured).
- **S3/S4** remain candidates but are unbuilt; their gates are fan-out dwell (S3) and loaded clutch
  independence + jam containment (S4).
- **S5** is the most specified (Test08/Test09) but the 5 N cam-buckling abuse gate is **not passed**
  even in the ideal model (≈4.96 N).
- A requirements re-scope (pitch, level count, surprise-map support, or cost ceiling) is a **product
  decision for the CEO** if the §5 bet fails; it is not an engineering workaround.

## 4. Integration status (why the administrative gate is closed)

- SSH deploy-key **push** works; **PR creation works with no PAT** via the reusable
  `.github/workflows/open-pr.yml` (workflow-scoped `GITHUB_TOKEN`, `pull-requests: write`).
- Open PRs against `main`: #12 (cost/printability), #13 (S3/S4 selector), #14 (reusable opener),
  #15 (shared-drive invention), #16 (S1/S2 rejection screen + coupon), #17 (falsification library +
  J2 isolation rig).
- **Merge remains board-authorized.** Agents do not merge.

## 5. Binding next tests (ranked, cheapest first)

These are the plan's elimination order (see [`convergence-plan.md`](convergence-plan.md) §3):

1. **Step 0 — common isolation rig (Q5/J2):** two adjacent loaded full-pitch tiles, measure
   untouched-neighbour peak vertical/lateral motion and miniature movement. Supplies the shared
   disturbance baseline. Protocol written by the Falsifier; fixture is **PRINT-READY PENDING
   HARDWARE**; physical run owned by the CTO (DND-14).
2. **Step 1 — passive pitch/backlash capability coupon** at final pitch on the X1C/PLA: the cheapest
   global kill.
3. **Step 2 — printed one-bit passive memory cell:** holds ≥1 N, toggles with small force, no
   vibration release, thousands of cycles. Kills the central bet if it fails.
4. Then isolation 2×2 stack (step 3), selector/register (step 4), writer path (step 5), load/power
   (step 6).

## 6. What would change the decision

- Step 2 **passes** broadly → the field is real; race moves to timing/cost.
- Step 2 **fails** → escalate a requirements re-scope to the CEO **before** any further candidate
  invention (this is the single most important rule of the plan).
- Step 1 shows the X1C/PLA process cannot hold the geometry → escalate a fabrication-baseline
  change (e.g. resin/SLA memory layer) to the CEO; do not silently relax criteria.

## 7. Honesty statement

Every figure above is **sourced fact, stated assumption, or calculation**. No printed or measured
shape-display evidence exists. This ADR records a decision made on analytical evidence and names the
cheap physical tests that can overturn it.
