from collections import deque


def read_data(filename):
    with open(filename, "r") as f:
        grid = [list(line.strip()) for line in f]
    return grid


def find_char(grid, char):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == char:
                return (r, c)
    return None


def bfs(grid, start, end):
    rows = len(grid)
    cols = len(grid[0])
    q = deque([(start, 0, set())])  # (row, col), distance, visited
    while q:
        (r, c), dist, visited = q.popleft()
        if (r, c) == end:
            return dist
        if (r, c) in visited:
            continue
        visited.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                q.append(((nr, nc), dist + 1, set(visited)))
    return float("inf")


def part1(grid):
    start = find_char(grid, "S")
    end = find_char(grid, "E")
    rows = len(grid)
    cols = len(grid[0])

    shortest_path = bfs(grid, start, end)

    cheats_saving_100_or_more = 0

    for r1 in range(rows):
        for c1 in range(cols):
            if grid[r1][c1] != "#":
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    r2, c2 = r1 + dr, c1 + dc
                    if 0 <= r2 < rows and 0 <= c2 < cols and grid[r2][c2] == "#":
                        for dr2, dc2 in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            r3, c3 = r2 + dr2, c2 + dc2
                            if (
                                0 <= r3 < rows
                                and 0 <= c3 < cols
                                and grid[r3][c3] != "#"
                            ):
                                grid_copy = [row[:] for row in grid]
                                grid_copy[r2][c2] = "."
                                saved_time = shortest_path - bfs(grid_copy, start, end)
                                if saved_time >= 100:
                                    cheats_saving_100_or_more += 1
    return cheats_saving_100_or_more


def main():
    grid = read_data("20.txt")
    result = part1(grid)
    print(result)


if __name__ == "__main__":
    main()
