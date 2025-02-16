from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.stock import router as stock_router
from app.routes.item import router as item_router
from app.routes.cat import router as cat_router
from app.routes.user import router as user_router
from app.routes.frontend import router as frontend_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(stock_router)
app.include_router(item_router)
app.include_router(cat_router)
app.include_router(user_router)
app.include_router(frontend_router)
