---
status: complete
builds-on: [E-157, E-109, E-108, E-060, E-063, E-153]
---

# Stationary yield removes boundary rollback, not leakage or release-state risk

**Stop these fluid-retention implementations and explore nonfluid memory next.**
Ideal shear yield retains a low-load hold/flow window, but none combines bounded
leakage, release/cut behavior, selection and joint cost/time. Published miniature
EPM costs fail even with free pole pieces; latched-open EPMs remain open after cut.
This is not a universal MR rejection. No assumed zero-leak plug repairs the failures.

Input main `b683b89`. Replay: `python3 tools/curated-experiment-checks/E-158/yield_plug.py`
(`--all` emits all 2,916 grid cases). Evidence: primary literature, analytical
conservation/rheology, deterministic sensitivity and self-review. No CAD, field/contact
solution, calibrated process/material distribution, new measurement or hardware pass.
All load, accuracy, timing and constitutive values below are **scenarios** except
stage-02 constraints and explicitly attributed source results. No print or purchase.

## Causal alternatives and new evidence

| Construction | Selection / shared motion / return | Retention, load path / proof and recovery |
|---|---|---|
| PM-biased shear-yield slit | Local opposing coil cancels a resident permanent field. Shared pressure supplies lift; a .30-N resident down-bias supplies unloaded descent against .05-N drag. | Piston → fluid shear → stationary walls/housing → frame. Remove cancellation, recover field, then read/prove hold. Cut closure must outrun lost volume; failed proof needs supported service. |
| EPM-induced granular arch | Two resident magnets and pulse coil switch the constriction field; common pressure transports MR suspension. Same explicit piston return. | Grains react through constriction walls. Closing must arrest flow; reversal must reform the arch. Open EPM stays open after cut. A closing capacitor/control circuit or second isolation is extra hardware. |
| Confined nonmagnetic wet granular plug | A normally compressed sleeve confines retained grains; a selected dry head opens the sleeve. Shared pressure drives the piston; down-bias returns it. | Grains → sleeve/frame; carrier may cross pores. Particle screens, sleeve return/preload, seals and reverse re-packing remain unsolved. Head release does not prove sealing. |
| E-109 control | Dry heads open fine/bypass poppets; springs return seats; common pressure moves piston. | Grounded seats avoid MR rheology and E-157 moving-boundary rollback. Its demonstrated return-force and priced-head failures remain; no new pass. |

All need chamber-side gating, ≥40-mm guided outputs, reservoir/return, fill/bleed,
readback and service access. The 2-mm bore is not packaged CAD; 5.08-mm tops permit
remote/tiered valves at added routing/dead volume. Shared heads need positioning/dwell.

Three distinct searches added evidence: fail-safe damper bias, EPM granular arches
and two-phase filtration. Known principles, not patent novelty. E-063 laminar brakes
hold sheets, not liquid; E-153 capillary pores need interface rearming whereas MR
needs particle reformation/redispersion. No free reset or saturation claim.

Primary sources accessed 2026-10-11:

- [Kubík et al., 2020, full primary paper](https://dspace.vut.cz/server/api/core/bitstreams/20384d7a-2795-4f23-986b-6132def35e79/content),
  DOI 10.1051/matecconf/202032201049: measured magnetic response with **air** in the
  gap; MR response is simulated. Its body reports a 17-ms primary rise in one MR
  positive-current case, so the abstract's 1.2–5-ms range is not a universal bound.
  No static leak or miniature pressure-hold qualification follows.
- [Leps et al., author-uploaded accepted manuscript](https://www.researchgate.net/publication/343565336_A_low-power_jamming_magnetorheological_valve_using_electropermanent_magnets_suitable_for_distributed_control_in_soft_robots),
  DOI 10.1088/1361-665X/abadd4: abstract reports 4×4×6-mm EPM, $7.32 materials at
  quantity 100, >415-kPa hold and .02-g leakage/24 h at 105 kPa. The abstract does
  not establish effluent density, leakage history or a population distribution.
  [Author's dissertation, chapter 3, pp.52–73](https://api.drum.lib.umd.edu/server/api/core/bitstreams/7b15b33b-61c5-45bc-8463-be7bca2d9e1a/content)
  supplies methods: 100-µs/~10-mJ electrical pulses; flow arrest measured only to
  <1-s resolution in fast cases; failures to jam or reopen depend on mix/throat.
  Two-day settling required stirring. $6.30 of valve cost was EDM end caps;
  electronics excluded. SLA throats were gauge-selected within .05 mm, not X1C priors.
- [Gallentine et al., 2024, pp.5–8](https://par.nsf.gov/servlets/purl/10586340),
  DOI 10.1115/FPMC2024-140393: the nested-ring prototype failed meaningful switching/
  latching. Magnet matching and residual flux mattered. Later simulated resistance
  improvements used variable viscosity, explicitly omitting Bingham rigid-body
  behavior. Neither its calculated flow resistance nor field strength proves sealing.
- [Ismail et al., 2012, primary institutional abstract](https://research-portal.uws.ac.uk/en/publications/fluidparticle-separation-of-magnetorheological-fluid-in-squeeze-m/),
  DOI 10.1143/JJAP.51.067301: compression experiments observed carrier/particle
  separation. Squeeze geometry differs from this stationary valve: evidence for a
  missing transport mode, **not** a transferable permeability or leakage rate.

## Joint yield, flow and field bounds

Homogeneous no-slip Bingham slit, gap g, active length L, width w:

`p_y = 2 τ_y L/g`, `b=p_y/|Δp|`,
`Q = w g³ Δp/(12 μ L) (1−b)²(1+b/2)` for b<1; otherwise Q=0.

The two walls react pressure force without a translating boundary. This continuum
result **assumes** no wall slip, creep, filtration or bypass. Omitted sidewall/entrance
losses favor release flow. Field uniformity, continuum applicability and printed
gap capability remain unqualified.

Use A=π mm², w=3 mm, .5-MPa supply, .30-N bias, .05-N drag and 0….10-N moving
payload: ≥356.76-kPa raising head, **79.58 kPa** unloaded lowering head. Parked
1/10-N service tests include bias. Raising 10 N already exceeds the .5-MPa source.

| Ideal channel, μ=.10 Pa·s | Nominal supported payload after bias | Unloaded field-free flow | Conditional 160-channel time |
|---|---:|---:|---:|
| g=.30 mm, L=5 mm, τ=20 kPa | 1.7944 N | 1.0743 mL/s | 18.9578 s |
| g=.15 mm, L=10 mm, τ=50 kPa | 20.6440 N | .06714 mL/s | 159.3256 s |

Time is the generous allocation `6 + ceil(6400/H)[2(A*40mm/Q+.020)+.050]`.
Two full-stroke pressure directions cover arbitrary targets within each group;
independent stopping is assumed. Six seconds includes preparation/indexing/final
proof/settle/one retry; .050 s/group includes acquisition/reset/local proof.
These are **unearned allocations** with perfect fair sharing of a 16-L/min source
(Q≤source/H). Actual regulation is unbuilt; E-108 pump starvation remains. The
fast channel takes **31.9157 s with 80 channels** under the same assumptions.

Field law uncertainty: `τ/τ_nom=(|B|/B_nom)^m`, m=1 or 2, neither fitted to a
material. Selected residual field fraction e=.02/.10/.25; worst unchanged-site
fraction `max(0,1−e−c)`, aggregate adverse neighbor exposure c=.05/.20/.50.
These coherent bounds are not a field solution or independent random draws; c must
include **all** energized neighbors. At .10 residual, the fast channel's conditional
160-channel time changes from **260.16 s (linear law) to 20.30 s (quadratic)**.
At .25 residual, linear release stalls; quadratic takes 42.28 s. The strong
channel stalls at only .02 residual under the linear law.

Enumerate 81 channels from g=.15/.30/.60 mm, L=2/5/10 mm, μ=.05/.10/.30 Pa·s,
τ=5/20/50 kPa, across 36 load/field-law/exposure cases: **2,916 cases**.
At 1 N and c=.05, e=.02 gives 17 linear/22 quadratic hold-plus-time cases;
e=.10 gives 0/18; e=.25 gives none. At 10 N none passes time. These are grid counts,
not yield or a universal bound. Ideal survivors lack seepage/cost/proof qualification.

Half-select cancellation halving the unchanged-site field reduces fast-channel
support to **.7472/.2236 N** for m=1/2: both fail at 1 N. A custom flux circuit
could escape but needs geometry/hysteresis evidence. Eight coherent gap ±.05-mm,
length ±2%, viscosity ±30% corners give
560–816-kPa nominal hold and .4689–2.4868-mL/s field-free lowering. These are
explicit uncertainty bounds, not PLA or fluid priors; gap improves flow cubically
while reducing pressure capacity.

## Source loss, reset and return witnesses

Open cancellation coil → cut → rising permanent field is not instantaneous
hydraulic arrest. In a quasistatic witness let the reservoir dump to ambient and
retain field-free conductance until closure. For the fast channel at zero payload,
.30-N bias minus .05-N drag drives **.6839/6.8392 mm** loss during 2/20 ms.
At 1 N, losses are **3.4196/34.1959 mm**. These omit inertia and partial-field
recovery: model witnesses, not fault-excursion predictions/bounds. At 10 N the fully restored fast channel cannot hold.

An EPM cut while OPEN stays open: this witness drains 40 mm in **.11697 s at zero
payload**. Close-on-loss energy needs fault detection, surviving switches and tested
re-jamming; no such mechanism is credited.
At constant .1/1-mL/s flow, a diagnostic .1-mm error permits only **3.142/.314 ms**
of uncompensated flow. Electrical pulse duration does not establish that integral.
Slow approach or holding source pressure through closure adds control/time/hardware.

No bias/payload and ambient return gives no downward drive. Even ideal vacuum
provides only **.31832 N**; .35-N drag defeats it. The assumed bias repeats 6,400
return elements and stores **76.8 J/board**. Double-acting repair adds pressure
boundaries, routing and controlled ports.

No stem sweeps volume, but particle rearrangement can. E-060/E-108 still applies:
reconnecting a 10-mm³ pocket with .5-MPa mismatch and K=100 MPa transfers
.05 mm³ = **.01592 mm** piston travel. Repeated *refreshed* pockets accumulate;
one equilibrated pocket does not. Source reversal must occur with all unchanged
chambers closed. Supply pressure cannot be used to unjam all cells together.
Rigid-liquid load sag `FH/(KA)` at 10 N and K=10/100/1000 MPa is
**12.732/1.273/.1273 mm**, before wall/gas/dead-volume compliance. Largest strain
is outside a precise linear-liquid model; retain it only as a compliant scenario.

## Carrier transport defeats a nominal yield-only proof

For an alternative porous-plug model `Q=k S Δp/(μ_c L)`, choose S=1 mm²,
L=1 mm, Δp=105 kPa. k=10⁻²⁰…10⁻¹⁴ m² and μ_c=.01/.10 Pa·s are competing
**unmeasured scenarios**, not fitted jamming properties. Four-hour travel ranges
.0000481–481.28 mm (large values truncate at a physical stop). A diagnostic
.1-mm/four-hour allowance requires **k≤2.078×10⁻¹⁸ m²** at μ_c=.01, or
Q≤**.02182 nL/s**. Grain arches alone provide no such bound.

Converting the published .02-g/24-h leakage with an explicitly assumed effluent
density range .8–4 g/mL yields **1.592–7.958 mm/24 h** for this piston, with
mean .0579–.2894 nL/s. This does not predict our fluid, leak timing or higher pressure.
It exceeds a .1-mm allowance over the *same* 24 h. Stage 02 sets no numerical hold
accuracy: diagnostic concern, not an imposed product rejection or a zero-leak prior.

For .1-s full-stroke writing at 200 kPa versus .1-mm/four-hour drift at 105 kPa,
open/closed conductance must differ by **30.24 million**. A fixed restriction cannot
do this; reversible connected-porosity changes need evidence. An impermeable membrane
is another seal; dry grains bearing load directly are a changed nonfluid mechanism.

At the diagnostic leak limit, **7,200 s** is needed for .05-mm measurable drift.
Short proof/readback detects gross flow, not long-term sealing. Sensor bias, settling
and bad batches correlate false accepts; no detection probability is assigned.
Persistent leakage/jams require supported module service, outside retry timing.

## Board accounting, decision and reopening

Nominal swept volume **.80425 L** requires >**1.6085 L/min** for a full upward stroke
in 30 s before overhead; return reservoirs, manifolds and dead volume add inventory.
Resident PM route needs 6,400 each of magnets, flux circuits, sealed piston/guides,
returns and cartridges; local coils add 12,800 terminations. EPM doubles magnets
to 12,800; separate two-cap circuits add 12,800 steel pieces. The cited two-pulse
energy scales to **128 J/full map** before drivers, pumping and recovery.
Nonmagnetic confinement instead repeats 6,400 sleeves, grain packs/screens and
preload/release interfaces. Shared heads still need priced positioning and dwell.

Published 2020 EPM materials at quantity 100 scale to **$46,848**; even gifting
all $6.30 EDM caps leaves **$6,528**, before electronics/fluid/cylinders/returns.
Historical route extrapolations, not current bulk quotes/market floors: reject
*this route*. With $250 shared reserve, all local purchases get <$0.03906/site.
PM-only/shared-field/custom routes lack a complete BOM; unknown cost is not a pass.
Joint reserve must include magnets, steel, wire, drivers,
pumps, fluid, containment, sensors, guides, fasteners and power once each.
Print volume/time lacks geometry; 10–30-s handling/site alone costs 17.8–53.3 h.

No qualified X1C gap/pressure-boundary prior exists. Common shrinkage, hole bias,
first-layer intrusion, layer quantization, warp/alignment and roughness alter flow;
PLA anisotropy, wall creep/interlayer weakness, particles/seal abrasion, sedimentation,
wear and fatigue alter retention. Batch magnet remanence, return steel saturation,
shared coil droop and aging correlate across banks. No yield/life/tail probability
follows. Field simulation cannot bound filtration;
material calibration cannot repair cost or latched-open cuts.

**Stop** field-off-only retention, unqualified wet granular sealing, resident EPM
procurement at the cited route, and further slit optimization as a primary campaign.
**Reopen** only with a changed complete combination: affordable local field hardware,
bounded closed carrier loss and bidirectional reset, genuine source-loss closure,
zero-payload return, then actual neighboring-field geometry and joint cost/time.
Ideal PM slit remains conditional knowledge. No physical article is justified now.

Self-review independently integrates shear-rate-derived flow at 64/256/1,024
subdivisions: relative errors 3.19e−4/2.00e−5/1.25e−6. Wall-force balance, Newtonian,
yield/no-flow, signed reversal, volume/mass conversions and zero-pressure reset
limits pass. These verify reduced equations; they do not validate material laws,
field geometry, dynamics, cost at scale or manufactured hardware.
