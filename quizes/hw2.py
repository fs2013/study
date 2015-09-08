__author__ = 'fahri.surucu'
import os
import sys

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

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data, price_type, price_threshold):
    ''' Finding the event dataframe '''
    df_price = d_data[price_type]
    print('Finding Events')

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_price)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_price.index

    n = 0
    for s_sym in ls_symbols:
        n += 1
        print('%d: %s' % (n, s_sym))
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_price[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_price[s_sym].ix[ldt_timestamps[i - 1]]

            # Event is found if the symbol is less than 5 today while being more or equal to 5.0 yesterday
            if f_symprice_yest >= price_threshold and f_symprice_today < price_threshold:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events


def question(symbol_list, price_type, price_threshold):
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)

    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    ls_symbols = dataobj.get_symbols_from_list(symbol_list)
    ls_symbols.append('SPY')

    print('Question2: Data Access for %s symbols' % symbol_list)
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    df_events = find_events(ls_symbols, d_data, price_type, price_threshold)
    print('Creating Study')
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20, b_market_neutral=True, b_errorbars=True,
                     s_filename='Thr_%s_EventProfiler_for_%s.pdf' % (str(price_threshold), symbol_list),
                     s_market_sym='SPY')


def main():
    question('sp5002008', 'actual_close', 7.0)
    question('sp5002012', 'actual_close', 10.0)

if __name__ == '__main__':
    main()
