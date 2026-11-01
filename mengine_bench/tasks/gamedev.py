"""Gamedev tasks: Pixel Arena flavored, Terminal-Bench style gold.

The agent edits real code and runs tests; the gold runs hidden unittest code
it never saw, so a change that only satisfies the visible test still fails.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

from mengine_bench.core import (
    CheckResult,
    EvalTask,
    Step,
    read,
    checkpoints,
    run_hidden_tests,
    write,
)

# ---------------------------------------------------------- gd-astar-doors --

ASTAR_STUB = '''"""Pixel Arena level pathing: bots walk a tile map painted in primary colors."""

Cell = tuple[int, int]  # (row, col)


def find_path(grid: list[str]) -> list[Cell] | None:
    """Cheapest 4-neighbour path from 'S' to 'G', both inclusive.

    '.' floor costs 1 to enter, 'D' door costs 3, '#' is a wall, 'S'/'G' cost 1.
    Return None when G is unreachable.
    """
    raise NotImplementedError
'''

ASTAR_VISIBLE = '''import unittest

from pathfind import find_path


class VisibleTest(unittest.TestCase):
    def test_straight_corridor(self):
        self.assertEqual(find_path(["S..G"]), [(0, 0), (0, 1), (0, 2), (0, 3)])


if __name__ == "__main__":
    unittest.main()
'''

ASTAR_HIDDEN = '''import heapq
import unittest

from pathfind import find_path

COST = {".": 1, "S": 1, "G": 1, "D": 3}


def locate(grid, ch):
    for r, row in enumerate(grid):
        c = row.find(ch)
        if c >= 0:
            return (r, c)


def optimal(grid):
    s, g = locate(grid, "S"), locate(grid, "G")
    best = {s: 0}
    heap = [(0, s)]
    while heap:
        d, (r, c) = heapq.heappop(heap)
        if (r, c) == g:
            return d
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#":
                nd = d + COST[grid[nr][nc]]
                if nd < best.get((nr, nc), 1e9):
                    best[(nr, nc)] = nd
                    heapq.heappush(heap, (nd, (nr, nc)))
    return None


def cost_of(grid, path):
    total = 0
    for (r0, c0), (r1, c1) in zip(path, path[1:]):
        assert abs(r0 - r1) + abs(c0 - c1) == 1, "non-adjacent step"
        assert grid[r1][c1] != "#", "walks through a wall"
        total += COST[grid[r1][c1]]
    return total


class HiddenTest(unittest.TestCase):
    def assert_cheapest(self, *grids):
        for grid in grids:
            best = optimal(grid)
            path = find_path(list(grid))
            if best is None:
                self.assertIsNone(path, grid)
                continue
            self.assertIsNotNone(path, grid)
            self.assertEqual(path[0], locate(grid, "S"))
            self.assertEqual(path[-1], locate(grid, "G"))
            self.assertEqual(cost_of(grid, path), best, grid)

    def test_plain_floor(self):
        self.assert_cheapest(["S..G"])

    def test_walks_around_door(self):
        self.assert_cheapest(["SDDDG", "....."])

    def test_takes_door(self):
        self.assert_cheapest(["S..D..G"], ["S.......", "#######D", "G.......", "........"])

    def test_dead_ends(self):
        self.assert_cheapest(["S.#.....", "..#.###.", "..D...#G", "####..#."],
                             ["S#......", ".#.####.", ".#.#..#.", ".D.#G.#.", "...####.", "........"])

    def test_unreachable(self):
        self.assert_cheapest(["S.#", "###", "..G"])


if __name__ == "__main__":
    unittest.main()
'''

ASTAR_REFERENCE = '''import heapq

Cell = tuple[int, int]
COST = {".": 1, "S": 1, "G": 1, "D": 3}


def find_path(grid):
    start = goal = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
    dist = {start: 0}
    prev = {}
    heap = [(0, start)]
    while heap:
        d, cell = heapq.heappop(heap)
        if cell == goal:
            path = [cell]
            while path[-1] != start:
                path.append(prev[path[-1]])
            return path[::-1]
        if d > dist[cell]:
            continue
        r, c = cell
        for nxt in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            nr, nc = nxt
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#":
                nd = d + COST[grid[nr][nc]]
                if nd < dist.get(nxt, 1 << 30):
                    dist[nxt] = nd
                    prev[nxt] = cell
                    heapq.heappush(heap, (nd, nxt))
    return None
'''


def _astar_setup(ws: Path) -> None:
    write(ws, "pathfind.py", ASTAR_STUB)
    write(ws, "test_pathfind.py", ASTAR_VISIBLE)


ASTAR_CASES = (("plain floor", "test_plain_floor"), ("walks around a door when that is cheaper", "test_walks_around_door"),
               ("takes a door when it is the way", "test_takes_door"), ("finds the way past dead ends", "test_dead_ends"),
               ("returns None when G is unreachable", "test_unreachable"))


def _astar_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    # #82: one case per check, so a failure names what went wrong and earns the rest.
    for case, method in ASTAR_CASES:
        selection = f"\n\ndef load_tests(loader, tests, pattern):\n    return unittest.TestSuite([HiddenTest('{method}')])\n"
        ok, why = run_hidden_tests(ws, ASTAR_HIDDEN + selection)
        result.add(f"hidden {case}", ok, why)
    return result


def _astar_reference(ws: Path) -> list[str]:
    write(ws, "pathfind.py", ASTAR_REFERENCE)
    return ["done"]


# ------------------------------------------------------ gd-ecs-collision --

ECS_FILES = {
    "arena_ecs/__init__.py": "",
    "arena_ecs/components.py": '''from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    x: float
    y: float


@dataclass
class Box:
    w: float
    h: float
''',
    "arena_ecs/world.py": '''class World:
    def __init__(self):
        self.entities = {}
        self._next = 1

    def spawn(self, **components):
        eid = self._next
        self._next += 1
        self.entities[eid] = dict(components)
        return eid

    def query(self, *names):
        for eid, comps in self.entities.items():
            if all(name in comps for name in names):
                yield eid, comps
''',
    "arena_ecs/systems/__init__.py": "",
    "arena_ecs/systems/movement.py": '''def movement_system(world, dt):
    for _, comps in world.query("pos", "vel"):
        pos, vel = comps["pos"], comps["vel"]
        pos.x += vel.x * dt
        pos.y += vel.x * dt
''',
    "arena_ecs/systems/collision.py": '''def overlaps(pa, ba, pb, bb):
    """Axis-aligned boxes anchored at their top-left corner; touching edges do not collide."""
    return (
        pa.x < pb.x + bb.w
        and pa.x + ba.w > pb.x
        and pa.y < pb.y + bb.h
        and pa.y + ba.h > pa.y
    )


def collision_system(world):
    hits = []
    bodies = list(world.query("pos", "box"))
    for i, (ea, ca) in enumerate(bodies):
        for eb, cb in bodies[i + 1:]:
            if overlaps(ca["pos"], ca["box"], cb["pos"], cb["box"]):
                hits.append((ea, eb))
    return hits
''',
    "tests/test_systems.py": '''import unittest

from arena_ecs.components import Box, Position, Velocity
from arena_ecs.systems.collision import collision_system
from arena_ecs.systems.movement import movement_system
from arena_ecs.world import World


class SystemsTest(unittest.TestCase):
    def test_movement_uses_each_axis(self):
        world = World()
        eid = world.spawn(pos=Position(0, 0), vel=Velocity(2, -1))
        movement_system(world, 0.5)
        pos = world.entities[eid]["pos"]
        self.assertEqual((pos.x, pos.y), (1.0, -0.5))

    def test_vertical_gap_is_not_a_hit(self):
        world = World()
        world.spawn(pos=Position(0, 0), box=Box(1, 1))
        world.spawn(pos=Position(0, 5), box=Box(1, 1))
        self.assertEqual(collision_system(world), [])


if __name__ == "__main__":
    unittest.main()
''',
}

ECS_HIDDEN = '''import unittest

from arena_ecs.components import Box, Position, Velocity
from arena_ecs.systems.collision import collision_system
from arena_ecs.systems.movement import movement_system
from arena_ecs.world import World


class MovementTests(unittest.TestCase):
    def test_each_axis_and_multiple_steps(self):
        world = World()
        eid = world.spawn(pos=Position(1, 10), vel=Velocity(2, -4))
        movement_system(world, 2.0)
        pos = world.entities[eid]["pos"]
        self.assertEqual((pos.x, pos.y), (5.0, 2.0))
        movement_system(world, 0.5)
        self.assertEqual((pos.x, pos.y), (6.0, 0.0))


def pairs(world):
    return {frozenset(pair) for pair in collision_system(world)}


def collide(first, second):
    world = World()
    for (x, y), (w, h) in (first, second):
        world.spawn(pos=Position(x, y), box=Box(w, h))
    return bool(pairs(world))


class CollisionTests(unittest.TestCase):
    def test_overlap_matrix(self):
        a = ((0, 0), (2, 2))
        cases = [((1, 1), True), ((2, 0), False), ((0, 2), False), ((-1.5, 1.5), True),
                 ((0, 3), False), ((0, -1.9), True), ((-2, 0), False), ((0, -2), False)]
        for at, expected in cases:
            self.assertEqual(collide(a, (at, (2, 2))), expected, at)

    def test_different_box_sizes(self):
        a = ((0, 0), (2, 2))
        cases = [((-3, 0), (4, 1), True), ((-1.5, 0), (1, 1), False),
                 ((0, -3), (1, 4), True), ((0, -1.5), (1, 1), False)]
        for at, size, expected in cases:
            self.assertEqual(collide(a, (at, size)), expected, (at, size))
            self.assertEqual(collide((at, size), a), expected, (at, size))

    def test_collision_pairs(self):
        world = World()
        a = world.spawn(pos=Position(0, 2), box=Box(1, 1))
        b = world.spawn(pos=Position(0, 0), box=Box(1, 1))
        self.assertEqual(pairs(world), set())
        world.entities[a]["pos"].y = 0
        self.assertEqual(pairs(world), {frozenset((a, b))})


if __name__ == "__main__":
    unittest.main()
'''


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _ecs_setup(ws: Path) -> None:
    for rel, text in ECS_FILES.items():
        write(ws, rel, text)


def _ecs_check(ws: Path, answers: Sequence[str]) -> CheckResult:
    result = CheckResult()
    untouched = _sha(read(ws, "tests/test_systems.py") or "") == _sha(ECS_FILES["tests/test_systems.py"])
    result.mandatory.append(("visible tests left untouched", untouched))
    for name, case in (("movement", "MovementTests"), ("collision", "CollisionTests")):
        selection = f"\n\ndef load_tests(loader, tests, pattern):\n    return loader.loadTestsFromTestCase({case})\n"
        ok, why = run_hidden_tests(ws, ECS_HIDDEN + selection)
        result.add(f"hidden {name}", ok, why)
    return result


def _ecs_reference(ws: Path) -> list[str]:
    move = ECS_FILES["arena_ecs/systems/movement.py"].replace("pos.y += vel.x * dt", "pos.y += vel.y * dt")
    coll = ECS_FILES["arena_ecs/systems/collision.py"].replace("pa.y + ba.h > pa.y", "pa.y + ba.h > pb.y")
    write(ws, "arena_ecs/systems/movement.py", move)
    write(ws, "arena_ecs/systems/collision.py", coll)
    return ["fixed movement.py:5 and collision.py:8"]


TESTS_RUN = ("ran the tests", r"unittest|pytest")

TASKS = [
    EvalTask(
        id="gd-astar-doors", category="gamedev",
        provenance="Terminal-Bench style: implement + hidden tests; weighted doors on a Pixel Arena tile map",
        summary="Make units find the cheapest route across a game map where doors cost more to cross.",
        setup=_astar_setup, check=_astar_check, reference=_astar_reference, timeout_s=300,
        checkpoints=checkpoints(("read the module", r"pathfind"), TESTS_RUN),
        steps=(Step("Units in our tile game cannot find their way yet: find_path in {WS}/pathfind.py is still empty. Make it "
                    "work as its docstring says. The project takes no new dependencies."),),
    ),
    EvalTask(
        id="gd-ecs-collision-bug", category="gamedev",
        provenance="SWE-bench style debug: two planted bugs across an ECS package; visible tests must stay untouched",
        summary="Find out why units move and collide wrong in a small game codebase, and fix it.",
        setup=_ecs_setup, check=_ecs_check, reference=_ecs_reference, timeout_s=300,
        checkpoints=checkpoints(TESTS_RUN, ("read movement", r"movement"), ("read collision", r"collision")),
        steps=(Step("Playtesters say units in {WS}/arena_ecs drift and collide wrong, and the tests in {WS}/tests fail. Find out "
                    "why and fix it. The tests describe the behavior we want, so they stay as they are, and the project takes "
                    "no new dependencies."),),
    ),
]
