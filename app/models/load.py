from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req, str_req_uq
from app.models.invoice import Invoice


class Load(Base):
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    truck: Mapped[str_req]
    consignee: Mapped[str_req]
    note: Mapped[str | None]

    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="load", cascade="all, delete-orphan"
    )
    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="load")
