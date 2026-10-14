#!/usr/bin/env python3
"""Bounded assembly observations and operation ledger; no hardware/yield claims."""
from itertools import product
from math import ceil, isclose

LEAD = 3.0
# Required measurement/process bounds, not measured printer or sensor accuracy.
LEAD_ERROR, GAIN_ERROR, READ_ERROR, LOST_MOTION = .06, .002, .1, .3


def band(turns):
    return ((LEAD-LEAD_ERROR)*turns*(1-GAIN_ERROR)-2*READ_ERROR-LOST_MOTION*(1+GAIN_ERROR),
            (LEAD+LEAD_ERROR)*turns*(1+GAIN_ERROR)+2*READ_ERROR+LOST_MOTION*(1+GAIN_ERROR))


def trace(lead, gain=0, bias=0, noise=0, lost=0):
    # Direct screw-collar displacement relative to fixed nut; same batch bias
    # cancels within each segment. No commanded Z is substituted for observation.
    result = []
    for turns in (2, 16, -2, 2):
        a = bias - noise
        b = bias + (lead*turns + lost)*(1+gain) + noise
        result.append(abs(b-a))
    return result


def accepts(samples, torque=.7, read_ok=True):
    return read_ok and torque <= 1.5 and all(
        lo-1e-9 <= z <= hi+1e-9
        for z, (lo, hi) in zip(samples, (band(t) for t in (2,16,2,2))))


def check():
    good = list(product((2.94,3,3.06),(-.002,0,.002),(-.15,0,.15),(-.1,0,.1),(-.3,0,.3)))
    for p,g,b,e,l in good:
        assert accepts(trace(p,g,b,e,l))
    jam = trace(.5)
    wrong_lead = trace(2.7)
    damaged_same_lead = trace(3)
    assert not accepts(jam)
    assert band(2)[0] <= wrong_lead[0] <= band(2)[1]
    assert not accepts(wrong_lead)
    assert accepts(damaged_same_lead)  # decisive indistinguishable fault witness
    assert not accepts(trace(3), torque=1.6)
    assert not accepts(trace(3), read_ok=False)
    # An imposed Z feed could generate the good trace with a stripped thread.
    assert accepts(trace(3))
    turns = (64-2)/3
    assert isclose(turns*3,62)
    auto = (turns+4)/2 + 7  #120rpm, reverse proof, seek/dock/read/retract allowance
    print('good corners',len(good),'bands',band(2),band(16))
    print('faults: jam rejected; lead2.7 rejected; same-lead damage ACCEPTED')
    print('insertion turns',turns,'automatic cycle seconds',auto)
    for n in (1024,6400):
        print('N',n,'nominal manual touches',5*n,'fixture touches',4*n)
        for y in (1,.8):
            attempts=ceil(n/y); rejects=attempts-n
            for label,thread in (('manual-fast',5),('manual-mid',15),('manual-slow',30),('fixture',None)):
                extra_setup=4 if thread is None else 0
                hands=10 if thread is None else 9+thread+4
                assembly=extra_setup+(attempts*hands+rejects*60)/3600
                serial=extra_setup+(attempts*(hands+(auto if thread is None else 0))+rejects*60)/3600
                # Common manufacturing handling, install, frame/electrical setup,
                # four channels and two assumed 289-up production streams.
                low=8+4/6+(attempts*20+n*8)/3600+2*ceil(attempts/289)*5/60
                high=16+4*.5+(attempts*60+n*20)/3600+2*ceil(attempts/289)*5/60
                print(y,label,'assembly_h',round(assembly,2),'serial_h',round(serial,2),
                      'whole_maker_h',[round(low+assembly,2),round(high+assembly,2)])
        print('threading break-even seconds',10+4*3600/n-13)
    # Intervals, not prevalence: identical observations defeat every deterministic
    # classifier operating on these channels, irrespective of a timing improvement.
    assert trace(3) == damaged_same_lead

def proof_check():
    """Quasi-static bounded examples, NOT measured strength or proof settings."""
    force, force_error, displacement_error = .4, .02, .04
    def observed_band(k_min, k_max):
        return ((force-force_error)/k_max-displacement_error,
                (force+force_error)/k_min+displacement_error)
    good = observed_band(10,40)
    weak = observed_band(.5,2)
    assert good[1] < weak[0]
    threshold = (good[1]+weak[0])/2
    # Independent corner replay: force/read errors may oppose classification.
    for k,df,dz in product((10,40),(-.02,.02),(-.04,.04)):
        assert (force+df)/k+dz < threshold
    for k,df,dz in product((.5,2),(-.02,.02),(-.04,.04)):
        assert (force+df)/k+dz > threshold
    # At larger read/fixture uncertainty the observation bands overlap.
    assert (force+.02)/10+.08 >= (force-.02)/2-.08
    # Safe fracture-discrimination interval: bad strongest must fail, good
    # weakest must not be damaged, charging force error and transient overshoot.
    def safe_window(bad_max, good_nondamage_min):
        return bad_max+.02, good_nondamage_min-.02-.05
    separated = safe_window(.3,.8)
    overlapping = safe_window(.4,.35)
    assert separated[0] < force < separated[1]
    assert overlapping[0] > overlapping[1]
    # Equal immediate stiffness and slip => equal proof observations, even if
    # an unobserved later creep/durability property differs. No prevalence claim.
    def observations(k, rotation):
        return force/k, force/k+LEAD*rotation/360, rotation
    good_pair = {"k": 20, "rotation": 0, "delayed_failure": False}
    latent_fault = {"k": 20, "rotation": 0, "delayed_failure": True}
    assert good_pair != latent_fault
    assert observations(good_pair["k"], good_pair["rotation"]) == observations(
        latent_fault["k"], latent_fault["rotation"])
    locked, free, angle = observations(20,30)
    assert isclose(free-locked, .25)
    assert angle > 2*2  # +/-2 degree readings on either end: illustrative bound
    travel_error = 2*.1-displacement_error  # E-286 original position-channel difference error
    assert good[1]+travel_error > weak[0]-travel_error
    # Distal contact changes admitted failure observability; finite proof at
    # full insertion cannot cover a damaged zone touched only near extension.
    sampled_z = {2,52}  # S50 endpoints; nut spans [z,z+10] on 64mm thread
    assert all(not z <= 30 <= z+10 for z in sampled_z)
    print('proof displacement bands',good,weak,'threshold',threshold)
    print('proof force windows',separated,overlapping,'N')
    print('locked/free 30-degree example',locked,free,angle)
    for n in (1024,6400):
        for usable in (1,.8):
            attempts=ceil(n/usable)
            # Two static positions require S50 out and back, at assumed120rpm.
            motion=2*50/LEAD/2
            # Per position locked/free load + unload/read: 12s allocation.
            static=24
            print('proof N/y',n,usable,'extra dwell_h',
                  round(attempts*(motion+static)/3600,2),
                  'extra active_h at 2s/pair',round(attempts*2/3600,2))
    print('finite proof does not establish full-stroke/durability qualification')


def installed_runin_check():
    """Changed assembly boundary; dimensions exact, time allocations unmeasured."""
    length, nut, low, stroke = 64., 10., 2., 50.
    high = low + stroke
    def engagement(z):
        return max(0., min(length, z + nut) - max(0., z))
    # Count turns from first thread contact, excluding the separate pilot approach.
    start_turns = (length - high) / LEAD
    full_turns = (length - low) / LEAD
    assert isclose(start_turns, 4)
    assert isclose(engagement(high), nut)
    two_turn_z = length - 2 * LEAD
    assert two_turn_z > high and engagement(two_turn_z) == 6
    for neutral in (0, 20, 30):
        run_turns = (high - (low + neutral)) / LEAD
        assert isclose(start_turns + run_turns, (length-low-neutral)/LEAD)
    # An intact close journal aperture cannot admit the larger finished collar.
    assert 2.8 < 3.0 < 4.4  # 3.0 is an illustrative aperture, not selected fit
    # Separate fixed pickup from rotation: allocate 5s pickup +10s full advance.
    # This reproduces manual-mid15s; proportional time applies only to advance.
    shallow_seconds = 5 + 10 * start_turns / full_turns
    saved_per_pair = 15 - shallow_seconds
    print('installed: first-contact turns',start_turns,'two-turn engagement',engagement(two_turn_z))
    print('shallow manual seconds',shallow_seconds,'saved seconds/pair',saved_per_pair)
    for n in (1024,4096,6400):
        attempts = n  # No fabricated usable-yield or detection claim.
        saved_h = attempts * saved_per_pair / 3600
        # Replace ONLY manual threading in E-286 mid ledger; same common work.
        assembly = n * (9 + shallow_seconds + 4) / 3600
        base_low = 8+4/6+(n*20+n*8)/3600+2*ceil(n/289)*5/60
        base_high = 16+4*.5+(n*60+n*20)/3600+2*ceil(n/289)*5/60
        print('installed N',n,'saved_h',round(saved_h,3),'whole maker pre extras',
              [round(base_low+assembly,2),round(base_high+assembly,2)])
        for rpm in (120,850):
            for neutral in (0,20,30):
                # Four independent spindles, ideal full batches; 2s visit allocation
                # includes reposition/dock/undock/read. Not E-276 route replay.
                visits = ceil(n/4)
                turns = (stroke-neutral)/LEAD
                minutes = visits*(turns*60/rpm + 2)/60
                assert minutes >= visits*2/60
                print('commission N/rpm/neutral/min',n,rpm,neutral,round(minutes,3))
        # At 120rpm and zero home, fully attending the entire new run-in operation
        # charges a conservative increment, without crediting prior commissioning.
        attended_h = ceil(n/4)*((stroke/LEAD)*60/120+2)/3600
        print('maximum extra fixture/setup h after full attendance',round(saved_h-attended_h,3))
    # Manufacturing/replacement identity: cold-start whole-board run-in is not
    # a local replacement protocol. No blanket homing of unchanged loaded cells.
    print('installed run-in: conditional assembly saving; no support or qualification pass')


def bottom_thrust_service_check():
    """Finite aperture/force-direction screen, not contact or hardware proof."""
    from math import pi, sqrt
    from itertools import product
    # Changed stationary stack, unchanged E-280 finished screw.
    # Driver bottom z=-10 rests on annulus; socket entered through its aperture.
    # Top split journal/keeper surrounds z=-4..0 and arrests upward collar travel.
    tool_af, aperture, driver, journal = 2., 2.8, 4.4, 2.8
    assert tool_af * 2/sqrt(3) < aperture < driver
    assert journal < 3.2 < driver
    corners=[]
    for tool_error, hole_error, body_error, eccentricity in product(
            (-.05,.05),(-.1,.1),(-.1,.1),(0.,.1)):
        rt=(tool_af+tool_error)/sqrt(3)
        rh=(aperture+hole_error)/2
        ro=(driver+body_error)/2
        tool_margin=rh-rt-eccentricity
        bearing_width=ro-rh-eccentricity
        # Conservative complete concentric ring remaining despite hole offset.
        ring_area=pi*(ro**2-(rh+eccentricity)**2)
        assert min(tool_margin,bearing_width,ring_area)>0
        corners.append((tool_margin,bearing_width,ring_area))
    print('bottom thrust: 16 bounded aperture cases; minima mm/mm/mm2',
          [round(min(x[i] for x in corners),6) for i in range(3)])
    ro,rh=driver/2,aperture/2
    mean_radius=2/3*(ro**3-rh**3)/(ro**2-rh**2)
    assert rh < mean_radius < ro
    # Uniform pressure Coulomb friction only. Actual wear/contact/preload unknown.
    for force in (.2,.338):
        print('bottom thrust F/assumed mu .1-.4/drag Nmm',force,
              [round(mu*force*mean_radius,6) for mu in (.1,.4)])
    # Constraint graph: radial here means dedicated lower-journal support,
    # not claimed zero movement or replacement by the loaded thread/upper guides.
    def constraints(bottom,keeper,service_keeper=False):
        return (bottom,keeper or service_keeper,keeper or service_keeper)
    assert constraints(True,True)==(True,True,True)
    assert constraints(False,False)==(False,False,False) # open load-bearing row
    assert constraints(True,False)==(True,False,False) # gravity-only escape
    assert constraints(True,False,True)==(True,True,True) # unbuilt third interface
    assert 4.4 < 10.8 # axial collar through illustrative coarse body guide
    assert 4.4 > 3.2 # fixed keeper obstructs the same extraction
    # Full body still requires known yaw/straightness/clearance, not just this check.
    # Single coarse row opens transversely, adjacent row rails stay closed.
    half_width, opening, pitch, radial_error = 4.5, 2.4, 12.7, .1
    assert opening > driver/2 + radial_error
    neighbor_gap=pitch-2*half_width-opening
    assert isclose(neighbor_gap,1.3)
    print('coarse row nominal outer gap mm',neighbor_gap)
    for side in (32,80):
        n=side**2
        print('support replication sites/row half rails/added ring contacts',
              n,2*side,n)
        print('illustrative rail lock operations at two/rail',4*side,
              'temporary neighbor restraint sites for single row',side-1)
        print('assumed rail placement+lock maker h',
              [round((2*side+4*side)*seconds/3600,3) for seconds in (10,30)])
    # Common lower-plate downward error transfers directly into surface height.
    for settlement in (0.,.05,.2):
        assert isclose((52-settlement)-52,-settlement,abs_tol=1e-12)
    print('gravity continuity does not prove upward capture, radial guidance or unchanged height')



def single_pair_service_check():
    """Necessary access/constraint bounds; no contact, strength or repair proof."""
    # Same finite screw as bottom_thrust_service_check. No fit optimization.
    collar, journal_bore, bottom_bore = 4.4, 3.2, 2.8
    # Even favorable +/-0.1 mm independent diameter bounds block intact removal.
    assert collar-.1 > journal_bore+.1
    assert collar-.1 > bottom_bore+.1
    # Opening a fixed keeper to pass this collar also removes its capture shoulder.
    for aperture in (4.6, 4.8):
        assert aperture > collar and (collar-aperture)/2 < 0
    for side, pitch in ((32,12.7),(80,5.08)):
        n = side**2
        # Optimistic translating single window, ignoring collisions of the rest
        # of the plate with journal shafts. Closed constraints are granted except
        # where the window is centered. Every intermediate center is reached by
        # any continuous in-plane path along this row from its left edge.
        window_width = 4.6
        assert window_width < pitch  # single-site endpoint is possible in 1D
        for target in range(side):
            crossed = [j for j in range(side) if -pitch <= j*pitch <= target*pitch]
            assert crossed == list(range(target+1))
            assert len([j for j in crossed if j != target]) == target
        # Mid-row target defeats even a choice of the nearer row end.
        worst_nearest = max(min(j,side-1-j) for j in range(side))
        assert worst_nearest == side//2-1
        print('service sliding window N/worst-nearest crossed neighbors',n,worst_nearest)
        for block in (1,4,side):
            assert side % block == 0
            segments=n//block
            # Each segment has two halves and two locks per half, inherited
            # allocation, not a physical lock design or universal lower bound.
            halves, locks = 2*segments, 4*segments
            neighbor_contacts=block-1
            # 8 common actions +4 unlock+2 open+2 close+4 lock =20.
            # Per neighbor: engage temporary restraint, verify, verify restored
            # permanent restraint, release temporary restraint. Not free batching.
            operations=20+4*neighbor_contacts
            print('service N/block/halves/locks/neighbors/repair actions',
                  n,block,halves,locks,neighbor_contacts,operations)
            print('service all-site-once diagnostic actions',n*operations)
            # Explicit constraint replay. All neighbors retain bottom support;
            # radial/upward paths vanish when keeper opens unless transferred.
            permanent = {j: True for j in range(block)}
            target=0
            temporary=set()
            permanent={j:False for j in permanent}
            unsupported=[j for j in permanent if j != target and
                         not(permanent[j] or j in temporary)]
            assert len(unsupported)==neighbor_contacts
            # Granting an unqualified bypass can satisfy a graph; it is NOT a
            # geometric implementation. Label this assumption, never a pass.
            temporary=set(range(1,block))
            assert all(permanent[j] or j in temporary for j in range(1,block))
        assert 2*n == n+n  # body+screw count unchanged by access architecture
    print('service STOP: shared opening needs restraint transfer; cell closure repeats locks')



def detachable_shank_check():
    """Rigid axial envelope and explicitly allocated labor, not joint design."""
    # Original thread is ABOVE keeper. Only the released lower tail crosses it.
    # Common diametric errors may take opposite extremes; no process PDF.
    margins=[]
    for bore_error,tail_error,ecc in product((-.1,.1),(-.1,.1),(0,.1)):
        margins.append((3.2+bore_error-(2.8+tail_error))/2-ecc)
    assert isclose(min(margins),0,abs_tol=1e-12)
    assert isclose((3.2-2.8)/2,.2)
    # Collar/driver remains captured: this does not repair its faults.
    assert 4.4-.1 > 3.2+.1 and 4.4-.1 > 2.8+.1
    faults={'body':True,'threaded_shank':True,'driver_socket':False,
            'driver_thrust_face':False,'keeper':False,'bottom_plate':False}
    assert sum(faults.values())==2  # enumerated classes, NOT reliability coverage
    # At minimum nut bottom2, tip64 must withdraw62mm relative to a held body.
    assert isclose((64-2)/LEAD,62/3)
    for n in (1024,4096,6400):
        print('detachable N',n,'resident pieces',4*n,'extra pieces',2*n,
              'added join+proof hours',[round(n*t/3600,2) for t in (15,45)],
              'optimistic 32h budget minus prior low whole maker',
              round(32-(22.97 if n==1024 else 65.71 if n==4096 else 97.72),2))
        # Seven distinct added actions, no credit for automatic feed/gauging.
        assert 7*n > n
    print('detachable nominal/min bounded radial margin',.2,round(min(margins),9))
    print('detachable: only body/shank extraction; captive driver faults unresolved')


if __name__ == '__main__':
    check()
    proof_check()
    installed_runin_check()
    bottom_thrust_service_check()
    single_pair_service_check()
    detachable_shank_check()
