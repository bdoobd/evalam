from typing import Literal

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.schemas.stock import StockAdd, Stock
from app.schemas.cat import Cat


class Item(BaseModel):
    lot: str | None = Field(None, title="Item lot number")
    pallet: str | None = Field(None, title="Item pallet number")
    roll: str | None = Field(None, title="Item roll number")
    # lot: str = Field(..., title="Item lot number", min_length=5)
    # pallet: str = Field(..., title="Item pallet number", min_length=4)
    # roll: str = Field(..., title="Item roll number", min_length=4)
    note: str | None = Field(None, title="Item note", max_length=200)
    stock_id: int | None = Field(None, title="Stock ID", ge=1)
    cat_id: int = Field(..., title="Category ID", ge=1)
    load_id: int | None = Field(None, title="Load ID")

    model_config = ConfigDict(from_attributes=True)


class ItemWithID(Item):
    id: int


# Тестирование множественной аннотации типов
class ItemAddBase(BaseModel):
    type: Literal["base"]
    lot: str | None = Field(None, title="Item lot number")
    pallet: str | None = Field(None, title="Item pallet number")
    roll: str | None = Field(None, title="Item roll number")
    qty: int = Field(..., ge=1)
    note: str | None = Field(None, title="Item note", max_length=200)
    cat_id: int = Field(..., title="Category ID", ge=1)
    load_id: int | None = Field(None, title="Load ID")

    model_config = ConfigDict(from_attributes=True)


class ItemAdd(ItemAddBase):
    type: Literal["exist"]
    stock_id: int = Field(..., title="Stock ID", ge=1)


class ItemAddWithNewStock(ItemAddBase):
    type: Literal["new"]
    new_stock: StockAdd


class FilterItems(BaseModel):
    lot: str | None = Field(None, title="Item lot number")
    pallet: str | None = Field(None, title="Item pallet number")
    roll: str | None = Field(None, title="Item roll number")
    # note: str | None = Field(None, title="Item note", max_length=200)
    # stock_id: int | None = Field(None, title="Stock ID", ge=1)
    # cat_id: int | None = Field(None, title="Category ID", ge=1)
    # load_id: int | None = Field(None, title="Load ID")
    id: int | None = Field(None, title="Item ID", ge=1)

    model_config = ConfigDict(from_attributes=True)


# ====================================================
class ItemInStock(BaseModel):
    id: int
    lot: str
    pallet: str
    roll: str
    note: str | None
    stock: Stock
    cat: Cat
    # load_id: int | None = Field(None, title="Load ID")

    model_config = ConfigDict(from_attributes=True)

# Validators
@field_validator("lot", "pallet", "roll")
@classmethod
def check_value_length(cls, value, info):
    min_length = {
        "lot": 5,
        "pallet": 4,
        "roll": 4
    }
    if value is not None and len(value) < min_length[info.field_name]:
        raise ValueError(f"{info.field_name} must be at least {min_length[info.field_name]} characters long")
    return value