import re
from itertools import combinations, permutations, product


def read_data(filename="24.txt"):
    """
    Reads puzzle input from 24.txt. Returns a tuple (wire_values, gates).
      wire_values: dict {wire_name: bit_value} for initially known wires
      gates: list of (in1, operation, in2, out)
    """
    wire_values = {}
    gates = []

    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # First section: lines of the form "<wire>: <bit>"
    idx = 0
    wire_pattern = re.compile(r"^(\w+):\s*([01])$")
    while idx < len(lines):
        match = wire_pattern.match(lines[idx])
        if match:
            wire_name, bit_str = match.groups()
            wire_values[wire_name] = int(bit_str)
            idx += 1
        else:
            break

    # Second section: lines of the form "<wire> <op> <wire> -> <wire>"
    gate_pattern = re.compile(r"^(\w+)\s+(AND|OR|XOR)\s+(\w+)\s*->\s*(\w+)$")
    while idx < len(lines):
        match = gate_pattern.match(lines[idx])
        if not match:
            raise ValueError(f"Invalid gate line: {lines[idx]}")
        in1, op, in2, out = match.groups()
        gates.append((in1, op, in2, out))
        idx += 1

    return wire_values, gates


def simulate_gates(initial_wire_values, gates):
    """
    Given initial_wire_values and a list of gates, simulate until no more outputs
    can be computed. Return a dict of all wire values (0 or 1).
    """
    wire_values = dict(initial_wire_values)
    resolved_gates = set()
    changed = True
    while changed:
        changed = False
        for i, (in1, op, in2, out) in enumerate(gates):
            if i in resolved_gates:
                continue
            if in1 in wire_values and in2 in wire_values:
                a = wire_values[in1]
                b = wire_values[in2]
                if op == "AND":
                    result = a & b
                elif op == "OR":
                    result = a | b
                elif op == "XOR":
                    result = a ^ b
                else:
                    raise ValueError(f"Unknown operation: {op}")
                wire_values[out] = result
                resolved_gates.add(i)
                changed = True
    return wire_values


def part1(data):
    """
    Original logic for part1: simulate all gates, read final binary from wires
    starting with 'z', interpret as decimal.
    """
    wire_values, gates = data
    final_values = simulate_gates(wire_values, gates)

    # Gather wires that start with 'z', sorted by numeric suffix
    z_wires = [w for w in final_values if w.startswith("z")]
    z_wires.sort(key=lambda w: int(w[1:]))  # 'zNN' -> NN

    # Build binary from these bits (z00 is rightmost/least significant)
    bits = [str(final_values[z]) for z in z_wires]
    bits_reversed = "".join(reversed(bits))  # MSB..LSB
    decimal_value = int(bits_reversed, 2) if bits_reversed else 0
    return decimal_value


def set_xy_bits(wire_values, x_val, y_val, x_bits, y_bits):
    """
    Given a base wire_values dict, set the bits for xNN and yNN from x_val, y_val.
    x_bits, y_bits indicate how many bits we expect for x, y respectively.
    Example: if x_bits=4, x_val=13(=1101 bin), then
        wire_values["x00"] = 1, wire_values["x01"] = 0, wire_values["x02"] = 1, wire_values["x03"] = 1
    """
    # Copy so we don't mutate the original
    wv = dict(wire_values)

    # Set xNN bits
    for i in range(x_bits):
        bit = (x_val >> i) & 1
        wv[f"x{str(i).zfill(2)}"] = bit

    # Set yNN bits
    for i in range(y_bits):
        bit = (y_val >> i) & 1
        wv[f"y{str(i).zfill(2)}"] = bit

    return wv


def read_z_value(final_values):
    """
    Convert wires z00, z01, z02, ... into a single integer.
    We assume that z00 is the least significant bit, z01 next, etc.
    """
    z_wires = [w for w in final_values.keys() if w.startswith("z")]
    if not z_wires:
        return 0
    z_wires.sort(key=lambda w: int(w[1:]))  # sort by numeric part
    bits = [(final_values[w] if w in final_values else 0) for w in z_wires]
    # bits[0] is z00, bits[1] is z01, ...
    value = 0
    for i, b in enumerate(bits):
        value |= b << i
    return value


def check_adder_correctness(wire_values, gates, x_bits, y_bits, test_full=True):
    """
    Return True if for all (or some) combinations of x and y, the circuit's z bits
    match x+y. Otherwise, False.

    If test_full=True, test ALL combinations up to 2^(x_bits + y_bits)
    which might be huge if x_bits+y_bits is large.
    """
    max_x = 1 << x_bits  # 2^x_bits
    max_y = 1 << y_bits  # 2^y_bits

    # For big circuits, you may want to do random sampling or partial checks.
    # We'll do a full check for demonstration (works if x_bits+y_bits is small).
    for x_val in range(max_x):
        for y_val in range(max_y):
            # Set up x,y bits
            wv = set_xy_bits(wire_values, x_val, y_val, x_bits, y_bits)

            # Simulate
            final = simulate_gates(wv, gates)

            # Read z
            z_val = read_z_value(final)

            # Check correctness
            if z_val != (x_val + y_val):
                return False

    return True


def swap_gate_outputs(gates, swap_pairs):
    """
    Given a list of gates and a list of pairs (i,j) indicating that gate i's output wire
    should be swapped with gate j's output wire, return a *new copy* of gates with those swaps.

    Each (i, j) is a pair of *indices in the gates list*.
    We'll replace gate_i.out with gate_j.out and vice versa.

    Example: if gates[i] = (in1, op, in2, out_i),
             gates[j] = (in1, op, in2, out_j),
    after swap,
             gates[i] = (in1, op, in2, out_j),
             gates[j] = (in1, op, in2, out_i).
    """
    new_gates = list(gates)  # shallow copy of the list
    # But each element is a tuple, so to modify, we need to create new tuples
    new_gates = [tuple(g) for g in new_gates]

    # Convert each gate to a list so we can modify the 'out' field
    mutable_gates = [list(g) for g in new_gates]

    for i, j in swap_pairs:
        # Swap the outputs
        mutable_gates[i][3], mutable_gates[j][3] = (
            mutable_gates[j][3],
            mutable_gates[i][3],
        )

    # Convert back to tuples
    swapped_gates = [tuple(g) for g in mutable_gates]
    return swapped_gates


def part2(data):
    """
    Attempt to find exactly four pairs of gates (eight gates total) whose outputs are swapped.
    Then produce the puzzle's required output: the sorted wire names involved, joined by commas.

    This is a naive brute force approach:
      1. We gather the indices of all gates.
      2. We try all ways to pick 8 distinct gates, then partition them into 4 pairs.
      3. For each pairing, we swap those outputs and test if the circuit is correct.
      4. If correct, we gather the wire names from those swaps, sort them, and print them.

    Potentially huge search. For a large circuit, you'll need a more optimized method.
    """
    wire_values, gates = data

    # You may need to adjust x_bits and y_bits to match your puzzle's real inputs
    # For demonstration, let's guess that we have 4 bits of x, 4 bits of y
    # (or read them from the data if you can detect it).
    x_bits = 4
    y_bits = 4

    # First, test if the circuit is already correct with no swaps (unlikely, but let's check):
    if check_adder_correctness(wire_values, gates, x_bits, y_bits, test_full=False):
        print("No swaps needed; circuit is already correct!")
        return

    n = len(gates)
    if n < 8:
        print("Not enough gates to have 4 swap pairs.")
        return

    # We'll gather all gate indices [0..n-1]
    gate_indices = range(n)

    # 1) Choose exactly 8 distinct gates from n.
    # 2) Then we must partition those 8 gates into 4 disjoint pairs.
    # We'll do combinations(gate_indices, 8) for the selection of 8,
    # then all ways to pair them up.
    # For the pairing, we can do permutations of the 8 chosen gates
    # in steps of 2, or a known "all pairings" approach.

    def all_pairings(eight_indices):
        """
        Generate all ways to partition eight distinct items into four pairs.
        For example, if eight_indices = [a,b,c,d,e,f,g,h],
        yield sequences of pairs like [(a,b), (c,d), (e,f), (g,h)], etc.
        """
        if not eight_indices:
            yield []
        else:
            first = eight_indices[0]
            for i in range(1, len(eight_indices)):
                # pick partner for 'first'
                partner = eight_indices[i]
                pair = (first, partner)
                remaining = list(eight_indices[1:i]) + list(eight_indices[i + 1 :])
                for rest in all_pairings(remaining):
                    yield [pair] + rest

    # A small optimization: we might do partial or random checks.
    # We'll do a BFS-style approach but keep it plain here:

    found_solution = False
    for chosen_8 in combinations(gate_indices, 8):
        chosen_8 = list(chosen_8)
        # Create all pairings of these 8 gates into 4 pairs
        for pairing in all_pairings(chosen_8):
            # pairing is something like [(i1, i2), (i3, i4), (i5, i6), (i7, i8)]
            swapped = swap_gate_outputs(gates, pairing)
            # Now check correctness:
            if check_adder_correctness(
                wire_values, swapped, x_bits, y_bits, test_full=False
            ):
                # If correct, we gather the output wires that got swapped
                # Indices i1,i2,... correspond to gates[i]'s output
                wire_names = []
                for i1, i2 in pairing:
                    wire_names.append(gates[i1][3])
                    wire_names.append(gates[i2][3])
                # Sort them
                wire_names.sort()
                # Join them with commas
                answer = ",".join(wire_names)
                print("Swapped wires found! They are:", answer)
                found_solution = True
                break
        if found_solution:
            break

    if not found_solution:
        print("No 4-pair swaps found that fix the circuit (with this naive approach).")


def main():
    data = read_data("24.txt")

    # part1: original puzzle's part1
    p1 = part1(data)
    print("Part1 result:", p1)

    # part2: attempt to find the 4 pairs that fix the addition
    print("\n--- Part2 searching for swaps ---")
    part2(data)


if __name__ == "__main__":
    main()
