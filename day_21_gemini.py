import heapq


def read_data(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f]


def keypad_moves(start, target):
    keypad = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3),
    }
    reverse_keypad = {v: k for k, v in keypad.items()}
    q = [(0, start, "")]
    visited = {start}
    while q:
        dist, current, path = heapq.heappop(q)
        if current == target:
            return path
        x, y = keypad[current]
        for dx, dy, move in [(0, -1, "^"), (0, 1, "v"), (-1, 0, "<"), (1, 0, ">")]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < 3 and 0 <= ny < 4) and (nx, ny) in reverse_keypad:
                neighbor = reverse_keypad[(nx, ny)]
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(q, (dist + 1, neighbor, path + move))
    return None


def directional_moves(start, target):
    keypad = {
        "^": (1, 0),
        "A": (2, 0),
        "<": (0, 1),
        "v": (1, 1),
        ">": (2, 1),
    }
    reverse_keypad = {v: k for k, v in keypad.items()}
    q = [(0, start, "")]
    visited = {start}
    while q:
        dist, current, path = heapq.heappop(q)
        if current == target:
            return path
        x, y = keypad[current]
        for dx, dy, move in [(0, -1, "^"), (0, 1, "v"), (-1, 0, "<"), (1, 0, ">")]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < 3 and 0 <= ny < 2) and (nx, ny) in reverse_keypad:
                neighbor = reverse_keypad[(nx, ny)]
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(q, (dist + 1, neighbor, path + move))
    return None


def part1(codes):
    total_complexity = 0
    for code in codes:
        moves = ""
        current_pos = "A"
        for digit in code:
            path = keypad_moves(current_pos, digit)
            moves += path + "A"
            current_pos = digit

        moves_level2 = ""
        current_pos_level2 = "A"
        for move in moves:
            path = directional_moves(current_pos_level2, move)
            moves_level2 += path + "A"
            current_pos_level2 = move

        moves_level3 = ""
        current_pos_level3 = "A"
        for move in moves_level2:
            path = directional_moves(current_pos_level3, move)
            moves_level3 += path + "A"
            current_pos_level3 = move

        complexity = len(moves_level3) * int(code[:-1])
        total_complexity += complexity
    return total_complexity


def main():
    codes = read_data("21.txt")
    result = part1(codes)
    print(result)


if __name__ == "__main__":
    main()
