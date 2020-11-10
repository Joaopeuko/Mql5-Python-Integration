from Include.trade import Trade
from Include.tick import Tick
from Include.rates import Rates
from Include.indicator_connector import Indicator

# You need this MQL5 service to use indicator:
# https://www.mql5.com/en/market/product/57574
indicator = Indicator()

trade = Trade('Example',  # Expert name
              0.1,  # Expert Version
              'PETR4',  # symbol
              567,  # Magic number
              100.0,  # lot
              10,  # stop loss - 10 cents
              30,  # emergency stop loss - 30 cents
              10,  # take profit - 10 cents
              30,  # emergency take profit - 30 cents
              '9:15',  # It is allowed to trade after that hour. Do not use zeros, like: 09
              '17:30',  # It is not allowed to trade after that hour but let open all the position already opened.
              '17:50',  # It closes all the position opened. Do not use zeros, like: 09
              0.5,  # average fee
              )

time = 0
while True:
    # You need this MQL5 service to use indicator:
    # https://www.mql5.com/en/market/product/57574
    stochastic = indicator.stochastic(symbol=trade.symbol)

    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, 1, 0, 1)

    try:
        k = stochastic['k_result']
        d = stochastic['d_result']

        if tick.time_msc != time:
            buy = (k > d)
            sell = (k < d)

            trade.open_position(buy, sell, 'Example Advisor')

    except TypeError:
        pass

    time = tick.time_msc

    if trade.days_end():
        trade.close_position('End of the trading day reached.')
        break

print('Finishing the program.')
print('Program finished.')
