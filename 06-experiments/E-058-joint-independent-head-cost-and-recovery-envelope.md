---
status: complete
builds-on: [E-050, Q-012, A-013]
---

# Joint head-count, recovery and cost envelope

Input `dc19a58`; `python3 tools/curated-experiment-checks/E-058/joint_envelope.py`
couples the previously separate timing and budget screens. This is deterministic
system accounting within A-013, not a new mechanism or supplier BOM. It enumerates
1–80 complete rows of independent heads (80–6,400 channels), three inherited
motion scenarios and 0/1/8 additional full-station retries: 720 timing cases.
No probability or calibrated manufacturing prior is introduced. A retry repeats
motion, contact and read while remaining at the station; reacquisition after a
lost grip, fault diagnosis and re-indexing would add time. Persistent/common-mode
faults are outside successful-update timing, not cured by retry allowances.

For r rows of heads and k retries, retain the original allocation:
`T = overhead + ceil(80/r)*(cycle + index(r)) + k*cycle`, where cycle includes
worst unequal-state home→old→new→home motion, contact and read; index is the
larger of the inherited minimum and rest-to-rest travel of r row pitches.
This charges an index at every station, including the last, as E-050 does.
It is a conditional schedule allocation, **not a universal physical lower
bound**: exact last travel/return, banking geometry, simultaneous power, moving
bank mass and overhead may change it. Larger banks are granted the same
acceleration and reserve to expose their most favorable budget envelope;
that scaling is not established. Non-divisor banks need inactive heads at the
board edge. Their packaging and isolation are unimplemented.

Minimum timing-feasible head counts under this allocation:

| Motion scenario | Retries | Heads | Full map s | Channel ceiling at $500 total, $250 reserve, no cell purchases |
|---|---:|---:|---:|---:|
| Fast | 0 / 1 | 80 | 29.350 / 29.660 | $3.125 |
| Fast | 8 | 160 | 18.696 | $1.5625 |
| Central | 0 / 1 / 8 | 240 | 23.877 / 24.497 / 28.837 | $1.0417 |
| Slow | 0 / 1 | 640 | 28.280 / 29.720 | $0.3906 |
| Slow | 8 | 2,160 | 29.223 | $0.1157 |

Fast 80-head operation permits only two full-station retries before exceeding
30 s (29.970 s for two; 30.280 s for three). These counts are explicit fault
budgets, not predicted failure frequency or board reliability. Central timing
can be rescued algebraically by a third row of heads; E-050's 160-head failure
must not be generalized to all independent-head counts. The rescue tightens
rather than resolves the cost problem.

For complete-channel cost c, purchased-cell allocation p, shared reserve B and
ceiling C, `c <= (C-B-6400*p)/(80*r)`. All grip/position/release actuators,
drivers, links, sensing and connectors must be assigned exactly once between c
and B; printed returns have print/assembly burdens even when p=0. The script
reports C=$400/$500, B=$150/$250/$350 and p=$0/$0.02/$0.05 for each minimum.
These are competing budget scenarios, not quotes or manufacturing distributions.
At C=$500, B=$250, p=$0.02, the 80/160/240-head channel ceilings fall to
$1.525/$0.7625/$0.5083. At C=$400, the 240-head ceiling is $0.625 with
p=0, or $0.0917 with p=$0.02. At B=$250, p=$0.05 already exhausts the
$500 cap before buying any channel. More generally p must be below
$0.0390625 to leave any positive channel budget in that scenario.

Positive c and fixed B,p make the smallest timing-feasible bank the largest
per-channel allowance; the search does not assume time is monotone in r.
Larger banks can buy timing margin, but cannot rescue a channel that exceeds
that maximum without changing assumptions. Fixed row partitions also make
regional work alignment-dependent: a contiguous five-row update occupies two
or three stations with a three-row bank, rather than always ceil(5/3)=2.
The script checks every legal start row; column selection is still assumed
independent. No untouched-cell disturbance or regional hardware time is proven.

Self-review: reproduce both original 80/160-head timing cases in all scenarios;
verify the fast 80-head result using a separately written motion expression;
check retry increments and exact cost recomposition; independently enumerate
row sets for all 6,080 bank-size/start combinations. Finite enumeration, no seed,
mesh or convergence claim. Reproducible JSON remains untracked.

**Decision:** retain 80/160 heads only under fast motion, with the stated retry
scope; add 240 heads as a conditional central-motion comparator. Do not grow
head count as an uncosted cure or continue local pawl/FEA refinement first.
The next discriminating result is one complete realizable drive channel with
cost allocation and load-dependent motion, compared against these ceilings.
If none fits, switch addressing/energy-sharing principle instead of tuning
another tolerance. Reopen envelopes with changed reserve, cell purchases,
implemented schedule or sourced complete-channel costs. No geometry gate,
physical calibration or product selection is granted by this extension.
