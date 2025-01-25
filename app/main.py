from fastapi import FastAPI

from app.routes.stock import router as stock_router
from app.routes.item import router as item_router

app = FastAPI()


@app.get("/", summary="Root endpoint")
async def index():
    return {"message": "Root of service"}


app.include_router(stock_router)
app.include_router(item_router)
