from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.schemas.item import ItemAddWithID


class StockAdd(BaseModel):
    reference: str = Field(..., title="Stock reference", min_length=8)
    date_in: datetime = Field(..., title="Stock date inbound")
    sender: str = Field(..., title="Sender on goods", min_length=5)
    note: str | None = Field(None, title="Motes of the stock", max_length=200)

    model_config = ConfigDict(from_attributes=True)


class StockRef(BaseModel):
    id: int
    reference: str

    model_config = ConfigDict(from_attributes=True)


class Stock(StockRef):
    date_in: datetime
    sender: str
    note: str | None

    model_config = ConfigDict(from_attributes=True)


class StockData(Stock):
    item_data: list[ItemAddWithID] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def get_stock_days(self) -> int:
        return (datetime.now() - self.date_in).days
