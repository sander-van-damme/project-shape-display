---
status: complete
builds-on: [DES-003, Q-005]
---
Question: can DES-003's calculated zero rigid-body neighbour motion be treated as sufficient isolation during 5x5, 10x10 and 20x20 updates?

Method: `analysis/a2_elastic_disturbance_check.py` is a bounded spring sensitivity model. It uses the design-calculated loaded-neighbour service load of 3.27 N and the Q-005 coupon proposal of 0.10 mm. For each region it counts perimeter cells and sweeps an explicit, unknown per-boundary-cell coupling fraction (1%, 5%, 10%). It also reports the coupling fraction that would consume the proposed gate at candidate stiffness values of 10, 32.7 and 50 N/mm. These candidate stiffnesses are sensitivities only; none is sourced or measured.

Calculated result: the single-neighbour full-load bound requires 32.70 N/mm, independent of region size. Under the perimeter-coupling sensitivity, the required stiffness grows with boundary size: at 5% coupling it is 26.16 N/mm (5x5), 58.86 N/mm (10x10), and 124.26 N/mm (20x20). At 10% coupling it is 52.32, 117.72, and 248.52 N/mm respectively. The 20x20 case therefore becomes unacceptable for modest coupling even if a 50 N/mm support stiffness were later demonstrated.

Verdict: NOT FALSIFIED, but OPEN and not qualified. DES-003 only establishes zero rigid-body displacement and positive geometric clearance. It does not establish elastic stiffness, actuation-to-neighbour coupling, miniature tipping margin, or wear drift. The previous “marginal” verdict and 50 N/mm plausible maximum were unsupported and are removed.

Evidence class: calculation over placed CAD geometry and design-calculated service load; coupling and stiffness are assumptions/sensitivity inputs. No physical validation, FEA, or material test was performed.

Cheapest decisive next action: run the existing coupon-B protocol with a loaded untouched neighbour and a displacement logger. Measure peak vertical/lateral motion and residual error for 5x5, 10x10 and 20x20 boundary sweeps; derive effective stiffness/coupling from the same traces, then test miniature displacement/tipping and cycle-induced drift. Until those measurements or a validated FEA model exist, regional isolation remains an open requirement.
