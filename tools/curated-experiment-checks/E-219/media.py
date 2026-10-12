"""E-219: necessary packing/inventory bounds, not hardware qualification.
All dimensions, speeds and error boxes are explicit assumptions. Stdlib only.
"""
import itertools as it
import json
import math

PITCH = 5.08
HEIGHTS = (0, 10, 20, 30, 40)
N = 6400
ROW = 80


def move(d, a=2000, v=200):
    return 2*math.sqrt(d/a) if d <= v*v/a else d/v+v/a


def wheel(e, levels=5, w=1.6, length=2, lane_centres=2.4):
    # Vertical-axis circular five-sector block, with a horizontal land in each
    # sector. Bearing rectangle enlarged on every side by the total error bound.
    # Minimum radial position that keeps both inner corners inside one sector.
    W, L = w+2*e, length+2*e
    radius_to_foot = W/2+L/(2*math.tan(math.pi/levels))
    outer = math.hypot(radius_to_foot+W/2,L/2)
    # Two axles outboard of the two foot lanes; bearing lands point inward.
    half_axes = lane_centres/2+radius_to_foot
    def conflict(dx,dy):
        return min(math.hypot(dx*PITCH+s,dy*PITCH)
                   for s in (-2*half_axes,0,2*half_axes)) < 2*outer-1e-10
    # Actual circular bases collide; not merely a rotation-envelope heuristic.
    radius_cells = math.ceil((2*half_axes+2*outer)/PITCH)+1
    offsets = [(x,y) for x in range(-radius_cells,radius_cells+1)
               for y in range(-radius_cells,radius_cells+1)
               if (x or y) and conflict(x,y)]
    # Exhaustive rectangular residue-class deck layouts, mx*my phases. Every
    # within-deck displacement is a multiple of mx,my; test all conflict offsets.
    feasible=[]
    for mx,my in it.product(range(1,17),repeat=2):
        if not any(x%mx==0 and y%my==0 for x,y in offsets):
            feasible.append((mx*my,mx,my))
    best=min(feasible)
    # Independent clique witness: every pair of cells in a rectangle conflicts.
    cliques=[]
    for nx,ny in it.product(range(1,9),repeat=2):
        pts=list(it.product(range(nx),range(ny)))
        if all(conflict(x1-x2,y1-y2) for (x1,y1),(x2,y2) in it.combinations(pts,2)):
            cliques.append((nx*ny,nx,ny))
    clique=max(cliques)
    assert best[0] >= clique[0]
    assert math.isclose(math.atan2(L/2,radius_to_foot-W/2), math.pi/levels)
    return dict(error_mm=e,foot_radius_mm=radius_to_foot,diameter_mm=2*outer,
                pair_axis_separation_mm=2*half_axes,
                own_pair_clearance_mm=2*half_axes-2*outer,
                minimum_lane_centres_mm=2*(outer-radius_to_foot),
                rectangular_decks=best,clique_lower_bound=clique,
                allocated_depth_mm=90*best[0] if half_axes>=outer else None,
                area_lower_bound=math.ceil(2*math.pi*outer**2/PITCH**2),
                # Solid five-sector stock; hub/bearings/carriers omitted.
                media_cm3_at_16_heads=80*96*math.pi*outer**2*24/1000)


def inventory(n=80,rows=80,b=16,levels=5):
    # Complete row replacement, skip unchanged rows; old media retained until
    # target dock proof. Max code k copies: N+(n-1)*b. Witness old all k,
    # target changes one cell per simultaneously serviced row away from k.
    per_code=n*rows+(n-1)*b
    return dict(per_code=per_code,total=levels*per_code,
                installed_and_spare_sockets=n*(rows+b),
                solid_cm3=per_code*1.6*2*sum(4+h for h in HEIGHTS)/1000)


def inventory_check():
    # Independent exhaustive two-row/two-level state enumeration, B=1 and 2.
    # At takeover both old boards and all changed target rows coexist.
    n,rows=3,2
    for b in (1,2):
        found=0
        for old,new in it.product(it.product((0,1),repeat=n*rows),repeat=2):
            changed=[r for r in range(rows) if old[r*n:(r+1)*n]!=new[r*n:(r+1)*n]]
            for k in range(2):
                incoming=sorted((new[r*n:(r+1)*n].count(k) for r in changed),reverse=True)[:b]
                found=max(found,old.count(k)+sum(incoming))
        assert found==n*rows+(n-1)*b


def handling(a):
    # A captured fork removes a vertical block fully from its sleeve, places it
    # into a sorted vertical magazine, picks target, inserts into the empty slot.
    # Old withdrawal + magazine insertion; new extraction + socket insertion.
    # At least 1 mm clearance each stroke. Lateral moves, gates, registration,
    # sorting decision, readers and fork resets are omitted from this lower bound.
    return max((2*move(5+o,a)+2*move(5+n,a),o,n)
               for o,n in it.product(HEIGHTS,repeat=2) if o!=n)


def schedule(b,q,a,arrest='continuous',aux=.5):
    # q forks per bank. Reuse E-218 loaded exchange obligations, but not its
    # slider programming. Absolute selected stock; no free premade target map.
    programming=math.ceil(ROW/q)*(handling(a)[0]+.02)
    programming+=(math.ceil(ROW/q)-1)*move(PITCH,a)
    vertical=4*move(45,a) if arrest=='continuous' else 90*(move(1,a)+.001)+2*move(45,a)
    row=programming+vertical+2*move(2.4,a)+move(PITCH,a)+aux
    return 2+(math.ceil(ROW/b)+1)*row


def main():
    inventory_check()
    assert math.isclose(move(40),.3)
    assert wheel(0)['rectangular_decks'][0]==6
    assert wheel(0)['clique_lower_bound'][0]==6
    assert inventory()['total']==38320
    results=[]
    for a,arrest,b in it.product((2000,8000),('continuous','indexed'),(1,2,4,8,16)):
        passing=[q for q in (1,2,4,8,16,40,80) if schedule(b,q,a,arrest)<30]
        if passing:
            q=min(passing)
            results.append(dict(a=a,arrest=arrest,b=b,q=q,lanes=b*q,seconds=schedule(b,q,a,arrest)))
    inv=inventory()
    print(json.dumps(dict(
        evidence='geometry, exact inventory enumeration, assumed schedule bounds; no physical data',
        wheels=[wheel(e) for e in (0,.15,.35,.7)],
        inventory=inv,
        print_hours={str(rate):inv['solid_cm3']*1000/rate/3600 for rate in (5,15)},
        sorting_hours={str(t):inv['total']*t/3600 for t in (5,10)},
        handling_worst={str(a):handling(a) for a in (2000,8000)},
        optimistic_schedules=results,
        auxiliary_sensitivity={str(aux):schedule(16,40,8000,aux=aux) for aux in (.25,.5,1,2)},
        euler_pinned_N={str(E):math.pi**2*E*(2*1.6**3/12)/44**2 for E in (1000,3000)},
    ),indent=2))

if __name__=='__main__': main()
