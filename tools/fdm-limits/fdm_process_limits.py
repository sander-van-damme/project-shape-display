#!/usr/bin/env python3
"""FDM screening limits; calculation, not physical validation.
R1: Protolabs/Hubs FDM guide (45° overhang, 5 mm bridge, small-pin caution):
https://www.hubs.com/knowledge-base/how-design-parts-fdm-3d-printing/
R2: X1C 256 mm build envelope: https://bambulab.com/en/x1
R3: extrusion width 1.1× nozzle; walls 2–3 lines: engineering conventions.
R4: ±0.1 mm per face: generic dimensional-accuracy assumption, not a vendor guarantee.
Declared process: X1C, PLA, 0.4 mm nozzle, 0.20 mm layers, three perimeters.
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
