__author__ = 'fahri.surucu'


import datetime as dt


LONG = 'buy'
SHORT = 'sell'

import Position

class Portfolio(object):
    ''' A portfolio class consists of a number of equity positions and some cash.
    Each position is represented by a stock symbol, position type (long or short),
    number of shares, original price (bought or sold)

    Attributes:
        year:        int indicating the order year
        month:       int indicating the order month
        day:         int indicating the order day
        symbol:      string indicating the symbol of the equity
        order_type:  string either buy or sell as the type of the order
        shares:      int indicating the number of shares
    '''

    def __init__(self, capital):
        self.position_list = []
        self.current_value = capital
        self.cash_amount   = capital
        self.max_drawdown  = 0.0
        self.mean_return   = 0.0
        self.std           = 0.0
        self.sharpe_ratio  = 0.0
        self.sortino_ratio = 0.0

    def add_transaction(self, order, price_data):
        shares = order.shares
        symbol = order.symbol
        date = order.date
        price = price_data[symbol].ix[date]
        transaction_value = shares * price
        self.cash_amount -= transaction_value

        ''' Check if a position with the same symbol already exists
        '''
        for k in range(len(self.position_list)):
            pos = self.position_list[k]
            if pos.symbol == symbol:
                pos.add_transaction(date, price, shares)
                self.position_list[k] = pos
                print('\tOn:%s %s %d shares of %s @ $%f' % (date.strftime('%b %d, %Y'), order.order_type, shares,
                                                              symbol, price))
                print('\t\tCash amount:%d' % self.cash_amount)
                return

        ''' A new position is being added with this transaction
        '''
        pos = Position.Position(symbol, shares, price, date)
        self.position_list.append(pos)
        print('\tOn:%s %s %d shares of %s @ $%f' % (date.strftime('%b %d, %Y'), order.order_type, shares, symbol,
                                                      price))
        print('\t\tCash amount:%d' % self.cash_amount)


    def current_positions_value(self, date, price_data):
        current_value = 0.0
        npositions = 0
        for position in self.position_list:
            symbol = position.symbol
            current_value += position.shares * price_data[symbol].ix[date]
            if position.shares != 0:
                npositions += 1
        return current_value + self.cash_amount, self.cash_amount, npositions

