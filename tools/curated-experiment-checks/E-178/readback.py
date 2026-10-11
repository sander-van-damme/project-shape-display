"""E-178: finite reflected rays, discrete optical codes, and serial scan bounds.
Standard library. Length mm, time s. Explicit epistemic scenarios, not yield.
"""
import itertools as it
import json
import math

P = 5.08
LEVELS = tuple(10.1*k for k in range(5))
CODES = (3, 5, 6, 9, 10)  # four bits, constant weight 2; 12 is reserved
TRACKS = (-1.2, -.4, .4, 1.2)


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def mul(s,a): return tuple(s*x for x in a)


def hit_box(a,b,lo,hi):
    """Closed finite segment/AABB intersection by slabs; endpoint contact counts."""
    lower,upper=0.,1.
    for x,v,l,h in zip(a,sub(b,a),lo,hi):
        if abs(v)<1e-12:
            if not l<=x<=h:return False
        else:
            t0,t1=sorted(((l-x)/v,(h-x)/v))
            lower=max(lower,t0);upper=min(upper,t1)
            if lower>upper:return False
    return True


def ray(target, camera, mirror_y=1.6, mirror_z=0., tilt=0.):
    theta=math.radians(45+tilt)
    n=(0.,math.cos(theta),math.sin(theta))
    tangent=(0.,math.sin(theta),-math.cos(theta))
    center=(0.,mirror_y,mirror_z)
    virtual=sub(target,mul(2*dot(sub(target,center),n),n))
    v=sub(virtual,camera)
    fraction=dot(sub(center,camera),n)/dot(v,n)
    m=add(camera,mul(fraction,v))
    along=dot(sub(m,center),tangent)
    # Verify reflection direction and path length using an independent law.
    vin=sub(m,camera);vout=sub(target,m)
    reflected=sub(vin,mul(2*dot(vin,n),n))
    assert abs(dot(reflected,vout)**2-dot(reflected,reflected)*dot(vout,vout))<1e-6
    assert dot(reflected,vout)>0
    assert abs(math.dist(camera,m)+math.dist(m,target)-math.dist(camera,virtual))<1e-9
    return m, .7*math.sqrt(2)-abs(along)


def optical_scenario(error,tilt,pupil,subdivisions=1):
    # Four camera segments, each 20 columns. Translation to interior segments
    # leaves geometry invariant. Check the first segment and neighbors outside it.
    # Each error sign may be shared by an entire row/batch. Opposing local tail
    # shifts are enveloped by expanded swept boxes, not iid samples.
    total=clipped=blocked=0; min_edge=float('inf'); witness=None
    for sy,sz,sc,st,sp,sa in it.product((-1,1),repeat=6):
        my=1.6+sy*error;mz=sz*error;cy=1.6+sc*error
        for col,track,dx,dz in it.product(range(20),TRACKS,(-.08,.08),(-.08,.08)):
            target=(col*P+track+dx,.6+st*error,dz)
            # Pupil support along Y is decisive for corridor visibility; x pupil
            # does not change YZ. Mirror extends along X with board-edge margin.
            camera=(9.5*P,cy+sp*pupil,-50.)
            m,edge=ray(target,camera,my,mz,sa*tilt)
            assert -2.54 <= m[0] <= 79*P+2.54
            # Finite reflected path may meet its intended tail only at the face.
            # Opposed local offsets on eight neighboring tails remain enclosed.
            for rc,cc in it.product((-1,0,1),repeat=2):
                if rc==cc==0:continue
                lo=((col+cc)*P-1.6-error,rc*P-.6-error,-42.4)
                hi=((col+cc)*P+1.6+error,rc*P+.6+error,42.4)
                assert not hit_box(m,target,lo,hi)
            total+=1;min_edge=min(min_edge,edge)
            if edge<0:clipped+=1;continue
            # An exact continuous-in-X opaque row is conservative for every tail
            # in that row. On collision, find a real finite tail as a witness.
            possible=False
            for row in (-1,0,1):
                lo=(-1e6,row*P-.6-error,-42.4)
                hi=(1e6,row*P+.6+error,42.4)
                if hit_box(camera,m,lo,hi):possible=True;break
            if possible:
                blocked+=1
                if witness is None:
                    for r,c,h in it.product((-1,0,1),range(20),LEVELS):
                        lo=(c*P-1.6,r*P-.6+error,h-42.4)
                        hi=(c*P+1.6,r*P+.6+error,h+2.)
                        if hit_box(camera,m,lo,hi):
                            witness={'camera':camera,'target':target,'mirror':m,
                                     'occluder_row_col_height':(r,c,h)};break
            # Straight segment discretization is a holdout for exact YZ bounds.
            if not possible:
                for k in range(subdivisions+1):
                    q=add(camera,mul(k/subdivisions,sub(m,camera)))
                    if -42.4<=q[2]<=42.4:
                        assert all(abs(q[1]-r*P)>.6+error for r in (-1,0,1))
    # Finite reflecting strip and backing must also clear the moving tail.
    theta=math.radians(45+tilt)
    edge_y=1.6-error-.7*math.sqrt(2)*math.sin(theta)
    mechanical_gap=edge_y-(.6+error)
    a=(0.,edge_y,.7*math.sqrt(2)*math.cos(theta))
    b=(0.,1.6-error+.7*math.sqrt(2)*math.sin(theta),-.7*math.sqrt(2)*math.cos(theta))
    collision=hit_box(a,b,(-1.6,-.6-error,-42.4),(1.6,.6+error,2.))
    assert collision==(mechanical_gap<=0)
    return dict(mirror_tail_gap_mm=mechanical_gap,finite_strip_tail_collision=collision,error_mm=error,tilt_deg=tilt,pupil_radius_mm=pupil,rays=total,
                finite_mirror_misses=clipped,conservative_blocked=blocked,
                min_mirror_edge_mm=min_edge,real_tail_witness=witness)


def code_analysis():
    # Exhaustive five-word code search on the binary cube for n=3,4,
    # excluding uniform dark/light words.
    feasible={}
    for n in (3,4):
        feasible[n]=sum(all((a^b).bit_count()>=2 for a,b in it.combinations(words,2))
                        for words in it.combinations(range(1,2**n-1),5))
    assert feasible[3]==0 and feasible[4]>0
    flips={}
    for count in (1,2,3,4):
        words=[w ^ sum(1<<b for b in bits) for w in CODES for bits in it.combinations(range(4),count)]
        flips[count]={'trials':len(words),'accepted_wrong':sum(w in CODES for w in words)}
    assert flips[1]['accepted_wrong']==0
    complement=[(w,w^15) for w in CODES if w^15 in CODES]
    # A height code tells nothing about an independently failed support or pickup.
    aliases=sum(1 for h in LEVELS for support,pickup in it.product((0,1),repeat=2)
                if (support,pickup)!=(1,0))
    return dict(five_word_codebooks=feasible,codewords=[format(w,'04b') for w in CODES],
                bit_faults=flips,complement_aliases=complement,
                hidden_support_pickup_states=aliases,
                five_track_alternative=dict(words=['00011','00110','01100','11000','10001'],
                    min_distance=min((a^b).bit_count() for a,b in it.combinations((3,6,12,24,17),2)),
                    complement_aliases=sum((w^31) in (3,6,12,24,17) for w in (3,6,12,24,17)),
                    horizontal_reserve_at_point2mm=.24-.08-.2))


def read_code(height,datum=0,half_band=.4,footprint=.08):
    # Reject samples intersecting a mark edge. Blank background is 0000 invalid.
    for k,h in enumerate(LEVELS):
        if abs(height-h-datum)+footprint<=half_band:return k
    return None


def error_bounds(e):
    # e is total vertical scale/datum/mark/optical error, including coherent bias.
    # Registration and shape must be independently bounded; no distribution.
    guaranteed=.4-.08-e
    possible=.4-.08+e
    for h in LEVELS:
        for sign in (-1,1):
            # Analytic endpoints plus infinitesimal exterior holdout.
            d=sign*e;err=sign*possible
            assert read_code(h+err,d) in (None,LEVELS.index(h))  # floating boundary
            assert read_code(h+sign*(possible+1e-6),d)!=LEVELS.index(h)
    return dict(total_vertical_error_mm=e,guaranteed_accept_radius_mm=max(0,guaranteed),
                same_level_false_accept_extent_mm=possible,
                guaranteed_nominal_accept=guaranteed>=0,
                # horizontal bit: halfwidth .3, footprint .08.
                horizontal_registration_reserve_mm=.3-.08-e)


def move(d,v=200.,a=5000.):
    if d<=v*v/a:return 2*math.sqrt(d/a)
    return d/v+v/a


def scan(rows,slot=.02,prep=.5,retry=.2):
    # Start at first row, return there; no overlap; one repeated acquisition.
    distance=(rows-1)*P
    return (rows-1)*move(P)+move(distance)+rows*slot+prep+retry+slot


def main():
    assert hit_box((0,0,-2),(0,0,2),(-1,-1,-1),(1,1,1))
    assert not hit_box((2,0,-2),(2,0,2),(-1,-1,-1),(1,1,1))
    # Independent nominal virtual-image formula.
    m,e=ray((0,.6,0),(0,1.6,-50))
    assert all(abs(a-b)<1e-10 for a,b in zip(m,(0,1.6,0)))
    scenarios=[optical_scenario(*s) for s in [(0,0,.5),(.05,.2,.5),(.1,.5,.5),(.2,1,.5),(.1,.5,1.5)]]
    # Repeat the useful bounded survivor at finer segment holdouts.
    for n in (4,16):
        hold=optical_scenario(.1,.5,.5,n)
        assert {k:v for k,v in hold.items()}==scenarios[2]
    # Inverting E-004's height field gives an underside endpoint counterexample.
    endpoint_camera=(0.,0.,-100.);endpoint_target=(10*P,0.,-2.)
    assert hit_box(endpoint_camera,endpoint_target,(9*P-1.6,-.6,-42.4),(9*P+1.6,.6,2.))
    corridor_reserve=min(1.6-.1-.5,1.6-.1-.7*math.sqrt(2)*math.sin(math.radians(45.5)))-(.6+.1)
    assert corridor_reserve>0
    output={'endpoint_occlusion_witness':dict(camera=endpoint_camera,target=endpoint_target,occluder_column=9),
            'continuous_incoming_corridor_reserve_mm':corridor_reserve,'rays':scenarios,'code':code_analysis(),
            'registration':[error_bounds(e) for e in (0,.1,.2,.35)],
            'scan_s':{str(slot):scan(80,slot) for slot in (.005,.02,.05,.1)},
            'five_row_worst_return_s':move(75*P)+4*move(P)+move(79*P)+5*.02+.5+.2+.02,
            'continuous_scan_floor_s':2*move(79*P)+.5+.2+.02,
            'continuous_max_exposure_for_point1mm_s':.1/200,
            'continuous_frame_period_s':P/200,
            'direct_control_plus_scan_s':19.469+scan(80),
            'broadcast_control_plus_scan_s':21.494+scan(80),
            'mirrors_m':80*80*P/1000,
            'tail_blank_volume_l':6400*3.2*1.2*44.4/1e6,
            'minimum_flat_scanner_optical_distance_mm':42.4+1.,
            'pixel_per_bit_at_1280_20_columns':1280/(20*P)*.6}
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()
