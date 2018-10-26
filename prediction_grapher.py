import pandas as pd
import matplotlib.pyplot as plt
import sys
import datetime

"""
DEFAULT SETTINGS
"""

base = sys.argv[1] if len(sys.argv) > 1 else "USDT"
coin = sys.argv[2] if len(sys.argv) > 2 else "XRP"
interval = sys.argv[3] if len(sys.argv) > 3 else "fiveMin"
forecast_period = sys.argv[4] if len(sys.argv) > 4 else "2"
model = sys.argv[5] if len(sys.argv) > 5 else "LR"


base = 'USDT'
coin = 'XRP'
interval = 'fiveMin'
model = 'LR'
forecast_period = 5

Var = sys.argv[2] if len(sys.argv) > 2 else "empty"


def historical_single_prediction(base, coin, interval, model, forecast_period):
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


historical_single_prediction(base, coin, interval, model, forecast_period)


def future_single_prediction(base, coin, interval, model, forecast_period):
    historical_data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/prediction_logs/{base}-{coin}_{interval}-prediction_log.csv")
    historical_data = historical_data.set_index(historical_data['T'])
    historical_data = historical_data.drop(['T'], axis=1)
    historical_data.index = pd.to_datetime(historical_data.index)
    historical_data = historical_data[['Actual Close', F"{model}-{forecast_period}"]]
    historical_graph_data = historical_data[historical_data[F"{model}-{forecast_period}"] != 0]

    new_data = pd.read_csv(
        F"/users/kylesink82/desktop/forecaster/future_prediction/{base}-{coin}-{interval}-{forecast_period}.csv")
    new_data = new_data.set_index(new_data['T'])
    new_data = new_data.drop(['T'], axis=1)
    new_data.index = pd.to_datetime(new_data.index)
    new_data = new_data[["model_predictions"]]

    if interval == "fiveMin":
        time_delta = datetime.timedelta(minutes=5)

    index = historical_graph_data.index
    historical_index = index.to_series().diff()
    historical_index = pd.DataFrame(historical_index)

    end_date = historical_index.index[-1]
    avg_interval = historical_index.mean()
    future_date = end_date + time_delta

    future_dates = []
    for index in new_data.index.values:
        future_dates.append(future_date)
        future_date += time_delta

    future_index = pd.Index(future_dates)
    future_graph_data = pd.DataFrame(new_data['model_predictions'].values, index=future_index, columns=[
                                     F'LR-{forecast_period}'])
    graph_data = historical_graph_data.append(future_graph_data, sort=True)

    print(historical_graph_data.tail(), new_data.head(), new_data.tail(), graph_data.tail(10))


future_single_prediction(base, coin, interval, "LR", forecast_period)
