from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.dependencies import get_current_active_user
from app.schemas.user import User

router = APIRouter(prefix="", tags=["Frontend часть проекта"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", summary="Интерфейс проекта")
async def index(request: Request):
    return templates.TemplateResponse(name="base.html", context={"request": request})
