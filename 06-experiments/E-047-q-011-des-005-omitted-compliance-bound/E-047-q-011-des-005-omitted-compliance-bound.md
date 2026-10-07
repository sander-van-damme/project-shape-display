---
status: active
builds-on: [Q-011, DES-006]
---

# E-047: DES-006/Q-011 omitted-compliance bound

## Question

Can seam opening, support seating, bearing housing/play, and rotor/post
hard-stop compliance be bounded from the frozen DES-006 geometry and load
inputs strongly enough to pass Q-011's `<0.10 mm` integration screen?

## Reproducible method

Run from the repository root:

```text
python3 06-experiments/E-047-q-011-des-005-omitted-compliance-bound/q011_compliance_bound.py
python3 08-integrated-designs/DES-006-a-011-frozen-full-scale-load-path/analysis/q011_seam_contact_model.py
./repo check
```

`q011_compliance_bound.py` retains the frozen 25 mm square rail, 406.4 mm
span, aluminium `E=69,000 N/mm²`, 8 mm shaft, steel `G=79,000 N/mm²`, 80
rotors, 2 mm actuation radius, 100 N incidental-hand screen, and the 0.10 mm
gate. It models the four omitted interfaces as nonnegative series
displacements:

```text
delta_omitted = F * (1/k_seam + 1/k_support + 1/k_bearing + 1/k_stop)
```

The stiffnesses are parameters, not claimed properties. No preload, contact
area, fit, housing section, stop material, gap, or slip law is frozen, so the
calculation does not silently turn an unknown interface into a positive
stiffness.

## Result

| Quantity | Result | Evidence class |
|---|---:|---|
| 100 N rail displacement | 0.06226 mm | calculated from frozen beam equation |
| 80-rotor shaft torsion displacement | 0.06693 mm | calculated from frozen torsion equation |
| retained rail + shaft baseline | 0.12919 mm | calculated; before omitted compliance |
| allowance to `<0.10 mm` at 100 N | -0.02919 mm | calculated decisive failure |
| required omitted displacement | `<0 mm` | calculated; impossible for nonnegative compliance |
| required equivalent omitted stiffness | no finite positive value | calculated |
| service rail + shaft baseline | 0.06897 mm | calculated sensitivity |
| service allowance before 0.09 mm fixed stack | 0.03103 mm | calculated sensitivity |

Even the limiting case `k_seam, k_support, k_bearing, k_stop -> infinity`
remains at 0.12919 mm for the 100 N envelope. Illustrative 10,000 N/mm
stiffnesses add 0.04000 mm; these values are sensitivity points only, not
DES-006 properties.

## Disposition

**Q-011/DES-006 remains HOLD / reject for integration against the `<0.10 mm`
screen.** This is an analytical disposition, not hardware validation. The
global 100 N screen is already over the gate before seam, support, bearing, or
stop compliance is included. The four terms therefore remain unresolved for
the drawing-level design, but resolving them cannot rescue this particular
100 N combined screen without changing a retained load-path input or the
requirement.

The service case is not a pass claim: the 0.09 mm credited alignment allowance
would produce 0.15897 mm when added to the service rail-plus-shaft result.
Analytical contact compliance and hardware performance remain unvalidated.

## Missing inputs / next decisive evidence

To quantify the four individual terms for a revised load case, provide a
contact or measurement model with: seam section, clamp preload/friction and
load eccentricity; support land and seating gap/preload; bearing type, fit,
housing section and radial play; and stop material, contact land, gap and
crush/wear law. A loaded 5x5 seam coupon plus direct bearing/play and
post/stop displacement measurements supplies these parameters, but no physical
testing was performed for this experiment.
