#!/usr/bin/env python3
"""Necessary production/section bounds, not a forming or hardware simulation.

All process times, material prices, thickness and elastic moduli are scenarios.
E-282 records sourced process cautions and inherited actual slicer totals.
No third-party dependencies. stdout is reproducible scratch output.
"""
import json
import math

W, T, L, LAP = 10.3, .5, 124., 3.
# Square median-line development; ideal sharp bends, no springback allowance.
BLANK = 4*(W-T)+LAP


def guide(bump):
    # E-277: unchanged minimum width; an outward seam widens required aperture.
    g = W+.5+.1+bump
    minimum = W-.1
    envelope = g+.2+2*52*(g-minimum+.2)/82
    return 12.7-envelope


def section():
    a = (W-T)**2
    j_closed = (W-T)**3*T
    j_slit = 4*(W-T)*T**3/3
    return dict(blank_width_mm=BLANK, cavity_min_at_inward_lap_mm=W-3*T-.2032,
                ideal_ring_area_mm2=W**2-(W-2*T)**2,
                ideal_closed_J_mm4=j_closed, slit_J_mm4=j_slit,
                ratio=j_closed/j_slit,
                guide_separation_mm={str(b):guide(b) for b in (0,.2032,.5,.7032)},
                bump_exhausting_bound_mm=guide(0)/(1+104/82),
                seam_shear_MPa_at_5Nmm=5/(2*a*LAP),
                twist_deg_at_1Nmm_54mm_G200={
                    'closed':math.degrees(54/(200*j_closed)),
                    'slit':math.degrees(54/(200*j_slit))})


def packing():
    # 1m x .5m sheet, 10mm edge margin, 2mm interblank clearance.
    candidates=[]
    for a,b in ((L,BLANK),(BLANK,L)):
        nx=math.floor((980+2)/(a+2)); ny=math.floor((480+2)/(b+2))
        candidates.append((nx*ny,nx,ny,a,b))
    return max(candidates)


def ledger(n):
    per_sheet=packing()[0]; sheets=math.ceil(n/per_sheet)
    # Actual E-277/E-279 three-copy comparison slices, NOT production forecasts.
    channel_h=n*4057/3/3600
    nut_shank_h=n*(1571+640)/3/3600
    # E-276 four-output installation base, scaled resident work plus shared setup.
    # Read directly from canonical executable source through import below.
    import importlib.util
    from pathlib import Path
    path=Path(__file__).resolve().parents[1]/'E-276/coarse.py'
    spec=importlib.util.spec_from_file_location('coarse',path)
    c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
    base=c.d.cost(int(math.isqrt(n)),4)
    labor=[]
    for j,seconds in enumerate((5,15)):
        # Blank handling; 3 corner folds; seam close; cap join; nut join; gauge.
        # Gang cutting is NOT included in these eight manual operations.
        extra=8*n*seconds/3600
        setup=(4,12)[j]
        labor.append(base['maker_hours'][j]+extra+setup)
    room_s=[(32-base['maker_hours'][j]-(4,12)[j])*3600/n for j in (0,1)]
    return dict(sites=n,per_sheet=per_sheet,sheets=sheets,bought_sheet_m2=sheets*.5,
                net_shell_L=n*BLANK*L*T/1e6,
                purchased_sheet_L=sheets*.5*T,
                seam_m=n*L/1000,joins=3*n,manual_operations=8*n,
                eliminated_channel_print_h=channel_h,
                retained_nut_bare_shank_print_h=nut_shank_h,
                print_h_with_cap_seconds={str(t):nut_shank_h+n*t/3600 for t in (0,60,180)},
                base_maker_h=base['maker_hours'],manual_maker_h=labor,
                seconds_per_body_remaining_within32h=room_s,
                material_USD_allocation=[sheets*.5*p for p in (5,20)],
                tooling_USD_allocation=[100,500],
                four_output_bought_USD=[base['bought_USD'][j]+sheets*.5*(5,20)[j]+(100,500)[j]
                                          for j in (0,1)])


def cure(seats, seconds=60, n=1024):
    batches=math.ceil(n/seats)
    # Conservative adhesive seam example: fill fixture, wait 3h, unload next cycle.
    # Cure begins per part but no staggered release is credited. Does not count ends.
    occupancy=(n*seconds+batches*3*3600)/3600
    return dict(seats=seats,batches=batches,station_occupancy_h=occupancy,
                steady_seats_needed=math.ceil(3*3600/seconds))


def checks():
    count,nx,ny,a,b=packing()
    # Independently enumerate finite blank rectangles and check no sheet escape.
    boxes=[(10+i*(a+2),10+j*(b+2),10+i*(a+2)+a,10+j*(b+2)+b)
           for i in range(nx) for j in range(ny)]
    assert len(boxes)==count==70
    for x,y,xx,yy in boxes: assert x>=10 and y>=10 and xx<=990 and yy<=490
    for i,p in enumerate(boxes):
        for q in boxes[i+1:]:
            assert p[2]<=q[0] or q[2]<=p[0] or p[3]<=q[1] or q[3]<=p[1]
    assert math.isclose(W**2-(W-2*T)**2,4*(W-T)*T)
    s=section(); assert s['ratio']>280 and guide(0)>0 and guide(.5)<0
    assert abs(guide(s['bump_exhausting_bound_mm']))<1e-12
    for n in (1024,4096,6400):
        d=ledger(n)
        assert d['sheets']*count>=n>(d['sheets']-1)*count
        assert d['purchased_sheet_L']>d['net_shell_L']
        # Independent layer-volume identity: developed blank = ring + lap.
        assert math.isclose(d['net_shell_L'],n*(W**2-(W-2*T)**2+LAP*T)*L/1e6)
        assert math.isclose(d['print_h_with_cap_seconds']['180']-
                            d['print_h_with_cap_seconds']['0'],n/20)
    # Inventory-limited cure witness matches explicitly enumerated batches.
    assert cure(16)['batches']==64 and cure(16)['steady_seats_needed']==180
    assert cure(1024)['station_occupancy_h']<cure(16)['station_occupancy_h']


if __name__=='__main__':
    checks()
    print(json.dumps(dict(section=section(),packing=packing(),
                          ledgers=[ledger(n) for n in (1024,4096,6400)],
                          cure=[cure(k) for k in (16,64,256,1024)]),indent=2))
