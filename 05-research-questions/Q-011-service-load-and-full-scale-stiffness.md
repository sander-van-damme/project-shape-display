---
status: active
builds-on: [P-007, P-010]
---

# Q-011: service load and full-scale stiffness

## Falsifier disposition

**HOLD for integration.** The current DES-006/A-011 direction has no credible
full-scale service-load or stiffness envelope. The nominal E-015 result is a
conditional screening calculation only; it is rejected as an integration or
release gate. This is an analytical/CAD-evidence disposition, not hardware
validation.

## Evidence and classification

| Item | Evidence | Status |
|---|---|---|
| 406.4 mm span | 80 × 5.08 mm pitch in E-015/E-041 | CAD-derived arithmetic |
| 25 × 25 mm rail, 8 mm shaft, 69/79 GPa materials | E-015 selected values | structural assumptions; absent from DES-006/A-011 geometry |
| 100 N mid-span load and 0.10 mm motion limit | E-015 screen and Q-005/E-009 inherited criterion | assumptions/screening criteria, not product requirements |
| 25 mm rail at 100/150/200 N | 0.062258/0.093386/0.124515 mm | calculated sensitivity; pass/pass/fail |
| 20 mm rail at 100 N | 0.151996 mm | calculated sensitivity; fail |
| 8 mm shaft at 4/8 N·mm per rotor | 0.040937/0.081874 mm torsional end motion | calculated, torsion only |
| 3.27 N cell load applied at 2 mm radius | 6.54 N·mm/rotor; 8 mm shaft gives 0.066932 mm, 6 mm gives 0.211539 mm | calculated limiting check; load path still unresolved |
| actual frame seams, bearing compliance, post/clamp/cartridge contacts, creep, wear, bending and runout | not represented in E-015 or A-011 | unresolved |

The 3.27 N check is important because E-041 lists that service load while
E-015 uses only 4 N·mm/rotor (equivalent to 2 N at 2 mm). Even after using the
higher 6.54 N·mm torque, the 8 mm shaft result remains only a torsion-only
calculation; it does not establish the actual reaction vector or local contact
stress. A-011 specifies a clamp/cartridge/post load path architecturally but
does not specify dimensions, supports, seams, or stiffness values. ADR-008 also
rejects the represented A-010 five-state load-path claim.

## Reproducible analytical gate

Run from the repository root:

```text
python3 tools/curated-experiment-checks/E-041/q011_uncertainty_check.py
./repo check
```

The checks use, in mm/N units, `I = b h^3 / 12`,
`delta_frame = P L^3 / (48 E I)`, `J = pi d^4 / 32`, and
`delta_shaft = (T L / (J G)) * 10 mm`. Acceptance is `< 0.10 mm` at every
specified measurement point, with the load case and boundary conditions
owned by the design. A pass is not transferable between architectures.

## Cheapest decisive next gate

Before integration, the design owner must freeze one load-path drawing covering
rail section/material/span/supports, shaft diameter and bearing spacing, writer
force vector and torque, rotor/post/stop contacts, cartridge/clamp seams, and
the 3.27 N service-load direction/contact area. Re-run the beam/shaft model
with those boundaries plus local contact/tilt checks. The smallest decisive
CAD-derived gate is a worst-case tolerance model of that frozen path against
the `< 0.10 mm` limit; no physical test is implied. If the model cannot
bound seams, support compliance, and load transfer, integration remains on
HOLD.

## Requirement question

What load cases and frame stiffness are required for tabletop play and reliable
full-scale actuation? Existing per-cell force and stiffness inputs remain
assumptions until the load path is dimensioned and checked. E-015 and E-041
are the supporting analytical records; neither closes Q-011.

## DES-006 seam/contact bound (2026-10-07)

The reproducible sensitivity model in
`08-integrated-designs/DES-006-a-011-frozen-full-scale-load-path/analysis/q011_seam_contact_model.py`
represents seam opening, support seating, bearing housing compliance, and
rotor/post hard-stop compliance as four series springs. It cannot assign a
defensible stiffness to any term because the frozen design has no clamp
preload, contact area, housing section, bearing fit, stop material, or gap/slip
law. More importantly, the retained 100 N rail-plus-shaft baseline is already
`0.12919 mm`, before any omitted term, versus the `<0.10 mm` gate.

Result: **HOLD / reject current DES-006 integration against the Q-011 screen**;
no physical validation is claimed. E-047 records each term as unresolved and gives the cheapest falsification: a loaded 5x5 seam
coupon plus bearing/play and post/stop displacement measurements.
