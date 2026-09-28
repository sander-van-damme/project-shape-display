# DND-38 / DND-45 — Analytic detent contact sweep for S5 (K2)

**Question.** Does the S5 printed rotary detent (0.45 mm leaf, 10 mm long, 1 mm wide,
0.2 mm deflection; `params.json`) hold height and **repeat** after a slipped motor step —
the one quantitative residual (**K2**) on the winner's risk register?

**Answer (CALCULATION, no print/measurement, [DND-27](/DND/issues/DND-27)).**
K2 is **closed by a named geometry at the sourced friction midpoint** (DND-45) and
previously bounded quantitatively (DND-38):

1. The detent's ideal peak restoring torque is **0.00298 mN·m** (reproduces the Test09
   anchor), peak leaf force **6.58 mN**, surface strain **0.13 %**.
2. **The nominal 0.20 mm scallop does not correct a one-step (18°) slip at the sourced
   PLA–PLA friction midpoint μ = 0.35.** Restoring torque at the slip is **0.00256 mN·m**
   vs a friction moment of **0.00278 mN·m** — torque/friction = **0.92 < 1**.
3. The governing ratio is **`T_r/T_f = A·k/(μ·r)`**, **independent of E, preload and leaf
   thickness** (both torques carry the leaf force). For the nominal A = 0.10 mm, k = 5,
   r = 1.55 mm this gives a **μ cliff at 0.323**.
4. **K2 closure (DND-45):** sweep the scallop depth 0.20 → 0.40 mm inside the cam
   envelope. The exact minimum depth for a **1.25 margin** at μ = 0.35 is **0.271 mm**;
   the **chosen 0.40 mm scallop** gives **ratio 1.84** at μ = 0.35, clears 1.25 at the
   sourced worst case μ = 0.50 (ratio **1.29**), and fits the **0.50 mm** envelope
   (radius 1.5 − core 1.0). The chosen depth is written to `params.json`
   (`cam.detent_scallop_depth_mm = 0.40`) and lands in the generated `results/parameters.scad`.
5. Independent second problem: at the seated valley the friction dead-band is only
   **0.00093 mN·m**, ~**25× below the 0.02356 mN·m** toe-flat plateau disturbance anchor.
   The detent alone cannot hold the terrain load; **height retention remains the hard
   stop's job**, exactly as §3 of `08-current-design` states.

**Verdict: K2 → `closed-analytically (named geometry)` at μ ≤ 0.35; `conditional` above.**
The 0.40 mm scallop clears the 1.25 target at the sourced midpoint and the sourced worst
case; the *as-printed* μ, creep and tip bluntness remain measurement-only terms, so the
residual named risk is **print realisation of a 0.40 mm scallop and a sharp tip**, not a
kinematic impossibility. This does not kill S5.

## K2 geometry sweep (DND-45)

Ratios `T_r/T_f` at the 18° slip, sharp tip (flank-tilt/wedge model reduces exactly to
`A·k/(μ·r)`; the tilt raises drive and lowers friction by matched factors):

| Scallop depth [mm] | μ=0.20 | μ=0.35 | μ=0.50 | in envelope |
|---:|---:|---:|---:|:---:|
| 0.20 (nominal) | 1.613 | 0.922 ✗ | 0.645 ✗ | yes |
| 0.28 | 2.258 | **1.290 ✓** | 0.903 ✗ | yes |
| 0.30 | 2.419 | 1.382 ✓ | 0.968 ✗ | yes |
| **0.40 (chosen)** | 3.226 | **1.843 ✓** | **1.290 ✓** | yes |

- Exact minimum depth for a 1.25 margin at μ = 0.35: **0.2712 mm** (`depth_for_ratio`).
- Exact minimum depth for a 1.25 margin at μ = 0.50: **0.3875 mm** → the **0.40 mm**
  choice clears the *sourced high* friction with margin too.
- **Envelope:** max scallop depth = radius 1.5 − core 1.0 = **0.50 mm**. 0.40 mm is
  inside it, leaving 0.10 mm of core wall. A 0.55 mm depth is rejected by
  `sweep_scallop_depth` as `within_envelope: false`.
- **Finite-tip sensitivity:** an 8° contact half-angle (conservative blunt printed tip)
  scales the drive by η = sinc(k·β) = 0.921 → exact minimum depth **0.2946 mm**, still
  under 0.40 mm and inside the envelope. The choice is not knife-edge on tip sharpness.

**Verdict note.** The printed detent *as dimensioned at 0.20 mm* is not sufficient across
the sourced friction range; the named **0.40 mm** geometry is. This **does not kill S5** —
it is the "closes ⇒ deepen the existing printed scallop" branch of the DND-35
cheapest-falsification plan.

## Model

```
Rim      r(θ) = R0 − A(1 + cos(kθ))                (test09 params.json)
Leaf     F(δ) = K·δ,  K = E·b·t³/(4·L³)            (test09 analyse.py detent())
Contact  δ(θ) = preload + A(1 − cos(kθ))
Restore  T_r(θ) = F(θ)·A·k·sin(kθ)   (energy-consistent, T = dU/dθ)
Friction |T_f|   = μ·F·r(θ),  opposing the slide
Wedge     tan(α) = A·k/r  →  U/f = tan(α)/μ = A·k/(μ·r)   (first order)
Tip       η = sinc(k·β), β = tip contact half-angle
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
torque/friction = **0.645** at the nominal 0.20 mm depth, still fails. Tolerance moves the
ratio only via the moment arm and depth; it does not rescue the ∂/∂E-independent 0.92
nominal figure. At the chosen **0.40 mm** depth the same weak corner is **1.084** at
μ = 0.5 — inside the 1.25 margin only up to μ = 0.35. The K2 closure at μ = 0.50 (ratio
1.290) is for the sharp-tip model; a blunt tip plus the weak tolerance corner at μ = 0.50
is the residual combined risk, stated, not hidden.

## What this does / does not establish

- **Does:** turn K2 from "qualitative, no closed form" into a bounded, parameterised
  condition (`μ < A·k·η/r`); name a **crossing geometry (0.40 mm, ratio 1.84 at μ = 0.35)**
  inside the cam envelope; report the finite-tip sensitivity; reproduce all three existing
  detent anchors.
- **Does not:** measure a printed leaf's real μ, creep, wear, or the actual scallop depth
  achieved by FDM. **μ, creep, tip bluntness and the as-printed scallop remain the named
  un-modeled terms.** Under DND-27 no coupon can retire them, so K2 stays **conditional on
  print realisation**, now with a quantitative pass/fail rule and a geometry that passes
  analytically.

## Run

```text
python detent_contact.py     # full classified result, JSON (incl. K2 sweep)
python detent_checks.py      # regression + honesty gates (DND-38 + DND-45)
```
