"""Full-scale architecture experiment. Python standard library only; mm, s, N, USD.

This is an event/geometry/force bound model, not a contact physics simulation.
Run: python experiments/test08_architecture_search/analysis.py
"""
from pathlib import Path
import csv
import copy
import hashlib
import json
import math
import random

HERE = Path(__file__).resolve().parent


def move_time(distance, speed, accel):
    """Symmetric rest-to-rest trapezoid, including acceleration and braking."""
    if distance < 0 or speed <= 0 or accel <= 0:
        raise ValueError("Invalid motion inputs")
    if distance <= speed * speed / accel:
        return 2 * math.sqrt(distance / accel)
    return distance / speed + speed / accel


def validate(p):
    g, t, c, m = (p[k] for k in ("grid", "terrain", "cam", "motion"))
    if min(g["rows"], g["columns"], m["head_channels"]) < 1:
        raise ValueError("Empty grid/head")
    if t["levels"] < 2 or t["travel_mm"] <= 0:
        raise ValueError("Invalid travel/levels")
    if g["body_width_mm"] >= g["pitch_mm"]:
        raise ValueError("Columns overlap")
    if abs(360 / t["levels"] / m["step_angle_deg"] - round(360 / t["levels"] / m["step_angle_deg"])) > 1e-9:
        raise ValueError("Cam levels must align with motor full steps")
    if m["home_steps"] * m["step_angle_deg"] < 360:
        raise ValueError("Homing sweep does not cover unknown phase")
    if c["body_bottom_mm"] - c["follower_length_mm"] != c["base_mm"]:
        raise ValueError("Follower and cam datum mismatch")
    if c['follower_guide_top_mm'] < c['body_bottom_mm']+t['travel_mm']:
        raise ValueError('Follower loses guidance at full extension')
    if c['body_relief_height_mm'] <= c['follower_guide_top_mm']-c['body_bottom_mm']:
        raise ValueError('Body relief does not clear fixed follower guide')
    if g['body_length_mm']-c['body_relief_height_mm'] < t['travel_mm']:
        raise ValueError('Relieved body becomes exposed beside a low neighbor')


def patterns(p):
    r, c = p["grid"]["rows"], p["grid"]["columns"]
    k = p["terrain"]["levels"] - 1
    rng = random.Random(20260927)
    return {
        "all_low": [[0] * c for _ in range(r)],
        "all_high": [[k] * c for _ in range(r)],
        "checkerboard": [[k * ((x+y) % 2) for x in range(c)] for y in range(r)],
        "alternating_rows": [[k * (y % 2)] * c for y in range(r)],
        "stairs": [[min(k, x * (k+1)//c) for x in range(c)] for _ in range(r)],
        "random_seed_20260927": [[rng.randrange(k+1) for _ in range(c)] for _ in range(r)]}


def schedule(p, targets, channels=None, step_rate=None, coupled_override=None):
    """Every cell homed and rewritten; even a zero target is visited.

    Start/end head parked at the same origin. Arbitrary OLD map is lifted clear.
    No overlapping operations credited. Groups use serpentine row traversal.
    """
    g, t, m = p["grid"], p["terrain"], p["motion"]
    channels = channels or m["head_channels"]
    rate = step_rate or m["step_rate_hz"]
    if len(targets) != g["rows"] or any(len(row) != g["columns"] for row in targets):
        raise ValueError("Target shape mismatch")
    if any(not isinstance(v, int) or not 0 <= v < t["levels"] for row in targets for v in row):
        raise ValueError("Invalid target level")
    elapsed, events = 0., []
    def add(kind, duration, **kw):
        nonlocal elapsed
        events.append(dict(kind=kind, start_s=elapsed, duration_s=duration, **kw))
        elapsed += duration
    add("axis_reference", m["axis_reference_s"])
    lift = move_time(t["travel_mm"] + m["unload_clearance_mm"], m["lift_speed_mm_s"], m["lift_accel_mm_s2"])
    add("lift_all_clear", lift)
    pos = (0., 0.)
    rows_written = 0
    for group, x0 in enumerate(range(0, g["columns"], channels)):
        order = range(g["rows"]) if group % 2 == 0 else reversed(range(g["rows"]))
        for row in order:
            next_pos = (x0 * g["pitch_mm"], row * g["pitch_mm"])
            add("head_index", move_time(math.dist(pos, next_pos), m["scan_speed_mm_s"], m["scan_accel_mm_s2"]))
            pos = next_pos
            values = targets[row][x0:x0+channels]
            add("communicate", m["communication_s"])
            couple = m["couple_each_s"] if coupled_override is None else coupled_override
            add("couple", couple)
            add("home_rotors_to_stop", m["home_steps"]/rate + m["step_settle_s"])
            steps = max(values) * 360 / t["levels"] / m["step_angle_deg"]
            add("write_rotors", steps/rate + m["step_settle_s"], row=row, first_column=x0, cells=len(values))
            add("uncouple", couple)
            add("detent_seat", m["detent_settle_s"])
            rows_written += 1
    add("park_head", move_time(math.dist(pos, (0, 0)), m["scan_speed_mm_s"], m["scan_accel_mm_s2"]))
    add("lower_platen", lift)
    add("ready_settle", m["ready_settle_s"])
    totals = {}
    for event in events:
        totals[event["kind"]] = totals.get(event["kind"], 0) + event["duration_s"]
    return dict(time_s=elapsed, below_30_s=elapsed < 30, row_groups=rows_written,
                cells_written=sum(e.get("cells", 0) for e in events), breakdown_s=totals, events=events)


def geometry(p):
    g, t, c, u = (p[k] for k in ("grid", "terrain", "cam", "uncertainty"))
    # Exact circular-envelope clearance to closest corner of the two guide lips.
    lip_clear = math.hypot(c["guide_inner_x_mm"]-c["center_x_mm"], c["guide_slot_half_width_mm"]) - c["radius_mm"]
    toe_angle = math.degrees(math.atan2(c["toe_width_mm"]/2, c["toe_x_mm"]-c["center_x_mm"]))
    angular_margin = 180/t["levels"] - toe_angle
    # Numerically integrate the actual planar toe/cam contact region, no centreline shortcut.
    dx = 0.002
    area = 0
    for i in range(math.ceil((c["center_x_mm"]+c["radius_mm"]-c["toe_x_mm"])/dx)):
        x = c["toe_x_mm"] + (i+.5)*dx
        half_y = min(c["toe_width_mm"]/2, math.sqrt(max(0, c["radius_mm"]**2-(x-c["center_x_mm"])**2)))
        area += 2*half_y*dx
    # Kinematic acceptance of all height pairs and raised rotation sweep.
    supported = []
    for old in range(t["levels"]):
        for new in range(t["levels"]):
            clear_z = c["base_mm"] + t["travel_mm"] + p["motion"]["unload_clearance_mm"]
            highest = c["base_mm"] + t["travel_mm"]
            assert clear_z > highest
            supported.append(dict(old=old, new=new, rotation_clearance_mm=clear_z-highest,
                                  final_height_mm=new*t["travel_mm"]/(t["levels"]-1)))
    gap = g["pitch_mm"]-g["body_width_mm"]
    volume = g["body_width_mm"]**2*g["body_length_mm"]
    if g["body_hollow"]:
        volume -= (g["body_width_mm"]-2*g["body_wall_mm"])**2*(g["body_length_mm"]-g["body_floor_mm"]-g["body_roof_mm"])
    # Relief removes the guide envelope from the lower body. Its narrow bridge
    # crosses the guide's open slot and still transmits load to the guided stem.
    relief_volume=(g['body_width_mm']/2-c['body_relief_x_mm'])*2*c['body_relief_half_width_mm']*c['body_relief_height_mm']
    if g['body_hollow']:
        overlap_x=max(0,g['body_width_mm']/2-g['body_wall_mm']-c['body_relief_x_mm'])
        overlap_y=min(2*c['body_relief_half_width_mm'],g['body_width_mm']-2*g['body_wall_mm'])
        overlap_z=max(0,min(c['body_relief_height_mm'],g['body_length_mm']-g['body_roof_mm'])-g['body_floor_mm'])
        relief_volume-=overlap_x*overlap_y*overlap_z
    volume-=relief_volume
    volume+=(c['stem_x_mm']+c['stem_thickness_mm']-c['body_relief_x_mm'])*c['bridge_width_mm']*c['bridge_thickness_mm']
    volume += c["stem_thickness_mm"]*c["stem_width_mm"]*c["follower_length_mm"]
    volume += (c["stem_x_mm"]-c["toe_x_mm"])*c["toe_width_mm"]*c["toe_thickness_mm"]
    return dict(active_width_mm=g["columns"]*g["pitch_mm"], active_depth_mm=g["rows"]*g["pitch_mm"],
        column_solid_volume_mm3=volume, column_mass_g=volume*p["loads"]["density_g_cm3"]/1000,
        top_gap_mm=gap, top_area_fraction=(g["body_width_mm"]/g["pitch_mm"])**2,
        loaded_worst_top_gap_mm=gap-u["body_width_plus_mm"]-u["local_pitch_minus_mm"]-2*u["lateral_top_deflection_each_mm"],
        cam_to_guide_lip_clearance_mm=lip_clear, toe_contact_area_mm2=area,
        toe_to_full_height_core_clearance_mm=c['toe_x_mm']-c['center_x_mm']-c['core_radius_mm'],
        nominal_angle_margin_deg=angular_margin, remaining_angle_margin_deg=angular_margin-u["cam_angle_error_deg"],
        guide_slot_to_toe_clearance_each_mm=c["guide_slot_half_width_mm"]-c["toe_width_mm"]/2,
        guide_slot_to_bridge_clearance_each_mm=c['guide_slot_half_width_mm']-c['bridge_width_mm']/2,
        guide_top_at_max_body_bottom_mm=c['follower_guide_top_mm']-(c['body_bottom_mm']+t['travel_mm']),
        unrelieved_upper_body_length_mm=g['body_length_mm']-c['body_relief_height_mm'],
        minimum_body_guide_web_mm=g["pitch_mm"]-g["body_width_mm"]-2*g["body_guide_clearance_mm"],
        transition_cases=supported,
        limitations=["Only named analytic envelopes checked; not complete assembly collision certification",
                     "Body-guide walls are only 0.2 mm: fine-nozzle/resin coupon required; ordinary 0.4 mm nozzle assumption fails",
                     "CAD coupon deliberately omits an unvalidated finished head and full platen structure"])


def forces(p, geo):
    l, c, g = p["loads"], p["cam"], p["grid"]
    n = g["rows"]*g["columns"]
    mass_g = geo["column_mass_g"]
    weight = mass_g/1000 * 9.81
    inertia = c["stem_width_mm"] * c["stem_thickness_mm"]**3 / 12
    unsupported = math.pi**2*l["elastic_modulus_mpa"]*inertia/(2*c["follower_length_mm"])**2
    guided = math.pi**2*l["elastic_modulus_mpa"]*inertia/(2*5)**2
    lift_force = (n*mass_g/1000+l["platen_mass_kg"])*(9.81+p["motion"]["lift_accel_mm_s2"]/1000)+n*l["guide_drag_n"]
    detent_i = c["detent_width_mm"]*c["detent_thickness_mm"]**3/12
    spring_force = 3*l["elastic_modulus_mpa"]*detent_i*c["detent_deflection_mm"]/c["detent_length_mm"]**3
    return dict(column_weight_n=weight, gravity_return_drag_limit_n=weight,
        assumed_gravity_margin_n=weight-l["guide_drag_n"], unbraced_follower_euler_n=unsupported,
        five_mm_effective_span_euler_n=guided,
        bearing_stress_at_1n_mpa=1/geo["toe_contact_area_mm2"],
        bearing_stress_at_5n_mpa=5/geo["toe_contact_area_mm2"],
        toe_root_bending_at_1n_mpa=6*(c["stem_x_mm"]-c["toe_x_mm"])/(c["toe_width_mm"]*c["toe_thickness_mm"]**2),
        lift_peak_n=lift_force,
        lift_screw_total_torque_nm=lift_force*l["screw_lead_mm"]/1000/(2*math.pi*l["screw_efficiency"]),
        lift_mechanical_peak_w=lift_force*p["motion"]["lift_speed_mm_s"]/1000,
        head_motor_electrical_peak_w=p["motion"]["head_channels"]*2*l["motor_voltage_v"]**2/l["phase_resistance_ohm"],
        system_peak_allowance_w=max(p["motion"]["head_channels"]*2*l["motor_voltage_v"]**2/l["phase_resistance_ohm"]+l['lift_hold_electrical_allowance_w'],l["lift_electrical_allowance_w"])+l["actuator_loss_allowance_w"],
        detent_leaf_force_n=spring_force,
        detent_leaf_surface_strain=1.5*c["detent_thickness_mm"]*c["detent_deflection_mm"]/c["detent_length_mm"]**2,
        qualification="Euler values are screening bounds; printed properties, guide stiffness, friction and creep are unmeasured")


def costs():
    with (HERE/"bom.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    totals = {band: sum(float(r["quantity"])*float(r[f"unit_{band}_usd"]) for r in rows) for band in ("low", "working", "high")}
    totals["working_plus_20_percent_usd"] = totals["working"]*1.2
    non_motor = totals["working"]-80*1.25
    totals["max_motor_price_for_500_with_20_percent_usd"] = (500/1.2-non_motor)/80
    totals["max_motor_price_for_400_with_20_percent_usd"] = (400/1.2-non_motor)/80
    totals["sourced_FS90_80_servos_only_usd"] = 80*7.90
    totals["status"] = "Allowances, NOT procurement-ready quotes. Tax/freight exposure is represented only by contingency."
    return totals


def main():
    p = json.loads((HERE/"params.json").read_text())
    validate(p)
    out = HERE/"results"
    out.mkdir(exist_ok=True)
    maps = patterns(p)
    cases = {name: schedule(p, target) for name, target in maps.items()}
    (out/"worst_schedule.json").write_text(json.dumps(cases["all_high"], indent=2)+"\n")
    geo = geometry(p)
    mass_variants = {}
    for hollow in [0,1]:
        variant=copy.deepcopy(p); variant['grid']['body_hollow']=hollow
        gv=geometry(variant)
        mass_variants['hollow' if hollow else 'solid'] = dict(mass_g=gv['column_mass_g'], forces=forces(variant,gv))
    metric = dict(configuration_sha256=hashlib.sha256((HERE/"params.json").read_bytes()).hexdigest(),
        timing={name: {k:v for k,v in value.items() if k != "events"} for name,value in cases.items()},
        geometry=geo, forces=forces(p,geo), mass_variants=mass_variants, bom=costs(),
        reliability={str(q): {"probability_perfect_map": (1-q)**6400, "expected_bad_cells":6400*q}
                     for q in p["uncertainty"]["per_cell_failure_probabilities"]},
        required_cell_failure_probability_for_99_percent_perfect_maps=1-.99**(1/6400),
        zero_failures_trials_for_95_percent_upper_bound=math.ceil(math.log(.05)/math.log(.99**(1/6400))),
        conclusion="NO PRODUCT PASS: timing is conditional; surface guidance, friction, retention, coupling, sourcing and miniature measurement remain open")
    (out/"metrics.json").write_text(json.dumps(metric, indent=2)+"\n")
    with (out/"timing_sweep.csv").open("w", newline="") as stream:
        writer=csv.writer(stream); writer.writerow(["channels","step_rate_hz","couple_each_s","time_s","under_30"])
        for channels in [16,20,40,80]:
            for rate in [100,200,400,800]:
                for couple in [.025,.05,.1]:
                    run=schedule(p,maps["all_high"],channels,rate,couple)
                    writer.writerow([channels,rate,couple,run["time_s"],run["below_30_s"]])
    # Dependency-free reproducible plot of full-map schedule.
    colors=["#6699cc","#b97a57","#47a385","#b57cd1","#c2a74b"]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1050" height="430" viewBox="0 0 1050 430">',
         '<rect width="1050" height="430" fill="#ffffff"/>',
         '<text x="20" y="30" font-family="sans-serif" font-size="20">Full 80 x 80 update: conditional event timing, including row homing</text>']
    for i,(name,run) in enumerate(cases.items()):
        y=65+i*48; x=205; width=run["time_s"]*22
        svg += [f'<text x="20" y="{y+18}" font-family="sans-serif" font-size="13">{name}</text>',
                f'<rect x="{x}" y="{y}" width="{width}" height="27" fill="{colors[i%5]}"/>',
                f'<text x="{x+width+8}" y="{y+18}" font-family="sans-serif" font-size="14">{run["time_s"]:.2f} s</text>']
    svg += ['<path d="M865 50 V360" stroke="#b42d39" stroke-dasharray="5 4"/>',
            '<text x="865" y="385" text-anchor="middle" font-family="sans-serif">30 s limit</text>',
            '<text x="20" y="414" font-family="sans-serif" font-size="13">No measured actuator qualification. Jam recovery and manual miniature handling are not bounded.</text>','</svg>']
    (out/"timing.svg").write_text("\n".join(svg))
    # SCAD gets the exact same dimensions; this generated include is never hand edited.
    (out/"parameters.scad").write_text("\n".join(f"{key} = {json.dumps(value)};" for group in [p["grid"],p["terrain"],p["cam"]] for key,value in group.items() if isinstance(value,(int,float)) and not isinstance(value,bool))+"\n")
    print(json.dumps({"timing_s":{k:v["time_s"] for k,v in cases.items()},"geometry":{k:v for k,v in geo.items() if k not in ["transition_cases","limitations"]},"forces":metric["forces"],"bom":metric["bom"],"conclusion":metric["conclusion"]},indent=2))


if __name__ == "__main__":
    main()
