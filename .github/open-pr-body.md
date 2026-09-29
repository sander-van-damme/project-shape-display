# DND-104 child: reliability-first envelope (DND-109) + reliability-first machines (DND-107)

Child PR of [DND-104](/DND/issues/DND-104) (reliability-first low-cost shape display).
Two agent deliverables share this branch:

- **DND-109** (CostManufacturing): the sourced-class cost + FDM-printability **envelope** for the
  mechanism classes the program is choosing among.
- **DND-107** (InventorBeta): **three materially different reliability-first whole machines**
  (2 non-mask + 1 mask) screened against the DND-103 reliability gate.

## Engineering question

After [DND-103](/DND/issues/DND-103) made reliability and buildability first-class gates: which
complete machine minimizes **what must work correctly 6,400 times**, at <$250 purchased and
<30 s full-map — and what does its bought hardware cost and print?

## DND-107 — reliability-first machines (this change)

Three complete machines, none a trim of S6-LC and none like each other. Each answers the ten
functional jobs, has a sourced-class BOM, an honest 7-stage timing decomposition, the DND-103
per-architecture reliability audit, and the cheapest no-print test that can kill it.

| | **B1** shared-shaft screw memory | **B2** pressure blanket + hold | **B3** rotary drum mask |
|---|---|---|---|
| Mask? | **No** | **No** | Yes |
| Repeat count of the decision element | 6,400 passive threads | 6,400 binary toggles | **80** row tracks |
| Compliant per-cell elements | **0** | 6,400 (binary flip only) | 6,400 (hard-stop pawl) |
| Delivered | $79.33 | **$72.85** | $86.29 |
| Visible transition | **170.9 s (FAIL)** | **14.26 s (PASS)** | **22.46 s (PASS)** |
| Verdict | **FAIL_AS_DRAWN** | **PASS** | **PASS** |

- **B1 is a reported failure**, not hidden: `gang_sweep` and `lead_sweep` show the timing-feasible
  and torque-feasible sets are **disjoint**, so a shared-shaft binary screw memory cannot meet 30 s
  on a low-cost stepper class. A real negative result.
- **B2** lifts all 6,400 columns with one common bladder (force margin **+3,520 N**) and holds with a
  positive 2-state toggle on hard stops. Limit: regional update needs a zoned bladder; terrain is
  binary 0/40 mm.
- **B3** writes one drum track per **row** (80 tracks) instead of 6,400 keepers — an **80× reduction**
  in repeated decisions — and a bad track fails a whole row **visibly**. Limit: drum write is the
  product (45 s off-line, double-buffered).

New files: `09-low-cost-variant/divergent/analysis/reliability_machines_beta.py` (+ checks),
`reliability_machines_beta.md`, `scad/b2b3_reliability_cell.scad`,
`tools/run_reliability_machines_checks.py`, plus a `check_reliability_cell` checker in
`tools/validate/analytic_printability.py`.

## DND-109 — cost + printability envelope (also in this branch)

Adds the sourced-class cost/printability envelope, 44 bought lines with scenario bands, media
classification, `PROVISIONAL vs sourced` printability rules, and the per-cell sensitivity result
(**zero per-cell bought hardware is mandatory**): `09-low-cost-variant/reliability_sourcing/`.

## Evidence produced

- **CALCULATION + CAD only.** No part printed, purchased or measured
  ([DND-27](/DND/issues/DND-27)).
- Imported S5-R/S6-LC model so the baseline and cost convention cannot drift
  ($263.05 delivered, 11.96 s; ×1.16 uplift).
- **DND-107 gate:** 28/28 checks PASS; CAD printability of the B2/B3 repeated features **PASS**.
- **DND-109 gate:** `cost_envelope_checks.py` all PASS.

## What passed / failed

- **Passed:** DND-107 checks (28/28); B2 and B3 clear cost + 30 s; B3 80× decision reduction;
  B2 blanket margin; CAD printability. DND-109 envelope gate.
- **Failed:** B1 as drawn (timing/torque disjoint) — recorded as a negative result. Regional reveal
  is a stated limitation of B2; drum-write latency a stated limitation of B3.

## What remains uncertain

- B2 toggle hinge **fatigue life**; B3 drum-track **registration tolerance** — both measurement-only.
- All force/torque/pressure/timing figures are assumption-class over a sourced model.
- No full multi-row assembly interference check; only unit cells/witnesses.

## Reproduce

```bash
python 09-low-cost-variant/divergent/tools/run_reliability_machines_checks.py
python 09-low-cost-variant/reliability_sourcing/cost_envelope_checks.py
```

Closes [DND-109](/DND/issues/DND-109) and [DND-107](/DND/issues/DND-107).
