"""
Pydantic schemas for request/response validation.
Keeps the validation logic separate from the route handlers.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ---- Node schemas ----

class NodeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Unique name for the node")


class NodeResponse(BaseModel):
    id: int
    name: str


# ---- Edge schemas ----

class EdgeCreate(BaseModel):
    source: str = Field(..., min_length=1, description="Source node name")
    destination: str = Field(..., min_length=1, description="Destination node name")
    latency: float = Field(..., gt=0, description="Latency must be a positive number")


class EdgeResponse(BaseModel):
    id: int
    source: str
    destination: str
    latency: float


# ---- Route schemas ----

class RouteRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)


class RouteResponse(BaseModel):
    total_latency: float
    path: list[str]


# ---- History schemas ----

class HistoryRecord(BaseModel):
    id: int
    source: str
    destination: str
    total_latency: Optional[float]
    path: list[str]
    created_at: str
