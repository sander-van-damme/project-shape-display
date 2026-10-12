"""E-237: causal supported overwrite; deliberately unqualified physical bounds.
Stdlib, stdout only. Ideal state flags do not qualify contacts or power-loss safety.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path

spec = importlib.util.spec_from_file_location('e236', Path(__file__).resolve().parents[1]/'E-236'/'screen.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
move = prior.move
SEQ = (-2, -1, 3, -1, 1)
C = move(2)+.003
W = C


def clearance_time(g, stroke=2, a=8000):
    """First passage of g during symmetric triangular stroke from rest.
    Contact speed/acceleration inherited; stroke=2 never reaches 200 mm/s.
    g is actual engagement + adverse error, NOT nominal printed tolerance.
    """
    assert 0 <= g <= stroke
    half = math.sqrt(stroke/a)
    return math.sqrt(2*g/a) if g <= stroke/2 else 2*half-math.sqrt(2*(stroke-g)/a)


def segment(rows, delay, overlap=True, lift_a=8000):
    """One block of rows; initial write cannot be prepared before receipt.
    Inhibit and forced return granted; start next write only after reseat proof
    and clearance. New mask remains disconnected until entire retraction ends.
    Row feed may overlap writing, with output bridge routing granted.
    """
    ready = W
    end = 0.
    n = rows*5
    for k in range(n):
        start = max(end, ready)
        reseated = start+3*C+move(abs(SEQ[k%5])*10,a=lift_a)
        end = reseated+C
        if k%5 == 4:
            end += move(5.08)
        if k+1 < n:
            ready = (reseated+delay if overlap else end)+W
    return end


def schedule(banks=4, delay=0, overlap=True, lift_a=8000, rows=None):
    n = math.ceil(80/banks) if rows is None else rows
    # Retry cannot use prewritten commands: discard any speculative next mask,
    # safely reseat, empty reset from q=-3, measure actual heights, regenerate.
    return 2+move(30,a=lift_a)+.010+segment(n,delay,overlap,lift_a)+segment(1,delay,overlap,lift_a)


def state_checks():
    cases = observations = 0
    for old, new in it.product(it.product((False,True),repeat=4),repeat=2):
        # After stroke: old selected pickups are the only load path in active row.
        row = False; col = [not b for b in old]; pickup = list(old)
        def check():
            nonlocal observations
            assert all(row or c or p for c,p in zip(col,pickup))
            observations += 1
        check()
        # Resident support must be proved BEFORE home override and disconnect.
        row = True; col = [True]*4; check()
        inhibit = True
        command = list(new)  # all arbitrary overwritten masks are safe here
        assert inhibit
        # Common return holds outputs on home path regardless of new command.
        pickup = [False]*4; check()
        assert row and all(col) and not any(pickup)
        inhibit = False
        # Next acquisition connects only the new proven command.
        pickup = command[:]; check()
        assert pickup == list(new)
        row = False; col = [not b for b in new]; check()
        cases += 1
    # Counterexample: erase while last support remains active.
    assert not (False or False or False)  # row out, selected bar out, pickup erased
    # A global inhibit setting all outputs home cannot preserve arbitrary active
    # masks. Keeping those masks requires distinct output configurations.
    assert len(set(it.product((0,1),repeat=4))) == 16
    return dict(overwrite_pairs=cases,support_observations=observations,
                active_erase_witness=dict(row=False,column=False,pickup=False))


def drive(banks, load, lift_a, diameter_mm=12):
    mass=.5*banks+.003*80*banks
    force=80*banks*load*1.2+.5*banks*9.81+mass*lift_a/1000
    torque=.01*force
    return dict(force_N=force,torque_Nm=torque,peak_input_W=.2*force/.7,
        shaft_twist_mm=1000*.01*torque*.4/(80e9*math.pi*(diameter_mm/1000)**4/32),
        gravity_drag_ceiling_N=.003*(9.81-lift_a/1000))


def main():
    # Independent closed form for this regime: cross-row feed hides remaining W;
    # four within-row overwrites pay delay; initial normal and retry writes remain.
    for delay in (0,.003,.013,.020,C):
        expected=prior.schedule(SEQ,0,4)+2*W+84*delay
        assert abs(schedule(delay=delay)-expected)<1e-9
    assert abs(schedule(overlap=False)-prior.schedule(SEQ,W,4))<1e-9
    assert abs(clearance_time(1)-math.sqrt(2/8000))<1e-12
    assert abs(clearance_time(2)-move(2))<1e-12
    assert all(clearance_time(i/100)<=clearance_time((i+1)/100) for i in range(200))
    free=prior.schedule(SEQ,0,4)
    max_delay=(30-free-2*W)/84
    scenarios=[]
    for g in (0,.15,.35,.5,.65,1,1.35,1.7,2):
        delay=clearance_time(g)+.003
        b=next(b for b in range(1,81) if schedule(b,delay)<30)
        scenarios.append(dict(clearance_mm=g,release_delay_ms=delay*1000,
            four_bank_s=schedule(delay=delay),min_banks=b,
            shared_base_allocation=195+b*(20+80*.52)))
    sensitivity=[]
    for a in (2000,4000,6000,8000):
        sensitivity.append(dict(lift_acceleration_mm_s2=a,
            four_bank_s=schedule(delay=clearance_time(.35)+.003,lift_a=a),
            **drive(4,3.27,a)))
    # Actual actual-clearance = engagement + adverse correlated/local error.
    # Solve strict tipping point, not a fitted probability distribution.
    tips=[]
    for proof in (0,.003,.006):
        g=.5*8000*(max_delay-proof)**2 if max_delay>=proof else None
        tips.append(dict(clearance_proof_ms=1000*proof,max_actual_clearance_mm=g))
    # Optimistic two-register / retained-output bracket. Whole write hidden;
    # extra clamp+disconnect and reconnect+release stages each take C. No copy
    # mechanism, retained output force or actual geometry is thereby supplied.
    output_memory={
        'zero_extra_stage_B4_s':free+2*W,
        'two_extra_stages_B4_s':free+2*W+105*2*C,
        'added_min_output_bits_B4':320,
        'added_min_routing_isolation_sites_B4':640,
        'remaining_bought_allowance_B4':500-(195+4*(20+80*.52)),
    }
    print(json.dumps(dict(checks=state_checks(),unbuffered_B4=schedule(overlap=False),
        free_write_B4=free,zero_clearance_zero_proof_B4=schedule(),
        max_release_delay_ms=1000*max_delay,clearance_thresholds=tips,
        clearance_scenarios=scenarios,lift_sensitivity=sensitivity,
        output_retention_bracket=output_memory,
        load_sensitivity=[dict(load_per_cell_N=f,**drive(4,f,8000)) for f in (1,3.27,10)],
        regional_five_rows_s=schedule(delay=clearance_time(.35)+.003,rows=5)),indent=2))

if __name__ == '__main__': main()
