from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class StockAdd(BaseModel):
    reference: str = Field(..., title="Stock reference", min_length=8)
    date_in: datetime = Field(..., title="Stock date inbound")
    sender: str = Field(..., title="Sender on goods", min_length=5)
    note: str | None = Field(None, title="Motes of the stock", max_length=200)

    # model_config = ConfigDict(from_attributes=True)
