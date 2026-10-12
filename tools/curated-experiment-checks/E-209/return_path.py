"""E-209: extensible curved return, mm/N/MPa; explicit bounds, not process priors.
Run with OPENBLAS_NUM_THREADS=1. Output is disposable JSON; NumPy only.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

spec = importlib.util.spec_from_file_location('rock', Path(__file__).resolve().parents[1]/'E-208/rocking.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def solve(angle=0., withdraw=0., n=32, L=12., amp=.3, t=.4,
          offset=(0., 0.), initial=None, audit=False):
    ref, rpos = r.rod_reference(n, L, amp)
    ds = L/n
    stiffness = 12/t**2  # EA/EI, rectangular homogeneous section
    root = r.A-rpos[-1]+offset
    target = r.move(r.A[None, :], angle, withdraw)[0]-root
    x = (np.r_[ref[1:-1], np.ones(n), np.zeros(2)] if initial is None
         else initial.copy())
    B = (np.diag(np.full(n-1, 2/ds)) + np.diag(np.full(n-2, -1/ds), 1)
         + np.diag(np.full(n-2, -1/ds), -1))

    def value(x):
        th = np.r_[0., x[:n-1], -angle]
        stretch, lam = x[n-1:2*n-1], x[-2:]
        sn, cs = np.sin(th), np.cos(th)
        tangent = .5*np.c_[sn[:-1]+sn[1:], cs[:-1]+cs[1:]]
        err = np.diff(th-ref)
        v = ds*.5*np.c_[cs[1:-1], -sn[1:-1]]
        Jth = (stretch[:-1]+stretch[1:])[:, None]*v
        residual = np.r_[(err[:-1]-err[1:])/ds+Jth@lam,
                         ds*(stiffness*(stretch-1)+tangent@lam),
                         ds*(stretch@tangent)-target]
        H = B+np.diag(ds*.5*(stretch[:-1]+stretch[1:])*
                      (-lam[0]*sn[1:-1]-lam[1]*cs[1:-1]))
        cross = np.zeros((n-1, n))
        for i, c in enumerate(v@lam):
            cross[i, i:i+2] = c
        J = np.vstack((Jth, ds*tangent))
        hess = np.block([[H, cross], [cross.T, ds*stiffness*np.eye(n)]])
        K = np.block([[hess, J], [J.T, np.zeros((2, 2))]])
        return residual, K, th, stretch, lam, tangent

    for iteration in range(100):
        res, K, th, stretch, lam, tangent = value(x)
        if max(abs(res)) < 2e-10:
            break
        step = np.linalg.solve(K, -res)
        fac = 1.
        while fac > 1e-8:
            trial = x+fac*step
            if min(trial[n-1:2*n-1]) > 0 and np.linalg.norm(value(trial)[0]) < np.linalg.norm(res):
                x = trial
                break
            fac *= .5
        else:
            raise RuntimeError(('line search', angle, withdraw, offset))
    else:
        raise RuntimeError(('convergence', angle, withdraw, offset))
    J = K[:-2, -2:]
    _, _, V = np.linalg.svd(J.T, full_matrices=True)
    Z = V[2:].T
    eig = float(np.linalg.eigvalsh(Z.T@K[:-2, :-2]@Z)[0])
    assert eig > 0, ('unstable', angle, withdraw, offset)
    pos = root+np.vstack(([0., 0.], np.cumsum(ds*stretch[:, None]*tangent, axis=0)))
    assert np.max(abs(pos[-1]-root-target)) < 1e-9
    curv = np.diff(th-ref)/ds
    fiber = np.array([stretch-1+t/2*curv, stretch-1-t/2*curv])
    # First-order fiber kinematics above; finite reference-radius correction
    # is a discrepancy diagnostic, not a nonlinear material constitutive law.
    corrected = fiber/np.array([1+t/2*np.diff(ref)/ds, 1-t/2*np.diff(ref)/ds])
    endgrad = (th[-1]-ref[-1]-th[-2]+ref[-2])/ds
    endjac = ds*.5*stretch[-1]*np.array([np.cos(th[-1]), -np.sin(th[-1])])
    energy = (np.dot(np.diff(th-ref), np.diff(th-ref))/ds
              + ds*stiffness*np.dot(stretch-1, stretch-1))/2
    jacerr = 0.
    if audit:
        for j in range(len(x)):
            delta = np.zeros(len(x)); delta[j] = 1e-6
            jacerr = max(jacerr, float(max(abs((value(x+delta)[0]-value(x-delta)[0])/2e-6-K[:, j]))))
        assert jacerr < 1e-6
    return dict(theta=th, pos=pos, x=x, fiber=fiber, corrected=corrected,
                force=-lam, moment=-(endgrad+endjac@lam), energy=float(energy),
                eig=eig, residual=float(max(abs(res))), jacerr=jacerr,
                axial=float(max(abs(stretch-1))), D=float(rpos[-1, 1]), root=root)


def frame(D, offset):
    f = r.fixed(D=D)
    # Shift the finite root ledge/crossbar, keeping side uprights fixed.
    for i in (10, 11):
        q, x = f[i]; f[i] = (q+offset, x)
    assert r.p.hit(f[10], f[11])
    assert r.p.hit(f[10], f[4]) and r.p.hit(f[10], f[9])
    return f


def seated_bound(state, load_y):
    """Optimistic frictionless planar reaction relaxation, normalized by EI.
    All upward support y in [-1,1.6]; one signed key-wall resultant z in [-.2,0].
    Ignores gaps and grants resultant contact: necessary, never sufficient.
    No arbitrary opposing key couple, friction hold, cap, or applied tool moment.
    """
    fy, fz = state['force']
    c = r.A[0]*fz-r.A[1]*fy+state['moment']
    cmin, cmax = c+min(0., -.2*fy), c+max(0., -.2*fy)
    ymin, ymax = -1., 1.6
    w = max(0., -fz, (cmin-ymax*fz)/(ymax-load_y),
            (ymin*fz-cmax)/(load_y-ymin))
    reaction = w+fz
    lo = max(cmin, ymin*reaction-w*load_y)
    hi = min(cmax, ymax*reaction-w*load_y)
    assert reaction > -1e-12 and lo < hi+1e-12
    return float(w)


def run_path(n=32, steps=32, L=12., amp=.3, t=.4, offset=(0., 0.), neighbor_bias=.05):
    outward = [(a, 0.) for a in np.linspace(0, .22, steps+1)]
    outward += [(.22, w) for w in np.linspace(0, 1.4, steps+1)[1:]]
    poses = outward+outward[-2::-1]
    states = []; first = None; initial = None
    peak = 0.; peak_pose = None; force = 0.; moment = 0.; min_eig = float('inf')
    residual = 0.; corrected_peak = 0.; max_axial = 0.; near_rack = 1e9
    for i, (angle, w) in enumerate(poses):
        a = solve(angle, w, n, L, amp, t, offset, initial)
        initial = a['x']; states.append(a)
        strain = float(np.max(abs(a['fiber'])))
        if strain > peak:
            peak = strain; peak_pose = dict(index=i, angle=angle, withdraw=w)
        corrected_peak = max(corrected_peak, float(np.max(abs(a['corrected']))))
        max_axial = max(max_axial, a['axial'])
        force = max(force, float(np.linalg.norm(a['force'])))
        moment = max(moment, abs(a['moment']))
        min_eig = min(min_eig, a['eig']); residual = max(residual, a['residual'])
        leaf = r.rod_bodies(a, t)
        collar = r.bodies(angle, w, t=t)[6][0]
        assert np.max(abs(leaf[-1][0][[3, 2]]-collar[[0, 1]])) < 1e-9
        f = frame(a['D'], offset)
        root_face = leaf[0][0][[0, 1]]
        assert np.max(abs(root_face[:, 1]-f[11][0][:, 1].max())) < 1e-9
        assert root_face[:, 0].min() >= f[11][0][:, 0].min()
        assert root_face[:, 0].max() <= f[11][0][:, 0].max()
        groups = {'frame': f, 'rack': r.p.rack(1.5), 'jaw': r.p.writer(1.5),
                  'blade': r.tool(angle, w), 'toe': r.bodies(angle, w, t=t)[:6]}
        for dy in (-5.08, 5.08):
            groups['neighbor'+str(dy)] = [(q+[dy+neighbor_bias, 0], x) for q, x in
                                         r.bodies(0, t=t)+frame(a['D'], offset)+r.p.rack()]
        # Include coherent neighboring returns and their shifted root ledges.
        restleaf = r.rod_bodies(states[0], t)
        for dy in (-5.08, 5.08):
            groups['neighbor'+str(dy)] += [(q+[dy+neighbor_bias, 0], x) for q, x in restleaf]
        low = np.array([q.min(axis=0) for q, x in leaf])
        high = np.array([q.max(axis=0) for q, x in leaf])
        pairs = np.argwhere(np.triu(np.all(np.minimum(high[:, None, :], high[None, :, :])-
                                          np.maximum(low[:, None, :], low[None, :, :]) > 1e-10, axis=2), 2))
        if any(r.p.hit(leaf[j], leaf[k]) for j, k in pairs) and first is None:
            first = dict(index=i, angle=angle, withdraw=w, body='self')
        for name, obs in groups.items():
            if r.collides(leaf, obs) and first is None:
                first = dict(index=i, angle=angle, withdraw=w, body=name)
        near_rack = min(near_rack, min(q[:, 0].min() for q, x in leaf)-(-5.08+neighbor_bias+2.2))
    retrace = max(float(np.max(abs(states[i]['pos']-states[-1-i]['pos']))) for i in range(len(outward)))
    assert retrace < 1e-7
    fibers = np.array([a['fiber'] for a in states])
    strain_range = float(np.max(np.max(fibers, axis=0)-np.min(fibers, axis=0)))
    rest = states[0]
    # Spring-on-toe force is -force; unilateral horizontal ledges only push up.
    # W >= max(0, -Fz) is NECESSARY ONLY for the modeled downward load.
    minimum_downward = max(0., float(-rest['force'][1]))
    return dict(n=n, steps=steps, L=L, amp=amp, t=t, offset=offset,
                first_collision=first, peak_strain=peak, peak_pose=peak_pose,
                corrected_peak=corrected_peak, max_axial=max_axial,
                fiber_cycle_range=strain_range, max_force_over_EI=force,
                max_moment_over_EI=moment, min_hessian=min_eig,
                max_residual=residual, reverse_error=retrace,
                rest_force_over_EI=rest['force'].tolist(), rest_moment_over_EI=float(rest['moment']),
                minimum_downward_over_EI=minimum_downward,
                seated_load_bound_over_EI=[seated_bound(rest, y) for y in (.8, 1.2)],
                previous_rack_projection_gap=near_rack)


def verify():
    zero = solve(n=32)
    assert zero['energy'] < 1e-20 and np.linalg.norm(zero['force']) < 1e-12
    # Independent straight-bar limit: EA delta/L, with zero bending.
    bar = solve(amp=0., offset=(0., -.1))
    expected = (12/.4**2)*.1/12
    assert abs(bar['force'][1]-expected) < 1e-10
    assert abs(bar['force'][0]) < 1e-12 and np.max(abs(bar['theta'])) < 1e-12
    thin = solve(.22, 1.4, t=.01)
    rigid = r.rod(.22, 1.4, n=32, amp=.3)
    limit_error = float(np.linalg.norm(thin['force']-rigid['force_over_EI'])/np.linalg.norm(rigid['force_over_EI']))
    assert limit_error < .001
    workerrs = []; jacerrs = []; holdouts = []
    for offset in [(0., 0.), (.1, -.1), (-.1, .1)]:
        for angle, w in [(.1, 0.), (.22, .7), (.22, 1.4)]:
            kw = dict(n=32, offset=offset)
            a = solve(angle, w, audit=True, **kw); eps = 1e-5
            plus = solve(angle+eps, w, **kw); minus = solve(angle-eps, w, **kw)
            delta = (r.move(r.A[None, :], angle+eps, w)[0]-r.move(r.A[None, :], angle-eps, w)[0])/(2*eps)
            workerrs.append(abs((plus['energy']-minus['energy'])/(2*eps)-a['force']@delta-a['moment']))
            plus = solve(angle, w+eps, **kw); minus = solve(angle, w-eps, **kw)
            workerrs.append(abs((plus['energy']-minus['energy'])/(2*eps)+a['force'][0]))
            jacerrs.append(a['jacerr'])
    # Pure vertical downward load at y=0 is admissible; upward rear spring
    # requires W=2.2/.6 in a hand-solvable unit force/moment example.
    assert seated_bound(dict(force=np.array([0., 1.]), moment=.6), 1.) == 0.
    assert abs(seated_bound(dict(force=np.array([0., -1.]), moment=0.), 1.)-2.2/.6) < 1e-12
    for L, amp, t in [(12., .3, .4), (11.5, .25, .45)]:
        a = solve(.22, 1.4, L=L, amp=amp, t=t)
        old = r.extensible_holdout(L=L, amp=amp, t=t)
        err = abs(np.linalg.norm(a['force'])-old['force_over_EI'])
        assert err < 1e-8
        holdouts.append(float(err))
    assert max(workerrs) < 1e-7
    return dict(straight_bar_force_error=float(abs(bar['force'][1]-expected)), inextensible_limit_relative_error=limit_error, energy_work_error=max(workerrs), jacobian_error=max(jacerrs), E208_endpoint_errors=holdouts)


def endpoint_refinement():
    out = []
    for L, amp, t in [(12., .3, .4), (11.5, .25, .45)]:
        for offset in [(-.1, .1), (.1, -.2)]:
            for n in (32, 64, 128):
                for angle, w in [(0., 0.), (.22, 0.), (.22, 1.4)]:
                    a = solve(angle, w, n=n, L=L, amp=amp, t=t, offset=offset)
                    out.append(dict(L=L, offset=offset, n=n, angle=angle, w=w,
                                    force=float(np.linalg.norm(a['force'])),
                                    strain=float(np.max(abs(a['fiber']))),
                                    bound=seated_bound(a, 1.2) if angle == 0 else None))
    return out


def unloaded_escape():
    # A geometric zero-load alternative to the constrained seat. This does
    # not solve departure under gravity, friction, load, or contact dynamics.
    offset = np.array([0., .1])
    toe = [(q+offset, x) for q, x in r.bodies(0.)]
    ref, pos = r.rod_reference(64, 12., .3)
    leaf = r.rod_bodies(dict(theta=ref, pos=pos+r.A-pos[-1]+offset))
    rack = r.p.rack(.1)
    f = frame(float(pos[-1, 1]), offset)
    assert not r.collides(toe, f+rack)
    assert not r.collides(leaf, f+rack+toe[:6])
    # Socket is at z=-.35..0, translated key at z=-.1..+.1.
    overlap = min(0., .1)-max(-.35, -.2+.1)
    assert abs(overlap-.1) < 1e-12
    return dict(root_height=.1, toe_rise=.1, key_vertical_overlap=overlap,
                meaning='stress-free zero-load geometry, not a loaded equilibrium or departure path')


def main():
    geometries = [(12., .3, .4), (11.5, .25, .45)]
    out = {'verification': verify(), 'unloaded_escape': unloaded_escape(),
           'endpoint_refinement': endpoint_refinement(),
           'convergence': [run_path(n=n, steps=n, L=L, amp=a, t=t, neighbor_bias=0.)
                           for L, a, t in geometries for n in (16, 32, 64)],
           'registration': [run_path(L=L, amp=a, t=t, offset=(dy, dz))
                            for L, a, t in geometries
                            for dy, dz in itertools.product((-.1, 0., .1), (-.2, -.1, 0., .1))]}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
