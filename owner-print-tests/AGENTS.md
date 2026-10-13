# Owner print-test handoff (CTO instructions)

This directory is a low-friction handoff for **optional physical tests by Sander**, not a parallel research backlog or proof of any printed result. The CTO owns test selection, CAD, STL export, priorities and retirement. Sander has **no print deadline**, may respond much later or may never print a proposed test. Do not block independent research on a human print.

## Only prepare decision-changing, small tests

- First ask what engineering or D&D-usability decision physical evidence could change. Prefer simulation/reasoning before requesting a print if those can decide it. Historical CAD is a candidate, not a standing print order.
- Keep **at most three READY print jobs in total**, preferably just one. A job is one small build-plate batch (which may contain several clearly labelled alternatives); avoid dozens of variants, large batches and manual assembly. Assign the READY jobs **P1, P2, P3** in genuine priority order. Anything speculative stays outside the ready queue.
- When a useful test is justified, copy `TEST-TEMPLATE.md` to `owner-print-tests/<short-test-name>/test.md` and fill in all CTO sections. Place **fully exported, ready-to-slice .stl files** next to that `test.md`. A source `.scad`, Python generator, CAD screenshot, or instructions for Sander to compile/export a mesh are **not** a deliverable. Ordinary slicing on the user's printer is expected.
- Before marking READY: check that the exact referenced STL files exist, are non-empty, show the intended geometry, have correct millimetre-scale dimensions, are correctly oriented/separated, and have printable/manifold geometry where required. Explain material, suggested slicer settings/supports, number of parts, estimated print time, simple assembly, safe measurement steps and what observations reject the hypothesis. If export/checks are incomplete, status stays DRAFT, **not** READY. Do not ask Sander to buy equipment or materials without explicit approval.
- Give the user an easy, short result section to fill out in `test.md`. Do not invent measurements or infer success from silence. Document observations as observations; CTO interpretations and product decisions follow only after results exist.

## Maintain priorities as knowledge changes

Each test's `test.md` carries **Status** (DRAFT / READY / DEFERRED / COMPLETED / RETIRED), **Priority** (P1 / P2 / P3 / none), **Last reviewed**, and a brief **reason**. A test awaiting Sander is still optional and is not a reason to halt CTO work or repeatedly remind him.

When new calculations, geometry, architecture choices or other evidence make a test less useful, **reorder, defer or retire it promptly** and explain why, with a link to the new evidence. A RETIRED test must not be offered as print-ready: remove obsolete STL payloads and retain a concise reason in `test.md` (or the relevant canonical result and Git history). If a replacement is warranted, prepare a new small validated pack rather than asking Sander to print stale parts. Keep the ready queue genuinely useful, not full.
