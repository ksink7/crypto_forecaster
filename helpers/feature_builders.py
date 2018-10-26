import pandas as pd
import numpy as np
import talib
import glob
from sklearn import preprocessing
"""
list_of_files = glob.glob('/Users/Kylesink82/desktop/forecaster/database/raw_data/*.csv')
days_to_predict = [1, 2, 3, 4, 5, 6, 7, 21, 28]

"""
"""
# BUILDS FEATURE SETS FROM ALL CSV FILES IN THE RAW DATA FOLDER
# THE LABEL FOR THESE DATAFRAMES IS THE FUTURE COLUMN
base = 'USDT'
coin = 'ETH'
interval = 'day'
forecast = 1


list_of_files = F"/users/kylesink82/desktop/forecaster/database/raw_data/{base}-{coin}_{interval}.csv"
"""


def future_period_prediction_label_feature_builder(file, predict_period):
    base = file[55:59]
    coin = file[60:63]
    if coin == 'SC_':
        coin = file[60:62]

    if coin == "SC":
        interval = file[63:-4]
    else:
        interval = file[64:-4]
    #print(coin, interval)
    # print(len(file))

    """
    LOADS IN DATA FROM THE FILE AND SETS THE INDEX
    """
    df = pd.read_csv(file)
    df = df.set_index(df['T']).drop(['T'], axis=1)

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

    """
    CREATES FEATURE DATASET FOR FUTURE PERIOD PREDICTIONS
    """
    df_f = df_f.copy()
    predict_df = df_f.drop(['FUTURE'], axis=1)
    #predict_df = predict_df.dropna()
    predict_df = predict_df[~predict_df.isin([np.nan, np.inf, -np.inf]).any(1)]
    pred_col_names = predict_df.columns
    pred_index = predict_df.index

    pred_x = predict_df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    pred_x_scaled = min_max_scaler.fit_transform(pred_x)
    pred_feat_scaled = pd.DataFrame(pred_x_scaled, columns=pred_col_names, index=pred_index)
    pred_feat_scaled = pred_feat_scaled[(pred_feat_scaled.index >= predict_date)]

    pred_feat_scaled.to_csv(
        F"/users/kylesink82/desktop/forecaster/database/future_predict_features/{base}-{coin}-{predict_period}-{interval}_LR.csv", index=True)

    """
    CREATING FEATURE DATASET FOR MODEL BUILDING/HISTORICAL PREDICTIONS
    """
    df_f = df_f.dropna()
    future_df = df_f[['FUTURE']]
    features_df = df_f.drop(['FUTURE'], axis=1)
    features_df = features_df[~features_df.isin([np.nan, np.inf, -np.inf]).any(1)]

    feature_col_names = features_df.columns
    feature_index = features_df.index

    # print(features_df.describe())
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
        F'/Users/Kylesink82/desktop/forecaster/database/feature_data-priceprediction/{base}-{coin}_{interval}-interval_{predict_period}-dayprediction.csv', index=True)

    # return predict_df


#future_period_prediction_label_feature_builder(list_of_files, forecast)
