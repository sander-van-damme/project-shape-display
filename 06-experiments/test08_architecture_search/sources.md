# Evidence and sourcing ledger

Checked 2026-09-27. USD unless specified. These sources bound the search; none
qualifies the proposed assembly. Bulk allowances in `bom.csv` are deliberately
labelled unquoted. Printed parts and fabrication time are excluded from the
purchased-hardware total; purchased stock, electronics and fasteners are included.

| Source | Fact used | Limits |
|---|---|---|
| [Archived PM08-2 datasheet](../test00_pneumatic_multiplexer/docs/micro-stepper-datasheet.pdf) | 18° step, 3.3 V, 40 Ω, 8 mm body, 5 gf·cm = 0.490 mN·m pull-in torque; >800 pps no-load response | No loaded torque/speed curve; surplus identification and price unresolved; not a verified production supply |
| [FEETECH FS90 manufacturer datasheet hosted by Pololu](https://www.pololu.com/file/0J1435/FS90-specs.pdf) | 0.12 s/60° at 4.8 V, 0.10 at 6 V, 120° commanded range, 120 mA no-load and 800 mA stall at 6 V | No-load timing, not loaded positioning time; analog deadband and coupling error matter |
| [Pololu FS90 listing](https://www.pololu.com/product/2818) | $8.40 single / $7.90 at five | 80 × $7.90 = $632 before other hardware; no inferred cheaper 80-piece tier |
| [Tower Pro SG90](https://towerpro.com.tw/product/sg90-7/) | 23 × 12.2 × 29 mm, 0.1 s/60° at 4.8 V | Speed/dimensions reference, not a quote for unbranded clone performance |
| [Adafruit mini solenoid 2776](https://www.adafruit.com/product/2776) | $4.46 at 10–99; 5 V, 1.1 A, 3 mm throw | 80 selectors alone cost $356.80 and could draw 440 W; mechanical response not specified |
| [DFRobot FIT0708](https://www.dfrobot.com/product-2199.html) | 18° PM motor, 1500 pps minimum no-load auto-start specification; $11.90 at ten | Linear assembly, different motor: evidence for the motor class only, not a drop-in torque guarantee or qualifying BOM |
| [MOONS permanent-magnet motors](https://www.moonsindustries.com/c/permanent-magnet-stepper-motors-a0208) | 8 mm 18° motor listed at 0.4 mN·m holding torque / $40 | Industrial retail is far outside budget; holding torque is NOT running torque |
| [MIT inFORCE](https://tangible.media.mit.edu/project/inforce/) | Individually driven 10×5 closed-loop force display | Supports the direct-actuation family; does not establish low-cost 6400-cell feasibility |
| [Reconfigurable discrete pin tooling research](https://research.sabanciuniv.edu/16383/1/Design_and_analysis_of_a_reconfigurable_discrete_pin_tooling_system_for_molding_of_three-dimensional_free-form_objects.pdf) | Research precedent for passive self-locking pin tooling | Not evidence that this project's density, price or update time is attained |

Engineering assumptions, not sourced measurements: 400 pulses/s loaded PM motor
operation; 25 ms engagement and 25 ms disengagement; 15 ms motor/detent settling;
250 mm/s carriage with 4000 mm/s² acceleration; 35 mm/s lift; 1.5 GPa effective
printed modulus; 1.24 g/cm³ solid polymer density; 5 mN guide drag. These must be
tested together. The sensitivity sweep includes slower motors and slower couplers.

No representative miniature has been physically measured in this investigation.
40 mm usable travel is a provisional design envelope, not a claim that the
authoritative miniature-height requirement has been verified.
