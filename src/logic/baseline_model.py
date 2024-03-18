# src/logic/baseline_model.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def prepare_data(stock_data, feature_days=200):
    """
    Prepares data for the baseline model, using the last 'feature_days' closing prices as features, 
    and other features like Open, High, Low, Volume, including the Quarterly P/E Ratio 
    as an additional feature to predict the next closing price.
    """
    # Convert historical stock data to DataFrame and reset the index to make 'Date' a column
    df_history = pd.DataFrame(stock_data['history']).reset_index()
    df_history.rename(columns={'index': 'Date'}, inplace=True)  # Rename 'index' column to 'Date'
    df_history['Date'] = df_history['Date'].dt.tz_localize(None)

    df_pe_ratio = pd.DataFrame(stock_data['valuation_measures'], columns=['asOfDate', 'PeRatio'])
    df_pe_ratio['asOfDate'] = df_pe_ratio['asOfDate'].dt.tz_localize(None)

    # Sort DataFrames by date to ensure proper alignment for merge_asof
    df_history = df_history.sort_values('Date')
    df_pe_ratio = df_pe_ratio.sort_values('asOfDate')
    
    # Use merge_asof to align P/E Ratio data with stock history
    df = pd.merge_asof(df_history, df_pe_ratio, left_on='Date', right_on='asOfDate',
                       direction='forward')  # 'forward' fills each P/E Ratio forward seeing as it's quarterly data

    # Merge P/E Ratio data with stock history, forward-filling P/E Ratios
    df_merged = pd.merge_asof(df_history, df_pe_ratio, left_on='Date', right_on='asOfDate', direction='forward')
    df_merged['PeRatio'] = pd.to_numeric(df_merged['PeRatio'], errors='coerce').ffill()

    # Selecting features and the target variable
    X = df_merged[['Open', 'High', 'Low', 'Volume', 'PeRatio']].values  # Features including P/E Ratio
    y = df_merged['Close'].values  # Target variable

    # Convert all of X to float to avoid issues with np.isnan
    X = np.asarray(X, dtype=np.float64)

    # Handling rows with NaN values - these might originate from the forward fill if the first rows do not have P/E Ratio data
    valid_rows = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
    X, y = X[valid_rows], y[valid_rows]

    return X, y

def train_baseline_model(X, y):
    """
    Trains the baseline Linear Regression model on the given data and returns the trained model.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model





