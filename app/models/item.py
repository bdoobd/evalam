from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db_base import Base, str_req, str_opt

from app.models.load import Load
from app.models.cat import Cat


class Item(Base):
    stock_id: Mapped[int] = mapped_column(ForeignKey("stocks.id"))
    load_id: Mapped[int | None] = mapped_column(ForeignKey("loads.id"))
    cat_id: Mapped[int] = mapped_column(ForeignKey("cats.id"), nullable=False)
    lot: Mapped[str_req] = mapped_column(default='Untagged')
    pallet: Mapped[str_req] = mapped_column(default='Untagged')
    roll: Mapped[str_opt] = mapped_column(unique=True)
    note: Mapped[str | None]

    stock: Mapped["Stock"] = relationship("Stock", back_populates="items")
    load: Mapped["Load"] = relationship("Load", back_populates="items")
    cat: Mapped["Cat"] = relationship("Cat", back_populates="items")
