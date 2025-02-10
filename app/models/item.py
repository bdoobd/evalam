from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req

from app.models.load import Load


class Item(Base):
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"))
    load_id: Mapped[int | None] = mapped_column(ForeignKey("loads.id"))
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id"), nullable=False)
    lot: Mapped[str_req]
    pallet: Mapped[str_req]
    roll: Mapped[str_req]
    note: Mapped[str | None]

    stock: Mapped["Stock"] = relationship("Stock", back_populates="items")
    load: Mapped["Load"] = relationship("Load", back_populates="items")
    cat: Mapped["Cat"] = relationship("'Cat'", back_populates="items")
