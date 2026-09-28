# DND-38 — Analytic detent contact sweep for S5 (bounding K2)

**Question.** Does the S5 printed rotary detent (0.45 mm leaf, 10 mm long, 1 mm wide,
0.2 mm deflection; `params.json`) hold height and **repeat** after a slipped motor step —
the one quantitative residual (**K2**) on the winner's risk register?

**Answer (CALCULATION, no print/measurement, [DND-27](/DND/issues/DND-27)).**
K2 is **not closed** but is **bounded and now quantitative**:

1. The detent's ideal peak restoring torque is **0.00298 mN·m** (reproduces the Test09
   anchor), peak leaf force **6.58 mN**, surface strain **0.13 %**.
2. **The nominal leaf does not correct a one-step (18°) slip at the sourced PLA–PLA
   friction midpoint μ = 0.35.** Restoring torque at the slip is **0.00256 mN·m** vs a
   friction moment of **0.00278 mN·m** — torque/friction = **0.92 < 1**. A slipped rotor
   therefore stays one 10 mm level wrong.
3. The governing ratio is **`T_r/T_f = A·k/(μ·r)`**, **independent of E, preload and leaf
   thickness** (both torques carry the leaf force). For the nominal A = 0.10 mm, k = 5,
   r = 1.55 mm this gives a **μ cliff at 0.323**. The detent closes only if the printed
   contact is cleaner than μ = 0.323 (possible at the low end of the sourced 0.2–0.5
   range) — not at the midpoint or the high end.
4. **Two concrete closing levers** (neither kills the architecture): reduce the running
   contact to μ ≤ 0.32, or **deepen the scallop from 0.20 mm to ≥ 0.31 mm** (1.55×) to
   tolerate μ = 0.5 with margin.
5. Independent second problem: at the seated valley the friction dead-band is only
   **0.00093 mN·m**, ~**25× below the 0.02356 mN·m** toe-flat plateau disturbance anchor.
   The detent alone cannot hold the terrain load; **height retention remains the hard
   stop's job**, exactly as §3 of `08-current-design` states. This is now quantified, not
   hand-waved.

**Verdict: `conditional`.** The printed detent *as dimensioned* is not sufficient across
the sourced friction range; a geometry/friction change is required. This **does not kill
S5** — it is the "closes ⇒ the winner needs a spring detent (costs, but does not kill the
architecture)" branch of the DND-35 chea­pest-falsification plan, with the additional
finding that deepening the existing printed scallop is an alternative to adding a separate
spring.

## Model

```
Rim      r(θ) = R0 − A(1 + cos(kθ))                (test09 params.json)
Leaf     F(δ) = K·δ,  K = E·b·t³/(4·L³)            (test09 analyse.py detent())
Contact  δ(θ) = preload + A(1 − cos(kθ))
Restore  T_r(θ) = F(θ)·A·k·sin(kθ)   (energy-consistent, T = dU/dθ)
Friction |T_f|   = μ·F·r(θ),  opposing the slide
```

Valleys (stable rest) are θ = m·2π/k; the unstable crests sit 36° from each valley, so a
one-step 18° slip parks the rotor mid-basin on the steep flank. The detent drives the rotor
home only while `|T_r| > μ·F·r`; where it does not, the tip sticks. `T_r/T_f =
A·k·|sin(kθ)|/(μ·r)`, so the 18° correction condition is `A·k/(μ·r) > 1`.

## Sweep results (E ∈ {700, 1500, 2500} MPa; μ ∈ {0.2, 0.35, 0.5})

| E (MPa) | μ | torque/friction at 18° | corrects a step? | inner lock-in |
|---:|---:|---:|---|---:|
| any | 0.20 | **1.61** | **yes** | 7.66° |
| any | 0.35 | **0.92** | **no** | 18.90° |
| any | 0.50 | **0.65** | **no** | 18.90° |

The E-independence is exact and asserted by `detent_checks.py`. The inner lock-in angle is
where the tip freezes near the valley; when the rotor does recover, the **hard stop**
removes this sub-level residual, so it is a diagnostic, not a level error.

## ±0.05 mm print-tolerance stack-up

Weak corner (thinnest, longest, shallowest, lightest preload at E = 700 MPa, μ = 0.5):
torque/friction = **0.645**, still fails. Tolerance moves the ratio only via the moment arm
and depth; it does not rescue the ∂/∂E-independent 0.92 nominal figure.

## What this does / does not establish

- **Does:** turn K2 from "qualitative, no closed form" into a bounded, parameterised
  condition (`μ < A·k/r`); reproduce all three existing detent anchors; give two concrete
  closing levers with numbers.
- **Does not:** measure a printed leaf's real μ, creep, wear, or the actual scallop depth
  achieved by FDM. **μ, creep and the as-printed scallop remain the named un-modeled terms.**
  Under DND-27 no coupon can retire them, so K2 stays on the risk register as
  **conditional**, now with a quantitative pass/fail rule.

## Run

```text
python detent_contact.py     # full classified result, JSON
python detent_checks.py      # regression + honesty gates
```
