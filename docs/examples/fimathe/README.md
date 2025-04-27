
# Fimathe

This is a simple version that I made for Fimathe strategy to be used as a base for your strategy
and your improvements.

This strategy does not cover price reversion.
It covers only continuity.

# Table of contents:

- [Strategy](#strategy)

- [Example](#example)
  - [Forex:](#forex)
    - [EURUSD](#eurusd)
  - [B3 - Brazilian Stock Exchange:](#b3---brazilian-stock-exchange)
    - [WIN](#win)




## Strategy:

The initial setup is the area that the price has the freedom to move, which goes from 0, the most recent candle,
to the 5 past candles.
```python
space_to_trade = 5
```

How many bars in the past the code will be check to calculate the Fibonacci Zones.
```python
period = 15
```
The period starts after the space_to_trade. (5 + 15)


The trading zones are calculated with the difference from high and low price inside of period, in this example
the period is 15 after the freedom movement.

The difference is multiplied by their percentage amount desired to find the zone.
```python
# Zones:
zone_236 = int(trade.sl_tp_steps) * round(((np.amax(rates.high) -
                                            np.amin(rates.low)) * 0.236) / int(trade.sl_tp_steps))  # 23.60%

zone_382 = int(trade.sl_tp_steps) * round(((np.amax(rates.high) -
                                            np.amin(rates.low)) * 0.381) / int(trade.sl_tp_steps))  # 38.20%

zone_500 = int(trade.sl_tp_steps) * round(((np.amax(rates.high) -
                                            np.amin(rates.low)) * 0.500) / int(trade.sl_tp_steps))  # 50.00%

zone_618 = int(trade.sl_tp_steps) * round(((np.amax(rates.high) -
                                            np.amin(rates.low)) * 0.618) / int(trade.sl_tp_steps))  # 61.80%
```

The strategy to open a position check the trend:
```python
# Bull trend:
if np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0] < 0:

# Bear trend:
if np.where(rates.low == np.amin(rates.low))[0][0] - np.where(rates.high == np.amax(rates.high))[0][0] > 0:
```
The strategy looks for the minimum and maximum values and identifies their array position.

With the array position, it is possible to identify the slop direction.

Example 1:
Low position = 8
High position = 10
8 - 10 = -2,
which means bull trend, because the high price are farther than the low price.

Example 2:
Low position = 12
High position = 7
12 - 7 = 5,
which meas bear trend, because the low price are farther than the high price.

For open a BUY position the strategy waits the price goes 38.2% above the highest price in 15 period.
```python
buy = tick.last > np.amax(rates.high) + zone_382 and \
      util.minutes_counter_after_trade(trade.symbol, delay_after_trade)
```

To open the SELL position, the logic is the same, however, it waits the price goes below 38.2% the
lowest price in 15 periods.
```python
sell = tick.last < np.amin(rates.low) - zone_382 and \
                   util.minutes_counter_after_trade(trade.symbol, delay_after_trade)
```
Also, for buy and sell, it checks if some operation recently happened.
When a recent operation has happened, it will wait for the number of minutes to return True to trade again.
```python
util.minutes_counter_after_trade(trade.symbol, delay_after_trade)
```
The util.minutes_counter_after_trade, when not used as a condition to open a position, it prints how many minutes
remains to be able to trade again.

The amount of minutes the strategy waits to be able to open a new position is set by the user
through the variable delay_after_trade = 5

After the position is opened the StopLoss and TakeProfit are applied.
The StopLoss will be at 38.2% of the opened price, and the TakeProfit will be at 61.8% of the opened price.
```python
trade.stop_loss = zone_382
trade.take_profit = zone_618
```

Also, the stop is moved when the price goes to right direction, when the price moved more than 23.6% for the right
direction, the stop is moved to the nearest price to zero.
```python
if len(Mt5.positions_get(symbol=trade.symbol)) == 1:

    if Mt5.positions_get(symbol=trade.symbol)[0].type == 0:  # if Buy
        if tick.last > Mt5.positions_get(symbol=trade.symbol)[0].price_open + zone_236:
            trade.stop_loss = trade.sl_tp_steps

    elif Mt5.positions_get(symbol=trade.symbol)[0].type == 1:  # if Sell
        if tick.last < Mt5.positions_get(symbol=trade.symbol)[0].price_open - zone_236:
            trade.stop_loss = trade.sl_tp_steps
```

## Example:

- ## Forex:
  - ## [EURUSD](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/examples_of_expert_advisor/Fimathe/eurusd_fimathe.py)
- ## B3 - Brazilian Stock Exchange:
  - ## [WIN](https://github.com/Joaopeuko/Mql5-Python-Integration/blob/master/examples_of_expert_advisor/Fimathe/win_fimathe.py)
