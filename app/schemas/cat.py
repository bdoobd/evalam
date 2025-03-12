from pydantic import BaseModel, Field, ConfigDict


class CatAdd(BaseModel):
    name: str = Field(..., title="Название продукта")
    cat: str = Field(..., title="Тип продукта")
    width: int = Field(..., title="Размер, ширина продукта", gt=0)
    weight: float = Field(..., title="Вес единицы продукта", gt=0)
    note: str = Field(
        default="Сгенерированное примечание к категории",
        title="Примечание к продукту",
    )

    model_config = ConfigDict(from_attributes=True)


class Cat(BaseModel):
    name: str
    cat: str
    width: int
    weight: float
    note: str | None

    model_config = ConfigDict(from_attributes=True)


class CatWithID(Cat):
    id: int


class CatByID(BaseModel):
    id: int
