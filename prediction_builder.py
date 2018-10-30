from helpers.database_updater import *
from helpers.feature_builders import *
from helpers.model_builders import *
from progressbar import ProgressBar, Counter, ETA, Bar, Percentage
import sys

"""
SETTINGS FOR PREDICTION_BUILDER
"""
coins_to_build = ['BTC', 'ETH', 'XRP', 'TRX', 'SC', 'LTC', 'BCH', 'ADA', 'XVG', 'ZEC']
base_currencies = ['USDT']
base_currency = 'USDT'
tickIntervals = ['oneMin', 'fiveMin', 'thirtyMin', 'hour', 'day']
forecast_periods = [1, 2, 3, 4, 5, 6, 7, 21, 28]
#coins_to_build = ['XRP']
#tickIntervals = ['oneMin', 'fiveMin']
#forecast_periods = [1, 2, 3, 4]

"""
FILE DIRECTORIES
"""
raw_ohlc_files = glob.glob('/Users/Kylesink82/desktop/forecaster/database/raw_data/*.csv')

"""
PROGRESS BARS
"""
pbar_database = ProgressBar(widgets=[Percentage(), Bar(), ETA()])
pbar_features = ProgressBar(widgets=[Percentage(), Bar(), ETA()])
pbar_models = ProgressBar(widgets=[Percentage(), Bar(), ETA()])
pbar_logs = ProgressBar(widgets=[Percentage(), Bar(), ETA()])


def argv_method(argv=None):
    import sys
    if argv is None:
        argv = sys.argv
    arg_strs = argv[1:]
    kwargs = {}
    for s in arg_strs:
        if s.count("=") == 1:
            key, value = s.split("=", 1)
            kwargs[key] = value
    return kwargs


def update_ohlc_database():
    """
    UPDATES ALL INTERVALS FOR THE COINS IN THE ABOVE LIST
    GETS DATA FROM BITTREX, OTHER EXCHANGES WILL BE ADDED IN THE FUTURE

    """
    global coins_to_build
    global base_currencies

    updates = [[base, coin, interval]
               for base in base_currencies for coin in coins_to_build for interval in tickIntervals]
    for base, coin, interval in pbar_database(updates):
        database_update(base, coin, interval)

    pass


def build_features(ohlc_data_files, forecast_periods):
    """
    -BUILD FEATURES FOR ALL INTERVALS IN THE RAW PRICING FILE IF MAIN
    CURRENTLY A FEATURE SET CONTAINING A LABEL OF A FUTURE PRICE
         IS BEING USED
    -DIFFERENT BUILDERS CAN BE INPUTED HERE FOR OTHER MODEL TYPES

    """
    # builds feature sets as a future price for the label
    iterations = [[file, predict_period]
                  for file in ohlc_data_files for predict_period in forecast_periods]

    for file, predict_period in pbar_features(iterations):
        future_period_prediction_label_feature_builder(file, predict_period)

    # create a function to build out feature sets for categorical labels
    pass


def build_models():
    """
    BUILDS NEW MODELS
    -OTHER MODELS CAN BE INPUTED HERE, CURRENTLY ONLY LINEAR REG.
    IS GEING USED FOR FRAMEWORK PURPOSES
    """
    global base_currencies
    global coins_to_build
    global forecast_periods
    global tickIntervals

    builds = [[base, coin, period, interval]
              for base in base_currencies for coin in coins_to_build for period in forecast_periods for interval in tickIntervals]

    for base, coin, period, interval in pbar_models(builds):
        regression_model_build(base, coin, period, interval)
        # lstm_model_build()    ##need to build out


def update_prediction_log():
    """
    !!!!!! PREDICTION BUILDER FUNCTION NEEDS FINISHED !!!!!!!!

    BUILDS PREDICTION LOGS FOR WHATEVER COINS-INTERVAL ARE PASSED TO IT
    NEEDS UPDATED TO CORRECTLY BUILD PREDICTION DATABASE, DATE ISSUE CURRENTLY EXISTS
    NEEDS UPDATED TO ONLY ADD NEW VALUES, AND NOT OVERWRITE EXISTING PREDICTIONS
    """
    global base_currencies
    global coins_to_build
    global forecast_periods
    global tickIntervals

    builds = [[base, coin, period, interval]
              for base in base_currencies for coin in coins_to_build for period in forecast_periods for interval in tickIntervals]

    for base, coin, period, interval in pbar_logs(builds):
        MSE, accuracy, prediction_df = build_linreg_prediction_log(base, coin, period, interval)
        historical_prediction_csv_logger(prediction_df, base, coin, interval, period, 'LR')
        # print(
        #    F"Updated Prediction log for {base}-{coin} on interval {interval} forecasting {forecast} periods ")

    pass


def main(**kwargs):
    print()

    if ('D' in kwargs):
        update_trigger = kwargs['D']
        if update_trigger == "Yes":
            print("-----------------UPDATING DATABASE-----------------")
            update_ohlc_database()
            print()

        else:
            print("-----------------OLD DATA USED--------------------")
            print()
    else:
        print("-----------------OLD DATA USED--------------------")
        print()

    if ('F' in kwargs):
        feature_rebuild_trigger = kwargs['F']
        if feature_rebuild_trigger == "Yes":
            print("-----------------BUILDING NEW FEATURES------------")
            build_features(raw_ohlc_files, forecast_periods)
            print()

        else:
            print("-----------------OLD FEATURES USED----------------")
            print()
    else:
        print("-----------------OLD FEATURES USED----------------")
        print()

    if ('M' in kwargs):
        model_rebuild_trigger = kwargs['M']
        if model_rebuild_trigger == "Yes":
            print("-----------------REBUILDING MODELS----------------")
            build_models()
            print()

        else:
            print("-----------------OLD MODELS USED------------------")
            print()
    else:
        print("-----------------OLD MODELS USED------------------")
        print()

    if ('L' in kwargs):
        pred_log_update_trigger = kwargs['L']
        if pred_log_update_trigger == "Yes":
            print("-----------------BUILDING PREDICTION LOGS-------")
            update_prediction_log()
            print()

        else:
            print("--------------PREDICTION LOGS NOT UPDATED----------")
            print()
    else:
        print("--------------PREDICTION LOGS NOT UPDATED----------")
        print()


# main_test(update_database=True, rebuild_features=True,
#          rebuild_models=True, prediction_logs_update=True)
# main(rebuild_features=True)

if __name__ == "__main__":
    import sys
    kwargs = argv_method(sys.argv)
    main(**kwargs)


"""
Function needs built to rerun all model builds for a particular ticker
and interval for more timeconsuming models.
"""
