---
status: complete
builds-on: [E-113, E-110, A-018]
---

# Open capillary bridge: conditional pressure window, unresolved cold carryout

Input main `0899017`. **Park the generated package; conclude the studied
thermal-support campaign without a machine survivor.** A fixed open capillary
accumulator is a real change from E-113's contacting seals/films. It has a
nominal pressure window, so this is not a proof against capillary containment
or all fusible support. The nominal pass depends on liquid-interface behavior
and does not close the generated cold-guide material cycle. ADR-019 records
selection and reopening; no thermal tuning, fabrication or calibration request.

Reproduce `python3 tools/curated-experiment-checks/E-114/retention.py`.
One generated topology, 18 deterministic uncertainty cases; no random seed.
Units mm, N and Pa (solid stress MPa). Evidence is analytical geometry,
quasistatic pressure/volume bounds and primary sources, not measurements or a
free-surface/contact simulation. Cases are competing bounds, not yield samples.

## Finite mechanism and sequence

A dry rack shoulder drives a grounded sliding jaw outward: illustrative
vertical load 10 N and 30° shoulder give H=5.774 N. The jaw has a 2×2-mm metal
stem/pressure face. Its face x=q moves from 0 to .5; stem occupies [q−1.3,q].
The fixed cup runs from rear lip x=−.65 to load wall x=.6, with inside y,z
±1.15. Four circular bores of radius .4 centered at (y,z)=(±.55,±.55) pass
through the .3-thick wall, then provide 2.5-mm meniscus travel, ending at x=3.4.
Bores are open to local air, with no shared liquid manifold. A .3 wall allowance
bounds the fixed body by x=[−.95,3.7], y,z=±1.45. Including the stem, the bare
5.0×2.9-mm projection fits 5.08 pitch **in a separate layer below the rack**;
heater, thermal breaks, connections and jaw linkage are additional. This is
not the already-failed 1.89-mm side bay, nor a complete packing pass.

Frozen metal between jaw face and grounded perforated wall carries compression;
vertical force closes through jaw guides. Nominal bridge volume is 2.4 mm³;
wall's solid projected area is 4−4π(.4)²=1.989 mm². Necessary mean bearing
stress is 2.902 MPa, without concentrations, splitting or creep. Effective
whole-bridge allowables 1/5/20 MPa would respectively fail/pass/pass this
nominal cut; these are assumptions, not Field's-metal properties. The nominal
outer pore-to-contact edge land is only .05 mm. Growth of pores and shrinkage
of face can erase it; full-hole area subtraction then overstates the removed
contact area and is conservative, **not proof of leakage or fracture**.

Sequence: shared collet acquires and unloads selected pin; heater melts bridge
and all connected inventory; externally powered jaw withdraws .5, driving
liquid into the open bores; collet moves the dry pin through up to 40 mm; jaw
reseats, drawing liquid back; hold through freeze and support proof, then
release collet. Electrical selection needs isolated site switches, not passive
heater coincidence. Unchanged sites remain frozen and mechanically supported.
Return stroke is commanded by the shared head; capillary pressure only assists
liquid return, not loaded jaw retraction. A separate service catch is still
needed for an unintended heater-on fault. Recovery retains grip, remelts and
reseats locally once; continued inventory loss or cold fouling requires supported
cartridge service, not heating unchanged neighbors. Readback must test support,
not merely temperature. No false-accept probability is assumed.

## Retention and return limits

A wetting wick is not automatically a return reservoir: at θ=30°, γ=.417 N/m,
r=.1 mm it holds liquid at −7,223 Pa gauge, whereas a .6-mm wettable bridge
has only −1,204-Pa suction. This simple wick drains the broad bridge rather
than refilling it. Retrieved Field's-metal substrates are non-wetting, so the
studied escape instead uses their **positive** capillary pressure:

`p_pore=−2γ cosθ/r`, `p_escape=−2γ cosθ/c` for a parallel-wall rear clearance c.
Radii and clearances in these equations are metres. The slit expression ignores
width curvature; corners, contact-angle hysteresis and oxide films are not
solved by it. Four independent menisci must stay inside their bores; equal
penetration is an ideal symmetric limit, not guaranteed under pore variation.

Pressure screen requires both return and containment:
`margin=min(p_pore,min−d, p_escape,min−p_pore,max−d)−p_oxide > 0`,
with `d=ρ(g+a)L + ρu²/2 + Δp_viscous`.
Use labelled bounds ρ≤9,000 kg/m³, L=.004 m, a=10 m/s², u=.01 m/s:
713.61 Pa before viscosity. Four fully liquid circular tubes, maximum wetted
length 2.8 mm and .5-s transfer give the Poiseuille term. μ=.02 Pa·s is a
scenario, not sourced alloy viscosity; entrance and oxide effects are excluded.
This is a pressure excursion bound, not prediction of actual board vibration.

Angles 130–145° are a source-informed **static** scenario; 110–150° is a
competing dynamic/contamination bound. Neither bounds advancing/receding angles
on our manufactured parts. Opposing radius/clearance errors e=0/.05/.15 mm
and pressure penalties p_oxide=0/200/1,000 Pa are explicit uncalibrated scenarios.
A common surface/process shift can affect a whole batch; independent extremes
within one site conservatively cover differential interfaces. γ=.417 is the
clean-liquid reference, not a claim that oxide-coated interfaces obey Laplace.

| e mm | Angle range | Zero-oxide pressure margin Pa | Consequence |
|---|---|---:|---|
| 0 | 130–145° | 621.0 | Conditional static window; +200-Pa penalty leaves 421.0 |
| .05 | 130–145° | 4.4 | Almost no allowance for omitted interface physics |
| .15 | 130–145° | −1,707.6 | Pressure failure; rear and minimum front clearances also close |
| 0 | 110–150° | −623.2 | No robust pressure window in this package |
| .05 | 110–150° | −1,361.5 | Escape and return bounds conflict |
| .15 | 110–150° | −2,700.1 | Pressure and geometric failure |

At e=.05 in the narrow case, pore pressure spans 1,191–1,952 Pa and minimum
escape threshold is 2,680 Pa. Lowering a to zero restores 164.4-Pa margin even
with the 200-Pa penalty: **10 m/s² is not a product requirement**, and slowing
motion is a real conditional rescue. Likewise γ, wetting and oxide behavior
can change rankings. No universal physical rejection is inferred from these
bounds. Pressure alone therefore cannot select or reject the whole family.

## Inventory, carryout and freeze obstruction

A deliberately conservative slot-filled volume allocation gives nominal charge
5.621 mm³: bridge 2.4, fixed-wall/initial bore volume 1.6085, peripheral allocation
1.6125. Bores provide 5.0265 mm³ storage; initial penetration .5 mm occupies
1.0053 mm³ and nominal jaw travel transfers 2.0 mm³. ±5% charge-volume excursion
fits. A separate coherent corner grows piston/cup together and shrinks pores;
fixed nominal charge and explicit conservation retain capacity at e=.05, but
not .15. This checks aggregate capacity only: unequal meniscus pinning could
expel one bore before aggregate capacity is used. No perfectly shared filling
is credited as demonstrated. Melt pressure times the 4-mm² face gives only
millinewtons; it cannot hold H=5.774 N if the bridge melts while loaded.

Generated stem always overlaps the rear lip, and remains separated from the
fixed wall throughout 501 states. Frozen engaged bridge intersects the moving
stem by `4q` mm³, reaching 2 mm³ at release. Thus every load-blocking portion
must melt; an unobstructed endpoint or heater resistance is insufficient.

The fixed rear lip is x=−.65, while the allocated hot volume ends there. A
cold guide occupies x=[−1.25,−.85]. Material adhering at the lip can be carried
.5 mm inward during return, reaching −1.15 and overlapping **.30 mm of cold
guide**. Heating the pressure face and bores does not clear that deposited
film. A thin-film bound is `V_export=P s t=8(.5)t`: t=0/.01/.05/.15 mm gives
0/.04/.20/.60 mm³ per return. This is transported volume, not a measured loss
or a coating law; zero transport is the competing perfect-drainage assumption.
Two .05-mm layers (stem coating plus prior guide residue) close a .10-mm gap.
A repeated .20-mm³ unrecovered loss exhausts the nominal 1.005-mm³ initial
pore reserve in six cycles, earlier with shrinkage allowance. No probability,
wear rate or lifetime is inferred.

A warmed catch hood, scraper or return groove would be a changed recovery
mechanism requiring its own clearance, material return, heat and regional
isolation proof. It is not present here. Cold-guide fouling is the decision
stop, alongside fragile pressure/process closure; enlarging pores or merely
asserting nonwetting does not close this cycle. The 40-mm pin stays dry, so
E-110's much larger keyed-tail export is avoided, but export is not zero.

## Sources and process transfer

Accessed 2026-10-10; no alloy samples or printed measurements:

- [Zamora et al., Materials 2021, 14, 7392](https://doi.org/10.3390/ma14237392),
  Table 5 and sections 3.2–3.3; [author repository full text](https://repositorio.upct.es/server/api/core/bitstreams/245202b4-0cbf-4c34-af8f-88e5bf0b5f21/content).
  At 358 K, Field's metal on glass/316L/PTFE/resin has reported contact angles
  approximately 132–143° across oxygen/nitrogen conditions. Clean nitrogen
  pendant-drop tension is .417 N/m. Oxide changes apparent interface response;
  torsional steady shear near 55±10 Pa is **not** a transferable capillary
  breakaway pressure. Static drops and macroscopic rheometry do not qualify
  advancing/receding angles, repeated pore pinning, drainage or our penalties.
- [Senju patent US9175782B2](https://patents.google.com/patent/US9175782B2/en),
  Example 2: 28-mm plugs with 3-mm tip bores are pressure-tested at 15 MPa for
  24 h at 65/85°C for different alloy families. This demonstrates a specific
  creep-testing context, not a transferable allowable for this unconstrained
  bridge, alloy composition or cyclic duty.

The X1C/PLA baseline has no qualified .15-mm hot running clearance, .05-mm
contact land, finished nonwetting pore surface or hot-guide creep capability.
Density, dimensional errors, viscosity, angle hysteresis, film thickness and
oxide penalties above are bounds, not machine-resolution-derived priors.
Common hole bias/warp and batch surface chemistry matter; layer quantization,
first-layer effects and roughness cannot be reduced to an IID success rate.
PLA wall thermal creep/anisotropy and alloy long-term creep/fatigue remain open.
A metal insert/coating process is an additional manufacturing hypothesis.

## Complete-system comparator and burden

A grounded dry 1×1-mm crossbolt holds the same horizontal jaw force at nominal
5.774-MPa bearing/shear stress. Collet unloads; bolt withdraws 1.15 mm in depth
past the 1-mm jaw; jaw withdraws .5; reverse, seat and proof. It still needs
selection, retention, guidance, affordable head actuation and recovery, but
no thermal charge or liquid return. Neither mechanism has a qualified complete
<30-s arbitrary-map schedule; A-013's expensive drive and earlier shared-energy
scheduling failures remain constraints, not solved by changing the local stop.

The thermal route replaces 12,800 flexible/sliding seals with 6,400 capillary
clearance interfaces, 25,600 open bores, 6,400 charges/heaters/site switches and
retainer/guide processing/inspection operations; shared collets, scanner,
catch, power and cooling remain. At $150/$250/$350 shared reserve, **all** bought
site content must average below $.05469/$.03906/$.02344 to stay below $500.
These are residual allowances, not quotes. Assuming 5/15/30 seconds per site
for one handling step alone gives 8.9/26.7/53.3 hours; coating, fill, rework and
inspection are extra. Printed stock is uncapped in cost but not free in burden.
No price or sourced life evidence supports the required repeated process.

Regional independence is geometric only while liquid stays local and heaters
stay isolated. Common heating, loss of charge, frozen guide debris and false
support acceptance can disturb several cells; a whole bank stop and retained
collets may be necessary. No numerical disturbance/reliability claim follows.
All preparation, melt/freeze, jaw reset, readback and bounded repair belong in
map time if this family is reopened. No thermal timing was tuned past this gate.

Self-review: independent circumference-force/area balance verifies capillary
pressure and SI work units; circular-section quadrature at 100/1k/10k slices
converges to bore volume with errors .001557/.00004929/.000001559 mm³. Checks
cover wetting sign, inverse-radius scaling, neutral contact angle, swept stem
wall separation/frozen interference and cold-guide overlap. Aggregate-volume
and ideal pressure models omit free-surface shape, asymmetric menisci,
constitutive oxide behavior and contact stress. No external independent review
or physical validation is claimed. Preserve this positive nominal limit and
unique cold-carryout failure; do not turn uncertainty scenarios into a blanket
ban on capillary retention.
