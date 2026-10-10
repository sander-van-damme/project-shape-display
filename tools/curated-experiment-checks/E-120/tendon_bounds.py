#!/usr/bin/env python3
"""Deterministic necessary routing/drive bounds; mm, N, seconds, USD.
No process prior, cable material model, finite pulley, lock or machine pass.
"""
from itertools import combinations, product
from math import ceil, isclose, pi
import json

N = 80
P = 5.08
TRAVEL = 40.


def box_gap(a, b):
    # Largest separating projection. Negative means positive-volume overlap.
    return max(max(x[0]-y[1], y[0]-x[1]) for x, y in zip(a,b))


def routes(diameter, clearance, common=0.):
    lane = diameter+clearance
    r = diameter/2
    result = []
    # One row suffices: other rows differ only by y>=5.08 > corridor diameter.
    for side, j in product((-1,1), range(N//2)):
        x = (j+.5)*P if side == -1 else N*P-(j+.5)*P
        end = 0. if side == -1 else N*P
        z = common-(j+.5)*lane
        vertical = ((x-r,x+r),(-r,r),(z-r,common+r))
        horizontal = ((min(x,end)-r,max(x,end)+r),(-r,r),(z-r,z+r))
        result.append((vertical,horizontal))
    return result


def main():
    routing=[]
    for diameter, clearance in product((.6,1.,1.4),(.1,.2,.4)):
        rs=routes(diameter,clearance)
        gap=min(box_gap(a,b) for ra,rb in combinations(rs,2) for a in ra for b in rb)
        shifted=routes(diameter,clearance,123.)
        gap2=min(box_gap(a,b) for ra,rb in combinations(shifted,2) for a in ra for b in rb)
        assert isclose(gap,clearance,abs_tol=1e-10)
        assert isclose(gap,gap2,abs_tol=1e-10)
        assert diameter < P
        # Equal lengths for 80 repeated rows and mirrored halves. Includes only
        # under-map Manhattan centerlines, not tails, winding, terminations.
        horizontal=sum((j+.5)*P for j in range(40))*2*N
        vertical=sum((j+.5)*(diameter+clearance) for j in range(40))*2*N
        assert isclose(horizontal, N*N*N*P/4)
        assert isclose(vertical,N*N*N*(diameter+clearance)/4)
        length_m=(horizontal+vertical)/1000
        for e in (.05,.1,.2):
            corner_gaps=[clearance+a-b-width for a,b,width in product((-e,e),repeat=3)]
            assert isclose(min(corner_gaps),clearance-3*e,abs_tol=1e-10)
        routing.append(dict(corridor_mm=diameter,clearance_mm=clearance,
                            depth_mm=39.5*(diameter+clearance)+diameter/2,
                            corridor_gap_mm=gap,centerline_length_m=length_m,
                            cable_only_usd_per_m_ceiling=250/length_m,
                            error_box_margins={e:clearance-3*e for e in (.05,.1,.2)}))
    drums=[]
    for turns in (1,2,4,8):
        radius=TRAVEL/(2*pi*turns)
        outer=2*radius+3. # 1.5 mm assumed radial rim/structure allowance
        # Regular k-by-k residue coloring of fixed centers. This separates
        # disks within each layer only; cable access/axles/layer passage absent.
        k=ceil(outer/P)
        counts=[sum(1 for x,y in product(range(N),repeat=2) if x%k==i and y%k==j)
                for i,j in product(range(k),repeat=2)]
        assert sum(counts)==6400 and k*P >= outer
        assert isclose(2*pi*radius*turns,TRAVEL)
        # Full travel at every site. Per-head overhead includes all engagement,
        # locking, proof and disengagement; map overhead reserves 4 s. These
        # are necessary service-time offers, omit transport and retries.
        rates=[]
        for heads, overhead in product((80,160,320),(.05,.1)):
            available=(30.-4.)/(6400/heads)-overhead
            rates.append(dict(heads=heads,overhead_s=overhead,
                              minimum_rpm=60*turns/available if available>0 else None))
        drums.append(dict(turns=turns,effective_radius_mm=radius,outer_diameter_mm=outer,
                          disk_only_layers=k*k,largest_layer=max(counts),
                          torque_Nmm_per_N=radius,necessary_rates=rates))
    # A strict <30 target requires speed strictly above reported threshold.
    # Work invariance rejects fictitious energy savings from a small drum.
    for row in drums:
        assert isclose(row['torque_Nmm_per_N']*2*pi*row['turns'],TRAVEL)
    # Independent reconstructable witness: outer path ends at depth .7,
    # next horizontal is at 2.1 for diameter1/clearance.4: gap .4.
    assert isclose(2.1-.5-(.7+.5),.4)
    print(json.dumps(dict(evidence='necessary bounds and ideal routing corridors; self-review',
                          routing=routing,drums=drums,
                          repeated=dict(tendons=6400,ends=12800,drums=6400,
                                        local_locks=6400),
                          bought_budget=dict(reserve_usd=250,
                              all_cell_items_ceiling_usd=250/6400,
                              heads320_ceiling_if_no_cell_purchases_usd=250/320)),indent=2))


if __name__=='__main__':
    main()
