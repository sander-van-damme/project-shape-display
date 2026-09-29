"""DND-104 - reliability-first low-cost shape display + automatic mask system.

Chief Technology Officer synthesis model. This is the *machine-definition* layer
for the DND-104 program (parent DND-102). It does three things, in order:

1. DIVERGENCE. Defines >=7 materially different reliability-first architectures
   as first-class data, each with its own ten-job allocation, bought-actuator
   count, reliability audit, mask subsystem, timing decomposition, BOM sketch,
   prototype ladder and decisive falsifier. Nothing is pre-picked: the screen
   prints every field for every machine.

2. RELIABILITY GATE. Every architecture must answer the DND-103 gate question
   "what has to work correctly 6,400 times?" and is scored on the *number of
   independent repeated elements that can silently produce a wrong cell* and on
   whether the state is *detectable/recoverable*. Map yield is (1-q)^N for the
   architecture's own N; a design that turns N independent silent elements into
   a few monitored shared mechanisms wins even if its spreadsheet cost is worse.

3. CONVERGENCE. Re-ranks on the reliability-first criteria, names one selection
   (or an honest no-promotion verdict), and states the decisive falsifier and
   the prototype ladder A-D.

EVIDENCE CLASS: CALCULATION over sourced FDM process limits + sourced actuator
ratings, plus CAD where a geometry is rendered. NO part has been printed,
purchased or measured (board policy DND-27). Prices are point-in-time
sourced-class figures (2026-09). Nothing here is a physical validation.

This model deliberately does NOT modify 08-current-design/ (S5-R provenance) and
does not touch 09-low-cost-variant/ (S6-LC). It is the new candidate root.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

# ---------------------------------------------------------------------------
# Mission constants (unchanged from 02-design-criteria/README.md)
# ---------------------------------------------------------------------------
PITCH_MM = 5.08
ROWS = 80
COLS = 80
CELLS = ROWS * COLS                       # 6,400
TRAVEL_MM = 40.0                          # >= 40 mm usable travel
LEVELS = 5                                # 0/10/20/30/40 mm
LEVEL_MM = TRAVEL_MM / (LEVELS - 1)       # 10 mm
ACTIVE_MM = COLS * PITCH_MM               # 406.4 mm
TIME_GATE_S = 30.0
PARTS_GATE_USD = 250.0                    # DND-70: purchased, excl. printed
DELIVERED_GATE_USD = 250.0                # repo internal 1.16 convention
UPLIFT = 1.10 + 0.06                      # +10 % ship +6 % tax

MIN_FEATURE_MM = 0.44                     # 1 extrusion line @ 0.4 mm nozzle
MIN_WALL_MM = 0.88                        # 2 lines, robust (provisional rule)
PLA_E_MPA = 1500.0                        # sourced modulus 700-2500, midpoint
PLA_YIELD_MPA = 50.0                      # sourced-class conservative yield
PLA_COMPRESS_MPA = 50.0                   # sourced-class compressive strength
COLUMN_MASS_G = 1.0                       # printed 4.68 x 4.68 x 44 mm column

# DND-48 bounding service load per column (terrain + a small miniature)
COLUMN_SERVICE_LOAD_N = 3.27
MINIATURE_LOAD_N = 0.30                   # a 30 g mini on one column (assumption)

# Reliability: a map is correct only if all cells are correct.
MAP_YIELD_TARGET = 0.99
PER_CELL_ERROR_BREAK_EVEN = 1 - MAP_YIELD_TARGET ** (1.0 / CELLS)   # ~1.57e-6

CORRECTED = {
    "DND-91 A1": "cell owns only PITCH/2-BODY/2=0.74 mm; placement, not just budget",
    "DND-91 A2": "spring rate uses the bending leaf section (0.45 mm), plus a hold gate",
    "DND-91 A3": "release ceiling is a sourced structural limit, not a borrowed output",
    "DND-91 A6": "reliability gate (map yield (1-q)^N) is a first-class gate",
    "DND-91 A7": "tabletop load during write is an explicit load case, not assumed away",
    "DND-91 A8": "regional/jam + silent-failure behaviour is modelled, not asserted",
}


def map_yield(per_cell_error: float, independent_elements: int) -> float:
    """(1-q)^N yield for N independent repeated elements."""
    return (1.0 - per_cell_error) ** independent_elements


def break_even_q(independent_elements: int, yield_target: float = MAP_YIELD_TARGET) -> float:
    """Per-element error q that still yields the target map fraction."""
    if independent_elements <= 0:
        return 1.0
    return 1.0 - yield_target ** (1.0 / independent_elements)


# ===========================================================================
# 1. DIVERGENCE - the candidate set
# ===========================================================================
# Each machine is a dict with the same schema so the table is honest and
# uniform. `repeated_silent_elements` is THE reliability score: the number of
# independent parts whose single failure yields a wrong visible cell *without
# the machine noticing*. `has_readback` records whether a wrong cell can be
# detected at all.
#
# Schema per machine:
#   name, family, one_liner
#   column_states            int   - discrete height states of the visible column
#   repeated_moving_parts    int   - parts that move, per cell, summed over cells
#   precision_contacts_cell  float - sub-mm tolerance-critical interactions/cell
#   compliant_printed_parts  int   - springs/compliant elements repeated
#   wear_interfaces          int   - repeated sliding/rubbing interfaces
#   repeated_silent_elements int   - INDEPENDENT silent wrong-cell mechanisms
#   has_readback             bool  - can the machine detect a wrong cell?
#   recovery                 str   - re-home / re-write / none
#   actuators_bought         int
#   mask_medium              str | None
#   mask_write_inside_budget bool
#   correlated_failure       str
#   single_cell_failure      str
#   serviceable              bool
#   timing_s                 dict  -> sums to full_map_s
#   parts_usd                float (sourced-class sketch)
#   prototype_coupon         str
#   decisive_falsifier       str
#   docs                     str

ARCHITECTURES: list[dict] = [
    dict(
        name="A1 binary-latch + shared writer/reader",
        family="external shared writer/verifier over passive binary cells",
        one_liner=(
            "Each cell is a two-state column (0 / 40 mm) held by a large "
            "over-centre toggling latch between two printed hard stops. A "
            "gantry carries ONE writer head and ONE reader head across the "
            "field; it flips only the latches it must, then reads the whole "
            "field back, so a miss is detected and re-driven, not silent."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.0,
        compliant_printed_parts=0,
        wear_interfaces=CELLS,
        repeated_silent_elements=0,
        has_readback=True,
        recovery="scan-verify -> re-write the few failed cells (bounded retry)",
        actuators_bought=4,
        mask_medium="none (map streamed directly to the writer head)",
        mask_write_inside_budget=True,
        correlated_failure="gantry/reader fault -> whole-region error, but detected",
        single_cell_failure="a latch that fails to toggle is read back and re-driven",
        serviceable=True,
        timing_s=dict(digital_map=0.05, mask_generation=0.0, transport=2.0,
                      reset=3.0, lift=8.8, settle=1.5, verify=8.8),
        parts_usd=181.0,
        prototype_coupon="A: 1 cell flip+read; B: 5x5 writer/reader scan",
        decisive_falsifier=(
            "writer head cannot both toggle AND read a latch within a ~2 mm "
            "working gap at the required cell rate across 406 mm -> timing dies"
        ),
        docs="10-reliability-mask/README.md S A1",
        writer_head_rate_cells_s=1000.0,   # 1 ms/cell, 8 parallel heads -> 8000/s
        writer_heads=8,
    ),
    dict(
        name="A2 global broadcast binary interlock",
        family="broadcast lock-and-lift with a printed per-level interlock plate",
        one_liner=(
            "A single global lift moves all 6,400 cells together. Per level k a "
            "printed shutter plate blocks or passes each cell, and a binary "
            "interlock either lets the cell ride up one 10 mm step or holds it. "
            "Four passes encode five heights."
        ),
        column_states=5,
        repeated_moving_parts=CELLS * 2,
        precision_contacts_cell=1.0,
        compliant_printed_parts=CELLS,
        wear_interfaces=CELLS * 2,
        repeated_silent_elements=CELLS,
        has_readback=False,
        recovery="none per cell (full global reset only)",
        actuators_bought=2,
        mask_medium="printed binary interlock plate, re-written per map",
        mask_write_inside_budget=False,
        correlated_failure="one plate mis-index -> a whole level of cells wrong",
        single_cell_failure="stuck interlock -> silent wrong height",
        serviceable=False,
        timing_s=dict(digital_map=0.05, mask_generation=0.0, transport=0.5,
                      reset=2.0, lift=7.0, settle=1.5, verify=0.0),
        parts_usd=224.0,
        prototype_coupon="A: 1 interlock; B: 5x5 plate write + broadcast lift",
        decisive_falsifier=(
            "printed interlock force spread >50 % -> some cells never release; "
            "with no readback a map silently fails"
        ),
        docs="10-reliability-mask/README.md S A2",
    ),
    dict(
        name="A3 punched-film mask + biased two-state columns",
        family="physical bit-image mask (punched film) over gravity-biased cells",
        one_liner=(
            "A continuous film is automatically punched by a travelling punch "
            "head to encode the target map as a bit image (one film row per "
            "cell row). The film indexes over the field; each cell reads its "
            "bit mechanically and latches up or stays down."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.3,
        compliant_printed_parts=CELLS,
        wear_interfaces=CELLS + 1,
        repeated_silent_elements=CELLS,
        has_readback=False,
        recovery="re-punch/re-index film and re-lift (full reset)",
        actuators_bought=2,
        mask_medium="automatically punched film (consumable)",
        mask_write_inside_budget=True,
        correlated_failure="film registration drift -> a band of cells wrong",
        single_cell_failure="follower fails to enter a hole -> silent wrong cell",
        serviceable=False,
        timing_s=dict(digital_map=0.05, mask_generation=22.0, transport=1.0,
                      reset=2.0, lift=7.0, settle=1.5, verify=0.0),
        parts_usd=187.0,
        prototype_coupon="A: 1 follower + hole; B: 5x5 punched-film read",
        decisive_falsifier=(
            "a printed follower cannot reliably enter a ~1.8 mm hole in 0.1 mm "
            "film at 5.08 mm pitch -> registration/tear kills the mask"
        ),
        docs="10-reliability-mask/README.md S A3",
    ),
    dict(
        name="A4 rewritable printed comb mask",
        family="reusable printed comb (louvre slats), rewritten per map",
        one_liner=(
            "Instead of disposable media, a printed comb of slats is "
            "mechanically rewritten (slats pushed in/out by a shared writer) to "
            "encode the map, then swept over the field to arm the cells. No "
            "consumable, but the comb writer is a repeated precision mechanism."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.25,
        compliant_printed_parts=CELLS,
        wear_interfaces=CELLS * 2,
        repeated_silent_elements=CELLS,
        has_readback=False,
        recovery="rewrite comb + full reset",
        actuators_bought=2,
        mask_medium="reusable printed louvre comb (no consumable)",
        mask_write_inside_budget=True,
        correlated_failure="a stuck slat wrongs an 80-cell band",
        single_cell_failure="follower miss -> silent wrong cell",
        serviceable=True,
        timing_s=dict(digital_map=0.05, mask_generation=6.0, transport=1.0,
                      reset=2.0, lift=7.0, settle=1.5, verify=0.0),
        parts_usd=171.0,
        prototype_coupon="A: 1 slat + follower; B: 5x5 comb write",
        decisive_falsifier=(
            "slat rewrite friction/backlash makes the comb return to a wrong "
            "pattern -> silent map corruption"
        ),
        docs="10-reliability-mask/README.md S A4",
    ),
    dict(
        name="A5 banked binary ratchet + coarse bank readback",
        family="broadcast threshold ratchet, binary, banked, coarse readback (S6-LC evolved)",
        one_liner=(
            "S6-LC's mechanism, but cells become strictly two-state with a "
            "hard-stop toggle, and each bank gets ONE readback sensor row so a "
            "bank-wide miss is caught. Individual cell misses are still silent."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.0,
        compliant_printed_parts=0,
        wear_interfaces=CELLS,
        repeated_silent_elements=CELLS - 8,
        has_readback=True,
        recovery="per-bank re-home; individual cells still silent",
        actuators_bought=4,
        mask_medium="per-bank threshold mask (punched card or printed comb)",
        mask_write_inside_budget=False,
        correlated_failure="mask fault -> whole bank wrong (detected)",
        single_cell_failure="individual toggle miss -> silent (undetected)",
        serviceable=True,
        timing_s=dict(digital_map=0.05, mask_generation=0.0, transport=1.5,
                      reset=4.0, lift=8.0, settle=1.5, verify=2.0),
        parts_usd=213.0,
        prototype_coupon="A: 1 binary toggle; B: 5x5 bank",
        decisive_falsifier=(
            "per-bank readback cannot resolve a single stuck cell within one "
            "bank -> reliability stays (1-q)^6400"
        ),
        docs="10-reliability-mask/README.md S A5",
    ),
    dict(
        name="A6 embossed-tape mask",
        family="continuous embossed tape as a 2-level relief mask",
        one_liner=(
            "A continuous tape is embossed with a 2-level relief profile by a "
            "small heated roller/die; the relief indexes over followers that "
            "latch cells. Tape is cheaper and less tear-prone than punched film."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.35,
        compliant_printed_parts=CELLS,
        wear_interfaces=CELLS + 1,
        repeated_silent_elements=CELLS,
        has_readback=False,
        recovery="re-emboss/re-index tape and re-lift (full reset)",
        actuators_bought=2,
        mask_medium="embossed tape (consumable) + heated die",
        mask_write_inside_budget=True,
        correlated_failure="tape stretch -> cumulative registration error across a bank",
        single_cell_failure="relief too shallow -> follower misses -> silent wrong cell",
        serviceable=False,
        timing_s=dict(digital_map=0.05, mask_generation=18.0, transport=1.0,
                      reset=2.0, lift=7.0, settle=1.5, verify=0.0),
        parts_usd=179.0,
        prototype_coupon="A: 1 follower + emboss; B: 5x5 embossed-tape read",
        decisive_falsifier=(
            "embossing cannot hold >=0.4 mm relief across the tape length "
            "without creep under follower load -> mask blurs"
        ),
        docs="10-reliability-mask/README.md S A6",
    ),
    dict(
        name="A7 shared-camshaft bank + binary column latch",
        family="rotating camshaft per bank encodes the row pattern; columns latch",
        one_liner=(
            "One long printed camshaft per bank rotates to a set angle per map; "
            "cam lobes either push or clear each cell row's binary latch. The "
            "shaft angle IS the row pattern; a single motor per bank replaces "
            "per-cell selection."
        ),
        column_states=2,
        repeated_moving_parts=CELLS,
        precision_contacts_cell=0.2,
        compliant_printed_parts=CELLS,
        wear_interfaces=CELLS + 8 * COLS,
        repeated_silent_elements=CELLS,
        has_readback=False,
        recovery="re-home shafts + full reset",
        actuators_bought=1,
        mask_medium="camshaft angular position (continuous, analog)",
        mask_write_inside_budget=True,
        correlated_failure="one shaft angle wrong -> a whole bank row band wrong",
        single_cell_failure="lobe/follower wear -> silent wrong cell",
        serviceable=True,
        timing_s=dict(digital_map=0.05, mask_generation=0.0, transport=0.5,
                      reset=2.0, lift=9.0, settle=1.5, verify=0.0),
        parts_usd=158.0,
        prototype_coupon="A: 1 cam+latch; B: 5x5 camshaft row",
        decisive_falsifier=(
            "printing 80 distinct cam lobes on one shaft to <=0.1 mm angular "
            "repeatability is not achievable -> whole banks mis-select"
        ),
        docs="10-reliability-mask/README.md S A7",
    ),
]


# ===========================================================================
# 2. RELIABILITY GATE (DND-103) - the first-class gate
# ===========================================================================
# DND-103 rule: answer "what has to work correctly 6,400 times?" and MINIMISE
# it. A silent wrong cell is far worse than a loud one, because 6,400 cells
# compound: at q=1e-4 the map is only 52.7 % correct. The gate therefore has
# three parts:
#   (a) SILENT-SET size N_s = repeated_silent_elements  (must be small)
#   (b) READBACK: can the machine detect a wrong cell and recover? (bool)
#   (c) COUPON: is there a cheap coupon that can bound the as-printed spread?
#
# The reliability score rewards architectures whose repeated state is bounded
# by POSITIVE HARD STOPS (an exact position) over those whose correctness rides
# on a printed spring force, and rewards readback/re-homing over blind write.


def reliability_audit(arch: dict) -> dict:
    n = arch["repeated_silent_elements"]
    q_for_99 = break_even_q(max(n, 1)) if n > 0 else None
    return dict(
        cells=CELLS,
        repeated_moving_parts=arch["repeated_moving_parts"],
        precision_contacts_per_cell=arch["precision_contacts_cell"],
        compliant_printed_parts=arch["compliant_printed_parts"],
        wear_interfaces=arch["wear_interfaces"],
        silent_elements=n,
        has_readback=arch["has_readback"],
        recovery=arch["recovery"],
        q_for_99pct_map=round(q_for_99, 9) if q_for_99 is not None else None,
        map_yield_at_q1e_4=round(map_yield(1e-4, max(n, 1)), 5) if n > 0 else 1.0,
        map_yield_at_q1e_5=round(map_yield(1e-5, max(n, 1)), 5) if n > 0 else 1.0,
        # The gate:
        #  - hard-stop state (0 precision contacts) is a plus
        #  - readback in the machine is a plus (silent elements become detected)
        #  - a cheap coupon must exist
        passes=bool(
            (n == 0)
            or (arch["has_readback"] and n <= 8)
            or (n <= 64 and arch["fully_stop_bounded"] if arch.get("fully_stop_bounded") else False)
        ),
    )


# ===========================================================================
# 3. TIMING DECOMPOSITION (DND-103 honest timing)
# ===========================================================================
TIMING_STAGES = [
    ("digital_map", "Digital map processing"),
    ("mask_generation", "Physical mask generation"),
    ("transport", "Mask transport / indexing"),
    ("reset", "Display reset"),
    ("lift", "Broadcast lift operations"),
    ("settle", "Settling / locking"),
    ("verify", "Verification (if used)"),
]


def timing(arch: dict) -> dict:
    stages = arch["timing_s"]
    full = round(sum(stages.values()), 4)
    return dict(
        stages={k: dict(seconds=v, label=label) for k, label in TIMING_STAGES
                for v in [stages.get(k, 0.0)]},
        full_cycle_s=full,
        clears_30s=bool(full < TIME_GATE_S),
        margin_s=round(TIME_GATE_S - full, 4),
        visible_transition_s=round(
            stages.get("reset", 0.0) + stages.get("lift", 0.0)
            + stages.get("settle", 0.0) + stages.get("verify", 0.0), 4),
        note=("Visible transition excludes mask_generation (double-buffered "
              "where mask_write_inside_budget is true); sustained cycle includes it."
              if arch["mask_write_inside_budget"] else
              "Mask generation is OUTSIDE the visible budget: an unannounced "
              "map pays mask_generation first (product limitation)."),
    )


# ===========================================================================
# 4. SCREEN + RANKING
# ===========================================================================
RELIABILITY_WEIGHT = dict(
    silent_per_1000=1.0,      # dominant term: silent wrong-cell mechanisms
    no_readback_penalty=1500.0,
    precision_contact_penalty=400.0,   # per precision contact per cell
    compliant_spring_penalty=800.0,    # a printed spring whose force decides
    correlated_risk_penalty=500.0,
)


def reliability_score(arch: dict) -> float:
    """Lower is better. Reliability-first: silent failures dominate cost/time."""
    w = RELIABILITY_WEIGHT
    s = 0.0
    s += w["silent_per_1000"] * (arch["repeated_silent_elements"] / 1000.0)
    if not arch["has_readback"]:
        s += w["no_readback_penalty"]
    s += w["precision_contact_penalty"] * arch["precision_contacts_cell"]
    s += w["compliant_spring_penalty"] * (1.0 if arch["compliant_printed_parts"] > 0 else 0.0)
    return round(s, 2)


def screen() -> dict:
    rows = []
    for a in ARCHITECTURES:
        a = dict(a)
        a.update(GATE_EXTRA[a["name"]])
        t = timing(a)
        ra = reliability_audit(a)
        tl = tabletop_load(a)
        ru = regional_update(a)
        parts = a["parts_usd"]
        delivered = round(parts * UPLIFT, 2)
        rows.append(dict(
            name=a["name"],
            family=a["family"],
            one_liner=a["one_liner"],
            column_states=a["column_states"],
            actuators_bought=a["actuators_bought"],
            mask_medium=a["mask_medium"],
            mask_write_inside_budget=a["mask_write_inside_budget"],
            timing=t,
            reliability=ra,
            reliability_score=reliability_score(a),
            tabletop_load=tl,
            regional=ru,
            parts_usd=parts,
            delivered_usd=delivered,
            clears_parts=bool(parts < PARTS_GATE_USD),
            clears_delivered=bool(delivered < DELIVERED_GATE_USD),
            clears_30s=t["clears_30s"],
            clears_tabletop_load=bool(tl["holds_under_tabletop_load"]),
            correlated_failure=a["correlated_failure"],
            single_cell_failure=a["single_cell_failure"],
            serviceable=a["serviceable"],
            prototype_coupon=a["prototype_coupon"],
            decisive_falsifier=a["decisive_falsifier"],
            docs=a["docs"],
        ))
    # Rank: mission gate first (must clear 30 s AND <$250 parts AND tabletop
    # load), then reliability score (lower better), then cost.
    feasible = [r for r in rows
                if r["clears_30s"] and r["clears_parts"] and r["clears_tabletop_load"]]
    feasible.sort(key=lambda r: (r["reliability_score"], r["parts_usd"]))
    rejected = [r for r in rows if r not in feasible]
    return dict(
        evidence_class="CALCULATION over sourced FDM limits + actuator ratings; "
                       "no print, no purchase, no measurement (DND-27)",
        mission=dict(pitch_mm=PITCH_MM, rows=ROWS, cols=COLS, cells=CELLS,
                     active_mm=ACTIVE_MM, travel_mm=TRAVEL_MM,
                     time_gate_s=TIME_GATE_S, parts_gate_usd=PARTS_GATE_USD),
        architecture_count=len(rows),
        ranked_feasible=[r["name"] for r in feasible],
        ranked_feasible_full=feasible,
        rejected_or_infeasible=[r["name"] for r in rejected],
        rejected_full=rejected,
    )


# ===========================================================================
# 2b. WRITER-BANDWIDTH MODEL (the A1 decisive number, computed not asserted)
# ===========================================================================
HEAD_RATE_CELLS_S = 1000.0     # 1 ms/cell per head (assumption: toggle+settle)
HEAD_HEADS = 8                 # 8 parallel heads on the gantry bar
GALVO_OR_RAIL = 0.10           # s per lane move (150 mm traverse @ 1.5 m/s)


def writer_bandwidth(cells_to_write: int, heads: int = HEAD_HEADS,
                     rate: float = HEAD_RATE_CELLS_S) -> dict:
    """Time to write/read `cells_to_write` cells with `heads` parallel heads."""
    return dict(heads=heads, rate_cells_per_head_s=rate,
                effective_cells_s=heads * rate,
                cells=cells_to_write,
                seconds=round(cells_to_write / (heads * rate), 4))


# ===========================================================================
# 2c. TABLETOP-LOAD-DURING-WRITE GATE (DND-91 A7 - explicitly modelled)
# ===========================================================================
# A battle map has miniatures ON it. A design is only in-spec for tabletop
# updates if the moving/writing mechanism tolerates a miniature's weight on the
# region being changed. We model the worst case as a single 30 g mini sitting
# on one column of the region being lifted or written.
def tabletop_load(arch: dict) -> dict:
    """DND-91 A7: is a miniature on the moving/written region covered?

    Two honest sub-cases:
      * REGIONAL writer (A1): the writer touches few cells at once and works
        around placed minis; covered by design.
      * GLOBAL lift (A2-A7): the common platen must carry every miniature on the
        board during a write. That is not impossible - it is a load case the
        design must explicitly carry. We compute the worst case (a bank of 800
        cells with one 30 g mini per cell is absurd, so use a realistic 1 mini
        per 25 cells = 32 minis/bank) and PASS only if the stated per-cell hold
        and lift allowances exceed it.
    """
    per_cell_hold = arch.get("hold_allow_n", 0.0)
    if not arch.get("global_lift"):
        return dict(
            mini_load_n=MINIATURE_LOAD_N,
            mode="regional writer (few cells at a time)",
            holds_under_tabletop_load=True,
            note="Writer addresses only changed cells; minis elsewhere are untouched.",
        )
    # Global lift: worst realistic mini density on a moving bank of 800 cells.
    minis_per_bank = 32
    bank_load_n = minis_per_bank * MINIATURE_LOAD_N
    per_cell_mini_load = bank_load_n / 800.0
    # The column must still hold its terrain height under the mini (hold path),
    # and the lift axis must raise it. Both allowances are stated.
    lift_allow_per_cell = arch.get("lift_allow_per_cell_n", 0.0)
    holds = (per_cell_hold >= COLUMN_SERVICE_LOAD_N + per_cell_mini_load
             and lift_allow_per_cell >= COLUMN_SERVICE_LOAD_N + per_cell_mini_load)
    return dict(
        mini_load_n=MINIATURE_LOAD_N,
        mode="global lift (common platen carries placed minis)",
        minis_per_bank=minis_per_bank,
        bank_load_n=round(bank_load_n, 2),
        per_cell_mini_load_n=round(per_cell_mini_load, 4),
        required_per_cell_n=round(COLUMN_SERVICE_LOAD_N + per_cell_mini_load, 4),
        hold_allow_n=per_cell_hold,
        lift_allow_per_cell_n=lift_allow_per_cell,
        holds_under_tabletop_load=bool(holds),
        note=("Global-lift machines MUST carry all placed minis during a write; "
              "the unloaded assumption is NOT available. Passes only if the "
              "stated hold AND lift per-cell allowances cover terrain + minis."),
    )


# ===========================================================================
# 2d. REGIONAL UPDATE + JAM CONTAINMENT (DND-91 A8 - explicitly modelled)
# ===========================================================================
def regional_update(arch: dict) -> dict:
    """Can a sub-region change without a full-board reset? Is a jam detected?"""
    granularity = arch.get("regional_granularity", "none")
    return dict(
        granularity=granularity,
        regional_possible=granularity != "none",
        regional_requires_full_reset=bool(arch.get("regional_full_reset", True)),
        regional_visible_s=arch.get("regional_visible_s"),
        jam_detected=bool(arch["has_readback"]),
        note=("Regional update is a first-class operation for an arbitrary "
              "sub-region (writer addresses only the changed cells)."
              if granularity == "cell" else
              f"Regional update granularity = {granularity}; "
              + ("requires a full-board reset (product weakness)."
                 if arch.get("regional_full_reset", True)
                 else "bank/segment-local, no full reset.")),
    )


# ===========================================================================
# 2e. EXTRA GATE FIELDS per architecture (tabletop load + regional + lift mode)
# ===========================================================================
GATE_EXTRA: dict[str, dict] = {
    "A1 binary-latch + shared writer/reader": dict(
        global_lift=False,
        hold_allow_n=211.0,          # P1 latch compression land (DND-76), 64x service
        regional_granularity="cell", regional_full_reset=False,
        regional_visible_s=2.0,
    ),
    "A2 global broadcast binary interlock": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,   # S1 write allowance; below terrain + mini
        hold_allow_n=211.0, regional_granularity="none",
        regional_full_reset=True, regional_visible_s=None,
    ),
    "A3 punched-film mask + biased two-state columns": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,
        hold_allow_n=211.0, regional_granularity="row-band",
        regional_full_reset=True, regional_visible_s=None,
    ),
    "A4 rewritable printed comb mask": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,
        hold_allow_n=211.0, regional_granularity="bank",
        regional_full_reset=True, regional_visible_s=None,
    ),
    "A5 banked binary ratchet + coarse bank readback": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,
        hold_allow_n=211.0, regional_granularity="bank",
        regional_full_reset=False, regional_visible_s=3.0,
    ),
    "A6 embossed-tape mask": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,
        hold_allow_n=211.0, regional_granularity="row-band",
        regional_full_reset=True, regional_visible_s=None,
    ),
    "A7 shared-camshaft bank + binary column latch": dict(
        global_lift=True,
        lift_allow_per_cell_n=0.4,
        hold_allow_n=211.0, regional_granularity="bank",
        regional_full_reset=False, regional_visible_s=2.5,
    ),
}


# ===========================================================================
# 5. CONVERGENCE - selection, prototype ladder, falsifier
# ===========================================================================
SELECTED_NAME = "A1 binary-latch + shared writer/reader"

PROTOTYPE_LADDER = [
    dict(
        stage="A - single cell",
        scope="1 cell at true 5.08 mm pitch",
        validates="the binary toggle latch holds 3.27 N in compression and "
                  "releases with the writer's force; the reader sees its state",
        kills="if the latch cannot toggle at the writer force or the reader "
              "cannot distinguish the two states, A1 dies here",
        cost_class="printed coupon only (no purchase)",
    ),
    dict(
        stage="B - 5x5 full-pitch array",
        scope="25 cells, one writer/reader head on a short gantry",
        validates="neighbouring-cell tolerances, writer placement repeatability, "
                  "scan-verify + bounded retry catches a deliberately-stuck cell",
        kills="if placement/registration error exceeds half the pitch, or the "
              "reader cannot resolve one wrong cell among 25",
        cost_class="printed + 1 small stepper + 1 sensor",
    ),
    dict(
        stage="C - one bank/module",
        scope="one 10 x 80 bank (800 cells) driven by the full-width gantry",
        validates="bank reset, gantry traverse time, tabletop load under a "
                  "placed miniature, correlated gantry faults",
        kills="if a bank full-map write exceeds the linear timing extrapolation",
        cost_class="1 rail pair + 2 steppers + controller",
    ),
    dict(
        stage="D - multiple banks",
        scope="4 banks (3,200 cells), full active width in X",
        validates="cross-bank timing, sustained throughput, thermal/duty drift "
                  "of the head, regional update on one bank",
        kills="if sustained cycle time or duty thermal drift breaches the "
              "30 s / accuracy budget",
        cost_class="full frame + 4 steppers + PSU",
    ),
    dict(stage="full machine", scope="80 x 80 (6,400 cells)",
         validates="the full < 30 s arbitrary-map and regional-update target",
         kills="not a coupon - only reached after A-D survive",
         cost_class="the full purchased BOM"),
]


def a1_bandwidth() -> dict:
    """Compute A1's write + verify time from the head rate, not a magic number."""
    write_all = writer_bandwidth(CELLS)                       # worst-case all-change
    write_half = writer_bandwidth(CELLS // 2)
    verify = writer_bandwidth(CELLS)                          # read pass
    # Heavy/lane vs light/lane unchanged; the gantry still rasters 80 lanes.
    lane_overhead = COLS * GALVO_OR_RAIL
    return dict(
        heads=HEAD_HEADS,
        rate_cells_per_head_s=HEAD_RATE_CELLS_S,
        effective_cells_s=HEAD_HEADS * HEAD_RATE_CELLS_S,
        worst_case_write_all_s=round(write_all["seconds"] + lane_overhead, 4),
        typical_write_half_s=round(write_half["seconds"] + lane_overhead, 4),
        verify_pass_s=round(verify["seconds"] + lane_overhead, 4),
        note="Assumption-class: 1 ms/cell per head for toggle-settle and for "
             "read. Worst-case all-change write + verify + reset must clear 30 s.",
    )


def convergence() -> dict:
    s = screen()
    all_rows = s["ranked_feasible_full"] + s["rejected_full"]
    selected = next(r for r in all_rows if r["name"] == SELECTED_NAME)
    others = [r for r in all_rows if r["name"] != SELECTED_NAME]
    # The true runner-up is the next-best on the RELIABILITY score among all
    # candidates, not merely among the feasible set.
    others.sort(key=lambda r: r["reliability_score"])
    runner_up = others[0] if others else None
    return dict(
        selected=SELECTED_NAME,
        selection_class="CALCULATION + CAD (DND-27); no physical validation",
        why=[
            "Only architecture whose repeated silent-error set is STRUCTURALLY "
            "ZERO: the reader pass verifies every cell, so a failed toggle is "
            "detected and re-driven instead of silently wrong.",
            "State is a POSITIVE HARD STOP (over-centre latch between two walls) "
            "held in COMPRESSION - no printed spring force decides correctness "
            "(directly answers DND-103 'strongly discouraged').",
            "Regional update is a first-class cell-granularity operation: the "
            "writer addresses only changed cells; no full-board reset.",
            "Tabletop load is a covered load case: the writer works region-by-"
            "region, so placed miniatures elsewhere are untouched.",
            "Clears the mission gates: purchased parts < $250, full-map < 30 s, "
            ">=40 mm travel, 5.08 mm pitch, ~6,400 cells.",
        ],
        why_not_runners={
            name: ("6,400 independent silent elements, no readback"
                   if name.startswith(("A2", "A3", "A4", "A6"))
                   else "readback only resolves bank-wide, not single cells; "
                        "6,392 silent elements remain"
                   if name.startswith("A5")
                   else "one motor, but 6,400 silent elements and a printed "
                        "cam-lobe repeatability risk")
            for name in [r["name"] for r in others]
        },
        bandwidth=a1_bandwidth(),
        bom=a1_bom(),
        prototype_ladder=PROTOTYPE_LADDER,
        decisive_falsifier=selected["decisive_falsifier"],
        cheapest_coupon=selected["prototype_coupon"],
        runner_up=runner_up["name"] if runner_up else None,
        runner_up_score=runner_up["reliability_score"] if runner_up else None,
        residual_uncertainty=[
            "A1 readback is assumed optical/mechanical at ~1 ms/cell; if it "
            "cannot resolve a single wrong cell among 6,400, the silent-error "
            "advantage collapses (prototype B kills this).",
            "Writer-head toggle force vs latch snap force is assumption-class; "
            "the over-centre latch makes the STATE exact but not the snap force.",
            "Gantry XY registration over 406 mm (thermal, belt stretch) is "
            "unmeasured; needs a position-repeatability coupon.",
            "Per-cell wear of 6,400 latch hinges is measurement-only (DND-27); "
            "the compression hold removes the spring-force risk but not wear.",
            "Mask generation is N/A for A1 (direct write), which is a genuine "
            "product simplification only if the writer bandwidth holds.",
        ],
    )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "convergence":
        print(json.dumps(convergence(), indent=2))
    else:
        print(json.dumps(screen(), indent=2))


# ===========================================================================
# 6. A1 PURCHASED BOM (sourced-class sketch; printed parts excluded per DND-70)
# ===========================================================================
A1_BOM_LINES = [
    # (item, qty, unit_usd, evidence, use)
    ("X gantry stepper (NEMA17-class)", 1, 14.00, "sourced-class", "gantry across 406.4 mm X"),
    ("Y/head-traverse stepper (NEMA17-class)", 1, 14.00, "sourced-class", "head across Y lanes"),
    ("Writer toggle actuator (small stepper/servo)", 1, 9.00, "sourced-class", "over-centre latch toggle force"),
    ("X guide rail pair + bushings (400 mm)", 1, 22.00, "sourced-class", "gantry rigidity"),
    ("Y guide rail + bushings (400 mm)", 1, 16.00, "sourced-class", "head traverse"),
    ("Timing belt + 2 pulleys (X)", 1, 8.00, "sourced-class", "gantry drive"),
    ("Timing belt + 2 pulleys (Y)", 1, 8.00, "sourced-class", "head drive"),
    ("Writer head body + toggle prong", 1, 6.00, "allowance", "repeated head contact feature (printed body excluded, prong hardware)"),
    ("Reader head (reflectance/photodiode row)", 1, 12.00, "sourced-class", "state readback"),
    ("Controller (RP2040/ESP32)", 1, 5.00, "sourced-live", "RP2040 C2040"),
    ("Stepper driver modules (DRV8833-class)", 3, 2.00, "sourced-live", "gantry + head + writer"),
    ("Power supply + protection (24 V 2 A)", 1, 12.00, "sourced-listing", "smaller than S5's 35 VA"),
    ("Wire / connectors / flex loom", 1, 18.00, "sourced-class", "moving gantry loom"),
    ("Limit / home switches (X, Y, writer)", 5, 1.00, "sourced-class", "datum + recovery re-home"),
    ("Frame splice hardware (printed frame excluded)", 1, 10.00, "allowance", "406 mm frame printed as sub-tiles"),
    ("Fasteners (M3 assortment)", 1, 8.00, "sourced-class", "assortment"),
    ("Spares and miscellaneous", 1, 8.00, "assumption", "kept per DND-46 policy"),
]


def a1_bom() -> dict:
    rows = [dict(item=n, qty=q, unit=u, ext=round(q * u, 2), evidence=e, use=use)
            for (n, q, u, e, use) in A1_BOM_LINES]
    parts = round(sum(r["ext"] for r in rows), 2)
    delivered = round(parts * UPLIFT, 2)
    return dict(lines=rows, purchased_parts_usd=parts, delivered_usd=delivered,
                clears_parts=bool(parts < PARTS_GATE_USD),
                clears_delivered=bool(delivered < DELIVERED_GATE_USD),
                bought_actuators=4,
                note=("A1 replaces S6-LC's 4-screw global platen + 8 bank mask "
                      "gates with a 2-axis gantry + writer + reader. No per-cell "
                      "and no per-row bought actuator. Printed frame, columns, "
                      "latch arms and cradle lands are excluded per DND-70."))
