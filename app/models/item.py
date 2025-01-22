from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req


class Item(Base):
    reference: Mapped[str_req]
    name: Mapped[str_req]
    description: Mapped[str_req]
    qty: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float | None]
    stock_id: Mapped[int | None] = mapped_column(ForeignKey("stocks.id"))

    stock: Mapped["Stock"] = relationship("Stock", back_populates="items")
