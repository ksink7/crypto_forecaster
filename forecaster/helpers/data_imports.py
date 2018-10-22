import pandas as pd
import numpy as np
from collections import deque
import random
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm


def historical_price_import(base, coin, interval):
    file = F"/crypto_forecaster/database/raw_data/{base}-{coin}_{interval}.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    df.index = pd.to_datetime(df.index)
    close_df = df[['C']]
    return close_df


def future_features_import(base, coin, interval, days_to_predict):
    file = F"/crypto_future_predict_features/{base}-{coin}-{days_to_predict}-{interval}_LR.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    df.index = pd.to_datetime(df.index)
    X = np.array(df)
    dates = df.index
    return X, dates


def linreg_import_split(base, coin, interval, days_to_predict, test_pct=0.1):
    file = F"/crypto_forecaster/database/feature_data-priceprediction/{base}-{coin}_{interval}-interval_{days_to_predict}-dayprediction.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    df.index = pd.to_datetime(df.index)

    test_pct = test_pct
    times = sorted(df.index.values)
    validation_end_date = sorted(df.index.values)[-int(float(test_pct) * len(times))]

    regression_df = df[(df.index < validation_end_date)]
    backtest_df = df[(df.index >= validation_end_date)]
    dates = backtest_df.index
    # print("test_train", regression_df.tail())
    # print("backtest", backtest_df.head())
    X = np.array(regression_df.drop(['FUTURE'], 1))
    y = np.array(regression_df['FUTURE'])
    X_backtest = np.array(backtest_df.drop(['FUTURE'], 1))
    y_backtest = np.array(backtest_df['FUTURE'])

    """
    NEED TO HAVE CROSS_VALIDATION UPDATED TO BE BETTER SUITED FOR
    TIME SERIES ANALYSIS
    """
    X_train, X_validate, y_train, y_validate = model_selection.train_test_split(
        X, y, test_size=0.3)

    return X_train, y_train, X_validate, y_validate, X_backtest, y_backtest, dates


def get_backtest_data_linreg():

    pass
