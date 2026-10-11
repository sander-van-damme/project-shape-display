---
status: complete
builds-on: [E-182, E-074, E-080, E-149, M-004, A-016]
---

# Remanent coincidence must preserve state through the working gap

**Stop the tested opening-gap row/column electropermanent-magnet drive as a
machine lead.** A 5-mm magnet pair loses its equal-amplitude relay window at
.140-mm gap and retained ON state at .302 mm. Asymmetric set/reset pulses rescue
fixed-gap cases, but not the tested 1-mm working stroke. Longer fixed-gap magnets
remain conditional; their ranking changes with constitutive and manufacturing
bounds. No general rejection of EPMs, nonlinear selectors or ratchets; no machine,
fabrication or purchase selected.

Input main `30b802a`. Reproduce: `python3 tools/curated-experiment-checks/E-183/remanence.py`
(standard library; disposable JSON). Evidence: sourced material ranges, invented
circuit geometry, recoil/relay calculations, state enumeration and board bounds.
Self-review only; no field/contact FEA, assembly CAD, actual hysteresis calibration,
print-process prior, physical measurement or yield.

## Causal alternatives and provenance

| Combination | Address, motion, retention, load and recovery |
|---|---|
| Saturable series path | Coincident bias changes incremental permeability; shared AC supplies work; separate hold/reader required. Saturation increases reluctance, not intrinsically a positive coincidence amplifier. |
| Saturable bypass | Bias saturates a shunt, releasing flux to the load; finite feed/reset and bias/power isolation required (E-182). Local core inventory remains. No solved circuit here. |
| EPM resident stroke | Row/column windings reverse a low-coercivity magnet beside a hard magnet; ON pulls an armature; OFF permits spring return. Rack/catches store height and carry service loads; actual height/support proof governs retry. Circuit below. |
| EPM flag | Magnetic memory operates a powered cam; shared lift carries motion. Returns to A-016 grip/release/proof obligations. |
| Controls | E-182 screw avoids pickup but not coast; M-004 ratchet bounds increments only with a closed catch sequence. Spatial full-strength EPM writing avoids half-selects but restores transport/local flux access. |

Search axes: material hysteresis versus mechanical detents, and finite resident
stroke versus continuous screw rotation. E-074/080 test mechanical flags; here
polarization depends on gap/pulse history. E-149 has fixed magnetic height wells;
here grounded teeth would carry load. Functional recombination, not a new magnet
or ratchet principle; no new A/M object or landscape-saturation claim.

Sources checked 2026-10-11:

- [Deutsche Magnetwerke AlNiCo 500](https://www.guss-magnete.de/en/wp-content/uploads/2020/04/DABL_500_engl_2016_04.pdf):
  anisotropic cast material; typical Br 1.24 T, HcJ 51.7 kA/m, recoil permeability
  3–4.5, saturation field 240 kA/m; minimum Br/HcJ 1.12 T/48 kA/m. These are
  specifications, not installed-part distributions/pulse durations. Coercivity is
  not a guaranteed no-change minor-loop threshold; recoil slope is not a full
  reversal curve.
- [Keeys et al., 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10594592/):
  paired AlNiCo/NdFeB EPM, 173 turns, ±10 A, 1-s pulses, estimated ~100-kA/m field,
  40×34.55×8.35-mm assembly. Physical existence reference, not 5.08-mm-pitch,
  millisecond or half-select qualification.
- [Dantam and Afshar, 2022](https://arxiv.org/abs/2210.00142): measured AlNiCo
  B–H data and air-gap feedback inform magnetization tuning. This identifies
  missing constitutive evidence; no performance transfers.

## Closed circuit and histories

Hard h and wound switchable s magnets of equal length l connect common pole
shoes. Their parallel flux enters an armature through two equal series gaps g,
each area Ag. Translation changes both gaps together. Shoes/armature are granted
zero reluctance, leakage, eddy loss and saturation. Only s is wound; row/column
loops add signed ampere-turns F. This is a circuit, not packed pole CAD.

Set Ah=As=1 mm², Ag=4 mm², Brh=Brs=1.24 T, muh=1.05, mus=4, l=5 mm.
Hard-magnet properties/stability are matching assumptions, not a sourced part.
Low-core state s=±1 chooses a stipulated recoil branch:

`Bh=Brh−mu0*muh*V/l; Bs=s*Brs+mu0*mus*(F−V)/l`

`V=(Ah*Brh+s*As*Brs+mu0*mus*As*F/l)/[mu0*(muh*Ah/l+mus*As/l+Ag/(2g))]`

`Hs=(F−V)/l; Phi_gap=mu0*Ag*V/(2g); attraction=Phi_gap²/(mu0*Ag)`.

V is magnetic potential across branches. ON sources add; OFF cancels only when
AhBrh=AsBrs. Polarity changes external flux magnitude, not attraction sign; return
still needs a spring/opposed pole. Memory supplies neither indefinite work nor
bidirectional motion.

The optimistic law grants instantaneous complete reversal at opposing Hc, with
no subcoercive drift, rate dependence or partial magnetization. **Not validated
AlNiCo behavior.** Define a=dHs/dF and zero-current fields Hon,Hoff. Opposite
half-pulse onset limits are `Fset=(Hc−Hoff)/a`, `Freset=(Hc+Hon)/a`.
Equal signed single-line amplitude f needs
`max(Fset,Freset)/2 < f < min(Fset,Freset)` over every old state/gap/cell, with
stable states after current clears.

| l, mm | g, mm | ON demagnetizing H, kA/m | Frozen-ON attraction, N | Equal single-line AT window |
|---:|---:|---:|---:|---|
| 5 | .05 | 9.625 | 1.164 | 131.82–214.56 |
| 5 | .10 | 18.786 | 1.109 | 134.37–171.08 |
| 5 | .20 | 35.850 | 1.009 | none: >139.38 / <85.46 |
| 5 | .50 | 78.783 | .780 | ON unstable at zero current |
| 10 | .20 | 18.786 | 1.109 | 268.73–342.16 |
| 20 | .50 | 23.204 | 1.083 | 542.52–598.04 |

Matched 5-mm magnets need |Hon|<Hc/2 for equal-amplitude selection (g<.140262 mm)
and |Hon|<Hc for retention (g<.301909 mm). Exact limits of this law, not real
material thresholds. Frozen-ON forces are unavailable steady forces when ON is
unstable. At g=.2 mm, +280 AT sets OFF while −140 AT half-selects ON into OFF.
At .5 mm, removing current alone resets ON. Real material may partly demagnetize
instead of making that relay jump.

**Asymmetric rescue:** independently choose each sign using
`max(Fdirection)/2 < fdirection < min(Fdirection)`. At fixed .2 mm, set 140 and
reset 60 AT/line work. Across the .05…1.05-mm stroke, however, the 20-mm pair
needs reset >494.94 AT at closed sites and <131.35 AT at open sites. The 5/10-mm
pairs include zero-current unstable states. None of these lengths has one robust
signed protocol across the stroke. Gap-aware scheduling must account for every
neighbor's old gap/state; it was not constructed.

At .05 mm the source exhausts 512 old 3×3 states × three rows × eight masks ×
two signs =24,576 transactions, including clear to zero. Selected states change;
half/unselected states retain their values. Two-state invariance extends to any
sequence **only in this nonaccumulating relay law**. No physical minor-loop or
E-080 mechanical pumping immunity follows. Local closed returns are generous;
external neighbor fields and hard-magnet response remain unresolved.

## Manufacturing and constitutive sensitivity

A competing law requires post-reversal |H|=kHc to recover stipulated remanence.
Set/reset demand is the larger of onset and `(kHc−Hon)/a`, `(kHc+Hoff)/a`.
This recoil extrapolation is a sensitivity scenario, not a pulse prediction.
Near a closed unbiased gap, k<2 is necessary; current spread/parasitics tighten it.
The sourced 240/51.7=4.64 ratio cannot justify full-saturation coincidence under
this routing. The experimental ~100/48 ratio also exceeds two. Partial writes
might suffice: neither comparison rejects them, but Hc cannot simply stand in
for a full-write threshold. A required-remanence/minor-loop envelope is missing.

For g=.1/.2 mm and mus=3/4.5, each envelope has 64 corner inputs: common gap
bias ±e; common Br bias ±b plus opposing hard/soft mismatch ±b; Hc ±h; gap and
permeability endpoints. These represent shared batch, differential parts and
spatial extremes, not independent samples or certified global extrema. Selected
lines lose current error i; half sites gain i plus total parasitic fraction p.
Tight: e=10 µm, b=.03, h=.05, i=.03, p=.02. Wide: 50 µm, .10, .15, .05, .05.
Explicit bounds, **not X1C or purchased-magnet priors**.

| Length / envelope | Equal-amplitude relay AT | Equal-amplitude k=1.5 AT |
|---|---|---|
| 5 mm / nominal + mus range | none: >140.64 / <80.40 | none |
| 5 mm / tight | none: >155.98 / <49.41 | none |
| 20 mm / nominal + mus range | 528.57–853.11 | none: >891.02 / <853.11 |
| 20 mm / tight | 575.98–748.02 | none: >968.60 / <748.02 |
| 20 mm / wide | none: >656.23 / <568.80 | none |

Asymmetry rescues 20-mm nominal k=1.5: set 891.02–1,041.73, reset
792.86–853.11 AT. Tight k=1.5 removes both; wide relay fails reset. The source
also reports k=2/4.64, neither passing any enumerated envelope. Fixed-gap EPM
therefore remains conditional. Common ±50-µm gap shifts alone leave the 5-mm
.1–.2-mm span without an equal-amplitude window. No yield/probability follows.
Correlated faults can switch rows; mismatched Br gives OFF attraction. FDM mounts
add warp, alignment, hole bias, layer quantization and creep. Return-spring wear
and roughness affect motion but do not repair failed field windows.

## Bounded stroke and full-machine accounting

A resident EPM armature could pull a rack-driving pawl upward one tooth against
a normally engaged grounded catch. OFF plus a spring resets that pawl. Lowering
needs an opposing escapement catch engaged at the next tooth **before** the old
catch releases, followed by controlled descent; count a direction mechanism or
second drive. No lowering/overlapping-catch geometry is constructed. M-004 owns
the principle. A one-tooth fault bound requires a positive next catch in every
release state. Retained EPM ON after input loss may hold an armature at its stop;
it does not itself hold the output rack.

Frozen-remanence work from g=1.05 to .05 mm is .7799 mJ before spring/friction/
impact losses, versus 1 mJ for a 1-N/1-mm lift or 10 mJ at 10 N (load scenarios,
not requirements). Open-gap demagnetization invalidates even that allowance.
More area/mechanical advantage trades packing/stroke, not energy. Grounded teeth
could avoid E-149 magnetic-well escape only with the omitted sequence constructed.
Stop before treating a force scalar as working geometry.

For 80×80 and 40-mm travel, d=.5/1/2-mm steps need n=80/40/20 cycles. Conservative
arbitrary-map protocol: raise and lower stages per increment; rowwise set eligible
sites, complete a stroke, individually reset activated sites. Do not grant a global
reset that spares other modes/banks. B independent row banks need
`4*n*ceil(80/B)` row transactions. Grant 10 ms/shared mechanical stroke and
6 s/map for preparation, registration, final proof, one supported retry and settling;
these are unearned allocations. One-sign maps need fewer stages.

| Step | Unbanked transaction ceiling for <30 s | Eight-bank ceiling |
|---:|---:|---:|
| .5 mm | .875 ms | 7.00 ms |
| 1 mm | 1.8125 ms | 14.50 ms |
| 2 mm | 3.6875 ms | 29.50 ms |

No winding transient/stroke/proof model earns these limits. Published 1-s pulses
are neither a lower bound nor qualification. Regional masks still expose retained
half-selected sites. Read rack height and catch support, not magnet state/current.
On mismatch inhibit motion, retain proved catches, permit one supported correction,
then isolate the module. False acceptance is unbounded; repeated pulses do not
resolve common line/reader faults.

One EPM/site requires at least 12,800 magnets, 6,400 pole/yoke/armature sets,
12,800 local winding sections, 6,400 racks/drive pawls, grounded catches, lowering/
direction parts, springs, guides and readback. Series row/column wiring reduces
independent lines to 80+80B per array, not local winding inventory. A second drive
array adds its own inventory. High AT costs turns/current, copper, voltage rise
and heat. Longer magnets can occupy depth but do not erase assembly/repair costs.
No packed X1C geometry supports a printed mass/time/scrap estimate.

Assuming $250 shared reserve, <$500 purchases allows <3.906 cents/site for all
resident hardware; two magnets alone must average <1.953 cents each before iron,
copper/springs. At $400: 2.344 cents/site, 1.172 cents/magnet. No quote supports
these allowances; the $200 ideal band is already consumed by the assumed reserve.
Ten seconds/site assembly is 17.8 hours before winding/calibration/rework.
All-1-N raising needs 256 J useful board work; copper/core losses, spring cycling
and energy disposal during lowering are extra. No BOM/thermal qualification.

## Disposition and verification

Stop scaling the tested opening-gap drive. Keep small fixed-gap/long-core EPM
only as conditional memory. Reopen with a defensible full-write/half-disturb law
or changed addressing path, including gap history and signed mechanics. Biased
sequences, gap-aware schedules and saturable shunts were not solved; they inherit
no blanket rejection but need arbitrary-old-state/reset closure. No print yet.

Next: positive-displacement metering with an always-engaged output constraint.
Read E-134/E-139/E-147 before finite bidirectional rack escapement versus
captured-cam/indexing comparison. Seek a geometrically blocked next state under
both load signs/input loss; stop/recombine if it hides another capture pair or
repeats known free-input support failure. Material/current tuning is lower value.

Self-review: flux conservation, independent reluctance loops, OFF cancellation,
zero/large-gap and area limits, asymmetric rescue, force/energy derivative error
<1e−10, 24,576 transactions, failed half-select/reset histories and unbiased k<2.
Independent trapezoidal stroke-work errors: 2.09e−5/1.31e−6/8.17e−8 at
64/256/1,024 intervals. These check reduced equations, not actual magnetic geometry,
contact continuity, hysteresis, electronics or hardware performance.
