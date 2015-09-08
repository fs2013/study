__author__ = 'fahri.surucu'

import csv
import os
import sys

import my_portfolio
import my_order

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


def marketsim(initial_capital, orders_file, output_file):
    ''' identify dates for the simulation
    '''
    orders = my_order.read_orders(orders_file)
    dt_start = my_order.find_oldest_transaction_date(orders) - dt.timedelta(days=1)
    dt_end = my_order.find_latest_transaction_date(orders) + dt.timedelta(days=1)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    ''' initialize the portfolio with the input capital
    '''
    portfolio = my_portfolio.Portfolio(initial_capital)
    print('Portfolio:\n\t%14s: %.2f\n\t%14s: %.2f\n' % ('current_value', portfolio.current_value,
                                                        'cash', portfolio.cash_amount))


    ''' Obtain price data for all the symbols
    '''
    ls_symbols = my_order.get_symbol_list(orders)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    dataobj = da.DataAccess('Yahoo')
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_price = d_data['close']

    df_portfolio = pd.DataFrame(np.zeros(df_price.shape), index=ldt_timestamps,
                                columns=['current_value', 'cash_amount', 'number_of_positions', 'p&l'])

    with open(output_file, 'wt') as out:
        csv_writer = csv.writer(out, delimiter=',')
        iorder = 0
        number_of_orders = len(orders)
        for date in ldt_timestamps:
            while iorder < number_of_orders and orders[iorder].date == date:
                portfolio.add_transaction(orders[iorder], df_price)
                iorder += 1
            value, cash, npositions = portfolio.current_positions_value(date, df_price)
            df_portfolio.loc[date,:] = [value, cash, npositions, value - initial_capital]
            out_row = [date.year, date.month, date.day, value, value-initial_capital]
            csv_writer.writerow(out_row)


def main():
    usage = '''usage: python marketsim.py 1000000 orders.csv values.csv
            '''
    args = sys.argv
    if len(args) != 4:
        print(usage)
        return

    for arg in args:
        print(arg)
    initial_capital = float(args[1])
    orders_file = args[2]
    output_file = args[3]
    marketsim(initial_capital, orders_file, output_file)


if __name__ == '__main__':
    main()
