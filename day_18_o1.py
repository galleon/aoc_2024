from collections import deque


def read_data(filename: str = "18.txt") -> list[tuple[int, int]]:
    """
    Reads at most the first 1024 lines from the file 18.txt.
    Each line contains 'X,Y'.
    Returns a list of (x, y) tuples.
    """
    coords = []
    with open(filename, "r", encoding="utf-8") as f:
        for _ in range(1024):  # Read at most 1024 lines
            line = f.readline()
            if not line:
                break
            x_str, y_str = line.strip().split(",")
            x, y = int(x_str), int(y_str)
            coords.append((x, y))
    return coords


def part1(coords: list[tuple[int, int]]) -> int | None:
    """
    Given a list of up to 1024 (x, y) coordinates that become corrupted,
    find the shortest path from (0,0) to (70,70) on a 71x71 grid,
    where corrupted cells are impassable.
    Return the number of steps if reachable, else None.
    """

    SIZE = 71  # grid is 0..70 in both directions
    # Mark corrupted cells
    corrupted = [[False] * SIZE for _ in range(SIZE)]
    for x, y in coords:
        if 0 <= x < SIZE and 0 <= y < SIZE:
            corrupted[y][x] = True

    # If start or end is already corrupted, there's no path
    if corrupted[0][0] or corrupted[70][70]:
        return None

    # Distance array initialized to -1 (unvisited)
    dist = [[-1] * SIZE for _ in range(SIZE)]
    dist[0][0] = 0  # distance to start is 0

    # Standard BFS
    queue = deque()
    queue.append((0, 0))

    # Movements: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        cx, cy = queue.popleft()
        # If we've reached the exit, return the distance
        if (cx, cy) == (70, 70):
            return dist[cy][cx]
        # Check neighbors
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                if not corrupted[ny][nx] and dist[ny][nx] == -1:
                    dist[ny][nx] = dist[cy][cx] + 1
                    queue.append((nx, ny))

    # If we exhaust the BFS without finding (70,70), no path exists
    return None


def main():
    coords = read_data("18.txt")
    answer = part1(coords)
    print(answer if answer is not None else "No path found")


if __name__ == "__main__":
    main()
