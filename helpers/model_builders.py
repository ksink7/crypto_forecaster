import pandas as pd
import quandl
import math
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import seaborn as sns
import os
import talib
from helpers.data_processing import *
from helpers.data_imports import *
from helpers.prediction_builders import *
from sklearn.linear_model import LinearRegression


def regression_model_build(base, coin, forecast, interval):
    accuracy_cache = pd.DataFrame(columns=('model', 'accuracy'))

    ticker = F"{base}-{coin}"
    X_train, y_train, X_validate, y_validate, X_backtest, y_backtest, dates = linreg_import_split(
        base, coin, interval, forecast)
    #print(F"loaded data in for COIN: {coin}, INTERVAL: {interval}")

    clf = LinearRegression(n_jobs=-1)
    clf.fit(X_train, y_train)
    #print(F"Fit model for COIN: {coin}, INTERVAL: {interval}")
    accuracy = clf.score(X_validate, y_validate)
    if accuracy < 0:
        clf = LinearRegression(n_jobs=-1)
        clf.fit(X_train, y_train)
        accuracy = clf.score(X_validate, y_validate)
        if accuracy < 0:
            clf = LinearRegression(n_jobs=-1)
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_validate, y_validate)
            model_name = F"{ticker}_linreg_{forecast}days_{interval}"
            accuracy_data = [model_name, accuracy]
            accuracy_cache.loc[len(accuracy_cache)] = accuracy_data
            with open(F'/crypto_forecaster/saved_models/{ticker}-{forecast}-{interval}_linreg.pickle', 'wb') as f:
                pickle.dump(clf, f)
                # print(
                #    F"Saved model for {ticker}, forecasting {forecast} days on attempt 3, interval {interval}")

        else:
            model_name = F"{ticker}_linreg_{forecast}days_{interval}"
            accuracy_data = [model_name, accuracy]
            accuracy_cache.loc[len(accuracy_cache)] = accuracy_data
            with open(F'/crypto_forecaster/saved_models/{ticker}-{forecast}-{interval}_linreg.pickle', 'wb') as f:
                pickle.dump(clf, f)
                # print(
                #    F"Built model for {ticker}, forecasting {forecast} days on attempt 2, interval {interval}")

    else:
        model_name = F"{ticker}_linreg_{forecast}days_{interval}"
        accuracy_data = [model_name, accuracy]
        accuracy_cache.loc[len(accuracy_cache)] = accuracy_data
        with open(F'/crypto_forecaster/saved_models/{ticker}-{forecast}-{interval}_linreg.pickle', 'wb') as f:
            pickle.dump(clf, f)
            # print(
            #    F"Built model for {ticker}, forecasting {forecast} days on attempt 1, interval {interval}")

    # print(
        # F"Linear Regression Model Saved: COIN: {coin}, PREDICTION PERIODS: {forecast}, INTERVAL: {interval}")
