#!/usr/bin/env python3
"""Decision-changing controls: continuous retirement and a scanned retained mask.
These are prospective mechanisms, not hardware implemented by the bench STL.
"""
import json,math,itertools
from system import pv,motion,schedule,cost

def continuous(a,b,banks=4,rpm=850,lead=3):
 n=len(a);p=406.4/n;d=[[v-u for u,v in zip(ar,br)] for ar,br in zip(a,b)]
 if not any(any(r) for r in d):return 0
 times=[]
 for bank in range(banks):
  lo=n*bank//banks;hi=n*(bank+1)//banks;last=lo;t=0;retry=0
  for y in range(lo,hi):
   row=d[y]
   if not any(row):continue
   t+=motion((y-last)*p,150,1500);last=y
   runs=[max((sign*v for v in row if sign*v>0),default=0) for sign in (1,-1)]
   # At-speed individual release; cannot use this until moving-disconnect passes.
   dwell=.20+.25+.15+sum(.15+motion(h/lead,rpm/60,150) for h in runs if h)
   t+=dwell;retry=max(retry,dwell)
  times.append(t+motion((last-lo)*p,150,1500)+retry)
 return 5+max(times)

def main():
 maps,labs=pv.s.v.variants(64);maps,labs=pv.s.connected_walls(maps,labs,64)
 h=pv.aligned(maps,30,30);neutral=[[30]*64 for _ in range(64)]
 states=[neutral]+[h[k] for k in pv.s.SUITES['relief']]
 pairs=list(itertools.permutations(states,2));out=[]
 for banks in (2,4,6,8):
  for rpm in (850,1500):
   out.append(dict(banks=banks,rpm=rpm,
      stopped_loop=max(schedule(a,b,banks=banks,rpm=rpm)['seconds'] for a,b in pairs),
      continuous_retirement=max(continuous(a,b,banks,rpm) for a,b in pairs),
      release_50ms_height_travel_mm=3*rpm/60*.05,
      # 16 writers/head traverse four 16-channel mask sectors at 40 ms/sector;
      # station return/transfer needs another 80 ms. Time is paid at EVERY mask.
      scanned_mask=max(schedule(a,b,banks=banks,rpm=rpm,change=.24)['seconds'] for a,b in pairs),
      servo_bom=cost(64,banks)['cost_usd'],
      mask_unquoted_selector_subtotal=banks*(16*9.35+64*2.5+80)))
 print(json.dumps(dict(evidence='conditional controls, not selected hardware',cases=out),indent=2))
if __name__=='__main__':main()
