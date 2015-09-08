__author__ = 'fahri.surucu'


class Position(object):
    def __init__(self, symbol, shares, price, date):
        self.symbol = symbol
        self.price  = price
        self.shares = shares
        self.date   = date
        self.price_list = [price]
        self.share_list = [shares]
        self.date_list  = [date]
        self.transactions = 1

    def current_value(self, price):
        return self.shares * price

    def current_pl(self, price):
        pl = 0
        for k in range(self.transactions):
            pl += (price - self.price_list[k]) * self.share_list[k]
        return pl

    def add_transaction(self, date, price, shares):
        if shares == 0:
            return
        self.date_list.append(date)
        self.price_list.append(price)
        self.share_list.append(shares)
        self.transactions += 1
        self.shares = sum(self.share_list)

