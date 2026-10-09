---
status: complete
builds-on: [E-089, E-094, ADR-016]
---

# Open pickup contact separates without a per-deposit release latch

**Retain a unilateral lift-pad/pickup-lip section for finite stop-setting work.**
A grounded column can remain on its new stop while the deck continues down,
without retracting its extended pickup lip at that height. A captured bilateral
hook instead needs release or it drives the foot into the stop. This removes
an unnecessarily prescribed local release action from E-089's deck hypothesis;
it does not remove initial hook setting/retention, final clear/proof, or the
need for a physically settable load-bearing stop. No complete machine survives
yet. E-094's timing is not improved by silently deleting its proof allowances.

Input main `f057b4d`. Reproduce
`python3 tools/curated-experiment-checks/E-095/pickup_contact.py`.
Evidence: generated planar rectangles, contact-state calculation and deterministic
error corners; rigid quasistatic gravity only. No measured X1C prior, contact
strength, dynamic separation, load-bearing setter, 3D assembly or hardware test.
This is a support-contact topology discrimination, not a new whole architecture.

## Finite geometry and uncertainty

At 5.08-mm pitch, the nominal column occupies x=0…2.4 mm. In a lower pickup
lane, a 2.4-mm-long lip translates from x=0…2.4 (inactive) to 1.4…3.8 (active).
Its root overlaps the column/housing; that region is a joint, not a collision
between independent solids. A finite deck finger spans x=3.1…4.3 and is 0.9 mm
thick. The next column starts at x=5.08. The column foot rests on a ground
contact in a separate x=0…1.2 lane. The side housing is cut back from the ground-stop
lane below foot height; an upper cap joins the foot and side housing. The pickup
face sits above the foot so arm/clear does not cut through the loaded stop. Lip guidance, the positive arm/clear setter,
retention and housing voids are ungenerated; root overlap alone is not a joint.

Competing bounds assign each column, finger and neighbor datum ±e, with
lip-end, finger-edge and body-edge errors ±0.1 mm. Datum errors may be coherent
across a print/bank; the Cartesian corners also allow differential errors.
No probabilities or independence are inferred. Vertical lip datum is 1.0±0.2 mm
above the foot; old/new stop-height errors are separately ±0.2 mm and may
align. Lip thickness uses 0.9 mm. These are deliberately labelled hypotheses;
roughness, layer effects, angular error, flexure, wear and creep are not covered
by a claimed manufacturing distribution.

| Datum bound e, mm | Minimum capture overlap | Inactive/body gap | Neighbor gap | Section gate |
|---:|---:|---:|---:|---|
| 0 | 0.50 | 0.50 | 0.68 | survives |
| 0.10 | 0.30 | 0.30 | 0.48 | survives |
| 0.20 | 0.10 | 0.10 | 0.28 | survives |
| 0.30 | 0 | −0.10 | 0.08 | reject |

The nominal row still contains edge uncertainty. The independent interval bound
for overlap and inactive/body clearance is `0.5−2e`; neighbor gap is
`0.68−2e`. A chosen 0.05-mm geometric reserve requires **e≤0.225 mm** for this
section. This is a capture/isolation inequality, not a qualified tolerance or
sufficient bearing area. Root overlap remains ≥0.9 mm. At e=.3 a withdrawn lip
and passing finger have a concrete **0.05-mm² planar intersection**. A selected
lip can also lose overlap. Do not turn this into a tolerance requirement without
comparing changed geometry and actual process evidence.

## Actual contact and supported separation

Let e_z be finger top height, δ the lip-to-foot vertical datum and s the current
grounded stop height. A selected column in gravity has foot coordinate
`z=max(s,e_z−δ)`. At least one of its finite foot/stop or lip/finger contacts is
closed; neither interpenetrates. A nonnegative static load split exists. This
is a quasistatic existence result, not dynamic force, stiffness or impact proof.
An inactive lip has no horizontal intersection with the deck for the retained
bounds, so the unchanged column remains on its old stop throughout the sweep.

Start at e_z=−2 mm, arm selected lips while the deck is clear, rise to +45 mm,
then descend to −2 and clear: **94 mm total deck travel**, before additional
contact/proof excursions. This replaces the ideal 90-mm path for this subsection. Pickup occurs separately at each old height.
At the top, the foot is at least **3.6 mm above both old and target stops** under
the declared vertical errors. **Changing stop height there is a granted boundary
condition, not a generated setter**; a real rotor/structural-stop sweep could
hit the elevated column despite adequate endpoint height. That is the next gate.
During descent a column lands at its target stop; for e_z<s+δ, a positive gap
opens under the lip while its lateral position stays active. The deck finger
can continue downward in its separate lane. All hooks can be cleared once at
home; individual deposition must still be detected/proven before unsafe motion.

Generate finite finger, lip, column, neighbor and ground rectangles for all
81 old/target combinations, nine neighbor heights and eight vertical-error
corners: **5,832 cases / 116,640 contact states**. The horizontal proof separately
checks **400 unique error-corner assignments** over four datum bounds. A coherent
adverse-capture section supplies the vertical polygon replay; the independent
horizontal separation bounds cover all vertical positions of bodies/neighbors.
This is a two-cell section, not a bank tiling or arbitrary 3D collision proof.

Contact onset is an explicit breakpoint; between breakpoints the coordinates
are affine and contact/separation inequalities monotone. Uniform intermediate
samples supplement that argument. Eighteen extreme/mixed holdouts at 1/16/64
subdivisions agree. Arm and clear sweeps at home check 17 lip positions per
endpoint; their vertical separation proves the continuous horizontal sweep.
No dynamic time step or mesh claim is applicable.

A bilateral captured hook would impose `z=e_z−δ` after landing. With δ=0,
target=20 mm and e_z=19.5 mm, the finite foot penetrates its stop by 0.5 mm
(**0.6 mm²** in the tested plane). Hence a captured connection needs actual
release; the unilateral contact does not. Conversely, if a previously selected
lip fails to clear, the next upward deck pass can move an unchanged column:
e_z=10, δ=1.2, old=0 gives **8.8-mm unintended lift**. Positive neutralization
and individual readback remain essential. The open contact is not a reset-proof
selector and supplies no upward restraint against bounce or off-axis motion.

## Next discriminator and limits

Keep open support contact as the preferred pickup comparator and stop treating
per-level hook retraction as mandatory for every deck architecture. Preserve the
captured-hook exclusion and failed-clear witness. Continue with **finite
load-bearing memory and its unloaded setting sweep**, alongside positive hook
setting/retention and non-target passage; compare rotary, translating structural
and genuinely changed support hypotheses with direct positioning. Do not simply
add E-093's failed reversible output cam.

Strength, ground-frame deflection, friction, lip bending, print orientation,
retention against disturbance, full-board loading, true support sensing, repair
access and assembly remain unproved. A 0.1-mm geometric overlap carries no
credited force. No print, purchase, numerical yield or hardware pass follows.
