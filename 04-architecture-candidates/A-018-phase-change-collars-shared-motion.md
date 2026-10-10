---
status: candidate
builds-on: [P-001]
---

# Phase-change collars with shared motion

**Bounded; not rejected as a physical principle.** Descriptors: isolated local
heaters; frozen collar height memory; shared elevator mechanical energy;
collar shear into frame as service load path; one prismatic pin and one sealed
annulus/heater per site. This replaces a mechanical pawl, not the 40-mm drive.

A sealed fusible collar surrounds a rough/keyed metal tail inside a grounded
cup. While an elevator collet holds the selected pin, an addressed heater melts
its collar, allowing translation. The collet then drives down/up to arbitrary
height and retains load during cooling. Solidification transfers load through
the keyed collar to the cup/frame; proof unloading must precede disengagement.
Adjacent heaters stay off and cups need thermal breaks. Shared cold plates
must not move unchanged pins. Active-matrix electrical isolation is required;
passive resistor coincidence is not a demonstrated selector. Recovery remelts
and reseats a failed collar while gripped; leaking cartridges require mechanical
service catches and replacement. Read tail marks and collar resistance/
temperature, but temperature is not proof of shear strength or complete freeze.

A 3-mm tail with 0.1-mm radial annulus and 2-mm collar length contains about
1.95 mm³ (exact annulus); outer metal envelope 3.2 mm leaves 1.88 mm for cup,
heater, insulation and pitch clearance. 10-N support over roughly 19 mm²
interface requires about 0.53 MPa mean shear before stress concentration/creep.
This is an assumed research load, not measured bond strength. Tail track and
collet space add depth as in the shared-elevator comparators.

Repeat 6,400 cups, seals, alloy charges, heaters, sensing/drive connections
and collet interfaces. Shared lift, cooling hardware and scanner remain.
E-063 varies phase-change enthalpy density 0.2–1 J/mm³ and volume 0.5–10 mm³
as explicit generic bounds, not alloy data: 0.64–64 kJ/map, 21–2,133 W average
at 30 s before losses. A small collar is not automatically thermally fatal;
large collar/weak sink cases require up to 250 s optimistic cooling. Thermal
bridges that accelerate cooling also spread unlock heat. Containment/wetting,
freeze shrinkage, creep and repeated sliding make an FDM cup alone unqualified.

Gallium's approximately 29.765°C melting point excludes an uncooled gallium
service lock in a 30–35°C room scenario. This is a conditional environment
failure, not a specified room limit. A higher-melting alloy avoids it but
raises heating and PLA-isolation burdens. Thermoplastic locks similarly need
measured creep and solidification strength; conductivity cannot be assumed.
No credible component quote supports the $0.0391/site residual at $250 reserve.
Retain microvolume collars only as a bounded alternative; next discriminate
minimum load-bearing keyed volume against heat-sink/cross-talk requirements.

Primary leads: [submillimeter alloy catheter](https://pmc.ncbi.nlm.nih.gov/articles/PMC8456283/)
demonstrates small-scale stiffness control, not a sliding pin lock;
[NIST gallium standard](https://www.nist.gov/publications/standard-reference-material-1751-gallium-melting-point-standard)
establishes the melting temperature. Accessed 2026-10-08.

## Inverse annulus load/energy bound

Initial successor calculation at input main `50b81ee`; analytical necessary
bound and self-review, not material or contact evidence. Under an effective
allowable cylindrical interface shear stress τ, tail diameter d, radial alloy
gap g and supported force F, `L >= F/(π d τ)`. An annulus at that minimum length
has `V >= (F/τ)(g + g²/d)`. Thus shrinking the tail diameter does **not** reduce
minimum material/heat at fixed load, gap and allowable stress: required length
increases and the small curvature term gets worse. Gap, effective strength and
load allocation control this bound. Discrete keys or bridges can change the
failure section and must be modeled as different geometry, not credited from
this cylindrical formula.

At illustrative F=10 N, g=.1 mm and τ=.5 MPa, d=3 mm requires L≥2.1221 mm and
V≥2.0667 mm³. Reducing d to 1 mm increases L to 6.3662 mm and V to 2.2 mm³.
Using E-063's **assumed** .5 J/mm³ effective heating requirement, the 3-mm case
requires ≥6.613 kJ/full board and ≥220.44 W average over 30 s, before heating
the tail, cup, substrate or compensating losses. At g=.15 mm and τ=.25 MPa,
V≥6.3 mm³ and the same calculation gives 20.16 kJ / 672 W. There is no stage-02
power cap; these numbers are heat/circuit/cooling obligations, not rejection
criteria. Simultaneous release, repeated group operations and recovery may
raise peak power or total heat. The stress scenarios are not alloy strength,
creep allowables, adhesive qualification or a probability distribution.

Reproduce the inverse result and verify against independent annulus volume:

```python
from math import pi, isclose
for d, g, tau in [(3, .1, .5), (1, .1, .5), (3, .15, .25)]:
    length = 10 / (pi*d*tau)
    volume = pi*((d/2+g)**2-(d/2)**2)*length
    assert isclose(volume, 10/tau*(g+g*g/d))
    print(length, volume, 6400*volume*.5/30)
```

Finite-key follow-up E-110 generates annular and sector keys with exact
phase-volume and frozen-path collision checks. Positive keys remove reliance
on adhesion but introduce material transport: a 5.2-mm-long illustrative keyed
collar holds 13.283–13.635 mm³; fully wetted grooves can carry 28.149 mm³ out of
the heated zone during 40-mm translation. Perfect drainage is the competing
unverified bound. Geometric clearance does not prove liquid containment.

E-111 closes geometric inventory for a two-ended bath with seals on smooth
lands: the 40-mm stroke requires an 85.6-mm chamber and roughly 120 mm³ liquid
for the E-110 holdout. Heating that whole bath needs an assumed 384 kJ/board
(.5 J/mm³), before structural heating/losses. Deprioritize this embodiment;
a finite local drain/return could reopen it, but perfect drainage is unverified.

The changed short-stroke alternative uses a dry sloped rack shoulder, grounded
jaw guide and sealed thermal structural strut carrying the jaw's outward load.
Two opposed variable-volume chambers return liquid internally. At 10 N/30°,
1-MPa effective whole-strut allowable and .05-mm coherent error, its bounded
inventory is 8.860 mm³ with 50% added dead volume. Neither that allowance nor
the assumed strength is qualified. The .15-mm duct-closure scenario raises
0.5-s transfer force to 15.207 N at assumed 1 Pa·s. At least 12,800 flexible
boundaries repeat across the board; lower heat alone establishes no winner.

E-112 replaces the cap-only boundary with a finite circular rolling fold. Its
liquid displacement area is π(a²+b²)/2; material on that prescribed fold also
changes circumference. At 5-MPa assumed solid stress and .05-mm error, a .5-mm
jaw stroke requires .805-mm reservoir travel with ±5% volume allowance and
3.924 mm³ liquid. It fits the tested 1-mm dry-rack side bay but overruns the
2-mm version by .365 mm; hoop excursion reaches 53.6%. The 1-MPa counterpart
requires 12.462 mm³, exceeding E-111's reduced dead-volume estimate. None of
E-112's .15-mm-error cases passes its specific side-bay/fold geometry cuts.
These are prescribed surfaces, not pressure-stable or material-qualified seals.

Next discriminate guided, pressure-stable containment/return and a credible
repeated fabrication process against the mechanical jaw; no thermal tuning or
printing until that gate has an informative survivor. The free rolling film
still lacks backing geometry, compatible seals and a return/preload mechanism.
A thin FDM membrane, qualified hoop life and affordability are not assumed.
Stop this embodiment if those obligations fail; changing placement/topology can
reopen the scoped geometry exclusions. Strength/creep, thermal isolation,
addressing and full-machine schedule remain unqualified. Reduced tail diameter
alone remains no low-energy escape, and a command-only thermal latch is A-017.
