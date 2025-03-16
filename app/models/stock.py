from datetime import datetime

from sqlalchemy import DateTime, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db_base import Base, str_req, str_req_uq

# from app.models.item import Item


class Stock(Base):
    reference: Mapped[str_req_uq]
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    consignor: Mapped[str_req]
    ready: Mapped[bool] = mapped_column(server_default=text("FALSE"))
    note: Mapped[str | None]

    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="stock", cascade="all, delete-orphan"
    )
