from pydantic import BaseModel, Field


class Item(BaseModel):
    lot: str = Field(..., title="Item lot number", min_length=5)
    pallet: str = Field(..., title="Item pallet number", min_length=3)
    roll: str = Field(..., title="Item roll number", min_length=4)
    note: str | None = Field(None, title="Item note", max_length=200)
    stock_id: int = Field(..., title="Stock ID", ge=1)
    cat_id: int = Field(..., title="Category ID", ge=1)
    load_id: int | None = Field(None, title="Load ID")


class ItemWithID(Item):
    id: int
