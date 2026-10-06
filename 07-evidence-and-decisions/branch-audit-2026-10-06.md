# Branch audit — 2026-10-06

## Decision

The audit covered every `origin/*` branch after `git fetch --all --prune`, using
ancestry, patch equivalence (`git cherry`), open pull requests, and active
Paperclip work as independent checks.

- Merge `lab-46-des003-height-capability-gate`. It is one commit ahead of
  `main`, has no conflicting history, and records the already-completed binary
  height-capability gate.
- Retain `design/lab-52-five-level-successor` and
  `falsify/des004-independent-audit`. They currently share a tip, but belong to
  the active LAB-52/LAB-54 implementation and independent-review path. They are
  not eligible for integration until that review finishes.
- Delete every other topic branch. Thirty-three are strict ancestors of
  `main`; the remaining ten are obsolete legacy work, patch-equivalent
  duplicates, or intermediate LAB branches whose commits are all carried by
  the retained LAB-52/LAB-54 tip.

There were no open GitHub pull requests at audit time.

## Safe to delete: already merged into `main`

`ceo/dnd57-verdict-r6b`, `cost/dnd37-ratify-winner-bom`,
`cost/dnd98-reratify-s6lc-bom`, `cto/dnd104-reliability-mask`,
`cto/dnd111-writer-rate-bound`, `cto/dnd72-ultra-low-cost`,
`cto/dnd93-fix-g3`, `cto/dnd97-mechanism-repair`,
`dnd-38-detent-sweep`, `dnd-41-reconcile`,
`dnd-45-k2-scallop-sweep-k9-monte-carlo`,
`dnd-88-everything-assembled-renders`,
`dnd-94-reconcile-09-lowcost-subdirs`,
`dnd4/s3-m4-and-validator-fix`, `dnd4/s3-pivot-clearance-gate`,
`dnd41-followup`, `dnd41-reconcile`,
`dnd43/step6-load-structure-power`, `dnd69/s5r-renders`,
`docs/dnd102-fix-links`, `docs/dnd30-reconcile-adr001-merge-noprint`,
`fab/dnd29-software-validation-harness`,
`falsifier/dnd112-a1-rate-audit`, `falsifier/dnd35-adversarial-audit`,
`falsifier/dnd36-s5-review`, `falsifier/dnd74-s6lc-audit`,
`falsifier/dnd91-s6lc-audit`, `feat/dnd76-lowcost-primitives`,
`fix/dnd37-regression-gates`, `fix/dnd41-ratify-bom-consistency`,
`integrate/test11-all`, `re-scope/dnd28-analytic-gates`, and
`restructure/agent-native`.

## Safe to delete: superseded or duplicate

- `cost/dnd73-ratify-s6lc-bom` — superseded by the merged DND-98
  re-ratification and later low-cost work.
- `cto/dnd93-fix-s6lc-g3` — superseded by the merged DND-93 repair path; its
  remaining unique commits are an older repair variant and PR-body churn.
- `dnd44-readiness-closure` — its substantive patch is patch-equivalent to
  work already on `main`.
- `fab/dnd26-fabrication-package` — abandoned pre-restructure fabrication
  package from the legacy DND line; not compatible with the current design
  tree and has no open PR or active task.
- `falsifier/dnd104-preregistration` and
  `falsifier/dnd46-closure-audit` — substantive patches are already present;
  only stale PR-body commits remain unique.
- `lab-16-coupon-b-protocol`, `lab-17-e009-support-bound-model`,
  `lab-38-e010-regional-bound-repair`, and
  `lab-39-des003-eight-head-bom-reconciliation` — intermediate pointers into
  the history retained by `design/lab-52-five-level-successor` and
  `falsify/des004-independent-audit`.

## Local cleanup

Delete local topic branches that are merged into `main` or whose remote was
removed. Do not remove a branch checked out in a live worktree. The repository
history remains recoverable from `main` and the retained active branches.
