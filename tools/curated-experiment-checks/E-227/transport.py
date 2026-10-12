"""E-227 resource screen: finite side extraction, optimistic pooled handling.
Stdlib; stdout only. Bounds and queue replay, not a routed or qualified machine.
"""
import collections
import heapq
import itertools
import json
import math


def move(d, v=200, a=8000):
    assert d >= 0 and v > 0 and a > 0
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def times(v=200, a=8000, rotation=.375, handler_y=0, indexed=False):
    m=lambda d: move(d,v,a)
    writing=3*m(40)+4*m(10)+6*(m(3)+.002)+2*rotation+.3
    support=2*m(40) if not indexed else 80*(m(1)+.001)
    exchange=support+2*m(73)+2*m(113)
    shuttle=2*m(414)+exchange+2*m(2.4)+m(5.08)+.2
    handling=2*m(112)+m(handler_y)
    return dict(writer=writing, shuttle=shuttle, handling=handling)


def necessary(t, jobs=81, available=28):
    # Strict <, so equality needs another resource. Aggregate service only;
    # startup, precedence, travel beyond allotted strokes and queues omitted.
    return dict(writers=math.floor(jobs*t['writer']/available)+1,
                shuttles=math.floor(jobs*t['shuttle']/available)+1,
                handlers=math.floor(2*jobs*t['handling']/available)+1)


def replay(writers, banks, handlers, t, retry=True, spares=1):
    """Finite circulating blanks and staging docks/bank, one bed/writer.
    Queue routes: write -> deliver -> shuttle/exchange -> collect -> write.
    A finished writer stays occupied until delivery handler picks up its cassette.
    Final outgoing media are returned to docks (no hidden next-map preparation).
    All-to-all handlers are a favorable relaxation of one physical gantry:
    collision-free parallel paths and zero y displacement are NOT demonstrated.
    """
    assert 80 % banks == 0 and writers > 0 and handlers > 0
    count=[80//banks+int(retry and i==0) for i in range(banks)]
    issued=[min(spares,n) for n in count]
    todo=collections.deque(b for b,n in enumerate(issued) for _ in range(n))
    hq=collections.deque(); sq=[collections.deque() for _ in range(banks)]
    busy_s=[False]*banks
    total=count.copy()
    free_w=list(range(writers)); free_h=list(range(handlers))
    events=[]; seq=0; trace=[]; now=0.; finished=0; playable=0.
    def event(dt,kind,b,res):
        nonlocal seq
        heapq.heappush(events,(now+dt,seq,kind,b,res));seq+=1
    def record(kind,res,b,duration):
        trace.append((kind,res,b,now,now+duration))
    def start_shuttle(b):
        if sq[b] and not busy_s[b]:
            sq[b].popleft();busy_s[b]=True
            record('shuttle',b,b,t['shuttle'])
            event(t['shuttle'],'exchanged',b,b)
    def dispatch():
        # Handler pickup frees a blocked writer; loop then fills newly free beds.
        while True:
            progressed=False
            while free_h and hq:
                stage,b,w=hq.popleft();h=free_h.pop()
                if stage=='deliver': free_w.append(w)
                record('handler',h,b,t['handling'])
                event(t['handling'],stage,b,h);progressed=True
            while free_w and todo:
                b=todo.popleft();w=free_w.pop()
                record('writer',w,b,t['writer'])
                event(t['writer'],'written',b,w);progressed=True
            if not progressed: break
    dispatch()
    while events:
        now=events[0][0]
        batch=[]
        while events and abs(events[0][0]-now)<1e-10: batch.append(heapq.heappop(events))
        for _,_,kind,b,res in batch:
            if kind=='written': hq.append(('deliver',b,res))
            elif kind=='deliver':
                free_h.append(res)
                sq[b].append(True);start_shuttle(b)
            elif kind=='exchanged':
                playable=max(playable,now);hq.append(('collect',b,None))
                busy_s[b]=False;start_shuttle(b)
            elif kind=='collect':
                free_h.append(res);count[b]-=1;finished+=1
                if issued[b]<total[b]:
                    todo.append(b);issued[b]+=1
        dispatch()
    assert finished==80+int(retry) and not todo and not hq and not any(count)
    assert len(free_w)==writers and len(free_h)==handlers and not any(busy_s)
    assert all(not q for q in sq)
    assert sum(k=='writer' for k,*_ in trace)==finished
    assert sum(k=='handler' for k,*_ in trace)==2*finished
    assert sum(k=='shuttle' for k,*_ in trace)==finished
    assert all(sum(k=='shuttle' and b==bank for k,r,b,a,z in trace)==n
               for bank,n in enumerate(total))
    # Independent exclusivity and resource-work lower bounds.
    for kind,n in [('writer',writers),('handler',handlers),('shuttle',banks)]:
        for res in range(n):
            intervals=sorted((a,z) for k,r,b,a,z in trace if k==kind and r==res)
            assert all(z<=a2+1e-9 for (a,z),(a2,z2) in zip(intervals,intervals[1:]))
    jobs=80+int(retry)
    assert now+1e-8 >= max(jobs*t['writer']/writers,
                           2*jobs*t['handling']/handlers,
                           max(80//banks+int(retry),80//banks)*t['shuttle'])
    return dict(writers=writers,shuttles=banks,handlers=handlers,
                selectors=80*writers,spares_per_bank=spares,seconds=2+now,playable_seconds=2+playable,
                allocation=100+57*writers+42*banks+20*handlers)


def checks():
    assert move(0)==0 and math.isclose(move(5),.05)
    assert math.isclose(move(414),2.095)
    t=times()
    serial=replay(1,1,1,t)
    assert math.isclose(serial['seconds'],2+81*(t['writer']+t['shuttle']+2*t['handling']))
    # With no retry, 80 fully independent resource sets finish in one chain.
    parallel=replay(80,80,80,t,retry=False)
    assert math.isclose(parallel['seconds'],2+t['writer']+t['shuttle']+2*t['handling'])
    # Interval construction: 406.4 mm cassette clears x=406.4 with 4 mm gap.
    assert 414-406.4 >= 4
    # A 104-mm upright union can pass underneath a parked union with 8 mm gap.
    assert 112-104 == 8
    assert times(indexed=True)['shuttle']>t['shuttle']
    assert times(v=400,a=16000)['shuttle']<t['shuttle']
    return dict(serial_seconds=serial['seconds'],independent_seconds=parallel['seconds'],
                cases='resource exclusivity, work bounds, serial/parallel limits, finite intervals')


if __name__=='__main__':
    out=dict(checks=checks(),nominal_times=times(),necessary=necessary(times()),scenarios={})
    for name,kw in [('nominal',{}),('y100',dict(handler_y=100)),
                    ('y200',dict(handler_y=200)),('indexed',dict(indexed=True)),
                    ('double_speed',dict(v=400,a=16000)),
                    ('slow_rotation',dict(rotation=.75))]:
        t=times(**kw)
        runs=[replay(w,b,h,t,spares=s) for w,b,h,s in itertools.product(
            (4,6,7,8,10,12,16,20),(10,16,20,40,80),(1,7,8,12,16,20),(1,2,3))]
        feasible=[r for r in runs if r['seconds']<30]
        out['scenarios'][name]=dict(necessary=necessary(t),
            fastest=min(runs,key=lambda r:r['seconds']),
            cheapest_under30=min(feasible,key=lambda r:r['allocation']) if feasible else None)
    out['buffer_controls']=[replay(8,40,8,times(),spares=s) for s in (1,2,3)]
    out['controls']=[replay(w,b,h,times()) for w,b,h in [(6,20,1),(7,20,7),(8,20,8),(8,40,8)]]
    print(json.dumps(out,indent=2))
