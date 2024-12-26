from typing import Dict, Tuple, List
import re


def read_data(filename: str) -> Tuple[Dict[str, int], List[str]]:
    """
    Read and parse the input file containing initial wire values and gate definitions.
    Returns a tuple of (initial_values, gate_definitions).
    """
    initial_values = {}
    gate_definitions = []

    with open(filename, "r") as f:
        # Read until empty line
        while True:
            line = f.readline().strip()
            if not line:
                break

            wire, value = line.split(": ")
            initial_values[wire] = int(value)

        # Read gate definitions
        for line in f:
            if line.strip():
                gate_definitions.append(line.strip())

    return initial_values, gate_definitions


def evaluate_gate(gate_type: str, input1: int, input2: int) -> int:
    """Evaluate a logic gate given its type and input values."""
    if gate_type == "AND":
        return input1 & input2
    elif gate_type == "OR":
        return input1 | input2
    elif gate_type == "XOR":
        return input1 ^ input2
    raise ValueError(f"Unknown gate type: {gate_type}")


def part1(data: Tuple[Dict[str, int], List[str]]) -> int:
    """
    Simulate the logic circuit and return the decimal number represented by z-wires.
    """
    initial_values, gate_definitions = data
    wire_values = initial_values.copy()

    # Parse gate definitions into a more usable format
    gates = []
    for definition in gate_definitions:
        # Extract input wires, gate type, and output wire
        match = re.match(r"(\w+)\s+(AND|OR|XOR)\s+(\w+)\s+->\s+(\w+)", definition)
        if not match:
            raise ValueError(f"Invalid gate definition: {definition}")

        input1, gate_type, input2, output = match.groups()
        gates.append((input1, gate_type, input2, output))

    # Keep evaluating gates until no new values are computed
    while True:
        new_values = False

        for input1, gate_type, input2, output in gates:
            # Skip if output is already computed
            if output in wire_values:
                continue

            # Skip if we don't have both input values yet
            if input1 not in wire_values or input2 not in wire_values:
                continue

            # Evaluate gate and store result
            result = evaluate_gate(gate_type, wire_values[input1], wire_values[input2])
            wire_values[output] = result
            new_values = True

        # If no new values were computed, we're done
        if not new_values:
            break

    # Collect all z-wire values and convert to decimal
    z_wires = sorted(
        (wire, value) for wire, value in wire_values.items() if wire.startswith("z")
    )

    result = 0
    for wire, value in z_wires:
        result = (result << 1) | value

    return result


def main():
    data = read_data("24.txt")
    result = part1(data)
    print(result)


if __name__ == "__main__":
    main()
