import pandas as pd
import numpy as np
from collections import deque
import random
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, model_selection, svm
from helpers.date_handling import *
#from date_handling import *


def historical_price_import(base, coin, interval):
    #df = data_import_localtz(base, coin, interval)
    file = F"/users/kylesink82/desktop/forecaster/database/raw_data/{base}-{coin}_{interval}.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    #df.index = pd.to_datetime(df.index)
    close_df = df[['C']]
    return close_df


def future_features_import(base, coin, interval, days_to_predict):
    #df = data_import_localtz(base, coin, interval)
    file = F"/users/kylesink82/desktop/forecaster/database/future_predict_features/{base}-{coin}-{days_to_predict}-{interval}_LR.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    #df.index = pd.to_datetime(df.index)
    X = np.array(df)
    dates = df.index
    return X, dates


def linreg_import_split(base, coin, interval, days_to_predict, test_pct=0.1):
    file = F"/users/kylesink82/desktop/forecaster/database/feature_data-priceprediction/{base}-{coin}_{interval}-interval_{days_to_predict}-dayprediction.csv"
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    #df.index = pd.to_datetime(df.index)

    #df = data_import_localtz(base, coin, interval)

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
    TIMEE SERIES ANALYSIS
    """
    X_train, X_validate, y_train, y_validate = model_selection.train_test_split(
        X, y, test_size=0.3)

    return X_train, y_train, X_validate, y_validate, X_backtest, y_backtest, dates


def get_backtest_data_linreg():

    return X_backtest, y_backtest, dates


"""
X_train, y_train, X_validate, y_validate, X_backtest, y_backtest, dates = linreg_import_split(
    'USDT', 'ETH', 'DAILY', 2)
predictions = [204.67895114, 220.94416192, 216.9607604,  232.63878607, 253.41931008,
               245.80565175, 251.07787953, 233.92494577, 222.52466298, 222.98678476,
               237.56820293, 228.23521262, 239.785641,   239.03027612, 237.5421489,
               234.03476571, 228.24378264, 232.58549008, 235.19556553, 231.39523025,
               233.7797025,  237.19558852, 235.40488084, 233.48576612, 201.7620236,
               212.65748183]

coin = "ETH"
prediction_series = pd.Series(predictions)
actual_series = pd.Series(y_backtest)
type(predictions)
df = pd.DataFrame(index=dates)
df[F'{coin}-predictions'] = prediction_series.values
df['actual'] = actual_series.values
df.head(10)

"""
