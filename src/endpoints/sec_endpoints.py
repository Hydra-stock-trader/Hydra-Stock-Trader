from fastapi import APIRouter, HTTPException
from src.logic.sec_data import getTickers

router = APIRouter()

@router.get("/sec/retrieve_tickers")
async def getSECTickers():
    try:
        data = getTickers()
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))