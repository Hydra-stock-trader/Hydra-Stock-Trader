import yfinance as yf
import yahooquery as yq
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
    yq_ticker = yq.Ticker(ticker_symbol)
    
    # Get the historical data for the last year contains OHLCV data. 
    hist = ticker.history(period="12mo")
    
    # Dividends and splits
    dividends = ticker.dividends 
    splits = ticker.splits
    
    # Company info
    info = ticker.info
    
    # Valuation Measures Retrieves the most recent four quarters as well as the most recent date, currently only gathering PeRatio.
    valuation_measures = yq_ticker.valuation_measures
    last_4_quarters_pe = valuation_measures.tail(5)[['asOfDate', 'PeRatio']].to_numpy().tolist()
    
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
        "cashflow": cashflow.to_dict(),
        "valuation_measures":  last_4_quarters_pe,
    }
    
    # Handle non-finite float values in the data
    data = handle_non_finite_values(data)
    
    return data