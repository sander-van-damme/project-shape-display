"""E-137: reciprocal crossbar, directed paths and serial work bounds.

Python 3 + NumPy. Deterministic epistemic scenarios; no calibrated process
prior, dynamic fluid model, geometry qualification or reliability inference.
Run with OPENBLAS_NUM_THREADS=1. JSON output is disposable.
"""
import json
import math

import numpy as np


def crossbar(g):
    """Unit selected pressure R0=1, C0=0; all other boundary ports sealed.

    Each cell is a reciprocal two-terminal dissipative transducer with q=g*dp.
    Return nodal pressures, signed cell flows and dissipated power.
    """
    n = len(g)
    lap = np.zeros((2*n, 2*n))
    for r in range(n):
        for c in range(n):
            i, j, k = r, n+c, g[r, c]
            lap[i, i] += k
            lap[j, j] += k
            lap[i, j] -= k
            lap[j, i] -= k
    free = [i for i in range(2*n) if i not in (0, n)]
    p = np.zeros(2*n)
    p[0] = 1
    if free:
        p[free] = np.linalg.solve(lap[np.ix_(free, free)], -lap[free, 0])
    residual = lap @ p
    assert np.max(np.abs(residual[free]), initial=0) < 1e-10
    dp = p[:n, None] - p[None, n:]
    q = g*dp
    power = g*dp**2
    assert np.isclose(power.sum(), q[0].sum(), rtol=1e-11)
    assert np.isclose(q[0].sum(), q[:, 0].sum(), rtol=1e-11)
    return p, dp, q, power


def simple_paths(n, source, sink, reciprocal):
    adjacency = {i: [] for i in range(2*n)}
    for r in range(n):
        for c in range(n):
            adjacency[r].append(n+c)
            if reciprocal:
                adjacency[n+c].append(r)
    def walk(node, seen):
        if node == sink:
            return 1
        return sum(walk(k, seen | {k}) for k in adjacency[node] if k not in seen)
    return walk(source, {source})


def run():
    # Independent symmetry solution, including n=1 limiting case.
    for n in (1, 2, 3, 8, 80):
        p, dp, q, power = crossbar(np.ones((n, n)))
        if n > 1:
            assert np.allclose(p[1:n], (n-1)/(2*n-1))
            assert np.allclose(p[n+1:], n/(2*n-1))
            assert np.isclose(np.max(np.abs(dp[1:, 1:])), 1/(2*n-1))
        assert np.isclose(power.sum()-power[0, 0], (n-1)**2/(2*n-1))

    n = 80
    r, c = np.indices((n, n))
    masks = {
        "uniform": np.ones((n, n)),
        "common_low": np.full((n, n), .8),
        "common_high": np.full((n, n), 1.2),
        "row_bias": np.where(r < n//2, .8, 1.2),
        "column_bias": np.where(c < n//2, .8, 1.2),
        "quadrant_bias": np.where((r < n//2) & (c < n//2), .8, 1.2),
        "alternating": np.where((r+c) % 2, .8, 1.2),
        "target_low": np.where((r == 0) & (c == 0), .8, 1.),
        "target_high": np.where((r == 0) & (c == 0), 1.2, 1.),
    }
    scenarios = {}
    for name, g in masks.items():
        p, dp, q, power = crossbar(g)
        off = np.ones_like(g, dtype=bool)
        off[0, 0] = False
        scenarios[name] = {
            "worst_off_dp_over_target": float(np.abs(dp[off]).max()),
            "worst_off_power_over_target": float(power[off].max()/power[0, 0]),
            "total_off_power_over_target": float(power[off].sum()/power[0, 0]),
            "nonzero_off_paths": int(np.count_nonzero(np.abs(q[off]) > 1e-12)),
        }

    # Boundary clamping cannot make every other edge zero: each three-edge
    # alternate path has signed drops summing to the target drop (one).
    # A=unselected row pressure, B=unselected column pressure.
    grid = np.linspace(0, 1, 301)
    a, b = np.meshgrid(grid, grid)
    worst = np.maximum.reduce([np.abs(1-b), np.abs(a), np.abs(b-a)])
    assert np.isclose(worst.min(), 1/3)
    assert np.all(worst >= 1/3-1e-14)

    paths = {}
    for reciprocal in (False, True):
        up = simple_paths(3, 0, 3, reciprocal)
        down = simple_paths(3, 3, 0, reciprocal)
        paths[str(reciprocal)] = {"forward": up, "reverse": down}
        assert (up, down) == ((1, 0) if not reciprocal else (9, 9))

    timing = []
    for speed in (.1, .4, 1.):
        for overhead in (.005, .020):
            cycle = .04/speed + overhead
            k = next(k for k in range(1, 6401) if 6+math.ceil(6400/k)*cycle < 30)
            timing.append({"speed_m_s": speed, "overhead_s": overhead,
                           "minimum_concurrent_paths": k,
                           "time_s": 6+math.ceil(6400/k)*cycle})

    # Rooted routing tree: sum(outdegree-1)=leaves-1. This counts local
    # junctions, NOT external actuators nor contact surfaces within a valve.
    trees = [{"max_fanout": d, "minimum_branch_junctions": math.ceil(6399/(d-1))}
             for d in (2, 4, 8, 80)]
    return {"scenarios": scenarios, "directed_3x3_paths": paths,
            "best_boundary_clamp_worst_dp": float(worst.min()),
            "timing": timing, "trees": trees,
            "checks": "KCL, power conservation, symmetry n=1/2/3/8/80, path enumeration, clamp bound"}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
