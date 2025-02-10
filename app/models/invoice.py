from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req_uq


class Invoice(Base):
    reference: Mapped[str_req_uq]

    load: Mapped[list["Load"]] = relationship(
        "Load", back_populates="invoice", cascade="all, delete-orphan"
    )
