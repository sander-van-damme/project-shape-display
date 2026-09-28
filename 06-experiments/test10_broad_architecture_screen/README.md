# Test 10 — broad architecture scale screen

## Question

Which architecture families survive the cheapest full-scale count, information,
timing and bought-selector checks before mechanism-specific prototyping?

## Method and evidence level

`model.py` performs transparent arithmetic at 80×80 cells, five height states
and a 30 s boundary. It reports information lower bounds, tile counts, station
budgets and selector-cost sensitivity. These are **calculated bounds under stated
assumptions**, not simulated or measured mechanism performance. A quoted dwell
does not include reset, travel, settling or recovery unless explicitly stated.

Run from this directory with Python 3.11+:

```bash
python model.py
python checks.py
```

## Results

- 6,400 cells at five states contain at least 14,860 independent bits; a simple
  three-bit representation carries 19,200 bits.
- A cell-serial writer needs more than 213 completed cell transactions/s before
  any overhead.
- At an illustrative 0.40 s complete station dwell, one-row parallelism consumes
  32.0 s before reset; four rows consume 8.0 s. The dwell is an assumption, not
  evidence that a mechanism can achieve it.
- Sixty-four independently isolated 10×10-cell tiles cover the board.
- Four unary threshold decisions per cell require 25,600 passive decisions. This
  may be printable, but it makes programming and defect count explicit.
- Even unusually cheap bought selectors scale badly: 6,400 at $0.50 already cost
  $3,200. Selection must therefore be printed/passive, heavily shared, or moved
  into a reusable programmer.

## Consequence

The calculation does not select a design. It rejects purchased per-cell
selection and ordinary cell-serial writing on scale alone, and focuses physical
work on parallel readout, shared power, passive retention and tile isolation.
