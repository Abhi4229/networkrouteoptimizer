"""
In-memory data store for the network graph.

Using simple dicts and lists instead of a database — keeps the project
lightweight and easy to run without any setup. The tradeoff is that
data is lost when the server restarts, which is fine for this exercise.
"""

from datetime import datetime, timezone


# auto-increment counters
_node_counter = 0
_edge_counter = 0
_history_counter = 0

# storage
nodes = {}       # id -> {"id": int, "name": str}
edges = {}       # id -> {"id": int, "source": str, "destination": str, "latency": float}
route_history = []  # list of history records

# quick lookup: node name -> node id
node_name_index = {}



def add_node(name: str) -> dict:
    global _node_counter
    _node_counter += 1
    node = {"id": _node_counter, "name": name}
    nodes[_node_counter] = node
    node_name_index[name] = _node_counter
    return node


def get_node_by_name(name: str):
    node_id = node_name_index.get(name)
    if node_id is None:
        return None
    return nodes.get(node_id)


def get_all_nodes() -> list:
    return list(nodes.values())


def delete_node(node_id: int) -> bool:
    node = nodes.get(node_id)
    if node is None:
        return False

    name = node["name"]

    # remove any edges connected to this node
    to_remove = [
        eid for eid, e in edges.items()
        if e["source"] == name or e["destination"] == name
    ]
    for eid in to_remove:
        del edges[eid]

    del nodes[node_id]
    del node_name_index[name]
    return True


def add_edge(source: str, destination: str, latency: float) -> dict:
    global _edge_counter
    _edge_counter += 1
    edge = {
        "id": _edge_counter,
        "source": source,
        "destination": destination,
        "latency": latency,
    }
    edges[_edge_counter] = edge
    return edge


def edge_exists(source: str, destination: str) -> bool:
    for e in edges.values():
        if e["source"] == source and e["destination"] == destination:
            return True
    return False


def get_all_edges() -> list:
    return list(edges.values())


def delete_edge(edge_id: int) -> bool:
    if edge_id in edges:
        del edges[edge_id]
        return True
    return False


def add_history_record(source: str, destination: str, total_latency, path) -> dict:
    global _history_counter
    _history_counter += 1
    record = {
        "id": _history_counter,
        "source": source,
        "destination": destination,
        "total_latency": total_latency,
        "path": path,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    route_history.append(record)
    return record


def get_history(source=None, destination=None, limit=None, date_from=None, date_to=None) -> list:
    results = route_history[:]

    if source:
        results = [r for r in results if r["source"] == source]
    if destination:
        results = [r for r in results if r["destination"] == destination]
    if date_from:
        results = [r for r in results if r["created_at"] >= date_from]
    if date_to:
        results = [r for r in results if r["created_at"] <= date_to]

    # most recent first
    results = list(reversed(results))

    if limit:
        results = results[:limit]

    return results
