---
status: complete
builds-on: [E-112, A-018]
---

# Park the side-bay thermal strut after supported containment closure

Input main `aac9fff`. **Park these short-stroke thermal-strut embodiments.**
Guided rolling and sliding-seal packages close a conditional liquid cycle but
exceed the inherited side bay once roof/duct and return are included. Neither
establishes a repeated process or cost advantage over a dry mechanical stop.
This excludes the studied implementations, not thermal support in general.
No thermal optimization, fabrication or procurement follows.

Reproduce: `python3 tools/curated-experiment-checks/E-113/containment.py`.
Two topologies; deterministic bounds, no random seed. Units: mm, N, MPa, s.
Evidence: analytical geometry, reduced quasistatic calculations and sources;
no measurements, nonlinear film/contact solution or hardware qualification.

## Guided boundary, finite duct and return

E-112 puts liquid **below** its U. Positive pressure pushes the inner leg away
from an ordinary inner piston and the outer leg away from an outer bore.
Those supports cannot simply be appended to that liquid domain. Generate liquid
**above** the U, under roof `T=S/2+h`, h=.2. Retain b=a+2ρ, ρ=.2,
`zc=(q−S/2−.2)/2`, `−S/2≤q≤S/2`. The dry t=.05 offset has radius ρ+t,
inner radius a−t and outer radius b+t. A piston `r≤a−t` extends below the entire
fold sweep; a bore `r≥b+t` backs the outer leg. Positive pressure seats both.
The free fold still needs tensile/bending equilibrium; circular geometry and
constant thickness are not a constitutive solution or a pressure-stability pass.

Liquid volume and effective area are
`V=πb²T−πa²q−π(b²−a²)zc+π²(a+ρ)ρ²`, `dV/dq=−A`,
`A=π(a²+b²)/2`. The frozen core spans head to grounded roof, minimum gap .2;
head film is compression-loaded between them. Jaw guides carry vertical load.
At assumed H=10 tan30°=5.774 and effective solid stress σ=5, use
`am=sqrt(H/(πσ))+t+2e`, `ar=sqrt(H/(πσ))+t` for adverse opposite-radius errors.
σ is a whole-strut hypothesis, not an alloy strength or creep allowable.

Capsules have parallel horizontal axes at separate depth levels, fixed roofs
aligned, center separation D=outer diameter+.4. Generate a roof channel .8 wide,
hd=.2−e high, centered .3+hd/2 beyond each chamber roof. Two end ports connect
the channel to the chamber centers; moving boundaries never cross them.
The exact union volume of channel and overlapping rectangular ports is
`.8 hd(D+.6+hd)`. Roof allowance is .3+nominal .2+.3 cover=.8, replacing the
old unplumbed .3 wall. Body span includes deepest fold, .1 dry clearance and
this roof. Heater, insulation, attachment corners and seats remain additional.

Free reservoir travel accepts main stroke s=.45+e and both signs of ±ηV:
`Sr=(Am s+2ηV)/Ar`. Since Vr(Sr) is affine with slope Kr, solve
`Sr=[Am s+2η(Vm(s)+Vr(0)+Vduct)]/[Ar−2ηKr]`; reject nonpositive denominator.
This closes **liquid** inventory, not volume accommodation through a frozen duct.

A dry coaxial spring behind the reservoir transfers preload to ground: .08 wire,
.8 mean diameter, eight active/two inactive turns, assumed G=70,000.
`k=Gd⁴/(8D³n)=.0875 N/mm`; installed minimum length .9 leaves .1 above solid
height; maximum length .9+Sr; free length adds .03/k for .03-N preload.
It is an explicit candidate, not a qualified spring. Reservoir pressure is
`pr=(.03+kx)/Ar`, x travel from minimum-force endpoint. Virtual work independently
checks `Fm=pm Am` against reservoir spring work with area-ratio displacement.

## Different encapsulation: sliding seals

Replace films with piston O-rings and finished bores. A deliberately optimistic
custom .7 seal section, 15% radial squeeze, .15 core-to-groove ligament,
groove width 1.3 sections and .2 end lands gives piston radius
`sqrt(H/(πσ))+.15+.85(.7)` before error. This is not a catalog-qualified seal.
Liquid is `A(h+S/2−q)`; the swept seal band stays below the roof ports.
The same generated duct, accommodation and return apply. Hoop cycling disappears,
but breakaway, wear, alloy compatibility and precision bore manufacture enter.

At net gland error .05, squeeze spans 7.9–22.1%; at .15, −6.4–36.4%, including
lost interference. These are bounded scenarios, not X1C accuracy predictions.
With seal drag f, `(Fspring−f)/Ar≤pr≤(Fspring+f)/Ar`; increasing preload by f
preserves minimum pressure. f=0/.03/.3 are assumed bounds. The .3 case requires
about 1,779-MPa coil shear by the Wahl correction: different spring geometry
or evidence is needed. Even the rolling .05 case's 491-MPa coil stress has no
qualified fatigue margin. Bore finish, ovality, swelling and pressure extrusion
remain outside this model; printed layer resolution establishes none of them.

## Packing, equilibrium and failure results

E-112's centered 1-mm rack and .15 clearance leave a **1.89-mm axial side bay**.
Bodies and installed reservoir springs are end to end; no nesting, remote
preload or force-turning linkage is silently credited.

| Route / e | Sr | Inventory mm³ | Bare body | Body + spring | Bay overrun |
|---|---:|---:|---:|---:|---:|
| Rolling / 0 | .687 | 5.755 | 2.137 | 3.724 | 1.834 |
| Rolling / .05 | .889 | 6.598 | 2.339 | 4.128 | 2.238 |
| Rolling / .15 | 1.430 | 8.781 | 2.880 | 5.210 | 3.320 |
| Sliding / 0 | .553 | 5.891 | 2.863 | 4.315 | 2.425 |
| Sliding / .05 | .693 | 6.671 | 3.003 | 4.596 | 2.706 |
| Sliding / .15 | 1.046 | 8.630 | 3.356 | 5.303 | 3.413 |

All six packages fail this placement even without the spring. At e=.05,
η=0→.1 changes rolling Sr .617→1.224 and inventory 5.976→7.365; zero excursion
does not rescue body+spring. Rolling hoop cycle excursion is still 53.3% at the
middle case. Eccentricity .05/.15 is 10/30% of the .5 hardware convolution width.
These errors can repeat across a batch; there is no IID-cell yield inference.

For .5-s transfer, rectangular-duct Stokes flow with sidewall correction gives
`pm=pr±Δp`. Include straight port lengths; omit bend losses optimistically.
At e=.05, viscosity .002/.02/1 Pa·s gives Δp .000126/.001258/.06291 for rolling
and .000310/.003103/.15515 for sliding. Their minimum reservoir pressures are
.01235/.00523; thus the 1-Pa·s return has negative **gauge** main pressure.
This violates intended positive backing/return, not a prediction of cavitation
at that exact pressure. Higher preload or slower flow trades force/stress/time.
At e=.15 rolling loses positive return at .02 Pa·s, sliding even at .002.
Partial freeze, debris and non-Newtonian behavior invalidate the fully molten
calculation; these viscosity bounds are not material data or probabilities.

Melting before collet unloading requires 1.9255-MPa rolling main pressure.
Spring equilibrium extrapolates to 53.1-mm reservoir motion versus .889 allowed:
**the travel stop is reached**, not 53-mm physical travel. Sliding also reaches
its stop. Preload cannot support service load. Keep collet support through
melt/move/refill/freeze/proof and provide a separate catch for heater faults.
Stop contact does not establish seal pressure capacity.

If the roof duct freezes first, reservoir movement cannot relieve the chamber.
Constraining assumed 5% volume change at competing bulk-modulus bounds .1–30 GPa
would require elastic pressure 5–1,500 MPa. These are not alloy properties or
actual pressures: yielding, film expansion, cracks or voids intervene. A reopened
capsule must establish freeze sequence and sustained core creep; liquid-volume
closure and temperature readback cannot prove a solid load path.

Mechanical comparator: a grounded rectangular crossbolt holds the same sloped
jaw's H. A 1×1 contact/shear section requires nominal 5.774-MPa stress before
bending/concentrations. Collet unloads; bolt withdraws 1.15 in depth to clear a
1-mm-high jaw by .15; jaw withdraws .5. Reverse, seat and proof unload. Generated
intervals confirm bolt/jaw separation. The dry stop needs reset/addressing,
bearing/guide qualification and repair access, but no liquid boundaries, charge,
duct or freeze inspection. No complete-machine win is asserted; thermal
containment has not justified its extra burden against this simpler control.

## Material, process and repeated burden

Primary sources, accessed 2026-10-10:

- [Bellofram manual](https://damapi.marshbellofram.com/uploads/Bellofram_Diaphragm_Design_Manual_2022_7a922642c3.pdf), pp. 3, 24–25: pressure-side orientation, reversal damage and eccentricity guidance support backing/alignment requirements. They do not qualify our 50-μm film, alloy exposure or cycling. Its area formula remains different from the prescribed circular geometry (E-112).
- [Parker handbook](https://www.parker.com/content/dam/Parker-com/Literature/Praedifa/Catalogs/Catalog_O-Ring-Handbook_PTD5705-EN.pdf), table 2.8: hydraulic reciprocating contact Ra .40 μm, Rmax 1.60 μm. This is process guidance, not printed-PLA capability or molten-alloy seal compatibility.
- [Lussi et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8456283/), fabrication/material sections: a submillimeter catheter uses 150-μm UV-cured PFPE, custom heated aluminum microchannel molding and Cerrolow 117 containing lead/cadmium. Micro-encapsulation evidence does not transfer to rolling/sliding lifetime, creep or economical array manufacture.
- [RotoMetals](https://www.rotometals.com/roto-blog/fields-metal-from-scientific-oddity-to-essential-lowtemp-workhorse/): Roto144F is Bi/In/Sn, nominally 62°C. Its different chemistry/temperature prevents importing the catheter compatibility result. No retrieved source establishes the proposed pair's 5-MPa long-term creep, seal compatibility or film life.

Rolling requires preformed film, clamp/bond interfaces, aligned piston/bore,
sealed roof layers, filling/degas and inspection; sliding substitutes grooves,
finished bores and compatible lubrication. Neither is a thin-FDM-film process.
PLA guides/walls retain unqualified thermal creep, warp, anisotropy and fit.
No material-life distribution is invented from dimensions or tensile data.

Both routes repeat 12,800 moving boundaries, 6,400 charges/return paths/preloads,
heaters/switches and jaw/proof interfaces. Two attachments per film boundary can
mean 25,600 sealing lines. At shared reserve $150/$250/$350, the residual under
$500 is <$0.02734/$0.01953/$0.01172 per boundary **if all other site parts are
free**; no quote supports it. Assumed 5/15/30-second handling per boundary alone
means 17.8/53.3/106.7 hours before manufacture, charging, inspection and repair.
Integrated sheets could change this, but are a process hypothesis, not savings.
Batch swelling, clamp creep or shared heating can fail a module together.
Replacement requires a supported pin and preserved neighbors; no service design
or false-accept readback model is qualified by this local calculation.

## Disposition and checks

Stop these side-bay embodiments; keep A-018 a bounded family. Reopen only with
changed placement/return **and** a plausible compatible repeated process, or new
components altering these bounds. Smaller radii and ideal seals are insufficient.
This closes LAB-207's finite-containment gate without a thermal survivor; do not
start its dependent thermal/full-machine tasks. Next portfolio gate: identify a
materially different complete thermal architecture escaping inventory/process
failures, or conclude the campaign and redirect toward passive positive support
and shared addressing. Preserve the administrative recovery guard.

Self-review: independent radial integration at 128/512/2048 slices gives maximum
errors .00018316/.00002291/.000002865 mm³ on two off-grid cases. Complementary
volumes check the liquid-side change. 101-state dry-surface checks verify backing
envelopes/roof gap; monotonic bounds cover intermediate states. Both volume
excursion signs close over 101 main positions. Work/area ratios, spring-energy
integration, linear viscosity scaling, parallel-plate bound, closed duct, bolt
clearance and liquid-load stop failure are checked. This verifies reduced
necessary conditions, not nonlinear pressure stability, freeze mechanics or
hardware durability. No independent external review occurred.
