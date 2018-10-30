import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime

"""
DEFAULT SETTINGS
"""
base = "USDT"
coin = "XRP"
interval = "fiveMin"
forecast_period = "2"
model = "LR"

forecast_periods = [1, 2, 3, 4, 5, 6, 7, 21, 28]


def graph_command_line_arguments(argv=None):
    import sys
    try:
        if argv is None:
            argv = sys.argv
        graph_type, arg_strs = argv[1], argv[2:]
        kwargs = {}
        for s in arg_strs:
            if s.count("=") == 1:
                key, value = s.split("=", 1)
                kwargs[key] = value
        return graph_type, kwargs

    except IndexError:
        pass


def historical_single_prediction(**kwargs):
    global base
    global coin
    global interval
    global forecast_period
    global model
    g_base = base
    g_coin = coin
    g_interval = interval
    g_forecast_period = forecast_period
    g_model = model

    if ("c" in kwargs):
        g_coin = kwargs['c']

    if ("b" in kwargs):
        g_base = kwargs['b']

    if ("i" in kwargs):
        g_interval = kwargs["i"]

    if ("f" in kwargs):
        g_forecast_period = kwargs["f"]

    if ("m" in kwargs):
        g_model = kwargs["m"]

    data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/prediction_logs/{g_base}-{g_coin}_{g_interval}-prediction_log.csv")
    data = data.set_index(data['T'])
    data = data.drop(['T'], axis=1)
    data.index = pd.to_datetime(data.index)
    data = data[['Actual Close', F"{g_model}-{g_forecast_period}"]]
    graph_data = data[data[F"{g_model}-{g_forecast_period}"] != 0]
    #pred_df = data[[F"{model}-{forecast_period}"]]

    #pred_df = pred_df.dropna()
    #pred_start = pred_df.index[0]
    #graph_data = data[(data.index >= pred_start)]

    graph_data.plot()
    plt.show()


"""
def historical_single_prediction(base, coin, interval, forecast_period, model):

    data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv")
    data = data.set_index(data['T'])
    data = data.drop(['T'], axis=1)
    data.index = pd.to_datetime(data.index)
    data = data[['Actual Close', F"{model}-{forecast_period}"]]
    graph_data = data[data[F"{model}-{forecast_period}"] != 0]
    #pred_df = data[[F"{model}-{forecast_period}"]]

    #pred_df = pred_df.dropna()
    #pred_start = pred_df.index[0]
    #graph_data = data[(data.index >= pred_start)]

    graph_data.plot()
    plt.show()
"""
# NOT TESTED


def future_single_prediction(**kwargs):
    global base
    global coin
    global interval
    global forecast_period
    global model
    f_base = base
    f_coin = coin
    f_interval = interval
    f_forecast_period = forecast_period
    f_model = model

    if ("c" in kwargs):
        f_coin = kwargs['c']

    if ("b" in kwargs):
        f_base = kwargs['b']

    if ("i" in kwargs):
        f_interval = kwargs["i"]

    if ("f" in kwargs):
        f_forecast_period = kwargs["f"]

    if ("m" in kwargs):
        f_model = kwargs["m"]

    historical_data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/prediction_logs/{f_base}-{f_coin}_{f_interval}-prediction_log.csv")
    historical_data = historical_data.set_index(historical_data['T'])
    historical_data = historical_data.drop(['T'], axis=1)
    historical_data.index = pd.to_datetime(historical_data.index)
    historical_data = historical_data[['Actual Close', F"{f_model}-{f_forecast_period}"]]
    historical_graph_data = historical_data[historical_data[F"{f_model}-{f_forecast_period}"] != 0]

    future_predictions = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/future_prediction/{f_base}-{f_coin}-{f_interval}-{f_forecast_period}.csv")
    future_predictions = future_predictions.set_index(future_predictions['T'])
    future_predictions = future_predictions.drop(['T'], axis=1)
    future_predictions.index = pd.to_datetime(future_predictions.index)
    future_predictions = future_predictions[["model_predictions"]]

    index = historical_graph_data.index
    historical_index = index.to_series().diff()
    historical_index = pd.DataFrame(historical_index)

    if f_interval == "oneMin":
        time_delta = historical_index.mean()

    if f_interval == "fiveMin":
        time_delta = datetime.timedelta(minutes=5)

    if f_interval == "thirtyMin":
        time_delta = datetime.timedelta(minutes=30)

    if f_interval == "hour":
        time_delta = datetime.timedelta(hours=1)

    if f_interval == "day":
        time_delta = datetime.timedelta(hours=24)

    end_date = historical_index.index[-1]
    future_date = end_date + time_delta

    future_dates = []
    for index in future_predictions.index.values:
        future_dates.append(future_date)
        future_date += time_delta

    future_index = pd.Index(future_dates)
    future_graph_data = pd.DataFrame(future_predictions['model_predictions'].values, index=future_index, columns=[
                                     F'LR-{f_forecast_period}'])

    graph_data = historical_graph_data.append(future_graph_data, sort=True)
    graph_data.plot()
    plt.show()

# NOT FUNCTIONAL


def future_multi_prediction(base, coin, interval, model):
    historical_data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv")
    historical_data = historical_data.set_index(historical_data['T'])
    historical_data = historical_data.drop(['T'], axis=1)
    historical_data.index = pd.to_datetime(historical_data.index)
    historical_data = historical_data[['Actual Close', F"{model}-{forecast_period}"]]
    historical_graph_data = historical_data[historical_data[F"{model}-{forecast_period}"] != 0]

    future_predictions = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/future_prediction/{base}-{coin}-{interval}-{forecast_period}.csv")
    future_predictions = future_predictions.set_index(future_predictions['T'])
    future_predictions = future_predictions.drop(['T'], axis=1)
    future_predictions.index = pd.to_datetime(future_predictions.index)
    future_predictions = future_predictions[["model_predictions"]]

    index = historical_graph_data.index
    historical_index = index.to_series().diff()
    historical_index = pd.DataFrame(historical_index)

    if interval == "oneMin":
        time_delta = historical_index.mean()

    if interval == "fiveMin":
        time_delta = datetime.timedelta(minutes=5)

    if interval == "thirtyMin":
        time_delta = datetime.timedelta(minutes=30)

    if interval == "hour":
        time_delta = datetime.timedelta(hours=1)

    if interval == "day":
        time_delta = datetime.timedelta(hours=24)

    end_date = historical_index.index[-1]
    future_date = end_date + time_delta

    future_dates = []
    for index in future_predictions.index.values:
        future_dates.append(future_date)
        future_date += time_delta

    future_index = pd.Index(future_dates)
    future_graph_data = pd.DataFrame(future_predictions['model_predictions'].values, index=future_index, columns=[
                                     F'LR-{forecast_period}'])

    graph_data = historical_graph_data.append(future_graph_data, sort=True)
    graph_data.plot()
    plt.show()


if __name__ == "__main__":
    import sys
    try:
        method_name, kwargs = graph_command_line_arguments(sys.argv)
        if method_name == "-h":
            print()
            print("---POSSIBLE INPUTS---")
            print("  -Model Types: historical, future")
            print("  -Supported kwargs: ")
            print("     b     :   base currency (USDT is default)")
            print("     c     :   coin (XRP is default)")
            print("     i     :   interval (fiveMin is default)")
            print("     f     :   future periods to predict (5 is default)")
            print("     m     :   model (Linear Regression is default)")
            print()

        if method_name == "historical":
            historical_single_prediction(**kwargs)
        if method_name == "future":
            future_single_prediction(**kwargs)

    except TypeError:
        print()
        print("!!!!!!!!!!    INPUT ERROR: NEED MODEL TYPE   !!!!!!!!!!!")
        print("  -Need to use following syntax: python prediction_grapher.py (model type) (kwargs *optional)")
        print()

        print("  -Supported Model Types: ")
        print("      historical     :    graphs predictions up to last date in raw data files")
        print("      -h         :    Help option, brings up supported arguments")
        print("      future         :   graphs predictions up to last date, and projected out forecast periods")
        print()

        print("  -Supported kwargs: ")
        print("     b     :   base currency (USDT is default)")
        print("     c     :   coin (XRP is default)")
        print("     i     :   interval (fiveMin is default)")
        print("     f     :   future periods to predict (5 is default)")
        print("     m     :   model (Linear Regression is default)")

        print("--------------------------------------------------------------------")
