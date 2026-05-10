from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas import RouteRequest, RouteResponse, HistoryRecord
from app.services.graph import find_shortest_path
from app import store

router = APIRouter(prefix="/routes", tags=["Routes"])


@router.post("/shortest", response_model=RouteResponse)
def get_shortest_route(payload: RouteRequest):
    """
    The result is also saved to query history for auditing.
    """

    source = payload.source.strip()
    destination = payload.destination.strip()

    # validate that both nodes exist in the graph
    if not store.get_node_by_name(source):
        raise HTTPException(status_code=400, detail=f"Node '{source}' does not exist")
    if not store.get_node_by_name(destination):
        raise HTTPException(status_code=400, detail=f"Node '{destination}' does not exist")

    if source == destination:
        raise HTTPException(status_code=400, detail="Source and destination cannot be the same")

    result = find_shortest_path(source, destination)

    if result is None:
        # log the failed query too — it's useful to know what people searched for
        store.add_history_record(source, destination, None, [])
        raise HTTPException(
            status_code=404,
            detail=f"No path exists between {source} and {destination}"
        )

    total_latency, path = result

    # save to history
    store.add_history_record(source, destination, total_latency, path)

    return {"total_latency": total_latency, "path": path}


@router.get("/history", response_model=list[HistoryRecord])
def get_route_history(
    source: Optional[str] = Query(None, description="Filter by source node"),
    destination: Optional[str] = Query(None, description="Filter by destination node"),
    limit: Optional[int] = Query(None, ge=1, description="Max number of records to return"),
    date_from: Optional[str] = Query(None, description="Filter from this ISO timestamp"),
    date_to: Optional[str] = Query(None, description="Filter up to this ISO timestamp"),
):
    """
    Retrieve past route queries with optional filtering.
    Results are returned in reverse chronological order (newest first).
    """

    records = store.get_history(
        source=source,
        destination=destination,
        limit=limit,
        date_from=date_from,
        date_to=date_to,
    )
    return records
