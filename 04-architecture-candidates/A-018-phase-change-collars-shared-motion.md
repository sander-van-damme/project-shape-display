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

## Current disposition after finite containment search

**Studied embodiments parked; thermal-support campaign technically concluded
(ADR-019).** The physical family remains bounded, not disproven. No informative
complete containment/material-cycle survivor warrants thermal tuning or printing.

E-110's finite keys give positive support but add molten transport and frozen
obstruction. Its holdout contains 13.283–13.635 mm³ and fully filled translating
grooves could export 28.149 mm³ over 40 mm. E-111's sealed full-track bath closes
geometric inventory at roughly 120 mm³ and 85.6-mm length; a drain/return escape
remains unqualified. These are conditional geometric bounds, not measurements.

E-111–113's dry-jaw thermal strut removes the long wet pin but introduces two
moving boundaries per site. Generated supported rolling/sliding packages with
roof ports and return at .05-mm error span 4.128/4.596 mm against a 1.89-mm side
bay, holding 6.598/6.671 mm³. Freeze sequence, creep, compatible seals and the
12,800-boundary process remain unresolved; cap-only volumes were optimistic.

E-114 tests a genuinely different fixed open capillary accumulator. Nonwetting
bores can return liquid under positive pressure while narrower jaw gaps resist
escape: its nominal clean-interface pressure margin is 621 Pa, with 5.621 mm³
charge. A .05-mm scenario reduces that margin to 4.4 Pa at the tested motion
load; slower motion can rescue that pressure case. Crucially, the finite stem
can carry liquid past its fixed hot lip into a cold guide. Static wetting angles
and aggregate reservoir capacity do not close the repeated material cycle.
This preserves a conditional capillary opportunity, not a machine survivor.

Reopen only with changed complete return/retention/isolation geometry or
credible interface evidence and an affordable repeated process. Do not infer
perfect drainage, liquid-volume closure through frozen paths, or durability
from analytical acceptance. A dry positive crossbolt remains the simpler
unqualified comparator. Next portfolio allocation is passive positive support
with shared selection/reset; earlier addressing and timing failures still apply.
