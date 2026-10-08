---
status: complete
builds-on: [E-052, A-013]
---

# Grounded pawl guide: packing bound

## Decision

Reject the **fixed rear guide in the same plane** at E-052's middle and wide
error bounds. Even a zero-length guide requires 5.25 mm at the middle bound,
exceeding 5.08-mm pitch. E-052's 4.89-mm witness is still a valid tooth/pawl
section, but cannot be extended into this grounded-guide embodiment. Stop
same-plane middle-bound head/linkage design. Retain A-013 only for changed
packaging (out-of-plane supports or staggered cartridges) or evidence supporting
smaller error. The tight scenario merits geometry work only conditionally;
no printing, complete machine selection or service-load qualification follows.

Input main `6c74a31`. Evidence: exact interval geometry and static force/moment
balance, not CAD, calibrated manufacturing priors, contact simulation or physical
measurements. This is a missing-support screen within one topology, not new
architecture discovery. Scope deliberately excludes side-cheek guides projecting
out of the tooth plane; they require separate 3D packing and interference checks.

## Model and independent bound

Run `python3 tools/curated-experiment-checks/E-053/guide_bound.py`.
It imports E-052's swept evaluator and replays its twenty unequal five-state
transitions for fitting witnesses. Nine deterministic combinations use error
`e=0.15/0.35/0.60 mm` and engaged guide span `g=0/0.4/0.9 mm`; no random seed.
Zero span is a rejection lower bound, never a functional bearing.

Reuse E-052's web minimum 1.6, pawl length minimum 0.8, reach minimum 0.8,
residual tooth overlap 0.4 and clearance `c=0.1 mm`. Rack and pawl placements
are ±e/2 relative to the bank; common bank placement is ±e/2. The fixed guide
is ideally registered to that bank (additional guide error can only tighten
this screen). All bounded placements are tested, not independent random draws.
The guide must stay to the right of the entire vertically travelling tooth
sweep. It contacts the pawl's rear tail above and below, grounding vertical
force and its overturning moment; a bottom-only sliding shelf is insufficient.

With nominal overlap `o`, reach `r`, pawl length `L`, and nominal tooth tip `t`:

- Guide front must be at least `t+e/2+c` to clear the adverse rack position.
- Engaged rear pawl edge can be `t-o+L-e/2`.
- Hence available guide span is at most `L-o-e-c`; necessary `L≥o+e+c+g`.
- From E-052: `o≥0.4+e`, `r≥max(0.8,0.5+2e)` and
  `W=1.6+r+L+3e+0.2` including the withdrawn pawl and bank margins.

Choose minimum feasible dimensions to obtain the exact lower bound for this
ideal class. Guide housing walls, attachment, retention stops and release links
are omitted, so a width pass is only a necessary condition. Retraction increases
tail coverage; the engaged state is limiting. A real finite guide can also lose
front coverage on withdrawal and needs an extended bearing track; this lower
bound does not establish its complete motion or housing geometry.

| e (mm) | W at g=0 | W at g=0.4 | W at g=0.9 | Maximum guide span within pitch |
|---|---:|---:|---:|---:|
| 0.15 | 3.85 | 4.25 | 4.75 | 1.23 |
| 0.35 | 5.25 | 5.65 | 6.15 | −0.17 |
| 0.60 | 7.00 | 7.40 | 7.90 | −1.92 |

Negative span means the tail ends before the permissible guide front.
E-052's particular middle witness has `0.8−0.77−0.35−0.1=−0.42 mm`.
Even increasing its length cannot rescue this class within pitch. For the
illustrative g=0.9 allocation (not a qualified FDM bearing dimension), the
packing threshold is `e≤(5.08−3.7)/7=0.19714 mm`. Sensitivity to the guide span
is one millimetre of width per millimetre of span once that constraint is active.
No yield or process capability is inferred from these competing bounds.

## Load support and evidence limits

A grounded sliding pawl needs an upward near reaction and a downward far
reaction. For load F a distance a outside the near contact and contact separation
d, `Rfar=F a/d`, `Rnear=F+Rfar`. The tight g=0.9 witness has o=0.55,
r=0.8, L=1.7; taking a=0.8 (adverse overlap plus clearance) and the optimistic
point-contact separation d=0.9 gives, at F=10 N, upward 18.89 N and downward
8.89 N. Loads 1/10/100 N retain E-050's explicitly assumed sensitivity cases;
they are not new product requirements. Finite pads reduce separation, increase
reactions and require bearing area and housing bending checks. No stress or
creep pass is claimed. As d→0 reactions diverge for nonzero a: the zero-span
packing bound cannot carry this eccentric load.

All 6,400 pawls require grounded bearing surfaces and retention; guides cannot
be omitted from E-050's repeated-interface, assembly and cost accounting.
An e=0.35 common registration scenario can invalidate a bank, not just isolated
cells. Friction, dimensional shape error, warp, anisotropy, roughness, creep,
wear and seams are not solved. There is no timing improvement: E-050/E-051
remain the complete-system comparators and head cost remains open.

Self-review checks force and moment conservation, the independent width-budget
expression for maximum guide span, adverse placement endpoints and both sides
of the g=0.9 packing threshold. E-052 supplies the swept tooth/pawl rejection
checks. Exact affine interval bounds need no mesh/time-step convergence; this
is not independent review or verification of an assembled guide. The next
useful discriminator is a genuinely 3D grounded-guide/retention embodiment and
its full channel bill of materials, not another refinement of this width grid.
