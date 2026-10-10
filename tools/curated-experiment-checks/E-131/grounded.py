"""E-131: deterministic necessary bounds; mm, N, s. No process probabilities.

Run from any directory with Python 3. Output is disposable/reproducible.
The finite wedge is a rigid 2D prism extrusion, not a completed machine.
"""
import itertools
import json
import math


def wedge(t, mt, mb):
    """Horizontal push for raising / pull for lowering, per vertical newton.

    Upper block has a frictionless vertical guide. Wedge has a horizontal bed.
    Wedge weight is omitted: its bed friction would add to both forces.
    """
    return (t + mt) / (1 - mt * t) + mb, (mt - t) / (1 + mt * t) + mb


def vector_check(t, mu, raising):
    # Independent unit-vector force resolution for the upper contact.
    alpha = math.atan(t)
    normal = (math.sin(alpha), math.cos(alpha))
    tangent = (math.cos(alpha), -math.sin(alpha))
    sign = 1 if raising else -1
    n = 1 / (normal[1] + sign * mu * tangent[1])
    fx = n * (normal[0] + sign * mu * tangent[0])
    return fx + mu if raising else mu - fx


def move(distance, speed=300, accel=3000):
    return 2 * math.sqrt(distance / accel) if distance <= speed**2 / accel else distance / speed + speed / accel


def finite_wedge(intervals, slope=.08, bias=0):
    # Local prism u=[-530.4,1.4], y=[-1.5,1.5], z=[0,1+bias-slope*u].
    # Upper sliding shoe x=[-1.2,1.2], z underside=1+bias+slope*(q-x).
    # Its horizontal upper face is 2.5+bias+slope*q; a guided stem carries top.
    # q runs through full 40-mm reach, leaving excess ramp at the ends.
    lo, hi = -530.4, 1.4
    minimum_land = float('inf')
    minimum_thickness = float('inf')
    for i in range(intervals + 1):
        q = 40 / slope * i / intervals
        for x in (-1.2, 0, 1.2):
            u = x - q
            ramp_z = 1 + bias - slope * u
            shoe_z = 1 + bias + slope * (q - x)
            assert abs(ramp_z - shoe_z) < 1e-12
            minimum_land = min(minimum_land, u - lo, hi - u)
            minimum_thickness = min(minimum_thickness, 2.5 + bias + slope*q - shoe_z)
        # Same contacts when lowering; no release, input freeze or new ground latch.
        assert abs(slope*q - 40*i/intervals) < 1e-12
    assert minimum_land > 0 and minimum_thickness > 0
    assert 1 + bias - slope*hi > 0
    # A center-loaded shoe and bilateral input at z=.4 mm give this bed
    # center of pressure. Check unilateral bed moment support, not a free couple.
    for q, mt, mb, raising in itertools.product((0, 40/slope), (.05, .1, .3), (.05, .1, .3), (False, True)):
        direction = 1 if raising else -1
        fx = (slope + direction*mt)/(1 - direction*mt*slope)
        applied = fx + direction*mb
        cop = .4*applied - (1+bias+slope*q)*fx
        assert lo+q < cop < hi+q
        # Feasible input-absent force distribution, including bed moments.
        static_fx = max(0, (slope-mt)/(1+mt*slope))
        assert static_fx <= mb
        static_cop = -(1+bias+slope*q)*static_fx
        assert lo+q < static_cop < hi+q
    # Parallel y lanes remain separate for arbitrary q; neighboring top 4.8 wide.
    return dict(land_mm=minimum_land, shoe_thickness_mm=minimum_thickness,
                prism_gap_mm=5.08-3, guide_envelope_gap_mm=5.08-4,
                top_gap_mm=5.08-4.8)


def run():
    coefficients = (.05, .1, .3)
    cases = []
    for w, mt, mb, slope in itertools.product((1, 3.27, 10), coefficients, coefficients, (.0798, .08, .0802)):
        up, down = wedge(slope, mt, mb)
        assert up > 0 and down > 0
        cases.append((w*up, w*down))
    for t in (.04, .08, .3):
        for mu in (0, .05, .3):
            up, down = wedge(t, mu, mu)
            assert abs(up-vector_check(t, mu, True)) < 1e-12
            assert abs(down-vector_check(t, mu, False)) < 1e-12
            assert up >= t and down >= -t  # dissipation nonnegative both ways
        assert wedge(t, 0, 0) == (t, -t)
    for mu in coefficients:
        limit = 2*mu/(1-mu*mu)
        assert abs(wedge(limit, mu, mu)[1]) < 1e-12
    geometry = [finite_wedge(n, t, b) for n in (64, 256, 1024)
                for t in (.0798, .08, .0802) for b in (-.05, 0, .05)]
    # Affine geometry extrema occur at endpoints; refinement confirms, not proves CAD.
    for i, result in enumerate(geometry):
        assert all(abs(value-geometry[i % 9][key]) < 1e-12 for key, value in result.items())
    local_angles = [math.degrees(math.atan(.08))+a for a in (-1.5, 0, 1.5)]
    local_margins = [wedge(math.tan(math.radians(a)), .05, .05)[1] for a in local_angles]
    # A positive static margin is not a kinetic arrest guarantee.
    kinetic = wedge(.08, .02, .02)[1]
    assert kinetic < 0
    # Grounded wedge weight helps: this .04-kg prism still backdrives at W=1 N.
    assert kinetic + .02*.04*9.81 < 0
    # Same-layer inline replication intersects at q=0 for all 80 sites.
    common_overlap = 1.4 - (79*5.08 - 530.4)
    assert common_overlap > 0
    length = 531.8
    max_height = 1+.08*530.4
    volume_mm3 = 3*length*(1+.08*(530.4-1.4)/2)
    # Counterbalance minimax over load and multiplicative common spring error.
    balances = []
    for e in (0, .1, .2):
        c = (1+10)/2
        residual = max(abs(w-c*(1+b)) for w in (1, 10) for b in (-e, e))
        # Piecewise convex maximum; equal limiting errors establishes minimizer.
        assert abs(10-c*(1-e) - (c*(1+e)-1)) < 1e-12
        for other in (0, c-.001, c+.001, 10):
            assert max(abs(w-other*(1+b)) for w in (1, 10) for b in (-e, e)) >= residual-1e-12
        balances.append(dict(common_fraction=e, nominal_N=c, residual_N=residual))
    # Strict 30s bound with illustrative 6s global + 50ms per-site completion.
    schedules = []
    for name, distance in (('wedge', 500), ('direct', 40)):
        service = move(distance)+.05
        minimum_heads = next(h for h in range(1, 6401) if 6+math.ceil(6400/h)*service < 30)
        schedules.append(dict(name=name, service_s=service, min_heads=minimum_heads,
                              time_160_heads_s=6+40*service,
                              max_USD_per_head_at_250_residual=250/minimum_heads))
    # Square-thread scalar control; favorable absence of collar/guide friction.
    screws = []
    for diameter in (3, 12):
        max_lead = math.pi*diameter*.05  # zero margin, upper limit only
        screws.append(dict(diameter_mm=diameter, max_lead_mm=max_lead,
                           min_turns=40/max_lead, rpm_lower_bound_160_heads=60*40/max_lead/.55))
    up, down = wedge(.08, .05, .05)
    return dict(scenarios=len(cases), force_ranges_N=dict(raise_=[min(x[0] for x in cases), max(x[0] for x in cases)],
                lower=[min(x[1] for x in cases), max(x[1] for x in cases)]),
                witness=dict(up_per_N=up, down_per_N=down, raising_work_ratio=up/.08),
                geometry=geometry[4], common_inline_overlap_mm=common_overlap,
                prism_volume_board_L=6400*volume_mm3/1e6,
                separate_layer_depth_mm=80*max_height,
                local_angles_deg=local_angles, local_hold_margin_per_N=local_margins,
                kinetic_pull_per_N=kinetic,
                travel_limits_mm={str(mu):40/(2*mu/(1-mu*mu)) for mu in (.02,.05,.1,.3)},
                counterbalance=balances, schedules=schedules, screw_control=screws,
                repeated_cost_USD_per_cell={str(cap):(cap-250)/6400 for cap in (400,500)},
                direct_drag_N=[2*100*.8*mu for mu in (.02,.05,.1)],
                counterweight_mass_board_kg=6400*5.5/9.81)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
