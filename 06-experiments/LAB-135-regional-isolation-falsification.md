---
status: hold
builds-on: [E-009, Q-005, A-011, ADR-006, E-017, E-018, E-040, DES-005]
---

# LAB-135: A-011 regional-update isolation falsification

## Verdict

**HOLD — regional isolation is unresolved.** A-011 remains a conditional
architecture boundary, but the current evidence does not provide a credible
analytical/CAD acceptance path for updating a region without disturbing a
neighbor. E-009 and Q-005 remain open/uncertified; neither is promoted to GO
and neither is rejected as a design class.

This is a documentation and calculation result only. No hardware, FEA, print,
supplier, or physical measurement was used.

## Reproducible acceptance model

The affected region is the commanded update region. For E-009, the required
untouched neighbor is the center station of the 5×5 Coupon-B fixture, loaded
vertically with the design input `F_service = 3.27 N`; the 10×10 and 20×20
cases retain the same pitch and loaded-neighbor definition on an extended
fixture. The update boundary has `n_boundary = 4(side−1)` cells: 16, 36, and
76 cells respectively.

Acceptance is `d_peak ≤ 0.10 mm` and `d_residual ≤ 0.10 mm` for every required
case, after subtracting the disabled-update baseline and rigid reference. The
upper uncertainty bound must also remain at or below 0.10 mm. This is the
E-009/Q-005 screening criterion, not a product limit.

The cheapest current sensitivity model is:

```text
F_equiv = 3.27 N × n_boundary × alpha
k_required = F_equiv / 0.10 mm
```

For assumed coupling `alpha = 5%`, the required support stiffness is 26.16,
58.86, and 124.26 N/mm for 5×5, 10×10, and 20×20. At candidate stiffness
`k = 32.7 N/mm`, the corresponding maximum coupling is only 6.25%, 2.78%, and
1.32%. These are sensitivity calculations, not evidence that any stiffness or
coupling value is achieved. Reproduce with:

```sh
python3 08-integrated-designs/DES-003-reliability-first/analysis/coupon_b_gate.py
python3 06-experiments/E-018-four-plane-mask-generator-coupon-package/analysis/coupon_protocol.py --check
./repo check
```

## Falsification findings

1. E-018 CAD checks field span, aperture web, writer overlap, parked clearance,
   reader clearance, and nominal fiducial/interface geometry. OpenSCAD and the
   protocol checker do not calculate clamp preload, actuator reaction force,
   support compliance, material stiffness, contact/friction, transient motion,
   or load transfer into a loaded neighbor.
2. E-018’s loaded-neighbor coupon gate is `≤0.20 mm per local write`; that is
   not equivalent to E-009/Q-005’s `≤0.10 mm peak and residual` gate. A result
   between 0.10 and 0.20 mm would pass E-018 while failing the assigned
   regional-isolation question.
3. E-018 models only a 5×5 interface coupon with N/E/S/W rigid dummy carriers;
   it does not model the E-009 loaded center station or the 10×10/20×20
   boundary cases. “Rigid dummy” is a clearance/protocol fixture assumption,
   not a demonstrated neighboring-cell load path.
4. A-011/E-017 regional latency numbers (0.72 s or 1.72 s for 5×5) are
   transport/write/verify accounting only. They do not establish that local
   clamping or four-plane engagement leaves the loaded terrain below the
   motion criterion.
5. E-040 correctly keeps clamp, actuator force/stroke/life, and reader/media
   compatibility on hold; it therefore supplies no isolation evidence.

The claim is consequently **not analytically passed**. A rejection is also
not justified because no model predicts `d_peak > 0.10 mm`; the missing input
is a bounded mechanical response, not a demonstrated failure.

## Smallest decisive next test

The next owner should run the E-018 5×5 coupon with the E-009 boundary
condition: replace the rigid center/dummy isolation setup with a calibrated
3.27 N loaded untouched neighbor, retain the frame-fixed datum and baseline
subtraction, and instrument vertical and lateral neighbor displacement during
the worst single local write and clamp/reseat event. Use the E-009 gate
(`0.10 mm` peak and residual, including uncertainty), not E-018’s looser
`0.20 mm` gate. If that 5×5 test passes, extend the same model and fixture
boundary to 10×10 and 20×20; a 5×5 pass alone cannot close Q-005.

An alternative nonphysical route is a validated FEA/contact model containing
the same support compliance, actuator trajectory/force, clamp preload,
material/process tolerances, loaded contact, and all three region sizes. A
nominal solid CAD clearance export is insufficient.

## Evidence classification

| Item | Classification | Disposition |
|---|---|---|
| 5.08 mm pitch, 40 mm coupon envelope, aperture/port/fiducial geometry | CAD-derived | nominal interface only |
| 3.27 N service load and 0.10 mm gate | calculated/proposed input | not physically verified |
| stiffness/coupling table above | calculated sensitivity | no defensible bound |
| E-018 protocol/checker output | calculated/schema and CAD coordinate checks | passed definition checks only |
| clamp, support, material, force, trajectory, neighbor motion | unresolved | decisive missing evidence |
| regional-isolation pass/fail | unresolved | HOLD |

