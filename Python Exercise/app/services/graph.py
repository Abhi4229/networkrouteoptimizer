import heapq
from app import store


def build_adjacency_list() -> dict:
    """
    Returns: {node_name: [(neighbor_name, latency), ...]}
    """
    graph = {}

    # initialize all nodes (even ones with no edges)
    for node in store.get_all_nodes():
        graph[node["name"]] = []

    # add edges
    for edge in store.get_all_edges():
        source = edge["source"]
        dest = edge["destination"]
        latency = edge["latency"]
        if source in graph:
            graph[source].append((dest, latency))

    return graph


def find_shortest_path(source: str, destination: str):
    """
    Run Dijkstra's algorithm to find the shortest path between two nodes.

    Returns:
        (total_latency, [path]) if a path exists
        None if no path exists
    """
    graph = build_adjacency_list()

    # edge case: source or destination not in graph
    if source not in graph or destination not in graph:
        return None

    # distances dict — tracks the best known distance to each node
    distances = {node: float("inf") for node in graph}
    distances[source] = 0

    # previous node tracker — used to reconstruct the path
    previous = {node: None for node in graph}

    # min-heap: (distance, node_name)
    # we always process the closest unvisited node first
    heap = [(0, source)]

    visited = set()

    while heap:
        current_dist, current_node = heapq.heappop(heap)

        # skip if already processed (we might have stale entries in the heap)
        if current_node in visited:
            continue

        visited.add(current_node)

        # found destination — no need to keep going
        if current_node == destination:
            break

        # check all neighbors
        for neighbor, latency in graph.get(current_node, []):
            if neighbor in visited:
                continue

            new_dist = current_dist + latency

            # found a shorter path to this neighbor
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current_node
                heapq.heappush(heap, (new_dist, neighbor))

    # if destination was never reached
    if distances[destination] == float("inf"):
        return None

    # reconstruct path by walking backwards from destination
    path = []
    node = destination
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return (round(distances[destination], 2), path)
