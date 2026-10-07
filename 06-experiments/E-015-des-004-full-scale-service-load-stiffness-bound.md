---
status: complete
builds-on: [Q-011, DES-004, DES-003, E-009, ADR-004]
---

# E-015: DES-004 full-scale service-load and stiffness bound

## Gate and disposition

This is one analytical gate for Q-011. It bounds a 406.4 mm full-width frame
and a continuous row shaft under tabletop service and worst-case rotary
actuation. It is a calculation, not FEA, CAD validation, or physical testing.

**DES-004 is conditionally retained.** The candidate is mechanically plausible
only with a separately specified structural frame and shaft. Under the frozen
screen below, a 20 mm square rail and a 6 mm shaft are falsified; a 25 mm
square rail and 8 mm shaft pass the simplified bound. The existing 1.00 mm
coupon axle is far beyond the 0.10 mm motion allowance and is not a full-scale
shaft specification.

## Frozen load cases and assumptions

| Item | Value | Class |
|---|---:|---|
| active width / shaft span, `L` | 406.4 mm | CAD-derived from 80 × 5.08 mm pitch |
| service point load | 100 N at midspan | bounded assumption for incidental hand load; unresolved product load case |
| frame rail | 25 × 25 mm rectangular section, simply supported | bounded structural assumption; not present in DES-004 CAD |
| frame material modulus, `E` | 69,000 N/mm² | sourced-class assumption for aluminium; alloy/temper unresolved |
| shaft torque per active rotor | 4.0 N·mm | worst-case assumption: 2.0 N tangential writer reaction at 2.0 mm radius |
| simultaneous rotor count | 80 | full row, conservative upper bound |
| shaft diameter cases | 1, 4, 6, 8 mm solid round | sensitivity; 1 mm is the DES-004 coupon axle nominal |
| shaft material modulus, `G` | 79,000 N/mm² | sourced-class assumption for steel; actual part unresolved |
| allowable frame motion | 0.10 mm | Q-005/E-009 screening threshold used as alignment bound |
| allowable shaft-end tangential motion | 0.10 mm at 10 mm lever arm | engineering acceptance assumption; reader/writer stack-up unresolved |

The 100 N hand load is not a claim about user behaviour. It is a declared
screening load so the calculation can be falsified or replaced. The point load
is deliberately more severe for midspan bending than a uniform miniature
load; it does not represent 6,400 miniatures simultaneously.

## Equations and calculated results

For the simply supported frame rail with a midspan point load:

`I = b h^3 / 12`; `delta_frame = P L^3 / (48 E I)`.

For the solid round shaft, with `n` simultaneous rotor reactions:

`T = n F_t r`; `J = pi d^4 / 32`; `theta = T L / (J G)`; and
`delta_shaft = theta * 10 mm`.

The executable `E-015-des-004-full-scale-service-load-stiffness-bound.py`
evaluates both equations and asserts the reported gate values. Its result is:

| Case | Calculated result | Gate |
|---|---:|---|
| 25 × 25 mm aluminium rail, 100 N midspan | `delta_frame = 0.0623 mm` | pass with 0.0377 mm nominal margin |
| 20 × 20 mm aluminium rail, 100 N midspan | `delta_frame = 0.1520 mm` | fail (sensitivity) |
| 1 mm steel continuous shaft, 80 × 4 N·mm | `delta_shaft = 167.678 mm` at 10 mm lever | fail by ~1,677× |
| 4 mm steel shaft | `delta_shaft = 0.6550 mm` | fail analytically |
| 6 mm steel shaft | `delta_shaft = 0.1294 mm` | fail analytically |
| 8 mm steel shaft | `delta_shaft = 0.0409 mm` | pass analytically |

The 25 mm frame result has limited margin: a 20% reduction in rail height
(20 mm) gives `0.1520 mm` and fails; a 20% reduction in modulus gives
`0.0779 mm` and passes this isolated calculation. The section and support
condition therefore require explicit full-scale design evidence.

## Interfaces and failure risks

The structural frame must carry the rail reactions into tabletop supports
without relying on printed 3 mm coupon sheet stiffness. The actuator reaction
must close locally through the rotor support/frame; it must not be carried by
a 1 mm axle over the full 406.4 mm span. An 8 mm shaft passes this simplified
torsion bound but has no allowance here for bearing compliance, keyway stress
concentration, bending from off-axis writer force, or assembly runout.

The bound also excludes seam compliance, local rotor/web stress, dynamic
acceleration, impact, creep, and load transfer between neighbouring modules.
Those remain unresolved and prevent a production or hardware-performance
claim. E-009/ADR-004 remain the relevant regional-isolation evidence and are
not closed by this calculation.

## Reproduction and integration

From the repository root:

```text
python3 06-experiments/E-015-des-004-full-scale-service-load-stiffness-bound.py
./repo check
```

The script uses only Python's standard library. Rollback is a single-object
revert of E-015; no DES-004 geometry or baseline was changed. Integration
requires a future DES-004 revision to specify the rail section, support span,
shaft diameter/material, bearing spacing, and actual writer reaction before
the conditional retention can become a design release.

## Unresolved owner/action

Design owner: freeze the full-scale frame/shaft interface and replace the
declared 100 N / 4 N·mm screening assumptions with measured or sourced design
inputs. The smallest next bounded check is a beam/shaft CAD or FEA model with
the actual seams and bearing supports; no such model or physical test exists
in this record.
