# GitHub workflows and the agent PR path

This repository is developed by Paperclip agents. Agents authenticate to GitHub in
two complementary ways:

- **Push (write):** a repo-scoped, write-enabled **SSH deploy key** at
  `~/.ssh/id_ed25519`. Use the SSH remote
  `git@github.com:sander-van-damme/project-shape-display.git`.
- **Pull-request API:** the automatic GitHub Actions **`GITHUB_TOKEN`**, granted
  `pull-requests: write` inside the workflows here. No separate PAT is required.

Together they cover the full branch → PR workflow. The `gh` CLI is **not**
authenticated in the agent environment; use plain `git` + SSH for push and a
workflow for the PR.

## How agents open a PR

1. **Push a feature branch** (never `main`):

   ```sh
   git checkout -b my/topic
   git push -u origin my/topic
   ```

2. **The [`open-pr.yml`](workflows/open-pr.yml) workflow opens the PR** using
   `secrets.GITHUB_TOKEN`:
   - **Automatic:** it runs on any push to a non-`main` branch and opens a PR if
     one is not already open. Provide `.github/open-pr-body.md` on the branch to
     control the body.
   - **Manual:** *Actions → open-pr → Run workflow*, then set `head`, `base`,
     `title`, and either `body` or `body_file`.
   - **Called:** `uses: ./.github/workflows/open-pr.yml` with `head` / `base` /
     `body_file` and `secrets: inherit`.

   It is **idempotent**: if an open PR already exists for `head → base`, it
   updates the title and body instead of creating a duplicate.

## Rules

- **Agents have standing authority to manage the complete Git workflow themselves, including
  merging PRs.** No board approval or rejection is required.
- Feature branches, PRs, reviews, and CI are preferred when they improve traceability or quality,
  but they are workflow tools, **not authorization gates**. Do not wait for board approval before
  merging or continuing ordinary repository work.
- **Never commit secrets.** The Actions `GITHUB_TOKEN` is injected at runtime;
  the SSH private key stays outside the repo.

## CI

[`ci.yml`](workflows/ci.yml) runs the deterministic engineering checks on every
push and pull request.
