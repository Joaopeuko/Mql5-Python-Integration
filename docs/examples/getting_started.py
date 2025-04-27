#!/usr/bin/env python3
"""Getting Started with MQPy.

This example demonstrates the basic usage of the MQPy framework for algorithmic trading
with MetaTrader 5. It shows how to fetch market data, access price information, and
execute basic trading operations.
"""

import logging

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Main execution function for the Getting Started example."""
    # Step 1: Initialize the trading strategy with basic parameters
    # This creates a Trade object that will handle your trading operations
    trade = Trade(
        expert_name="Getting Started Example",  # Name of your trading strategy
        version="1.0",  # Version of your strategy
        symbol="EURUSD",  # Trading symbol/instrument
        magic_number=123,  # Unique identifier for your strategy's trades
        lot=0.01,  # Trade size in lots (0.01 = micro lot)
        stop_loss=20,  # Stop loss in points
        emergency_stop_loss=100,  # Emergency stop loss in points
        take_profit=40,  # Take profit in points
        emergency_take_profit=120,  # Emergency take profit in points
        start_time="9:00",  # Trading session start time
        finishing_time="17:00",  # Time to stop opening new positions
        ending_time="17:30",  # Time to close all positions
        fee=0.0,  # Commission fee
    )

    # Log that we're starting the strategy
    logger.info(f"Starting Getting Started example on {trade.symbol}")

    # Step 2: Get current market data
    # Fetch the current tick data (latest price) for our trading symbol
    current_tick = Tick(trade.symbol)

    # Display the current price information
    logger.info(f"Current price for {trade.symbol}:")
    logger.info(f"  Bid price: {current_tick.bid}")  # Price at which you can sell
    logger.info(f"  Ask price: {current_tick.ask}")  # Price at which you can buy
    logger.info(f"  Last price: {current_tick.last}")  # Last executed price

    # Step 3: Get historical price data
    # Fetch the last 10 candles of price data
    historical_rates = Rates(trade.symbol, 10, 0, 1)  # 10 candles, starting from the most recent (0), timeframe M1

    # Display the historical price data
    logger.info(f"Last 10 candles for {trade.symbol}:")
    for i in range(min(3, len(historical_rates.time))):  # Show only first 3 candles for brevity
        logger.info(f"  Candle {i+1}:")
        logger.info(f"    Open: {historical_rates.open[i]}")
        logger.info(f"    High: {historical_rates.high[i]}")
        logger.info(f"    Low: {historical_rates.low[i]}")
        logger.info(f"    Close: {historical_rates.close[i]}")
        logger.info(f"    Volume: {historical_rates.tick_volume[i]}")

    # Step 4: Prepare the trading environment
    # This ensures the symbol is ready for trading
    trade.prepare_symbol()

    # Step 5: Implement a very simple trading logic
    # For this example, we'll use a simple condition:
    # Buy if the current price is higher than the average of the last 10 candles
    # Sell if the current price is lower than the average of the last 10 candles

    # Calculate the average price of the last 10 candles
    average_price = sum(historical_rates.close) / len(historical_rates.close)
    logger.info(f"Average closing price of last 10 candles: {average_price}")

    # Set up our trading signals
    should_buy = current_tick.ask > average_price
    should_sell = current_tick.bid < average_price

    # Log our trading decision
    if should_buy:
        logger.info(f"Buy signal generated: Current price ({current_tick.ask}) > Average price ({average_price})")
    elif should_sell:
        logger.info(f"Sell signal generated: Current price ({current_tick.bid}) < Average price ({average_price})")
    else:
        logger.info("No trading signal generated")

    # Step 6: Execute a trade if we're within trading hours
    if trade.trading_time():
        logger.info("Within trading hours, executing trade if signals are present")
        trade.open_position(should_buy=should_buy, should_sell=should_sell, comment="Getting Started Example Trade")
    else:
        logger.info("Outside trading hours, not executing any trades")

    # Step 7: Update trading statistics and log current positions
    trade.statistics()

    # Step 8: Demonstrate how to close all positions at the end of the trading day
    logger.info("Demonstrating position closing (not actually closing any positions)")

    # NOTE: In a real strategy, you would check if it's the end of the day and close positions
    # This would be implemented by checking days_end() and calling close_position()

    logger.info("Getting started example completed")


if __name__ == "__main__":
    main()
