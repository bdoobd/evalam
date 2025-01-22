from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req, str_req_uq


class Stock(Base):
    reference: Mapped[str_req_uq]
    date_in: Mapped[datetime] = mapped_column(nullable=False)
    sender: Mapped[str_req]
    note: Mapped[str] = mapped_column(nullable=True)

    items: Mapped[list["Item"]] = relationship("Item", back_populates="stock")
