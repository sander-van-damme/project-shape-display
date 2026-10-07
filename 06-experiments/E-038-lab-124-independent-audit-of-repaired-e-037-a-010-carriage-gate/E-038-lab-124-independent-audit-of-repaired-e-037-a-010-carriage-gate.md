---
status: complete
builds-on: [E-037, E-035, ADR-008]
---

# E-038: LAB-124 independent audit of repaired E-037 A-010 carriage gate

## Verdict

**FAIL for the claimed five-state CAD gate; PASS only for the bounded nominal
S2 section and the nominal indexed-stop geometry. Do not integrate A-010.**
The repair fixes the earlier state-index/load-axis representation error, but
the actual SCAD still does not model a five-state translating gate inside the
claimed guide envelope, and it does not represent the claimed stop-plate to
frame load-support connection.

| Gate | Disposition | Evidence and boundary |
|---|---|---|
| Shared x/y state datum | **PASS (CAD/calculated)** | `state_y` is generated once from `state_pitch`/`state_count`; the selected S2 gate, carriage, follower, shoulder and stop bores use the same y datum. This repairs the prior z/state conflation. |
| Aperture | **PASS for S2; FAIL for five-state claim (CAD)** | `gate_slider(state_y[2])` cuts one aperture at y=0. The four reference carriages are generated at other y values but their corresponding apertures are not cut; those followers therefore intersect the solid slider. A translating five-state gate is not represented. |
| Guide/carriage envelope | **FAIL (CAD)** | The claimed slider envelope is 4.20 × 4.60 mm, but `gate_slider()` creates `cube([slider_x,field,gate_t])` with y length `field=cartridge=30.48` mm. The guide y span is 4.90 mm. The actual slider therefore exceeds the guide datum by 25.58 mm in y, despite the checker asserting only parameter inequalities. The 4.00 × 0.42 mm carriage itself fits nominally. |
| Indexed-stop identity | **PASS nominal (CAD/calculated)** | Five bores are generated from the shared state list at −1.60, −0.80, 0, 0.80, 1.60 mm; selected S2 identity is unambiguous. This does not establish retention, wear, friction, or repeatability. |
| Follower-to-stop reaction | **PASS locally; FAIL as complete frame load path (CAD)** | Follower Ø1.20 passes the selected Ø1.60 bore and Ø3.00 shoulder gives 0.70 mm radial land on the stop plate. However, the SCAD places the stop plate at z=1.20–1.50 and the frame plate at z=0–0.20 with no modeled connector/support between them. `stop plate -> frame` is asserted in prose but absent from the solid geometry. |
| Writer path | **PASS nominal geometry; UNRESOLVED mechanism** | The red path spans 3.20 mm travel plus 0.20 mm approaches and the lower tab overlaps the S0 carriage region. It is a drawn volume, not evidence of actuator coupling, force, or reliable engagement. |
| Nominal clearances | **PASS only for checked scalar values; FAIL as whole-model envelope claim** | Aperture, stop bore, shoulder land and frame margin calculate positive. The checks do not test the actual slider y extent or support continuity, so they cannot support the broader clearance/load-path claim. |

## Reproduction

From the repository root:

```sh
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_gate_check.py
PYTHONPATH=06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_independent_recheck.py
openscad --export-format binstl -o /dev/null 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_bounded_carriage.scad
./repo check
```

Observed results: both Python checks PASS, OpenSCAD export PASS, and
`./repo check` reports `OK: 108 objects`. Those controls are insufficient:
the checks parse shared scalar parameters and do not parse the SCAD solids to
assert slider y extent, per-state aperture placement, or a connected stop
support. The decisive counter-calculations above come directly from the CAD:
`field=30.48`, guide y span `4.90`, and `gate_slider()` is invoked only with
`state_y[2]`.

## Evidence classification and remaining gaps

The PASS items are CAD-derived/calculated nominal evidence. No physical
measurements, fabrication, tolerance, flatness, registration, force,
friction, wear, reader, timing, lateral-disturbance, or hardware-performance
claims were made. Tolerance stack-up and support design remain unresolved;
they cannot be closed by the current analytical checks.

This audit preserves the earlier E-037 rejection of the original
representation defect, but rejects the stronger repaired conclusion that the
five-state gate and complete frame load path are established. A future repair
must model a bounded translating gate/aperture for every state, use a slider
solid whose actual envelope is within the guides, and explicitly model the
stop-plate support to the frame before another integration decision.
