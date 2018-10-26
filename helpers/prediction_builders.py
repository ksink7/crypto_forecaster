import pandas as pd
#from data_imports import *
from helpers.data_imports import *
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


base = "USDT"
coin = "XRP"
forecast = 4
interval = "fiveMin"

"""
FUNCION NEEDS TO BE MADE TO BE FED A LIST OF CURRENCIES, COINS
FORECAST PERIODS AND INTERVALS THAT UPDATES AN EXCEL SHEET
WITH ALL OF THE PREDICTIONS FOR THAT COIN/INTERVAL WITH THE
COLUMN NAMES BEING THE MODEL NAME/FORECAST PERIODS FOR THE
PREDICTED PRICE AT THAT TIMESTAMP
"""


def prediction_excel_logger(df, base, coin, interval, forecast):
    while True:
        try:
            spreadsheet_load = pd.ExcelFile(
                '/Users/Kylesink82/desktop/forecaster/predictions.xlsx', index=True)
            sh_df = spreadsheet_load.parse(F"{base}-{coin}")
            sh_df = sh_df.set_index('T', drop=True)
            print(sh_df.head())
            break

        except Exception:

            df.to_excel('/Users/Kylesink82/desktop/forecaster/predictions.xlsx',
                        sheet_name=F'{base}-{coin}', index=True)

            break


def historical_prediction_csv_logger(df, base, coin, interval, forecast, model_type):
    while True:
        try:
            data_load = pd.read_csv(
                F'/Users/Kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            log_end = loaded_df.index[-1]
            prediction_end = df.index[-1]

            if log_end < prediction_end:
                new_predictions = df[(df.index > loaded_df.index[-1])]
                if F"{model_type}-{forecast}" not in loaded_df:
                    loaded_df[F"{model_type}-{forecast}"] = 0

                updated_log = loaded_df.append(new_predictions, sort=True)
                updated_log.to_csv(
                    F'/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv')

            else:
                updated_log = loaded_df.copy()

                if F"LR-{forecast}" not in updated_log:
                    updated_log[F"LR-{forecast}"] = 0

                #print("column average", updated_log[F'LR-{forecast}'].mean())
                if updated_log[F"LR-{forecast}"].mean() == 0:
                    updated_log.update(df, overwrite=True)
                    #print("overwrote all values")
                else:
                    updated_log.update(df, overwrite=False)
                    #print("added new only")

                #print("updated", updated_log.tail())
                updated_log.to_csv(
                    F'/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv')

            break

        except OSError:
            pred_df = df
            pred_df.to_csv(
                F'/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv')
            #print(F"Downloaded new Minute data for {coin}")
            break


def build_linreg_prediction_log(base, coin, forecast, interval):
    hist_df = historical_price_import(base, coin, interval)

    X_train, y_train, X_validate, y_validate, X_backtest, y_backtest, dates = linreg_import_split(
        base, coin, interval, forecast)
    fut_pred, fut_dates = future_features_import(base, coin, interval, forecast)

    model_load = open(
        F"/users/kylesink82/desktop/forecaster/saved_models/{base}-{coin}-{forecast}-{interval}_linreg.pickle", 'rb')
    linreg_model = pickle.load(model_load)

    MSE = mean_squared_error(y_backtest, linreg_model.predict(X_backtest))
    accuracy = linreg_model.score(X_validate, y_validate)

    predictions = linreg_model.predict(X_backtest)
    prediction_series = pd.Series(predictions)

    future_predictions = linreg_model.predict(fut_pred)
    future_predictions_series = pd.Series(future_predictions)

    fut_df = pd.DataFrame(index=fut_dates)
    fut_df['model_predictions'] = future_predictions_series.values
    fut_df.to_csv(
        F"/users/kylesink82/desktop/forecaster/future_prediction/{base}-{coin}-{interval}-{forecast}.csv")

    pred_df = pd.DataFrame(index=dates)
    pred_df['model_predictions'] = prediction_series.values

    merged = pd.concat([pred_df, fut_df])
    #merged = merged.sort_index()
    merged = merged[~merged.index.duplicated(keep='last')]

    main_df = pd.DataFrame(index=hist_df.index)
    main_df['Actual Close'] = hist_df['C']
    main_df['model_prediction'] = merged['model_predictions']
    main_df[F"LR-{forecast}"] = main_df['model_prediction'].shift(forecast)

    main_df = main_df.drop(["model_prediction"], axis=1)
    #main_df = main_df.dropna()
    return MSE, accuracy, main_df


MSE, accuracy, prediction_df = build_linreg_prediction_log(base, coin, forecast, interval)

# prediction_df.tail()
#prediction_excel_logger(prediction_df, base, coin, interval, forecast)
#prediction_csv_logger(prediction_df, base, coin, interval, forecast, "LR")
