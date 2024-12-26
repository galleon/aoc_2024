import re


def read_data(filename):
    with open(filename, "r") as f:
        data = f.read().strip().split("\n\n")

    locks = []
    keys = []
    for block in data:
        lines = block.splitlines()
        if lines[0].startswith("."):
            # Key
            heights = []
            for j in range(len(lines[0])):
                height = 0
                for i in range(len(lines) - 1, -1, -1):
                    if lines[i][j] == "#":
                        height = len(lines) - 1 - i
                        break
                heights.append(height)
            keys.append(heights)
        else:
            # Lock
            heights = []
            for j in range(len(lines[0])):
                height = 0
                for i in range(len(lines)):
                    if lines[i][j] == ".":
                        height = i
                        break
                heights.append(height)
            locks.append(heights)
    return locks, keys


def part1(data):
    locks, keys = data
    count = 0
    for lock in locks:
        for key in keys:
            fit = True
            for i in range(len(lock)):
                if lock[i] + key[i] > 6:  # Total space is 6
                    fit = False
                    break
            if fit:
                count += 1
    return count


def main():
    locks, keys = read_data("25.txt")
    result1 = part1((locks, keys))
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
