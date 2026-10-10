Read `01-project-description/shape-display-mission.md` before choosing research work; its computational-invention mandate governs the program. Product constraints remain in 02.
Generate and compare materially different mechanisms and complete architectures; use executable synthesis/optimization where useful. Existing designs are comparison references, not a prescribed search space. Novelty guides exploration; feasibility and product value govern selection.
Prefer simulation before fabrication. Model relevant manufacturing variability, correlations and model uncertainty with sourced priors or explicitly labelled bounds; report sensitivity and evidence limits. Propose printing only for decision-relevant calibration, discrimination or physical qualification.
Update canonical results instead of spawning repeated audit/correction documents. Preserve unique failures and reproducible source; retire obsolete directions and remove redundant prose. A review must identify new decision-relevant evidence.

Keep context/output minimal; create only durable engineering knowledge, required product source, or genuinely reusable tools.
Use `./repo help`, `ls`, `find`, `get`, and `refs`; do not inspect or modify its source unless explicitly tasked with repository tooling. Allocate IDs with `./repo new`.
Use `./worktree help` for task-worktree lifecycle. Keep the canonical checkout on `main`; managed task worktrees live in the sibling `<repo>-worktrees` directory. Do not manually switch, reuse, or remove managed worktrees; use the helper unless explicitly tasked with repository tooling.
Treat task branches and worktrees as temporary execution state: integrate durable results into `main` serially, then clean up completed task branches/worktrees rather than retaining them as history.

The 01–08 roots are lifecycle stages; do not add numbered roots. Knowledge lives under 03; candidates in 04, questions in 05, experiments in 06, decisions in 07, integrated product source in 08.
Keep objects atomic with semantic ID-bearing filenames. Metadata: only `status` and optional `builds-on: [ID, ID]`; point backward to material inputs, never maintain reverse links.
Distinguish sourced facts, assumptions, calculations, simulations, CAD, and physical measurements. Analytical acceptance does not prove hardware performance.
After experiments, distill conclusions and remove scaffolding with `./repo finish`; Git history is the archive. Keep source and irreplaceable evidence; remove reproducible output.
No README, CONTRIBUTING, indexes, project-management documents, or engineering CI.
Exception: the single `.agents/memory/cto.md` file is a compact, non-canonical CTO research compass, not project-management history or technical evidence. The CTO curates it in place; everyone else treats 01-08 plus Paperclip as authoritative. Run `./repo check` and relevant engineering checks locally.
Change AGENTS.md only for instructions important to essentially all future agents in its scope. Never add findings, current status, or temporary task rules.
