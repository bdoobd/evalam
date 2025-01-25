from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req

# from app.models.stock import Stock
from app.models.load import Load


class Item(Base):
    reference: Mapped[str_req]
    name: Mapped[str_req]
    description: Mapped[str_req]
    qty: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    volume: Mapped[float | None]
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"))
    load_id: Mapped[int | None] = mapped_column(ForeignKey("loads.id"))
    note: Mapped[str | None]

    stock: Mapped["Stock"] = relationship("Stock", back_populates="items")
    load: Mapped["Load"] = relationship("Load", back_populates="items")
