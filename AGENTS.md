Keep context/output minimal; create only durable engineering knowledge, required product source, or genuinely reusable tools.
Use `./repo help`, `ls`, `find`, `get`, and `refs`; do not inspect or modify its source unless explicitly tasked with repository tooling. Allocate IDs with `./repo new`.

The 01–08 roots are lifecycle stages; do not add numbered roots. Knowledge lives under 03; candidates in 04, questions in 05, experiments in 06, decisions in 07, integrated product source in 08.
Keep objects atomic with semantic ID-bearing filenames. Metadata: only `status` and optional `builds-on: [ID, ID]`; point backward to material inputs, never maintain reverse links.
Distinguish sourced facts, assumptions, calculations, simulations, CAD, and physical measurements. Analytical acceptance does not prove hardware performance.
After experiments, distill conclusions and remove scaffolding with `./repo finish`; Git history is the archive. Keep source and irreplaceable evidence; remove reproducible output.
No README, CONTRIBUTING, indexes, project-management documents, or engineering CI. Run `./repo check` and relevant engineering checks locally.
Change AGENTS.md only for instructions important to essentially all future agents in its scope. Never add findings, current status, or temporary task rules.

DON'T FORGET TO MERGE BRANCHES WHEN FINISHED
