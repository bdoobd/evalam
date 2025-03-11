from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.db_base import Base, str_req, str_req_uq
from app.helpers.roles import Roles


class User(Base):
    username: Mapped[str_req_uq]
    password: Mapped[str_req]
    role: Mapped[Roles] = mapped_column(default=Roles.user)
    disabled: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    modified: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
