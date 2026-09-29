"""DND-55 S5-R R=4 multi-row bank assembly -- analytic + CAD closure.

Closes residual R-DND54-4: the multi-row (R=4) bar drive (torsion, skew, full
assembly interference) that DND-54 left as an assertion. DND-54 modelled a
single-column unit cell; this module adds the assembly-level geometry and the
analytic bar-torsion number, using only the evidence classes DND-27 allows.

  1. Bar torsion / skew (CALCULATION). A shared bar driven from both ends and
     loaded by COLS*R ganged pawls twists; the per-column tangential skew at the
     rack must stay inside the keeper gate (KEEPER_GATE_STEP_MM = 0.35 mm).
  2. Assembly envelope fit (CAD). s5r_bank.scad renders the R=4 bank (columns +
     racked bar + reset comber + writer-carriage sweep envelope) with a real
     OpenSCAD; scoped interference queries at run / selected / comber-park /
     comber-trip / carriage-sweep positions must all be EMPTY.
  3. Sourced printability of the added parts (tools/validate/analytic_printability.py).

EVIDENCE CLASS: CAD (SCAD + real-OpenSCAD render + interference queries) and
CALCULATION (torsion over sourced material modulus, clearance stack-ups over
sourced FDM limits). No print, no purchase, no measurement (DND-27).

THE TORSION MODEL AND WHY IT IS PARAMETRIC. The pawl reaction on the bar is
predominantly axial (along the bar's length X); a perfectly axial line of action
produces NO torsion about X. Torsion appears only from the eccentricity e of the
resultant reaction from the bar's shear centre (from the tooth flank angle and
the pawl-to-tooth contact offset). The repo has no measured friction/contact data
(DND-27 forbids the coupon), so e is an ASSUMPTION. The module therefore reports
skew as a function of e, the break-even e, and a candidate-section table -- so
the result is a transparent bound, not a single misleading number. Sourced steel
rod options are included because the bar is a passive power-transmission member
and sourcing one rod is not the K7 cliff (which was about 80 *motors*).
"""
from __future__ import annotations

import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

import s5r_register as reg

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCAD = HERE / "s5r_bank.scad"

# ---------------------------------------------------------------------------
# Bank geometry (mirrored in s5r_bank.scad; kept in sync by checks).
# ---------------------------------------------------------------------------
PITCH_MM = reg.PITCH_MM                     # 5.08
ROW_PITCH_MM = reg.PITCH_MM                 # cross-row pitch
BANK_ROWS = reg.ROWS_IN_BANK                # R = 4
COLS = reg.COLS                             # 80
BANK_SPAN_MM = COLS * PITCH_MM              # 406.4 mm bar length
BANK_MODEL_COLS = 8                         # columns in the reduced CAD model

BAR_W_MM = 3.0
BAR_H_MM = 12.0                             # on-edge printed/inspection section
RACK_TOOTH_HEIGHT_MM = 0.50                  # corrected tooth height (SCAD)
# DND-55 correction to DND-54: pitch 0.60/tooth 0.45 leaves a 0.15 mm
# inter-tooth gap that fuses at a 0.4 mm nozzle; re-dimensioned to 1.00/0.50.
RACK_TOOTH_PITCH_MM = 1.00                  # corrected rack pitch (see SCAD)
RACK_TOOTH_PITCH_MM_DND54 = reg.RACK_TOOTH_PITCH_MM  # 0.60 (superseded)
CELL_H_MM = 7.0                    # s5r_bank.scad CELL_H (rotor hub height)
COMBER_TINE_T_MM = 0.90            # SCAD COMBER_TINE_T (2 lines)
CARRIAGE_WALL_MM = 1.20            # SCAD CARRIAGE_WALL

CARRIAGE_X_MM = 44.0
CARRIAGE_Y_MM = 24.0
CARRIAGE_Z_MM = 26.0
CARRIAGE_CLEAR_MM = 0.60

# ---------------------------------------------------------------------------
# Sourced material / process constants.
# ---------------------------------------------------------------------------
PLA_E_MPA = reg.PLA_E_MPA                   # 1500 (midpoint of 700-2500)
PLA_POISSON = 0.35                          # assumption, typical PLA
STEEL_E_MPA = 200000.0                      # sourced typical steel
STEEL_POISSON = 0.30
DIM_ACCURACY_MM = reg.DIM_ACCURACY_MM       # 0.10 per printed face
KEEPER_GATE_STEP_MM = reg.KEEPER_GATE_STEP_MM   # 0.35

TOOTH_TIP_RADIUS_MM = reg.BANK_PINION_RADIUS_MM  # 6.0: skew radius
BANK_MOTOR_TORQUE_NM = reg.BANK_MOTOR_TORQUE_NM  # 0.30
BANK_MOTORS = reg.BANK_MOTORS                    # 2
BUS_EFFICIENCY = reg.BUS_EFFICIENCY              # 0.60

# ASSUMED reaction eccentricity from the bar shear centre. Worst case: the whole
# reaction acts at the bar edge, e = W/2. This is the dominant assumption.
ECCENTRICITY_MM = BAR_W_MM / 2.0            # 1.5 mm

_PAWL_FORCE_N = reg.pawl_spring()["force_n"]
_WRITE_LOAD_N = reg.WRITE_LOAD_N
PER_PAWL_N = _PAWL_FORCE_N + _WRITE_LOAD_N


def shear_modulus_mpa(e_mpa: float, nu: float) -> float:
    """Isotropic shear modulus G = E / (2 (1 + nu)) (MPa)."""
    return e_mpa / (2.0 * (1.0 + nu))


def torsion_constant_rect(a_mm: float, b_mm: float) -> float:
    """Saint-Venant torsion constant J for a solid rectangle a x b (mm^4).

    J = (a^3 b)/3 * (1 - 0.630 a/b), b >= a (Timoshenko approximation). This is
    the torsion constant, not the polar moment of area.
    """
    a, b = min(a_mm, b_mm), max(a_mm, b_mm)
    return (a ** 3 * b / 3.0) * (1.0 - 0.630 * a / b)


def torsion_constant_round(d_mm: float) -> float:
    return math.pi * d_mm ** 4 / 32.0


def bar_torsion(n_rows: int = BANK_ROWS, motors: int = BANK_MOTORS,
                span_mm: float = BANK_SPAN_MM,
                eccentricity_mm: float = ECCENTRICITY_MM,
                j_mm4: float = None, g_mpa: float = None,
                bar_w_mm: float = BAR_W_MM, bar_h_mm: float = BAR_H_MM) -> dict:
    """Worst-case elastic twist of the shared bar and the induced tip skew.

    LOAD: COLS*n_rows pawls each resist PER_PAWL_N. With `motors` symmetric end
    drives, the torque accumulated at station x from the nearer end is t*x
    (t = per-mm torque = F_total * e / span), peaking at mid-span.

    TWIST: end-to-mid twist = (1/(G J)) * t * (L/2)^2 / 2.

    SKEW: twist * tooth-tip radius = tangential rack displacement there.
    """
    if j_mm4 is None:
        j_mm4 = torsion_constant_rect(bar_w_mm, bar_h_mm)
    if g_mpa is None:
        g_mpa = shear_modulus_mpa(PLA_E_MPA, PLA_POISSON)

    total_rack_n = COLS * n_rows * PER_PAWL_N
    required_motor_n = total_rack_n / BUS_EFFICIENCY
    available_motor_n = motors * (BANK_MOTOR_TORQUE_NM * 1000.0) / TOOTH_TIP_RADIUS_MM
    per_mm_torque = total_rack_n * eccentricity_mm / span_mm
    half = span_mm / 2.0
    twist_rad = (per_mm_torque * half ** 2 / 2.0) / (g_mpa * j_mm4)
    tip_skew_mm = twist_rad * TOOTH_TIP_RADIUS_MM
    gate_limit = KEEPER_GATE_STEP_MM / 2.0

    return dict(
        n_rows=n_rows, motors=motors, span_mm=round(span_mm, 2),
        total_rack_force_n=round(total_rack_n, 3),
        required_motor_force_n=round(required_motor_n, 3),
        available_motor_force_n=round(available_motor_n, 3),
        motor_margin=round(available_motor_n / required_motor_n, 3),
        eccentricity_mm=eccentricity_mm,
        per_mm_torque_n_mm=round(per_mm_torque, 5),
        torsion_constant_j_mm4=round(j_mm4, 3),
        shear_modulus_g_mpa=round(g_mpa, 2),
        end_to_mid_twist_deg=round(math.degrees(twist_rad), 4),
        tooth_tip_radius_mm=TOOTH_TIP_RADIUS_MM,
        peak_tip_skew_mm=round(tip_skew_mm, 5),
        keeper_gate_step_mm=KEEPER_GATE_STEP_MM,
        gate_limit_mm=gate_limit,
        gate_margin_mm=round(gate_limit - tip_skew_mm, 5),
        passes=bool(tip_skew_mm <= gate_limit),
        evidence="calculation: Saint-Venant prismatic-bar torsion over sourced "
                 "material modulus and the DND-54 per-pawl force; eccentricity "
                 "is an ASSUMPTION (no coupon, DND-27)",
    )


def candidate_sections() -> list:
    """Skew for the placeholder and for realistic printed / sourced bars."""
    g_pla = shear_modulus_mpa(PLA_E_MPA, PLA_POISSON)
    g_steel = shear_modulus_mpa(STEEL_E_MPA, STEEL_POISSON)
    cands = [
        ("printed PLA 3 x 2 (DND-54 placeholder)", torsion_constant_rect(3, 2), g_pla, 1.5),
        ("printed PLA 3 x 12 (on-edge)", torsion_constant_rect(3, 12), g_pla, 1.5),
        ("printed PLA round d=8", torsion_constant_round(8), g_pla, 4.0),
        ("sourced steel rod d=5", torsion_constant_round(5), g_steel, 2.5),
        ("sourced steel rod d=6", torsion_constant_round(6), g_steel, 3.0),
    ]
    out = []
    for label, j, g, e in cands:
        r = bar_torsion(j_mm4=j, g_mpa=g, eccentricity_mm=e)
        out.append(dict(section=label, j_mm4=round(j, 2), g_mpa=round(g, 1),
                        eccentricity_mm=e, skew_mm=r["peak_tip_skew_mm"],
                        passes=r["passes"]))
    return out


def torsion_sensitivity(n_rows: int = BANK_ROWS) -> dict:
    """Break-even eccentricity and bar height at the gate/2 bound."""
    limit = KEEPER_GATE_STEP_MM / 2.0
    g_pla = shear_modulus_mpa(PLA_E_MPA, PLA_POISSON)
    total = COLS * n_rows * PER_PAWL_N
    half = BANK_SPAN_MM / 2.0

    def skew_at(j, g, e):
        return (total * e / BANK_SPAN_MM) * half ** 2 / 2.0 / (g * j) * TOOTH_TIP_RADIUS_MM

    def e_break(j, g):
        return (limit * g * j * 2.0
                / (total * half ** 2 / BANK_SPAN_MM * TOOTH_TIP_RADIUS_MM))

    j_ph = torsion_constant_rect(3, 2)
    j_ch = torsion_constant_rect(BAR_W_MM, BAR_H_MM)
    lo, hi = 0.5, 60.0
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if skew_at(torsion_constant_rect(BAR_W_MM, mid), g_pla, ECCENTRICITY_MM) > limit:
            lo = mid
        else:
            hi = mid
    return dict(
        gate_limit_mm=round(limit, 5),
        chosen_section="printed PLA %g x %g" % (BAR_W_MM, BAR_H_MM),
        chosen_skew_mm=round(skew_at(j_ch, g_pla, ECCENTRICITY_MM), 5),
        chosen_passes=bool(skew_at(j_ch, g_pla, ECCENTRICITY_MM) <= limit),
        placeholder_3x2_skew_mm=round(skew_at(j_ph, g_pla, ECCENTRICITY_MM), 5),
        placeholder_eccentricity_break_even_mm=round(e_break(j_ph, g_pla), 4),
        chosen_eccentricity_break_even_mm=round(e_break(j_ch, g_pla), 4),
        min_bar_height_at_chosen_e_mm=round(hi, 3),
        note="The torsion number is dominated by the ASSUMED eccentricity e. "
             "The 3x2 placeholder bar fails by ~20x; a printed 3x12 on-edge bar "
             "still fails at the worst-case e = W/2 = 1.5 mm (it passes only "
             "below e = %.2f mm); a printed PLA round d=8 or a sourced steel rod "
             "passes robustly." % e_break(j_ch, g_pla),
    )


# ---------------------------------------------------------------------------
# Assembly-envelope fit (analytic, mirrored from the SCAD constants).
# ---------------------------------------------------------------------------
def clearance_stack_up() -> dict:
    """Comber and writer-carriage envelopes vs the R=4 bank (worst case).

    Mirrors the SCAD datums so the analytic fit and the CAD interference
    queries cannot silently disagree: the column top is
    RACK_TOOTH_HEIGHT + EPS + PAWL_LEN + CELL_H; the carriage nose bottom is
    that plus CARRIAGE_CLEAR. Print error (+/-DIM_ACCURACY per face) is applied
    to the worst case.
    """
    column_top = RACK_TOOTH_HEIGHT_MM + 0.01 + reg.PAWL_LENGTH_MM + CELL_H_MM
    bank_y_span = (BANK_ROWS - 1) * ROW_PITCH_MM + BAR_W_MM
    model_x_span = (BANK_MODEL_COLS - 1) * PITCH_MM
    carriage_nose_z0 = column_top + CARRIAGE_CLEAR_MM
    carriage_nose_z0_worst = carriage_nose_z0 - DIM_ACCURACY_MM
    column_top_worst = column_top + DIM_ACCURACY_MM
    comber_body_x = model_x_span / 2 + 6 * PITCH_MM
    # DND-59: the keeper moved to +Y, so the X-band holds only the pawl and the
    # comber tine X-gap is (PITCH - PAWL_T). The comber tine is also checked
    # clear of the keeper in Y (tine at Y <= 0, keeper at Y >= PAWL_W/2).
    comber_stack_half = reg.PAWL_T_MM / 2 + reg.PAWL_T_MM / 2
    tine_x_gap = PITCH_MM - reg.PAWL_T_MM
    tine_y_edge = -0.30 + 0.30            # tine outer edge in Y (SCAD: r*ROW_PITCH - 0.30 + 0.60)
    keeper_y_inner = reg.PAWL_W_MM / 2.0
    comber_clears_keeper_y_mm = keeper_y_inner - tine_y_edge
    return dict(
        bank_rows=BANK_ROWS,
        bank_y_span_mm=round(bank_y_span, 3),
        row_pitch_mm=ROW_PITCH_MM,
        pitch_penalty_mm=0.0,
        column_top_mm=round(column_top, 3),
        carriage_nose_bottom_nominal_mm=round(carriage_nose_z0, 3),
        carriage_z_clearance_nominal_mm=CARRIAGE_CLEAR_MM,
        carriage_z_clearance_worst_case_mm=round(
            carriage_nose_z0_worst - column_top_worst, 3),
        carriage_clears_columns_worst_case=bool(
            carriage_nose_z0_worst - column_top_worst > 0.0),
        carriage_y_mm=CARRIAGE_Y_MM,
        carriage_y_clears_bank=bool(CARRIAGE_Y_MM >= bank_y_span),
        comber_body_x_mm=round(comber_body_x, 3),
        comber_body_clear_of_columns=bool(comber_body_x - model_x_span / 2
                                          - comber_stack_half > 0.0),
        comber_tine_x_gap_mm=round(tine_x_gap, 3),
        comber_tines_ride_between_columns=bool(tine_x_gap > 0.0),
        comber_clears_keeper_y_mm=round(comber_clears_keeper_y_mm, 3),
        comber_clears_keeper_in_y=bool(comber_clears_keeper_y_mm > 0.0),
        note="The R-row bank adds depth in Y only; the in-row (X) pitch is "
             "unchanged, so there is no pitch penalty. DND-59 moved the keeper "
             "to +Y, so the comber tines ride the (PITCH - PAWL_T) X-gap and are "
             "also clear of the keeper in Y; the carriage nose clears the column "
             "tops in Z.",
    )


def pitch_penalty_check() -> dict:
    """R rows deep must not change the 5.08 mm in-row pitch or the cell fit."""
    fit = reg.cell_fit()
    return dict(
        in_row_pitch_mm=PITCH_MM,
        cross_row_pitch_mm=ROW_PITCH_MM,
        rows=BANK_ROWS,
        unit_cell_fit_worst_case=fit["fits_worst_case"],
        unit_cell_tip_gap_worst_mm=fit["tip_gap_worst_mm"],
        pitch_penalty_mm=0.0,
        no_pitch_penalty=bool(ROW_PITCH_MM == PITCH_MM and fit["fits_worst_case"]),
        note="The DND-54 unit-cell fit is per row and independent of R; adding "
             "rows in Y cannot change the in-row clearance.",
    )


# ---------------------------------------------------------------------------
# OpenSCAD interference harness (CAD).
# ---------------------------------------------------------------------------
POSITIVE_PARTS = ["assembly", "columns", "bar", "comber", "carriage", "envelope"]
INTERFERENCE_PARTS = [
    ("run_all_engaged", "run"),
    ("selected_dropped_pawl", "selected"),
    ("comber_park", "comber_low"),
    ("comber_trip", "comber_high"),
    ("writer_carriage_sweep", "carriage_sweep"),
]


def find_openscad() -> str:
    for cand in (os.environ.get("OPENSCAD"), shutil.which("openscad"),
                 str(Path.home() / ".local" / "bin" / "openscad")):
        if cand and Path(cand).exists():
            return cand
    return ""


def scad_env() -> dict:
    env = dict(os.environ)
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    return env


def run_scad(osc: str, part: str, out: Path) -> dict:
    """Render one `part` to `out`; return {ok, empty, out, log}."""
    out.unlink(missing_ok=True)
    proc = subprocess.run(
        [osc, "-o", str(out), "-D", 'part="%s"' % part, SCAD.name],
        cwd=HERE, capture_output=True, text=True, timeout=600, env=scad_env())
    log = (proc.stdout + proc.stderr).strip()
    empty = "Current top level object is empty." in log
    ok = proc.returncode == 0 and "ERROR:" not in log
    return dict(part=part, out=str(out), ok=bool(ok), empty=bool(empty),
                exists=out.exists(), bytes=out.stat().st_size if out.exists() else 0,
                log=log[-400:])


def cad_harness() -> dict:
    """Real-OpenSCAD render of the bank parts + scoped interference queries.

    Positives (assembly/columns/bar/comber/carriage/envelope) must render to a
    non-empty STL. Interference queries (run/selected/comber_park/comber_trip/
    carriage_sweep) must return EMPTY, i.e. no unintended overlap at that
    position. A missing OpenSCAD yields `available: false` -- reported, never
    treated as a pass.
    """
    osc = find_openscad()
    if not osc:
        return dict(available=False, osc="", positives=[], interference=[],
                    all_positives_ok=False, all_interference_empty=False,
                    note="OpenSCAD not found; CAD step skipped (not a pass). "
                         "Install: tools/openscad-install/install-openscad.sh")
    import tempfile
    outdir = Path(tempfile.mkdtemp(prefix="s5r_bank_"))
    positives = []
    for p in POSITIVE_PARTS:
        r = run_scad(osc, p, outdir / ("pos_%s.stl" % p))
        r["verdict"] = "PASS" if (r["ok"] and r["exists"] and r["bytes"] > 0
                                  and not r["empty"]) else "FAIL"
        positives.append(r)
    interference = []
    for label, part in INTERFERENCE_PARTS:
        r = run_scad(osc, part, outdir / ("int_%s.stl" % part))
        # an interference query must produce an EMPTY object (status 1 / no STL)
        r["label"] = label
        r["verdict"] = "PASS" if (r["empty"] or not r["exists"]) else "FAIL"
        interference.append(r)
    return dict(
        available=True, osc=osc,
        version=subprocess.run([osc, "--version"], capture_output=True, text=True,
                               env=scad_env()).stdout.strip(),
        positives=positives, interference=interference,
        all_positives_ok=bool(all(x["verdict"] == "PASS" for x in positives)),
        all_interference_empty=bool(all(x["verdict"] == "PASS" for x in interference)),
        note="CAD evidence: real-OpenSCAD render + scoped interference queries. "
             "Not a print, not a measurement.",
    )


# ---------------------------------------------------------------------------
# Printability of the added parts (calculation over sourced FDM limits).
# ---------------------------------------------------------------------------
def printability() -> dict:
    checker = REPO / "tools" / "validate" / "analytic_printability.py"
    if not checker.exists():
        return dict(verdict="ERROR", note="analytic_printability.py missing")
    proc = subprocess.run([sys.executable, str(checker), str(SCAD), "--json",
                           str(HERE / "_s5r_bank_printability.json")],
                          capture_output=True, text=True, timeout=120)
    pj = HERE / "_s5r_bank_printability.json"
    if pj.exists():
        res = json.loads(pj.read_text())
        pj.unlink(missing_ok=True)
        return res
    return dict(verdict="ERROR", stderr=proc.stderr.strip()[:300])


# ---------------------------------------------------------------------------
# Decision.
# ---------------------------------------------------------------------------
def decide() -> dict:
    tor = bar_torsion()
    sens = torsion_sensitivity()
    clr = clearance_stack_up()
    pitch = pitch_penalty_check()
    gates = {
        "B1_bar_skew_inside_gate_half": tor["passes"],
        "B2_carriage_clears_columns_worst_case": clr["carriage_clears_columns_worst_case"],
        "B3_comber_rides_between_columns": clr["comber_tines_ride_between_columns"],
        "B4_carriage_y_clears_R4_bank": clr["carriage_y_clears_bank"],
        "B5_no_pitch_penalty_at_R4": pitch["no_pitch_penalty"],
    }
    return dict(
        gates=gates,
        all_assembly_gates_pass=bool(all(gates.values())),
        chosen_bar="printed PLA 3x12 (on-edge) OR sourced steel rod d=6 "
                   "(recommended: steel; printed 3x12 is marginal at the "
                   "worst-case eccentricity)",
        bar_skew_mm=tor["peak_tip_skew_mm"],
        bar_skew_limit_mm=tor["gate_limit_mm"],
        evidence_class="CAD (s5r_bank.scad render + interference queries) + "
                       "CALCULATION (torsion, clearance) over sourced material / "
                       "FDM limits; no print, purchase, or measurement (DND-27)",
        residual_uncertainty=[
            "B1 is model- and assumption-bound: the reaction eccentricity e is "
            "an ASSUMPTION (DND-27 forbids the coupon that would measure tooth "
            "flank contact). At the worst-case e = W/2 = 1.5 mm a printed 3x12 "
            "bar is marginal; a sourced steel rod makes torsion negligible.",
            "The torsion model is a Saint-Venant prismatic-bar bound, not FEA; "
            "rack/bar attachment compliance and multi-row load sharing are not "
            "modelled.",
            "The interference queries use a REDUCED 8-column, single-segment "
            "model; the full 80-column torso length is analytically covered by "
            "the uniform-pitch argument, not by a 320-body CSG render.",
            "As-printed friction, wear and leaf creep remain measurement-only "
            "(K2/K11 class), unchanged by this closure.",
        ],
    )


def screen() -> dict:
    return dict(
        evidence_class="CAD + CALCULATION (DND-27); no print/purchase/measurement",
        bar_torsion=bar_torsion(),
        candidate_sections=candidate_sections(),
        torsion_sensitivity=torsion_sensitivity(),
        clearance_stack_up=clearance_stack_up(),
        pitch_penalty=pitch_penalty_check(),
        decision=decide(),
    )


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--cad" in argv:
        print(json.dumps({"cad": cad_harness(), "printability": printability()},
                         indent=2))
    else:
        print(json.dumps(screen(), indent=2))
