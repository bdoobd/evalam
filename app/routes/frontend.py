from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_active_user, user_powered, user_admin
from app.schemas.user import User
from app.routes.cat import all_cats
from app.routes.user import all_users, get_roles

router = APIRouter(prefix="", tags=["Frontend часть проекта"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", summary="Project home page")
async def index(
    user: Annotated[User, Depends(get_current_active_user)], request: Request
):
    return templates.TemplateResponse(
        name="home.html", context={"request": request, "username": user.username}
    )


@router.get("/login", summary="Login page")
async def login(request: Request):
    return templates.TemplateResponse(name="login.html", context={"request": request})


@router.get("/forbidden", summary="Forbidden page")
async def forbidden(request: Request):
    return templates.TemplateResponse(
        name="forbidden.html", context={"request": request}
    )


@router.get("/cats", summary="Available categories")
async def cats(
    request: Request,
    categories: Annotated[all_cats, Depends()],
    user: Annotated[User, Depends(user_powered)],
):
    return templates.TemplateResponse(
        name="categories.html",
        context={
            "request": request,
            "categories": categories,
        },
    )


@router.get("/admin", summary="Раздел администатирования пользователей")
async def users(
    request: Request,
    users: Annotated[all_users, Depends()],
    roles: Annotated[get_roles, Depends()],
    user: Annotated[User, Depends(user_admin)],
):
    return templates.TemplateResponse(
        name="users.html", context={"request": request, "users": users, "roles": roles}
    )
