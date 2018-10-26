import pandas as pd


def data_import_localtz(base, coin, interval, timezone='US/Mountain'):
    raw_data = pd.read_csv(
        F'/users/kylesink82/desktop/forecaster/database/raw_data/{base}-{coin}_{interval}.csv', parse_dates=['T'])
    utc_dates = pd.to_datetime(raw_data['T'])
    utc_dates_index = pd.Index(utc_dates)
    mst_dates_index = utc_dates_index.tz_localize('UTC').tz_convert(timezone)

    data_local_time = raw_data.set_index(mst_dates_index)
    data_local_time = data_local_time.drop(['T'], axis=1)
    return data_local_time


def timezone_conversion(df, timezone='US/Mountain'):
    dates = pd.to_datetime(df['T'])
    utc_index = pd.Index(dates)
    mst_index = utc_index.tz_localize('UTC').tz_convert(timezone)

    localtz_df = df.set_index(mst_index)
    localtz_df = localtz_df.drop(['T'], axis=1)

    return localtz_df
