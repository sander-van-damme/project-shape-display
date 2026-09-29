# DND-111 — Analytic bound on the A1 writer/reader rate + single-cell read

> **CORRECTED BY DND-113 (this ADR is superseded on the READ axis).** The DND-112
> independent audit found that §3.3's single-cell read claim is wrong: the reader
> reads the column top face, so the read gap is state-dependent (42 mm over a down
> cell, not 2 mm), and §3.3's "registration ±0.264 mm" is **not** the binding read
> limit. See [`dnd113-a1-read-mechanism.md`](dnd113-a1-read-mechanism.md). The
> **rate** bound (§3.1–3.2) stands, with the DND-113 per-line ramp correction to
> the full cycle (16.278 s ideal → **18.278 s** honest at 8 heads). Read §3.3,
> §4 and §5 below as historical; they are superseded.

- **Issue:** [DND-111](/DND/issues/DND-111) (CTO). Parent gate: [DND-110](/DND/issues/DND-110).
  Program: [DND-102](/DND/issues/DND-102).
- **Architecture:** A1 binary-latch + shared writer/reader,
  [`10-reliability-mask/`](../08-integrated-designs/a1-reliability-first/README.md).
- **Criteria of record:** [`02-design-criteria/README.md`](../02-design-criteria/README.md)
  (strengthened by [DND-103](/DND/issues/DND-103)).
- **Evidence class:** **CALCULATION over sourced component-class limits + CAD**.
  No print, no purchase, no measurement ([DND-27](/DND/issues/DND-27)). No board
  contact ([DND-32](/DND/issues/DND-32)).
- **Deliverable:** [`10-reliability-mask/analysis/a1_writer_rate.py`](../08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py),
  [`10-reliability-mask/scad/a1_reader_head.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_reader_head.scad),
  the updated model/checks/README, and this ADR.
- **Outcome: (a) BOUNDED.** The decisive number is now a bounded calculation,
  not an unconstrained placeholder.

## 1. Why this issue exists

The DND-110 terminal gate found A1 passes every *printable* gate, but its whole
timing and reliability advantage rested on a bare assumption in
`reliability_mask.py`:

```python
HEAD_RATE_CELLS_S = 1000.0   # 1 ms/cell per head
```

The design named prototype A/B as its physical kill test; DND-27 forbids that
coupon. So the honest next step (the DND-54 pattern) was to decide the rate
**analytically** from sourced kinematics + CAD.

## 2. Method

[`a1_writer_rate.py`](../08-integrated-designs/a1-reliability-first/analysis/a1_writer_rate.py) bounds
four independent per-cell limits and takes the binding one:

1. **Stop-and-go** kinematics: move one pitch, stop, settle.
2. **Fly-over traverse**: continuous traverse at speed v, one cell per pitch/v.
3. **Write actuation**: the over-centre latch snap (device-class snap-trigger
   3 ms; pessimistic full 6 mm sweep 13 ms).
4. **Read integration**: reflectance channel integration + ambient rejection + ADC.

The per-cell time for a pass is `max(traverse, actuation_or_read) + settle`; the
per-head rate is the slower of the write and verify passes; the full cycle is
`cells / (heads · rate)` plus the non-motion stages.

Constants and evidence classes (all in the module):

| Constant | Value | Class |
|---|---|---|
| X1C max toolhead speed | 500 mm/s | sourced (X1C spec) |
| X1C max acceleration | 20,000 mm/s² | sourced (X1C spec) |
| Repo-prior gantry speed | 1,500 mm/s | assumption (GALVO_OR_RAIL) |
| NEMA17-class usable speed | 600 rpm (400 mm/s on 20T GT2) | sourced-class |
| Read integration | 50 µs (200 µs conservative) | assumption |
| Photodiode rise | 100 ns | sourced-class |
| Latch snap-trigger pulse | 3 ms | device-class |
| Latch full-sweep | 13 ms | calc from CAD (6 mm @ 0.5 m/s) |
| Settle | 1 ms | assumption |

## 3. Result

### 3.1 The rate is traverse/actuation-bounded, ~164 cells/s/head

| Kinematics | Rate (cells/s/head) | Note |
|---|---:|---|
| Stop-and-go @ 20 m/s² | 30 | **excluded** |
| Stop-and-go @ 100 m/s² | 90 | **excluded** |
| Fly-over 0.5 m/s snap-trigger | 90 | conservative |
| Fly-over 1.0 m/s snap-trigger | **164.5** | **primary design point** |
| Fly-over 1.5 m/s snap-trigger | 228 | optimistic |
| Fly-over 1.0 m/s full-sweep | 71.4 | pessimistic |

The placeholder **1,000 cells/s overstates the achievable rate by 4.4–14×**.
Stop-and-go is excluded outright: at 5.08 mm pitch it is 30–90 cells/s, i.e. a
1,000 cells/s step rate would need ~5.08 m/s, a 20T GT2 pulley at ~7,620 rpm.

### 3.2 The full cycle still clears < 30 s

Re-derived DND-103 stages at the primary design point (8 heads, 1.0 m/s,
snap-trigger):

| Stage | Seconds |
|---|---:|
| Digital map processing | 0.05 |
| Physical mask generation | 0.00 (no mask) |
| Mask transport / indexing | 2.00 |
| Display reset | 3.00 |
| Broadcast lift / write | 4.864 |
| Settling / locking | 1.50 |
| Verification | 4.864 |
| **Full cycle** | **16.278** |

Head-count sweep at 1.0 m/s (write + verify + reset + settle):

| Heads | 1 | 2 | 4 | 8 | 12 | 16 |
|---|---:|---:|---:|---:|---:|---:|
| snap-trigger cycle (s) | 84.4 | 45.5 | **26.0** | **16.28** | 13.0 | 11.4 |
| full-sweep (pessimistic) cycle (s) | 135.1 | 70.8 | 38.7 | **22.61** | 17.3 | 14.6 |

The map clears < 30 s at **8 heads (16.28 s)** and even at **4 heads (26.0 s)**
on the primary model; the pessimistic full-sweep toggle still clears at 8 heads
(22.61 s). Heads are cheap printed bodies, so the honest rate is bought back with
parallelism rather than an over-optimistic number.

### 3.3 Single-cell read resolution reduces to registration

[`scad/a1_reader_head.scad`](../08-integrated-designs/a1-reliability-first/scad/a1_reader_head.scad)
models the reader over a 3×3 cell patch with the aperture at worst-case corner
alignment. A 2 mm aperture at a 2 mm working gap makes a **3.072 mm spot**:

| Check | Value | Verdict |
|---|---:|---|
| Spot fits 3.60 mm top face (centre-aligned) | reach 1.54 ≤ 1.80 mm | fits |
| Spot at worst-case cell corner | reach 2.172 mm > 1.80 mm | does not fit |
| **Required head-to-cell registration** | **±0.264 mm** | the real limit |
| Gap for zero-error corner fit | 5.77 mm | not used |
| Up/down contrast SNR (50 µs) | ~1,460 (gate 5.0) | trivially clears |

Photometrically a single wrong cell is easy to see; **geometrically** it is
resolved only if the head is registered to cell centres within **±0.26 mm**.
That is exactly the classic 2-axis gantry-registration question the README
already flagged, now with a number.

## 4. Outcome

**OUTCOME (a) BOUNDED — on the RATE axis only (corrected by DND-113).**
The A1 writer rate is analytically bounded from sourced component-class
kinematics + placed CAD. The dominant limit is gantry traverse (with the latch
snap binding only if the gantry is pushed to 1.5 m/s). The full map clears
< 30 s including verification at 8 heads (**18.278 s** after the DND-113 per-line
ramp correction; this ADR's 16.278 s omitted it).

**The READ axis is NOT resolved.** DND-112 showed §3.3 is wrong: the reader's
fixed height makes the interrogated gap state-dependent, and the ±0.264 mm
registration number is an up-state-only figure, not the binding limit. The read
residual is the **state-dependent standoff** (down-state spot 24.5 mm = 4.82
pitches; up neighbours swamp the pocket ~441×). See
[`dnd113-a1-read-mechanism.md`](dnd113-a1-read-mechanism.md).

The residuals are:
1. **State-dependent read standoff** — the decisive read/verify problem; fix is a
   common-height read target (proposed) or a priced per-line Z refocus.
2. **As-built gantry registration** (±0.26 mm over 406 mm) — now a *secondary*
   read concern once a common-height target exists.
3. **As-printed latch snap force** at the writer contact — a tolerance question
   (the state itself is exact by hard stop).

**DND-110's "SUCCESS-eligible on the rate axis" does NOT extend to the
read/verify axis until the read target is settled.**

## 5. What was changed

- `reliability_mask.py`: `HEAD_RATE_CELLS_S` is now derived from
  `a1_writer_rate.achievable_rate()`; the placeholder is retained as
  `PLACEHOLDER_HEAD_RATE_CELLS_S` for provenance. A1 timing stages updated from
  8.8/8.8 to 4.864/4.864; full cycle 24.15 s → 16.278 s.
- `reliability_mask_checks.py`: the old `rate == 1000.0` check is replaced by
  the derived value plus **10 new DND-111 checks** (50/50 total).
- `a1_writer_rate.py` (new): the derivation + outcome.
- `a1_reader_head.scad` (new) + `render_a1_cad.py`: CAD validation of the read
  geometry (reader-head mesh watertight, spot-fits-top-face assertion).
- `README.md`: sections 4.2, 4.2a, 4.3, 4.7, 7, 9, 10 updated; headline
  full-map time 24.15 s → 16.28 s; the decisive falsifier re-stated as the
  registration tolerance.
- `.github/workflows/ci.yml`: DND-111 step added.
- `08-current-design/` and `09-low-cost-variant/` untouched.

## 6. Residual uncertainty

- **DND-113 correction:** the decisive read residual is the **state-dependent
  standoff** (down cell read at ~42 mm, drowned by up neighbours ~441×), not
  ±0.26 mm registration. See
  [`dnd113-a1-read-mechanism.md`](dnd113-a1-read-mechanism.md).
- The reflectance pair (0.80/0.15), aperture, LED power and ambient level are
  assumption/sourced-class, not measured.
- The sourced component-class limits (X1C speed, NEMA17 speed) are
  representative of the class, not of the exact selected part.
- The latch snap-trigger pulse (3 ms) is device-class; the full-sweep case
  (13 ms) is the conservative bound, and the design clears even that.
- As-built registration (±0.26 mm) and as-printed snap force are unmeasured
  (DND-27).

Nothing here is a physical validation.
