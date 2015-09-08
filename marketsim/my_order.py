__author__ = 'fahri.surucu'

import csv
import datetime as dt

from operator import attrgetter

LONG = 'buy'
SHORT = 'sell'


class Order(object):
    ''' Any order to buy or sell of equities should be covered with this class.

    Attributes:
        year:        int indicating the order year
        month:       int indicating the order month
        day:         int indicating the order day
        symbol:      string indicating the symbol of the equity
        order_type:  string either buy or sell as the type of the order
        shares:      int indicating the number of shares
    '''

    def __init__(self, date, symbol, order_type, shares):
        '''Initialize order fields'''
        self.date       = date
        self.symbol     = symbol
        self.order_type = order_type
        self.shares     = shares



def read_orders(orders_file):
    orders = []
    with open(orders_file, 'r') as ofile:
        csv_reader = csv.reader(ofile, delimiter=',')
        for row in csv_reader:
            year, month, day, symbol, buy_sell, shares = row[:6]
            if buy_sell.lower() == 'buy':
                order_type = LONG
                shares = abs(int(shares))
            elif buy_sell.lower() == 'sell':
                order_type = SHORT
                shares = -abs(int(shares))
            date = dt.datetime(int(year), int(month), int(day), 16, 0, 0)
            order = Order(date, symbol, order_type, shares)
            orders.append(order)
    orders = sorted(orders, key=attrgetter('date'))
    return orders


def find_oldest_transaction_date(orders):
    oldest = dt.datetime(3000, 1, 1, 16, 0, 0)
    for order in orders:
        if order.date < oldest:
            oldest = order.date
    return oldest


def find_latest_transaction_date(orders):
    latest = dt.datetime(1000, 1, 1, 16, 0, 0)
    for order in orders:
        if order.date > latest:
            latest = order.date
    return latest


def get_symbol_list(orders):
    symbol_list = list()
    for o in orders:
        if not o.symbol in symbol_list:
            symbol_list.append(o.symbol)
    return symbol_list

