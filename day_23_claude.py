from collections import defaultdict
from itertools import combinations


def read_data(filename="23.txt"):
    """
    Read the network connections from the input file and return as adjacency list.
    """
    graph = defaultdict(set)

    with open(filename) as f:
        for line in f:
            comp1, comp2 = line.strip().split("-")
            # Add both directions since connections are bidirectional
            graph[comp1].add(comp2)
            graph[comp2].add(comp1)

    return graph


def find_triangles(graph):
    """
    Find all sets of three computers that are fully connected to each other.
    Returns a set of frozensets to eliminate duplicates.
    """
    triangles = set()

    # Get all computers
    computers = list(graph.keys())

    # Check all possible combinations of three computers
    for comp1, comp2, comp3 in combinations(computers, 3):
        # Check if they form a triangle (all connected to each other)
        if comp2 in graph[comp1] and comp3 in graph[comp1] and comp3 in graph[comp2]:
            triangles.add(frozenset([comp1, comp2, comp3]))

    return triangles


def part1(graph):
    """
    Find the number of triangles that contain at least one computer
    starting with 't'.
    """
    triangles = find_triangles(graph)

    # Count triangles with at least one computer starting with 't'
    count = sum(
        1 for triangle in triangles if any(comp.startswith("t") for comp in triangle)
    )

    return count


def is_clique(graph, computers):
    """
    Check if a set of computers forms a clique (all connected to each other).
    """
    return all(other in graph[comp] for comp, other in combinations(computers, 2))


def find_max_clique(graph):
    """
    Find the largest set of computers that are all connected to each other.
    Uses a bottom-up approach starting from triangles to reduce search space.
    """
    # Start with triangles as base cliques
    triangles = find_triangles(graph)
    if not triangles:
        return None

    # Convert triangles to lists for easier handling
    current_cliques = [set(triangle) for triangle in triangles]

    # Keep track of the maximum clique found
    max_clique = max(current_cliques, key=len)

    # Try to expand each clique
    while current_cliques:
        new_cliques = []
        for clique in current_cliques:
            # Find potential computers to add
            candidates = set.intersection(*(set(graph[comp]) for comp in clique))
            candidates -= clique  # Remove computers already in the clique

            # Try adding each candidate
            for candidate in candidates:
                new_clique = clique | {candidate}
                if is_clique(graph, new_clique):
                    new_cliques.append(new_clique)
                    if len(new_clique) > len(max_clique):
                        max_clique = new_clique

        # If we can't expand any cliques further, we're done
        if not new_cliques:
            break

        current_cliques = new_cliques

    return max_clique


def part2(graph):
    """
    Find the password for the LAN party by getting the largest fully connected
    set of computers and joining their names with commas in alphabetical order.
    """
    max_clique = find_max_clique(graph)
    if not max_clique:
        return None

    # Sort computers alphabetically and join with commas
    return ",".join(sorted(max_clique))


def main():
    graph = read_data()
    result = part1(graph)
    print(result)
    result = part2(graph)
    print(result)


if __name__ == "__main__":
    main()
