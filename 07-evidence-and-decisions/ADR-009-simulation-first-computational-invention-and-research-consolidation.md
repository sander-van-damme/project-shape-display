---
status: active
builds-on: [E-001, E-002, E-039, E-042, E-047]
---

# ADR-009: computational invention and research consolidation

Decision (2026-10-07, user-directed research reset): adopt the simulation-first computational-invention mandate in `01-project-description/shape-display-mission.md`. Search materially different architectures and synthesize mechanisms under manufacturing uncertainty. No existing candidate is selected as the product leader. Stage 02 product requirements remain in force.

Basis: the earlier program accumulated repeated audits and coupon handoffs while decisive mechanisms remained undefined. E-039 rejects a bounded slider geometry; E-042 identifies missing five-stop/load geometry and a defective transition schedule; E-047 rejects the frozen combined structural screen. These are useful negative results, not physical tests or universal rejections of their mechanism classes. E-001/E-002 preserve full-scale throughput and reliability constraints on any new search.

Consequences:

- A-001/A-002/A-005/A-011 and DES-001 through DES-004 become comparison references. Their primitives can seed new combinations, but incremental repair or another coupon is no longer the default research program. DES-006 is rejected against its declared combined screen.
- Retire A-010's current implementation. Reopening requires a materially redefined mechanism that resolves the retained geometry contradiction and competes on complete-system evidence.
- Remove the global-release-comb and three-bit-latch variant proposals. ADR-003 retains the global-reset tradeoff. For the three-bit idea, three bits provide eight codes, of which five may encode heights and three remain unused; the prior five-code sequence does not limit arbitrary transitions to two bit changes (001→110 changes three). Parallel bit lanes add contacts/read channels; serial lanes multiply timing. No complete mechanical height decoder or physically qualified mechanism was established. State encoding remains an available primitive, not an active successor design.
- Consolidate writer/reader fixture reviews into E-018; rotor acceptance-contract findings into E-042; sourcing corrections into E-044/E-046; and slider-repair rejection into E-035/E-039. Remove the administrative blocker report, duplicate coupon wrapper, repeated cost/compatibility input copies and obsolete boundary-reconciliation handoff. Preserve executable source and distinct results. Full originals are recoverable from parent revision `ce8135eb4f1b1cb138bdf71edd6092f7ac9c1db8`.
- Use two standing roles: administrative CEO and hands-on CTO research lead, as selected by the user. Store their prompts at `tools/agent-prompts/ceo.md` and `tools/agent-prompts/cto.md`. The CTO owns execution, review and curation directly; temporary independent assistance is optional and bounded. There is no mandatory specialist pipeline. Root `AGENTS.md` supplies the common mandate. Live Paperclip configuration must be updated separately; repository prompt files do not activate or pause agents.

This supersedes the research-priority/next-coupon prescriptions of ADR-001, ADR-002 and ADR-006, while retaining their useful engineering constraints and negative evidence. It does not relax cost, update, regional-isolation or physical qualification requirements. Broad search must still converge: promote, refine or reject candidates on reproducible evidence, and choose physical tests when they become the best way to reduce consequential model uncertainty.
