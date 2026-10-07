---
status: complete
builds-on: [E-035, ADR-008, E-031]
---

# E-037: LAB-123 repair of the E-035 A-010 carriage gate

## Revised verdict

**PASS, bounded analytical/CAD gate; physical and integration gates remain
open.** The rejected model used z both as state index and load axis, placing
the carriage outside its guides and separating the follower shoulder from the
stop. The repaired model uses one explicit shared datum: x/y locate a state
and z is the load axis. The gate, guide, carriage, follower, selected stop,
shoulder, and writer path now coincide for the single-state S2 section; all
five state positions are generated from the same parameter set.

| Gate | Verdict | Evidence boundary |
|---|---|---|
| Aperture | **PASS (calculated/CAD)** | Ø1.20 follower in 3.00 square aperture, centered at the selected shared x/y datum; 0.90 mm radial clearance. |
| Guide/carriage envelope | **PASS (calculated/CAD)** | 4.00 mm carriage within 4.50 mm guide x envelope; 4.20 x 4.60 slider envelope within 4.50 x 4.90 guide datum. |
| Indexed stop | **PASS (calculated/CAD)** | Five stop bores at y = −1.60, −0.80, 0, 0.80, 1.60 mm, generated from `state_pitch` and `state_count`. |
| Follower load reaction | **PASS (calculated/CAD)** | Follower and Ø3.00 shoulder are coaxial with selected 1.60 mm stop bore; 0.20 mm bore radial clearance and 0.70 mm shoulder land. |
| Writer path | **PASS (calculated/CAD)** | Shared state positions give 3.20 mm travel and 3.60 mm bounded stroke including approaches; writer path is modeled, not just printed. |
| Clearances | **PASS (calculated/CAD)** | Gate, stop, guide, shoulder, and frame/cartridge clearances are positive at nominal dimensions. |

## Reproduction

```sh
python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_gate_check.py
PYTHONPATH=06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis python3 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/analysis/a010_carriage_independent_recheck.py
openscad --export-format binstl -o /dev/null 06-experiments/E-035-a-010-bounded-five-state-carriage-load-path-gate/cad/a010_bounded_carriage.scad
./repo check
```

The primary and independent checks parse the shared SCAD parameter file and
independently assert state reach, aperture/stop/shoulder clearances,
guide/carriage bounds, z-plane order, indexed-stop count, writer stroke, and
frame margin. This is calculated and CAD-derived evidence, not physical
validation. Tolerance stack, tilt, flatness, layer registration, force,
friction, wear, reader, timing, lateral disturbance, and E-032 measurement
remain **UNRESOLVED**.

## Disposition

This repair closes only the rejected E-037 representation defect. Do not
start fabrication or A-011 integration from this result. The separate
physical and system gates in ADR-008/E-031 remain required.
