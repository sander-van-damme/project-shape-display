"""E-235: finite thin-web command layout, causal writing and feed.
Stdlib, stdout only. All dimensions/rates/prices are unqualified scenarios.
This constructs nonoverlapping information windows, NOT a routed mechanism.
"""
from bisect import bisect_left, insort
import importlib.util
import itertools
import json
import math
import random
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    'e229', Path(__file__).resolve().parents[1] / 'E-229' / 'screen.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
move = old.move
DIV = (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)


def layout(banks, writers=1, pitch=4000, lead=20000, retry=True):
    """Coordinates are integer micrometres. Identical independent web groups.
    s is web advance at service; u=s-y is the material coordinate at a reader.
    Every phase/bank gets a reserved pitch-wide mask window. A monotone greedy
    allocator is sufficient, not optimal or a necessary minimum consumption.
    Return worst group including one causal last-row retry at its far reader.
    """
    assert 80 % writers == banks % writers == 0 and writers <= banks <= 80
    heads, group_rows = banks // writers, 80 // writers
    sizes = [group_rows//heads + (b < group_rows % heads) for b in range(heads)]
    starts = [sum(sizes[:b]) for b in range(heads)]
    rows = max(sizes)
    centers, events, masks = [], [], []
    s = 0
    for r in range(rows):
        active = [b for b in range(heads) if r < sizes[b]]
        ys = [lead + (starts[b] + r) * 5080 for b in active]
        for phase in range(6):
            s = max(s + pitch, max(ys) + pitch)
            while True:
                shifted = s
                for y in ys:
                    u = s - y
                    lo = bisect_left(centers, u - pitch + 1)
                    hi = bisect_left(centers, u + pitch)
                    if lo < hi:
                        shifted = max(shifted, centers[hi - 1] + pitch + y)
                if shifted == s:
                    break
                s = shifted
            for bank, y in zip(active, ys):
                u = s - y
                insort(centers, u)
                masks.append((u, len(events), bank, y, False))
            events.append((s, phase, phase == 5, False))
    normal_end = s
    if retry:
        # A stable wrong final height is detected only after last normal service.
        # New signed deltas must be punched downstream of the current writer.
        y = lead + (group_rows - 1) * 5080
        for phase in range(6):
            s = max(s + pitch, normal_end + y + pitch)
            u = s - y
            assert u > normal_end
            insort(centers, u)
            masks.append((u, len(events), heads - 1, y, True))
            events.append((s, phase, False, True))
    assert all(b - a >= pitch for a, b in zip(centers, centers[1:]))
    assert len(centers) == 480 // writers + (6 if retry else 0)
    assert all(u + y == events[e][0] and u < events[e][0]
               for u, e, _, y, _ in masks)
    return dict(events=events, masks=masks, end=s, normal_end=normal_end,
                centers=centers, banks=banks, writers=writers, pitch=pitch)


def schedule(lay, a=8000, v=200, selector=2, punch=.5, proof=.005,
             coincidence_overlap=False):
    """Stop web at every punch and probe event; no free offline preparation.
    Punch cycle: data select, common down/up stroke, optical read.
    At service: clamp, low-force probe, backed shared yokes, signed pulse,
    reseat, probe release and row feed. Web is stationary until probes clear.
    All masks including all-solid words are proof/read stops (worst-useful
    all-changed map has holes in every phase distributed across the row).
    """
    def feed(d):
        return move(d, a=a, v=v)
    select_time = feed(selector)
    punch_time = 2 * feed(punch) + proof
    stops = {}
    for u, _, _, _, _ in lay['masks']:
        stops.setdefault(u, [0, 0])[0] += 1
    service = 0
    for s, phase, row_feed, _ in lay['events']:
        # E-229 pulse plus two probe/clamp strokes and explicit height reads.
        duration = (2 * move(old.STROKES[phase]) + old.transfer()
                    + 2 * (move(2) + .003) + .010
                    + (move(5.08) if row_feed else 0))
        stops.setdefault(s, [0, 0])[1] += duration
        service += duration
    t, pos, transport, write, overlap = 2., 0, 0., 0., 0.
    last_punch_end = 2.
    for s, (n, dwell) in sorted(stops.items()):
        dt = feed((s - pos) / 1000)
        transport += dt
        # With the common ram up, prepare the next data gates during feed or
        # service. Only unfinished preparation extends this stopped interval.
        assert n in (0, 1)
        wt = (max(0, last_punch_end + select_time - (t + dt))
              + punch_time) if n else 0
        if n:
            last_punch_end = t + dt + wt
        write += wt
        saved = min(wt, dwell) if coincidence_overlap else 0
        overlap += saved
        t += dt + wt + dwell - saved
        pos = s
    assert pos == lay['end']
    assert abs(t - (2 + transport + write + service - overlap)) < 1e-8
    return dict(seconds=t, feed_s=transport, writing_s=write, service_s=service,
                overlap_s=overlap, stopped_punch_s=punch_time, web_m=lay['end'] / 1e6,
                service_stops=len(lay['events']), punch_stops=len(lay['masks']),
                distinct_stops=len(stops))


def allocation(b, w, channel=.5, web_hardware=20):
    # E-230 shared drive/base + bank hardware; no precision tooling quote.
    # Each web has feed/hold $8, punch drive/die/stripper $8, writer reader $4.
    return 195 + 20*b + 80*w*channel + web_hardware*w


def free_flying_writer(lay, a=32000, v=400):
    """Changed-interface relaxation: zero punch stops, time, force and gates.
    Keep reader stops, finite feed and causal retry. NOT a writer construction.
    """
    time, pos = 2., 0
    for s, phase, row_feed, _ in lay['events']:
        time += move((s-pos)/1000, a=a, v=v)
        time += (2*move(old.STROKES[phase]) + old.transfer()
                 + 2*(move(2)+.003) + .010 + (move(5.08) if row_feed else 0))
        pos = s
    return time


def checks():
    # Support topology is inherited, not newly qualified by a new carrier.
    for before, after in itertools.product(itertools.product(range(5), repeat=2), repeat=2):
        old.replay(before, after)
    for b in range(1,81):
        for w in DIV:
            if b % w == 0:
                l = layout(b, w)
                assert min(l['centers']) >= l['pitch']
                plain = schedule(l)
                shared = schedule(l, coincidence_overlap=True)
                assert plain['seconds'] >= shared['seconds']
                assert plain['seconds'] > 2 + plain['writing_s'] + plain['service_s']
    # A naive one-pitch stream aliases independently commanded reader masks:
    # y2-y1 = 50.8 mm; after 13 advances of 4 mm their windows overlap.
    assert abs(13*4000 - 50800) < 4000
    assert abs(4000 - 5080) < 4000  # Next row moves reader too: -1.08-mm reuse.
    # Causal retry must move a fresh word from writer to farthest reader.
    l = layout(8, 1)
    first = next(m for m in l['masks'] if m[-1])
    assert first[0] > l['normal_end']
    assert l['events'][first[1]][0] - l['normal_end'] >= first[3] + 4000
    # Rest-to-rest triangle check, independent of imported implementation.
    assert abs(move(4) - 2*math.sqrt(4/8000)) < 1e-12
    # Construct a realizable full map with 480 distinct nonempty words. This
    # avoids claiming worst-useful throughput from six repeated +/-40 masks.
    rng = random.Random(235)
    words, rows, rejected = set(), [], 0
    while len(rows) < 80:
        before = tuple(rng.randrange(5) for _ in range(80))
        after = tuple(rng.randrange(5) for _ in range(80))
        masks = []
        for sign in (1, -1):
            codes = [old.base.code(max(0, sign*(b-a)), (1,1,2))
                     for a,b in zip(before, after)]
            masks.extend(tuple(bool(c[k]) for c in codes) for k in range(3))
        if len(set(masks)) != 6 or any(not any(m) or m in words for m in masks):
            rejected += 1
            continue
        old.replay(before, after)
        words.update(masks)
        rows.append(masks)
    assert len(words) == 480
    l = layout(8, retry=False)
    web = {u: rows[(y-20000)//5080][e % 6] for u,e,_,y,_ in l['masks']}
    # Reconstruct from sheet coordinate at each reader, not a bank word index.
    for u,e,_,y,_ in l['masks']:
        assert web[l['events'][e][0]-y] == rows[(y-20000)//5080][e % 6]
    return dict(two_cell_maps=625, fixed_reader_alias_um=1200,
                naive_row_feed_alias_um=-1080,
                causal_far_reader_mm=first[3]/1000, workload_seed=235,
                distinct_nonempty_mask_words=len(words), rejected_rows=rejected)


def main():
    out = dict(evidence='unqualified deterministic bounds and layout; no physical pass',
               checks=checks())
    grids = []
    for name, a, v, selector in [('base',8000,200,2),
                                ('short_selector',8000,200,.25),
                                ('fast_short',32000,400,.25)]:
        picks = []
        for b in range(1,81):
            for w in DIV:
                if b % w:
                    continue
                l = layout(b,w)
                s = schedule(l,a,v,selector,coincidence_overlap=True)
                if s['seconds'] < 30:
                    picks.append(dict(banks=b,writers=w,channels=80*w,
                                      allocation=allocation(b,w),**s))
        grids.append(dict(scenario=name, feasible=len(picks),
                          cheapest=min(picks,key=lambda x:x['allocation']) if picks else None,
                          fewest_channels=min(picks,key=lambda x:(x['channels'],x['allocation'])) if picks else None))
    out['grid'] = grids
    out['one_writer'] = {str(b): schedule(layout(b), coincidence_overlap=True) for b in (8,16,80)}
    out['layout_sensitivity'] = {
        str(p): dict(b8_w1_m=layout(8,pitch=p)['end']/1e6,
                     b8_w1_seconds=schedule(layout(8,pitch=p),coincidence_overlap=True)['seconds'])
        for p in (3000,4000,6000)}
    # Minimal gap-feed work between 486 pitch-separated punch locations;
    # rest-to-rest travel is concave, so t(pitch) per consecutive pair applies.
    # Writer work may overlap service but cannot overlap its own stopped feed.
    out['one_writer_feed_plus_punch_lower_s'] = {
        str(a): 485*move(4,a=a,v=v) + 486*2*move(.5,a=a,v=v)
        for a,v in ((8000,200),(32000,400))}
    out['free_flying_writer_relaxation'] = {
        str(b):dict(seconds=free_flying_writer(layout(b)),allocation=allocation(b,1))
        for b in (8,10,12,16)}
    out['consumption_b16_w4'] = dict(
        normal_m2=4*.42*layout(16,4,retry=False)['end']/1e6,
        one_retry_m2=.42*(3*layout(16,4,retry=False)['end']+layout(16,4)['end'])/1e6)
    out['punch_force_N'] = {
        f't{t}_tau{tau}':82*math.pi*3*t*tau  # 80 data + two fixed registration holes.
        for t in (.05,.1,.2) for tau in (10,20,40)}
    out['probe_margin_mm'] = {str(e):(3-1)/2-e for e in (.15,.35,.7,1.)}
    out['scale_drift_over_401mm'] = {str(e):e*401.32 for e in (.001,.0025,.005)}
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    main()
