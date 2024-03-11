from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from src.models.models import  Item

from src.logic.stock_data import get_stock_data

router = APIRouter()

@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = get_item(item_id)
    return item

@router.get("/stock/{ticker_symbol}", response_model=Dict[str, Any])
async def stock(ticker_symbol: str):
    try:
        data = get_stock_data(ticker_symbol)
        return {"ticker_symbol": ticker_symbol, "data": data}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


