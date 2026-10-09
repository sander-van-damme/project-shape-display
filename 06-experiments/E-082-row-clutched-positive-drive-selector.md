---
status: complete
builds-on: [E-077, E-079, E-081, M-011]
---

# A row clutch removes blocked springs but adds insertion, bending and scan limits

**Retain row-clutched push/pull addressing as a changed coupling topology, not an
accepted selector.** A finite pin/socket section fits the ±0.10-mm box, but its
force window depends strongly on common sliding drag. The specified serial
stop-and-go controller fails the five/21-height adverse workloads. Stop further
single-row width tuning. E-083 completes the banked addressing/mask comparison;
ADR-014 retains only conditional reserves with explicit reopening gates.

Input main `3a4688e`. Reproduce:
`python3 tools/curated-experiment-checks/E-082/row_clutch.py`.
Standard-library deterministic section synthesis, corner enumeration, kinematic
replay and analytical bounds. **All dimensions, friction, loads, modulus-free
strength allowances and accelerations are epistemic scenarios**, not X1C priors,
supplier data or measurements. No probability, manufacturing yield, field/contact
solution, assembled CAD or hardware qualification is reported.

## Changed addressing mechanism and sequence

Place 80 long column bars below the command dogs. Each bar translates in x and
carries 80 captive vertical keys. A row rail raises/pulls down the 80 keys in
one row; their captive feet must slide in x along that rail. Raised key tips
enter downward-open rectangular sockets in the dogs. Column bars then push
or pull those dogs to either command endpoint. Lowered keys stay clear while
the bars program another row. Separate upper bosses route cam energy as in
E-077. Independent column support remains in the pawls/grips, not these keys.

This replaces two shutter apertures and blocked push springs with one row
clutch per intersection plus 80 bidirectional shared data drives. It is a
mutation of M-011's mechanical matrix, not a renamed magnetic flag or a new
height-support architecture. Selection, power and reset have causal paths:
row lift engages keys; column translation supplies set/reset work; vertical
clearance isolates unselected rows; endpoint retention stores the command.
Retention itself is still a required detent, not a property of an open socket.

Specified serial protocol: park cam → with all rows withdrawn, align bars to
the **known old** command endpoints → raise selected row → drive new endpoints
through bounded series compliance → unload/recenter bars inside the sockets →
withdraw row positively → prove withdrawal and read command endpoints → enable
cam. Unknown old states inhibit insertion; recovery needs direct readback or
an explicit reset tool. Addressing a row is not permission to change its
unchanged command bits. A row must be withdrawn before arbitrary column changes.

The nominal two-cell replay exhausts all 16 old/new binary combinations,
including simultaneous set/reset and unchanged bits. It traverses the actual
pin-to-socket free gap, then a side-wall contact to the stop; recentering removes
side load before extraction. Affine path endpoints bound the continuous nominal
section. Retention during recentering is an explicit prerequisite, not simulated
spring physics. A broken/jammed key invalidates isolation; plate position alone
is insufficient, as E-077 established.

## Finite section and uncertainty

Dog stroke d; socket width S; square pin width p; nominal side gap g=(S−p)/2.
Socket walls are 0.4 mm each, with another 0.4-mm guide reserve per side.
The dog has a 2-mm-high lower socket body with 0.4-mm roof; pin tip moves from
−0.4 to +0.6 mm relative to its underside. The upper cam boss is 0.8 mm wide.
Socket depth in y, guide/foot/rail and detent packaging are **not** synthesized;
this is a finite x/z joint section, not full 3D clearance acceptance.

Bound pin and socket centers, full widths and dog stop offset independently
by ±e. Pin/dog z registration each varies by ±e. The stop offset must be counted
again when inserting into an already retained dog; knowing its binary state
is not knowing its manufactured endpoint. Wall thickness is fixed in this
screen; actual wall/edge/tilt and compliance errors reduce the displayed reserves.

Exact worst margins are:

- Insertion: `g−4e` (two centers, one stop, two half-width contributions).
- Adjacent opposite-state dog envelopes: `5.08−d−S−1.6−4e`.
- Upper cam overlap/bypass: `0.8−4e` / `d−0.8−3e`.
- Withdrawn z clearance / raised engagement / roof gap:
  `0.4−2e` / `0.6−2e` / `1.0−2e`.

Generate d={1.2,1.5,1.8}, S={1.2,1.4,1.6,1.8,1.85,2.0},
p={0.6,0.8,1.0,1.2} mm. Of 72 sections at each error bound,
27/6/0 pass at e=0.05/0.10/0.20. The wide box also closes withdrawn clearance;
counts are generator outcomes, not independent-cell samples. Coherent bar or
row shifts are included in the box and are never averaged over the board.

At d=1.2, S=1.85, p=1.0, e=0.10 mm, insertion and neighbor reserves are only
**0.025/0.030 mm**; cam overlap/bypass are 0.40/0.10 mm and z clearance/engagement
are 0.20/0.40 mm. A further 0.03-mm relative error defeats this witness.
A slimmer d=1.5, S=1.4, p=0.6 section has zero insertion reserve at this error
bound and also fails the transverse force screen below. Its nominal fit cannot
be promoted using the earlier axial writer capacity.

## Lateral pin load and common drag

A pin now receives **bending**, not E-077's axial tension. For square minimum
width b=p−e, effective force lever L=1 mm and hypothetical effective allowable
sigma=10 MPa, a cantilever section gives `F_pin=sigma*b³/(6L)`.
The 0.6-mm pin permits only 0.2083 N; the 1.0-mm witness permits 1.215 N.
These are necessary stress bounds: root notches, socket bearing, foot capture,
bar bending, fatigue and elastic error can reduce them. A shorter supported
lever or metal key changes the mechanism/cost and may reopen this bound.

Assume every captive foot contributes f N of x drag, coherently across a bar,
and the selected dog requires at most 0.3 N to cross/hold through its detent.
Then `F_req=80f+0.3`. A one-key jam can receive the entire input force; no
load-sharing credit is allowed. Actual detent geometry and this 0.3-N bound
remain unproved. Per-column series spring stiffness k bounds stop error:
required contact overtravel lies in `g±4e`, so a fixed input with minimum
compression `F_req/k` can reach `F_peak=F_req+8ke`. It needs
`F_peak<F_limit<F_pin`, including limiter uncertainty and dynamic overshoot.
This is a necessary static window, not a qualified jam interlock.

For f=0.005 N, k=0.5 N/mm, F_req=0.7 N and F_peak=1.1 N, leaving only
**0.115 N** below pin capacity. The chosen sufficient drive/unload strokes
are `d+g+4e+F_req/k` and `g+4e+F_req/k`: **3.425/2.225 mm**.
At f=0.010 N that stiffness fails; k=0.1 restores a tiny 0.035-N window but
requires **13.025-mm** drive stroke. At f=0.030, F_req=2.7 N exceeds pin
capacity before spring sizing. Halving/doubling the assumed allowable halves/
doubles capacity; none of these drag or strength scenarios is calibrated.

For the low-drag witness, even an ideal force cap at pin capacity allows at
most (1.215−0.7)/m acceleration: 103/25.75/10.3 m/s² for 5/20/50 g moving mass.
These optimistic bounds exclude overshoot, transmission inertia and the larger
end-compression force. The separate 100-m/s² timing scenario is therefore not
a demonstrated compatible drive. A common row withdrawal rail also needs its
own finite force/deflection interlock; this source does not implement one.

## Serial schedule and complete-system implication

For each row, allocate five rest-to-rest input legs: prepare ≤d, engage 1 mm,
drive 3.425 mm, unload 2.225 mm, withdraw 1 mm. With infinite speed limit and
acceleration a, each leg takes `2 sqrt(D/a)` in SI units. This chosen worst-leg
controller grants instantaneous readback, settling and row addressing. It is
not an optimal scheduler, nor a dynamic solution of the spring/bar system.

| Row writes from E-081 | Motion alone at 20 m/s² | Motion alone at 100 m/s² |
|---|---:|---:|
| 320, favorable direct-displacement cyclic maps | 29.134 s | 13.029 s |
| 800, five-height adverse/reset maps | 72.835 s | 32.573 s |
| 3,360, 21-height adverse/reset maps | 305.907 s | 136.806 s |

Add the E-081 **assumed** 6-s non-row allocation and all omitted row overhead.
Only the 320-write/100-m/s² numerical case retains time headroom; it does not
establish an arbitrary-map or actuator pass. Five/21 states remain workloads,
not new product height requirements. Even deleting all horizontal work, the
serial 1-mm engagement/withdrawal pair takes **42.501 s** at 3,360 writes and
100 m/s². Fitting that pair alone into 24 s requires **a>313.6 m/s²**.
These rejections apply to the stated serial sequence. Overlapped partial row
motions, continuous coupling or more banks require an explicit new schedule;
no universal lower bound over those architectures is claimed.

One array still has 6,400 dogs/detents, **6,400 captive keys and sliding feet**,
80 column bars/force-limited drives and 80 row rails. Individual row actuators
add 80 channels; a travelling row lifter substitutes indexing and registration,
not a free decoder. A second array duplicates these unless a physical shared
command sequence proves reuse with independently retained grip/pawl outputs.
Repeated friction/assembly burden is relocated, not eliminated.

At a hypothetical $250 bought reserve, 80 data channels can average strictly
less than $3.125 before any row drive, key purchase or other omitted hardware;
160 independently driven row/data channels less than $1.5625. Bought keys at
$0.02 each consume $128, leaving $1.525 per 80 data channels under the $500 cap
before row drives. These are allowances, not quotes. Print time, assembly,
service access, false read acceptance and recovery remain unquantified. Local
row addressing preserves nominal unselected dog state; shared frame vibration
and actual column support/isolation remain separate gates.

## Decision and checks

The positive drive removes passive snap-completion dependence, but it does not
remove endpoint retention, high-density fits, common drag or serial scan time.
Keep only a conditional low-drag joint comparator; reject treating the tested
serial implementation as a five/21-height whole-board solution. No printing.
E-083 resolves the banked/differential-mask comparison: numerical time survivors
need many complete drives within very small residual allowances. ADR-014 closes
the campaign with conditional reserves and explicit reopening inputs, rather
than further aperture/spring sweeps. Magnetic comparisons remain governed by E-080's
signed-pulse and finite-field gates; this joint supplies no magnetic validation.

Self-review, not independent validation: all 216 generated sections reconstruct
32 error corners for insertion and stop contact; independent interval endpoints
check neighbor envelopes. All 16 binary two-cell transitions pass the nominal
contact replay, including reverse reset; rectangular pin/wall overlap detects an injected failed
withdrawal. Zero-distance and integrated triangular
motion limits agree; wide-box fit, stiff spring and increased-drag counterexamples
are retained. These closed-form checks need no timestep convergence claim.
