import yfinance as yf

# Gets OHLCV data for a given stock ticker, also Dividends and Stock Splits. 
def get_stock_data(ticker_symbol: str):
    ticker = yf.Ticker(ticker_symbol)
    hist = ticker.history(period="1mo")
    return hist
