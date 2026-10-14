#!/usr/bin/env python3
"""Whole-body process scenarios, not measured rates or a mold-release pass."""
import json
from math import ceil, isclose

BODY_MM3 = 3118.742 + 1002.089 + 1.90 / 1.024  # E-277 90-degree nut delta

def screen(n=1024, usable=1., cavities=16, shared=False, cure_min=30,
           touch_s=10, batch_s=120, setup_h=8, install_h=10.94):
    assert n > 0 and 0 < usable <= 1 and cavities > 0
    batches = ceil(n / usable / cavities)
    attempts = batches * cavities  # complete lots; final surplus charged
    # Manual: remove threaded core, reset core, demold, trim, gauge.
    # Shared: two core operations become a gang mechanism; other three remain.
    touches = 3 if shared else 5
    operator_s = batches * batch_s + attempts * touches * touch_s
    # 10-mm thread at lead 3, 60rpm assumed; out + return.
    gang_machine_s = batches * (2 * 10 / 3) if shared else 0
    # Core work/demold in-tool; finishing/gauging outside mold, paid in operator time.
    in_tool_touches = 1 if shared else 3
    occupied_s = batches * (cure_min * 60 + batch_s) + attempts * in_tool_touches * touch_s + gang_machine_s
    return dict(cells=n, usable=usable, cavities=cavities, shared_core=shared,
        batches=batches, attempts=attempts, core_turns=2*10/3*attempts,
        joins=0, resident_parts=2*n, hands_on_h=setup_h + install_h + operator_s/3600,
        mold_occupancy_h=occupied_s/3600, retained_bare_screw_print_h=n*640/3/3600,
        removed_body_print_h=n*(4057+1571)/3/3600,
        net_body_l=n*BODY_MM3/1e6, mixed_resin_l=attempts*BODY_MM3/1e6*1.5)

def checks():
    a=screen(); b=screen(shared=True)
    assert isclose(a['hands_on_h']-b['hands_on_h'],1024*20/3600)
    assert isclose(a['hands_on_h'],8+10.94+(64*120+1024*50)/3600)
    assert isclose(a['mold_occupancy_h'],64*(30+2+16*30/60)/60)
    assert screen(n=17)['attempts']==32
    assert screen(usable=.8)['attempts']==1280
    assert screen(cavities=32)['hands_on_h'] < a['hands_on_h']
    assert screen(cure_min=60)['hands_on_h']==a['hands_on_h']
    assert screen(cure_min=60)['mold_occupancy_h'] > a['mold_occupancy_h']
    assert screen(usable=.8)['hands_on_h'] > a['hands_on_h']
    # Fixed resin stock and no extra service claim from removing the joint.
    assert isclose(a['removed_body_print_h'],533.6177777777777)
    # A 32h target: residual per-attempt handling excludes setup/install/shared work.
    residual=(32-8-10.94-64*120/3600)*3600/1024
    assert isclose(8+10.94+64*120/3600+1024*residual/3600,32)
    return residual

if __name__=='__main__':
    residual=checks()
    rows=[]
    for n in [1024,4096,6400]:
        for shared in [False,True]:
            for usable in [1.,.8]:
                lo=screen(n,usable,shared=shared,install_h=10.94*n/1024)
                hi=screen(n,usable,shared=shared,touch_s=30,batch_s=300,setup_h=16,install_h=23.69*n/1024)
                rows.append(dict(n=n,shared=shared,usable=usable,
                    maker_h=[lo['hands_on_h'],hi['hands_on_h']],
                    mold_h=[lo['mold_occupancy_h'],hi['mold_occupancy_h']],
                    mixed_l=lo['mixed_resin_l']))
    # Four-head hardware allocation from E-283, excluding stock/tooling.
    hardware=[797.68,1768.23]
    budgets=[dict(total_usd=cap,body_tool_and_process_usd=cap-hardware[0],
                  per_body_usd=(cap-hardware[0])/1024) for cap in [500,1000,1500]]
    print(json.dumps(dict(body_mm3=BODY_MM3,nominal=screen(),rows=rows,
        residual_seconds_all_individual_duties_at_32h=residual,
        optimistic_budget_ceiling=budgets,
        resin_only_usd=[screen()['mixed_resin_l']*1.05*p for p in [30,80]],
        gang_setup_extra_hour_ceiling=1024*20/3600),indent=2))
