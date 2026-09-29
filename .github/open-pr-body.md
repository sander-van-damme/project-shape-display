# DND-102: fix broken relative links in `10-reliability-mask/README.md`

## What changed

Two relative links in `10-reliability-mask/README.md` pointed to
`../../07-evidence-and-decisions/...` instead of `../07-evidence-and-decisions/...`.
From the `10-reliability-mask/` directory, `../../` escapes the repository root, so
both links were dead.

- `falsifier_dnd104_criteria.md` link (the DND-108 pre-registered audit criteria).
- `dnd104-reliability-mask.md` link (the DND-104 ADR / decision record).

Fixed to `../07-evidence-and-decisions/...`. Paperclip UI links (`/DND/issues/...`)
are unchanged and remain correct.

## Engineering question

Repository hygiene only — no engineering claim, calculation or CAD changed. The
DND-104 decision record and audit are unchanged; this only makes the existing
candidate documentation navigable.

## Evidence

- **Link check (calculation):** a relative-link resolver over every `](…​)` in
  `10-reliability-mask/README.md` now reports zero broken *file* links (only the
  intentional `/DND/issues/...` UI links resolve non-locally).
- Diff is 2 lines (`1 file changed, 2 insertions(+), 2 deletions(-)`).

## Assumptions / uncertainty

None. Purely a documentation-path correction.

## Next test

Run the deterministic `engineering-checks` CI on this PR (unchanged suite).
