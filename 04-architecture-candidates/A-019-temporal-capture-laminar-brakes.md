---
status: candidate
builds-on: [P-001]
---

# Spatiotemporal capture with mechanically clamped laminates

**Bounded; merge temporal scheduling with other shared-motion families.**
Descriptors: stored local clamp command; frictional laminar height memory;
shared elevator; grounded laminate shear load path; prismatic pin with parallel
sliding leaves. Temporal capture is a scheduling principle, not an additional
independent selection mechanism.

Pin tails carry thin sliding leaves interleaved with grounded leaves. A local
bistable wedge squeezes the stack after capture at the requested height. A
shared squeeze rail provides clamp energy only where a magnetically stored
flag couples its cam dog; reset pulses decouple/open the selected wedge while
the moving collet holds the pin. Collet elevator down/reset/up permits arbitrary
transitions; independently retained wedges leave unrelated cells supported.
A simple single vacuum envelope cannot encode independent capture times:
without local valves or local clamps all regions jam together. Reject that
embodiment for arbitrary maps. Mechanically stored clamp force avoids a pump
running continuously and 6,400 vacuum valves, at the expense of 6,400 wedges.

At 40-mm² contact, assumed 50-kPa compression and friction 0.2 give only
0.4 N per sliding interface; 10-N holding needs 25 active interfaces even
before uneven pressure. Increasing clamp stress to 0.5 MPa lowers that count
to three but requires 20 N normal squeeze per cell: 128 kN distributed reaction
if all cells clamp, not one end-loaded rail. Leaves must overlap throughout
40-mm travel (20-mm overlap implies at least 60-mm sliding leaves). At assumed
0.05-mm foil thickness, 26 leaves occupy 1.3 mm before clamp and guides;
printed PLA laminates are not granted that thickness or friction.

Repeated leaves, wedges, flags, collets and wear surfaces dominate assembly;
shared elevator, segmented clamp rails, pulse drivers and scanner provide
power/selection. A 2×20-mm footprint is only an area allocation, not swept
packaging. Friction, contamination, clamp creep and wear permit slow slip;
read tail height after proof unload and periodically during use. Regrip,
reclamp and re-read once on error; persistent slip needs a mechanical service
catch, module stop and replaceable leaf cartridge. Common clamp-rail relaxation
can release many pins; no independent-cell reliability assumption applies.

Continue only if a dry laminated cartridge offers a cost/manufacturing advantage
over a positive pawl at the same load. $250 reserve allows $0.0391/site for all
bought foil/flag parts; 26 separately purchased leaves would leave $0.00150
per leaf before other parts. Sheet-cut arrays may reduce procurement but not
contacts or assembly. No cost advantage or lifetime is demonstrated.
[Laminar-jamming research](https://doi.org/10.1002/adfm.201707136) establishes
pressure-controlled friction as a variable-stiffness mechanism; it does not
validate this independently addressed pin array. Accessed 2026-10-08.
