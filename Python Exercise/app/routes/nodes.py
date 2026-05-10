from fastapi import APIRouter, HTTPException, status
from app.schemas import NodeCreate, NodeResponse
from app import store

router = APIRouter(prefix="/nodes", tags=["Nodes"])


@router.post("", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
def create_node(payload: NodeCreate):
    """Add a new node to the network graph."""

    name = payload.name.strip()

    if not name:
        raise HTTPException(status_code=400, detail="Node name cannot be empty")

    # check for duplicates
    if store.get_node_by_name(name):
        raise HTTPException(status_code=400, detail=f"Node '{name}' already exists")

    node = store.add_node(name)
    return node


@router.get("", response_model=list[NodeResponse])
def list_nodes():
    """List all nodes in the graph."""
    return store.get_all_nodes()


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: int):
    """Delete a node and all its connected edges."""

    deleted = store.delete_node(node_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Node with id {node_id} not found")
