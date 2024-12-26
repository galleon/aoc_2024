def read_data(filename):
    with open(filename) as f:
        content = f.read().strip()

    sections = content.split("\n\n")
    locks = []
    keys = []

    for section in sections:
        lines = section.strip().split("\n")
        # Check if it's a lock (top row filled) or key (bottom row filled)
        is_lock = "#" in lines[0]
        heights = []

        for col in range(len(lines[0])):
            height = 0
            for row in range(len(lines)):
                if lines[row][col] == "#":
                    if is_lock:
                        height = len(lines) - row - 1
                        break
                    else:
                        height = row
            heights.append(height)

        if is_lock:
            locks.append(tuple(heights))
        else:
            keys.append(tuple(heights))

    return locks, keys


def part1(data):
    locks, keys = data
    valid_pairs = 0

    # For each lock-key pair, check if heights sum exceeds available space
    for lock in locks:
        for key in keys:
            if all(l + k <= len(lock) for l, k in zip(lock, key)):
                valid_pairs += 1

    return valid_pairs


def main():
    data = read_data("25.txt")
    result = part1(data)
    print(result)


if __name__ == "__main__":
    main()
