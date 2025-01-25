from pydantic import BaseModel, Field


class ItemAdd(BaseModel):
    reference: str = Field(..., title="Item reference", min_length=10)
    name: str = Field(..., title="Item name", min_length=2)
    description: str = Field(..., title="Item description", min_length=10)
    qty: int = Field(..., title="Item quantity", ge=1)
    weight: float = Field(..., title="Item weight", ge=0)
    volume: float | None = Field(None, title="Item volume")
    stock_id: int = Field(..., title="Stock ID", ge=1)
    load_id: int | None = Field(None, title="Load ID")
    note: str | None = Field(None, title="Item note", max_length=200)
