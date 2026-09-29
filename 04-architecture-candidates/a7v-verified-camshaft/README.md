# A7-V — verified shared-camshaft bank (SHA-8 challenger)

> Challenger family for SHA-8. Evidence class: CALCULATION over sourced-class
> figures + repo CAD priors. No print, purchase or measurement (DND-27).

## Mechanism (one paragraph)

A7 base (`reliability_mask.py` A7: 1 bought actuator, $158 parts, 13.05 s,
6,400 silent): one long printed camshaft per bank (8 banks) rotates to a set
angle per map; cam lobes push/clear each cell's binary latch. **A7-V adds an
A1-class cell-resolving verify pass**: a travelling reader bar (or equivalent
scan) reads every cell at a common-height target (DND-114/115 pattern) and a
failed bank is re-homed and replayed. Structural silent set goes 6,400 → 0
*iff* the reader resolves a single cell and retry converges.

## Why this family (and not the others)

- Headroom vs A1 ($181 parts) is largest: A7 $158 → **$23 headroom**.
  Runners-up leave less: A4 $171 → $10, A6 $179 → $2, A3 $187 → negative,
  A2 $224 / A5 $213 → negative. S1-B/S2/S3/S4 paths were already screened:
  S1 force + mask-write ≥500 channels, S2 surprise-media, S3 killed
  (1.27 mm row land), S4 64×$6 bought clutch = $384.
- A7 keeps the fewest bought actuators (1) and a bank-local retry boundary,
  so it is the only base where adding verification could plausibly stay under
  A1 on cost.

## Kill criteria (stated up front, cheapest first)

- **K1 cost:** A7-V purchased parts must beat A1 ($181). Kill if verified
  total ≥ $181 (meaningful beat needs ≤ ~$171, i.e. ≥$10 clear).
- **K2 silent-error:** reader must resolve a single cell at one fixed
  standoff with ≥2× on/off contrast (DND-115 gate). Kill if only bank-coarse
  readback is affordable (that is A5: 6,392 silent remain).
- **K3 timing:** write + verify + reset + transport + settle < 30 s. Kill if
  the verify pass needs a per-cell Z stroke or a single slow scan row.
- **K4 density:** 80 lobes/shaft at 5.08 mm pitch, shaft ≥406 mm (≥2 printed
  segments in a 256 mm volume) must hold ≤0.1 mm lobe repeatability. Kill if
  joint backlash + torsion exceeds budget analytically.

## Binding-gate screen

See `06-experiments/test15_a7v_challenger_screen/screen_a7v.py`. Result:
**killed on K1** ($208–219 vs $181); K3 passes only with an 8-head reader
(+cost); K4 is a second independent kill risk. Decision record:
`07-evidence-and-decisions/sha8-a7v-challenger-verdict.md`.
