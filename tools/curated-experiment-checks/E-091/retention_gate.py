"""E-091: finite sign apertures/stop tongues and square-key command retention.
mm, N. Deterministic rigid geometry + bounded uncertainty, not manufacturing
statistics, a dynamic solver, a complete setter, or hardware qualification.
"""
import importlib.util
import itertools as it
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location('trip', Path(__file__).resolve().parents[1] / 'E-090/finite_trip.py')
trip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trip)
EPS = 1e-8
LEVELS = (5, 9, 17, 18, 19, 21)


def sign_walls(h, phase, edge_lo=0., edge_hi=0.):
    """Two distinct lanes; phase + reads the negative window on the cursor."""
    p = 40 / (h-1)
    lo, hi = (-41.1, -p+1.1) if phase == 1 else (p-1.1, 41.1)
    lo, hi = lo+edge_lo, hi+edge_hi
    return [trip.rectangle(-42, lo, 0, 1), trip.rectangle(hi, 42, 0, 1)]


def contact_depth(x, width, walls):
    def hit(d):
        return any(trip.overlap(trip.probe(x, d, width), wall) for wall in walls)
    if not hit(1.5):
        return 1.5
    lo, hi = 0., 1.5
    for _ in range(36):
        mid = (lo+hi)/2
        if hit(mid): hi = mid
        else: lo = mid
    return lo


def tongue_blocks(depth, overlap=.8):
    # Output lug translates horizontally across x=0..1. Sign plunger withdraws
    # the integral stop tongue perpendicular to that path. No friction credited.
    tongue = trip.rectangle(0, 1, -2-depth, overlap-depth)
    # Positive collision at x=.5 suffices to block the required full stroke.
    lug = trip.rectangle(.1, .9, 0, 1)
    return trip.overlap(tongue, lug)


def sign_screen():
    count = 0
    reserve = float('inf')
    for h in LEVELS:
        p = 40/(h-1)
        for q, phase, datum, width, el, eh in it.product(range(1-h, h), (-1, 1),
                (-.65, .65), (.3, .5), (-.1, .1), (-.1, .1)):
            walls = sign_walls(h, phase, el, eh)
            x = -q*p+datum
            depth = contact_depth(x, width, walls)
            allowed = q*phase > 0
            assert (depth >= 1.5-EPS) == allowed, (h,q,phase,x,depth)
            # Two independent depth/stop placement bounds. Both can be common
            # to an entire bank. Check the actual stop/lug rectangles.
            for depth_error, stop_error in it.product((-.1,.1), repeat=2):
                assert tongue_blocks(depth+depth_error,.8+stop_error) != allowed
            if allowed:
                lo, hi = walls[0][1][0], walls[1][0][0]
                reserve = min(reserve, x-width/2-lo, hi-x-width/2)
            count += 1
    # Return bar limits sign travel to .3 +/- .1 mm; an additional .1 depth
    # error still cannot withdraw the shortest (.7) stop tongue.
    assert tongue_blocks(.3+.1+.1, .8-.1)
    # Missing tongue exposes E-090's finite-face bypass regardless of equality.
    assert trip.depth_polygon(80., .4, 2.4, 39.05) == 1.5
    assert tongue_blocks(0.)
    # All sign pins clear the cursor after a phase: insertion -0.2 +/- .1 is wholly
    # outside cursor plates. Command motion then has no pin/plate intersection.
    for d in (-.3, -.1):
        assert all(not trip.overlap(trip.probe(0,d,.5), w)
                   for w in sign_walls(21,1))
    return dict(state_error_cases=count,stop_lug_cases=count*4,
                least_target_edge_reserve_mm=round(reserve,6),
                body_length_mm=84,command_stroke_mm=80,swept_length_mm=164)


def rack_walls(h, width):
    p = 40/(h-1)
    holes = [(k*p-width/2,k*p+width/2) for k in range(1-h,h)]
    ends = [-42]+[v for hole in holes for v in hole]+[42]
    return [trip.rectangle(a,b,0,1) for a,b in zip(ends[::2],ends[1::2])]


def dog_collision(cursor, depth, dog_width, walls):
    dog = trip.rectangle(-dog_width/2,dog_width/2,depth-3,depth)
    return any(trip.overlap(dog,[(x+cursor,y) for x,y in wall]) for wall in walls)


def retention_screen():
    count = transition_count = 0
    # Generated square slots W=1.3+/-0.1; square dog D=.6+/-0.1.
    # Setter error relative to the actual slot is an interface assumption .2.
    for h in LEVELS:
        p = 40/(h-1)
        for q,w,d,set_error in it.product(range(1-h,h),(1.2,1.4),(.5,.7),(-.2,.2)):
            walls=rack_walls(h,w)
            assert not dog_collision(-q*p+set_error,1.5,d,walls)
            # Collision at either beyond-clearance position confirms positive
            # restraint. The separate collar/keeper section below retains depth.
            clearance=(w-d)/2
            for side in (-1,1):
                assert dog_collision(-q*p+side*(clearance+.01),1.5,d,walls)
            count+=1
        # Every old/new command transition clears the rack if the whole dog
        # is below y=0. The swept rectangle is a geometric holdout independent
        # of endpoint state fitting; every wall remains at y in [0,1].
        for old,new in it.product(range(1-h,h), repeat=2):
            sweep=trip.rectangle(min(old,new)*p-.35,max(old,new)*p+.35,-3.1,-.1)
            assert all(not trip.overlap(sweep,w) for w in rack_walls(h,1.4))
            transition_count+=1
        # Two valid indexed endpoints do not prove a valid engaged transition.
        assert not dog_collision(0.,1.5,.6,rack_walls(h,1.3))
        assert not dog_collision(p,1.5,.6,rack_walls(h,1.3))
        assert dog_collision(p/2,1.5,.6,rack_walls(h,1.3))
    # A separate keeper below each dog collar prevents its axial withdrawal.
    # This is a local section of a row keeper, which must itself be positively
    # driven/retained. Fully seated collar y=[-1.9,-1.5], keeper=[-2.4,-2.0].
    # +/-0.1 relative placement permits 0..0.2 free withdrawal; then a hard
    # collision leaves dog insertion >=1.3 mm. The side-entry keeper occupies
    # another lane; its actuator, row bending and neighboring lanes are open.
    for error in (-.1,0.,.1):
        keeper=trip.rectangle(-1,1,-2.4+error,-2.+error)
        collar=lambda retreat: trip.rectangle(-.8,.8,-1.9-retreat,-1.5-retreat)
        assert not trip.overlap(keeper,collar(0.))
        assert trip.overlap(keeper,collar(.21))
    return dict(insertion_cases=count,withdrawn_swept_transitions=transition_count,
                minimum_insertion_reserve_mm=.05,maximum_locked_play_mm=.45,
                residual_registration_bound_mm=.2,composed_datum_bound_mm=.65)


def combined_screen():
    rows=[]
    checks=0
    # Position may drift to either wall after setter disengagement. Square key
    # remains fully inserted in both witnesses, so seating readback is no help.
    for h in LEVELS:
        p=40/(h-1)
        misses=false=0
        for q,r,dw,ds,datum,gain in it.product(range(1-h,h),range(1-h,h),
                (-.1,.1),(-.1,.1),(-.65,.65),(-.01,.01)):
            if q*r<=0: continue  # finite sign gate checked separately
            dx=(r-q)*p+datum+r*p*gain
            depth=trip.depth_reduced(dx,.4+dw,.4+p+ds)
            assert (depth>=1.5-EPS) == (not trip.collision(dx,1.5,.4+dw,.4+p+ds,42))
            misses += q==r and depth<1.5-EPS
            false += q!=r and depth>=1.5-EPS
            checks+=1
        rows.append(dict(levels=h,command_positions=2*h-1,pitch_mm=p,
                         margin_mm=round(p/2-.65-.4-.1,6),
                         target_miss_corners=misses,wrong_full_entry_corners=false))
    assert all(r['target_miss_corners']==r['wrong_full_entry_corners']==0 for r in rows if r['levels']<=18)
    assert all(r['target_miss_corners']>0 and r['wrong_full_entry_corners']>0 for r in rows if r['levels']>18)
    # Specific generated polygon witnesses: q=20,r=20 misses; q=19,r=20
    # inserts fully at the neighboring target. Both are same-sign commands.
    miss=trip.depth_polygon(1.05,.5,2.3,39.3)
    wrong=trip.depth_polygon(.95,.3,2.5,39.3)
    assert miss<.4+EPS and wrong==1.5
    return dict(same_sign_state_error_cases=checks,levels=rows,
                polygon_witness_depths_mm=dict(target=miss,wrong_neighbor=wrong))


def feasibility_frontier():
    # g=W-D. Cmin=g/2-s; Cmax=g/2+s. Capture needs Cmin>=Eset.
    # Thus even at zero capture reserve, Cmax>=Eset+2s. Requiring strict
    # capture reserve makes the bound strictly worse. Slot tuning cannot fix it.
    rows=[]
    for setter,reg,gain in it.product((.05,.1,.2,.4),(.1,.2,.4),(0.,.01)):
        lower_play=setter+2*.1
        best_margin=1-(lower_play+reg+40*gain)-.1
        rows.append(dict(setter_error_mm=setter,registration_mm=reg,gain=gain,
                    best_possible_margin_mm=round(best_margin,6),
                    tunable_with_positive_reserve=best_margin>EPS))
    bad=next(r for r in rows if r['setter_error_mm']==.2 and r['registration_mm']==.2 and r['gain']==.01)
    assert bad['best_possible_margin_mm']==-.1
    # Deliberately separate a derived frontier from sampled width candidates.
    for g in (.3,.4,.5,.6,.7,.8,1.):
        capture=g/2-.1-.2
        decode=1-(g/2+.1+.2+.4)-.1
        assert not(capture>EPS and decode>EPS)
    return dict(adverse_best_possible_margin_mm=-.1,
                generated_key_critical_gain_strictly_below=.00625,
                scenarios=rows)


def proof_faults():
    # Common carrier can advance while a sign pin, key or query pin stays
    # behind. These are fault witnesses, not a designed readback system.
    assert tongue_blocks(0.) and not tongue_blocks(1.5)
    walls=rack_walls(21,1.3)
    assert not dog_collision(0,1.5,.6,walls)
    assert dog_collision(1,1.5,.6,walls)  # stuck dog after requested withdrawal
    # A depth-confirmed dog at either clearance endpoint is still fully seated.
    for e in (-.45,.45):
        assert not dog_collision(e,1.5,.5,rack_walls(21,1.4))
    # Reuse E-090 isolator scenarios, not new material/friction priors. One
    # sign bank remains queried during deposition; equality insertion adds a
    # second force contribution. Two all-blocked banks is a conservative upper
    # bound, not necessarily an attainable scheduled state.
    return dict(individual_proofs_required=['sign clearance','key engagement and withdrawal',
                 'query depth and withdrawal','command position after writer release'],
                sign_plus_query_bank800_upper_N=[1600*(f0+k*1.5)
                    for k,f0 in ((.05,.02),(.2,.1),(.8,.1))],
                per_board=dict(sign_pins=12800,query_pins=6400,square_keys=6400,
                               memory_cursors=6400,total_local_sliding_members=32000,
                               independently_compliant_probe_push_paths=19200))


def main():
    print(json.dumps(dict(evidence='bounded rigid contact sections; self-review; no hardware claim',
        sign=sign_screen(),retention=retention_screen(),combined=combined_screen(),
        frontier=feasibility_frontier(),proof=proof_faults()),indent=2))


if __name__=='__main__':main()
