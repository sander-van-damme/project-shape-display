# SHA-17: trim CI bloat — drop redundant gate re-runs, enforce the printability gate

## Context

[SHA-17](/SHA/issues/SHA-17): GitHub CI had grown to 587 lines / 8 jobs with
accumulated redundant steps. This PR removes the parts that cost wall-clock
without pinning anything, and turns one vacuous step into a real gate.
**No gate coverage is removed.**

## What changed

- `concurrency: cancel-in-progress` on the workflow so rapid agent pushes get a
  fast signal from the latest run instead of queueing stale duplicates.
- DND-112/113/114/115 steps no longer re-run `a1_writer_rate.py`,
  `reliability_mask_checks.py`, or the DND-104 audit: the DND-111 step runs
  them authoritatively on the same checkout earlier in the job, and each
  `--gate` checker recomputes its numbers independently in-file (verified: the
  gate scripts read no artifacts). Saves ~33 s of job CPU (~19%).
- Removed the DND-54 `s5r_register.scad` printability step: it ran the same
  file as the DND-59 step **without** `--fail-on-design-fail`, so it exited 0
  even on a design FAIL and pinned nothing.
- The surviving DND-59 `s5r_register.scad` printability step now passes
  `--fail-on-design-fail`, enforcing its stated "must PASS". Verdict is
  currently PASS.
- Single `pip install` step per CAD job + `cache: "pip"` on `setup-python`.

## Kept deliberately (the expensive parts are load-bearing)

- K2/K9 sweeps (~100 s), detent sweep (~40 s), writer-rate derivation (~12 s),
  test09 (~9 s), T11-A/J2 analytic gates (~35 s combined): each pins a distinct
  DND/SHA claim. Not touched.
- S5-R `fab-package` full-set render (~10.5 min CGAL): still the promoted-build
  evidence (DND-60/DND-61, DND-64 coherence gate). Follow-up, not this PR.

## Evidence (CALCULATION, [DND-27](/DND/issues/DND-27))

Full local simulation of all 49 `engineering-checks` steps in CI order:
**48/48 green** (only `pip install` skipped — sandbox has no pip; numpy 1.26.4
preinstalled; runner path unchanged). Total ~246 s. The enforced DND-59 gate
exits 0 with `--fail-on-design-fail` (verdict PASS).

## Assumptions / residual uncertainty

- CAD-render jobs (`dnd104-cad-render`, `lowcost-cad-render`, `j2-cad-render`,
  `lowcost-primitives-cad-render`, `winner-cad-render`, `fab-package`,
  `geometry-validation-harness`) need a real runner with OpenSCAD; validated
  by CI, not locally.
- Wall-clock is still dominated by `fab-package`; see follow-up above.
