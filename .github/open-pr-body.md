# DND-52: Actuator-class / drive-topology pivot — resolve K7 analytically

Advances [DND-52](/DND/issues/DND-52). After [DND-49](/DND/issues/DND-49) refuted K7 on
sourced evidence (no matched 8 mm 18° bipolar PM stepper ≤ $1.86 delivered), this holds the
**S5 mechanism** and screens six head-actuator / drive-topology options against the $500
delivered ceiling and the 30 s full-map cap.

**Evidence class: CALCULATION over sourced listings and stated assumptions. No purchase,
print or physical measurement** ([DND-27](/DND/issues/DND-27)).

## What changed

- `06-experiments/test12_winner_convergence/nx52_head_actuator.py` — the screen. Imports the
  committed `timing_closure.py`, `cost_closure.py`, `k7_motor_trace.py` so nothing drifts;
  charges each option from a no-channel base ($218.70) so a channel swap cannot double-count the
  driver block ($63.64).
- `nx52_head_actuator_checks.py` — 12 regression + honesty gates.
- `07-evidence-and-decisions/dnd52-head-actuator-pivot.md` — the ADR / recommendation.
- `08-current-design/README.md` — K7 rows in §7/§9 and the top banner updated.
- `05-research-questions/README.md` — Q3 follow-up result.
- `.github/workflows/ci.yml` — runs the new module + checks.

## Result

| Option | Actuators | Delivered | <$500 | Full map | <30 s | Verdict |
|---|---:|---:|:--:|---:|:--:|---|
| S5 incumbent | 80 | $1,366.87 | no | 26.25 s | yes | refuted ([DND-49](/DND/issues/DND-49)) |
| **Shared rotary register (S5-R)** | 10 | **$304.73** | **yes** | 24.65 s | **yes** | **cost+time feasible, mechanism unproven** |
| Wider head R=4 | 20 | $531.99 | no | 11.83 s | yes | refuted on the order-tier motor price |
| Micro-servo head | 80 | $485.69 | yes | 30.17 s | no | rejected on pitch (12–23 mm body) |
| Printed pancake stepper | 80 | $383.19 | yes | 26.25 s | yes | torque-unproven (needs magnetic FEA) |
| Global lift + printed memory | 3 | $295.45 | yes | 56 s | no | killed earlier (S1 force / S2 mask write) |

**Two numeric results decide the direction:**

1. **The wider-head lever is refuted on cost, not just pitch.** R=4 clears only for a
   per-station matched motor ≤ **$9.82**, between the two real tiers ($11.20 @100 / $8.20
   @3,001+). At the order tier actually buyable (20–40 pcs) it is **$531.99, over** —
   compounding the 30 s failure already recorded in [DND-49](/DND/issues/DND-49).
2. **One serious survivor — S5-R**, a shared-drive one-time programmable rotary register:
   2 index motors + 8 off-pitch writer solenoids → **$304.73 delivered (ideal <$400 band)**,
   **24.65 s**, pitch unchanged. It removes the entire 80-bought-motor cliff — but its decisive
   quantity is mechanical (selective dropout/re-engage of an 80-rotor bank at 5.08 mm pitch),
   which the repo's CAD does not represent and [DND-27](/DND/issues/DND-27) forbids couponing.

## Disposition

Mission target **NOT DEMONSTRATED** as reachable and **not** a proven dead end: a cost+time
viable pivot exists. Recommendation: adopt **S5-R** as the next machine-definition target
(backed by an *analytic/CAD* dropout-latch model, not a print); keep S5 only as a nominal
fallback; retire the wider-head lever; park the printed-pancake class pending an FEA.
No board contact ([DND-32](/DND/issues/DND-32)); no print-metric acceptance ([DND-27](/DND/issues/DND-27)).
