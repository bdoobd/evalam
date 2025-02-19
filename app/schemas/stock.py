from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.schemas.item import ItemWithID


class StockAdd(BaseModel):
    reference: str = Field(..., title="Stock reference", min_length=8)
    date: datetime = Field(..., title="Stock date inbound")
    consignor: str = Field(..., title="Sender on goods", min_length=5)
    note: str | None = Field(None, title="Motes of the stock", max_length=200)

    model_config = ConfigDict(from_attributes=True)


class Stock(BaseModel):
    reference: str
    date: datetime
    consignor: str
    note: str

    model_config = ConfigDict(from_attributes=True)


class StockWithID(Stock):
    id: int


class StockData(StockWithID):
    item_data: list[ItemWithID] = Field(default_factory=list)

    @computed_field
    def get_stock_days(self) -> int:
        return (datetime.now() - self.date_in).days
