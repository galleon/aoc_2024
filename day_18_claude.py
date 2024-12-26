from collections import deque
from typing import List, Set, Tuple


def read_data(filename: str) -> List[Tuple[int, int]]:
    coordinates = []
    with open(filename) as f:
        for line in f:
            x, y = map(int, line.strip().split(","))
            coordinates.append((x, y))
    return coordinates


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def has_path(corrupted: Set[Tuple[int, int]], grid_size: int) -> bool:
    start = (0, 0)
    end = (grid_size, grid_size)
    queue = deque([(start, 0)])
    visited = {start}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return True

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)

            if (
                0 <= new_x <= grid_size
                and 0 <= new_y <= grid_size
                and new_pos not in corrupted
                and new_pos not in visited
            ):
                remaining_dist = manhattan_distance(new_x, new_y, end[0], end[1])
                if steps + 1 + remaining_dist < len(corrupted):
                    queue.append((new_pos, steps + 1))
                    visited.add(new_pos)

    return False


def part1(coordinates: List[Tuple[int, int]], grid_size: int = 70) -> int:
    corrupted = set(coordinates[:1024])
    start = (0, 0)
    end = (grid_size, grid_size)
    queue = deque([(start, 0)])
    visited = {start}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while queue:
        (x, y), steps = queue.popleft()

        if (x, y) == end:
            return steps

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            new_pos = (new_x, new_y)

            if (
                0 <= new_x <= grid_size
                and 0 <= new_y <= grid_size
                and new_pos not in corrupted
                and new_pos not in visited
            ):
                remaining_dist = manhattan_distance(new_x, new_y, end[0], end[1])
                if steps + 1 + remaining_dist < len(corrupted):
                    queue.append((new_pos, steps + 1))
                    visited.add(new_pos)

    return -1


def part2(coordinates: List[Tuple[int, int]], grid_size: int = 70) -> str:
    corrupted = set()

    # Binary search for approximate blocking point
    left, right = 0, len(coordinates)
    first_blocking = len(coordinates)

    while left < right:
        mid = (left + right) // 2
        corrupted = set(coordinates[:mid])

        if has_path(corrupted, grid_size):
            left = mid + 1
        else:
            first_blocking = mid
            right = mid

    # Linear search around the blocking point to find exact coordinate
    corrupted = set(coordinates[: first_blocking - 1])
    for i in range(
        max(0, first_blocking - 100), min(first_blocking + 100, len(coordinates))
    ):
        corrupted.add(coordinates[i])
        if not has_path(corrupted, grid_size):
            return f"{coordinates[i][0]},{coordinates[i][1]}"

    return "No blocking coordinate found"


def main():
    data = read_data("18.txt")
    result1 = part1(data)
    result2 = part2(data)
    print(result1)
    print(result2)


if __name__ == "__main__":
    main()
