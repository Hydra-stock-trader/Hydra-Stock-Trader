from fastapi import APIRouter, HTTPException
from src.models.models import  Item

from src.logic.stock_data import get_stock_data

router = APIRouter()

@router.get("/stock/{ticker_symbol}")
async def stock(ticker_symbol: str):
    try:
        data = get_stock_data(ticker_symbol)
        return {"ticker_symbol": ticker_symbol, "data": data.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


