from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.db_base import Base, str_req, str_req_uq, str_opt


class Cat(Base):
    name: Mapped[str_req]
    cat: Mapped[str_req]
    width: Mapped[int] = mapped_column(unique=True)
    weight: Mapped[float]
    note: Mapped[str]

    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="cat", cascade="all, delete-orphan"
    )
