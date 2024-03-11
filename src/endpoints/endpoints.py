from fastapi import APIRouter, HTTPException
from typing import Any, Dict
from src.models.models import  Item

from src.logic.stock_data import get_stock_data
from src.logic.baseline_model import prepare_data, train_baseline_model

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

@router.get("/stock/{ticker_symbol}/predict")
async def predict_stock_price(ticker_symbol: str):
    data = get_stock_data(ticker_symbol)
    X, y = prepare_data(data)
    model, rmse = train_baseline_model(X, y)
    last_day_features = X[-1].reshape(1, -1)
    prediction = model.predict(last_day_features)[0]
    return {"ticker_symbol": ticker_symbol, "predicted_next_close": prediction, "rmse": rmse}

