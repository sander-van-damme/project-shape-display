#!/usr/bin/env python3
"""Reproduce the E-018/DES-003 drawing-level compatibility arithmetic."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Timing:
    inherited_cycle_s: float = 20.18
    analytical_bound_s: float = 30.0
    full_readback_bits: int = 4 * 25
    fiducials: int = 2
    retries: int = 1

    @property
    def margin_s(self) -> float:
        return self.analytical_bound_s - self.inherited_cycle_s


def main() -> None:
    plane_stack = 4 * 0.80 + 3 * 1.20
    nominal_standoff_delta = 2.00 - 1.80
    actuator_current = 5.0 / 6.0
    actuator_power = 5.0 * actuator_current
    timing = Timing()

    print(f"plane_stack_mm={plane_stack:.2f}")
    print(f"nominal_standoff_delta_mm={nominal_standoff_delta:.2f}")
    print(f"actuator_nominal_current_A={actuator_current:.3f}")
    print(f"actuator_nominal_power_W={actuator_power:.3f}")
    print(f"four_actuator_steady_current_A={4 * actuator_current:.3f}")
    print(f"four_actuator_steady_power_W={4 * actuator_power:.3f}")
    print(f"complete_readback_bits={timing.full_readback_bits}")
    print(f"fiducial_reads={timing.fiducials}")
    print(f"bounded_retries={timing.retries}")
    print(f"inherited_cycle_s={timing.inherited_cycle_s:.2f}")
    print(f"analytical_margin_s={timing.margin_s:.2f}")
    print("physical_validation=False")


if __name__ == "__main__":
    main()
