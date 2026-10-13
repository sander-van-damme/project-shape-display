#!/usr/bin/env python3
"""Conditional production accounting; no measured yields, labor or process priors.

Run directly for compact JSON; --check runs analytical/exhaustive checks only.
Batch model: independent lots draw latent good/bad class, then cell defects are
independent conditional on that class. Persistent retries KEEP their class.
"""
import argparse
import itertools
import json
import math

CLASSES = ((0.9, 0.005), (0.1, 0.05))  # labelled sensitivity case, NOT an FDM prior


def mean_defect(classes):
    assert math.isclose(sum(w for w, _ in classes), 1)
    assert all(w >= 0 and 0 <= p < 1 for w, p in classes)
    return sum(w * p for w, p in classes)


def module_stats(size, classes=CLASSES):
    assert size > 0
    mean = mean_defect(classes)
    clean = sum(w * (1-p)**size for w, p in classes)
    return dict(size=size, mean_defect=mean, clean=clean,
                iid_same_mean_clean=(1-mean)**size,
                fresh_lot_attempts=1/clean,
                persistent_class_attempts=sum(w/(1-p)**size for w, p in classes),
                individual_good_part_factor=1/(1-mean))


def screen(size, sensitivity, classes=CLASSES):
    """Perfect specificity; defective cells detected independently conditional on p.
    Clean probability conditional on *acceptance*, not unconditional yield.
    No repeat test assumed independent; latent undetectable modes can persist.
    """
    assert 0 <= sensitivity <= 1
    accepted = sum(w * (1-p*sensitivity)**size for w, p in classes)
    clean = sum(w * (1-p)**size for w, p in classes)
    return dict(accepted=accepted, clean_given_accepted=clean/accepted)


def fixture_seconds(stroke, neutral, lead=3, rpm=300, hold=30, overhead=12):
    # Start at bottom; bottom -> top -> bottom -> neutral, then hold.
    assert 0 <= neutral <= stroke and lead > 0 and rpm > 0
    return (2*stroke+neutral)/lead/(rpm/60) + hold + overhead


def labor(n, touch_s, module_size=64, setup_h=8, closure_s=120,
          rework_s=120, defect=0.0095):
    # Touch includes loading/start/inspection/install. Setup includes fixture
    # setup but NOT development; print cleanup, electronics etc remain separate.
    module_count = math.ceil(n/module_size)
    fixed_h = setup_h + module_count*closure_s/3600 + n*defect*rework_s/3600
    return dict(total_maker_h=fixed_h+n*touch_s/3600, fixed_h=fixed_h,
                touch_ceiling_16h=(16-fixed_h)*3600/n,
                touch_ceiling_32h=(32-fixed_h)*3600/n,
                expected_one_pass_bad_pairs=n*defect)


def board(n, stroke, neutral):
    # Fixture supports 16 complete pairs, not 16 serially tested sites.
    cycle = fixture_seconds(stroke, neutral)
    reserve = 250 + 2*55
    drive_subset = 2*math.isqrt(n)*4.24
    return dict(cells=n, stroke=stroke, neutral=neutral,
                threaded_length_min=stroke+10,  # BEFORE end/runout margins
                fixture_serial_h=n*cycle/3600,
                fixture_16_h=math.ceil(n/16)*cycle/3600,
                manual= labor(n,17), fixture_assisted=labor(n,8),
                extra_minute_per_pair_h=n/60,
                residual_faults_at_95pct_detection=n*0.0095*0.05,
                detection_for_union_bound_95pct=1-0.05/(n*0.0095),
                resident_budget_500=(500-reserve-drive_subset)/n,
                resident_budget_1000=(1000-reserve-drive_subset)/n,
                resident_budget_1500=(1500-reserve-drive_subset)/n)


def checks():
    # Exhaustive Bernoulli outcomes for each latent class reconstruct the mixture.
    cases = 0
    for m in range(1,9):
        for sensitivity in (0,0.5,0.95,1):
            clean = accepted = 0
            for w,p in CLASSES:
                for bits in itertools.product((0,1), repeat=m):
                    k=sum(bits); prob=w*p**k*(1-p)**(m-k)
                    clean += prob*(k == 0)
                    accepted += prob*(1-sensitivity)**k
            result=screen(m,sensitivity)
            assert math.isclose(result['accepted'], accepted, abs_tol=1e-12)
            assert math.isclose(result['clean_given_accepted'], clean/accepted, abs_tol=1e-12)
            cases += 1
        stats=module_stats(m)
        assert stats['clean'] >= stats['iid_same_mean_clean'] - 1e-12
        assert stats['persistent_class_attempts'] >= stats['fresh_lot_attempts'] - 1e-12
    assert module_stats(64, ((1,0),))['fresh_lot_attempts'] == 1
    assert screen(64,1)['clean_given_accepted'] == 1
    assert math.isclose(screen(64,0)['clean_given_accepted'],module_stats(64)['clean'])
    assert math.isclose(fixture_seconds(40,20),48+2/3)
    assert math.isclose(fixture_seconds(50,30),50+2/3)
    for n in (4096,6400):
        assert math.isclose(labor(n,8)['total_maker_h']-labor(n,0)['total_maker_h'], n*8/3600)
        assert math.isclose(labor(n,17)['total_maker_h']-labor(n,8)['total_maker_h'], n*9/3600)
        assert math.isclose(board(n,50,30)['fixture_serial_h']/board(n,50,30)['fixture_16_h'],16)
        # Board budget must exactly reconcile, replacing the old $.02 resident allowance.
        allowance=board(n,50,30)['resident_budget_1500']
        assert math.isclose(360+2*math.isqrt(n)*4.24+n*allowance,1500)
    # Deterministic hostile batch: every cell can fail together. Mean alone
    # cannot justify iid risk, even though expected defect count is unchanged.
    assert math.isclose(sum(w*p for w,p in CLASSES),.0095)
    return {'exhaustive_mixture_checks':cases,'other_checks':'passed'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    verified=checks()
    if args.check:
        print(json.dumps(verified));return
    result=dict(evidence='conditional calculations; all labor/yield inputs assumed',
                classes=CLASSES,checks=verified,
                modules=[module_stats(m) for m in (16,64,256)],
                screening={str(s):screen(64,s) for s in (0.9,0.95,0.99,1)},
                boards=[board(n,t,z) for n in (4096,6400) for t,z in ((40,20),(50,30))],
                bad_class_sample_miss={str(k):.95**k for k in (8,32,59)},
                thread_core_turns=10/3,
                core_release_hours_1rev_s={str(n):n*10/3/3600 for n in (4096,6400)})
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
