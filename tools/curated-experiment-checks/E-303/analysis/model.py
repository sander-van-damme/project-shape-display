"""E-303 analytical screening models. SI internally; no measured clutch data.

Pressure calculations are different virtual-displacement models, not guarantees
of real contact area. Magnetic saturation is a screening limit, not a B-H solve.
"""
from math import pi, cos, tan, atan, hypot, floor, exp, sqrt

MU0 = 4e-7 * pi
EPS0 = 8.8541878128e-12
RHO_CU = 1.724e-8  # ohm m, nominal 20 degC
G0 = 9.80665


def annulus(outer_m, inner_m=0):
    """Area m², uniform-pressure effective radius m, uniform-wear radius m."""
    if not 0 <= inner_m < outer_m:
        raise ValueError("Require 0 <= inner radius < outer radius")
    area = pi * (outer_m**2 - inner_m**2)
    rp = 2 / 3 * (outer_m**3 - inner_m**3) / (outer_m**2 - inner_m**2)
    return area, rp, (outer_m + inner_m) / 2


def friction_torque(normal_n, mu, radius_m, surfaces=1):
    if min(normal_n, mu, radius_m) < 0 or surfaces < 1:
        raise ValueError("Invalid friction inputs")
    return surfaces * mu * normal_n * radius_m


def efficiency_torque(load_n, lead_m, efficiency):
    if load_n < 0 or lead_m <= 0 or not 0 < efficiency <= 1:
        raise ValueError("Invalid efficiency model inputs")
    return load_n * lead_m / (2 * pi * efficiency)


def thread_torque(load_n, lead_m, mean_d_m, mu, half_angle_rad=pi / 4,
                  direction="raise"):
    """V-thread approximation; lower returns applied torque in lowering direction.

    Negative lowering torque means an ideal gravity load overhauls the screw and
    needs braking. This omits collars, guides, thread distortion and eccentricity.
    """
    if load_n < 0 or min(lead_m, mean_d_m) <= 0 or mu < 0:
        raise ValueError("Invalid screw inputs")
    slope = lead_m / (pi * mean_d_m)
    mup = mu / cos(half_angle_rad)
    if direction == "raise":
        if 1 - mup * slope <= 0:
            raise ValueError("Wedge singularity: model outside applicable range")
        ratio = (slope + mup) / (1 - mup * slope)
    elif direction == "lower":
        ratio = (mup - slope) / (1 + mup * slope)
    else:
        raise ValueError("Direction must be raise or lower")
    return load_n * mean_d_m / 2 * ratio


def screw_scenario(weight_n, guide_n, mu_thread, parasitic_nm,
                   lead_m=.003, mean_d_m=.0023, mu_thrust=.10,
                   thrust_radius_m=.0012):
    """Separate guide axial opposition from a conservative lumped parasitic torque.

    Lowering net axial load reverses if guide resistance exceeds gravity. Thrust
    friction uses the resulting axial force, not clutch attraction. Real distributed
    thread contact and plastic distortion remain unmodeled.
    """
    up_force = weight_n + guide_n
    down_net = weight_n - guide_n
    raise_t = thread_torque(up_force, lead_m, mean_d_m, mu_thread)
    if down_net >= 0:
        lower_t = thread_torque(down_net, lead_m, mean_d_m, mu_thread,
                                direction="lower")
    else:
        lower_t = thread_torque(-down_net, lead_m, mean_d_m, mu_thread)
    raise_t += mu_thrust * up_force * thrust_radius_m + parasitic_nm
    lower_t += mu_thrust * abs(down_net) * thrust_radius_m + parasitic_nm
    return raise_t, lower_t


def magnetic_circuit(ampere_turns, gap_sections, steel_sections,
                     core_limit_t=1.2, bottleneck_m2=None):
    """Sections are (length_m, area_m2) for gaps; (length,area,mu_r) for steel.

    One series flux, no fringing or leakage. All gaps contribute closing force only
    if they act on the intended armature; do not count fixed yoke joins as armature
    attraction. Linear prediction above chosen core limit is flagged invalid. The
    limited force is a screening ceiling at that core limit, NOT a saturation solve.
    """
    if ampere_turns < 0 or not gap_sections or not steel_sections:
        raise ValueError("Need nonnegative excitation and a complete circuit")
    reluctance = sum(g / (MU0 * a) for g, a in gap_sections)
    reluctance += sum(l / (MU0 * a * mr) for l, a, mr in steel_sections)
    if reluctance <= 0:
        raise ValueError("Invalid reluctance")
    phi = ampere_turns / reluctance
    amin = min(a for _, a, _ in steel_sections)
    if bottleneck_m2 is not None:
        amin = min(amin, bottleneck_m2)
    phimax = core_limit_t * amin
    screened_phi = min(phi, phimax)
    linear_force = sum(phi**2 / (2 * MU0 * a) for _, a in gap_sections)
    screened_force = sum(screened_phi**2 / (2 * MU0 * a)
                         for _, a in gap_sections)
    return dict(reluctance_a_per_wb=reluctance, flux_wb=phi,
                gap_flux_t=[phi / a for _, a in gap_sections],
                linear_force_n=linear_force, screen_force_n=screened_force,
                core_flux_t=phi / amin, below_core_limit=phi <= phimax,
                ampere_turns_at_core_limit=phimax * reluctance)


def winding(inner_m, outer_m, height_m, copper_d_m=.00008,
            insulated_d_m=.00009, fill=.55):
    """Circular-turn bobbin envelope, not a complete magnetic clutch layout.

    fill is insulated-wire occupied area/window area. Leads and bobbin margins
    excluded; electrical dimensions are approximate. Copper temperature coefficient
    is applied separately by the caller when needed.
    """
    if not 0 < inner_m < outer_m or height_m <= 0 or not 0 < fill <= .9:
        raise ValueError("Invalid winding envelope")
    window = (outer_m - inner_m) / 2 * height_m
    turns = floor(fill * window / (pi * insulated_d_m**2 / 4))
    wire_length = turns * pi * (inner_m + outer_m) / 2
    copper_area = pi * copper_d_m**2 / 4
    resistance = RHO_CU * wire_length / copper_area
    copper_mass = 8960 * wire_length * copper_area
    return dict(turns=turns, wire_length_m=wire_length,
                resistance_ohm=resistance, copper_mass_kg=copper_mass,
                copper_area_m2=copper_area)


def coil_operating_point(coil, ampere_turns, duty=1):
    current = ampere_turns / coil["turns"]
    power = current**2 * coil["resistance_ohm"]
    return dict(current_a=current, voltage_v=current * coil["resistance_ohm"],
                power_w=power, average_power_w=power * duty,
                current_density_a_per_mm2=current / coil["copper_area_m2"] / 1e6,
                initial_adiabatic_k_per_s=power / (coil["copper_mass_kg"] * 385))


def electrostatic(area_m2, radius_m, voltage_v, thickness_m, epsilon_r,
                  gap_m=0, mu=.3, split=False):
    """Uniform-gap parallel plate and two equal floating-electrode halves.

    thickness_m is TOTAL solid dielectric thickness in each local field path.
    For balanced equal halves, local voltage is V/2; terminal capacitance is
    one quarter of the otherwise identical conventional single-area capacitor.
    Gap-closing force differentiates capacitance w.r.t. air-gap separation. Bulk
    dielectric stress is the alternate model for dielectric thickness compression.
    A conformal real contact need not realize either pressure as friction traction.
    """
    if min(area_m2, radius_m, thickness_m, epsilon_r) <= 0 or gap_m < 0:
        raise ValueError("Invalid electrostatic geometry")
    effective_gap = gap_m + thickness_m / epsilon_r
    local_v = voltage_v / 2 if split else voltage_v
    p_gap = .5 * EPS0 * (local_v / effective_gap)**2
    e_dielectric = local_v / (thickness_m + epsilon_r * gap_m)
    p_bulk = .5 * EPS0 * epsilon_r * e_dielectric**2
    full_c = EPS0 * area_m2 / effective_gap
    terminal_c = full_c / 4 if split else full_c
    return dict(gap_pressure_pa=p_gap, bulk_pressure_pa=p_bulk,
                normal_gap_n=p_gap * area_m2,
                torque_gap_nm=mu * p_gap * area_m2 * radius_m,
                torque_bulk_nm=mu * p_bulk * area_m2 * radius_m,
                capacitance_f=terminal_c,
                stored_energy_j=.5 * terminal_c * voltage_v**2,
                resistive_cycle_energy_j=terminal_c * voltage_v**2,
                dielectric_field_v_per_m=e_dielectric,
                air_field_v_per_m=local_v / effective_gap)


def floating_voltage(c1_f, c2_f, v1, v2, net_charge_c=0,
                     stray_c_f=0, stray_v=0):
    return (c1_f*v1 + c2_f*v2 + stray_c_f*stray_v + net_charge_c) / (
        c1_f+c2_f+stray_c_f)


def electrical_power(count, unit_power_w):
    return count * unit_power_w


def slip_heat(torque_nm, relative_rpm):
    return abs(torque_nm * relative_rpm * 2 * pi / 60)


def retained_voltage(initial_v, time_s, resistance_ohm, capacitance_f):
    return initial_v * exp(-time_s / (resistance_ohm * capacitance_f))


def nearest_same_tier(pitch_m, tiers):
    """Enumerate square lattice; tiers=2 checkerboard, tiers=4 2x2 coloring."""
    if tiers not in (1, 2, 4):
        raise ValueError("Supported tier counts: 1,2,4")
    same = lambda x, y: (tiers == 1 or
        (tiers == 2 and (x+y) % 2 == 0) or
        (tiers == 4 and x % 2 == 0 and y % 2 == 0))
    return min(hypot(x, y) * pitch_m for x in range(-4, 5)
               for y in range(-4, 5) if (x or y) and same(x, y))


def matrix_voltages(rows, cols):
    return tuple(tuple(r-c for c in cols) for r in rows)


def matrix_on(rows, cols, mode="unsigned"):
    vals = matrix_voltages(rows, cols)
    # Ideal 0/1-rail examples only: active threshold 0.5 normalized V.
    return tuple(tuple((abs(v) if mode == "unsigned" else max(v, 0)) > .5
                       for v in row) for row in vals)
