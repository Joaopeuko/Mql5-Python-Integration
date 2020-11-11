from Include.trade import Trade
from Include.tick import Tick
from Include.rates import Rates
from Include.indicator_connector import Indicator
import MetaTrader5 as Mt5

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

    # Example of calling the same indicator with different parameters.
    stochastic_now = indicator.stochastic(symbol=trade.symbol, time_frame=Mt5.TIMEFRAME_M1)
    stochastic_past3 = indicator.stochastic(symbol=trade.symbol, time_frame=Mt5.TIMEFRAME_M1, start_position=3)

    moving_average = indicator.moving_average(symbol=trade.symbol, period=50)

    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, 1, 0, 1)

    # It uses "try" and catch because sometimes it returns None.
    try:

        # When in doubt how to handle the indicator, print it, it returns a Dictionary.
        # print(moving_average)
        # It prints:
        # {'symbol': 'PETR4', 'time_frame': 1, 'period': 50, 'start_position': 0, 'method': 0,
        # 'applied_price': 0, 'moving_average_result': 23.103}

        k_now = stochastic_now['k_result']
        d_now = stochastic_now['d_result']

        k_past3 = stochastic_now['k_result']
        d_past3 = stochastic_now['d_result']

        if tick.time_msc != time:
            # It is trading of the time frame of one minute.
            #
            # Stochastic logic:
            # To do the buy it checks if the K value at present is higher than the D value and
            # if the K at 3 candles before now was lower than the D value.
            # For the selling logic, it is the opposite of the buy logic.
            #
            # Moving Average Logic:
            # If the last price is higher than the Moving Average it allows to open a buy position.
            # If the last price is lower than the Moving Average it allows to open a sell position.
            #
            # To open a position this expert combines the Stochastic logic and Moving Average.
            # When Stochastic logic and Moving Average logic are true, it open position to the determined direction.

            # It is the buy logic.
            buy = (

                # Stochastic
                (
                        k_now > d_now
                        and
                        k_past3 < d_past3
                )

                and

                # Moving Average
                (
                        tick.last > moving_average['moving_average_result']
                )

            )  # End of buy logic.

            # -------------------------------------------------------------------- #

            # It is the sell logic.
            sell = (
                # Stochastic
                (
                        k_now < d_now
                        and
                        k_past3 > d_past3
                )

                and

                # Moving Average
                (
                        tick.last < moving_average['moving_average_result']
                )
            )  # End of sell logic.

            # -------------------------------------------------------------------- #

            # When buy or sell are true, it open a position.
            trade.open_position(buy, sell, 'Example Advisor Comment, the comment here can be seen in MetaTrader5')

    except TypeError:
        pass

    time = tick.time_msc

    if trade.days_end():
        trade.close_position('End of the trading day reached.')
        break

print('Finishing the program.')
print('Program finished.')
