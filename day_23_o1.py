import itertools


def read_data() -> dict[str, set[str]]:
    """
    Reads the file 23.txt and returns an adjacency list representation of the graph.
    """
    adjacency: dict[str, set[str]] = {}
    with open("23.txt") as f:
        for line in f:
            a, b = line.strip().split("-")
            adjacency.setdefault(a, set()).add(b)
            adjacency.setdefault(b, set()).add(a)
    return adjacency


def part1(adjacency: dict[str, set[str]]) -> int:
    """
    Finds all triangles (3-cliques) in the graph and returns the number
    of triangles containing at least one computer name starting with 't'.
    """
    triangles = set()
    for u in adjacency:
        for v in adjacency[u]:
            if v <= u:
                continue
            # Intersection of neighbors of u and v are candidates to form triangles
            common_neighbors = adjacency[u].intersection(adjacency[v])
            for w in common_neighbors:
                # Keep everything in a consistent sorted order to avoid duplicates
                if w > v:
                    triangles.add(frozenset([u, v, w]))

    # Now filter for sets that have a node starting with 't'
    count_with_t = sum(any(node.startswith("t") for node in tri) for tri in triangles)
    return count_with_t


import itertools
import random


def part2_bruteforce_incremental(data):
    """
    Incremental, backtracking BFS/DFS approach to find the 4 swapped pairs.

    data = (init_wires, gates)
      init_wires: dict wire_name -> 0/1 for known initial values
      gates: list of (in1, op, in2, out)
    Returns: comma-separated list of the 8 swapped wires (sorted).
    """
    init_wires, gates = data

    # Build a list of gates, each has a unique index and a unique output wire
    # Example: gates_with_idx = [(0, in1, op, in2, out_wire0),
    #                           (1, in1, op, in2, out_wire1),
    #                            ...]
    gates_with_idx = [
        (i, in1, op, in2, out) for i, (in1, op, in2, out) in enumerate(gates)
    ]

    # For convenience, map gate_idx -> output_wire
    gate_outputs = {i: out for (i, _, _, _, out) in gates_with_idx}

    # We'll track which gates have already been swapped
    swapped_already = set()  # set of gate indices

    # We'll store the final result of 4 pairs if found
    solution_pairs = []

    # Generate a small set of test patterns for x,y
    # (Corner cases + random patterns)
    test_patterns = generate_test_patterns(data, max_tests=80)

    # We'll do a backtracking search
    def backtrack(chosen_pairs):
        """
        chosen_pairs is a list of (gateA_idx, gateB_idx).
        If len(chosen_pairs) == 4, test the final circuit thoroughly.
        Otherwise, pick the next pair and keep going.
        """
        if len(chosen_pairs) == 4:
            # We have 4 pairs. Test thoroughly (or at least more extensively).
            if circuit_ok_with_swaps(chosen_pairs, data, test_patterns):
                return chosen_pairs  # success
            return None

        # Otherwise, pick the next pair among gates not used so far
        used_gates = set(g for pair in chosen_pairs for g in pair)
        candidates = [g for g in gate_outputs if g not in used_gates]

        # Generate all 2-combinations among the remaining gates
        # We'll do a BFS/DFS: pick a pair, test quickly, then recurse.
        for g1, g2 in itertools.combinations(candidates, 2):
            new_pairs = chosen_pairs + [(g1, g2)]
            # Quick partial test
            if quick_test_swaps(new_pairs, data):
                # Recurse
                ans = backtrack(new_pairs)
                if ans is not None:
                    return ans
        return None

    # Kick off the search
    result = backtrack([])
    if result is None:
        return "No valid 4-pair swap found"

    # result is a list of 4 pairs of gate indices
    # We want the 8 wires
    swapped_wires = []
    for ga, gb in result:
        swapped_wires.append(gate_outputs[ga])
        swapped_wires.append(gate_outputs[gb])
    swapped_wires = sorted(swapped_wires)
    return ",".join(swapped_wires)


def quick_test_swaps(chosen_pairs, data):
    """
    A faster, partial check to see if 'chosen_pairs' can still be valid.
    For example, we might only test a few bit patterns here (like all-0, all-1).
    Or if we see an immediate contradiction, we return False.
    """
    # You can do a handful of patterns or even just 2-3:
    small_test_patterns = generate_test_patterns(data, max_tests=4)
    return circuit_ok_with_swaps(chosen_pairs, data, small_test_patterns)


def circuit_ok_with_swaps(chosen_pairs, data, test_patterns):
    """
    Fully simulate the circuit with the chosen swaps for each (x,y) in test_patterns.
    If for any pattern, z != x+y, return False. Otherwise True.
    """
    for x_asg, y_asg in test_patterns:
        if not simulate_one_case(chosen_pairs, data, x_asg, y_asg):
            return False
    return True


def simulate_one_case(chosen_pairs, data, x_asg, y_asg):
    """
    1. Build a swap_map so that gate_outputs[G] -> gate_outputs[H] if (G,H) is a chosen pair.
       If G isn't in a pair, it maps to itself.
    2. Then run the usual gate simulation, but whenever a gate with index i produces output,
       we actually store it in swap_map[i].
    3. At the end, check if z == x+y.
    """
    init_wires, gates = data
    # Build swap_map from gate index -> gate index
    # e.g. if (g1,g2) is a pair, then swap_map[g1] = g2, swap_map[g2] = g1
    # default identity if not swapped
    swap_map = {}
    for i, _ in enumerate(gates):
        swap_map[i] = i
    for a, b in chosen_pairs:
        swap_map[a] = b
        swap_map[b] = a

    # We'll keep a dict of wire -> value
    wire_vals = dict(init_wires)  # start with known initial wires
    wire_vals.update(x_asg)
    wire_vals.update(y_asg)

    changed = True
    while changed:
        changed = False
        for gate_idx, (in1, op, in2, out) in enumerate(gates):
            if in1 in wire_vals and in2 in wire_vals:
                a = wire_vals[in1]
                b = wire_vals[in2]
                if op == "AND":
                    val = a & b
                elif op == "OR":
                    val = a | b
                elif op == "XOR":
                    val = a ^ b
                else:
                    raise ValueError(f"Unknown op: {op}")

                # But the actual wire that receives this output is gate_outputs[ swap_map[gate_idx] ]
                swapped_gate_idx = swap_map[gate_idx]
                out_wire = gates[swapped_gate_idx][
                    3
                ]  # index 3 is the 'out' in (in1,op,in2,out)
                # Actually, be careful: gates[swapped_gate_idx] is a full gate tuple
                # with out-wire. Another simpler approach is to store gate_idx->out_wire
                # in a dictionary up front. Let's do that:
                # out_wire = gate_outputs[ swap_map[gate_idx] ] if we had gate_outputs = {idx -> out_wire}

                # If you kept a dict: gate_outputs = { i: out_wire_name, ... }:
                # out_wire = gate_outputs[ swap_map[gate_idx] ]
                # So let's assume that for clarity:
                #
                # out_wire = gate_outputs[swap_map[gate_idx]]

                # For illustration, assume we have that dictionary:
                # (We'll define it outside in part2_bruteforce_incremental)

                # We'll assume out_wire = gate_outputs[ swapped_gate_idx ]
                # Then:
                out_wire_name = gate_outputs[swapped_gate_idx]

                if (out_wire_name not in wire_vals) or (
                    wire_vals[out_wire_name] != val
                ):
                    wire_vals[out_wire_name] = val
                    changed = True

    # Now extract x-bits, y-bits, z-bits to see if z = x+y
    x_bits = collect_bits(wire_vals, "x")
    y_bits = collect_bits(wire_vals, "y")
    z_bits = collect_bits(wire_vals, "z")

    x_val = bits_to_int(x_bits)
    y_val = bits_to_int(y_bits)
    z_val = bits_to_int(z_bits)

    return z_val == x_val + y_val


def collect_bits(wire_vals, prefix):
    """
    Gather bits for wires that start with `prefix`, sorted by numeric suffix,
    returning a list [LSB, next, ...].
    """
    relevant = [(int(w[len(prefix) :]), w) for w in wire_vals if w.startswith(prefix)]
    relevant.sort(key=lambda x: x[0])
    return [wire_vals[wname] for (_, wname) in relevant]


def bits_to_int(bits):
    val = 0
    for i, b in enumerate(bits):
        val |= b << i
    return val


def generate_test_patterns(data, max_tests=50):
    """
    Return a list of (x_assignment, y_assignment).
    We'll gather all 'x??' and 'y??' wires, then either:
      - if few bits, do full enumeration
      - if many bits, do corner + random
    """
    init_wires, gates = data
    all_wires = set(init_wires.keys())
    for i1, _, i2, o in gates:
        all_wires.update([i1, i2, o])
    x_wires = sorted(w for w in all_wires if w.startswith("x"))
    y_wires = sorted(w for w in all_wires if w.startswith("y"))

    n_x = len(x_wires)
    n_y = len(y_wires)
    total_bits = n_x + n_y

    # If it's small, do full enumeration:
    if total_bits <= 10:
        patterns = []
        for xv in range(1 << n_x):
            for yv in range(1 << n_y):
                xa = {}
                ya = {}
                for i, w in enumerate(x_wires):
                    xa[w] = (xv >> i) & 1
                for j, w in enumerate(y_wires):
                    ya[w] = (yv >> j) & 1
                patterns.append((xa, ya))
        return patterns

    # Otherwise, corner + random
    patterns = []
    corner_x = [0, (1 << n_x) - 1] if n_x > 0 else [0]
    corner_y = [0, (1 << n_y) - 1] if n_y > 0 else [0]
    for cx in corner_x:
        for cy in corner_y:
            xa, ya = {}, {}
            for i, w in enumerate(x_wires):
                xa[w] = (cx >> i) & 1
            for j, w in enumerate(y_wires):
                ya[w] = (cy >> j) & 1
            patterns.append((xa, ya))

    # random
    tries = 0
    import random

    while len(patterns) < max_tests and tries < max_tests * 5:
        tries += 1
        rx = random.randint(0, (1 << n_x) - 1) if n_x > 0 else 0
        ry = random.randint(0, (1 << n_y) - 1) if n_y > 0 else 0
        xa = {}
        ya = {}
        for i, w in enumerate(x_wires):
            xa[w] = (rx >> i) & 1
        for j, w in enumerate(y_wires):
            ya[w] = (ry >> j) & 1
        if (xa, ya) not in patterns:
            patterns.append((xa, ya))

    return patterns


def main():
    data = read_data()
    print(part1(data))
    print(part2_bruteforce_incremental(data))


if __name__ == "__main__":
    main()
