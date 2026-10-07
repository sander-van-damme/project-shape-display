---
status: open
builds-on: [P-007, P-010]
---

What load cases and frame stiffness are required for tabletop play and reliable full-scale actuation?

Define representative miniature and incidental-hand loads; measure column support, local abuse, module seams, full-width frame/shaft deflection and worst-case actuation. Existing per-cell force and stiffness inputs are assumptions until measured.

## DES-005 seam/contact bound (2026-10-07)

The reproducible sensitivity model in
`08-integrated-designs/DES-005-des-005-a-011-frozen-full-scale-load-path/analysis/q011_seam_contact_model.py`
represents seam opening, support seating, bearing housing compliance, and
rotor/post hard-stop compliance as four series springs. It cannot assign a
defensible stiffness to any term because the frozen design has no clamp
preload, contact area, housing section, bearing fit, stop material, or gap/slip
law. More importantly, the retained 100 N rail-plus-shaft baseline is already
`0.12919 mm`, before any omitted term, versus the `<0.10 mm` gate.

Result: **HOLD / reject current DES-005 integration against the Q-011 screen**;
no physical validation is claimed. The linked analysis report records each
term as unresolved and gives the cheapest falsification: a loaded 5x5 seam
coupon plus bearing/play and post/stop displacement measurements.
