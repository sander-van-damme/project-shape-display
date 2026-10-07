---
status: complete
builds-on: [Q-011, E-015, A-011, DES-003, DES-004, ADR-008]
---

# E-041: Q-011 service-load and full-scale stiffness uncertainty falsification

## Verdict

**FAIL as an integration gate; unresolved as a product envelope.** E-015's
25 mm rail / 8 mm shaft result is a conditional calculation, not a defensible
full-scale bound for A-011, DES-003, or DES-004. It passes only after selecting
structural dimensions, support conditions, load magnitude, shaft reaction, and
an alignment allowance that are not specified by the integrated designs.

The cheapest decisive analytical result is the sensitivity below: a 25 mm
square rail passes the inherited 0.10 mm screen at 100 N and 150 N, but fails
at 200 N; a 20 mm rail fails at 100 N. An 8 mm shaft passes the inherited
torsion-only screen at 4 and 8 N·mm per rotor, while a 6 mm shaft fails at both.
Thus the “pass” is not robust to the currently unresolved geometry or load
inputs. A-010/A-011 cannot inherit this result because their frame, clamp,
post, and cartridge seam stiffness are also unspecified.

## Evidence classification

| Item | Result | Evidence class |
|---|---|---|
| 406.4 mm span | 80 × 5.08 mm pitch | CAD-derived arithmetic |
| 100 N point load, 4 N·mm/rotor, 0.10 mm limits | chosen in E-015 | assumptions / screening criteria |
| 25 mm rail, 69 GPa aluminium, 8 mm steel shaft | chosen in E-015 | structural assumptions; not in DES-004 CAD |
| 3.27 N cell service load | inherited by DES-004 coupon plans | design input, not measured; load fixture/path unresolved |
| E-041 sensitivity outputs | equations below | calculated, no FEA or physical measurement |
| actual deflection, contact stress, wear, creep, seams | absent | unresolved |

## Reproducible calculation

The check uses E-015's simplified equations, with its simply-supported
midspan beam and continuous solid shaft assumptions:

`I = b h^3 / 12`; `delta_frame = P L^3 / (48 E I)`.

`T = n * torque_per_rotor`; `J = pi d^4 / 32`; `delta_shaft = T L /
(J G) * 10 mm`.

Run:

```text
python3 tools/curated-experiment-checks/E-041/q011_uncertainty_check.py
```

Expected decisive outputs are:

| Case | Calculated displacement | Screen |
|---|---:|---|
| 25 mm rail, 100 N | 0.062258 mm | pass |
| 25 mm rail, 150 N | 0.093386 mm | pass, 0.006614 mm margin |
| 25 mm rail, 200 N | 0.124515 mm | fail |
| 20 mm rail, 100 N | 0.151996 mm | fail |
| 8 mm shaft, 4 N·mm/rotor | 0.040908 mm | pass, torsion only |
| 8 mm shaft, 8 N·mm/rotor | 0.081817 mm | pass, torsion only |
| 6 mm shaft, 4 N·mm/rotor | 0.129381 mm | fail |
| 6 mm shaft, 8 N·mm/rotor | 0.258763 mm | fail |

The load and torque variations are not claims about actual use; they expose
how little margin exists before the assumed envelope changes verdict. The
shaft model excludes bending from off-axis writer force, bearing compliance,
keyways, runout, local rotor support, and frame coupling. The beam model
excludes module seams, support settlement, torsion, local plate bending, and
the actual load footprint. These omissions can only increase or redistribute
motion; they do not justify treating the nominal pass as hardware evidence.

## Candidate dispositions

- **DES-003:** no full-scale service-load/stiffness envelope. Its historical
  per-cell and regional calculations remain analytical assumptions; no
  structural release follows.
- **DES-004 / A-005:** conditionally plausible only as a concept. The 8 mm
  shaft and 25 mm rail are candidate requirements, not existing design facts.
  The 3.27 N rotor load path remains unproved, as independently noted in
  E-042.
- **A-010 / A-011:** no bound. Existing evidence is architecture/CAD-level;
  post buckling, cartridge/clamp registration, seam compliance, and loaded
  neighbour displacement are unmodeled or unmeasured. ADR-008's rejection of
  the represented A-010 five-state geometry remains in force.

## Smallest missing gate and owner action

The design owner must freeze one full-scale load-path drawing before any
integration claim: rail section/material/span/supports, shaft diameter and
bearing spacing, writer reaction vector and torque, rotor/post/stop contact
geometry, module seams, and the 3.27 N service-load fixture direction and
contact area. Then run a beam/shaft plus local-contact CAD/FEA check with
worst-case tolerances against a requirement-owned displacement limit. If the
design remains physical, measure the same points on a full-span structural
coupon; analytical agreement is not hardware validation.

Until that owner action is complete, Q-011 remains open and the correct
disposition is **UNRESOLVED**, with the nominal E-015 screen **rejected as a
release gate**. No candidate is analytically bounded for service load and
full-scale stiffness from current repository evidence.
