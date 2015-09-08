__author__ = 'fahri.surucu'
import os
import sys

import csv
from marketsim import my_portfolio
from marketsim import my_order


here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(here, '../../QSTK-0.2.6')))


import pandas as pd
import numpy as np
import math
import copy

import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep



LONG = 'buy'
SHORT = 'sell'



def find_current_value(orders_file, year, month, day):
    orders = my_order.read_orders(orders_file)

    ''' identify dates for the simulation
    '''
    dt_start = find_oldest_transaction_date(orders)
    dt_end = dt.datetime(year, month, day) + dt.timedelta(days=1)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    ls_symbols = []
    for o in orders:
        if not o.symbol in ls_symbols:
            ls_symbols.append(o.symbol)

    dataobj = da.DataAccess('Yahoo')

    ''' Data Access for the symbols
    '''
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_price = d_data['actual_close']

    today = dt.datetime(year, month, day, 16, 0, 0)
    portfolio = my_portfolio.Portfolio(0.0)
    for order in orders:
        odate = dt.datetime(order.year, order.month, order.day)
        if odate < today:
            portfolio.add_transaction(order, df_price)
            print('\t\t%s: portfolio value=%f' % (today.strftime('%b %d, %Y'),
                                                  portfolio.current_positions_value(today, df_price)))

    print('%s: portfolio value=%f' % (today.strftime('%b %d, %Y'), portfolio.current_positions_value(today, df_price)))


def main():
    find_current_value('../resources/orders.csv', 2011, 11, 9)
    find_current_value('../resources/orders2.csv', 2011, 11, 9)


if __name__ == '__main__':
    main()
