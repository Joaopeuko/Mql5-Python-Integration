from include.trade import Trade
from include.tick import Tick
from include.rates import Rates


trade = Trade('Example',  # Expert name
              0.1,  # Expert Version
              'WING21',  # symbol
              567,  # Magic number
              1.0,  # lot, it is a floating point.
              25,  # stop loss
              300,  # emergency stop loss
              25,  # take profit
              300,  # emergency take profit
              '9:15',  # It is allowed to trade after that hour. Do not use zeros, like: 09
              '17:30',  # It is not allowed to trade after that hour but let open all the position already opened.
              '17:50',  # It closes all the position opened. Do not use zeros, like: 09
              0.5,  # average fee
              )

time = 0
while True:

    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, 1, 0, 1)

    if tick.time_msc != time:
        buy = (tick.last > rates.open)
        sell = (tick.last < rates.open)

        trade.open_position(buy, sell, 'Example Advisor')

    time = tick.time_msc

    if trade.days_end():
        trade.close_position('End of the trading day reached.')
        break

print('Finishing the program.')
print('Program finished.')
