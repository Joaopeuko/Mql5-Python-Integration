"""WIN FiMathe Expert Advisor for MetaTrader 5.

This Expert Advisor is designed for WING21 futures, using Fibonacci retracement levels to 
determine entry and exit points.
"""
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
    "WING21",  # symbol
    567,  # Magic number
    1.0,  # lot, it is a floating point.
    25,  # stop loss
    300,  # emergency stop loss
    25,  # take profit
    300,  # emergency take profit
    "9:25",  # It is allowed to trade after that hour. Do not use zeros, like: 09
    "17:45",  # It is not allowed to trade after that hour but let open all the position already opened.
    "17:50",  # It closes all the position opened. Do not use zeros, like: 09
    0.0,  # average fee
)

buy = False
sell = False

delay_after_trade = 5
space_to_trade = 5
period = 15

time = 0
while True:
    tick = Tick(trade.symbol)
    rates = Rates(trade.symbol, Mt5.TIMEFRAME_M1, space_to_trade, period)

    if tick.time_msc != time:
        util.minutes_counter_after_trade(trade.symbol, delay_after_trade)

        # Zones:
        zone_236 = int(trade.sl_tp_steps) * round(
            ((np.amax(rates.high) - np.amin(rates.low)) * 0.236) / int(trade.sl_tp_steps)
        )  # 23.60%

        zone_382 = int(trade.sl_tp_steps) * round(
            ((np.amax(rates.high) - np.amin(rates.low)) * 0.381) / int(trade.sl_tp_steps)
        )  # 38.20%

        zone_500 = int(trade.sl_tp_steps) * round(
            ((np.amax(rates.high) - np.amin(rates.low)) * 0.500) / int(trade.sl_tp_steps)
        )  # 50.00%

        zone_618 = int(trade.sl_tp_steps) * round(
            ((np.amax(rates.high) - np.amin(rates.low)) * 0.618) / int(trade.sl_tp_steps)
        )  # 61.80%

        # Bull trend:
        if np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0] < 0:
            # Buy
            buy = tick.last > np.amax(rates.high) + zone_382 and util.minutes_counter_after_trade(
                trade.symbol, delay_after_trade
            )

            if buy:
                trade.stop_loss = zone_382
                trade.take_profit = zone_618

        # Bear trend:
        if np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0] > 0:
            # Sell
            sell = tick.last < np.amin(rates.low) - zone_382 and util.minutes_counter_after_trade(
                trade.symbol, delay_after_trade
            )
            if sell:
                trade.stop_loss = zone_382
                trade.take_profit = zone_618

        if len(Mt5.positions_get(symbol=trade.symbol)) == 1 and (
            (
                Mt5.positions_get(symbol=trade.symbol)[0].type == 0 and 
                tick.last > Mt5.positions_get(symbol=trade.symbol)[0].price_open + zone_236
            ) or (
                Mt5.positions_get(symbol=trade.symbol)[0].type == 1 and 
                tick.last < Mt5.positions_get(symbol=trade.symbol)[0].price_open - zone_236
            )
        ):
            trade.stop_loss = trade.sl_tp_steps

        trade.emergency_stop_loss = trade.stop_loss
        trade.emergency_take_profit = trade.take_profit
        trade.open_position(buy, sell, "")

    time = tick.time_msc

    if trade.days_end():
        trade.close_position("End of the trading day reached.")
        break
