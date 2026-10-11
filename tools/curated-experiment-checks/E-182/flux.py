"""E-182. Explicit SI reluctance/screw scenarios, not finite-element fields or yield.
Run with Python standard library; JSON output is disposable. No random sampling.
"""
import importlib.util
import itertools
import json
import math
from pathlib import Path

MU0 = 4e-7 * math.pi
AREA = 8e-6
A = .0002                 # angular equivalent-gap amplitude, not manufactured teeth
G = .0004                 # .2-mm working + two .1-mm seated router gaps
RADIUS, LEAD = .0015, .00015


def gap(delta, base=G, amplitude=A):
    return base + amplitude * (1 - math.cos(2 * delta))


def torque(delta, mmf, base=G, amplitude=A, area=AREA):
    # delta = field angle - rotor angle; torque positive reduces positive delta.
    return MU0 * area * mmf**2 * amplitude * math.sin(2 * delta) / gap(delta, base, amplitude)**2


def peak(mmf=1., base=G, amplitude=A, area=AREA):
    if amplitude == 0:
        return 0., 0.
    b = base + amplitude
    y = 4 * amplitude / (b + math.sqrt(b*b + 8*amplitude*amplitude))
    angle = .5 * math.acos(y)
    return torque(angle, mmf, base, amplitude, area), angle


def thread(W, mu, direction, radius=RADIUS, lead=LEAD):
    slope = lead/(2*math.pi*radius)
    return W*radius*(mu + direction*slope)/(1-direction*mu*slope)


def required_gap_addition(drive, hold, e=0.):
    # Adversarial mixed-cell geometry: three selected gaps +e each, neighbor -e.
    # An additional -e shutter-stroke error is included. A and AREA remain fixed.
    if hold <= 0:
        return None
    selected = peak(base=G+3*e)[0]
    def margin(stroke):
        return selected / peak(base=G-3*e+stroke-e)[0] - drive/hold
    lo, hi = e, .001
    while margin(hi) < 0:
        hi *= 2
    for _ in range(70):
        mid = (lo+hi)/2
        if margin(mid) > 0: hi = mid
        else: lo = mid
    return hi


def fanout(selected_columns, stroke, base=G, area=AREA, bcap=1.2):
    # Complete bipartite gate mask, one selected row, parallel ideal branch circuits.
    n = (selected_columns, 80-selected_columns+79*selected_columns,
         79*(80-selected_columns))
    assert sum(n) == 6400
    gaps = (base, base+stroke, base+2*stroke)
    # All rotors aligned gives maximum instantaneous total flux at fixed bus MMF.
    reluctances = [x/(MU0*area) for x in gaps]
    conductance = sum(ni/ri for ni,ri in zip(n,reluctances))
    bus_mmf = bcap*base/MU0
    flux = bus_mmf*conductance
    # Required total common return area at the same stipulated field cap.
    return {'class_counts': n, 'return_area_mm2': flux/bcap*1e6,
            'source_mmf_AT_ideal': bus_mmf,
            'common_reluctance_for_10pct_bus_drop_A_per_Wb': (1/.9-1)/conductance,
            'half_B_over_selected': base/(base+stroke)}


def shunt_peak(stroke, feed_gap, closed=.0001, half=False):
    # Rotor has .2-mm minimum working gap, two bypass shunts in parallel.
    # Source -> feed -> (rotor || row bypass || column bypass) -> return.
    shunts = (closed if half else closed+stroke, closed+stroke)
    q = 1 + feed_gap * sum(1/h for h in shunts)
    return peak(mmf=1/q, base=.0002+feed_gap/q)[0]


def checks():
    # Numerical derivative of coenergy at fixed field angle vs rotor angle.
    errors = []
    for delta,base in itertools.product((-.7,-.3,.1,.8),(.0002,.0004,.0029)):
        h = 1e-6
        co = lambda th: .5*MU0*AREA*123**2/gap(delta-th,base)
        fd = (co(h)-co(-h))/(2*h)
        errors.append(abs(fd-torque(delta,123,base)))
    assert max(errors) < 1e-12
    convergence = []
    for n in (256,1024,4096):
        numerical = max(torque(math.pi*i/(2*n),1.) for i in range(n+1))
        convergence.append(abs(numerical/peak()[0]-1))
    assert convergence[-1] < 1e-7
    assert peak(amplitude=0)[0] == 0 and torque(.3,0) == 0
    assert abs(torque(.3,-10)-torque(.3,10)) < 1e-20  # current reversal is not motion reversal
    assert torque(.3,10) == -torque(-.3,10)
    assert abs(peak(2)[0]/peak(1)[0]-4) < 1e-12
    assert peak(base=G+.001)[0] < peak()[0]
    # Independently integrate torque over a closed rotor turn; conservative fixed field.
    cycle = sum(torque(2*math.pi*(i+.5)/8192,123) for i in range(8192))*2*math.pi/8192
    assert abs(cycle) < 1e-15
    # Square-thread lossless and incipient-overhaul limits.
    assert abs(thread(1,0,1)-LEAD/(2*math.pi)) < 1e-20
    assert abs(thread(1,LEAD/(2*math.pi*RADIUS),-1)) < 1e-20
    # Exhaustive tiny crossbar masks validate the analytic population classes.
    for row in range(4):
        for mask in range(16):
            n = [0,0,0]
            for i,j in itertools.product(range(4),repeat=2):
                n[(i!=row)+(not bool(mask & (1<<j)))] += 1
            s = mask.bit_count()
            assert n == [s,4-s+3*s,3*(4-s)]
    # Independent Kirchhoff solution for parallel flux plus finite common reluctance.
    rels = [G/(MU0*AREA), (G+.0025)/(MU0*AREA)]
    rc, source = 1e5, 100.
    permeance = sum(1/r for r in rels)
    bus = source/(1+rc*permeance)
    fluxes = [bus/r for r in rels]
    assert all(abs(source-rc*sum(fluxes)-r*p)<1e-10 for r,p in zip(rels,fluxes))
    assert abs(source*sum(fluxes)-(rc*sum(fluxes)**2+sum(r*p*p for r,p in zip(rels,fluxes)))) < 1e-10
    return {'coenergy_derivative_max_error_Nm':max(errors),
            'angular_grid_relative_peak_errors':convergence,'closed_cycle_work_J':cycle}


def main():
    result = {'checks': checks()}
    capacity = []
    for cap in (.4,.8,1.2):
        mmf = cap*G/MU0     # B never exceeds cap at any phase in this ideal branch.
        t,angle = peak(mmf)
        capacity.append({'stipulated_B_cap_T':cap,'branch_mmf_AT':mmf,
                         'peak_torque_Nmm':1000*t,'phase_rad':angle,
                         'max_gate_attraction_N':cap*cap*AREA/(2*MU0)})
    result['capacity'] = capacity
    result['shunt_comparison'] = [
        {'stroke_mm':d*1000,'feed_gap_mm':f*1000,
         'torque_contrast':shunt_peak(d,f)/shunt_peak(d,f,half=True),
         'mmf_for_1N_mu03_AT':math.sqrt(thread(1,.3,1)/shunt_peak(d,f))}
        for d,f in itertools.product((.0005,.0025,.01), (0.,.0002,.002,.02))]
    assert shunt_peak(.0025,0) == shunt_peak(.0025,0,half=True)
    # Validate reduced shunt expression against explicit flux/node equations.
    rotor_gap, feed, hrow, hcol, source = .00031,.0002,.0001,.0026,100.
    conductance = MU0*AREA*(1/rotor_gap+1/hrow+1/hcol)
    node = source/(1+feed/(MU0*AREA)*conductance)
    rotor_flux = node*MU0*AREA/rotor_gap
    reduced = source*MU0*AREA/(feed+rotor_gap*(1+feed/hrow+feed/hcol))
    assert abs(rotor_flux-reduced) < 1e-18
    # Independent derivative of whole-source coenergy (includes shunt/feed energy).
    for half in (False, True):
        feed, delta, mmf, step = .0002, .3, 100., 1e-6
        hr, hc = (.0001 if half else .0026), .0026
        def full_coenergy(theta):
            permeance = MU0*AREA*(1/gap(delta-theta,.0002)+1/hr+1/hc)
            total_reluctance = feed/(MU0*AREA)+1/permeance
            return .5*mmf*mmf/total_reluctance
        fd = (full_coenergy(step)-full_coenergy(-step))/(2*step)
        q = 1+feed/hr+feed/hc
        predicted = torque(delta,mmf/q,.0002+feed/q)
        assert abs(fd-predicted) < 1e-12
    select = []
    for W,mu in itertools.product((.02,1.,10.),(.02,.05,.3)):
        drive = thread(W,mu,1)
        hold = thread(.02,.02,-1)
        select.append({'selected_load_N':W,'selected_mu':mu,'drive_Nmm':1000*drive,
                       'neighbor_hold_Nmm':1000*hold,'torque_contrast_required':drive/hold,
                       'ideal_equal_crossed_fields_contrast':4,
                       'stroke_mm_nominal':1000*required_gap_addition(drive,hold),
                       'stroke_mm_adverse_50um':1000*required_gap_addition(drive,hold,.00005)})
    result['selection'] = select
    result['contrast_sensitivity'] = [
        {'stroke_mm':d*1000,'error_um':e*1e6,
         'torque_contrast':peak(base=G+3*e)[0]/peak(base=G-3*e+d-e)[0]}
        for d,e in itertools.product((.0005,.0025,.005,.01), (0.,.000025,.00005))]
    result['neighbor_friction_sensitivity'] = [
        {'neighbor_mu':mu,'hold_Nmm':thread(.02,mu,-1)*1000,
         'required_contrast_1N_mu03':None if mu<=LEAD/(2*math.pi*RADIUS)
         else thread(1,.3,1)/thread(.02,mu,-1)} for mu in (.01,.02,.05,.1,.3)]
    # Common bias shifts both cells; differential scenario above is a separate envelope.
    result['common_gap_bias'] = [
        {'bias_per_gap_um':b*1e6, 'contrast_2p5mm':peak(base=G+3*b)[0]/peak(base=G+3*b+.0025)[0]}
        for b in (-.00005,0,.00005)]
    result['fanout'] = [{'selected_columns':s,'stroke_mm':d*1000,**fanout(s,d)}
                        for s,d in itertools.product((1,40,80),(.0025,.01))]
    spec = importlib.util.spec_from_file_location('e156',Path(__file__).resolve().parents[1]/'E-156'/'screen.py')
    previous = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(previous)
    inertia = previous.rotor(RADIUS,LEAD)[0]
    result['moving_loss'] = []
    for mu,v,mult,direction in itertools.product((.01,.02,.05),(.02,.1),(1,5),(-1,1)):
        coast = previous.coast(RADIUS,LEAD,mu,.02,.002,inertia*mult,direction,v)
        result['moving_loss'].append({'mu_kinetic':mu,'speed_m_s':v,'inertia_multiplier':mult,
                                      'direction':direction,**coast})
    # One row per bank, mixed-sign full strokes in separate field-direction passes.
    result['schedules'] = []
    for v in (.02,.05,.1,.2):
        row_service = 2*.04/v+.02
        banks = next(b for b in range(1,81) if 6+math.ceil(80/b)*row_service <30)
        result['schedules'].append({'speed_m_s':v,'rotor_rpm':60*v/LEAD,
                                    'single_bank_map_s':6+80*row_service,
                                    'minimum_banks':banks,'map_s':6+math.ceil(80/banks)*row_service,
                                    'row_gates':80,'column_gates':80*banks})
    # Worst raising work, including thread friction. No geometric actuator efficiency claimed.
    result['board_raising_work_J'] = {str(mu):6400*thread(1,mu,1)*(.04/LEAD)*2*math.pi
                                     for mu in (.02,.05,.3)}
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
