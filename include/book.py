import MetaTrader5 as Mt5


class Book:
    def __init__(self,
                 symbol):
        self.symbol = symbol
        if Mt5.market_book_add(self.symbol):
            print(f'The symbol {self.symbol} was successfully added to market book.')

        else:
            print(f'Some thing happened adding {self.symbol} to market book, error: {Mt5.last_error()}')

    def get(self):
        return Mt5.market_book_get(self.symbol)

    def release(self):
        return Mt5.market_book_release(self.symbol)
