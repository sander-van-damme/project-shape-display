# Test11 — S3/S4 shared-drive machines + S5 rotary-stop gate closure

## What changed

- Adds `06-experiments/test11_shared_drive_gate_analysis/`:
  `model.py` (system arithmetic), `checks.py` (rejection-threshold asserts),
  `coupon_geometry.py` (calculated fit screen), `rejection_tests.json`
  (cheapest-kill test register), `selector_fanout_coupon.scad` (**unrendered**
  CAD), `README.md`.
- Updates `04-architecture-candidates/README.md` (S3–S5 refinement),
  `05-research-questions/README.md` (partial answers Q3/Q4/Q5/Q6/Q8),
  `06-experiments/README.md`, `07-evidence-and-decisions/README.md`.
- Adds `.github/workflows/open-pr.yml` (reusable Actions-token PR opener; no PAT).

## Engineering question

Can the shared-drive / multi-row survivors S3 and S4 be specified as **complete
machines with real component counts**, and what is the **cheapest test that would
reject each one**? For S5, can each of the five open Test09 gates be reduced to a
smallest qualifying coupon?

## Evidence produced (calculated / CAD only — no physical measurement claimed)

- **S3 — multi-row mechanical DMA head.** Bit-plane cam programmer: a carriage
  dwells over 4 rows (20 stations); two 4-plane cam banks/station write all 80
  columns of a row per sweep. **41 head motors, 0 bought per-channel selectors**,
  ~$94 allowance. Calculated full-map schedule **25.20 s** (4.80 s margin vs the
  strict <30 s). Primary killer named: 4 rows share one 5.08 mm band → **1.27 mm
  row land, 0.47 mm web** at 0.4 mm nozzle.
- **S4 — distributed passive tiles on a shared bus.** 64 tiles read 4 bus
  revolutions. Arithmetic shock: 64 × $6 absolute = **$384 bought clutches before
  the rest of the machine**, so the coupler must be **printed**. Dominant distinct
  risk: **correlated bus backlash** (1°/joint → 0.088 mm last-tile error inside a
  0.25 mm margin; 3°/joint → 0.264 mm and fails).
- **S5 — rotary-stop reference.** Five gates, all **open**, each with one smallest
  coupon (T11-F..J). Reproduced cost boundary: $332 working non-motor leaves
  **$1.058/motor** vs Test08's $1.25 allowance — **does not fit $500 with 20%
  contingency**.

`checks.py` runs 10 PASS/FAIL gates and **all pass**, i.e. every asserted
rejection threshold is currently survived by the corresponding candidate's
arithmetic.

## Reproduce

```bash
cd 06-experiments/test11_shared_drive_gate_analysis
python model.py             # S3/S4/S5 arithmetic
python checks.py            # asserts the rejection thresholds
python coupon_geometry.py   # S3 coupon fit screen
# optional, OpenSCAD 2021.01 on PATH:
openscad -o selector_fanout_coupon.stl selector_fanout_coupon.scad
```

Python 3.11+, standard library only.

## Passed / failed

- PASS: S3 full-map <30 s (25.20 s); S3 per-bank motor force <2 N (1.38 N assumed
  μ=0.30); S3 bought per-channel selectors == 0; S3 selector features on a 0.4 mm
  nozzle; S4 full-map <30 s (1.10 s); S4 bought clutch path unaffordable (proves
  printed clutch required); S4 backlash within margin; S5 0/5 gates passed (honest
  status); S5 motor allowance does not fit.
- FAIL (design rejections, expected): none asserted-passing failed; the FAILs are
  the *consequences* encoded in the thresholds, not script failures.

## Assumptions

- 5.08 mm pitch, 4.68 mm body, 0.10 mm/side clearance, 40 mm stroke, 5 levels
  (Test09 params).
- Per-sweep friction μ=0.30, 0.1 N preload; head mass ~5–6 kg (Test09).
- $6/absolute and $3/ideal per-channel cost ceilings are the project's own.
- Motor/driver allowances are budget placeholders, not delivered quotes.

## What remains uncertain / next test

- **T11-A first** (one X1C print, ~45 min): the 2×4 fan-out fit coupon. If the
  0.47 mm web fuses, S3 density is dead — do this before any S3 drive CAD.
- T11-B (2×4 loaded engage/write/disengage dwell), T11-C (80-column bank friction
  sweep) qualify S3.
- T11-D/E (printed clutch + jam; multi-joint backlash) qualify S4.
- T11-F..J qualify the five S5 gates; S5 must not scale until F and G pass.

No architecture is promoted into `08-current-design/`.

## Links

- Source issue: DND-4
- Related: DND-6 Test11 cost/printability patch (cost/dnd6-...) and the
  selector-coupon PR #13 are separate, complementary Test11 artifacts.
