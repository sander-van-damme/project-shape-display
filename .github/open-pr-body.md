## What changed

Adds an explicit `python -m pip install numpy` step to the `engineering-checks`
job, before the Test12 DND-44 readiness-closure step.

## Why (this is a fix for a red `main`)

`main` is currently **red** for every branch and for `main` itself. The failing
step is `Test12 DND-44 readiness closures (K1/K5/K6/K8/K10/K11)`.

Root cause (reproduced): `buckling_closure.py` — added by
[DND-44](/DND/issues/DND-44) / PR #42 — imports `numpy` inside
`core_reference()` (via `test08/cam_strength.py`). The `engineering-checks` job
never installs numpy. On the GitHub runner's `setup-python@v5` 3.11 toolcache
interpreter, numpy is absent, so the step fails with
`ModuleNotFoundError: No module named 'numpy'` and exit code 1. The check is
runner-image dependent, which is why some runs passed and others failed.

Evidence:
- `main` run `36498294541` (push at `2dff577b`) → failure, step 21.
- DND-44's own branch run `36497648668` (`74ef033f`) → failure, step 20 — i.e.
  PR #42 was merged with this step already red.
- Every branch in the run list after the DND-44 merge (`dnd48`, `dnd49`,
  `dnd-45`, `falsifier/dnd46`) fails on the same step.
- Local reproduction with numpy import blocked: `ModuleNotFoundError` from
  `buckling_closure.core_reference()`.
- No other CI script imports numpy; no other workflow needs this.

This PR is scoped strictly to the CI dependency. The DND-44 closure code itself
is untouched (its scope belongs to DND-44/DND-46).

## Verification

- YAML parses.
- `buckling_closure.py` and `buckling_closure_checks.py` pass with numpy 2.x.
- The added step is a no-op where numpy already exists.

## Related

- [DND-45](/DND/issues/DND-45) — the K2/K9 work whose CI run surfaced this.
