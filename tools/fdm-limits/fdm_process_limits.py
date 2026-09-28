#!/usr/bin/env python3
"""Sourced FDM process limits for the Shape Display program's target printer.

This module is the *analytic replacement for a print test*. Instead of printing
a coupon and measuring whether a feature survived, we compare the CAD geometry
against published FDM process limits and report PASS / FAIL / RISK with an
explicit evidence class per rule.

EVIDENCE CLASSES (per program policy, board directive DND-27)
-------------------------------------------------------------
    sourced fact  - vendor datasheet / published design guide / standard.
    assumption    - explicitly flagged engineering judgement.
    calculation   - derived from the sourced facts + the declared process.

Every number carries `evidence` and `source`. Nothing here is a measurement:
this module never claims physical validation.

TARGET PROCESS (declared in 06-experiments/test11_falsification_library/
PRINTABILITY_REPORT.md and the SCAD headers)
----------------------------------------------------------------------------
    Printer        Bambu Lab X1C
    Material       PLA
    Nozzle         0.4 mm
    Layer height   0.20 mm
    Perimeters     3
    Build volume   256 x 256 x 256 mm

REFERENCES
----------
    [R1] Protolabs Network (Hubs), "How to design parts for FDM 3D printing".
         https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
         - overhangs printable to ~45 deg without support; above 45 requires
           support (sourced fact).
         - bridges under 5 mm print cleanly; longer bridges sag (sourced fact).
         - vertical pins under 5 mm diameter print weak / may fail (sourced
           fact).
         - corners/edges have a radius equal to the nozzle diameter (sourced
           fact).
    [R2] Bambu Lab X1C product specification, build volume 256 x 256 x 256 mm.
         https://bambulab.com/en/x1 (sourced fact).
    [R3] Standard extrusion-width rule: a single extruded line at a 0.4 mm
         nozzle is ~0.4-0.5 mm wide; a feature narrower than one line cannot be
         printed reliably. Minimum self-supporting wall is therefore ~1x the
         extrusion width; a robust, infill-free feature is >= 2x (0.8 mm) and a
         load-bearing wall is conventionally >= 3x (1.2 mm) for a 0.4 mm nozzle
         / 3 perimeters (sourced fact + engineering convention -> labelled).
    [R4] FDM dimensional accuracy: typical +/-0.1 mm on a well-tuned printer,
         worse on small holes (undersize). Vendors publish ~+/-0.1 mm for X1C-
         class machines (assumption for the generic figure; see source note in
         `fits`).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProcessSpec:
    """The declared target FDM process. All limits derive from these."""

    printer: str = "Bambu Lab X1C"
    material: str = "PLA"
    nozzle_mm: float = 0.4
    layer_mm: float = 0.20
    perimeters: int = 3
    bed_x_mm: float = 256.0
    bed_y_mm: float = 256.0
    bed_z_mm: float = 256.0

    @property
    def extrusion_width_mm(self) -> float:
        """Typical extruded line width; ~1.0-1.25x nozzle for PLA (R3)."""
        return 1.1 * self.nozzle_mm

    @property
    def min_feature_mm(self) -> float:
        """Minimum reliable standalone feature (one extrusion line, R3)."""
        return self.extrusion_width_mm

    @property
    def min_wall_mm(self) -> float:
        """Robust infill-free wall: ~2 extrusion widths (R3)."""
        return 2.0 * self.extrusion_width_mm

    @property
    def recommended_wall_mm(self) -> float:
        """Load-bearing wall: `perimeters` lines wide (R3)."""
        return self.perimeters * self.extrusion_width_mm


# --- Published, per-rule limits -------------------------------------------------

MAX_UNSUPPORTED_OVERHANG_DEG = 45.0
MAX_BRIDGE_MM = 5.0
MIN_PIN_DIAMETER_MM = 5.0
DIM_ACCURACY_MM = 0.1


@dataclass(frozen=True)
class Rule:
    """One checkable process rule with provenance."""

    key: str
    label: str
    limit: float
    units: str
    evidence: str        # sourced fact | assumption | calculation
    source: str
    note: str = ""


def rules(spec: ProcessSpec = ProcessSpec()) -> list[Rule]:
    """Return the active rule set for the declared process, with citations."""
    return [
        Rule(
            key="min_feature",
            label="minimum standalone feature width",
            limit=round(spec.min_feature_mm, 3),
            units="mm",
            evidence="sourced fact",
            source="[R3] extrusion width = 1.1 x nozzle",
            note="narrower than one extrusion line cannot be printed reliably",
        ),
        Rule(
            key="min_wall",
            label="minimum robust wall (infill-free)",
            limit=round(spec.min_wall_mm, 3),
            units="mm",
            evidence="calculation",
            source="[R3] 2 x extrusion width",
            note="2 lines wide so the wall is solid and not a one-line waver",
        ),
        Rule(
            key="recommended_wall",
            label="load-bearing wall (perimeters wide)",
            limit=round(spec.recommended_wall_mm, 3),
            units="mm",
            evidence="calculation",
            source="[R3] perimeters x extrusion width",
            note="target for structural members",
        ),
        Rule(
            key="max_overhang",
            label="max unsupported overhang",
            limit=MAX_UNSUPPORTED_OVERHANG_DEG,
            units="deg",
            evidence="sourced fact",
            source="[R1] Protolabs/Hubs FDM design guide",
            note="above 45 deg requires support",
        ),
        Rule(
            key="max_bridge",
            label="max clean bridge span",
            limit=MAX_BRIDGE_MM,
            units="mm",
            evidence="sourced fact",
            source="[R1] Protolabs/Hubs FDM design guide",
            note="longer bridges sag or need support",
        ),
        Rule(
            key="min_pin_dia",
            label="minimum reliable printed pin diameter",
            limit=MIN_PIN_DIAMETER_MM,
            units="mm",
            evidence="sourced fact",
            source="[R1] Protolabs/Hubs FDM design guide",
            note="smaller pins print weak or fail; prefer inserted pins",
        ),
        Rule(
            key="dim_accuracy",
            label="dimensional accuracy (per axis)",
            limit=DIM_ACCURACY_MM,
            units="mm",
            evidence="assumption",
            source="[R4] generic X1C-class figure; not vendor-quoted here",
            note="use for clearance stack-ups; small holes are worse",
        ),
    ]


# --- Clearance / fit helper ----------------------------------------------------

@dataclass(frozen=True)
class ClearanceVerdict:
    nominal_mm: float
    pessimistic_mm: float
    required_mm: float
    ok: bool
    evidence: str
    source: str


def lateral_clearance(
    nominal_mm: float, required_mm: float, spec: ProcessSpec = ProcessSpec()
) -> ClearanceVerdict:
    """Worst-case free clearance after subtracting per-side print error.

    `nominal_mm` is the designed gap *across both faces* (the total void). Two
    printed faces each carry up to DIM_ACCURACY_MM of inward growth, so the
    pessimistic gap is nominal - 2 * accuracy. Compare against the required
    running clearance for the joint.
    """
    pessimistic = nominal_mm - 2.0 * DIM_ACCURACY_MM
    return ClearanceVerdict(
        nominal_mm=nominal_mm,
        pessimistic_mm=round(pessimistic, 3),
        required_mm=required_mm,
        ok=pessimistic >= required_mm,
        evidence="calculation",
        source="[R4] +/-0.1 mm per printed face -> worst-case stack",
    )


def rule_table_markdown(spec: ProcessSpec = ProcessSpec()) -> str:
    """Render the rule set as a markdown table (for reports/docs)."""
    lines = [
        "| Rule | Limit | Units | Evidence | Source |",
        "|---|---:|---|---|---|",
    ]
    for r in rules(spec):
        lines.append(
            f"| {r.label} | {r.limit} | {r.units} | {r.evidence} | {r.source} |"
        )
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover - manual inspection helper
    spec = ProcessSpec()
    print(f"Process: {spec.printer}, {spec.material}, "
          f"{spec.nozzle_mm} mm nozzle, {spec.layer_mm} mm layers\n")
    print(rule_table_markdown(spec))
