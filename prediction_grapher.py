import pandas as pd
import matplotlib.pyplot as plt
import sys

"""
DEFAULT SETTINGS
Update to accept optional arguments for easier use at commandline
"""

base = sys.argv[1] if len(sys.argv) > 1 else "USDT"
coin = sys.argv[2] if len(sys.argv) > 2 else "XRP"
interval = sys.argv[3] if len(sys.argv) > 3 else "fiveMin"
forecast_period = sys.argv[4] if len(sys.argv) > 4 else "2"
model = sys.argv[5] if len(sys.argv) > 5 else "LR"


"""
base = 'USDT'
coin = 'XRP'
interval = 'fiveMin'
model = 'LR'
forecast_period = 2

Var = sys.argv[2] if len(sys.argv) > 2 else "empty"
"""


def graph_predictions(base, coin, interval, model, forecast_period):
    data = pd.read_csv(
        F"/crypto_forecaster/prediction_logs/{base}-{coin}_{interval}.csv")
    data = data.set_index(data['T'])
    data = data.drop(['T'], axis=1)
    data.index = pd.to_datetime(data.index)
    data = data[['Actual Close', F"{model}-{forecast_period}"]]
    pred_df = data[[F"{model}-{forecast_period}"]]

    pred_df = pred_df.dropna()
    pred_start = pred_df.index[0]
    graph_data = data[(data.index >= pred_start)]

    graph_data.plot()
    plt.show()


graph_predictions(base, coin, interval, model, forecast_period)
