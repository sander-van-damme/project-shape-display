"""E-136: finite, passive flexural modal network; SI units; no latch/yield model.
Run with OPENBLAS_NUM_THREADS=1 python3 .../loaded_bus.py. JSON goes to stdout.
Only NumPy required. Bounds are scenarios, not fitted manufacturing priors.
"""
import json
from dataclasses import dataclass, replace
import numpy as np


@dataclass(frozen=True)
class Model:
    n: int = 40
    modes: int = 40
    pitch: float = .00508
    young: float = 2e9
    thick: float = .001
    density: float = 1240.
    nu: float = .35
    zp: float = .03
    mr: float = 1e-5
    fr: float = 5000.
    zr: float = .05
    extract: float = .5  # fraction of receiver viscous loss credited as useful work
    lattice: bool = True

    def basis(self):
        j = np.arange(1, self.n + 1)
        a = np.arange(1, self.modes + 1)
        s = np.sqrt(2 / (self.n + 1)) * np.sin(np.pi * j[:, None] * a / (self.n + 1))
        if self.lattice:
            lam = 4 * np.sin(np.pi * a / (2 * (self.n + 1)))**2 / self.pitch**2
        else:  # dispersion holdout: continuum spectral rather than discrete Laplacian
            lam = (np.pi * a / ((self.n + 1) * self.pitch))**2
        d = self.young * self.thick**3 / (12 * (1 - self.nu**2))
        w = np.sqrt(d / (self.density * self.thick)) * (lam[:, None] + lam[None, :])
        return s, w

    def receiver(self, w, mass=1., stiffness=1., extraction=1.):
        m = self.mr * mass
        k = self.mr * (2 * np.pi * self.fr)**2 * stiffness
        c0 = 2 * self.zr * self.mr * 2 * np.pi * self.fr
        ce = c0 * self.extract * extraction
        c = c0 * (1 - self.extract) + ce
        spring = k + 1j * w * c
        h = spring / (spring - m * w*w)
        return h, -m * w*w * h, ce, spring - m * w*w


def ports(n, count=16):
    j = np.linspace(2, n - 3, count // 4).round().astype(int)
    return [(1, int(k)) for k in j] + [(n-2, int(k)) for k in j] + [(int(k), 1) for k in j] + [(int(k), n-2) for k in j]


def shape(s, sites):
    return np.array([np.outer(s[i], s[j]) for i, j in sites])


def spatial(s, q):
    return np.einsum('ia,abf,jb->ijf', s, q, s, optimize=True)


def inverse(model, w):
    s, wn = model.basis()
    h, load, ce, den = model.receiver(w)
    mp = model.density * model.thick * model.pitch**2
    z = mp * (wn[:, :, None]**2 - w*w + 2j * model.zp * wn[:, :, None] * w) + load
    return s, 1/z, h, ce, den


def calibration(model, targets, dt, nt, count=16, duration=.002):
    """Causal finite record of response to a short smooth force pulse, reversed.
    Calibrates loaded relative velocity (optimistically accessible at every site).
    FFT period is long and convergence checked; it is not an instantaneous focus.
    """
    w = 2*np.pi*np.fft.rfftfreq(nt, dt)
    s, inv, h, _, _ = inverse(model, w)
    pp = shape(s, ports(model.n, count))
    tt = shape(s, targets).sum(axis=0)
    transfer = np.einsum('ab,pab,abf->pf', tt, pp, inv, optimize=True) * (1j*w*(h-1))
    pulse = np.zeros(nt)
    npulse = round(.0001/dt)
    pulse[:npulse] = np.sin(np.pi * (np.arange(npulse)+.5)/npulse)**2
    record = np.fft.irfft(transfer * np.fft.rfft(pulse), n=nt, axis=-1)
    nc = round(duration/dt)
    force = np.zeros((count, nt))
    force[:, :nc] = record[:, :nc][:, ::-1]
    force /= np.sqrt(dt*np.sum(force*force))  # sum integral F^2 dt = 1 N^2 s
    return np.fft.rfft(force, axis=-1)


def evaluate(model, drive, targets, dt, nt, defect=None, direct=False, guard=0):
    """Whole-period extraction with receiver reaction fed back onto the bus.
    defect=(site, mass factor, spring factor, extraction factor) rank-one update.
    Direct control applies force to receiver mass, with reaction through its spring.
    """
    s, _ = model.basis()
    pp = shape(s, targets if direct else ports(model.n, drive.shape[0]))
    energy = np.zeros((model.n, model.n))
    work = loss = 0.
    vt = np.zeros((len(targets), nt//2+1), complex)
    allw = 2*np.pi*np.fft.rfftfreq(nt, dt)
    for lo in range(0, len(allw), 128):
        hi = min(lo+128, len(allw))
        w = allw[lo:hi]
        _, inv, h, ce, den = inverse(model, w)
        f = drive[:, lo:hi]
        qf = np.einsum('pab,pf->abf', pp, f, optimize=True)
        if direct:
            qf *= h
        q = inv*qf
        x = spatial(s, q)
        ce_map = np.full((model.n, model.n), ce)
        if defect:
            site, mass, stiffness, extraction = defect
            ht, loadt, cet, _ = model.receiver(w, mass, stiffness, extraction)
            _, load, _, _ = model.receiver(w)
            phi = shape(s, [site])[0]
            greenq = inv * phi[:, :, None]
            gtt = np.einsum('ab,abf->f', phi, greenq)
            correction = (loadt-load)*x[site]/(1+(loadt-load)*gtt)
            q -= greenq*correction
            x = spatial(s, q)
            ce_map[site] = cet
        vrel = 1j*w*(h-1)*x
        if defect:
            vrel[site] = 1j*w*(ht-1)*x[site]
        if direct:
            for i, target in enumerate(targets):
                vrel[target] += 1j*w*f[i]/den
        weights = np.full(len(w), 2*dt/nt)
        if lo == 0:
            weights[0] *= .5
        if hi == len(allw):
            weights[-1] *= .5
        energy += ce_map * np.sum(np.abs(vrel)**2*weights, axis=-1)
        # Work from actual velocities at force ports; all passive dissipation.
        if direct:
            vp = np.array([1j*w*x[t] + vrel[t] for t in targets])
        else:
            vp = np.array([1j*w*x[t] for t in ports(model.n, drive.shape[0])])
        work += float(np.sum(np.real(np.conj(f)*vp)*weights))
        _, wn = model.basis()
        mp = model.density*model.thick*model.pitch**2
        loss += float(np.sum(2*model.zp*mp*wn[:, :, None]*np.abs(1j*w*q)**2*weights))
        # ce/(total c) differs for a defect; reconstruct intrinsic receiver loss.
        c0 = 2*model.zr*model.mr*2*np.pi*model.fr
        loss += float(np.sum((c0*(1-model.extract)+ce_map[:, :, None])*np.abs(vrel)**2*weights))
        for i, t in enumerate(targets):
            vt[i, lo:hi] = vrel[t]
    target_e = np.array([energy[t] for t in targets])
    mask = np.ones_like(energy, bool)
    if guard:
        mask[:guard] = False; mask[-guard:] = False
        mask[:, :guard] = False; mask[:, -guard:] = False
    for t in targets:
        mask[t] = False
    off = float(energy[mask].max())
    waves = np.fft.irfft(vt, n=nt, axis=-1)
    tail = np.sum(waves[:, 3*nt//4:]**2)/np.sum(waves**2)
    balance = abs(work-loss)/max(work, 1e-30)
    assert work > 0 and balance < 1e-8, (work, loss, balance)
    inner = mask.copy()
    inner[:4] = False; inner[-4:] = False
    inner[:, :4] = False; inner[:, -4:] = False
    return dict(interior_off_over_target=float(energy[inner].max()/target_e.min()) if inner.any() else None, target_J=float(target_e.min()), off_over_target=off/float(target_e.min()),
                target_fraction=float(target_e.sum()/work), input_J=work,
                force_squared_integral=float(dt*np.sum(np.fft.irfft(drive, n=nt, axis=-1)**2)),
                peak_target_velocity=float(np.max(np.abs(waves))), tail_fraction=float(tail),
                energy_balance_relative=balance,
                worst_site=[int(v) for v in np.unravel_index(np.argmax(np.where(mask, energy, -1)), energy.shape)]), energy


def independent_checks():
    # Dense physical-coordinate solve versus modal elimination, INCLUDING defect.
    m = Model(n=4, modes=4)
    s, wn = m.basis()
    p = np.kron(s, s)
    assert np.max(np.abs(p.T@p - np.eye(16))) < 1e-14
    w = np.array([2*np.pi*3700.])
    _, inv, h, _, _ = inverse(m, w)
    mp = m.density*m.thick*m.pitch**2
    k = (p*(mp*wn.ravel()**2))@p.T
    c = (p*(2*m.zp*mp*wn.ravel()))@p.T
    mass = np.full(16, m.mr); mass[6] *= 2
    kr = np.full(16, m.mr*(2*np.pi*m.fr)**2); kr[6] *= .7
    cr = np.full(16, 2*m.zr*m.mr*2*np.pi*m.fr)
    sr = np.diag(kr+1j*w[0]*cr)
    z = np.block([[k-w[0]**2*mp*np.eye(16)+1j*w[0]*c+sr, -sr],
                  [-sr, sr-w[0]**2*np.diag(mass)]])
    f = np.zeros(32); f[0] = 1
    dense = np.linalg.solve(z, f)
    x0 = p@(inv[:, :, 0].ravel()*p[0])
    g = p@(inv[:, :, 0].ravel()*p[6])
    _, l0, _, _ = m.receiver(w)
    hd, ld, _, _ = m.receiver(w, 2, .7)
    x = x0-g*(ld-l0)[0]*x0[6]/(1+(ld-l0)[0]*g[6])
    y = h[0]*x; y[6] = hd[0]*x[6]
    err = np.linalg.norm(np.r_[x,y]-dense)/np.linalg.norm(dense)
    assert err < 1e-11
    # Static added inertia vanishes.
    assert m.receiver(np.array([0.]))[1][0] == 0
    return dict(dense_defect_relative=err, static_load_zero=True)


def main():
    dt, nt = 1e-5, 8192
    model = Model()
    target = (19, 19)
    base = calibration(model, [target], dt, nt)
    def run(name, m=model, d=base, targets=[target], step=dt, samples=nt, **kw):
        row, energies = evaluate(m, d, targets, step, samples, **kw)
        print(json.dumps({name: row}), flush=True)
        return energies
    run('nominal')
    for name, m in [('plate_E_minus20', replace(model, young=1.6e9)),
                    ('plate_E_plus20', replace(model, young=2.4e9)),
                    ('plate_thickness_plus5', replace(model, thick=.00105)),
                    ('damping_low', replace(model, zp=.01, zr=.02)),
                    ('damping_high', replace(model, zp=.1, zr=.15)),
                    ('all_receivers_mass_double', replace(model, mr=2e-5, fr=model.fr/np.sqrt(2)))]:
        run(name, m=m)
    run('target_mass_double', defect=(target, 2., 1., 1.))
    run('target_spring_plus20', defect=(target, 1., 1.2, 1.))
    run('neighbor_extraction_x4', defect=((19,20), 1., 1., 4.))
    biased = replace(model, young=2.4e9)
    run('recalibrated_E_plus20', m=biased, d=calibration(biased, [target], dt, nt))
    # Direct local force on target receiver: expensive spatial addressing control.
    direct = np.zeros((1, nt)); ncmd = round(.002/dt)
    t = np.arange(ncmd)*dt
    direct[0,:ncmd] = np.sin(2*np.pi*model.fr*t)*np.sin(np.pi*t/.002)**2
    direct /= np.sqrt(dt*np.sum(direct**2))
    run('direct_receiver', d=np.fft.rfft(direct), direct=True)
    for modes in [20, 32]:
        m = replace(model, modes=modes)
        run('modes_'+str(modes), m=m, d=calibration(m,[target],dt,nt))
    cont = replace(model, lattice=False)
    run('continuum_dispersion', m=cont, d=calibration(cont,[target],dt,nt))
    for label, step, samples in [('dt_half',dt/2,nt*2), ('period_double',dt,nt*2)]:
        run(label, d=calibration(model,[target],step,samples), step=step,samples=samples)
    guardmodel = replace(model, n=48, modes=48)
    gt = (23,23)
    run('guarded_40x40', m=guardmodel, d=calibration(guardmodel,[gt],dt,nt), targets=[gt], guard=4)
    guardcont = replace(guardmodel, lattice=False)
    run('guarded_continuum', m=guardcont, d=calibration(guardcont,[gt],dt,nt), targets=[gt], guard=4)
    other = (9, 13)
    run('offcenter', d=calibration(model,[other],dt,nt), targets=[other])
    multi = [target, (9,9), (9,29), (29,29)]
    run('four_foci_fixed_force_budget',d=calibration(model,multi,dt,nt),targets=multi)
    print(json.dumps({'checks': independent_checks(), 'energy_envelope':
                     {str(r): (.8/1.2)*(.9/1.1)**2/sum(r**i for i in range(80)) for r in [0,.5,.9,.99,1.]}}))


if __name__ == '__main__':
    main()
