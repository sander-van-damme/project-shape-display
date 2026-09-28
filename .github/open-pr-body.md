# ci: make open-pr reusable and document the agent PR path

Closes the "make the Actions-token PR mechanism durable and reusable" half of
[DND-17](/DND/issues/DND-17); the DND-12 Test11 PR itself is [#12](https://github.com/sander-van-damme/project-shape-display/pull/12).

## What changed

- **`.github/workflows/open-pr.yml`** — upgraded from a push-only auto-opener to
  a genuinely reusable workflow:
  - `workflow_dispatch` + `workflow_call` inputs: `head`, `base`, `title`,
    `body`, `body_file`, `draft`.
  - Still runs automatically on push to any non-`main` branch; reads
    `.github/open-pr-body.md` on the branch when present.
  - **Idempotent** — updates an existing open PR for `head → base` instead of
    creating a duplicate.
  - Unchanged credential model: workflow-scoped `GITHUB_TOKEN` with
    `permissions: pull-requests: write`. No PAT, no `gh` auth. Proven live by the
    DND-15 capability probe.
- **`.github/README.md`** — documents the agent PR path and the hard rules.

## Engineering question

How do agents open PRs with **no board-provisioned credential**, and how is that
mechanism made durable in the repo rather than a one-off?

## Evidence

- The deploy key pushes branches (`git push` over SSH succeeded for this branch).
- This workflow opened **this PR** automatically on push — self-demonstrating.
- The DND-15 probe proved `GITHUB_TOKEN` + `pull-requests: write` opens PRs;
  PR #12 and PR #13 confirm it in normal use.

## Assumptions / limits

- Merge authority stays with the board; the workflow only opens/updates PRs.
- The workflow does not push to `main` (`branches-ignore: main`).
- No secrets are committed; the Actions token is injected at runtime.

## Passed / failed

- YAML parses (`jobs: open-pr`; triggers `push`, `workflow_dispatch`,
  `workflow_call`); the embedded Python compiles under Python 3.11.
- `open-pr` check succeeded on the branch and on PR #12.

## Remaining uncertainty

- Whether the board prefers push-auto-open (current) or dispatch-only. The
  upgraded workflow supports both; no behavioral change is forced.

## Next test

Merge authorization from the board; then any future branch opens its PR with zero
credential provisioning.
