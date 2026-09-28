# Falsifier adversarial review — S5 promotion to winner (ADR-002 / Test12)

- **Status:** Independent adversarial review ([Falsifier](/DND/agents/falsifier)). Hostile review, not consensus.
- **Date:** 2026-09-28.
- **Issue:** [DND-36](/DND/issues/DND-36) — falsify the [DND-35](/DND/issues/DND-35) promotion of S5.
- **Targets:** `convergence-decision-2026-09-b.md` (ADR-002), `08-current-design/README.md` (on the
  `dnd-35-convergence-winner` branch), and `06-experiments/test12_winner_convergence/`
  (`model.py`, `checks.py`, `README.md`).
- **Evidence discipline:** every claim below is **calculation** on repository inputs, a
  **sourced-fact** reading of the repository's own documents, or a **CAD/OpenSCAD** observation.
  **Nothing here is a print or a measurement** ([DND-27](/DND/issues/DND-27)). No board contact.

## 0. Verdict (short)

**S5 promotion SURVIVES AS A DIRECTION but FAILS AS STATED.**

- S5 is genuinely the **best-evidenced** candidate and the only one with CAD + a reproducible timing
  model + a majority-sourced BOM. Promoting it over S1–S4 is defensible.
- But **three of the six "closed-analytically" killers are not closed** as stated (K1 contested, K4's
  own source returns `INCONCLUSIVE`, K6 is a best-corner of a sweep that mostly fails), and the **cost
  stack-up has arithmetic and double-counting defects** that move the headline by $2–20 and erase the
  claimed margin. The winner is **on or over the $500 ceiling**, not "clearing with margin".
- The promotion's **honesty statement is accurate** (ADR-002 §5): residual risks are named. The defect
  is that the **headline killer list presents contestable / measurement-only risks as
  `closed-analytically`**, which overstates readiness for a printable board test.

Recommendation: **keep S5 as the single winner, but re-label K1/K4/K6 and re-state the cost as a
corrected range** before `08-current-design` is treated as print-ready.

---

## 1. Finding A (material, arithmetic) — cost stack-up is internally inconsistent; the $500 margin is an artifact

### A.1 Two different "delivered" uplifts are used

- `delivered_3scenario/delivered_cost_model.py:86` defines delivered **additively**:
  `sub + sub*0.10 + sub*0.06 = sub*1.16`.
- `test12_winner_convergence/model.py:73` sets `DELIVERED_UPLIFT = 1.10 * 1.06 = 1.166`
  (**multiplicative**), applied to a `FIXED_SUBTOTAL_USD` taken from the **additive** expected scenario.

### A.2 The published tables do not reproduce

ADR-002 §3.2 and `08-current-design/README.md` §5 both print:

| Claimed row | Parts | Delivered |
|---|---:|---:|
| As-listed sourced pair | **$434.20** | **$503.71** |
| − registers onto PCB | **$420.20** | **$487.46** |
| − RP2040 | **$415.20** | **$481.56** |

Recomputed from the same inputs (`FIXED_SUBTOTAL_USD=284.00`, 80×$1.05 motor, 80×$0.80 driver):

- correct parts subtotal = `284 + 84 + 64 =` **$432.00**, not $434.20 (unexplained **+$2.20**);
- `$434.20 × 1.16 = $503.67`, not $503.71;
- the model's $503.71 is only reached with the **1.166** multiplicative uplift: `432.00 × 1.166 = $503.712`.
- the repository's **own** `delivered_3scenario/README.md` prints this exact cell as **$501.12**
  (`432.00 × 1.16`). **The DND-35 model disagrees with the repo's own grid** by $2.59 for the same
  two prices.

### A.3 The claimed clearing of $500 rests entirely on a partly double-counted reduction

On the repository's consistent additive basis:

- sourced pair delivered = **$501.12 — over the ceiling by $1.12**;
- reduced path = `(284−14−5 + 84 + 64) × 1.16 = 413.00 × 1.16 =` **$479.08**.

The reduction is at least partly double-counted:

- folding 40 × 74HC595 onto the driver PCB removes the `$0.35` **expected allowance** line
  (40 × $0.35 = $14), but the chips are still bought. Sourced LCSC 74HC595D is **$0.0925**;
  40 × $0.0925 = **$3.70**. The "custom driver PCBs and passives" line is a **fixed $25.00
  allowance** that does not change to add 40 on-board packages, board area and reflow. Realistic net
  register saving ≈ **$10.30, not $14**.
- the controller saving takes the **$5 Pico** price against the fixed subtotal's **$10 expected**
  line — a scenario mix, only defensible if that line is genuinely Pico-class.

**Consequence.** Honest headline: **S5 sourced-pair delivered ≈ $501–$504 (at/over the ceiling);
reduced ≈ $485 ± single digits — a real but small margin, not the advertised $18.44.**

### A.4 Cheapest falsification of A
Run `delivered_cost_model.py` and read its own sourced-pair cell (**$501.12**). Adopt the additive
basis project-wide and delete `1.10 * 1.06`.

---

## 2. Finding B (material) — K6 "time closed at 26.251 s" is a best-corner of a sweep that mostly fails

Test12 presents time as **PASS, 26.251 s, closed-analytically**. That value is one corner of the
repository's own 540-case `test09.../results/timing_sweep.csv`:

| Rate | under 30 s | total | max time |
|---:|---:|---:|---:|
| 200 pps | 0 | 108 | 52.67 s |
| 300 pps | 6 | 108 | 47.60 s |
| **400 pps** | **17** | **108** | **45.07 s** |
| 600 pps | 38 | 108 | 42.54 s |
| 800 pps | 54 | 108 | 41.27 s |

At the design rate of 400 pps, **84 % of the sweep fails the 30 s cap**; worst case **45.07 s**. The
26.251 s baseline uses `inspection_s=0`, `couple_each_s=0.025`, `settle_each_s=0.015`. Test09's own
README: *"only 0.749 s to the ≤27 s engineering target. No measured operating region exists.
**Inspection/recovery can consume that margin immediately.**"*

**Cheapest falsification of B.** Count `under_30` at 400 pps in `timing_sweep.csv` (17/108).
**Consequence if it stands:** K6 becomes `conditional — passes only in a ~16 % corner of the
assumed-parameter sweep; needs a measured ≥400 pps loaded rate`; withdraw the "3.749 s margin".

---

## 3. Finding C (material) — K4 "regional isolation closed" contradicts its own source, which returns INCONCLUSIVE

Test12 K4 says isolation is **closed-analytically, 0.017 mm vs 0.10 mm**. The cited source
`test11_falsification_library/analytic/README.md` states:

- *"`isolation_rig_runner.py` returns **INCONCLUSIVE** for each tile: every analytically boundable
  gate passes, but **J2-0 rig qualification is missing by design**."*
- its disposition table marks **rig noise floor, cumulative drift (100 cycles) and stiction release
  force as `measurement`** — not analytically derivable.

The 0.017 mm is a **rail-bending structural sub-bound**. The gate as a whole is **not closed**: the
failure-relevant terms (stiction release, wear drift) are measurement-only and were waived as
`INCONCLUSIVE`.

**Cheapest falsification of C.** Run `python isolation_rig_runner.py --input runs/isolation_analytic.csv`
— verdict is `INCONCLUSIVE`. **Consequence if it stands:** K4 becomes `partially-closed (structural
bound only); stiction release + drift are open measurement-class risks`.

---

## 4. Finding D (material) — the K1 reclassification is defensible in principle but contradicts Test08's own text

ADR-002 §3.1 reclassifies 5 N from a design gate to a *handling screen* because the product load is
**1 N service** and the model gives **4.96 N** (≈5×). That is **engineering-sound if 1 N/24 h is the
true product load**. But the source does not support calling the 5 N "not a gate":

- `test08/README.md:263`: *"The cam-beam model predicts only 4.96 N ideal critical load even after the
  core revision. Use a sacrificial coupon for the 5 N test; **expect that a support or material
  redesign may be necessary.** A passed miniature-weight demonstration must not override this failure
  gate."*
- `test08/README.md` lists the 5 N abuse load as a **measurement-protocol gate** with pass/fail.

**Attack.** The reclassification is only valid if 1 N is a *true* bound on tabletop load. The repo has
not sourced that: no miniature measured (R2, `miniature_measured: false`) and the real handling load
(a hand, a metal miniature, a book) is not established at 1 N. If the true worst case is 5 N, the
4.96 N cam **fails** by 0.8 % and Test08's anticipated redesign is required.

**Cheapest falsification of D.** Source the maximum tabletop vertical load, or run the existing
uniform-beam buckling check at 5 N. **Consequence if it stands:** K1 becomes `open — 4.96 N < 5 N;
service load must be sourced ≤4.5 N or the core re-sized`. This is the decisive re-label: it is the
difference between "no quantitative blocker" and "one quantitative blocker remains".

---

## 5. The other candidates (are S1/S2/S4 wrongly parked?)

- **Finding E (minor, agrees).** S1/S2/S4 "park" is **honest** and matches the earlier Falsifier
  audit: their nominal BOMs carry **$192–$224 of fallback purchase** for parts intended to print, so
  their cost verdicts are **undetermined**, not failed. ADR-002 does not wrongly kill them, but its §2
  table omits that qualifier. Non-blocking; add for symmetry.
- **Finding F (minor).** S3's kill is genuine and CI-visible (analytic printability FAIL; $2,880.98
  delivered). No objection.
- **Finding G (assumption, cross-cutting).** Reliability R1 is stated honestly (P(all 6,400 correct) =
  52.7 % at q = 1e-4; q ≤ 1.57e-6 needed for 99 %). This is the programme's largest unretired risk and
  is **unclosable under DND-27** (no per-cell feedback, no measured q). State it as such in ADR-002 —
  a product-level decision, not an engineering leftover.

---

## 6. Unstated killers the winner's list missed

1. **The cost cliff is a purchased-actuator cliff (80 motors + 80 drivers).** ADR-002 §2 claims
   "Per-cell bought parts: 0" — true — but the only traceable matched 8 mm PM stepper is **$40/ea**
   (MOONS 8PM020S1): 80 × $40 = **$3,200**, 8× the ceiling. The BOM uses an **untraced $1.05
   multipack**. This belongs in the **killer list** (K7), not only the risk register, and it is not
   "closed-analytically".
2. **No lateral-holding killer.** The hard stop resists **downward** load; a knocked miniature applies
   **lateral** load, resisted only by the detent (peak restoring torque ≈ **0.00139 mN·m**,
   `detent_torque.csv`) and the printed bushing. Test08's own measurement protocol includes a
   "Lateral handling 0.1 N / 1 N" gate; the winner's killer list is silent (K8).
3. **Angular margin vs print tolerance.** `levels.csv` gives 5 levels a nominal 12.50° margin, reduced
   to **6.50° after a 6° seating error**; the toe envelope is 23.50°. A ±0.05 mm print tolerance on a
   1.5 mm-radius rotor is several degrees of angular error and is not propagated in Test12. This
   sharpens K2 and interacts with K1 (a mis-seated toe can load the thin core).
4. **Regional-update time is untested end to end.** Test12 says regional = "rewrite only affected
   rows", but the head must still **home and reference** (0.5 s axis reference + 0.4 s ready settle
   per activation) and the platen must make a **full 41 mm stroke** (regionally! the whole platen
   moves) for any write. Regional time is not bounded in Test12; `reliability.regional_update_seconds`
   is explicitly "perfect-scaling benefit of the doubt".
5. **Cycle life of printed detent/ratchet.** No K-number at all. `detent_torque` is a single-cycle
   static model; creep/fatigue of a printed 0.45 mm leaf over thousands of writes is unmodelled.
   Cross-cutting with K2.

---

## 7. Ranked cheapest falsification experiments (all analytic, no print)

| # | Experiment | Kills / closes | Cost |
|---|---|---|---|
| 1 | Source the max tabletop vertical + lateral load (one product statement) | K1, K8 | sourced fact |
| 2 | Re-run `delivered_cost_model.py`; adopt additive uplift; net register saving $10.30 | K5 | minutes |
| 3 | Count `under_30` in `timing_sweep.csv` at 400 pps; propagate inspection | K6 | minutes |
| 4 | Run `isolation_rig_runner.py --input analytic`; read `INCONCLUSIVE` | K4 | minutes |
| 5 | Monte-Carlo angular error from ±0.05 mm print tolerance on the rotor | new K3 | hours |
| 6 | Buckling check at 5 N with the 1.0 mm core | K1 | minutes |

## 8. What would change my verdict

- A **sourced ≤4.5 N tabletop-load bound** → K1 genuinely closes and Finding D falls.
- A **measured ≥400 pps loaded rate** (or a timing model at inspection>0 still <30 s) → K6 closes.
- A **matched sub-$1.05 motor quote** → the cost cliff (K7) genuinely closes.
Any of these would move the verdict from **"fails as stated"** back to **"passes as stated"**. None
requires a print, so all can be closed inside current policy.
