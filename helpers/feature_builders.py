import pandas as pd
import numpy as np
import talib
import glob
from sklearn import preprocessing


def future_period_prediction_label_feature_builder(file, predict_period):
    base = file[55:59]
    coin = file[60:63]
    if coin == 'SC_':
        coin = file[60:62]
    
    if coin == "SC":
        interval = file[63:-4]
    else:
        interval = file[64:-4]
    

    """
    LOADS IN DATA FROM THE FILE AND SETS THE INDEX
    """
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)
    df.index = pd.to_datetime(df.index)

    times = sorted(df.index.values)
    predict_date = sorted(df.index.values)[-int(predict_period)]

    """
    BUILDS ON FEATURES
    """
    df_f = df
    df_f['FUTURE'] = df_f['C'].shift(-predict_period)
    df_f['RSI'] = talib.RSI(df_f.C.values, timeperiod=14)
    df_f["RSI_PCT_DIFF"] = (df_f["RSI"] - df_f['RSI'].shift(predict_period)
                            ) / df_f['RSI'].shift(predict_period)
    df_f['CHANGE'] = df_f['C'] - df_f['C'].shift(predict_period)
    """
    -SPLITS OUT THE LABEL AND FEATURES
    -NORMALIZES THE FEATURES
    -MERGES THE DATAFRAMES
    """
    df_f = df_f.copy()
    future_predict_features = df_f.drop(['FUTURE'], axis=1)
    predict_df = future_predict_features[(future_predict_features.index >= predict_date)]
    predict_df.to_csv(
        F"/crypto_forecaster/database/future_predict_features/{base}-{coin}-{predict_period}-{interval}_LR.csv", index=True)

    df_f = df_f.dropna()
    future_df = df_f[['FUTURE']]
    features_df = df_f.drop(['FUTURE'], axis=1)
    feature_col_names = features_df.columns
    feature_index = features_df.index

    x = features_df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    scaled_features = pd.DataFrame(x_scaled, columns=feature_col_names, index=feature_index)
    scaled_features['FUTURE'] = future_df
    """
    SLICING FOR FILE SAVING AND PROGRESS PRINTOUTS
    """
    base = file[55:59]
    coin = file[60:63]
    if coin == "SC_":
        coin = file[60:62]
    if coin == "SC":
        interval = file[63:-4]
    else:
        interval = file[64:-4]
    scaled_features.to_csv(
        F'/crypto_forecaster/database/feature_data-priceprediction/{base}-{coin}_{interval}-interval_{predict_period}-dayprediction.csv', index=True)

    # return predict_df

#future_period_prediction_label_feature_builder(list_of_files, forecast)
