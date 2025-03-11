from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db_base import Base, str_req_uq


class Invoice(Base):
    reference: Mapped[str_req_uq]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    modified: Mapped[datetime] = mapped_column(
        server_default=func.now(), server_onupdate=func.now()
    )
    note: Mapped[str]

    load: Mapped[list["Load"]] = relationship(
        "Load", back_populates="invoice", cascade="all, delete-orphan"
    )
