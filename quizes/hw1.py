__author__ = 'fahri.surucu'
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../../QSTK-0.2.6')))

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da


import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import math


def hw1():
    # List of symbols
    symbols = ['C', 'GS', 'IBM', 'HNZ']
    symbols = ['AAPL', 'GOOG', 'NFLX']
    # Start and End dates
    beg = dt.datetime(2011, 1, 1)
    end = dt.datetime(2011, 4, 1)
    # Closing prices at the end of day: hours=16.
    time_day_end = dt.timedelta(hours=16)

    timestamps, prices, returns = get_returns(symbols, beg, end, time_day_end, 'close')
    initial_capital = 1000000.0

    for k in range(len(symbols)):
        symbol = symbols[k]
        print('Symbol: %s' % symbol)
        sharpe = calculate_sharpe_ratio(returns[:, k])
        print('%s\' sharpe ratio: %f' % (symbol, sharpe))
        # Plotting the prices with x-axis=timestamps
        plt.clf()
        plt.plot(timestamps, prices[:, k])
        plt.legend(symbol)
        plt.ylabel('Close')
        plt.xlabel('Date')
        plt.savefig('%s_Close.pdf' % symbol, format='pdf')




def calculate_sharpe_ratio(rets):
    ret_mean = rets.mean()
    ret_std = rets.std()
    sharpe_ratio = math.sqrt(252.0) * ret_mean / ret_std
    return sharpe_ratio


def get_returns(symbols, beg, end, time_of_day, price_type):

    # Trading days between the beg and the end.
    ldt_timestamps = du.getNYSEdays(beg, end, time_of_day)

    # Data Access class with Yahoo as the source.
    data_access = da.DataAccess('Yahoo')

    # Keys to be read from the data, it is good to read everything in one go.
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    data_df = data_access.get_data(ldt_timestamps, symbols, keys)
    data = dict(zip(keys, data_df))

    # Filling the data for NAN
    for s_key in keys:
        data[s_key] = data[s_key].fillna(method='ffill')
        data[s_key] = data[s_key].fillna(method='bfill')
        data[s_key] = data[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices.
    na_price = data[price_type].values

    # Normalizing the prices to start at 1 and see relative returns
    na_normalized_price = na_price / na_price[0, :]
    # Copy the normalized prices to a new ndarry to find returns.
    na_rets = na_normalized_price.copy()
    # Calculate the daily returns of the prices. (Inplace calculation)
    # returnize0 works on ndarray and not dataframes.
    tsu.returnize0(na_rets)

    return ldt_timestamps, na_price, na_rets


def main():
    hw1()


if __name__ == '__main__':
    main()
