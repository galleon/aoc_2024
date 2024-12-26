

def read_data(filename):
    with open(filename, "r") as f:
        lines = f.read().splitlines()

    initial_values = {}
    gates = []

    for line in lines:
        if ":" in line:
            wire, value = line.split(": ")
            initial_values[wire] = int(value)
        elif "->" in line:
            parts = line.split(" -> ")
            output_wire = parts[1]
            input_parts = parts[0].split()
            if len(input_parts) == 3:  # Binary gate
                input1, op, input2 = input_parts
                gates.append((input1, op, input2, output_wire))
            else:  # NOT gate
                op, input1 = input_parts
                gates.append((input1, op, None, output_wire))

    return initial_values, gates


def part1(data):
    initial_values, gates = data
    wires = initial_values.copy()

    while True:
        new_values = {}
        changed = False

        for input1, op, input2, output_wire in gates:
            if output_wire in wires:
                continue

            val1 = wires.get(input1)
            if op != "NOT":
                val2 = wires.get(input2)

            if val1 is not None and (op == "NOT" or val2 is not None):
                if op == "AND":
                    new_values[output_wire] = val1 & val2
                elif op == "OR":
                    new_values[output_wire] = val1 | val2
                elif op == "XOR":
                    new_values[output_wire] = val1 ^ val2
                elif op == "NOT":
                    new_values[output_wire] = 1 - val1

                changed = True

        wires.update(new_values)
        if not changed:
            break

    z_values = []
    for wire, value in wires.items():
        if wire.startswith("z"):
            z_values.append((wire, value))

    z_values.sort(key=lambda x: int(x[0][1:]))

    binary_string = "".join(str(val) for _, val in z_values)

    return int(binary_string, 2) if binary_string else 0


def main():
    data = read_data("24.txt")
    result1 = part1(data)
    print(f"Part 1: {result1}")


if __name__ == "__main__":
    main()
