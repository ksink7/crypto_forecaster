import pandas as pd
import matplotlib.dates as mdates
from sklearn import preprocessing
import numpy as np
import talib


validation_pct = .1
backtest_pct = .05
forecast_periods = 3


def X_y_split(df):
    X = np.array(df.drop(['label'], 1))
    #X = preprocessing.scale(X)
    y = np.array(df['label'])
    return X, y


def feature_build_w_split(ohlc_data, forecast_periods, validation_pct, backtest_pct):
    """
    FEATURE BUILDING
    """
    ind_days = 15
    #df = ohlc_data
    ohlc_data['label'] = ohlc_data['C'].shift(-forecast_periods)

    ohlc_data['HL_PCT'] = (ohlc_data['H'] - ohlc_data['C']) / ohlc_data['C'] * 100.0
    ohlc_data['PCT_CHANGE'] = (ohlc_data['C'] - ohlc_data['O']) / ohlc_data['O'] * 100.0
    ohlc_data['RSI'] = talib.RSI(ohlc_data.C.values, timeperiod=14)
    ohlc_data['rsi_pct_diff'] = (
        ohlc_data['RSI'] - ohlc_data['RSI'].shift(ind_days)) / ohlc_data['RSI'].shift(ind_days)
    ohlc_data['change'] = ohlc_data['C'] - ohlc_data['C'].shift(ind_days)
    # ohlc_data = ohlc_data[['label', 'C', 'HL_PCT',
    #                       'PCT_CHANGE', 'V', 'RSI', 'rsi_pct_diff', 'change']]
    ohlc_data = ohlc_data.copy()
    for col in ohlc_data.columns:
        if col != 'label':
            ohlc_data.dropna(inplace=True)
            ohlc_data.loc[:, col] = preprocessing.scale(ohlc_data[col].values)

    """
    SPLITTING DATA UP INTO TRAIN, VALIDATE, AND BACKTEST DATAFRAMES
    """
    times = sorted(ohlc_data.index.values)
    validation_date = sorted(ohlc_data.index.values)[-int(float(validation_pct) * len(times))]
    backtest_date = sorted(ohlc_data.index.values)[-int(float(backtest_pct) * len(times))]

    train_mask = (ohlc_data.index <= validation_date)
    validate_mask = (ohlc_data.index > validation_date) & (ohlc_data.index < backtest_date)
    backtest_mask = (ohlc_data.index >= backtest_date)

    train_df = ohlc_data[train_mask]
    validate_df = ohlc_data[validate_mask]
    backtest_df = ohlc_data[backtest_mask]

    train_df = train_df.dropna()
    validate_df = validate_df.dropna()
    backtest_df = backtest_df.dropna()

    """
    SPLITTING THE DATAFRAMES INTO X AND y
    """
    X_train, y_train = X_y_split(train_df)
    X_validate, y_validate = X_y_split(validate_df)
    X_backtest, y_backtest = X_y_split(backtest_df)

    # return train_df, validate_df, backtest_df
    return X_train, y_train, X_validate, y_validate, X_backtest, y_backtest


def load_ohlc(coin, interval, new_data):
    if new_data == True:
        candlestick_link = 'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=' + \
            str(coin) + '&tickInterval=' + str(interval) + '&_='
        candlestick_data = pd.read_json(candlestick_link)
        candlestick_data = candlestick_data['result']
        candlestick_data = candlestick_data.apply(pd.Series)
        candlestick_data = candlestick_data.set_index(candlestick_data['T'])
        candlestick_data = candlestick_data.drop(['T'], axis=1)
        candlestick_data.index = pd.to_datetime(candlestick_data.index)
        candlestick_data.to_csv(
            F"/crypto_forecaster/pricing_data/{coin}_{interval}.csv", index=True)
        print(F"New Data downloaded for {coin}, interval - {interval}")

    else:
        """
        need to correct index
        """
        candlestick_data = pd.read_csv(
            F"/crypto_forecaster/pricing_data/{coin}_{interval}.csv")
        print(candlestick_data)
        print(F"Old Data used for {coin}, interval - {interval}")

    return candlestick_data
