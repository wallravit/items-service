"""
This is the main entry point for the FastAPI application.

It sets up the application, includes routes, and initializes the database on startup.

Routes:
- Items API: Accessible at the `/api/v1` endpoint.

Events:
- Startup: Initializes the database connection.
"""

from fastapi import FastAPI
from items_api.store.sqlite import init_db
from items_api.routes.items_route import router as items_router_v1
from items_api.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.include_router(items_router_v1, prefix="/api/v1", tags=["Items"])


@app.on_event("startup")
async def on_startup(): # pragma: no cover
    """Initialize the database connection on application startup."""
    await init_db()
