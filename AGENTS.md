Read `01-project-description/shape-display-mission.md` before choosing research work; its computational-invention mandate governs the program. Product constraints remain in 02.
Generate and compare materially different mechanisms and complete architectures; use executable synthesis/optimization where useful. Existing designs are comparison references, not a prescribed search space. Novelty guides exploration; feasibility and product value govern selection.
Prefer simulation before fabrication. Model relevant manufacturing variability, correlations and model uncertainty with sourced priors or explicitly labelled bounds; report sensitivity and evidence limits. Propose printing only for decision-relevant calibration, discrimination or physical qualification.
Update canonical results instead of spawning repeated audit/correction documents. Preserve unique failures and reproducible source; retire obsolete directions and remove redundant prose. A review must identify new decision-relevant evidence.

Keep context/output minimal; create only durable engineering knowledge, required product source, or genuinely reusable tools.
Navigate with `./repo help`, `ls`, `find`, `get`, and `refs`; allocate IDs with `./repo new`. Inspect/modify its source only for assigned tooling work.
Use `./worktree help` for task-worktree lifecycle. Keep the canonical checkout on `main`; managed task worktrees live in the sibling `<repo>-worktrees` directory. Do not manually switch, reuse, or remove managed worktrees; use the helper unless explicitly tasked with repository tooling.
Integrate durable results into `main` serially, then close temporary task branches/worktrees; Git preserves history.

The 01–08 roots are lifecycle stages; do not add numbered roots. Knowledge lives under 03; candidates in 04, questions in 05, experiments in 06, decisions in 07, integrated product source in 08.
Keep objects atomic with semantic ID-bearing filenames. Metadata: only `status` and optional `builds-on: [ID, ID]`; point backward to material inputs, never maintain reverse links.
Distinguish sourced facts, assumptions, calculations, simulations, CAD, and physical measurements. Analytical acceptance does not prove hardware performance.
After experiments, distill conclusions and remove scaffolding with `./repo finish`; Git history is the archive. Keep source and irreplaceable evidence; remove reproducible output.
No README, CONTRIBUTING, indexes, project-management documents, or engineering CI.
Exception: `.agents/memory/cto.md` is a compact, non-canonical research compass, curated by the CTO, not management history or evidence. 01–08 and Paperclip remain authoritative. Run `./repo check` and relevant engineering checks locally.
Change AGENTS.md only for instructions important to essentially all future agents in its scope. Never add findings, current status, or temporary task rules.
