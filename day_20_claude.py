from collections import defaultdict, deque
from dataclasses import dataclass
from typing import List, Set, Dict
import heapq


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class RaceTrack:
    def __init__(self, grid: List[str]):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.start = self._find_point("S")
        self.end = self._find_point("E")
        # Replace S and E with . for easier navigation
        row = list(self.grid[self.start.y])
        row[self.start.x] = "."
        self.grid[self.start.y] = "".join(row)
        row = list(self.grid[self.end.y])
        row[self.end.x] = "."
        self.grid[self.end.y] = "".join(row)

    def _find_point(self, char: str) -> Point:
        for y, row in enumerate(self.grid):
            if char in row:
                return Point(row.index(char), y)
        raise ValueError(f"Character {char} not found in grid")

    def is_valid(self, p: Point) -> bool:
        return 0 <= p.x < self.width and 0 <= p.y < self.height

    def is_wall(self, p: Point) -> bool:
        return self.grid[p.y][p.x] == "#"

    def get_neighbors(self, p: Point) -> List[Point]:
        directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
        return [p + d for d in directions if self.is_valid(p + d)]


def read_data(filename: str = "20.txt") -> RaceTrack:
    with open(filename) as f:
        return RaceTrack([line.strip() for line in f])


def find_shortest_path(track: RaceTrack) -> int:
    """Find shortest path from start to end without cheating"""
    queue = [(0, track.start)]
    seen = {track.start}

    while queue:
        steps, pos = heapq.heappop(queue)
        if pos == track.end:
            return steps

        for next_pos in track.get_neighbors(pos):
            if next_pos not in seen and not track.is_wall(next_pos):
                seen.add(next_pos)
                heapq.heappush(queue, (steps + 1, next_pos))
    return float("inf")


def find_all_cheats(track: RaceTrack, base_time: int) -> Dict[int, int]:
    """
    Find all possible cheats and group them by time saved.
    Returns a dict mapping time_saved -> count of cheats
    """
    savings = defaultdict(int)
    seen_cheats = set()

    # Try every possible starting point for the cheat
    for y in range(track.height):
        for x in range(track.width):
            if track.grid[y][x] == "#":
                continue

            start = Point(x, y)
            # Find all possible end points after 1-2 moves through walls
            end_points = find_cheat_endpoints(track, start)

            for end in end_points:
                if (start, end) in seen_cheats:
                    continue

                # Calculate time saved by this cheat
                saved = calculate_time_saved(track, start, end, base_time)
                if saved > 0:
                    savings[saved] += 1
                    seen_cheats.add((start, end))

    return savings


def find_cheat_endpoints(track: RaceTrack, start: Point) -> Set[Point]:
    """Find all possible endpoints after 1-2 moves through walls"""
    endpoints = set()

    # BFS for 2 steps, allowing wall passage
    queue = deque([(start, 0)])
    seen = {start}

    while queue:
        pos, steps = queue.popleft()
        if steps == 2:
            if not track.is_wall(pos):
                endpoints.add(pos)
            continue

        for next_pos in track.get_neighbors(pos):
            if next_pos not in seen:
                seen.add(next_pos)
                queue.append((next_pos, steps + 1))

                # Single-step cheats are also valid
                if steps == 0 and not track.is_wall(next_pos):
                    endpoints.add(next_pos)

    return endpoints


def calculate_time_saved(
    track: RaceTrack, cheat_start: Point, cheat_end: Point, base_time: int
) -> int:
    """Calculate how much time is saved by using this cheat"""
    # Find time to reach cheat start
    time_to_start = find_shortest_path_to(track, track.start, cheat_start)
    if time_to_start == float("inf"):
        return 0

    # Find time from cheat end to finish
    time_from_end = find_shortest_path_to(track, cheat_end, track.end)
    if time_from_end == float("inf"):
        return 0

    # Calculate cheat distance (Manhattan distance)
    cheat_distance = abs(cheat_end.x - cheat_start.x) + abs(cheat_end.y - cheat_start.y)

    total_time = time_to_start + cheat_distance + time_from_end
    return max(0, base_time - total_time)


def find_shortest_path_to(track: RaceTrack, start: Point, end: Point) -> int:
    """Find shortest path between two points without cheating"""
    queue = [(0, start)]
    seen = {start}

    while queue:
        steps, pos = heapq.heappop(queue)
        if pos == end:
            return steps

        for next_pos in track.get_neighbors(pos):
            if next_pos not in seen and not track.is_wall(next_pos):
                seen.add(next_pos)
                heapq.heappush(queue, (steps + 1, next_pos))
    return float("inf")


def part1(track: RaceTrack) -> int:
    # First find the base time without cheating
    base_time = find_shortest_path(track)

    # Find all possible cheats
    savings = find_all_cheats(track, base_time)

    # Count cheats that save >= 100 picoseconds
    return sum(count for saved, count in savings.items() if saved >= 100)


def main():
    track = read_data()
    result = part1(track)
    print(f"Number of cheats saving >=100 picoseconds: {result}")


if __name__ == "__main__":
    main()
