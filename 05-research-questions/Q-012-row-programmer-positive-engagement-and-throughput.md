---
status: open
builds-on: [A-013, Q-009, Q-011]
---

# Can row programming retain positive support within cost and timing limits?

Determine whether an independently addressed rack/pawl head can acquire arbitrary initial heights, unload, release, reposition, relatch and verify at final pitch without disturbing non-targets. Compare 80 independent linear channels against a common elevator with independently disengageable grippers; the latter must explicitly implement capture at different initial heights, isolation, lowering and reset. Address-bit counts do not establish that mechanism.

Next discriminator: complete channel BOM and load-dependent motion for those two alternatives, including actuators, release channels, grippers, readers, links and recovery; require this before further local pawl refinement. With $250 shared hardware reserve, the $500 ceiling permits $3.125 per 80-head channel or $1.5625 per 160-head channel before any cell purchases. These are budget envelopes, not supplier prices. Reject channels exceeding the envelope or lacking continuous support; do not further optimize their nominal timing.

Bound common alignment error and per-cell fit separately. Required overlap and pitch compete; changing to staggered wider internal supports is allowed by stage 02 and should be compared with a single-plane latch. A viable route needs a complete <30 s schedule and a bounded load/support model; absence of a robust survivor does not justify printing. Calibrate only if an actual remaining fit/friction parameter changes selection after cost and geometry survive.

E-051 rejects the zero-offset, stop-at-contact 80-head shared elevator under the fast E-050 bounds (33.350 s even with instantaneous contacts). A 160-head version needs <32.73 ms total dwell per event stop at fast motion; central motion fails before contacts. Require an affordable implemented gripper/release contact sequence within that bound before further optimization. Continuous-motion capture or independently offset grippers change the model and remain unexplored; do not inherit the rejection.

E-051's load extension reduces mixed-map peak attachment with delayed capture,
but uniform maps still attach all heads. Its symmetric fast profile exceeds
gravity: unsecured miniatures on changed cells cannot retain contact. Limiting
vertical acceleration to g tightens the 160-head dwell ceiling to <15.97 ms
with zero normal-force margin; at 0.5g even zero dwell fails for symmetric motion. These are conditional
loaded-surface bounds, not a new requirement on changed cells. Carry this scope,
full-row moving mass and support-proof timing into the geometry/cost comparison.

E-052 supplies a conditional translating-pawl swept section: at a 0.35-mm
relative placement bound, an interior witness needs 4.89-mm width, 1.22-mm
withdrawal and 0.47-mm unload. A continuous packing bound rejects the 0.60-mm
case for web≥1.6/pawl length≥0.8 mm, even though the coarser grid also missed
the feasible middle case. This does not implement the guide, return/retention,
gripper or release drive and does not inherit E-050 strength or timing passes.
Carry the actual withdrawal/unload operations into head synthesis and costing;
stop refining the bare section grid. Wider staggered supports remain an escape.

E-054 side-cheek rails escape the rear-guide obstruction. Equal 0.4-mm walls/shelves fail the assumed 10-N/8-MPa strip-bending screen, but decoupling shelf thickness to 0.8 mm retains the same 4.89 × 5.00-mm middle-bound footprint and avoids that rejection. Retain this conditional geometry; next resolve side-wall grounding, plate/contact behavior, loaded rotation and complete channel cost. Do not promote it or print from clearance alone.

E-055 finds no opposing-shelf angular stop and rejects same-section lengthening to the tested middle-bound 5–15-degree stops within pitch. E-056 shows that a seated vertical load can nevertheless balance on the lower shelves. Uniform tooth pressure gives conditional absolute H/F≤0.105, falling to 0.055 with 0.10-mm bearing-edge loss; arbitrary edge pressure has zero guaranteed margin. E-057 resolves the inset-pad screen: retaining 0.40-mm overlap gives only 0.02-mm pitch margin before bearing-edge loss. A pawl-fixed pad reaches 0.12-mm margin at 0.10-mm edge loss only by reducing overlap to an unqualified 0.20 mm. Stop pad refinement; retain keyed/staggered guidance with unloaded capture/return/retention for investigation after the channel-cost gate. Reject missing continuous support or unaffordable channels before detailed FEA.

E-050 now enumerates all 1–80 complete row banks with 0/1/8 total full-station
retries, exact rational price ceilings and aligned/adversarial 5×5 allocations.
The 240-head central case takes 24.4974 s with one retry and permits at most
nine retries. Its exact channel ceilings at $250 reserve/$500 cap are $25/24
with free cell hardware and $61/120 at $0.02/cell. Fast 80-head timing permits
only two full-station retries. The 240-head central one-retry regional
allocation is 6.0924–6.8286 s, subject to dispatch/return fitting the fixed
overhead. At fixed reserve and cell spend, a channel above the smallest
passing bank's ceiling rejects every tested larger bank. For $250 reserve,
purchased cell cost ≥$5/128 leaves no positive channel budget under $500.
Continue only to a complete channel and load-dependent bank schedule within
these bounds; stop nominal pawl refinement. Reopen with changed schedule,
reserve, purchased-cell allocation or sourced channel evidence. This is a
conditional system envelope, not a supplier BOM, hardware feasibility or print
release; keyed/staggered support remains unresolved after the cost gate.

E-058 adds a shared-power gate to that channel comparison. At 240 heads,
central motion, 20 g moving mass/lane and 50 W lift allocation at 50%
efficiency, sustained 0/1/10 N additional resistance gives optimistic
arbitrary-map bounds of 23.8774/28.5665/120.7265 s without retries. The 1-N
case already requires reshaping the synchronized nominal profile (124.44-W
peak). These are correlated bounded scenarios, not measured guide friction;
10-N static support is not automatically a moving-load requirement. Require
force–speed, efficiency and actual supply allocation in the complete-channel
BOM. More parallel heads do not eliminate full-map lift energy. Retain the
channel-cost gate and stop local pawl refinement; no print release follows.


E-051's asymmetric extension narrows that loaded-surface rejection: retaining
20 m/s² upward acceleration while limiting downward acceleration to 0.5g
preserves an ideal half-weight normal force and gives 26.618 s at 160 heads
before contacts. Total event dwell must be <9.395 ms; 10 ms already fails.
Uniform up/down maps take 15.878 s but still attach all heads. This is an
ideal common-profile calculation, not actuator or miniature qualification;
upward force peaks remain unchanged. Carry this conditional comparator into
the complete channel/drive comparison, and stop schedule refinement until
cost and the support-proof contact critical path have evidence. No print.

E-059 excludes the sourced FS0307/FS90 servo-per-head route before gripper
and release design: 80 positioning servos alone exceed $500. A cheaper
complete channel needs actual price and loaded-motion evidence; a shared-energy
selector needs an explicit capture/release/support-proof critical path within
E-051's dwell gate. Stop layout of these catalog-servo embodiments; their
rejection does not generalize to all suppliers or shared actuation.

E-051's serial-contact extension includes E-052's 1.22-mm pawl stroke and
0.47-mm unload. It excludes both tested 160-head half-weight-margin serial
paths even with instantaneous pawls: an optimistic one-vertical-leg-per-stop
relaxation already takes 32.179 s. Unloaded seat-cycle motion takes 30.820 s
at 20 m/s² lateral acceleration; at 50 m/s² it takes 28.753 s but leaves only
3.463 ms/event for omitted grip/proof/settling/recovery. These are stipulated
motion bounds, not drive capability or qualified geometry. Stop serial dwell
refinement. Next realize an affordable selector/support-transfer mechanism;
merging microtravel with transit or independent gripper support must replay
actual geometry and coordinates and cannot inherit the old timing pass.
