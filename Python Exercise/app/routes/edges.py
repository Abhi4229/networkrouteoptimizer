from fastapi import APIRouter, HTTPException, status
from app.schemas import EdgeCreate, EdgeResponse
from app import store

router = APIRouter(prefix="/edges", tags=["Edges"])


@router.post("", response_model=EdgeResponse, status_code=status.HTTP_201_CREATED)
def create_edge(payload: EdgeCreate):
    """Add a weighted edge between two nodes."""

    source = payload.source.strip()
    destination = payload.destination.strip()
    latency = payload.latency

    # can't create an edge from a node to itself
    if source == destination:
        raise HTTPException(status_code=400, detail="Source and destination cannot be the same")

    # both nodes must exist
    if not store.get_node_by_name(source):
        raise HTTPException(status_code=400, detail=f"Source node '{source}' does not exist")
    if not store.get_node_by_name(destination):
        raise HTTPException(status_code=400, detail=f"Destination node '{destination}' does not exist")

    # no duplicate edges
    if store.edge_exists(source, destination):
        raise HTTPException(
            status_code=400,
            detail=f"Edge from '{source}' to '{destination}' already exists"
        )

    edge = store.add_edge(source, destination, latency)
    return edge


@router.get("", response_model=list[EdgeResponse])
def list_edges():
    """List all edges in the graph."""
    return store.get_all_edges()


@router.delete("/{edge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_edge(edge_id: int):
    """Remove an edge from the graph."""

    deleted = store.delete_edge(edge_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Edge with id {edge_id} not found")
