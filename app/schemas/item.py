from pydantic import BaseModel, Field

from app.schemas.stock import StockAdd


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


class ItemAddWithNewStock(Item):
    new_stock: StockAdd


class FilterItems(BaseModel):
    lot: str | None = Field(None, title="Item lot number", min_length=5)
    pallet: str | None = Field(None, title="Item pallet number", min_length=3)
    roll: str | None = Field(None, title="Item roll number", min_length=4)
    note: str | None = Field(None, title="Item note", max_length=200)
    # stock_id: int | None = Field(None, title="Stock ID", ge=1)
    # cat_id: int | None = Field(None, title="Category ID", ge=1)
    # load_id: int | None = Field(None, title="Load ID")
    id: int | None = Field(None, title="Item ID", ge=1)
