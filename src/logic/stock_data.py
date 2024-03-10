import yfinance as yf
import math

# Function to handle non-finite float values
def handle_non_finite_values(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = handle_non_finite_values(value)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            data[i] = handle_non_finite_values(value)
    elif isinstance(data, float):
        if not math.isfinite(data):
            return str(data)
    return data

# Gets OHLCV data for a given stock ticker, also Dividends and Stock Splits. 
def get_stock_data(ticker_symbol: str):
    ticker = yf.Ticker(ticker_symbol)
    
    # Get the historical data for the last month contains OHLCV data. 
    hist = ticker.history(period="1mo")
    
    # Dividends and splits
    dividends = ticker.dividends 
    splits = ticker.splits
    
    # Company info
    info = ticker.info
    
    # Financials
    financials = ticker.financials
    balance_sheet = ticker.balance_sheet
    cashflow = ticker.cashflow
 
    data = {
        "history": hist.to_dict(),
        "dividends": dividends.to_list(),
        "splits": splits.to_list(),
        "info": info,
        "financials": financials.to_dict(),
        "balance_sheet": balance_sheet.to_dict(),
        "cashflow": cashflow.to_dict()
    }
    
    # Handle non-finite float values in the data
    data = handle_non_finite_values(data)
    
    return data