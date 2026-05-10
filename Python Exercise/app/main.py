from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import nodes, edges, routes

app = FastAPI(
    title="Network Route Optimizer",
    description="API for managing network nodes, edges, and finding shortest routes using Dijkstra's algorithm.",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def custom_validation_handler(request, exc):
    """
    Override the default Pydantic error format.
    Instead of returning the raw validation details, we return
    a single clean error message that's easier to read.
    """
    errors = exc.errors()

    missing = []
    invalid = []

    for err in errors:
        field_name = err["loc"][-1] if err["loc"] else "unknown"
        if err["type"] == "missing":
            missing.append(field_name)
        else:
            invalid.append(field_name)

    messages = []

    # group source/destination together since they're related
    src_dst = [f for f in missing if f in ("source", "destination")]
    if src_dst:
        messages.append("Source/Destination missing")

    if "latency" in missing:
        messages.append("Latency missing")

    if "name" in missing:
        messages.append("Name missing")

    # any other missing fields we didn't handle above
    handled = {"source", "destination", "latency", "name"}
    for f in missing:
        if f not in handled:
            messages.append(f"{f} missing")

    # invalid values (e.g. latency <= 0)
    for f in invalid:
        if f == "latency":
            messages.append("Latency must be greater than 0")
        else:
            messages.append(f"Invalid value for {f}")

    detail = ". ".join(messages) if messages else "Validation error"

    return JSONResponse(status_code=400, content={"detail": detail})


# register route handlers
app.include_router(nodes.router)
app.include_router(edges.router)
app.include_router(routes.router)


@app.get("/", tags=["Health"])
def health_check():
    """Simple health check to verify the API is running."""
    return {"status": "ok", "service": "network-route-optimizer"}
