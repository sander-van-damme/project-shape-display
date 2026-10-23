# Finite technical review

[Report](engineering-report.md) · [Calculations](calculations.md) · [Print verification](../../../owner-print-tests/2026-10-23-clutch-friction-screen/verification.md)

Reviewed 23 October 2026. This review concerns analytical consistency, concept force paths and the delivered passive measurement fixture. It is **not a physical test, magnetic finite-element analysis, production tolerance qualification or high-voltage design approval**.

## Checks completed

- Read the E-295 geometry and evidence, E-300 stationary-friction lesson, DES-009 component baseline, A/B technical reports, electrical selection, material/cost assessment, analytical code and generated tables, both concept CAD sources, and the fixture CAD/procedure/slicer evidence.
- Independently ran `python -m unittest discover -s analysis -p 'test_*.py' -v` from this experiment directory: **38 tests passed**. Relevant tests compare annular torque with independent numerical integration, electrostatic force with capacitance derivatives, thread work with ideal energy per revolution, magnetic series-gap behavior, and geometry/matrix counterexamples. Their passing does not verify the assumed coefficients, gaps or material properties.
- Confirmed that the magnetic model adds fixed-joint reluctance without counting it as extra armature force, and distinguishes core-limit screening from a nonlinear magnetic solution. The separate finite winding envelope is not presented as a complete compact clutch.
- Checked the floating-electrode quarter-force/quarter-capacitance result under its stated equal-area, equal-gap, initially neutral conditions. The documents include stray capacitance, net charge, leakage and the two powered rotating-input contacts.
- Checked the matrix exception: opposite-polarity diagonal voltages can select a polarity-insensitive 2×2 diagonal. Binary rails still do not provide arbitrary masks. Analog three-corner selection can have unequal force; the 3×3 middle-column argument establishes a broader limitation without falsely excluding that example.
- Reviewed the saved and reopened print evidence: seven embedded parts, X1C/0.4-mm settings, support-free paths, open guide/eyelet cores and continuous contact-ring bands. Bambu's actual save/reopen/reslice and the independent G-code feature checks are documented in the print pack; this reviewer did not perform a second redundant slicer run. Initial and reopened G-code are honestly reported as different, with both separately checked.

## Findings resolved during this investigation

| Finding | Resolution retained in the deliverable |
|---|---|
| Fixed axial supports could shunt A's attraction away from the friction interface | A now exposes an integral compliant carrier, its elastic preload and measured-shim requirement. It does not claim zero selection motion. |
| Input thrust drag was liable to be confused with lost output capacity | Reports distinguish added shared-drive torque/heat from output-side stationary rubbing that reduces useful screw torque. |
| B's closed contact could be interpreted as sending the entire attraction into its collars | B separates open pull-in from the closed-contact balance `Ncontact ≈ Felectrostatic − Felastic`; locally opposed attraction/contact forces are not counted twice as bearing load. |
| A's upper input capture initially lacked radial overlap; screw shoulder initially touched the upper support | Capture bore now overlaps the flange while clearing the rotor. The screw shoulder has explicit axial clearance above the upper land. |
| A's keeper features and drive interface needed real connections/access | Radial keeper webs connect to the housing. A small radial access port exposes the input rim without specifying a full shared drivetrain. |
| A's flexure required space above the washer | The conceptual carrier has an explicit stand-off under the free beams; stiffness remains an approximate, unqualified estimate. |
| Fine OFF drag could be reported as zero below a cheap gauge's sensitivity | Fixture instructions give actual force-arm resolution, preserve unresolved readings and distinguish static upper bounds from conservative dynamic output readings. Guide side load/tilt and washer mass are explicit confounders. |
| Different component-count scopes could make A/B appear artificially simple | Cost accounting distinguishes baseline pin/screw, separate films/tracks/brushes, housing, closure, shims, bonds and repeated electronics. Material allocations remain assumptions where no assembled quotation exists. |

## Remaining limits that determine the recommendation

The actual screw starting/running torque is missing. A's gap, washer flatness, flexure preload/creep, steel properties, remanence and thermal duty are unmeasured; its full housing exceeds even the four-height same-tier spacing. B's ordinary-film contact quality, release, electrical-contact wear and energized insulation are unverified. Staggering does not remove neighboring shaft interference. Neither concept proves unselected height retention.

The manual fixture can reject poor friction pairs, expose print variation and establish instrument-limited torque ranges. It cannot validate either actuator, a pitch-compatible assembly, a blocked shared drivetrain or a safe obstruction force. Its technically verified print package is **DEFERRED solely to avoid a fourth READY offer**. DES-009 remains primary, and no follow-on research or owner print is scheduled.
