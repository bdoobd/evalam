from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.routes.stock import router as stock_router
from app.routes.item import router as item_router
from app.routes.cat import router as cat_router
from app.routes.user import router as user_router
from app.routes.frontend import router as frontend_router
from app.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    InvalidTokenException,
)


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), "static")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(TokenNotFoundException)
async def token_not_found_exception_handler(
    request: Request, exc: TokenNotFoundException
):
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(InvalidTokenException)
async def invalid_token_exception_handler(request: Request, exc: InvalidTokenException):
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(403)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    return RedirectResponse(
        url="/forbidden",
        status_code=status.HTTP_303_SEE_OTHER,
    )


app.include_router(stock_router)
app.include_router(item_router)
app.include_router(cat_router)
app.include_router(user_router)
app.include_router(frontend_router)
