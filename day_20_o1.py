from collections import deque


def read_data(filename: str = "20.txt"):
    """
    Reads the puzzle input from '20.txt' and returns:
      - grid: list of lists of characters
      - (sr, sc): coordinates of 'S'
      - (er, ec): coordinates of 'E'
    """
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f]

    grid = []
    start = None
    end = None

    for r, row in enumerate(lines):
        grid.append(list(row))
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)

    return grid, start, end


def bfs_on_track(grid, start):
    """
    Performs a BFS on normal track only ('S', 'E', or '.') from 'start'.
    Returns a 2D list 'dist' where dist[r][c] is the cost to reach (r,c),
    or None if unreachable.
    """
    R = len(grid)
    C = len(grid[0])
    (sr, sc) = start

    dist = [[None] * C for _ in range(R)]
    dist[sr][sc] = 0

    queue = deque()
    queue.append((sr, sc))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C:
                # Check if it's track (or S/E which is also track)
                if grid[nr][nc] != "#" and dist[nr][nc] is None:
                    dist[nr][nc] = dist[r][c] + 1
                    queue.append((nr, nc))

    return dist


def part1(data) -> int:
    """
    Part 1: Cheating for up to 2 picoseconds.
    Returns how many cheats would save at least 100 picoseconds.
    """
    grid, (sr, sc), (er, ec) = data
    R = len(grid)
    C = len(grid[0])

    distS = bfs_on_track(grid, (sr, sc))  # cost from S to each cell
    distE = bfs_on_track(grid, (er, ec))  # cost from E to each cell
    dist_normal = distS[er][ec]
    if dist_normal is None:
        return 0  # No path at all => no cheats

    # Gather all track positions
    track_positions = [(r, c) for r in range(R) for c in range(C) if grid[r][c] != "#"]

    big_savers = set()

    # For each track cell T, if reachable from S, do BFS ignoring walls for up to 2 steps
    for r, c in track_positions:
        if distS[r][c] is None:
            continue

        base_cost_to_T = distS[r][c]

        # BFS ignoring walls up to distance=2
        visited_ignore_walls = [[None] * C for _ in range(R)]
        visited_ignore_walls[r][c] = 0
        queue = deque([(r, c)])

        while queue:
            rr, cc = queue.popleft()
            steps_so_far = visited_ignore_walls[rr][cc]
            if steps_so_far == 2:
                continue  # Can't go further than 2 steps ignoring walls

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < R and 0 <= nc < C:
                    if visited_ignore_walls[nr][nc] is None:
                        visited_ignore_walls[nr][nc] = steps_so_far + 1
                        queue.append((nr, nc))

        # Now, check all track positions that are reachable in up to 2 ignoring-walls steps
        for rr, cc in track_positions:
            steps = visited_ignore_walls[rr][cc]
            if steps is not None and 1 <= steps <= 2 and distE[rr][cc] is not None:
                cheat_cost = base_cost_to_T + steps + distE[rr][cc]
                time_saved = dist_normal - cheat_cost
                if time_saved >= 100:
                    big_savers.add(((r, c), (rr, cc)))

    return len(big_savers)


def part2(data) -> int:
    """
    Part 2: Cheating for up to 20 picoseconds.
    Returns how many cheats would save at least 100 picoseconds.
    """
    grid, (sr, sc), (er, ec) = data
    R = len(grid)
    C = len(grid[0])

    distS = bfs_on_track(grid, (sr, sc))  # cost from S to each cell
    distE = bfs_on_track(grid, (er, ec))  # cost from E to each cell
    dist_normal = distS[er][ec]
    if dist_normal is None:
        return 0  # No path at all => no cheats

    # Gather all track positions
    track_positions = [(r, c) for r in range(R) for c in range(C) if grid[r][c] != "#"]

    big_savers = set()

    # For each track cell T, if reachable from S, do BFS ignoring walls for up to 20 steps
    for r, c in track_positions:
        if distS[r][c] is None:
            continue

        base_cost_to_T = distS[r][c]

        # BFS ignoring walls up to distance=20
        dist_ignore = [[None] * C for _ in range(R)]
        dist_ignore[r][c] = 0
        queue = deque([(r, c)])

        while queue:
            rr, cc = queue.popleft()
            steps_so_far = dist_ignore[rr][cc]
            if steps_so_far == 20:
                continue  # Can't go beyond 20 cheat steps

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = rr + dr, cc + dc
                if 0 <= nr < R and 0 <= nc < C:
                    if dist_ignore[nr][nc] is None:
                        dist_ignore[nr][nc] = steps_so_far + 1
                        queue.append((nr, nc))

        # Now, check all track positions that are reachable in up to 20 ignoring-walls steps
        for rr, cc in track_positions:
            steps = dist_ignore[rr][cc]
            # We can end the cheat if 1 <= steps <= 20
            if steps is not None and 1 <= steps <= 20:
                if distE[rr][cc] is not None:
                    cheat_cost = base_cost_to_T + steps + distE[rr][cc]
                    time_saved = dist_normal - cheat_cost
                    if time_saved >= 100:
                        big_savers.add(((r, c), (rr, cc)))

    return len(big_savers)


def main():
    data = read_data("20.txt")

    answer1 = part1(data)
    print(answer1)

    # Part 2 (up to 20 picoseconds of cheating)
    answer2 = part2(data)
    print(answer2)


if __name__ == "__main__":
    main()
