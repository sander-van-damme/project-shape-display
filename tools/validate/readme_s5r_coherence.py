#!/usr/bin/env python3
"""DND-64 CI coherence gate: the promoted-machine README must match the model.

The source-of-truth document `08-current-design/README.md` must lead with the
**promoted S5-R machine**, not the superseded incumbent S5. This gate fails if
the README's *promoted-machine headline* contradicts the promoted model
(`06-experiments/test12_winner_convergence/s5r_register.py`), so the document
cannot silently drift back to a superseded architecture.

WHAT IT CHECKS
--------------
    R1  The machine name in the H1 title and the status block is S5-R.
    R2  The headline actuator count (2 bank motors + 40 writer solenoids = 42)
        matches `BANK_MOTORS` + `WRITERS`.
    R3  The headline full-map time matches `timing.full_map_s5r_s` (24.615 s)
        and the README's headline states it as under the 30 s cap.
    R4  The headline delivered cost matches `bom.delivered_usd` ($404.60).
    R5  The headline is not the superseded incumbent-S5 figures: the *live*
        headline block must not present the incumbent S5 machine description
        (80-channel programming head / 80 bought steppers) as current, and must
        not present the incumbent S5 cost/time as the promoted headline.
    R6  A live S5-R residual register exists (the consolidated DND-59 ids), and
        the incumbent K1-K12 register is explicitly labelled legacy.

WHAT IT IS / IS NOT
-------------------
    evidence class: DOCUMENTATION / CALCULATION over the promoted model.
    It is not a print and not a measurement ([DND-27]).

USAGE
-----
    python tools/validate/readme_s5r_coherence.py

EXIT CODES
----------
    0   the README headline is coherent with the promoted model.
    1   a coherence check failed (documentation drift).
    2   the checker could not run (missing README or model).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
README = REPO / "08-current-design" / "README.md"
MODEL = (REPO / "06-experiments" / "test12_winner_convergence"
         / "s5r_register.py")

FAILS: list[str] = []


def check(cond: bool, msg: str) -> None:
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {msg}")
    if not cond:
        FAILS.append(msg)


def load_model() -> dict:
    proc = subprocess.run(
        [sys.executable, str(MODEL)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    if not README.exists():
        print(f"ERROR: missing {README}", file=sys.stderr)
        return 2
    if not MODEL.exists():
        print(f"ERROR: missing promoted model {MODEL}", file=sys.stderr)
        return 2

    text = README.read_text()
    model = load_model()

    bank_motors = int(model["bom"]["bank_motors"])
    writers = int(model["bom"]["writers"])
    actuator_count = int(model["bom"]["actuator_count"])
    full_map_s = float(model["timing"]["full_map_s5r_s"])
    delivered = float(model["bom"]["delivered_usd"])

    print(f"Promoted model: S5-R | actuators={actuator_count} "
          f"({bank_motors} bank + {writers} writers) | "
          f"full_map={full_map_s} s | delivered=${delivered}")
    print("=" * 72)

    # The headline is the title + status block: everything before the first "## "
    # section that is not the title/intro. Take the top-of-file block up to "## 1".
    m = re.search(r"^## 1\.", text, re.M)
    headline = text[:m.start()] if m else text

    # --- R1 machine name -------------------------------------------------
    print("\n[R1] promoted machine named S5-R in the title and status block")
    first_line = text.splitlines()[0]
    check("S5-R" in first_line, f"H1 names S5-R: {first_line!r}")
    check("PROMOTED" in headline, "status block marks the machine PROMOTED")

    # --- R2 actuator count ----------------------------------------------
    print("\n[R2] actuator count matches the promoted model")
    check(str(actuator_count) in headline,
          f"headline states the actuator count {actuator_count}")
    check(str(bank_motors) in headline and str(writers) in headline,
          f"headline states {bank_motors} bank motors and {writers} writers")

    # --- R3 full-map time ------------------------------------------------
    print("\n[R3] full-map time matches the promoted model")
    time_str = f"{full_map_s:g}"
    check(time_str in headline,
          f"headline states the promoted full-map time {time_str} s")
    check("30" in headline and ("< 30" in headline or "under 30" in headline),
          "headline frames the full-map time as under the 30 s cap")

    # --- R4 delivered cost ----------------------------------------------
    print("\n[R4] delivered cost matches the promoted model")
    cost_str = f"${delivered:.2f}"
    check(cost_str in headline, f"headline states the delivered cost {cost_str}")

    # --- R5 no superseded incumbent S5 as the current machine ------------
    print("\n[R5] incumbent S5 is not presented as the promoted machine")
    # The live headline must not carry the incumbent machine description as current.
    check("80-channel" not in headline,
          "headline does not describe the incumbent 80-channel head as current")
    check(not re.search(r"PROMOTED as the single buildable winner by", headline),
          "headline is not the old S5 promotion sentence")
    # The headline must not *declare S5 promoted/current*; historical mentions of
    # S5 (e.g. "S5 ... superseded", "the incumbent S5") are allowed only when the
    # headline also declares S5-R promoted.
    declares_s5_current = bool(re.search(
        r"(?:^|\n)# 08 .*S5\b(?!-)", headline)) or \
        re.search(r"Status:?\*{0,2}\s*PROMOTED[^\n]*\bS5\b(?!-)", headline) is not None
    check(not declares_s5_current,
          "the title/status does not declare S5 (non-R) as the promoted machine")
    # The superseded machine must be labelled.
    body_after = text[m.start():] if m else text
    check("Superseded incumbent S5" in text or "superseded incumbent S5" in text,
          "the incumbent S5 is explicitly labelled superseded")
    # The old S5 headline numbers must not be the promoted headline.
    check("$482.95" not in headline,
          "headline does not present the incumbent S5 $482.95 as the cost")
    check("26.251" not in headline,
          "headline does not present the incumbent S5 26.251 s as the time")

    # --- R6 live S5-R register + labelled legacy K-register --------------
    print("\n[R6] live S5-R residual register; K-register labelled legacy")
    check("S5-R residual register (live)" in text,
          "a live S5-R residual register section exists")
    for resid in ("R-DND54-KEEPER", "R-DND54-6", "R-DND55-4"):
        check(resid in text, f"register lists {resid}")
    check("Append" in body_after and "legacy" in body_after.lower(),
          "the incumbent K-register is relocated to a labelled legacy appendix")

    print("\n" + "=" * 72)
    if FAILS:
        print(f"GATE: FAIL ({len(FAILS)} failing check(s))")
        for f in FAILS:
            print(f"   - {f}")
        return 1
    print("GATE: PASS (README coherent with the promoted S5-R model)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
