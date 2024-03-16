import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from .baseline_model import prepare_data, train_baseline_model

def evaluate_model(stock_data, feature_days=5, threshold_percentage=0.01):
    """
    Evaluates the baseline model on the given stock data and returns MSE, MAE, and a strict form of "accuracy"
    based on the closing price predictions being within a narrow threshold percentage of the actual values.

    Parameters:
    - stock_data: The stock data to be used for evaluation.
    - feature_days: The number of days to use as features for the prediction.
    - threshold_percentage: The narrow percentage threshold within which a prediction is considered 'accurate'.

    Returns:
    - mse: Mean Squared Error
    - mae: Mean Absolute Error
    - accuracy: The percentage of predictions within the specified narrow threshold of the actual values.
    - r_squared: R-Squared value indicating the proportion of the variance in the dependent variable that is predictable from the independent variables.
    - rmse: Root Mean Squared Error (the square root of the MSE)
    """
    X, y = prepare_data(stock_data, feature_days)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_baseline_model(X_train, y_train)
    y_pred = model.predict(X_test)


    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r_squared = r2_score(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)


    percentage_diff = np.abs((y_pred - y_test) / y_test)
    strict_accurate_predictions = percentage_diff <= threshold_percentage
    accuracy = np.mean(strict_accurate_predictions) * 100 
    
    return mse, mae, accuracy, r_squared, rmse
