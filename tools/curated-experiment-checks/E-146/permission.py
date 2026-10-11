#!/usr/bin/env python3
"""E-146: finite bilateral catches + permission counterexamples. Stdlib only.
Geometry in mm, impact in SI. Deterministic scenarios, no calibrated priors/yield.
"""
import itertools
import json
import math
from dataclasses import dataclass
from functools import cache


@dataclass(frozen=True)
class Section:
    pitch: float = 4.
    width: float = 3.2
    bolt: float = .8
    depth: float = .6
    phase_error: float = 0.

    @cache
    def intervals(self, side):
        phase = side*self.pitch/2 + side*self.phase_error
        a = (self.width-self.bolt)/2
        return [(-k*self.pitch-phase-a, -k*self.pitch-phase+a)
                for k in range(-11, 2)]

    def depths(self, q):
        return self.depth+q, self.depth-q

    def allowed(self, h, q):
        return all(d <= 0 or any(lo-1e-9 <= h <= hi+1e-9
                                for lo, hi in self.intervals(s))
                   for s, d in enumerate(self.depths(q)))

    def cell(self, h, q):
        lo, hi = -math.inf, math.inf
        for s, d in enumerate(self.depths(q)):
            if d > 0:
                a,b = next((a,b) for a,b in self.intervals(s)
                           if a-1e-9 <= h <= b+1e-9)
                lo,hi = max(lo,a),min(hi,b)
        return lo,hi

    @cache
    def solids(self, h):
        # boxes x,y,z. Two pocket rows, joined by central continuous spine.
        boxes = [(2.,4.,0.,2.,-46.+h,6.+h)]
        for side in (0,1):
            phase = side*self.pitch/2 + side*self.phase_error
            cuts = sorted((k*self.pitch+phase-self.width/2,
                           k*self.pitch+phase+self.width/2) for k in range(-12,3))
            start = -46.
            for low,high in cuts:
                if high <= start: continue
                if low >= 6.: break
                if low > start:
                    boxes.append((0. if side==0 else 4.,2. if side==0 else 6.,
                                  0.,2.,start+h,min(low,6.)+h))
                start=max(start,high)
            if start<6.:
                boxes.append((0. if side==0 else 4.,2. if side==0 else 6.,
                              0.,2.,start+h,6.+h))
        return boxes

    @cache
    def yoke(self,q):
        # Rigid translating U, bridge behind the rack; noses never reach spine.
        b=self.bolt/2
        return [(-3+q,self.depth+q,0,2,-b,b),
                (6-self.depth+q,9+q,0,2,-b,b),
                (-4+q,-3+q,0,4,-b,b),(9+q,10+q,0,4,-b,b),
                (-4+q,10+q,3,4,-b,b)]


def overlap(a,b):
    return math.prod(max(0.,min(a[i+1],b[i+1])-max(a[i],b[i])) for i in (0,2,4))


def solid_overlap(s,h,q):
    return sum(overlap(a,b) for a in s.solids(h) for b in s.yoke(q))


def sweep(s, steps):
    # A end -> insert B/withdraw A -> move to B end; repeat, then reverse.
    h=(s.width-s.bolt)/2
    q=1.
    start=h
    phases=[]
    for direction in (1,-1):
        for _ in range(20 if direction==1 else 21):
            # The current window end is inside the other row's next window.
            for j in range(steps+1):
                qt=q*(1-2*j/steps)
                assert s.allowed(h,qt)
                assert solid_overlap(s,h,qt)<1e-8
                phases.append((h,qt))
            q=-q
            lo,hi=s.cell(h,q)
            target=hi if direction==1 else max(start,lo)
            for j in range(steps+1):
                ht=h+(target-h)*j/steps
                assert s.allowed(ht,q)
                assert solid_overlap(s,ht,q)<1e-8
                phases.append((ht,q))
            h=target
    assert math.isclose(h,start)
    # Reverse cycle needs one extra partial packet; parked support must hold
    # a target inside a window. A fixed bolt alone permits its residual slack.
    max_span=max(s.cell(h,q)[1]-s.cell(h,q)[0] for h,q in phases)
    return {"states":len(phases),"max_seated_selector_span_mm":max_span,
            "min_one_nose_depth_mm":min(max(s.depths(q)) for h,q in phases),
            "height_extrema_mm":[min(h for h,q in phases),max(h for h,q in phases)],
            "start_mm":start,"finish_mm":h}


def energy_bound(m,v,force,free_distance,k,stored=0.):
    e=.5*m*v*v+force*free_distance+stored
    delta=(force+math.sqrt(force*force+2*k*e))/k
    return {"incident_J":e,"compression_mm":delta*1000,
            "excursion_mm":(free_distance+delta)*1000,"peak_N":k*delta}


def contact_integral(m,v,f,k,dt):
    # Undamped linear contact until first turning point; RK4 independent of root.
    x=0.; t=0.; last=(0.,v)
    while v>0 and t<1:
        def rhs(a,b): return b,(f-k*a)/m
        a,b=rhs(x,v); c,d=rhs(x+a*dt/2,v+b*dt/2)
        e,g=rhs(x+c*dt/2,v+d*dt/2); j,l=rhs(x+e*dt,v+g*dt)
        last=(x,v)
        x+=dt*(a+2*c+2*e+j)/6
        v+=dt*(b+2*d+2*g+l)/6
        t+=dt
    # Linear interpolation in velocity to first maximum (second order in dt).
    frac=last[1]/(last[1]-v)
    return last[0]+frac*(x-last[0])


def permission(path, mode, budget=2.):
    used=0.; trip=None
    for n,dx in enumerate(path):
        if mode=="absolute": used+=abs(dx)
        elif mode=="signed": used+=dx
        elif mode=="positive": used+=max(0,dx)
        if used>=budget-1e-12 and trip is None: trip=n+1
    return {"used_mm":used,"first_trip_segment":trip,"net_mm":sum(path),
            "path_mm":sum(map(abs,path))}


def reset_graph(safe, events=None):
    # Supported reset is deliberately granted. Show whether held OPEN can repeat.
    state="ready"; packets=0; trace=[]
    for event in (events if events is not None else ["open","trip","seat","reset"]*5):
        if state=="ready" and event=="open": state="moving"; packets+=1
        elif state=="moving" and event=="trip": state="spent"
        elif state=="spent" and event=="seat": state="supported"
        elif state=="supported" and event=="reset" and not safe: state="ready"
        elif state=="supported" and event=="close": state="ready"
        trace.append(state)
    # Safe requires actual CLOSE + seated support before resetting; held OPEN
    # never supplies CLOSE. This is a logical requirement, not built hardware.
    return {"packets_with_held_open":packets,"final":state,"trace":trace}


def heads(cycle):
    return next(h for h in range(1,6401) if 6+math.ceil(6400/h)*cycle<30)


def main():
    s=Section(); report={}
    report["geometry_convergence"]=[sweep(s,n) for n in (8,32,128)]
    assert solid_overlap(s,1.2+0.05,1)>0 # catch face, not an ideal state flag
    assert solid_overlap(s,0,-1)>0 # insertion into web blocks yoke
    unions=[max(b,d)-min(a,c) for a,b in s.intervals(0)
            for c,d in s.intervals(1) if max(a,c)<=min(b,d)]
    assert math.isclose(max(unions),4.4)
    report["single_monotone_switch_span_mm"]=max(unions)
    report["penetration_witness_mm3"]=solid_overlap(s,1.25,1)
    # Check every feasible sampled fixed-yoke failure phase over one periodic cell.
    count=0
    for i in range(81):
        h=i*.05
        for j in range(41):
            q=-1+j*.05
            if s.allowed(h,q):
                assert solid_overlap(s,h,q)<1e-8
                lo,hi=s.cell(h,q)
                assert hi-lo<=2.4+1e-9
                assert max(s.depths(q))>=.6-1e-9
                count+=1
    report["arbitrary_phase_samples"]=count
    # Continuous certificate: depth_A + depth_B=2d, max >=d. At least one
    # finite window confines h if the rigid yoke and walls remain intact.
    # Axial errors: each row width changes by +/-e; each bolt thickness +/-e;
    # relative row phase +/-e. Corner counts are not probabilities.
    report["dimensional_boxes"]=[]
    for e in (0,.025,.05,.1,.15):
        margins=[]; spans=[]
        for wa,wb,ba,bb,phase in itertools.product((-1,1),repeat=5):
            aa=(3.2+wa*e-(.8+ba*e))/2
            ab=(3.2+wb*e-(.8+bb*e))/2
            margins.append(aa+ab-2-abs(phase*e))
            spans.extend((2*aa,2*ab))
        report["dimensional_boxes"].append({"e_mm":e,"worst_handoff_margin_mm":min(margins),
                   "negative_corners":sum(m< -1e-9 for m in margins),"corners":32,
                   "max_free_span_mm":max(spans),
                   "min_engagement_mm_with_common_recession":.6-e})
    report["meters"]={mode:{name:permission(path,mode) for name,path in
                          {"reverse":[-.1]*100,"oscillate":[.1,-.1]*100,
                           "dwell_then_move":[0]*100+[.1]*21}.items()}
                      for mode in ("signed","positive","absolute")}
    report["reset"]={"output_seat_refresh":reset_graph(False),"close_edge_gate":reset_graph(True)}
    assert reset_graph(True,["open","close","open"])["packets_with_held_open"]==1
    assert reset_graph(True,["open","trip","seat","close","open"])["packets_with_held_open"]==2
    # Under a cycling shared yoke, a free gravity-loaded output reaches each next
    # end then is released again: these are all geometrically reachable seats.
    h=1.2; q=1.; seats=[h]
    for _ in range(20):
        assert s.allowed(h,-q)
        q=-q; h=s.cell(h,q)[1]; seats.append(h)
    report["shared_refresh_free_output"]={"packets":20,"travel_mm":h-seats[0],"seats_mm":seats}
    report["one_unfinished_switch_arrest"]=energy_bound(1.1,.1,10,.0044,1e5)
    report["arrest_examples"]=[]
    for k,stored in itertools.product((1e4,1e5,1e6),(0.,.05,.5)):
        report["arrest_examples"].append({"k_N_m":k,"stored_J":stored,
                                        **energy_bound(1.1,.1,10,.0024,k,stored)})
    report["energy_box"]={}
    bounds=[energy_bound(m,v,f,d,k,stored) for m,v,f,d,k,stored in itertools.product(
        (.05,1.1,4.1),(0.,.1),(.02,10.),(.0024,.0026,.0044,.0047),(1e4,1e5,1e6),(0.,.05,.5))]
    report["energy_box"]={"cases":len(bounds),"max_excursion_mm":max(b["excursion_mm"] for b in bounds),
                          "max_peak_N":max(b["peak_N"] for b in bounds)}
    # Independent contact numerical convergence and static/frictionless limits.
    e=.5*1.1*.1**2+10*.0024
    vin=math.sqrt(2*e/1.1)
    exact=energy_bound(1.1,.1,10,.0024,1e5)["compression_mm"]
    report["contact_convergence"]=[{"dt_s":dt,"compression_mm":1000*contact_integral(1.1,vin,10,1e5,dt)}
                                    for dt in (2e-4,1e-4,5e-5)]
    assert abs(report["contact_convergence"][-1]["compression_mm"]-exact)<.0001
    for b in bounds:
        assert b["excursion_mm"]>=b["compression_mm"]
    assert math.isclose(energy_bound(1,.1,0,0,1000)["compression_mm"],math.sqrt(.01/1000)*1000)
    # Boundary root energy balance, independently evaluate every combination.
    for m,v,f,d,k,stored in itertools.product((.05,1.1,4.1),(0.,.1),(.02,10.),(.0024,.0026,.0044,.0047),(1e4,1e5,1e6),(0.,.05,.5)):
        b=energy_bound(m,v,f,d,k,stored); x=b["compression_mm"]/1000
        assert abs(k*x*x/2-f*x-b["incident_J"])<1e-12
    report["schedule"]=[]
    for rearm in (0,.005,.01,.02,.05):
        cycle=.45+21*rearm
        h=heads(cycle)
        report["schedule"].append({"packet_overhead_s":rearm,"heads":h,"T_80_heads_s":6+80*cycle,
                                  "purchase_per_head_with_250_reserve_USD":250/h})
    report["rearm_work_box"]=[{"mu":mu,"load_N":f,"work_per_withdrawal_J":mu*f*.002,
                              "work_134400_withdrawals_J":134400*mu*f*.002}
                             for mu,f in itertools.product((.02,.1,.3),(.02,10.))]
    print(json.dumps(report,indent=2))


if __name__=="__main__": main()
