---
status: active
builds-on: [E-017, E-022, E-023, A-010, A-011, ADR-005, ADR-006, DES-004, DES-005, E-028, E-029, E-030]
---

# E-031: E-017 boundary reconciliation — A-010 versus A-011

## Decision-ready disposition

**Keep A-011 as the current architecture boundary; hold A-010 as its
mechanical implementation candidate.** A-011 is the stronger answer to the
arbitrary-map product question because it explicitly includes reusable
four-plane media, four parallel writer channels, registration/clamping,
per-cell verification, retry, and service media. A-010 is not a competing
complete boundary: it is one axle-free, laminated cartridge implementation of
that boundary. It may become the preferred mechanism only if its cartridge
coupon closes the load-separation, registration, regional-isolation, and
timing gates without adding a costly purchased guide or reader path.

This is an analytical disposition. No reader compatibility, media life,
durability, fabrication success, or hardware performance is claimed.

## Evidence basis and boundary correction

- **Sourced catalogue observations:** E-022/E-023 record public prices and
  availability observations for controller, driver, sensor/harness examples,
  stainless media/process, and actuator candidates. They are not quotes or
  fit evidence. E-023 leaves the exact medium, actuator, and inherited-reader
  overlay unresolved.
- **Allowances/calculations:** E-022 bounds the complete A-011 boundary at
  $486.29–$872.29 with compatible DES-003 readers, or $505.59–$921.59 with
  the explicitly alternative QRE1113/ADC/carrier fallback. The $370 DES-003
  baseline is shared-machine cost, not a complete mask-generator cost.
  E-017’s 20.18 s full-field and 0.72 s local 5x5 bounds require parallel
  writing and local registration; they are not measured performance.
- **CAD/tolerance-derived:** DES-004/DES-005 retain a candidate rotor with
  nominal 0.1046 mm vane/frame clearance, assumed 0.0546 mm worst case, and
  0.30 mm assumed worst-case axle/bore diametral clearance. These values do
  not establish process capability.
- **Unresolved physical/compatibility evidence:** E-023 leaves the eight
  DES-003 reader heads’ XY/Z/optical/cabling/timing compatibility open.
  E-029/E-030 reject or block E-028 as a fabrication-ready physical gate:
  stop/detent and load paths are not frozen in the coupon CAD, reader and
  writer margins are not operationally defined, loaded-neighbour evidence is
  incomplete, and no physical run exists.

Therefore E-028–E-030 cannot be used to select DES-004’s rotor over A-010,
nor to reject A-010 based on rotor-specific failures. They do establish that
the current rotor/readback evidence is not a closed mechanism gate.

## Compact comparison

| Criterion | A-010: laminated translating cartridge | A-011: buffered reusable boundary |
|---|---|---|
| Cost boundary | Printed per-cell gates may remove the DES-004 axle allowance, but guides, laminations, cartridge reinforcement, service media, and writer/lift interfaces are not closed. Apparent savings are a lower bound. | Complete conditional range is $486–$872 with reader reuse or $506–$922 with the alternative reader stack; excludes printed parts and unquoted fit/life risk. |
| Update mechanism | Change one indexed planar gate after unloading its post; hard stops define five states. O(changed cells) in principle. | Four-plane parallel write to a locally clamped reusable tile; O(changed cells) in principle, with bounded retry and readback. |
| Reader/writer compatibility | Reader target and writer tongue/follower geometry remain implementation-specific; E-028’s unresolved reader-margin definition applies. | Same reader uncertainty, but the boundary explicitly requires a compatible reader or a separately designed fallback; serial writing is excluded by the E-017 timing calculation. |
| Regional update | Potentially strong: cartridge can be 5x5/serviceable, but post unload/re-seat and adjacent displacement are unmeasured. | Strong at boundary level: local clamp avoids global reset, but registration and loaded-neighbour isolation are still gates. |
| Serviceability | Replaceable laminated cartridge and explicit state/load separation are advantages; debris, detent wear, slider creep, skew, and layer/guide assembly are risks. | Replaceable media/service stock and fault quarantine are explicit; more parallel channels and fiducial/clamp parts increase calibration burden. |
| Manufacturability/compactness | No axle drilling/pressing; many thin layers, planar clearances, guide flatness, and cartridge seams increase assembly-yield risk and stack height. | Mechanism-agnostic boundary; local clamp is simpler than full transport, but the four-plane stack and reader overlay remain unmanufactured. |
| Current risk | High mechanism risk, potentially lower purchased cost; A-010’s own 1,000-change coupon gate is not run. | Lower architectural risk because it is the only complete boundary already costed, but high unresolved media, actuator, reader, and physical-gate risk. |

## Conditional recommendation and holds

Use **A-011 as the requirements and cost boundary** for the next engineering
task. Within it, keep **A-010 as the preferred axle-free mechanism to
falsify** only if eliminating 6,400 axle pins and separating load from state
is worth its added planar-stack risk. Do not call A-010 cheaper until a
dimensioned cartridge BOM and scrap/service assumption close the apparent
delta. Do not promote DES-004’s rotor from its current candidate status:
E-029/E-030 leave its physical gate blocked/rejected as a contract, despite
the repaired nominal CAD arithmetic.

Explicit holds/rejections:

1. Hold any procurement or production commitment: E-022/E-023 contain
   allowances and catalogue observations, not delivered quotes or fit/life
   evidence.
2. Reject prepared-mask libraries, cassette-only, buffered-only, and
   serialized-writing substitutes as complete arbitrary-map boundaries, per
   E-017/ADR-006. Buffering can be an accessory, not the generator.
3. Hold A-010 promotion until its gate can be shown to be unloaded by the
   follower load, reach all five states, preserve registration after reseat,
   and avoid adjacent disturbance. Hold A-011 promotion until the same
   physical gates plus reader compatibility and parallel-write yield are
   evidenced.

## Exact next gate: E-031-G1 common cartridge falsification

**Next owner/role:** Mask-generator mechanical/controls owner, with the
reader/verification owner supplying the fixed reader overlay.

The cheapest credible discriminator is one final-pitch 5x5 coupon, not a
full display or a new sourcing round. Build the smallest A-010 cartridge
that implements its two fiducials, guide laminations, five hard stops, one
writer tongue, representative follower/load shoulder, and fixed reader
target. Instrument the same coupon envelope for an A-011 four-plane
parallel-write comparison where practical; if a full four-plane stack cannot
fit the coupon, preserve its exact datum/reader geometry and test A-010 first.
No procurement is authorized by this gate.

Acceptance criteria (all are required; missing raw evidence is unresolved):

- five-state reach and return in both travel directions, with no binding or
  gate face carrying the follower load;
- post-reseat transformed aperture/fiducial residual <= 0.20 mm and measured
  two-axis writer clearance >= 0.20 mm;
- target-update peak and residual displacement of every named loaded or
  unloaded adjacent witness <= 0.10 mm;
- fixed-reader raw code/confidence and declared calibration/threshold for
  every state; no manual-only classification; reader margin definition
  frozen before the run;
- complete event chain (command, writer contact, settled stop, reader-valid,
  return-stable) with monotonic timestamps; A-011 retains the E-017 parallel
  write requirement and no serial recovery path;
- at least 1,000 adversarial state changes for the cheap mechanism screen,
  including alternating extremes, single-cell neighbour updates, and
  reseat intervals. This is a falsifier, not life qualification.

**Decision rule:** promote A-010 as the preferred A-011 implementation only
if every criterion passes and its purchased additions plus service/scrap
allowance do not erase the E-022 reuse-case advantage. Otherwise retain the
A-011 boundary and select a different implementation; one failed criterion
is not averaged away by low unit cost. A-011 itself remains conditional until
the four-plane yield, reader overlay, media wear, and clamp/isolation results
are available.

## Reproduction and evidence boundary

The result is reproducible from E-017, E-022, E-023, A-010, A-011,
ADR-005/006, DES-004/005, and E-028–E-030. Any future run must preserve raw
records, article/configuration IDs, applied load/force trace, reader
calibration, and measurement uncertainty. Analytical scripts and synthetic
contract fixtures cannot close the physical gates. This artifact makes no
hardware-performance claim.
