from typing import List, Tuple, Dict
from collections import deque
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))


class KeypadSolver:
    def __init__(self):
        # Define the numeric keypad layout
        self.numeric_keypad = {
            Position(0, 0): "7",
            Position(1, 0): "8",
            Position(2, 0): "9",
            Position(0, 1): "4",
            Position(1, 1): "5",
            Position(2, 1): "6",
            Position(0, 2): "1",
            Position(1, 2): "2",
            Position(2, 2): "3",
            Position(1, 3): "0",
            Position(2, 3): "A",
        }

        # Define the directional keypad layout
        self.directional_keypad = {
            Position(1, 0): "^",
            Position(2, 0): "A",
            Position(0, 1): "<",
            Position(1, 1): "v",
            Position(2, 1): ">",
        }

        # Define movement directions
        self.directions = {
            "^": Position(0, -1),
            "v": Position(0, 1),
            "<": Position(-1, 0),
            ">": Position(1, 0),
        }

    def is_valid_position(self, pos: Position, keypad: Dict[Position, str]) -> bool:
        return pos in keypad

    def find_shortest_sequence(self, target_code: str) -> Tuple[str, int]:
        # Start from level 3 (your keypad) down to level 1 (numeric keypad)
        sequence_level3 = self.bfs_level3(target_code)
        return sequence_level3, len(sequence_level3)

    def bfs_level3(self, target_code: str) -> str:
        start_pos = Position(2, 0)  # Start at 'A' button
        queue = deque(
            [(start_pos, "", "")]
        )  # (position, sequence, generated_level2_sequence)
        visited = set()

        while queue:
            pos, sequence, generated = queue.popleft()
            state = (pos, generated)

            if state in visited:
                continue
            visited.add(state)

            if self.verify_sequence_generates_code(generated, target_code):
                return sequence

            # Try each possible move
            for direction, move in self.directions.items():
                new_pos = pos + move

                if not self.is_valid_position(new_pos, self.directional_keypad):
                    continue

                # Try moving without activating
                queue.append((new_pos, sequence + direction, generated))

                # Try activating after moving
                if self.directional_keypad[new_pos] == "A":
                    queue.append(
                        (
                            new_pos,
                            sequence + direction + "A",
                            generated + direction + "A",
                        )
                    )

        return ""

    def verify_sequence_generates_code(
        self, level2_sequence: str, target_code: str
    ) -> bool:
        # Simulate level 2 robot to generate level 1 sequence
        level1_sequence = self.simulate_level2(level2_sequence)
        if not level1_sequence:
            return False

        # Simulate level 1 robot to generate the final code
        generated_code = self.simulate_level1(level1_sequence)
        return generated_code == target_code

    def simulate_level2(self, sequence: str) -> str:
        pos = Position(2, 0)  # Start at 'A'
        result = ""

        for char in sequence:
            if char in self.directions:
                pos = pos + self.directions[char]
                if not self.is_valid_position(pos, self.directional_keypad):
                    return ""
            elif char == "A":
                button = self.directional_keypad[pos]
                result += button

        return result

    def simulate_level1(self, sequence: str) -> str:
        pos = Position(2, 3)  # Start at 'A'
        result = ""

        for char in sequence:
            if char in self.directions:
                pos = pos + self.directions[char]
                if not self.is_valid_position(pos, self.numeric_keypad):
                    return ""
            elif char == "A":
                button = self.numeric_keypad[pos]
                result += button

        return result


def read_data(filename: str) -> List[str]:
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def part1(codes: List[str]) -> int:
    solver = KeypadSolver()
    total_complexity = 0

    for code in codes:
        sequence, length = solver.find_shortest_sequence(code)
        numeric_part = int("".join(c for c in code if c.isdigit()))
        complexity = length * numeric_part
        total_complexity += complexity

    return total_complexity


def main():
    codes = read_data("21.txt")
    result = part1(codes)
    print(f"Part 1: {result}")


if __name__ == "__main__":
    main()
