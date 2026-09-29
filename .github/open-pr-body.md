# DND-112: Falsifier — independent adversarial audit of the DND-111 A1 writer/reader rate bound

## What changed

Independent, default-deny audit of the DND-111 decisive number (the
[DND-108] method). No re-write of the CTO model.

- `07-evidence-and-decisions/falsifier_dnd112_a1_rate_audit.md` **(new)** — the
  audit register: 11 attacks (T1–T4 rate, R1–R4 read, G1 gate impact, G2
  down-state read, P1 SNR), each with the deciding number, the independent
  recompute, and a pass/fail.
- `07-evidence-and-decisions/falsifier_dnd112_checks.py` **(new)** — stdlib-only
  companion checker. Recomputes every DND-111 number **independently of
  `a1_writer_rate.py`**. Default mode prints the verdict and exits 0; `--gate`
  exits non-zero on any unresolved attack.
- `07-evidence-and-decisions/README.md` — DND-112 section + evidence-matrix row.
- `.github/workflows/ci.yml` — DND-112 step (runs and prints the audit).
- `08-current-design/` and `09-low-cost-variant/` **untouched**.

## Engineering question addressed

Is the DND-111 bounded rate defensible, and is its single-cell read claim sound?
Decide **analytically + CAD only**, no print/measurement ([DND-27]).

## Verdict: NOT CLEAN

**The rate side reproduces and stands; the single-cell read side fails.**

| Attack | Result | Deciding number |
|---|---|---|
| T1 stop-and-go excluded | PASS* | 30.4 cells/s @ X1C 20 m/s² (claimed 30); the 100 m/s² row is a V-shaped approximation, true 61.9 not 89.6 (+45%) |
| T2 fly-over rate / band | PASS | 164.5 cells/s; band 71.4–228 reproduced exactly |
| T3 ramp overhead | PASS* | ~24.6 % per-line accel/reversal omitted; cycle still < 30 s |
| T4 seven-stage 16.278 s | PASS | reproduced exactly |
| **R1 read gap by state** | **FAIL** | down-cell gap 42 mm → spot 24.51 mm = 4.82 pitches |
| **R2 corner-reach formula** | **FAIL** | reported 2.172 mm; true reach 4.081 mm |
| R3 neighbour threshold | PASS | ADR fails against own edge 1.80 instead of neighbour edge 3.28 |
| **R4 registration decoupling** | **FAIL** | ±0.264 mm is not the binding read limit |
| G1 gate impact | PASS* | no A1 gate flips (24.15→16.28 s, both < 30 s) |
| **G2 down-state read** | **FAIL** | up-neighbour near-field return beats the pocket ~441× → silent miss |
| P1 SNR provenance | PASS* | SNR ~1,462 set by TIA noise, not optics (assumption-class) |

`*` reproduced, but recorded because the attack is non-decisive or the row is mis-stated.

## Why the read attack is decisive

The A1 state is the **column top height** and the reader rides at a fixed height
above the **up**-plane. DND-111's 3.072 mm spot is the **up-state** spot; over a
down cell the target is 40 mm lower, so the spot is 24.51 mm (4.82 pitches) and
the four up neighbours (2 mm away, 5.08 mm lateral) dominate the return by
~441×. A down cell reads **up** — a *silent* miss that defeats the
readback/retry feature A1's whole reliability advantage rests on. This is a
**mechanism** failure, not the gantry-registration tolerance DND-111 names as
its residual, and no DND-111 coupon retires it.

## Consequence

- The **rate axis** may be treated as bounded (T2/T4 reproduced).
- The **read/verify axis is UNRESOLVED**; DND-111's "SUCCESS-eligible on the
  rate axis" must **not** be extended to a reader/retry promotion.
- Next test (CTO): state whether any A1 artifact reads a **common-height**
  target (latch flag/toe). If not, restate the read as a mechanism/Z-standoff
  problem with a rate trade study — a per-cell Z stroke is rate-fatal (~6
  cells/s), a per-line refocus may be survivable. Breadboard optical check is a
  CTO physical handoff.

## Evidence class

CALCULATION + CAD geometry only. No print, no purchase, no measurement
([DND-27]). No board contact ([DND-32]).

## Checks run

```
python 07-evidence-and-decisions/falsifier_dnd112_checks.py         # report (exit 0)
python 07-evidence-and-decisions/falsifier_dnd112_checks.py --gate  # exit 1 (4 FAILs)
python 07-evidence-and-decisions/falsifier_dnd104_checks.py         # 26/26
python 10-reliability-mask/analysis/reliability_mask_checks.py      # 50/50
```

## What remains uncertain

- Optical constants are assumption-class (unmeasured). They do not change the
  geometric R1/R2/G2 deciding numbers (42 mm gap, 4.08 mm reach).
- A1 could refute R1/G2 by reading a common-height target; that is not in any
  artifact I can see, so it is recorded as the CTO's required next statement.
