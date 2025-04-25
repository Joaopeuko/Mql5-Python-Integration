import MetaTrader5 as Mt5
import numpy as np
from include.rates import Rates
from include.tick import Tick
from include.trade import Trade
from include.utilities import Utilities

util = Utilities()

trade = Trade(
    "Example",  # Expert name
    0.1,  # Expert Version
    "EURUSD",  # symbol
    567,  # Magic number
    0.01,  # lot, it is a floating point.
    25,  # stop loss
    300,  # emergency stop loss
    25,  # take profit
    300,  # emergency take profit
    "00:10",  # It is allowed to trade after that hour. Do not use zeros, like: 09
    "23:50",  # It is not allowed to trade after that hour but let open all the position already opened.
    "23:50",  # It closes all the position opened. Do not use zeros, like: 09
    0.0,  # average fee
)

buy = False
sell = False

delay_after_trade = 3
space_to_trade = 3
period = 10

time = 0
while True:
    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, Mt5.TIMEFRAME_M1, space_to_trade, period)

    util.minutes_counter_after_trade(trade.symbol, delay_after_trade)

    if tick.time_msc != time:
        # Zones:
        zone_236 = round(((np.amax(rates.high) - np.amin(rates.low)) * 23.6) * 1000)  # 23.60%

        zone_382 = round(((np.amax(rates.high) - np.amin(rates.low)) * 38.1) * 1000)  # 38.20%

        zone_500 = round(((np.amax(rates.high) - np.amin(rates.low)) * 50.0) * 1000)  # 50.00%

        zone_618 = round(((np.amax(rates.high) - np.amin(rates.low)) * 61.8) * 1000)  # 61.80%

        # Bull trend:
        if (np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0]) < 0:
            # Buy
            buy = tick.ask > np.amax(rates.high) + (zone_382 / 100000) and util.minutes_counter_after_trade(
                trade.symbol, delay_after_trade
            )
            if buy:
                trade.stop_loss = zone_236
                trade.take_profit = zone_618

        # Bear trend:
        if (np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0]) > 0:
            # Sell
            sell = tick.bid < np.amin(rates.low) - (zone_382 / 100000) and util.minutes_counter_after_trade(
                trade.symbol, delay_after_trade
            )
            if sell:
                trade.stop_loss = zone_236
                trade.take_profit = zone_618

        if len(Mt5.positions_get(symbol=trade.symbol)) == 1:
            if Mt5.positions_get(symbol=trade.symbol)[0].type == 0:  # if Buy
                if tick.last > Mt5.positions_get(symbol=trade.symbol)[0].price_open + zone_236:
                    trade.stop_loss = trade.sl_tp_steps

            elif Mt5.positions_get(symbol=trade.symbol)[0].type == 1:  # if Sell
                if tick.last < Mt5.positions_get(symbol=trade.symbol)[0].price_open - zone_236:
                    trade.stop_loss = trade.sl_tp_steps

        trade.emergency_stop_loss = trade.stop_loss + zone_236
        trade.emergency_take_profit = trade.take_profit + zone_236
        trade.open_position(buy, sell, "")

    time = tick.time_msc

    if trade.days_end():
        trade.close_position("End of the trading day reached.")
        break

print("Finishing the program.")
print("Program finished.")
