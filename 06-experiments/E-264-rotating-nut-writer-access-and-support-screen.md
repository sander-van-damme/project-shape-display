---
status: complete
builds-on: [E-262, E-259, E-261, E-156, E-195]
---

# Rotating nuts trade long-shaft rotation for writer access

**Park the closed annular row-socket implementation before CAD.** Rotating a
short nut instead of a long screw removes the latter's rotating-shaft excitation,
but its translating tail obstructs the writer. Under the stated sequential access
policy, full-depth extraction makes the 64-grid scene maxima38.95/45.51s at
40/50-mm travel, even granting2000rpm. Retain rotating nuts as a conditional
architecture alternative: side access could escape this specific obstruction.
No new print, purchase, head selection or physical speed/support pass follows.

Reproduce: `python3 tools/curated-experiment-checks/E-264/access.py` (`--check`
for controls). Standard library; JSON is disposable. Evidence is sourced mechanism
principles, interval geometry, analytical bounds and scheduling; self-review only.
No material/contact priors, mating CAD, measured reliability or cost quote is added.

## Changed topology and historical scope

[Roton screw motions](https://www.roton.com/screw-university/screw-basics/screw-motions/)
confirms the rotary-nut/translating-screw alternative. [Thomson critical-speed
training](https://www.thomsonlinear.com/en/training/ball_screws/critical_speed)
separates screw and nut speed limits. Both checked2026-10-13; the commercial
ball-nut ratings do not transfer to a printed sliding nut. Removing shaft spin
is not immunity to forced vibration, nut runout, wear, heating or buckling.

E-156 already used a captured rotating nut, translating screw and selective belt;
E-182 tested its field writer, and E-195 retained a rigid translating-screw control.
This is **not a newly invented motion principle**. The changed comparison uses
historical3-mm lead (rough owner2-mm lead as sensitivity), current physical
river/ravine scenes and independent stopped rotary channels. E-156's .15-mm lead,
40,000rpm, belt-retained source inertia, selector force and coast results keep
their original scope. None establishes present moving arrest or bans rotating nuts.

Candidate load path: miniature→square guided stem→nonrotating screw→threaded
rotating nut→captured thrust faces→shared bed/frame. Two stationary square guides
react torque and lateral loads. Nut radial location and bidirectional thrust capture
remain resident during docking and power loss; the writer never takes over axial
support. Relative thread angle stores height. Static friction/seat drag must hold
that angle after drive removal. Owner-reported hold of a different pair does not
qualify this nut or its changed thrust friction. A seized/stripped nut, failed
capture or moving power loss can defeat support; encoder position cannot prove it.
Stop, verify actual top/holding, then disengage. Failed proof requires retained
support and bounded recovery; no invented brake or free optical visibility.

## Finite travel and support construction

Coordinates in mm, z upwards, stroke S40/50, commanded rise u in0..S:

- Fixed nut occupies[0,10]; translating thread[u−S−2,u+12]. Thread stock S+14
  preserves2-mm full-overlap end margins. Hardware stops are still unbuilt.
- Square stem runs[u+12,u+S+56], joining the screw without an assumed detachable
  insert. Guides occupy[S+14,S+16] and[S+54,S+56], with40-mm center spacing.
  They always bear on square stem, never thread; full slab coverage is checked.
- Cap underside is u+S+56. Combined axial stock is2S+58=138/158mm; lowest cap
  is96/106mm above nut bottom. The longest tail lies42/52mm below it.
  Thus minimum-surface-to-lowest-tail envelope is138/158mm, before bed, writer
  and base. Maximum cap adds40/50mm. This is a feasible interval allocation,
  not finite bearing/end-stop CAD or a minimum possible machine height.

The longer solid stem is a cost of this simple route, unlike E-261's hollow pin
around a resident screw. Thin hollow square stem manufacture is an alternative,
but the screw/stem transition and service route must be constructed. The nut can
be printed/cast as one rotor with drive features; adding bought miniature bearings
or individually bonded screw inserts is not assumed.

Compression still matters. Nut top to lower guide is S+4=44/54mm. Treating that
entire segment as root1.4-mm polymer at assumed E1000MPa gives EI188.574Nmm².
Ideal pinned/pinned Euler values are .961/.638N; the cantilever controls give
.240/.160N. These are onset calculations under ideal supports, not rated loads or
bounds on a loose assembly. The actual stepped stem is stiffer than this root-only
section if its transition holds. Guide clearance/seat compliance can instead
remove assumed restraint; E-262's support lesson remains. A .2N scenario cannot
be accepted merely because one pinned formula exceeds it. Material/creep,
eccentric loading, print bow, frame correlation and thread stripping are unmeasured.

## The closed-socket obstruction

A closed coaxial socket surrounds the threaded tail. At u0 the tail extends42/52mm
below the nut. Dropping the socket2mm leaves it threaded around that tail even
when torque contact has disengaged. Lateral row motion must cross the closed
annulus wall. It cannot leave until the socket top clears the tail, or the socket
opens, the tail moves, or the drive approach changes. Resetting unchanged pins
to shorten their tails would violate the intended regional isolation.

Grant1-mm axial clearance: a universally clear transit plane needs43/53mm withdrawal.
The writer needs a through-bore/open drive route or cavity longer than the tail;
a motor directly closing the bore is not allowed. Side motor/transmission and
return routes remain unbuilt. End capture retaining the nut during extraction is
also unbuilt; no tall individual cartridge is selected.

Illustrative head-only radial allocation: nut OD4.4, socket ID4.7, .6-mm socket
wall gives OD5.9. Same-row socket gap is−.82mm at5.08 pitch and+.45mm at6.35.
Opposing radial growth .1mm each and .1mm relative center error reduce .45 to.15;
.2 each plus .1 gives−.05. These are labelled coherent bounds, not printer priors.
The numbers do not prove a torque interface or space for resident thrust seats.
The80-grid timings below grant a narrower/tiered head that has not been routed.
Do not repair that packing assumption with another fine-feature campaign.

## Paid access versus conditional speed gain

Reuse E-259's B2, K32 powered channels/head,1000rev/s²,3-mm lead, fixed row banks,
seek/return, .08-s selection/docking plus .02-s proof, four-second common allowance
and one conservative full-row retry. Installed channels remain128/160. New common
Z travel uses200mm/s and5000mm/s²; no simultaneous Z/Y motion is credited.
The old .08-s allowance is retained in full, so the added Z charge is conservative
about any small dock overlap. These are unqualified rates/overheads, not measured
end-to-end updates; homing/readback/settling still need physical implementation.

The adaptive policy uses all tails in each crossed row, including unchanged cells,
the new heights in the departed row and old heights ahead. Start/end remain at the
full-clear plane. It can shorten some transitions but does not improve the suite
maximum versus fixed full withdrawal. Returning below all tails makes recovery
possible geometrically, not safe against an actively backdriving nut.

| Grid / stroke / neutral | Free-access2000rpm control | Closed-socket2000rpm | Faster Z400mm/s,8000mm/s² | Rotating-screw850rpm control |
|---|---:|---:|---:|---:|
|64 /40 /20|22.12s|38.95s|32.51s|35.54s|
|64 /50 /30|25.38s|45.51s|37.43s|43.29s|
|80 /40 /20|28.07s|48.98s|40.98s|46.40s|
|80 /50 /30|33.50s|58.51s|48.47s|59.31s|

S40 runs the physical shallow scenes. S50 retains software shallow/deep presets
at fixedN30, including cross-preset transitions. It does not reinterpret a visual
river as physical relief or count software zero as extra motion. Both pitches
cover406.4mm; the64-grid/6.35-mm case has4096 cells versus6400 at5.08mm.
These three annotated maps remain a convenience sample, not observed typical play.

At64, closed-socket cold preparationN20/N30 costs42.81/52.71s; dense0→40/50 stress
56.01/65.91s, separately. At80 these are61.28/77.68s and85.88/102.28s.
Lead2 raises64-grid scene maxima to44.15/52.36s. The850rpm controls are not safe
ratings either. Missing~30s is a transparent tradeoff, not a universal rejection;
the new mechanism currently offers no demonstrated support or total-cost advantage
that pays for this access and stock burden. Faster Z can improve it but adds
unqualified force, moving mass and vibration. No modeled number earns2000rpm.

## Repeated duties, manufacture and next discriminator

Both layouts retain4096/6400 screws, nuts, thread pairs, resident thrust/radial
support and two shared guides (8192/12800 apertures). Inversion changes which
member moves; it does not eliminate those duties or prove cheaper fabrication.
No extra resident brake is introduced. The candidate adds long screw/stem stock
and nut drive rims; B2 adds128/160 hollow rotary tools and two common long-Z
carriages, their transmissions, cables, alignment and recovery. AtS50,158-mm
combined stock totals647.168/1011.2m, not material volume or print time.

E-259's dated motor/driver subset plus unquoted reserve is still$984.64/$1166.40,
not a new quote or BOM. Under$1500, $515.36/$333.60 remains for **all** missing
hardware, including these hollow drives and Z axes. $500 is already exceeded;
$1000 leaves$15.36/−$166.40. No finished product price or purchase permission.
Every extra10s resident operation adds11.38/17.78h; a minute adds68.27/106.67h.
Shared split beds must permit supported local nut/screw replacement without
unthreading an entire board or discarding a sealed module. Cast/molded rotors,
formed/machined hollow tools and outsourced shared beds merit comparison only
after access earns it; tooling, alignment, wear and assembly are not free.

**Next independent discriminator:** construct a coarse finite side-access route
between the real translating tails and resident nut beds; include service to both
adjacent rows, disengagement, unchanged-neighbor torque isolation and supported
power loss. Compare open positive-contact and friction contacts with E-156's
failures. Stop at an impossible swept route or implausible repeated burden before
selector detail. A split socket also changes topology but needs its own complete
closure/torque/release path; it is not a free exception to this result. E-263's
single optional manual print job stays unchanged; no human response blocks this
architectural work.

Checks:362 quarter-mm axial/guide states, exact dense access increment,
all inherited scene schedule anchors at zero added access, no-op and policy
ordering, motion-law/section scaling, and a low **unchanged** intermediate-tail
witness. No independent hardware validation is claimed.
