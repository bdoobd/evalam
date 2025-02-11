from fastapi import FastAPI

from app.routes.stock import router as stock_router
from app.routes.item import router as item_router
from app.routes.cat import router as cat_router

app = FastAPI()


@app.get("/", summary="Root endpoint")
async def index():
    return {"message": "Root of service"}


app.include_router(stock_router)
app.include_router(item_router)
app.include_router(cat_router)
