---
status: complete
builds-on: [E-209, E-056, E-206]
---

# Released rocking toe retains keys, with load-dependent tilt and rack-web contact

**Keep rocking as a conditional lead; do not add an upper keeper or select
root tension as a cure for seating.** Releasing the writer permits retained
floating and tilted equilibria that E-209's imposed seated-pose bound cannot
represent. Some light-load states touch the rack web. Lowering the root can
itself rock the toe on its heel and a socket corner. Neither leaving a ledge
nor moving the rack by a fraction of a millimetre is a product failure by itself;
stage 02 establishes no numerical height-error limit.

Input main `6e0c268`; LAB-337. Evidence: local quasistatic elastic/contact
simulation, deterministic dimensional bounds and self-review. No physical
measurement, calibrated manufacturing distribution, material qualification,
independent reviewer, purchase or fabrication. Reproduce with Python, NumPy and
SciPy using `OPENBLAS_NUM_THREADS=1 python tools/curated-experiment-checks/E-210/contact.py`.
Generated JSON is disposable. Tested numerical package versions: NumPy 2.5.4,
SciPy 1.18.1; dependencies were installed only in run scratch.

## Released coordinates and finite contacts

Inherit E-208's finite toe, pocket, paired keys, ledges, heel, collar, curved
return and rack, through E-209's source. The toe now has free y translation,
z translation and pitch about the reference heel. The rack has free vertical
translation. **Its horizontal position and pitch remain constrained by an
assumed rack guide**, whose required lateral force and pitch couple are
reported, not qualified. There is no residual blade force in released solutions,
no toe cap or resident toe guide, and no friction credit.

Minimize `EI * U_normalized(toe pose) + W * rack height`, using E-209's
extensible rod for the reduced toe energy and its analytic end wrench for the
gradient. The root stays fixed at its bounded offset; freeing the toe does not
free the root. Both nominal (L,a,t)=(12,.3,.4) and shorter/thicker
(11.5,.25,.45) returns are .8 mm wide. Lengths are mm, loads N and modulus MPa.
Modulus E=700/2200 remains an assumed elastic range, not an allowable.

Convex separating-axis inequalities enforce nonpenetration against the actual
finite ledges, heel and socket floor/end walls. Both rotated rack-pad top corners
must lie below the rack shelf; their y coverage is checked. The finite rack web
is also an obstacle. Omitting it produces a false light-load solution with
**.0663 mm penetration** in a nominal-geometry +.1-mm root / .01-N case.
That omitted-contact construction is rejected; the executable keeps the web.

After optimization, independently reconstruct actual pocket-bearing toe pieces,
leaf sections, all rack teeth and frame solids and check self/interference, collar
continuity and coherent adjacent-row geometry. Vertex/face contacts, including
both ends of touching flat faces, furnish possible compressive reactions.
Nonnegative least squares balances both toe forces, toe pitch moment and rack
vertical load. Thus the reported reactions establish a feasible distribution,
not unique contact pressure or finite contact stress. Both keys/side supports
are combined in the plane; roll, yaw and unequal transverse bearing are absent.

The rack guide's horizontal force and couple close its remaining equilibrium.
For an external vertical load at y=.8 or 1.2, the reported guide couple includes
the offset from the actual pad contact and any web reaction. Flat-pad pressure
is indeterminate; the selected feasible pressure distribution can change that
couple. The guide may not be silently deleted while retaining these results.

Zero load is an ideal limit omitting toe/rack weight. The unloaded rack can sit
at any noninterfering height above the pad; report the lowest touching height
as a gauge, not a uniquely selected gravitational equilibrium. Positive W
includes all assumed rack/miniature load. W=0/.1/1/10 are comparison scenarios,
not new product service requirements.

## Bounds and results

The core sweep uses y-root offsets −.1/0/+.1 and z offsets −.2/−.1/0/+.1,
with nominal socket end play .1, no socket translation and .2-mm key depth.
The unbiased assembly uses z=−.1…+.1; a nominal −.1-mm tensile setting with
±.1 error uses z=−.2…0. These are overlapping bounded sets, not independent
manufacturing samples. Common offsets can affect an entire 40-finger comb.

All **192 core equilibria** retain positive key overlap, including one exact
seated reconstruction after optimizer stagnation. The 16-segment sweep gives:

| Return / root setting | Rack rise range (mm) | Minimum embedded key depth (mm) | Maximum released-state fiber strain |
|---|---:|---:|---:|
| Nominal / unbiased | approximately 0–.1000 | .1000 | .693% |
| Nominal / tensile | approximately 0–.0550 | .1529 | 1.466% |
| Shorter/thicker / unbiased | approximately 0–.1000 | .1000 | .948% |
| Shorter/thicker / tensile | approximately 0 | .2000 | 2.107% |

These are sampled local equilibria, not bounds over every intermediate error.
The unloaded centered +.1-mm root reproduces E-209's stress-free .1-mm rise and
.1-mm remaining overlap. Finite geometry, not separation from a ledge alone,
determines retained capture. No scenario loses capture or reaches a search bound.

At root (−.1,+.1), E=2200 and W=.1 N, 64-segment holdouts give nominal /
shorter-thicker rack rise **.023709/.025568 mm**, key overlap
**.185596/.184361 mm**, pitch **−.031789/−.034495 rad** and fiber strain
**.1175/.1313%**. The rack pushes .1 N down on the pad; the front ledge supplies
.055638/.037687 N and the return supplies the rest upward. Rack-web normal
reactions are **.004225/.008217 N**. The assumed rack guide must react those
horizontal forces and, for load y=.8/1.2, couples of −.02051/+.01949 N mm
(nominal) or −.02660/+.01340 N mm (shorter/thicker). These small computed forces
do not qualify friction, wear or guide stiffness. At W=10 N both holdouts seat.

Tensile bias is not equivalent to flat seating. For nominal geometry, centered
root z=−.1, E=2200 and zero load, refinement to 128 segments gives **.057275 mm
rack rise**, .027238-rad pitch, **.150922 mm key overlap** and .7006% strain.
The toe bears on the rear heel and a socket corner. The shorter/thicker control
stays flat in the same case. This is a geometry-dependent contact result, not
a blanket rejection of tension or a claim that .057 mm violates a requirement.

An additional **48 fit cases** use nominal return geometry at E=2200,
end play .07/.13, socket translation ±.05, key depth .15/.25, root offsets
(−.1,+.1)/(+.1,−.2), and W=0/.1/10 N. All retain keys; minimum embedded depth is
**.0500 mm**, maximum rack rise .1000 mm and maximum released strain 1.578%.
These do not cross every fit with both geometries/moduli or cover angular,
roughness and shape error. A .05-mm rigid embedding is not a qualified load
bearing area. The .0055-mm release-path reserve in E-208 remains unresolved.

## Verification and evidence limits

The source checks exact stress-free translation, energy/work derivatives in
all four released coordinates (largest error **1.51e−10** in N or N mm),
analytical separating-axis/contact controls and a simple tipping counterexample.
It preserves the omitted-web collision as a failure regression. Reaction
certificates use actual contact points independently of the optimizer's gap
Jacobians. Contact-pressure distributions remain nonunique.

Sixteen 32/64-segment holdouts cover both returns, root (−.1,+.1)/(+.1,−.2),
E=2200 and W=.1/10. Maximum toe-coordinate change is **1.59e−5 mm/rad**;
maximum rack-height change is **4.17e−6 mm**. Maximum relative strain change
is .46%. Separate 32/64/128-segment tensile-bias holdouts expose the tilted
nominal branch above: 64→128 changes height by .000109 mm and strain by .052%.
These checks refine particular states, not all extrema or model discrepancy.
Twenty-two refined states each test 52 deterministic directions/step sizes
(26 directions at 1e−5/1e−3 mm or rad); only nonpenetrating perturbations are
compared, and none lowers energy by more than 1e−8 N mm. This is a local check,
not a rigorous stability certificate.

Four compliance-removal traces use nominal geometry, n=32, E=2200,
root (−.1,+.1)/(+.1,−.2), W=0/.1 and eleven writer-stiffness settings
1000→0. A hypothetical writer spring restrains the three toe coordinates;
its reactions are explicitly included and vanish at the final state. All 44
sampled finite poses clear and remain keyed; final coordinates agree with
direct released solves within **4.62e−6 mm/rad**. Maximum wrench residual in
these traces is **5.57e−6** in mixed N/N mm components. This is an elastic
quasistatic continuation witness, not the actual blade-release mechanism,
a continuous collision certificate, damping model or dynamic support transfer.

One core SLSQP solve stagnates within 2.4e−9 mm/rad of perfectly aligned faces
(shorter/thicker, centered +.1-mm root, E=700, W=1). The code explicitly uses
the exact zero pose only after an independent nonnegative reaction certificate
and feasible perturbation check; its wrench residual is <2e−17. It does not
label the optimizer failure as convergence. Other solver failures remain fatal.
All 262 released/refined equilibria and 44 continuation states were reconstructed
with the final finite-body and self-interference checks. Maximum released-state
wrench residual is 6.33e−7 in mixed N/N mm components. SAT/prism checks permit
at most 2e−7-mm numerical penetration; reaction acceptance is 2e−5 in mixed
N/N mm components. These are numerical tolerances, not hardware margins.

The optimizer searches y∈[−.3,.3], z∈[−.05,.4], pitch∈[−.12,.12] and rack
height∈[−.3,.8]. Accepted equilibria must lie strictly inside these numerical
bounds; no reaction is credited to them. The search is local. Mesh checks,
force balance and sampled feasible perturbations do not prove uniqueness,
absence of distant buckling branches, impact safety or a basin of attraction.
The finite solids are rigid except for the homogeneous planar return. Frame,
key, pad and rack compliance, roughness/friction, manufacturing angular error,
spatial warp, first-layer effects, anisotropy, creep, fatigue and wear remain
unqualified. No arbitrary stochastic distribution, cell yield, board yield or
lifetime is inferred. E-209's full writer-path peak strains remain applicable;
the smaller released-state strain does not replace them.

## Disposition and machine comparison

No tested result establishes a need for another 6,400 upper keepers. No result
establishes a reliable manufactured machine either. The comparison remains:

| Construction | What this evidence changes | Burden still owed |
|---|---|---|
| Rocking comb | Finite released support can retain the keys without an upper keeper; tensile bias can rock as well as preload | 6,400 returns/toes/pockets, 12,800 keys; socket margin, rack guidance, writer fit and three controlled planar toe coordinates |
| E-054/E-056 slider | Grounded seated support remains the simpler control | 6,400 separate pawls/guide fits, return/capture and pressure robustness |
| E-206 longer torsion lead | Still a materially different return/control option | Lip clearance, positive yaw retention and stock/length tradeoff; no released support qualification |

Do not add tensile registration as a default: E-209 already finds 3.44/4.31%
withdrawal strain and 2.41–7.56/4.71–14.80 N model force at its adverse −.2-mm
edge. Here the released contact state also disproves an assumption that tension
necessarily flattens the toe. These are scoped elastic predictions, not strain
allowables or measured forces.

There is no updated BOM, timing pass or new purchased component. The 160 comb
placements, ~6,400-cell consequences and <30-s complete update requirement
remain. With the inherited illustrative 6-s overhead, 40/80/160 heads still
allow strictly <.15/.30/.60 s per cell including acquisition, supported motion,
proof, departure, settling and bounded retry. A changed light-load pose makes
readback of commanded height or nominal blade closure insufficient support
proof; false acceptance and recovery are not solved by equilibrium existence.

**Next discriminator:** synthesize a more generous seat and reusable blade fit
around the released poses, including the rack web and its guide reactions.
Compare shortening/chamfering the toe's web-facing corner against retaining
that contact; check positive key capture, released equilibria and the complete
rock/withdraw/return path together. Keep unbiased root setting as the control.
Stop or redirect if retaining the advantage needs a resident precision guide,
if fit changes remove key capture, or if writer/return strain and force erase
the shared-comb benefit over the slider/longer-torsion controls. No print yet:
finite fit/topology synthesis is more informative than calibrating one nominal
leaf. No new fundamental principle or broad search saturation is claimed.
