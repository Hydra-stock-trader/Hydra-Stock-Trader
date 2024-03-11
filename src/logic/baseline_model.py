# src/logic/baseline_model.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def prepare_data(stock_data, feature_days=5):
    """
    Prepares data for the baseline model, using the last 'feature_days' closing prices as features
    to predict the next closing price.
    """
    df = pd.DataFrame(stock_data['history'])  # Convert dictionary to DataFrame
    X = np.array([df['Close'].shift(i) for i in range(1, feature_days + 1)]).T
    y = df['Close'].values
    X, y = X[feature_days:], y[feature_days:]  # Remove NaNs
    return X, y

def train_baseline_model(X, y):
    """
    Trains the baseline Linear Regression model and returns it along with its RMSE on the test set.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return model, rmse
