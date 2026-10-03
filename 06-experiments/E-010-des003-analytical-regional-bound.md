---
status: complete
builds-on: [E-006, E-007, E-009, DES-003]
---

# E-010: DES-003 analytical regional-coupling bound

## Objective

Check whether the existing DES-003 evidence can justify the E-009 proposed
gate of **0.10 mm peak motion of an untouched loaded neighbour** during 5×5,
10×10, and 20×20 updates. This record is deliberately pre-physical: no print,
purchase, material test, FEA, or physical validation is claimed.

## Reproducible method

Run from the repository root:

```text
python3 08-integrated-designs/DES-003-reliability-first/analysis/e009_analytical_bound.py
```

The model uses the E-009 design-calculated service load `F = 3.27 N`, the
proposed motion gate `g = 0.10 mm`, and the square-region perimeter
`n = 4 × (side − 1)`. For an assumed per-boundary-cell coupling `α`:

```text
F_equiv = F × n × α
k_required = F_equiv / g
d_predicted = F_equiv / k_eff
α_max = k_eff × g / (F × n)
```

The script reports sensitivities at α = 1%, 5%, and 10%, and candidate
stiffness labels of 10, 32.7, and 50 N/mm. These labels are not measured
properties of DES-003.

## Calculated result

| update region | boundary cells | required k at 1% | at 5% | at 10% |
|---|---:|---:|---:|---:|
| 5×5 | 16 | 5.23 N/mm | 26.16 N/mm | 52.32 N/mm |
| 10×10 | 36 | 11.77 N/mm | 58.86 N/mm | 117.72 N/mm |
| 20×20 | 76 | 24.85 N/mm | 124.26 N/mm | 248.52 N/mm |

At the candidate 50 N/mm stiffness label, the maximum coupling compatible with
the gate is approximately 9.56% (5×5), 4.25% (10×10), and 2.01% (20×20).
This is a sensitivity result, not evidence that the design has 50 N/mm
stiffness or that coupling is below those limits.

## Evidence audit and disposition

| case | disposition | reason |
|---|---|---|
| 5×5 | **UNRESOLVED** | DES-003 has no bounded effective support stiffness or coupling fraction; the CAD fixture defines geometry only. |
| 10×10 | **UNRESOLVED** | The 10×10 extension and its support boundary are not a validated CAD/FEA model; coupling and trajectory remain unspecified. |
| 20×20 | **UNRESOLVED** | The perimeter sensitivity becomes most demanding, while support compliance, actuator path, contact/clearance, and worst orientation remain unbounded. |

The calculation does not falsify the claim by itself because no justified
`k_eff`/`α` pair predicts motion above 0.10 mm. It also cannot promote the
claim: the E-009 promotion rule requires a geometry/material-justified model
including support compliance, actuator trajectory, contact/clearance, and
worst boundary orientation. None is available in the current repository.

## Smallest next evidence requirement

Either (a) run the frozen E-009 coupon-B sequence with a displacement logger,
loaded untouched neighbour, both update directions, and the worst boundary
orientation for all three region sizes, or (b) provide a validated FEA model
with the actual tile/support geometry, material properties, actuator
trajectory, contact/clearance, and boundary conditions. Record peak and
residual displacement plus the inferred force path. Until then DES-003 must
remain open and not qualified for regional-isolation promotion.
