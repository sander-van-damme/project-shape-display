---
status: active
builds-on: [E-017, E-018, DES-003]
---

# E-022: complete mask-generator boundary BOM sourcing screen

This is the active input record for the complete arbitrary-map boundary. It is
a catalogue/allowance calculation, not a supplier quote, procurement release,
or hardware validation. E-040 is the reconciled RFQ handoff; E-043 and E-045
are the later independent audits. Their detailed records supersede the
exploratory arithmetic below without changing this experiment's inputs.

## Boundary and evidence class

The boundary is the E-017/ADR-006 reusable four-plane medium, positive datum,
local clamp or transport, four independent writer channels, per-cell
verification/readback, bounded retry, and replacement/cleaning stock. This
screen chose local clamping as the priced boundary; cassette transport was not
silently costed.

The DES-003 shared-machine term is **$370.00** and is counted once. It covers
the inherited gantry, eight writer/reader head positions, controller, drivers,
power, loom, switches, fasteners, and spares. It is not a mask-generator-only
cost. All other non-sourced values are bounded allowances. Catalogue prices
and stock observations are sourced observations only; no physical measurement,
quote, life result, or compatibility result is implied.

## Canonical planning ranges

| Case | Calculation | Purchased total |
|---|---|---:|
| Inherited-reader reuse / low | `370+20+15+8+36+4.38+4.59+18.32+10` | **$486.29** |
| Inherited-reader reuse / base | `370+60+35+20+60+4.38+4.59+18.32+30` | **$602.29** |
| Inherited-reader reuse / high | `370+150+80+50+120+4.38+4.59+18.32+75` | **$872.29** |
| Fallback reader / low | reuse low `+6.40+2.90+10` | **$505.59** |
| Fallback reader / base | reuse base `+6.40+2.90+20` | **$631.59** |
| Fallback reader / high | reuse high `+6.40+2.90+40` | **$921.59** |

The fallback QRE1113/ADC/carrier rows are alternatives to inherited-reader
reuse, not additions. The observed catalogue subset is **$36.59**: two
DRV8833 ICs, one SC0915 controller, one MCP3008, eight QRE1113 sensors, and
eight example cables. The sourced subset does not close fit, timing, optical,
force, life, or availability gates.

## Disposition and traceability

**Product boundary: GO analytically / HOLD for integration. Purchased BOM:
HOLD; RFQ-ready, not procurement-ready.** The preferred reduction is reuse of
DES-003 readers only after the E-018 overlay and calibration/timing gates
close. Removing readback or serializing writing is rejected because it removes
fault observability or violates the inherited timing boundary.

The smallest closing action is one controlled RFQ/data package for five media
planes, one clamp/fiducial set, and four exact actuators, plus the eight-head
E-018 overlay and timing/calibration record. Media, clamp, actuator, and
reader compatibility remain unresolved; analytical acceptance does not prove
hardware performance.
