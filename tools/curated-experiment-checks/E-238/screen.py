"""E-238: jointly synthesize supported strokes and retained whole-row programs.
Stdlib, stdout only. Physical dimensions, dynamics and costs are labelled bounds,
not measured priors. Inherits ideal support replay, not physical validation.
"""
import importlib.util
import itertools as it
import json
import math
from pathlib import Path


def load(number):
    p = Path(__file__).resolve().parents[1]/number/'screen.py'
    s = importlib.util.spec_from_file_location(number.replace('-', ''), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


old = load('E-230')
stroke = load('E-236')
move = old.move
Q = old.Q


def minimum_programs(seq):
    """Exact set cover, separable by net delta. Up to five old heights/delta.
    One mask may cover several starting heights; it cannot cover two deltas.
    DP over subsets of old-height requirements proves each minimum. Tie-break
    by bit order; unchanged heights use all-zero only. Seven shelves retained.
    """
    selected = []
    for delta in range(-4, 5):
        pairs = [(a, b) for a in range(5) for b in range(5) if b-a == delta]
        covers = {}
        for bits in it.product((0, 1), repeat=len(seq)):
            if delta == 0 and any(bits):
                continue
            covered = 0
            for i, (a, b) in enumerate(pairs):
                path = stroke.path(seq, a, bits)
                if path and path[0] == b and path[1] <= 6:
                    covered |= 1 << i
            if covered:
                covers[bits] = covered
        dp = {0: ()}
        for bits, covered in covers.items():
            for seen, chosen in list(dp.items()):
                nxt = seen | covered
                candidate = chosen+(bits,)
                if nxt not in dp or (len(candidate), candidate) < (len(dp[nxt]), dp[nxt]):
                    dp[nxt] = candidate
        full = (1 << len(pairs))-1
        if full not in dp:
            return None
        selected.extend(dp[full])
    table = {}
    for a, b in it.product(range(5), repeat=2):
        options = []
        for bits in selected:
            if a == b and any(bits):
                continue
            p = stroke.path(seq, a, bits)
            if p and p[0] == b and p[1] <= 6:
                options.append((p[1], p[2], bits, p[3]))
        table[a, b] = min(options)
    assert len(set(x[2] for x in table.values())) == len(selected)
    return selected, table


def synthesize():
    counts, representatives = [], {}
    for n in (5, 6):
        tested = reachable = valid = 0
        minimum = 100
        for middle in it.product(range(-4, 1), repeat=n-1):
            qs = (0,)+middle+(0,)
            seq = tuple(b-a for a, b in zip(qs, qs[1:]))
            if 0 in seq:
                continue
            tested += 1
            if not all(len(stroke.reachable(seq, h)) == 5 for h in range(5)):
                continue
            reachable += 1
            answer = minimum_programs(seq)
            if answer is None:
                continue
            valid += 1
            codes, table = answer
            minimum = min(minimum, len(codes))
            # These keys contain every sequence-dependent scheduler/inventory input.
            key = (n, len(codes), sum(abs(d) for d in seq), max(abs(q) for q in qs))
            # Prefer low excursion/travel among schedule-equivalent representatives.
            score = (max(x[1]-abs(b-a) for (a,b), x in table.items()), seq)
            if key not in representatives or score < representatives[key][0]:
                representatives[key] = (score, seq)
        counts.append(dict(pulses=n, tested=tested, reachable=reachable,
                           seven_shelf_survivors=valid, minimum_codes=minimum))
    return counts, [v[1] for v in representatives.values()]


def writer(kind, q, count, phases, pitch, error=.35):
    if kind == 'position':
        n = 80//q
        distance = (count-1)*pitch
        seconds = (2*move(distance)+2*move(2)+.010+n*(2*move(distance)+.010)
                   +(n-1)*move(5.08)+move((n-1)*5.08))
        return dict(seconds=seconds, stroke_mm=distance, sites=80)
    n = 80*phases//q
    assert 80*phases % q == 0
    speed = .8*min(200, (5.08-2-2*error)/(move(2)+.001),
                   2*math.sqrt(20000/(2*math.pi*2)))
    length = (n-1)*5.08+4+2*5.08
    span = length+speed**2/8000
    return dict(seconds=length/speed+2*speed/8000+move(span)+2*move(2)+.010,
                stroke_mm=span, sites=80*phases)


def service(seq, track_pitch=0):
    n = len(seq)
    # Predecessor's n decoder events retained as favorable local retract/proof
    # allowance. Explicit finite carriage travel added: n-1 track hops + return.
    index = (n-1)*move(track_pitch)+move((n-1)*track_pitch)
    return (sum(move(10*abs(d)) for d in seq)+n*old.prev.transfer()+n*old.STEP
            +index+move(5.08)+.020)


def schedule(seq, w, banks, buffered, track_pitch=0, visits=None, retry=True):
    n = math.ceil(80/banks) if visits is None else visits
    s = service(seq, track_pitch)
    ready, end = [], []
    for i in range(n):
        start = max(ready[-1] if ready else 0, end[i-2] if i >= 2 else 0)
        if not buffered:
            start = end[-1] if end else 0
        ready.append(start+w+(old.STEP if buffered else 0))
        end.append(max(ready[-1], end[-1] if end else 0)+s+(old.STEP if buffered else 0))
    if retry:
        depth = max(abs(q) for q in it.accumulate(seq, initial=0))
        # Retry is written after actual support/height read and empty datum reset;
        # includes full service, phase home, writer home and conservative row feed.
        end[-1] += move(10*depth)+.010+w+s+(2*old.STEP if buffered else 0)
    return 2+end[-1]


def inventory(kind, q, banks, buffered, count, phases, pitch):
    registers = banks*(2 if buffered else 1)
    sites = 80*registers*(1 if kind == 'position' else phases)
    lands = sites*count*phases if kind == 'position' else sites
    volume = sites*((count-1)*pitch+8)*(phases*6)*3/1e6 if kind == 'position' else sites*20*4*3/1e6
    cost = 195+20*banks+.5*q*banks+.02*sites+(4*banks+16 if buffered else 0)
    return dict(channels=q*banks, media_sites=sites,
                index_or_endpoint_sites=sites*(count if kind == 'position' else 2),
                decoder_lands=lands, media_stock_L=volume,
                lean_allocation=cost, bars_pickups_probes_each=80*banks,
                links=160*banks, registers=registers)


def screen(seqs, track_pitch):
    picks = {}
    for seq in seqs:
        count = len(minimum_programs(seq)[0])
        for kind, pitch in (('position',3), ('position',4), ('position',5), ('position',6), ('tape',6)):
            for buffered in (False, True):
                key = f'{kind}/pitch{pitch}/buffer{int(buffered)}'
                for q in Q:
                    w = writer(kind,q,count,len(seq),pitch)
                    for banks in range(1,81):
                        t = schedule(seq,w['seconds'],banks,buffered,track_pitch)
                        if t >= 30:
                            continue
                        inv = inventory(kind,q,banks,buffered,count,len(seq),pitch)
                        candidate = dict(kind=kind,pitch=pitch,buffered=buffered,seq=seq,
                                         code_count=count,q=q,banks=banks,seconds=t,
                                         writer=w,service_s=service(seq,track_pitch),inventory=inv)
                        score = (inv['lean_allocation'],t,seq)
                        if key not in picks or score < picks[key][0]:
                            picks[key] = (score,candidate)
    return {k:v[1] for k,v in picks.items()}


def checks(seqs):
    chosen = (-2,-1,3,-1,1)
    programs, table = minimum_programs(chosen)
    assert len(programs) == 10
    # A single +2 code cannot serve all three starting heights. Independently
    # intersect sets of feasible words (including seven-shelf constraint).
    sets=[]
    for a in (0,1,2):
        sets.append({bits for bits in it.product((0,1),repeat=5)
                     if (p:=stroke.path(chosen,a,bits)) and p[0]==a+2 and p[1]<=6})
    assert not set.intersection(*sets)
    maps = obs = 0
    for seq in (chosen,(-1,-1,-2,1,1,2),(-2,1,1,-2,2)):
        _,table=minimum_programs(seq)
        for a,b in it.product(it.product(range(5),repeat=3),repeat=2):
            obs += stroke.replay(seq,table,a,b)
            maps += 1
    retries = 0
    for seq in seqs:
        _,table=minimum_programs(seq)
        for (a,b),entry in table.items():
            for h in entry[3]:
                stroke.replay(seq,table,(h,),(b,)); retries += 1
        for buffered in (False,True):
            for banks in (4,8,80):
                w=.7; n=math.ceil(80/banks); s=service(seq,6)
                baseline=schedule(seq,w,banks,buffered,6,retry=False)
                if not buffered:
                    assert abs(baseline-(2+n*(w+s)))<1e-9
                else:
                    # Independent two-machine pipeline makespan (two slots suffice).
                    expected=2+w+old.STEP+s+old.STEP+(n-1)*max(w+old.STEP,s+old.STEP)
                    assert abs(baseline-expected)<1e-9
                assert schedule(seq,w,banks,buffered,6)>baseline+w+s
    assert abs(writer('position',20,9,6,3)['seconds']-old.writer('position',20)['seconds'])<1e-9
    assert abs(writer('tape',20,9,6,6)['seconds']-old.writer('tape',20)['seconds'])<1e-9
    assert abs(service((-1,-1,-2,1,1,2),0)-(old.service()-1.1+.55))<1e-9
    # As in predecessor, phase/output proof is a grant; model checks reject faults.
    for fault in ('write','pickup','brake','active_rewrite','reseat'):
        try: stroke.replay(chosen,minimum_programs(chosen)[1],(0,4,2),(4,0,2),fault)
        except AssertionError: pass
        else: raise AssertionError(fault)
    return dict(three_cell_maps=maps,support_observations=obs,
                partial_retries=retries,injected_interlocks=5,
                schedule_crosscheck='independent pipeline formula',physical_measurements=0)


def main():
    counts,seqs=synthesize()
    finite=screen(seqs,6)
    oracle=screen(seqs,0)
    broad=min((c for c in finite.values() if c['pitch']==6),key=lambda c:c['inventory']['lean_allocation'])
    seq=tuple(broad['seq']); b=broad['banks']; q=broad['q']; buffered=broad['buffered']
    w=broad['writer']['seconds']
    out=dict(evidence='finite exact synthesis and unqualified assumption calculations',
        search=counts,scheduler_equivalence_classes=len(seqs),checks=checks(seqs),
        inherited_five_stroke_programs=minimum_programs((-2,-1,3,-1,1))[0],
        best_broad_max_extra_travel_mm=10*max(c[1]-abs(b-a) for (a,b),c in minimum_programs(seq)[1].items()),
        zero_span_phase_oracle=oracle,finite_6mm_track=finite,
        broad_best_five_row_patch=schedule(seq,w,b,buffered,6,visits=5),
        broad_best_no_retry=schedule(seq,w,b,buffered,6,retry=False),
        broad_best_drive={str(f):old.drive(b,f) for f in (1,3.27,10)},
        error_scenarios={str(e):dict(position3_margin=.5-e,position4_margin=1-e,position5_margin=1.5-e,position6_margin=2-e,
                                   track6_probe2_margin=2-e,resident_4_2_margin=1-e,
                                   support_settling=2*e) for e in (.15,.35,.70)},
        best_broad_code_table=[dict(old=a,target=b,mask=c[2],heights=c[3])
                              for (a,b),c in minimum_programs(seq)[1].items()])
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
