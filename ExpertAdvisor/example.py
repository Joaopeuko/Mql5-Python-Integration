from Include.trade import Trade
from Include.tick import Tick
from Include.rates import Rates


trade = Trade('Example',  # Expert name
              0.1,        # Expert Version
              'PETR4',    # symbol
              567,        # Magic number
              100.0,      # lot
              10,         # stop loss
              30,         # emergency stop loss
              10,         # take profit
              30,         # emergency take profit
              '9:15',     # It is allowed to trade after that hour. Do not use zeros, like: 09
              '17:30',    # It is not allowed to trade after that hour but let open all the position already opened.
              '17:50',    # It closes all the position opened. Do not use zeros, like: 09
              0.5,        # average fee
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
