import sys
import re
import heapq
import pyperclip as pc


def pr(s):
    print(s)
    pc.copy(s)


sys.setrecursionlimit(10**6)
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left

pad1 = ["789", "456", "123", " 0A"]
pad2 = [" ^A", "<v>"]


def read_data(file_path):
    """
    Reads input data from the given file path.
    Args:
        file_path (str): Path to the input file.
    Returns:
        list[str]: List of strings representing input lines.
    """
    with open(file_path, "r") as file:
        data = file.read().strip().split("\n")
    return data


def ints(s):
    return [int(x) for x in re.findall("-?\d+", s)]


def getPad1(p1):
    r, c = p1
    if not (0 <= r < len(pad1) and 0 <= c < len(pad1[r])):
        return None
    if pad1[r][c] == " ":
        return None
    return pad1[r][c]


def getPad2(p):
    r, c = p
    if not (0 <= r < len(pad2) and 0 <= c < len(pad2[r])):
        return None
    if pad2[r][c] == " ":
        return None
    return pad2[r][c]


def applyPad1(p, move):
    if move == "A":
        return (p, getPad1(p))
    elif move == "<":
        return ((p[0], p[1] - 1), None)
    elif move == "^":
        return ((p[0] - 1, p[1]), None)
    elif move == ">":
        return ((p[0], p[1] + 1), None)
    elif move == "v":
        return ((p[0] + 1, p[1]), None)


def applyPad2(p, move):
    if move == "A":
        return (p, getPad2(p))
    elif move == "<":
        return ((p[0], p[1] - 1), None)
    elif move == "^":
        return ((p[0] - 1, p[1]), None)
    elif move == ">":
        return ((p[0], p[1] + 1), None)
    elif move == "v":
        return ((p[0] + 1, p[1]), None)


def solve1(code, pads):
    start = [0, (3, 2), "A", "", ""]
    Q = []
    heapq.heappush(Q, start)
    SEEN = {}
    while Q:
        d, p1, p2, out, path = heapq.heappop(Q)
        if out == code:
            return d
        if not code.startswith(out):
            continue
        if getPad1(p1) is None:
            continue
        key = (p1, p2, out)
        if key in SEEN:
            continue
        SEEN[key] = d
        for move in ["^", "<", "v", ">", "A"]:
            new_p1 = p1
            new_out = out
            new_p1, output = applyPad1(p1, move)
            if output is not None:
                new_out = out + output
            cost_move = cost2(move, p2, pads)
            heapq.heappush(Q, [d + cost_move, new_p1, move, new_out, path])


DP = {}


def cost2(ch, prev_move, pads):
    key = (ch, prev_move, pads)
    if key in DP:
        return DP[key]
    if pads == 0:
        return 1
    else:
        Q = []
        start_pos = {"^": (0, 1), "<": (1, 0), "v": (1, 1), ">": (1, 2), "A": (0, 2)}[
            prev_move
        ]
        heapq.heappush(Q, [0, start_pos, "A", "", ""])
        SEEN = {}
        while Q:
            d, p, prev, out, path = heapq.heappop(Q)
            if getPad2(p) is None:
                continue
            if out == ch:
                DP[key] = d
                return d
            seen_key = (p, prev)
            if seen_key in SEEN:
                continue
            SEEN[seen_key] = d
            for move in ["^", "<", "v", ">", "A"]:
                new_p, output = applyPad2(p, move)
                cost_move = cost2(move, prev, pads - 1)
                new_d = d + cost_move
                heapq.heappush(Q, [new_d, new_p, move, out + (output or ""), path])


def part1(data):
    """
    Solves part 1 of the problem.
    Args:
        data (list[str]): Input data.
    Returns:
        int: Solution to part 1.
    """
    total = 0
    for line in data:
        s1 = solve1(line, 2)
        line_int = ints(line)[0]
        total += line_int * s1
    return total


def part2(data):
    """
    Solves part 2 of the problem.
    Args:
        data (list[str]): Input data.
    Returns:
        int: Solution to part 2.
    """
    total = 0
    for line in data:
        s2 = solve1(line, 25)
        line_int = ints(line)[0]
        total += line_int * s2
    return total


def main():
    """
    Main function to read input and print solutions for part 1 and part 2.
    """
    data = read_data("21.txt")
    solution1 = part1(data)
    pr(solution1)
    solution2 = part2(data)
    pr(solution2)


if __name__ == "__main__":
    main()
