from fastapi import FastAPI
from items_api.store.sqlite import init_db
from items_api.routes.items_route import router as items_router_v1

app = FastAPI()

app.include_router(items_router_v1, prefix="/api/v1", tags=["Items"])



@app.on_event("startup")
async def on_startup():
    await init_db()
