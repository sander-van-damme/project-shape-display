---
status: complete
builds-on: [E-198, E-054, E-056]
---

# A floating fold removes axial constraint but retains guide-friction leverage

**Stop passive-return refinement of this single folded suspension with E-198's
short backed island.** A freely translating/rotating turnaround nearly eliminates
the straight-leaf axial reaction. It does not eliminate the leaf's end moment:
the guide must resist that moment across a short contact span. Nominal sticking
is admissible at a traction/normal ratio about .0088, below the explicitly assumed
μ=.01/.05 bounds. This is a quasistatic counterexample, not a measured friction
threshold or rejection of folded suspensions generally. Retain shared manufacture
as an assembly option, without selecting a machine or fabrication process.

Input main `90b8939`; LAB-326. Reproduce with
`python3 tools/curated-experiment-checks/E-199/folded.py` (Python + NumPy).
Evidence: generated finite envelopes, variational beam calculation, unilateral
contact equilibrium and self-review. No physical measurements, process priors,
3D contact/plate simulation, dynamic return or independent review. JSON output
is reproducible and discarded.

## Changed mechanism and finite construction

The changed topology is a **floating U turnaround**, not a guided replacement for
the forbidden shortening in E-198. The primary-source analogy,
[US20160006372A1](https://patents.google.com/patent/US20160006372A1/en), describes
folded-beam shortening accommodated by floating bars and distinguishes static
balance from inertially induced axial stresses. It motivates the free bar degrees
of freedom; its MEMS dimensions, dynamic claims and material performance are not
transferred here. Accessed 2026-10-11. This is one continuation of the manufacturing
axis, not another independent architecture-search count.

Use E-198's 5.08-mm pitch, island x=[−1.75+q,.9+q], z=[−2,0], thickness .4
in y, q∈[−.75,0], and its rack with five heights 0/10/20/30/40 mm. One U per
island has two .1-mm-wide legs: anchor top (x,z)=(−.45,−3), output top
(−1.45+q,−2), natural output x=−1.25. Their unstressed lengths are 41/42 mm;
.2-mm preload is imposed by assembly. Bottom endpoints join a rigid .8-mm-span,
.3-mm-deep bar near z=−44. Its horizontal translation, rise and rotation are
solved, not prescribed or externally guided.

A sheet neck x=[−.65,.15], z=[−3,−2.5] joins the anchor to a fixed .1-mm rib
x=[.05,.15] down to a common spine z=[−46,−45]. The neck is captured in a
root bridge spanning y=±1.4, connected to E-198's side posts; the spine meets
the ground base at z=−46. These rigid bonds/clamps are explicit idealizations,
not qualified attachment designs. This route keeps a connected patterned sheet
without placing a transverse spine in the rack's 40-mm travel envelope. It adds
6,400 fixed ribs and floating bars; they are not separate placement operations.

Generated beam envelopes, bar, island, root bridge/rib/spine, frame and neighboring
rack envelopes clear at nominal dimensions. Release/reinsert occurs after .2-mm
rack unloading; all twenty unequal height transitions are checked while withdrawn.
4/16/64 subdivisions give 125/425/1,625 rack/island poses. The smallest turnaround
clearance above the common spine is .70014 mm. Leg envelopes remain disjoint.
Moving leaves, bar and fixed ribs stay left of the rack's x=.4 boundary;
the common spine lies below its entire sweep. The retracted island ends at .15. Neighbor rack webs end at x=−2.88, while the island extends
only to −2.5. These bounds cover intermediate rack travel, not just parked teeth.
Nominal guide faces still have zero play. Swept clearance is not contact acquisition,
assembly fit, arbitrary-map support continuity or a manufacturing yield pass.

## Beam and guide calculation

Units N, mm, MPa. E=200,000 and thickness t=.4 are metal-like assumptions. Each
leg has A=tw, I=tw³/12 and an Euler–Bernoulli transverse field v(s), represented
by endpoint Hermite cubics plus 0/2/4/6 independent polynomial bubble modes.
Integrated axial extension is

`e = end separation change + (1/2) integral(v'² ds)`;
`U = (EI/2) integral(v''² ds) + EA e²/(2L)`.

Minimize the sum over bar translation/rise/rotation and bubble coefficients.
A small-angle rigid bar supplies opposite ±.4θ changes of end height; the island
remains parallel to its guide. The source differentiates this energy for the
output horizontal force H, vertical force Fz and **end couple M**. Guide torque
about (x,z)=(0,−2) is `M + (−1.45+q)Fz` nominally. Omitting M is inconsistent
with the parallel end restraint.

| q mm | H N | Fz N | M N mm | Bar rise mm | Sticking traction ratio |
|---:|---:|---:|---:|---:|---:|
| 0 | .00011190 | −.00006838 | .00234354 | .00014463 | .0087743 |
| −.30 | .00027979 | −.00016006 | .00584102 | .00090382 | .0087549 |
| −.75 | .00053166 | −.00026759 | .01106277 | .00326251 | .0087392 |

Near engagement the vertical reaction is about 3,190 times smaller than E-198's
.21821 N, but that ratio alone does not predict return. The full-release guide
witness has .0305523-N lower and .0302847-N upper reactions. Their .0608371-N
sum supplies .000531665 N of opposing friction at traction ratio .0087392.
The active contact edges are lower x=−.25 and upper-front x=.15: their short
.4-mm moment arm, rather than the distant upper-rear face, opposes this moment.
All normal reactions are nonnegative and all three force/moment balances close.

The contact model uses six unilateral endpoint springs, at both ends of each
of the three E-198 faces. Equal stiffness taken toward the rigid limit selects
a contact branch without granting arbitrary interference preload. Static
tractions are −λNi with one λ≤μ, giving a sufficient sticking witness, not a
unique prediction of real friction. The common-ratio traction restriction cannot
exclude all compatible friction-cone equilibria. In particular, a pure horizontal force with no weight
or imposed interference can sustain guide wedging: lower x=−.25 and upper
x=.15 mm, separated vertically by 2 mm, admit N=2.5H on each face and
traction −.5H on each face at μ=.2. The normal couple −.4N balances the
upper-traction couple +H. This corrects the earlier broad no-witness claim;
the folded-return witnesses above remain sufficient counterexamples. At the
numerical regularizer k=10⁶ N/mm, maximum nominal guide rotation is 1.53e−7 rad; k is
**not** a claimed printed-guide stiffness. Finite guide play, pressure distributions,
compliance and resulting beam end rotation require a different coupled model.

An independent equal-length control gives exactly
`H=Etw³d/(2L³)`, `M/H=L/2`, `Fz=0`, and bar rise `.6(d/2)²/L`.
For two opposing contact edges separated by b=.4 and vertical spacing h=2,
force/moment balance gives `λ=b/(L+h)=.4/43=.00930233`, independently reproduced
by the variational/contact solver. Thus even perfectly matched legs with no
axial reaction have a sticking witness. Increasing E, stock thickness or return
force scales both H and guide normal force; it does not cure this friction ratio.

Self-review: endpoint work from independently differenced minimized energy matches
H within 1e−8 N; finite differences verify the analytical energy Hessian. Every
solved stationary point has a positive local Hessian. Four to six bubble modes
leave nominal H/Fz/M unchanged to displayed precision; zero to four modes changes
full-release Fz by about .075%, and H by less than .0001%. Geometry subdivision
checks agree. This tests the reduced model, not global uniqueness, exact elastica,
root stress concentrations, out-of-plane instability, bar inertia or wear.
Opposing contact stiffness ratios .1/1/10 and E=160,000/220,000 MPa reproduce
the nominal full-release ratio .0087392. Stiffness ratios change the tiny contact
displacements, while force/moment balance fixes the two active reactions here.

## Bounded manufacturing sensitivity and complete-machine comparison

The source evaluates twelve coherent error combinations at engagement/full
release: common leg-width bias ±.01 mm plus opposing ±.01-mm bias, and relative
output-attachment/seat height bias −.025/0/+.025 mm. These are **24 endpoint
scenarios**, not random samples or calibrated distributions. Widths range .08–.12 mm; both shared
and differential errors are represented. A common translation of the whole
assembly cancels; root-to-seat bias shared by a bank does not average away.
The nominal envelope check does not geometrically qualify these error cases.

Computed H spans −.00007694 to .00068177 N, Fz −.0132632 to .0131939 N,
and M −.0063440 to .0213774 N mm. Eight of these 24 endpoint cases reverse the
intended return force even at zero friction. The sixteen positive-H cases admit sticking at λ=.00481–.01876;
all are below the μ=.05 scenario. These counts are not failure probabilities.
Maximum bar angle is .02753 rad and peak reduced elastic strain .01297%; these are demands, not fatigue/strength acceptance.
The small-angle approximation becomes less accurate at the largest error cases;
those cases identify sensitivity rather than certify contact clearance. Gravity,
inertia and assembly preload are omitted; this unloaded idealization already
permits sticking. No yield,
service-life probability or physical return-time claim follows. Roughness, burrs,
residual stress, cutting yield, flatness, creep, guide wear, PLA anisotropy and
sheet-to-printed-frame registration remain unqualified. The .1-mm features are
cut-sheet hypotheses, not printable X1C features.

| Architecture combination | What this result changes; obligations retained |
|---|---|
| Folded sheet + backed positive lock + direct independent heads | Clears the specific axial-compatibility contradiction but fails guaranteed passive return in the stated contact scenarios. Still needs capture/unload, release, powered rack travel, return/seating, output/support proof and recovery. |
| Straight-leaf sheet, E-198 | Known axial-friction failure remains; no reason to retune only modulus or thickness. |
| Carrier-assembled rigid slider + separate force-only return | H-only, zero-gravity/zero-interference loading still admits friction-induced guide wedging at μ=.2 when independent contact tractions are allowed. The common-ratio control does not exclude it. A real return attachment, preload, gravity, guide play and friction must be constructed; this is not a completed return mechanism. Temporary carriers can share placement without integral leaves. |
| Same rigid slider + bilateral powered reset | Can avoid relying on passive-return margin, but needs actual push/pull engagement, jam detection, supported loss of power and completion proof. No free reset stroke, hardware or time credit. |

Forty-cell 203.2×46-mm allocated sheet envelopes require 160 placements and
1.495552 m² before nesting/waste/spares. The folded package retains 12,800 moving
leaves, 6,400 turnaround bars, fixed ribs and rack engagements, plus 19,200 guide
faces. A forty-site temporary carrier can also place 160 batches of separate
sliders; whether return fitting or carrier removal negates that benefit is
unmeasured. Shared sheets need independent support of forty columns before a
sheet replacement; individually removable sliders may reduce replacement scope
only if the carrier and guides actually permit extraction. No service-access win
has been demonstrated for either arrangement.

The complete bought ceiling remains `Cshared + Hheads*chead + 6400*ccell < $500`.
A hypothetical $250 reserve elsewhere leaves <$0.03906/site, or stock alone
<$167.16/m² if all processing/resident items were free. These are budget ceilings,
not quotes. The inherited schedule `6 + ceil(6400/Hheads)*s` gives 26 s for
160 heads and s=.5 s, exactly 30 s and therefore failure at s=.6 s. All capture,
unload, release, full travel, return, seating, proof, transport/preparation,
settling and bounded recovery must fit those allowances; this study earns none.
Unchanged cells stay seated in the intended local sequence, but root/frame
coupling, stuck-open outputs, readback false acceptance and moving-loss arrest
remain unresolved. Neither architecture passes the complete-machine gate.

**Decision/reopening:** retain E-199's finite folded geometry and moment-friction
failure; do not request a friction coupon or optimize another thin leaf. Reopen
passive return only with a constructed change that reduces the output couple per
unit return force, provides a different grounded contact topology, or explicitly
supplies bilateral reset. Paired opposed leaf moments are a possible synthesis
axis, not a free cancellation: mismatch, routing and added interfaces must be
counted. The next useful comparison should change the return/load-transfer
function or repair/assembly architecture, rather than further tune this fold.
No complete architecture is preferred by these results.
