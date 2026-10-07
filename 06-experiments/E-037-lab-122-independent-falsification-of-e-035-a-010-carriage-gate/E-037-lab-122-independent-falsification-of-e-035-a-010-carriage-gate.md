---
status: active
builds-on: [E-035, ADR-008, E-031]
---

# E-037: LAB-122 independent falsification of E-035 A-010 carriage gate

## Verdict

**FAIL as a bounded CAD/load-path gate.** The two Python checks pass only the
same nominal constants they define. The SCAD does not place the claimed gate,
guide, carriage, follower, and stop reaction in one connected geometry. This
rejects E-035's integration conclusion; it does not prove that a corrected
carriage architecture is impossible.

| Claim under audit | Verdict | Evidence boundary |
|---|---|---|
| Five-state reach | **FAIL (represented CAD); PASS only as arithmetic** | The scripts enumerate 0, 0.8, 1.6, 2.4, 3.2 mm, but the SCAD's carriage overlays are not inside the guide stack and no moving/coupled path is modeled. |
| Indexed-stop identity | **FAIL** | `indexed_stop_plate()` is one horizontal plate at z=1.20–2.00 mm. Its five translated cutter cubes share x/y and all intersect that same plate; they do not create five vertically separated stop shelves. S0–S4 cutter z-ranges are 0.78–1.60 through 3.98–4.80 mm. |
| Carriage/guide envelope | **FAIL** | The lower and upper guide slabs occupy z=0–0.40 and 0.80–1.20 mm. The nominal S2 carriage is translated to z=2.38–2.80 mm (`.78+z`), outside both guides; the other overlays are likewise outside the guide stack. |
| Follower bypass/load reaction | **FAIL** | At S2 the follower starts at z=2.80 and shoulder at z=3.60, while the stop plate ends at z=2.00. There is no shoulder-to-stop contact in the CAD. The stated `shoulder -> stop land` path is asserted by script output, not geometrically demonstrated. |
| Writer travel/engagement | **FAIL / unresolved** | The script calls 3.60 mm (3.20 + 0.40 approach) a writer stroke, while the document calls the envelope 4.00 mm. The SCAD has one static red block, not a 3.60/4.00 mm path, carriage coupling, or 0.60 mm engagement/contact check. |
| Tolerance-sensitive clearance | **UNRESOLVED** | Nominal arithmetic gives 0.90 mm gate radial, 0.20 mm stop radial, 0.70 mm shoulder land, and 0.30 mm guide clearance. No tolerance stack, tilt, flatness, layer registration, or worst-case contact geometry is modeled. |

## Reproduction and calculations

From the repository root:

```sh
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_gate_check.py
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_independent_recheck.py
timeout 8s openscad --export-format binstl -o /dev/null 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_bounded_carriage.scad
./repo check
```

The primary and independent scripts both pass. Their results are calculated
from duplicated constants and therefore do not validate SCAD intersections.
OpenSCAD was available but did not complete the requested export within the
8-second bounded run (`rc=124`); this is neither syntax-pass nor solid-export
evidence. `./repo check` is the required follow-up after this document is
committed.

The decisive section checks are direct coordinate comparisons from the SCAD:

- Gate slab: z=0.40–0.80; its aperture cutter is z=1.77–2.21. Thus the
  asserted aperture is not cut through the gate slab.
- S2 carriage: z=2.38–2.80; follower: z=2.80–4.80; shoulder:
  z=3.60–3.95; stop plate: z=1.20–2.00. Thus the claimed load reaction has
  a 1.60 mm minimum vertical gap even before tolerances.
- The script's 4.00 mm document claim is inconsistent with its own 3.60 mm
  stroke expression. This is a definition inconsistency, not actuator
  capability evidence.

## Scope and next bounded action

Evidence is calculated and CAD-derived only. No physical, friction, stress,
wear, reader, timing, procurement, or manufacturing-performance conclusion
is made. The E-035 author must first repair the datum convention and produce a
single-state section in which gate aperture, guide, carriage, follower,
shoulder, and the selected stop visibly intersect as intended; then encode
all five states and a real writer path from those shared geometry parameters.
An independent check should compute intersections from the CAD dimensions,
not duplicate the nominal constants. Only after that analytical gate passes
should the separate physical coupon gates in ADR-008/E-031 resume.
