# Software-only geometry validation harness

This directory holds the reproducible, container-runnable harness that replaced
the physical print test for the Shape Display program (board directive
[DND-27](/DND/issues/DND-27)). It renders the CAD fixtures with a real OpenSCAD,
validates the meshes, and applies a sourced analytic printability gate.

## Contents

| File | Purpose |
|---|---|
| `validate_geometry.py` | The unified harness: tool check → render → mesh → printability. |
| `analytic_printability.py` | Analytic FDM pass/RISK/FAIL table vs sourced process limits for a coupon `.scad`. |

Companion tooling:

| Path | Purpose |
|---|---|
| [`../openscad-install/install-openscad.sh`](../openscad-install/install-openscad.sh) | Rootless OpenSCAD installer for the dev container. |
| [`../openscad-install/TOOL_AVAILABILITY.md`](../openscad-install/TOOL_AVAILABILITY.md) | OpenSCAD version/method/evidence record. |
| [`../fdm-limits/fdm_process_limits.py`](../fdm-limits/fdm_process_limits.py) | Sourced FDM process-limit parameter module. |
| [`../fdm-limits/SOURCES.md`](../fdm-limits/SOURCES.md) | Citations and evidence classes for every limit. |

## Run it

```sh
# full run (renders + validates + printability)
python tools/validate/validate_geometry.py

# if OpenSCAD is not installed yet:
tools/openscad-install/install-openscad.sh
export PATH="$HOME/.local/bin:$PATH"

# machine-readable record
python tools/validate/validate_geometry.py --json /tmp/harness.json

# printability table alone against any coupon .scad
python tools/validate/analytic_printability.py \
    06-experiments/test11_shared_drive_gate_analysis/selector_fanout_coupon.scad
```

Exit code is non-zero only on a **hard harness error** (render failure or
unreadable mesh). A printability `FAIL` is reported as a *design* finding and
does not fail the harness — the harness's job is to produce the evidence, not to
hide a design risk.

The standalone `analytic_printability.py` follows the same rule: it exits `0`
when it produced a verdict (`PASS`/`RISK`/`FAIL`), and `2` only if it could not
run. Pass `--fail-on-design-fail` to opt into a non-zero exit on a design `FAIL`
when a downstream stage needs to gate on it. Neither path ever claims a print.

## Evidence classes (read this before quoting any number)

- **render** and **mesh validate** → **CAD** evidence: the geometry parses,
  produces a non-empty STL, has finite vertices and fits the X1C bed.
- **analytic printability** → **calculation** over CAD-declared parameters.
- **Nothing here is a print and nothing here is a physical measurement.**
  Physical print tests are out of scope by policy; residual uncertainty is
  printed alongside every result.

## What this harness does *not* do

- It is not a slicer: seam placement, thin-wall detection and bridging
  parameters are not modelled.
- It is not a printer: machine calibration, filament lot and environment are not
  modelled.
- It does not validate function, fit or mechanism behaviour — only
  geometry-vs-process risk.

## CI

`.github/workflows/ci.yml` runs `validate_geometry.py` in a dedicated job with
OpenSCAD installed via apt. That is the x86_64 CI path; the rootless installer
above is the equivalent path inside the container.
