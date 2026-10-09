"""Bounded rectangular shutter geometry and exhaustive two-row handoff checks.
All lengths mm; deterministic epistemic boxes, no process probability.
"""
from itertools import product, permutations
import json

PITCH = 5.08

def margins(w, a, d, e):
    # e bounds relative registration; width errors independently +/- e.
    return ((a-e)/2-(w+e)/2-e,
            d-e+(w-e)/2-(a+e)/2,
            PITCH-d-e-(a+e)/2-(w+e)/2)

def fits(w,a,offset):
    return abs(offset)+w/2 <= a/2 + 1e-12

def geometry():
    counts={}
    for e in (0.05,0.1,0.2):
        survivors=[]
        rejected=[]
        for w,a,d in product((0.6,0.8,1.0),(1.2,1.6,2.0),(1.0,1.5,2.0)):
            m=margins(w,a,d,e)
            # Interval endpoint test on actual 1-D rectangle containment and
            # nearest periodic aperture; orthogonal second layer is symmetric.
            opened=[];blocked=[];neighbor=[]
            for ew,ea,ex in product((-e,e),repeat=3):
                opened.append(fits(w+ew,a+ea,ex))
                blocked.append(not fits(w+ew,a+ea,d+ex))
                neighbor.append(abs(PITCH-d-ex)>(a+ea+w+ew)/2)
            assert (m[0]>=-1e-12)==all(opened)
            # strict positive obstruction required (touch alone is not blocking)
            if min(m)>1e-9:
                assert all(blocked) and all(neighbor)
                survivors.append((w,a,d,tuple(round(x,4) for x in m)))
            else:
                rejected.append({"geometry":(w,a,d),"fails":[name for name,v in zip(("open_clearance","closed_overlap","neighbor_aperture"),m) if v<=1e-9]})
        counts[e]={"survivors":survivors,"rejected":rejected}
    return counts

def handoffs():
    # Initially row 0 / column 0 selected with drive loaded; target row 1 / col 1.
    # Each command is atomic; evaluate every intermediate stable state.
    actions=('unload','row0off','col0off','row1on','col1on','load')
    valid=[]; wrong=[]; jam=[]
    for seq in permutations(actions):
        rows={0}; cols={0}; drive=True; bad=False; interference=False
        for action in seq:
            if action=='unload': drive=False
            elif action=='load': drive=True
            else:
                axis=rows if action.startswith('row') else cols
                i=int(action[3]); on=action.endswith('on')
                # Closing a shutter occupied by a fully inserted selected pin jams.
                if not on and drive and rows and cols and i in axis:
                    interference=True
                if on: axis.add(i)
                else: axis.discard(i)
            if drive and any((r,c) not in ((0,0),(1,1)) for r in rows for c in cols):
                bad=True
        # final loaded target required; unloading after load is not a handoff.
        if drive and rows=={1} and cols=={1}:
            if bad: wrong.append(seq)
            if interference: jam.append(seq)
            if not bad and not interference: valid.append(seq)
    safe=('unload','row0off','col0off','row1on','col1on','load')
    assert safe in valid
    assert all(s[0]=='unload' for s in valid)
    guarded=[s for s in valid if s[-1]=='load']
    assert len(guarded)==24
    return {'permutations':720,'safe_binary_states':len(valid),'unloaded_address_changes':len(guarded),
            'final_loaded_wrong_address':len(wrong),'final_loaded_closure_collision':len(jam),
            'wrong_example':wrong[0],'jam_example':jam[0]}

if __name__=='__main__':
    print(json.dumps({'geometry':geometry(),'handoffs':handoffs(),
       'witness_margins':margins(.8,1.6,1.5,.1),
       'global_block_force_N':{str(f):6320*f for f in (.01,.05,.1)},
       'row_local_block_force_N':{str(f):80*f for f in (.01,.05,.1)}},indent=2))
