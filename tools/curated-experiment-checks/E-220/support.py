"""E-220: ideal support/state and necessary schedule screens; no hardware claims.

All motion, timing and fabrication inputs are labelled scenario assumptions.
Standard library; stdout only. No stochastic process or reliability priors.
"""
import itertools as it
import json
import math

HEIGHTS = (0, 10, 20, 30, 40)
DELTAS = (-40, -30, -20, -10, 10, 20, 30, 40)


def move(distance, acceleration, speed=200):
    d = abs(distance)
    return (2 * math.sqrt(d / acceleration) if d <= speed**2 / acceleration
            else d / speed + speed / acceleration)


def separable():
    maps = list(it.product(HEIGHTS, repeat=4))
    # For real-valued additive row/column stops the cycle identity is exact.
    additive = {h for h in maps if h[0]+h[3] == h[1]+h[2]}
    # Max maps have a representation with row/column values drawn from output
    # levels: replace each row/column input by its output row/column minimum.
    max_maps = {tuple(max(a[i], b[j]) for i in range(2) for j in range(2))
                for a in it.product(HEIGHTS, repeat=2)
                for b in it.product(HEIGHTS, repeat=2)}
    witness = (40, 0, 0, 40)
    assert witness not in additive and witness not in max_maps
    for h in maps:
        a = [min(h[2*i:2*i+2]) for i in range(2)]
        b = [min(h[j], h[2+j]) for j in range(2)]
        assert (h in max_maps) == (h == tuple(max(a[i], b[j])
                                             for i in range(2) for j in range(2)))
    return dict(total=len(maps), additive=len(additive), maximum=len(max_maps))


def rectangle_check(n):
    # Free cells = withdrawn rows AND withdrawn columns. Off-diagonal cells
    # must stay supported; grant an ideal selective lift on the free rectangle.
    allowed = {(i, i) for i in range(n)}
    largest = 0
    for rm, cm in it.product(range(1, 1 << n), repeat=2):
        freed = {(i, j) for i in range(n) for j in range(n)
                 if rm >> i & 1 and cm >> j & 1}
        if freed <= allowed:
            largest = max(largest, len(freed))
    assert largest == 1


def replay(old, target, fault=None):
    """One visited row; other rows stay on their row combs.

    Columns store height. Ground combs can seat at each 10-mm grid height.
    Reusable fingers at one datum acquire the selected groove. A nonzero
    delta group moves affinely on the shared lift. This is ideal contact
    algebra, not generated fork/comb geometry or a qualified sensor protocol.
    """
    height = list(old)
    row_closed = True
    col_closed = [True] * len(old)
    acquired = [False] * len(old)
    steps = 0
    for delta in DELTAS:
        group = [i for i in range(len(old)) if target[i]-old[i] == delta]
        if not group:
            continue
        # Row remains seated while selected column supports withdraw and
        # their linked reusable fingers acquire the same fixed-datum shelves.
        for i in group:
            col_closed[i] = False
            acquired[i] = True
        if fault == 'missing_capture':
            acquired[group[0]] = False
        if fault == 'missing_capture' or fault == 'missing_arrest':
            assert row_closed
            return False
        assert all(col_closed[i] or acquired[i] for i in range(len(old)))
        row_closed = False
        before = height[:]
        # Continuous path is affine: endpoint bounds/monotonicity are exact;
        # midpoint is an additional implementation check.
        for t in (0, .5, 1):
            for i in range(len(old)):
                height[i] = before[i] + (delta*t if i in group else 0)
                assert row_closed or col_closed[i] or acquired[i]
                assert min(old[i], target[i]) <= height[i] <= max(old[i], target[i])
                if old[i] == target[i]:
                    assert height[i] == old[i]
                if acquired[i]:
                    assert height[i] == old[i] + delta*t
        # Re-seat/prove row before freeing fingers or returning elevator.
        if fault == 'missing_row_seat':
            assert all(col_closed[i] or acquired[i] for i in range(len(old)))
            return False
        row_closed = True
        for i in group:
            assert height[i] in HEIGHTS
            acquired[i] = False
            col_closed[i] = True
        steps += 1
    assert height == list(target)
    return steps


def schedule(banks, acceleration, auxiliary, indexed=False, rows=80):
    # Concrete row-at-a-time implementation: every row contains all eight
    # signed deltas (possible in eight cells). No prepared mask credited.
    # Sequential loaded move, positive deposit, empty return for each group.
    loaded = sum((abs(d)*(move(1, acceleration)+.001) if indexed
                  else move(d, acceleration)) for d in DELTAS)
    reset = sum(move(d, acceleration) for d in DELTAS)
    row = loaded + reset + 8*auxiliary + move(5.08, acceleration)
    # 2 s map preparation/readback/settling plus one entire worst-row retry.
    return 2 + (math.ceil(rows/banks)+1)*row


def main():
    for n in range(2, 6):
        rectangle_check(n)
    checked = 0
    for old, target in it.product(it.product(HEIGHTS, repeat=3), repeat=2):
        replay(old, target)
        checked += 1
    old = tuple(max(0, -d) for d in DELTAS) * 10
    target = tuple(max(0, d) for d in DELTAS) * 10
    assert replay(old, target) == 8
    for fault in ('missing_capture', 'missing_arrest', 'missing_row_seat'):
        assert replay(old, target, fault) is False
    # Independent sum of the eight loaded distances: 200 mm; with reset 400.
    assert sum(map(abs, DELTAS)) == 200
    assert math.isclose(sum(2*move(d, 8000) for d in DELTAS), 2.4)
    assert math.isclose(move(5, 8000), .05)  # triangular/trapezoidal boundary
    assert move(0, 8000) == 0
    # Diagonal full-stroke mask: one-cell rectangles => >=80 lift/reset cycles,
    # even granting a fully parallel rectangle head and zero line overhead.
    diagonal = 80 * 2 * move(40, 8000)
    assert math.isclose(diagonal, 36)
    grid = []
    for indexed, a, aux in it.product((False, True), (2000, 8000), (.1, .25, .5)):
        survivors = [b for b in (1, 2, 4, 5, 8, 10, 16, 20, 40, 80)
                     if schedule(b, a, aux, indexed) < 30]
        b = survivors[0] if survivors else None
        grid.append(dict(indexed=indexed, acceleration=a, aux_s=aux, banks=b,
                         selector_axes=80*b if b else None,
                         seconds=schedule(b, a, aux, indexed) if b else None))
    # Two independently seated paths with opposed bounded vertical errors;
    # common row or column biases produce coherent, not IID, movement.
    errors = [dict(error=e, insertion_margin=1-e, takeover_bound=2*e,
                   minimum_lateral_land=1-e) for e in (.15, .35, .70)]
    print(json.dumps(dict(separable=separable(), ideal_three_cell_replays=checked,
                          diagonal_lift_reset_lower_seconds=diagonal,
                          schedule_grid=grid,
                          fast16_aux_sensitivity={str(x):schedule(16,8000,x)
                                                 for x in (.1,.25,.5,1)},
                          error_scenarios=errors), indent=2))


if __name__ == '__main__':
    main()
