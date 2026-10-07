---
status: rejected
builds-on: [Q-011]
---

# DES-006: A-011 frozen full-scale load path

## Disposition

**Rejected against its declared combined integration screen.** E-047 establishes 0.12919 mm for the rail-plus-shaft screen before omitted compliance, exceeding the assumed <0.10 mm limit; including the credited 0.09 mm stack gives 0.21919 mm. Individual component passes do not overturn this result. The 100 N case and displacement threshold are screening assumptions, not approved product requirements. Retain the model as negative comparison evidence under ADR-009; no physical validation is claimed.

## Frozen drawing definition (millimetres)

| Interface | Frozen candidate | Evidence class |
|---|---:|---|
| active pitch / cells | 5.08 / 80 cells | inherited geometry assumption from Q-011 context |
| rail | 25 x 25 solid square, 406.4 span, Al `E=69,000 N/mm²` | structural assumption |
| rail supports | two hard supports at rail ends; simply-supported global model | boundary assumption |
| shaft | 8.00 mm solid steel, `G=79,000 N/mm²`, coaxial with rotor axes | structural assumption |
| shaft bearing stations | end bearings plus stations every 50.8 mm (8-pitch), 9 stations total | proposed drawing interface |
| bearing radial clearance | 0.05 mm diametral maximum per station | tolerance assumption |
| rotor/post contact | 3.00 mm nominal rotor body on 8.00 mm shaft; post reaction at 2.00 mm radius | DES-006-derived geometry / load assumption |
| hard stop | post stop takes radial writer reaction; stop contact width 2.00 mm minimum | proposed contact interface |
| cartridge/clamp seam | two 5x5 cartridges, seam at mid-span; four M4 clamps per cartridge, 20 mm clamp land | proposed interface; seam stiffness unresolved |
| service contact | one cell, 3.27 N normal force over 3.00 x 3.00 mm area; worst direction normal to rail plane | inherited service-load assumption |
| writer vector | `F=[0, 2.00, 0] N` tangential at 2.00 mm radius, `Tz=4.00 Nmm` per active rotor | actuation assumption |
| service torque vector | `F=[0, 3.27, 0] N` at 2.00 mm radius, `Tz=6.54 Nmm` | calculated from service force and radius |

The service vector is applied at the cell/post contact, not to the shaft as a
pure torque. The idealized shaft screen conservatively converts all 80 rotor
reactions into one end-to-end torsional resultant; it does not claim that the
post, stop, bearing, clamp, or cartridge carries no bending.

## Reproducible analytical gate

Run from the repository root:

```text
python3 08-integrated-designs/DES-006-a-011-frozen-full-scale-load-path/analysis/q011_frozen_load_path.py
./repo check
```

The script uses `I=b h^3/12`, `delta=P L^3/(48 E I)`, `J=pi d^4/32`, and
`delta=TL/(JG)*10 mm`. It reports:

| Check | Result | Gate |
|---|---:|---|
| 25 mm rail, 3.27 N at mid-span | 0.00204 mm | pass, global rail only |
| 25 mm rail, 100 N incidental hand screen | 0.06226 mm | pass, inherited screening case |
| 8 mm shaft, 80 x 6.54 Nmm | 0.06693 mm | pass, torsion-only |
| 8 mm shaft, one 3.27 N radial point load over 50.8 mm bearing pitch | 0.00064 mm | pass, local beam-only |
| declared non-elastic stack | 0.09000 mm | pass only if seams/compliance are bounded |
| combined 100 N rail + shaft + stack | 0.21919 mm | **fail** if effects are conservatively additive |

The additive line is intentionally the integration gate: the individual
idealized calculations do not establish `<0.10 mm` once the frozen tolerance
allowance and global frame motion are included. The script asserts both the
conditional component results and this fail disposition.

## Worst-case tolerance stack at the cell datum

| Contributor | Half/worst value | Classification |
|---|---:|---|
| cartridge-to-rail datum error | 0.20 mm | assumed assembly tolerance |
| clamp seam opening / local tilt equivalent | 0.20 mm | unresolved; placeholder upper bound |
| bearing radial clearance contribution | 0.05 mm | assumed tolerance |
| rotor/post radial clearance contribution | 0.05 mm | assumed DES-006 fit allowance |
| rail support seating | 0.10 mm | unresolved assembly assumption |
| subtotal | 0.60 mm | calculated assumed stack; not a measurement |

For the executable gate, only the currently bounded 0.09 mm alignment allowance
(0.05 bearing + 0.04 rotor/post) is credited. The 0.60 mm drawing-level stack
is not accepted as a stiffness pass because seam opening, support seating, and
cartridge registration lack a validated stiffness/contact model.

## Failure risks and boundary of evidence

The model omits rail torsion, local plate bending, fastener preload loss,
cartridge seam friction/slip, bearing housing compliance, shaft bending from
the writer vector, post buckling, contact pressure, wear, creep, dynamic
impact, and loaded-neighbour coupling. These omissions are unresolved model
boundary risks, not zero-valued terms. The 3.27 N value and all material,
support, bearing, contact, and tolerance values above are assumptions or
calculations; there are no physical measurements.

Therefore Q-011 is not bounded for integration. Reopening requires a changed load path or justified load-case revision, followed by a CAD/FEA or equivalent contact model with stated tolerances. Physical testing remains a separate
future gate and is not implied by this artifact.

## Seam/contact model follow-up

The parameterized equivalent-spring screen in
`analysis/q011_seam_contact_model.py`, with its durable result recorded in E-047, bounds the question that can be answered
without inventing joint properties. It keeps the frozen rail and shaft
equations and adds four nonnegative series compliance terms for seam, support,
bearing, and rotor/post stop. The 100 N rail-plus-shaft baseline is already
`0.12919 mm`; therefore the allowable omitted displacement is negative and no
positive stiffness assignment can make that combined case pass `<0.10 mm`.

The four omitted terms remain **unresolved**, rather than zero. The model is a
calculated sensitivity model, not FEA or physical validation. Q-011 remains
**HOLD / reject for current integration**. Further calibration cannot rescue this already-failed additive screen. Compare changed load paths computationally before proposing decision-relevant measurements; E-047 retains measurement interpretation limits.
