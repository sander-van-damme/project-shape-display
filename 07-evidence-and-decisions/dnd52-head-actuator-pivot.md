# DND-52 — Actuator-class / drive-topology pivot: K7 resolved analytically

- **Verdict:** **NO OPTION IS A PROVEN BUILDABLE MACHINE TODAY, and the mission target is
  NOT DEMONSTRATED as reachable.** But the option space is now closed and the binding
  residual is sharpened: the S5 incumbent is *cost-closed only on an untraced marketplace
  motor* ([DND-49](/DND/issues/DND-49)), and exactly **one serious pivot survives the screen —
  a shared-drive one-time programmable rotary register** — at **$304.73 delivered (24.65 s)**,
  clearing both gates, while resting on a single unproven mechanism (selective dropout/re-engage
  of an 80-rotor bank at 5.08 mm pitch). A second numeric result is decisive for the obvious
  "just use a wider head" lever: an R=4 wider head clears the ceiling **only if its per-station
  matched motor is ≤ $9.82**, which sits *between* the two real matched price tiers ($11.20 @100 /
  $8.20 @3,001+). At the order tier actually available (20–40 pcs) the wider head is **$531.99,
  over**. The wider-head lever is therefore **also refuted on sourced price**, not just on the
  S3 pitch gate.
- **Owner:** CTO.
- **Issue:** [DND-52](/DND/issues/DND-52), for [DND-49](/DND/issues/DND-49) (which refuted K7 on
  sourced evidence) and the mission goal.
- **Inputs:** `06-experiments/test12_winner_convergence/{nx52_head_actuator.py,
  nx52_head_actuator_checks.py}`, importing the committed `timing_closure.py`,
  `cost_closure.py`, `k7_motor_trace.py` so nothing drifts.
- **Evidence class:** CALCULATION over sourced listings and stated assumptions. **No part was
  bought, printed or measured** ([DND-27](/DND/issues/DND-27)).

Run:

```text
cd 06-experiments/test12_winner_convergence
python nx52_head_actuator.py            # full screen, JSON
python nx52_head_actuator_checks.py     # 12 regression + honesty gates
```

## 1. The question and the method

[DND-49](/DND/issues/DND-49) refuted K7: the S5 machine-preserving cost path (DND-48 basis)
clears $500 only for a matched 8 mm 18° bipolar PM stepper at **≤ $1.86 delivered**, and the
cheapest *matched, orderable* part is **$11.20 @100** (CCHT) → **$1,366.87 delivered**. The only
sub-$1.86 basis is an untraced multipack with no published step angle, and [DND-27](/DND/issues/DND-27)
forbids the purchase sample that would retire it.

This ADR does the remaining agent-reachable move: hold the S5 architecture (projected stepped
rotary stops + one common platen lift) and ask whether a different **actuator class** or
**drive topology** removes the 80-channel bought-motor cliff. Six options are costed against the
same ceiling and the same 30 s cap, each with an explicit actuator count, bought-BOM delta,
full-map time, pitch feasibility and the one quantity that would decide it.

**Cost basis (imported, not re-declared).** The fixed non-motor base is the DND-48 E1–E6 base
with the motor line at $0 → **$282.34 parts**, of which **$63.64** is the 80-channel TB6612
driver block. Options are charged from a **no-channel base of $218.70** and declare their own
channel cost exactly once, so a channel swap cannot double-count the driver. Delivered = parts ×
1.16 (additive ship+tax uplift, the repo's own convention). `checks.py` asserts the identity
`218.70 + 63.64 = 282.34`.

## 2. The screen

| Option | Actuators | Parts Δ | Delivered | <$500? | Full map | <30 s? | Verdict |
|---|---:|---:|---:|:--:|---:|:--:|---|
| **S5 incumbent** (80×8 mm PM) | 80 | +$896 matched | **$1,366.87** | no | 26.25 s | yes | refuted ([DND-49](/DND/issues/DND-49)) |
| **1. Shared rotary register** | 10 | +$44 | **$304.73** | **yes** | 24.65 s | **yes** | **cost+time feasible, mechanism unproven** |
| **2. Wider head R=4** | 20 | +$239.91 | **$531.99** | no | 11.83 s | yes | refuted on the order-tier motor price |
| 2b. Wider head R=2 | 40 | +$479.82 | $810.28 | no | 16.87 s | yes | refuted (cost) |
| 3. Micro-servo head | 80 | +$200 | $485.69 | yes | 30.17 s | **no** | rejected on pitch (12–23 mm body) |
| 4. Printed pancake stepper | 80 coils | +$111.64 | $383.19 | yes | 26.25 s | yes | unproven torque class (needs magnetic FEA) |
| 5. Global lift + printed memory | 3 | +$36 | $295.45 | yes | **56 s** | **no** | killed earlier (S1 force / S2 mask write) |

The two clean cost+time survivors are **#1 (shared rotary register)** and **#4 (printed
pancake)**. #4 is not really a *drive-topology* change — it keeps 80 channels and merely
replaces the bought motor with a printed axial multipole rotor plus a bought coil; it is the
cheapest of all at $383.19, but it cannot be shown to make the 0.15 mN·m running torque at
5.08 mm without a magnetic FEA the repo does not have, and a printed-pole torque coupon is
forbidden under [DND-27](/DND/issues/DND-27).

## 3. The two numeric results that decide the direction

**Result A — the wider-head lever is refuted on sourced price, not just on the S3 pitch gate.**
An R=4 head needs 20 stations (20 motors + 20 dual H-bridges). Solving the ceiling for the
per-station motor price gives

```
max_station_motor = (500/1.16 − 218.70)/20 − 0.7955 = $9.82
```

The two *real* matched price tiers are **$11.20** (@100) and **$8.20** (@3,001+). A 20–40 piece
order sits at the **$11.20** tier, so R=4 is **$531.99 — over the ceiling**. It would clear only
at the 3,001+ tier, which is not buyable at this quantity. The earlier S3 "reduced-head" lever
([DND-49](/DND/issues/DND-49)) already failed the 30 s budget; this result shows it **also fails
cost on the order tier**. The wider-head avenue is closed.

**Result B — the shared rotary register is the only serious survivor.** 2 index motors + 8
off-pitch writer solenoids = **$44 parts**, **$304.73 delivered** — inside the *ideal* <$400
band, not merely under the $500 ceiling. Per-cell step writes are replaced by a shared bank roll
(assumed 300 rpm, 0.05 s Geneva engage/disengage per station, 20 stations), giving **24.65 s**.
Pitch is unchanged because the register lives in the head, above the 5.08 mm field; the columns
keep the S5 five-level rotors. This is exactly the project's stated preference: move cost from
80 bought motors to printed selection.

## 4. Why Result B is *not* a SUCCESS under the board's two-trigger policy

The register clears every analytic gate the repo can compute, but its decisive quantity is
**mechanical**: whether an 80-rotor bank can be rotated in lockstep and each rotor selectively
*dropped out of the drive path* at its selected hard stop, then reliably *re-engaged* on the
next pass, at 5.08 mm pitch and within the row dwell. None of that is represented in the repo's
CAD, and the failure mode (a missed re-engage = a silent one-level error on a whole row) is
unmodelled. Closing it requires a printed coupon, which [DND-27](/DND/issues/DND-27) forbids.

So Result B is a **named, cost-and-time-attractive architecture hypothesis**, not a proven
machine. It shifts the binding residual from *cost* (K7) to *one mechanical reliability
quantity* (the register dropout/re-engage), which is the same *class* of residual as K2 (detent
contact) and K4 (stiction release) — but on the machine's only active selection mechanism, so
it is a heavier residual, not a lighter one.

## 5. Recommendation

1. **Adopt the shared-drive rotary register as the single serious pivot ("S5-R")** and treat it
   as the next machine-definition target: it is the only option that clears both gates
   *and* removes the entire 80-bought-motor cliff, and it is the project's stated preference.
2. **Keep S5 as the fallback**, contingent on a matched ≤$1.86 motor — which [DND-49](/DND/issues/DND-49)
   has refuted on sourced evidence, so the fallback is nominal only.
3. **Retire the wider-head lever.** It fails cost on the order tier (Result A) in addition to the
   S3 pitch gate and the earlier 30 s failure. Do not spend further analysis on it.
4. **Park the printed-pancake class** pending a magnetic FEA (external tooling is permitted;
   a printed-pole coupon is not). It is cheap enough to be worth an FEA-only look.
5. **The terminal state is unchanged in kind:** the machine is "one printed coupon (register or
   detent) or one purchase sample (matched motor) away" from print-ready, and [DND-27](/DND/issues/DND-27)
   forbids both. That is **not** a proven dead end (a cost+time-viable pivot exists), and it is
   **not** a buildable success. The mission-level disposition remains with the company `plan`.

## 6. What would change the verdict

- **S5-R → SUCCESS path:** an analytic or CAD demonstration that 80 ganged rotors can be indexed
  and selectively dropped/re-engaged at 5.08 mm pitch with a bounded per-row error budget. If
  that cannot be shown, S5-R falls back to S5 and the mission is coupon/sample-gated.
- **S5 → SUCCESS path:** a matched ≤$1.86 traceable motor lot (forbidden to sample under DND-27).
- **Pancake path:** a magnetic FEA showing ≥0.15 mN·m running torque from a 5.08 mm-pitch printed
  axial rotor.

## 7. Residual uncertainty

| id | Residual | Class | The one quantity that closes it |
|---|---|---|---|
| R-DND52-1 | Register selective dropout/re-engage at 5.08 mm | mechanism | **closed-analytically by [DND-54](/DND/issues/DND-54)** (`s5r_register.py`, ADR `dnd54-s5r-register-latch.md`): the R=4 shared-drive register clears cell fit, neighbour cross-talk, writer force, bank force, time and cost; only as-printed μ/creep and the full multi-row bar assembly remain measurement/CAD-gated |
| R-DND52-2 | Shared bank roll time (300 rpm assumed) and reflected inertia of 80 coupled rotors | calculation | a dynamic model of the coupled bank; feasible to add analytically |
| R-DND52-3 | Printed-pancake torque at 5.08 mm | mechanism | magnetic FEA (external tooling permitted) |
| R-DND52-4 | All K1/K2/K4/K6/K8/K9 residuals from the S5 register | inherited | unchanged by this pivot |
