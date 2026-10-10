---
status: candidate
builds-on: [A-003, A-007, A-012]
---

# Parallel rack programmer with grounded pawls

A travelling underside head bank independently grips column tails, unloads their positive pawls, retracts only those pawls, moves the columns to selected teeth, re-engages support and releases. Five provisional states at 0/10/20/30/40 mm; the requirements do not mandate five states. Each column has a rack, replaceable rigid pawl and guide. Service load closes through the pawl into a distributed base grid. A weak return element locates the pawl but must not carry service force. Inactive cells stay latched.

Unlike A-003's rejected printed shutter/register fanout, this embodiment uses independent linear positioning and pawl-release channels on 80 or 160 reusable heads. It trades selector complexity for expensive head count; it is a distinct embodiment within the travelling-writer family, not a newly discovered principle. Staggered actuators and links below the field must still be packed and checked. No existing 71-cell/s writer rate is inherited.

Sequence: acquire tail → confirm grip → slightly lift to unload → retract pawl → position → engage pawl → seat and verify height/support → release grip → return head → index. The motion budget includes an 80-mm total positioning path; separate engagement/seat time must cover unloading and recovery. Five-state arbitrary transitions are reachable in the abstract support-state machine. Physical contact continuity, release link collision, out-of-plane motion and acquisition over differing initial heights are unverified.

Head encoders plus an underside optical mark reader compare commanded and observed position before release; a short support-proof displacement/force check is needed to distinguish a supported column from a gripper-held column. Its timing is within the declared read/contact allowances, not established hardware capability. Failed reads retain grip and allow bounded retry; persistent faults stop the bank. A false support acceptance can drop a cell. Common registration/reader errors can affect a whole row. Replaceable underside row cartridges permit service but require access below the board.

Potential advantage: no physical mask transport, no 6,400 purchased actuators, direct arbitrary regional updates and positive local load support. Main liabilities: 6,400 pawls/returns, at least 19,200 critical guide/latch/grip interfaces, demanding head packing and unaffordable actuator count unless channel cost falls sharply. No product selection or print release follows from this proposal. E-050 is the first necessary-condition screen; Q-012 governs the next mechanism question.

E-053 rejects the fixed same-plane rear guide at the middle/wide placement bounds: even zero bearing span needs 5.25/7.00 mm against 5.08-mm pitch. The tight bound permits a conditional 4.75-mm section with 0.9-mm engaged guide allowance, not an assembled or load-qualified guide. Continue only with 3D/staggered support packaging or evidence for smaller error; do not extend E-052’s middle witness into a same-plane head.

E-054 side-cheek rails escape the rear-guide obstruction. Equal 0.4-mm walls/shelves fail the assumed 10-N/8-MPa strip-bending screen, but decoupling shelf thickness to 0.8 mm retains the same 4.89 × 5.00-mm middle-bound footprint and avoids that rejection. Retain this conditional geometry; next resolve side-wall grounding, plate/contact behavior, loaded rotation and complete channel cost. Do not promote it or print from clearance alone.

E-055 finds no opposing-shelf pitch stop; E-056 nevertheless establishes conditional seated vertical-load equilibrium on the lower shelves. Arbitrary edge pressure has zero guaranteed pitch margin, so neither clearance nor static equilibrium proves reliable support. E-057 rejects robust inset-pad support at inherited overlap; retain the slot as a comparator and keyed/staggered guidance as the geometric alternative with explicit unloaded capture, return and retention. Q-012 retains the complete channel-cost and support-sequence gates before FEA or printing.

E-050’s joint timing/cost extension admits a conditional 240-head central-motion comparator, but only $1.0417 per complete channel at a $250 shared reserve and $500 cap before cell purchases. The next gate is complete-channel costing and bank-load-dependent motion, ahead of further pawl refinement. Increasing head count is not a demonstrated system rescue.

E-059 rejects the sourced FS0307/FS90 servo-per-head procurement route:
80 positioning actuators alone cost $748/$632 at observed public prices,
above the entire $500 cap. This excludes these priced embodiments, not all
independent drives. Stop their layout work; reopen with a complete cheaper
channel or changed addressing/schedule. Shared-energy selection remains a
separate mechanism question with E-051's support-proof dwell gate.

E-115 retains a powered pivot-pawl section as a changed support alternative,
but its assumed gravity-return drag allowance is only 0.161–2.863 microN at the
tip. A compact toggle crossbolt retains only tight-bound section cases and no
demonstrated unloaded command retention. Keep the rectangular crossbolt as the
primary comparator for finite positive set/return coupling. Selection must
persist through ground reseat, support proof and selective carrier release;
direct ground=not-command coupling fails that sequence. These local results
do not reopen the rejected purchased servo route or establish a machine.
