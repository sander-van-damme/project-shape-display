# 09-lowcost-alternative/divergent — DND-75 divergent ultra-low-cost machines

**Status: three divergent machines clear both gates.** This subdirectory holds
the InventorAlpha response to [DND-75](/DND/issues/DND-75) (child of
[DND-71](/DND/issues/DND-71)), which asked for **2–3 materially different**
ultra-low-cost shape-display architectures — **not** a trim of the CTO's S6-LC.

> The CTO's S6-LC machine definition lives one level up in
> [`09-lowcost-alternative/`](../README.md). `08-current-design/` is untouched.

## The insight: the base is the binding term, so delete base lines

[DND-72](../README.md) (the S6-LC negative result) proved the S5-R/S6-LC
architecture cannot reach <$250 because its **fixed no-channel purchased base is
$218.70 parts → $253.69 delivered with zero actuators**. Its falsifier: the
verdict flips only if the *base itself* falls below **$215.52 parts**.

S6-LC trimmed the **actuator block**; that lever is exhausted because the base
is the floor. DND-75 attacks the **base's own expensive lines** — the ones that
exist *only* because S5-R has a travelling head, a zoned multi-screw lift and a
separate scanner axis:

| S5-R / S6-LC base line | Parts | Why it exists in S5-R |
|---|---:|---|
| Guide rods/rails and bearings | $25.00 | head actuator + scanner carriage |
| Four lift screws and nuts | $20.00 | zoned lift of the platen |
| Lift motor + coupling | $26.00 | platen stroke |
| Scanner motor | $12.00 | head indexing across rows |
| Belts pulleys idlers | $12.00 | lift sync + scanner |
| Head shafts and friction-pad material | $12.00 | head actuator + scanner |
| Axis drivers (3) | $9.00 | lift + scanner + writer axis |
| Axis reference sensors | $4.00 | axis homing |
| Wire connectors flexible loom | $22.00 | moving head + many channels |
| Power supplies and protection | $35.00 | all of the above |
| **Total attacked** | **$177.00** | of the $218.70 base |

Deleting this block leaves a **retained base of $41.70** (controller $5, driver
PCB/passives $25, shift registers $3.70, fasteners $8). A machine that needs
none of it starts ~6× below S6-LC's floor — *and must still move the same 6,400
columns 40 mm in under 30 s*.

**Hostile audit.** A deleted line with no substitute is an accounting trick. The
`ATTACK_AUDIT` table lists, for every attacked line, what removes it and what
replaces it, and every candidate pays for its own power supply, cables and any
retained axis (`SUBSTITUTE_LINES`: A1 +$11, A2 +$11, A3 +$12). All three still
land under $250.

## The three candidates

| | A1 — single-shaft cam | A2 — hand-crank + tape | A3 — S1-B banked broadcast |
|---|---|---|---|
| Bought motion actuators | 1 stepper | 0 (hand/spring) | 1 lift + 1 film-index |
| Selection | cam-actuated writer comb | punched-tape read comb | punched-film threshold planes |
| Parts (sourced-class) | $58.30 | $42.90 | $98.29 |
| **Delivered (×1.16)** | **$67.63** | **$49.76** | **$114.02** |
| + honest substitute lines | $80.39 | $62.52 | $127.94 |
| Full-map time | 17.76 s | 26.86 s | 22.06 s |
| <$250 | ✅ | ✅ | ✅ |
| <30 s | ✅ | ✅ | ✅ |
| Decisive failure mode | one motor must carry bank **and** lift | tape write is the product | punched-film registration |

**All three beat S6-LC's $253.69 base floor by 3–5× on delivered cost.**

- **A1 — single-shaft cam machine.** One stepper → printed camshaft (4 phased
  lift cams + bank cam + Geneva writer drum). No scanner motor, no lift
  motor/coupling, no lead screws, no belts, no guide rods, no head actuator, no
  writer solenoids. *Honest failure:* the lift cam alone needs **0.3302 Nm** vs
  the 0.30 Nm class allowance (the single-motor gate **fails by 0.0302 Nm**; the
  summed bank+lift case is 0.6099 Nm). A second $12 motor → **$80.39**, or a
  ~$16 stronger stepper → **$72.27**; both stay under $250. The cost claim
  survives; the single-motor claim does not.
- **A2 — hand-crank energy-reservoir + punched-tape reader.** Zero bought motion
  actuators. A torsion spring is charged by hand; an 80-channel mechanical tape
  reader selects; a printed escapement meters four 10 mm strokes. *Decisive
  failure:* the tape **writer** is the product — 25,600 holes at one needle
  ≈ 85 min off-line (~11 min at 8 needles); works only for known-ahead maps.
- **A3 — S1-B banked broadcast ratchet + punched-film media.** S1 revived per
  test11's prescription, with the mask-writing failure retired by an off-line
  punch carriage instead of 40 solenoids. *Correction to test11:* it prescribed
  **8 banks of 10 rows**; that is **38.9 s and FAILS 30 s**. The bank sweep
  shows **4 banks of 20 rows** clears both gates (22.06 s, 592 N release < 1500 N).
  *Decisive failure:* punched-film registration with no per-cell feedback.

## What is here

| File | Purpose |
|---|---|
| [`analysis/divergent_lowcost.py`](analysis/divergent_lowcost.py) | The screen: baseline decomposition, attack audit, three complete machines (ten-job allocation, BOM, timing, failure mode, killing test), summaries. Imports the promoted S5-R model so it cannot drift. |
| [`analysis/divergent_lowcost_checks.py`](analysis/divergent_lowcost_checks.py) | 18 CI-style assertions pinning every headline. |
| [`scad/a1_cam_cell.scad`](scad/a1_cam_cell.scad) | A1 unit cell + camshaft station at true 5.08 mm pitch. Printability **PASS**. |
| [`scad/a2a3_media_cell.scad`](scad/a2a3_media_cell.scad) | A2/A3 punched-media cell. Printed features PASS; film thickness reported as an honest **MEDIA RISK**. |
| [`tools/run_divergent_checks.py`](tools/run_divergent_checks.py) | Runs screen + checks + both CAD printability gates. |

Run:

```bash
python 09-lowcost-alternative/divergent/tools/run_divergent_checks.py
```

## Evidence discipline ([DND-27](/DND/issues/DND-27))

**No print, no purchase, no measurement.** Every figure is CALCULATION over the
promoted S5-R model and sourced-class allowances, or CAD (analytic
printability). Prices are point-in-time. The A1 force failure and the A2/A3
media risks are reported as failures, not hidden.

### Next test / remaining uncertainty
- A1: confirm the real cam-torque margin at the actual cam profile (friction, not
  the full-rise moment arm), then decide 1 vs 2 motors.
- A2/A3: the punched-media cell is the first coupon worth printing — it retires
  the whole family's central unknown (does a punched hole reliably gate a cell?).
- No candidate has a full multi-row assembly interference check; only unit cells
  are modelled.

See [`07-evidence-and-decisions/dnd75-divergent-low-cost.md`](../../07-evidence-and-decisions/dnd75-divergent-low-cost.md).
