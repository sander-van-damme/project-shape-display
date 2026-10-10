#!/usr/bin/env python3
"""E-104: deterministic optimistic hydraulic-writer screen; mm, N, s, MPa.
No fluid/actuator catalog data, probability model or hardware validation.
Exact events implement common scaling of per-channel free speeds at a pump cap.
"""
import itertools
import json
import math
from dataclasses import dataclass, replace

N = 80
PITCH = 5.08
TRAVEL = 40.0
LIMIT = 30.0


@dataclass(frozen=True)
class Scenario:
    bore: float = 3.0
    flow_lpm: float = 8.0  # magnitude, available in BOTH directions
    speed: float = 400.0  # free piston-speed cap, both directions
    shared_speed: float = 1.0
    speed_spread: float = 0.0  # alternating bounded channels, not a distribution
    bore_bias: float = 0.0
    bore_spread: float = 0.0
    acceleration: float = 5000.0
    index_speed: float = 200.0
    acquire_withdraw: float = 0.040  # total per visited row
    phase_overhead: float = 0.010  # pressure setup + open/close latency
    row_read_settle: float = 0.020  # parallel reader ASSUMED
    global_setup: float = 0.5  # per map, includes digital preparation

    @property
    def pump(self):
        return self.flow_lpm * 1e6 / 60.0  # mm^3/s

    def area(self, col):
        diameter = self.bore + self.bore_bias + (-1 if col % 2 else 1) * self.bore_spread
        assert diameter > 0
        return math.pi * diameter ** 2 / 4

    def cap(self, col):
        v = self.speed * self.shared_speed * (1 + (-1 if col % 2 else 1) * self.speed_spread)
        assert v > 0
        return v


def motion_time(distance, vmax, acceleration):
    """Rest-to-rest triangular/trapezoidal motion, with zero registration delay."""
    assert distance >= 0 and vmax > 0 and acceleration > 0
    if distance <= vmax * vmax / acceleration:
        return 2 * math.sqrt(distance / acceleration)
    return distance / vmax + vmax / acceleration


def phase(channels, s):
    """(column, positive stroke); ideal pressure flow sharing and exact closure.
    Pump scales all active free speeds equally. Completion events have zero
    latency here; finite phase overhead and closure-error diagnostics are separate.
    """
    if not channels:
        return dict(time=0.0, lower=0.0, volume=0.0)
    points = sorted((stroke / s.cap(col), s.area(col) * s.cap(col)) for col, stroke in channels)
    volume = sum(s.area(c) * h for c, h in channels)
    lower = max(volume / s.pump, points[-1][0])
    previous = elapsed = 0.0
    rate = sum(q for _, q in points)
    for event, q in points:
        elapsed += (event - previous) * max(1.0, rate / s.pump)
        rate -= q
        previous = event
    assert elapsed + 1e-9 >= lower
    return dict(time=elapsed, lower=lower, volume=volume)


def route(rows, start, s):
    if not rows:
        return 0.0
    def visit(order):
        last, elapsed = start, 0.0
        for row in order:
            elapsed += motion_time(abs(row - last) * PITCH, s.index_speed, s.acceleration)
            last = row
        return elapsed
    # Two monotone endpoint-first policies; no claim of optimal tour at finite accel.
    return min(visit(sorted(rows)), visit(sorted(rows, reverse=True)))


def evaluate(work, s, start=0, retries=0):
    """work maps row->[(column,signed change)]. One bank; up/down separate.
    Each retry budgets ALL changed channels through a full stroke in BOTH
    directions, bounding mixed under/overshoot correction after fault arrest.
    Unchanged channels remain closed. This is a bound, not a reset command.
    """
    flow = lower = volume = 0.0
    phase_count = 0
    row_times = []
    recovery_times = []
    rows = {r: [(c, dh) for c, dh in cs if dh] for r, cs in work.items()}
    rows = {r: cs for r, cs in rows.items() if cs}
    for channels in rows.values():
        rowtime = s.acquire_withdraw + s.row_read_settle
        for sign in (1, -1):
            p = phase([(c, abs(h)) for c, h in channels if h * sign > 0], s)
            if p['volume']:
                phase_count += 1
                rowtime += p['time'] + s.phase_overhead
                flow += p['time']
                lower += p['lower']
                volume += p['volume']
        row_times.append(rowtime)
        recovery_times.append(s.acquire_withdraw + s.row_read_settle +
                              2 * (s.phase_overhead + phase([(c, TRAVEL) for c, _ in channels], s)['time']))
    indexing = route(rows, start, s)
    retry_time = retries * max(recovery_times, default=0.0)
    total = (s.global_setup + indexing + sum(row_times) + retry_time) if rows else 0.0
    return dict(total=total, flow=flow, ideal_flow_lower=lower, volume_ml=volume/1000,
                index=indexing, phases=phase_count, rows=len(rows), retry=retry_time)


def workloads():
    return {
        'all_up': {r: [(c, 40.) for c in range(N)] for r in range(N)},
        'alternating_rows': {r: [(c, 40. * (-1 if r % 2 else 1)) for c in range(N)] for r in range(N)},
        'checkerboard': {r: [(c, 40. * (-1 if (r+c) % 2 else 1)) for c in range(N)] for r in range(N)},
        'minority_down': {r: [(c, -40. if c == 0 else 40.) for c in range(N)] for r in range(N)},
        'mixed_sparse': {r: [(0, 40.), (1, -40.)] for r in range(N)},
        'graded_mixed': {r: [(c, (-1 if c % 2 else 1) * (1 + (c*17+r*13) % 40)) for c in range(N)] for r in range(N)},
    }


def uniform_envelope(s, retries=1):
    """Exact arbitrary-map ideal bound at uniform area/speed.
    Every phase increases monotonically with strokes; set all nonzero strokes
    to 40. Symmetry leaves just 81 up/down counts, including unmixed cases.
    For mixed rows convex max(n*V/Q,H/v)+max((N-n)*V/Q,H/v) is largest
    at one minority cell. Zero changes cannot make this bound worse.
    """
    assert s.speed_spread == s.bore_spread == 0
    times=[]
    recovery=s.acquire_withdraw+s.row_read_settle+2*(s.phase_overhead+max(N*s.area(0)*TRAVEL/s.pump,TRAVEL/s.cap(0)))
    for n in range(N+1):
        up=max(n*s.area(0)*TRAVEL/s.pump,TRAVEL/s.cap(0)) if n else 0
        down=max((N-n)*s.area(0)*TRAVEL/s.pump,TRAVEL/s.cap(0)) if n<N else 0
        phases=int(n>0)+int(n<N)
        row=s.acquire_withdraw+s.row_read_settle+phases*s.phase_overhead+up+down
        times.append(s.global_setup+route(range(N),0,s)+N*row+retries*recovery)
    return dict(worst=max(times),up_count=times.index(max(times)),cases=len(times))


def cost_cap(shared, head, cell):
    return shared + N * head + N*N * cell


def pressure_bounds(area, bias, drag, payload, return_pressure):
    """Static necessary inequalities. Strict lowering reserve >0 required.
    Payload is downward external force; check unloaded lowering separately.
    """
    return dict(up_min_mpa=(bias + drag + payload)/area,
                down_reserve_n=bias + payload - drag - return_pressure*area)


def check():
    s = Scenario()
    a = s.area(0)
    assert math.isclose(a*40*6400/1e6, 1.8095573684677209)
    # Independent SI pump conversion and volume conservation.
    assert math.isclose(s.pump*1e-9, s.flow_lpm*1e-3/60)
    assert phase([], s)['time'] == 0
    assert evaluate({}, s)['total'] == 0
    assert motion_time(0,200,5000) == 0
    assert math.isclose(motion_time(8,200,5000), .08)
    assert math.isclose(motion_time(100,200,5000), .54)
    equal = [(c,40.) for c in range(80)]
    assert math.isclose(phase(equal,s)['time'], max(40/s.speed,80*a*40/s.pump))
    # In the flow-limited regime, duration*Q exactly equals moved volume.
    slowpump=replace(s,flow_lpm=.01)
    p=phase([(0,1.),(1,40.)],slowpump)
    assert math.isclose(p['time']*slowpump.pump,p['volume'])
    assert math.isclose(phase(equal,replace(s,flow_lpm=1e6))['time'],.1)
    # Unequal-stroke event model must NOT be mislabeled the max-of-bounds result.
    p=phase([(0,1.),(1,40.)],replace(s,flow_lpm=.01,speed=2))
    assert p['time'] >= p['lower']
    # Independent fixed-time-step integration of a heterogeneous phase.
    varied=replace(s,flow_lpm=.08,speed=100,speed_spread=.2,bore_spread=.05)
    channels=[(0,3.),(1,7.),(2,1.)]
    exact=phase(channels,varied)['time']
    for dt in (.001,.0005,.00025):
        remain=[h for _,h in channels]
        t=0
        while max(remain)>1e-12:
            rate=sum(varied.area(c)*varied.cap(c) for (c,_),h in zip(channels,remain) if h>1e-12)
            scale=min(1.,varied.pump/rate)
            remain=[max(0.,h-varied.cap(c)*scale*dt) for (c,_),h in zip(channels,remain)]
            t+=dt
        assert abs(t-exact) <= 4*dt
    w=workloads()
    assert evaluate(w['all_up'],s) == evaluate(w['alternating_rows'],s)
    assert evaluate(w['checkerboard'],s)['phases'] == 160
    assert math.isclose(uniform_envelope(s)['worst'], evaluate(w['minority_down'],s,retries=1)['total'])
    assert math.isclose(evaluate(w['all_up'],s)['volume_ml'],evaluate(w['checkerboard'],s)['volume_ml'])
    assert evaluate(w['mixed_sparse'],s)['flow'] == evaluate(w['checkerboard'],s)['flow']
    assert cost_cap(250,2,.0140625) == 500
    assert pressure_bounds(a,.1,.2,0,0)['down_reserve_n'] < 0
    for workload in w.values():
        assert evaluate(workload,replace(s,flow_lpm=4))['total'] >= evaluate(workload,s)['total']-1e-9
        assert evaluate(workload,replace(s,shared_speed=.5))['total'] >= evaluate(workload,s)['total']-1e-9
    return 'PASS: SI/conservation, event-vs-step, limits, sign/workloads, monotonicity, cost/force'


def main():
    report={'checks':check()}
    s=Scenario()
    ws=workloads()
    report['reference']={name:evaluate(w,s,retries=1) for name,w in ws.items()}
    report['grid']=[]
    for d,q,v in itertools.product((2.,3.,4.),(2.,4.,8.),(100.,250.,400.)):
        sc=replace(s,bore=d,flow_lpm=q,speed=v)
        envelope=uniform_envelope(sc)
        times={k:evaluate(ws[k],sc,retries=1)['total'] for k in ('all_up','checkerboard','minority_down')}
        report['grid'].append(dict(bore=d,lpm=q,speed=v,**times,**envelope,survives=envelope['worst']<LIMIT))
    report['inverse']={}
    available_row_flow=(30-s.global_setup-route(range(N),0,s))/(N+1)-(s.acquire_withdraw+s.row_read_settle+2*s.phase_overhead)
    for d in (2.,3.,4.):
        sc=replace(s,bore=d)
        # Solve the monotone complete envelope incl. conservative retry.
        lo,hi=.001,1000.
        for _ in range(50):
            mid=(lo+hi)/2
            if uniform_envelope(replace(sc,flow_lpm=mid))['worst']<30:
                hi=mid
            else:
                lo=mid
        report['inverse'][str(d)]={'minimum_lpm_at_400':hi}
    report['inverse']['minimum_speed_at_unlimited_flow']=80/available_row_flow
    report['uncertainty']={}
    for name,sc in {
        'reference':s,
        'two_mm_8lpm':replace(s,bore=2),
        'two_mm_8lpm_common80':replace(s,bore=2,shared_speed=.8),
        'three_mm_12lpm':replace(s,flow_lpm=12),
        'common_speed_80pct':replace(s,shared_speed=.8),
        'common_speed_50pct':replace(s,shared_speed=.5),
        'alternating_speed_20pct':replace(s,speed_spread=.2),
        'bore_plus_0.1_alternating_0.05':replace(s,bore_bias=.1,bore_spread=.05),
        'combined':replace(s,shared_speed=.8,speed_spread=.2,bore_bias=.1,bore_spread=.05),
        'double_row_overhead':replace(s,acquire_withdraw=.08,row_read_settle=.04,phase_overhead=.02),
    }.items():
        report['uncertainty'][name]={k:evaluate(w,sc,retries=1)['total'] for k,w in ws.items()}
    # All spatial translations of a 10x10 mixed patch, writer at either edge.
    local=[]
    for r0,c0 in itertools.product(range(71),range(71)):
        patch={r:[(c,40.*(-1 if (r+c)%2 else 1)) for c in range(c0,c0+10)] for r in range(r0,r0+10)}
        for start in (0,79):
            local.append(evaluate(patch,s,start=start,retries=1)['total'])
    report['local_10x10']={'alignments':len(local),'min':min(local),'max':max(local)}
    report['cost']=[dict(shared=shared,head=head,max_cell=(500-shared-80*head)/6400)
                    for shared,head in itertools.product((150,250,350),(1,2,3,5))]
    # Diagnostic accuracy allocation, NOT a product requirement or actuator price.
    report['closure_diagnostic']={'height_budget_mm':.2,'read_error_mm':.05,
       'residual_delay_limit_ms_at_400mm_s':1000*(.2-.05)/400,
       'speed_limit_at_2ms':(.2-.05)/.002,
       'serial_reader_samples_per_second_min':80*400/(.2-.05),
       'checkerboard_at_that_speed_s':evaluate(ws['checkerboard'],replace(s,speed=75),retries=1)['total']}
    report['pressure']=[dict(bias=b,drag=f,return_mpa=p,**pressure_bounds(s.area(0),b,f,0,p))
                        for b,f,p in itertools.product((.1,.5,1.),(0.,.2,.5),(0.,.01))]
    # Pump outlet differential is an assumption incl. circuit losses, not deduced
    # from piston load; MPa * L/min * (1000/60) = watts.
    report['pump_power_w']={str(p):p*s.flow_lpm*1000/60 for p in (.1,.5,1.5)}
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
