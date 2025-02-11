from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db_base import Base, str_req, str_req_uq, str_opt

# from app.models.item import Item


class Cat(Base):
    name: Mapped[str_opt]
    cat: Mapped[str_opt]
    width: Mapped[int] = mapped_column(unique=True)
    weight: Mapped[float]
    note: Mapped[str]

    items: Mapped[list["Item"]] = relationship(
        "Item", back_populates="cat", cascade="all, delete-orphan"
    )
