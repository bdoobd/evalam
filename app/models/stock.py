from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req, str_req_uq

from app.models.item import Item


class Stock(Base):
    reference: Mapped[str_req_uq]
    date_in: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now
    )
    sender: Mapped[str_req]
    closed: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    note: Mapped[str | None]

    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="stock", cascade="all, delete-orphan"
    )
