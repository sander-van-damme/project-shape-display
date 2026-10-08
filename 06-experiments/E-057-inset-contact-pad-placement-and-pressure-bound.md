---
status: complete
builds-on: [E-056, E-054, A-013]
---

# Inset pads trade robust pitch support against tooth overlap

Retain keyed/staggered guidance as the next geometric alternative. Stop refining
inset pads within E-054's 0.8-mm bearing length and inherited 0.40-mm minimum
tooth overlap: even the best pawl-fixed inset leaves only 0.02 mm of pitch
margin before shelf-edge loss. Neither carrier choice survives the explicit
0.10-mm edge-loss scenario at that overlap. A pawl-fixed pad with **reduced
0.20-mm overlap** is a conditional comparator, not a replacement that inherits
the prior geometry gate. Reopen with changed bearing geometry, justified smaller
edge loss, or evidence supporting the reduced overlap. No print or FEA release.

Input main `89404eb`. Analytical interval optimization and rigid equilibrium;
no measurements, calibrated manufacturing priors, compliant contact solution,
or complete mechanism implementation. This is parameter/contact-placement
comparison within A-013, not a new architecture. Run:
`python3 tools/curated-experiment-checks/E-057/pad_bound.py`.

## Geometry and optimum

E-056 places the seated pawl at x=[0,L], L=0.8 mm, with tooth force at h=2 mm.
Its full tooth interval is [o-r+delta,o+delta], delta∈[-e,e],
o=0.4+e+0.02 and r=max(0.8,o+e+0.1)+0.02. For e=0.15/0.35 mm,
the minimum right contact edge is a=0.42 mm and the left edge covers x=0.
These deterministic bounds include adverse common placement; no independence,
yield or probability is assumed. The widest e=0.60 case already fails packaging.

Compare an ideal isolated bearing pad fixed to the pawl versus fixed to the
rack. Non-pad surfaces are assumed recessed enough never to carry tooth load.
That relief and its manufacturing error are **not implemented**: actual pads
need vertical relief exceeding roughness, warp and elastic closure, and new
unload/transition checks. Pad edges are exact relative to their carrier in this
screen; additional edge error can only consume the reported margin.

For arbitrary nonnegative pressure, its centroid can reach either contact edge.
Support shelves have usable interval [d,L-d]. Equilibrium requires
`d <= x+h H/F <= L-d`; horizontal balance also needs friction or an explicit
link, with no friction coefficient established here.

For a pawl pad [m,L-m] and minimum contact width w, all placements require
`L-2m >= w` and `a-m >= w`. Thus the optimal guaranteed inset is
`m=min((L-w)/2,a-w)` and the signed pitch margin is m-d. Asymmetric pads
cannot improve this optimum: guaranteeing margin m requires both pad edges
inside [m,L-m], and the worst tooth edge still imposes a-m≥w.

For a rack pad of width w, choose center c as close to L/2 as the original
tooth permits: `c=min(L/2,o-w/2)` for these inputs. The guaranteed untruncated
margin is `min(c-w/2,L-c-w/2)-e-d`. A negative value rejects guaranteed
width/support; clipping at the pawl edge cannot restore both arbitrary-pressure
inset and the full width w. Increasing pad width only worsens the bound.

## Results

Signed pitch margins in mm; negative means the requested robust condition fails.
For nonnegative margin, maximum symmetric |H/F| from pitch balance is margin/2.

| Minimum overlap w | Placement e | Pawl pad, d=0 / 0.10 | Rack pad, d=0 / 0.10 |
|---|---|---|---|
| 0.40 | 0.15 | 0.02 / -0.08 | 0.02 / -0.08 |
| 0.40 | 0.35 | 0.02 / -0.08 | -0.15 / -0.25 |
| 0.20 | 0.15 | 0.22 / 0.12 | 0.15 / 0.05 |
| 0.20 | 0.35 | 0.22 / 0.12 | -0.05 / -0.15 |

The exploratory pawl pad [0.22,0.58] retains 0.20-mm worst-case overlap and
|H/F|≤0.06 at d=0.10, without assuming uniform pressure. This is conditional
static support only. At unchanged transverse width, halving overlap doubles
nominal average bearing pressure at the same force; local peak stress is not
bounded by this calculation. Neither width is a qualified printable/load-bearing
minimum. A pad creates another controlled surface on each of 6,400 pawls and
still supplies no unloaded capture, axial retention or return mechanism.
Complete head cost, proof/retry timing and regional isolation remain unchanged.

## Verification and next decision

Self-review: affine interval endpoints prove the continuous placement bounds;
1,001 placements per scenario supplement the proof with 36,036 reaction-sign
and moment-balance checks. Just-outside-margin loads fail; increasing the
pawl inset beyond the analytic optimum violates overlap or pad width. The
rack-pad generator checks containment in the original tooth (which shifts the
0.40-mm tight-bound pad off center). Deterministic search has no seed or
mesh convergence claim. Reproducible output is not retained.

Stop local pad optimization: preserving the current overlap does not resolve
robust support, and reduced overlap adds a new unqualified contact requirement.
The next useful comparison must implement keyed or staggered guidance with
unloaded retention and an affordable complete drive channel; another scalar
pad tolerance sweep cannot select A-013. No hardware reliability claim follows.
