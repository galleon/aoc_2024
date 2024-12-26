def parse_lock_heights(schematic: list[str]) -> list[int]:
    """
    Given a 7-line lock schematic (each line is 5 characters wide),
    compute the pin heights for each of the 5 columns.

    For locks:
      - The top row (schematic[0]) is always 'filled' (at least one '#'),
        and we skip it when computing heights.
      - Then from row 1..5, we count how many '#' appear consecutively
        from the top down for each column.
      - Stop counting as soon as we hit a '.' in that column.
    """
    heights = [0] * 5

    # We only consider rows 1..5 (inclusive). Row 6 is guaranteed all '.' for locks.
    # For each column, count consecutive '#' from row 1 downward.
    for col in range(5):
        h = 0
        for row in range(1, 6):
            if schematic[row][col] == "#":
                h += 1
            else:
                break
        heights[col] = h

    return heights


def parse_key_heights(schematic: list[str]) -> list[int]:
    """
    Given a 7-line key schematic, compute the pin heights for each of the 5 columns.

    For keys:
      - The bottom row (schematic[6]) is always 'filled' (at least one '#'),
        and we skip it when computing heights.
      - Then from row 5..0, count how many '#' appear consecutively
        from the bottom up for each column.
      - Stop counting as soon as we hit a '.' in that column.
    """
    heights = [0] * 5

    # We only consider rows 5..0 for measuring the shape,
    # skipping row 6 (which is guaranteed filled for keys).
    for col in range(5):
        h = 0
        for row in range(5, -1, -1):
            if schematic[row][col] == "#":
                h += 1
            else:
                break
        heights[col] = h

    return heights


def read_data() -> tuple[list[list[int]], list[list[int]]]:
    """
    Reads the file 25.txt in blocks of 7 lines.
    - Detects whether each block is a lock or a key:
      * lock => top row has at least one '#' AND bottom row is "....."
      * key  => top row is "....." AND bottom row has at least one '#'
    - Parses each block into a list of 5 heights.

    Returns:
      locks: a list of lock-height-lists
      keys:  a list of key-height-lists
    """
    with open("25.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    locks = []
    keys = []
    idx = 0
    total_lines = len(lines)

    while idx + 6 < total_lines:
        block = lines[idx : idx + 7]
        # Sometimes there could be blank lines between blocks; skip them.
        # Check if the block is actually 7 real lines or we hit empties.
        # If the top line is blank or we see that we can't parse a schematic, move on.
        # (We will do a simple check: if the length of the top line is not 5, skip.)
        if len(block[0]) != 5:
            idx += 1
            continue

        # Distinguish lock vs key by looking at top and bottom lines
        top_line = block[0]
        bottom_line = block[6]

        if top_line.count("#") > 0 and bottom_line == ".....":
            # It's a lock
            locks.append(parse_lock_heights(block))
        elif top_line == "....." and bottom_line.count("#") > 0:
            # It's a key
            keys.append(parse_key_heights(block))

        idx += 7

    return locks, keys


def part1(data: tuple[list[list[int]], list[list[int]]]) -> int:
    """
    Given (locks, keys), count how many unique lock/key pairs fit together
    without overlapping in any column.

    Overlap check:
      - For each column col, ensure lock_height[col] + key_height[col] <= 5.
      - If this is true for all columns, it's a valid pair.
    """
    locks, keys = data
    count = 0

    for lock in locks:
        for key in keys:
            # Check every column
            fits = True
            for col in range(5):
                if lock[col] + key[col] > 5:
                    fits = False
                    break
            if fits:
                count += 1

    return count


def main():
    data = read_data()
    answer = part1(data)
    print(answer)


if __name__ == "__main__":
    main()
