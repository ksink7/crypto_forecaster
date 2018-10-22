import pandas as pd
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler
import time

#sched = BlockingScheduler()

#oins = ['BTC', 'ETH', 'XRP', 'TRX', 'SC', 'LTC', 'BCH', 'ADA', 'XVG', 'ZEC']

#@sched.scheduled_job('interval', hours=48)


def database_update(base, coin, interval):
    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_{interval}.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval={interval}'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_{interval}.csv', index=True)

            #print(F"Updated Minute Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval={interval}'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_{interval}.csv', index=True)
            #print(F"Downloaded new Minute data for {coin}")
            break


def oneMin_ohlc_download(base, coin):

    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_oneMin.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=oneMin'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_oneMin.csv', index=True)

            #print(F"Updated Minute Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=oneMin'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_oneMin.csv', index=True)
            #print(F"Downloaded new Minute data for {coin}")
            break

#@sched.scheduled_job('interval', hours=48)


def fiveMin_ohlc_download(base, coin):

    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_fiveMin.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=fiveMin'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_fiveMin.csv', index=True)

            #print(F"Updated Five Minute Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=fiveMin'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_fiveMin.csv', index=True)
            #print(F"Downloaded new Five Minute data for {coin}")
            break

#@sched.scheduled_job('interval', hours=48)


def thirtyMin_ohlc_download(base, coin):

    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_thirtyMin.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=thirtyMin'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_thirtyMin.csv', index=True)

            #print(F"Updated Thirty Minute Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=thirtyMin'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_thirtyMin.csv', index=True)
            #print(F"Downloaded new Thirty Minute data for {coin}")
            break

#@sched.scheduled_job('interval', hours=48)


def hour_ohlc_download(base, coin):

    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_hour.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=hour'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_hour.csv', index=True)

            #print(F"Updated Hour Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=hour'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_hour.csv', index=True)
            #print(F"Downloaded new Hour data for {coin}")
            break

#@sched.scheduled_job('interval', hours=48)


def day_ohlc_download(base, coin):

    while True:
        try:
            data_load = pd.read_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_DAILY.csv')
            loaded_df = data_load.set_index(data_load['T'])
            loaded_df = loaded_df.drop(["T"], axis=1)
            loaded_df.index = pd.to_datetime(loaded_df.index)

            new_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=day'
            new_data = pd.read_json(new_link)
            new_data = new_data['result']
            new_data_df = new_data.apply(pd.Series)
            new_data_df = new_data_df .set_index(new_data_df['T'])
            new_data_df = new_data_df.drop(['T'], axis=1)
            new_data_df.index = pd.to_datetime(new_data_df.index)
            joined_df = pd.concat([loaded_df, new_data_df])
            joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
            joined_df.to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_DAILY.csv', index=True)

            #print(F"Updated Daily Data for {base}-{coin}")
            break
        except OSError:
            api_link = F'https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName={base}-{coin}&tickInterval=day'
            daily_data = pd.read_json(api_link)
            daily_data = daily_data['result']
            new_df = daily_data.apply(pd.Series)
            new_df = new_df .set_index(new_df['T'])
            new_df = new_df .drop(['T'], axis=1)
            new_df .index = pd.to_datetime(new_df .index)
            new_df .to_csv(
                F'/crypto_forecaster/database/raw_data/{base}-{coin}_DAILY.csv', index=True)
            #print(F"Downloaded new Daily data for {coin}")
            break


"""
CURRENTLY NOT WORKING, BITTREX API CHANGED AND URL DOES NOT WORK
"""


def market_history_download():

    global coins
    base = 'USDT'

    for coin in coins:
        while True:
            try:
                data_load = pd.read_csv(
                    F'/crypto_forecaster/database/raw_data/{base}-{coin}_MarketHistory.csv')
                loaded_df = data_load.set_index(data_load['T'])
                loaded_df = loaded_df.drop(["T"], axis=1)
                loaded_df.index = pd.to_datetime(loaded_df.index)

                new_link = F'https://bittrex.com/api/v2.0/pub/market/GetMarketHistory?marketName={base}-{coin}&_='
                new_data = pd.read_json(new_link)
                new_data = new_data['result']
                new_data_df = new_data.apply(pd.Series)
                new_data_df = new_data_df .set_index(new_data_df['T'])
                new_data_df = new_data_df.drop(['T'], axis=1)
                new_data_df.index = pd.to_datetime(new_data_df.index)
                joined_df = pd.concat([loaded_df, new_data_df])
                joined_df = joined_df[~joined_df.index.duplicated(keep='last')]
                joined_df.to_csv(
                    F'/crypto_forecaster/database/raw_data/{base}-{coin}_MarketHistory.csv', index=True)

                print(F"Updated Market History Data for {base}-{coin}")
                break
            except OSError:
                api_link = F'https://bittrex.com/api/v2.0/pub/market/GetMarketHistory?marketName={base}-{coin}&_='
                daily_data = pd.read_json(api_link)
                daily_data = daily_data['result']
                new_df = daily_data.apply(pd.Series)
                new_df = new_df .set_index(new_df['T'])
                new_df = new_df .drop(['T'], axis=1)
                new_df .index = pd.to_datetime(new_df .index)
                new_df .to_csv(
                    F'/crypto_forecaster/database/raw_data/{base}-{coin}_MarketHistory.csv', index=True)
                print(F"Downloaded new Market History data for {coin}")
                break


"""
USE DECORATORS TO HAVE PROGRAM RUNNING ON A SCHEDULE IF DESIRED
CURRENTLY BEING UPDATED WHEN MAIN FUNCTION IS RAN FOR PREDICTION_BUILDER
"""
#print("Starting Pricing Data Scheduler")
# sched.start()
"""
print()
print("--------------DOWNLOADING NEW ONE MINUTE OHLC DATA---------------------")
oneMin_ohlc_download()
print("--------------COMPLETED ONE MINUTE OHLC DATA DOWNLOAD ---------------")
print()

print("--------------DOWNLOADING NEW FIVE MINUTE OHLC DATA--------------------")
fiveMin_ohlc_download()
print("--------------COMPLETED FIVE MINUTE OHLC DATA DOWNLOAD ---------------")
print()

print("--------------DOWNLOADING NEW THIRTY MINUTE OHLC DATA----------------")
thirtyMin_ohlc_download()
print("--------------COMPLETED THIRTY MINUTE OHLC DATA DOWNLOAD ---------------")
print()

print("--------------DOWNLOADING NEW HOURLY OHLC DATA---------------------------")
hour_ohlc_download()
print("--------------COMPLETED HOURLY  OHLC DATA DOWNLOAD ---------------")
print()

print("--------------DOWNLOADING NEW DAILY OHLC DATA------------------------------")
day_ohlc_download()
print("--------------COMPLETED DAILY OHLC DATA DOWNLOAD ---------------")
print()
"""
