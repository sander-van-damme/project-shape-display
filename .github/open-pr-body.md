# DND-122 follow-up: fix the unsupported own-column clearance (3.41 → 3.42 mm) and gate it in A13

## What changed

- **ADR** `07-evidence-and-decisions/dnd115-a1-state-encoding-shutter.md` (§2 table
  and §7 prose) and **A1 README** `08-integrated-designs/a1-reliability-first/README.md`
  (table and prose): swept flap **own-column clearance 3.41 → 3.42 mm**.
- **Falsifier checker** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.py`:
  **A13 extended** to parse the ADR's **swept neighbour** (0.280 mm) and **swept
  own-column** (3.42 mm) clearances and compare them to the live model's swept
  envelope, so this subclass now fails the gate.
- **Audit register** `07-evidence-and-decisions/falsifier_dnd115_a1_shutter_audit.md`:
  a short "DND-122 follow-up" note recording the finding, the fix, and the negative
  control.

## Engineering question

Does the live main tree quote any DND-115 shutter number that **no artifact
supports** — the DND-112/DND-111 defect class that [DND-122](/DND/issues/DND-122)
closed for the superseded DND-121 branch?

## Evidence produced

- The [DND-122](/DND/issues/DND-122) review (A13) verified the live main figures
  0.280 / 0.084 / 0.434 / 4.48× / 0.325 mm — all reproduced by the model.
- Reviewing that pass surfaced one **uncovered** figure: the ADR/README quoted the
  swept own-column clearance as **3.41 mm**, while the live model's swept envelope
  produces `sweep_z_min − TRAVEL = 43.42 − 40.0 = ` **3.42 mm** (audit A8 reports
  3.420 mm). The CAD flat-underside echo is 3.55 mm, so **no artifact supported
  3.41 mm**.
- Fix applied and the figure is now gated: **negative control** — tampering the ADR
  own-column figure back to 3.41 makes A13 **FAIL** with exit 1 (verified).

## Calculations / simulations / tests run

- `falsifier_dnd115_a1_shutter_audit.py --gate` → **CLEAN 14/14**
- `falsifier_dnd115_checks.py --gate` → **CLEAN 12/12**
- `falsifier_dnd114_checks.py --gate` → **CLEAN 7/7**
- `falsifier_dnd112_checks.py --gate` → **CLEAN 11/11**
- `reliability_mask_checks.py` → **78/78**
- `a1_writer_rate.py` → exit 0

## Assumptions / uncertainty

- 3.42 mm is the model's fine-grid **swept envelope** min; the CAD flat-underside
  echo is 3.55 mm (the rotating corner dips lower than the flat underside). The ADR
  table labels the row "CAD envelope"; the authoritative swept value is the model's
  43.42 − 40.0. Only a wording/number fix — **no geometry change**.
- Evidence class **CALCULATION + CAD only** ([DND-27](/DND/issues/DND-27)); no print,
  no measurement. No board contact ([DND-32](/DND/issues/DND-32)).

## Remaining / next

- Superseded sibling [DND-121](/DND/issues/DND-121) and PR #94 (branch
  `cto/dnd121-shutter-framing`) should be **closed as superseded** — its model is
  the pre-DND-119 tree (`on_off_return_ratio` 7.41, no crosstalk field) and merging
  it would regress main. Handled separately on the issue thread.
