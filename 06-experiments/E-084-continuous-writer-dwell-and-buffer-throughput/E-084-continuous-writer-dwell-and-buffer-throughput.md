---
status: complete
builds-on: [E-083, E-082, ADR-014]
---

# Continuous command writing trades stopped rows for finite contact dwell

**Retain continuous shared-cam transport for geometry synthesis; reject the
assumption that a buffer repairs insufficient setter throughput.** An optimistic
single-bank writer at the E-083 adverse workload boundary travels at 0.7281 m/s.
A 2-mm contact window lasts only 2.747 ms. A smooth 1.2-mm cycloidal dog stroke
then demands about **999 m/s² peak follower acceleration**. Four banks reduce
that to 62.46 m/s² at 0.1820 m/s before turns, transitions and sensing. These are
kinematic demands, not achieved motion or an accepted mechanism.

Input `16975d8`. Reproduce:
`python3 tools/curated-experiment-checks/E-084/continuous_writer.py`.
Initial deterministic analytical screen for ADR-014's successor opportunity;
no empirical priors, geometry acceptance, manufacturing yield or hardware
measurement. It introduces timing/contact bounds, not a completed architecture.

## Three coupling hypotheses to discriminate

1. **Continuously transported programmable cam fingers.** A travelling row head
   carries 80 data gates, and its translation supplies dog-switching energy
   through cam profiles. Local passive endpoint retention remains at 6,400 dogs,
   but long column bars and 6,400 captive sliding keys are removed. A gate must
   select set/reset/bypass before contact, remain fixed through contact, and
   withdraw without moving unchanged dogs. The first geometry task must implement
   those paths and bypass/reset; assigning a bit to a finger is insufficient.
2. **Independent interleaved finger lanes.** Q separately programmable 80-finger
   lanes visit alternating rows, increasing time available to reset each lane.
   This may shorten per-lane duty but repeats 80Q data drives per bank and needs
   actual staggered routing. Adjacent lanes must not touch the wrong row. It is
   a temporal-storage mutation of the first hypothesis, not a separate height
   support architecture.
3. **Stationary setter with circulating retained command carriers.** One 80-bit
   setter programs successive reusable carriers before their cam contact zone.
   This relocates data actuators and can decouple preparation latency from
   contact, but cannot improve sustained word production unless multiple setters
   or a materially faster setting mechanism are provided. Carrier return,
   overwrite, registration, readback and transport are real operations. A
   pre-encoded whole-map tape must count physical preparation inside update time.

All hypotheses use the existing shared elevator/pawl support concept only as a
comparison boundary; support transfer and retained output states remain gates.
No new height-support mechanism or qualified D&D regional behavior is claimed.

## Dwell, buffering and smooth-cam requirements

Use 3,440 row transactions, pitch p=5.08 mm, and a **24-s boundary allocation**
for writing/transport with 6 s reserved elsewhere. Split rows equally among B
independent banks. Grant zero turnaround/index time and uninterrupted scanning:
row period `Delta=24B/3440`; boundary velocity `v=p/Delta`. Actual strict <30-s
operation requires greater velocity or less other work, including all omitted
operations. Forty-three mask passes cannot teleport between endpoints or move
through an unverified global support handoff.

Let active contact width w be 1/2/4 mm and contact duration `tc=w/v`. For a
hypothetical programmable gate stroke 1.2 mm with triangular rest-to-rest
acceleration a=20/100 m/s², setting alone takes `tg=2 sqrt(0.0012/a)`.
Gate proof adds 0/1 ms as a sensitivity, not a qualified reader. A lane must
complete setting and proof outside its contact window. Independently actuated
Q-way interleaving requires `Q*Delta > tg+proof+tc`. This strict inequality
leaves no finite design margin when nearly equal. Q is a timing allowance;
no spatial arrangement or idle-lane release path is provided.

A **single shared setter per data column** must additionally satisfy
`tg+proof < Delta`, regardless of carrier buffer depth. At B=1, a=20 m/s²,
tg=15.492 ms: fewer than 1,550 words can be produced in 24 s against 3,440
required. An arbitrarily deep preloaded buffer may hide a visible transition,
but not sustained arbitrary-map preparation. This excludes only that setter
stroke/acceleration model; a shorter gate, continuous setting cam or multiple
setters changes the bound and must be synthesized explicitly.

For a smooth cycloid `x(u)=d*(u−sin(2*pi*u)/(2*pi))`, u=t/tc and d=1.2 mm,
endpoint velocity/acceleration vanish. Peak acceleration is `2*pi*d/tc²`;
peak slope against transport is `2d/w`. At w=2 mm it is 1.2, a substantial
cam/guide reaction challenge even when time passes. For a hypothetical constant
0.3-N dog resistance, ideal mean transport reaction through contact is
`0.3*d/w=0.18 N per selected dog` (14.4 N for 80 simultaneous dogs), excluding
inertia, friction and retention peaks. This work identity is not a force cap;
it does not establish contact continuity, separation or acceptable wear.

| B | Boundary v | Row period | Contact, w=2 mm | Independent lanes at a=20, zero proof | Data drives | Cycloid peak acceleration |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.7281 m/s | 6.977 ms | 2.747 ms | 3 | 240 | 999.36 m/s² |
| 2 | 0.3641 m/s | 13.953 ms | 5.493 ms | 2 | 320 | 249.84 m/s² |
| 4 | 0.1820 m/s | 27.907 ms | 10.987 ms | 1 | 320 | 62.46 m/s² |
| 8 | 0.0910 m/s | 55.814 ms | 21.974 ms | 1 | 640 | 15.62 m/s² |

At B=4 and 1-ms proof, only 0.428 ms remains between setting/proof/contact and
the allocated row period. Independent lanes relax the setting deadline but
leave the cam contact duration unchanged. Wider cams lower acceleration and
slope but leave less gate-reset time, and eventually touch adjacent cells.
The executable crosses all 48 B/width/acceleration/proof combinations. These
are necessary timing scenarios, not Pareto-qualified whole machines.

## Next discrimination and evidence limits

The changed coupling potentially replaces E-083's 1,280 independent bank data
drives with a few hundred gate drives and shared translation, while eliminating
per-intersection captive keys. It still repeats local dog retention and needs
real set/reset/bypass geometry, print/assembly burden, service access and an
actual affordable actuator. Its value must be decided by geometry and forces,
not by counting encoded words or ideal carrier buffers.

Next synthesize finite opposed cam tracks and positively withdrawn gates,
checking contact through set/reset/unchanged transitions, lane-to-row registration,
unknown initial state and a stuck gate. Then incorporate finite acceleration,
turnarounds, global-cam barriers, sparse/local updates, readback and bounded retry.
Stop a topology when no contact/isolation path fits its timing and force bounds;
no printing or another arbitrary damping sweep follows this initial screen.

Self-review: cycloid displacement reconstructed by trapezoid integration at
100/200/400 intervals agrees to <1e-14 m; doubling banks doubles period and
quarters peak acceleration; an intentionally overloaded shared setter fails.
The sampling confirms a smooth closed-form identity, not contact dynamics or
manufacturing reliability. The assumed 1.2-mm gate stroke may be reduced only
by an actual alternative geometry; model constants are not process data.
