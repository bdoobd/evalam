from fastapi import APIRouter, Depends

from app.dao.stock import StockDAO
from app.schemas.stock import StockAdd

router = APIRouter(prefix="/stock", tags=["Stock"])


@router.post("/add_stock", summary="Add stock")
async def new_stock(stock: StockAdd = Depends()) -> dict:
    stock = await StockDAO.add_one(stock.model_dump())

    return {"message": "Stock added", "Stock ID": stock}
