#!/usr/bin/env python3
"""Indicator Connector Strategy Example.

This example demonstrates how to use the Indicator Connector to retrieve indicator
values from MT5 custom indicators. The strategy uses a simple moving average
crossover logic based on indicator values received through the connector.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from mqpy.indicators import Indicators
from mqpy.tick import Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_indicator_values(
    indicators: Indicators, indicator_name: str, indicator_args: dict[str, Any]
) -> list[float] | None:
    """Get indicator values from MT5 using the IndicatorConnector.

    Args:
        indicators: The Indicators connector instance
        indicator_name: Name of the MT5 indicator
        indicator_args: Dictionary of arguments for the indicator

    Returns:
        List of indicator values or None if the request failed
    """
    try:
        # Request indicator data from MT5
        response = indicators.get_indicator_data(
            indicator_name=indicator_name,
            symbol=indicator_args.get("symbol", ""),
            timeframe=indicator_args.get("timeframe", 0),
            count=indicator_args.get("count", 0),
            lines=indicator_args.get("lines", [0]),
            args=indicator_args.get("args", []),
        )
    except Exception:
        logger.exception("Exception while getting indicator values")
        return None

    # Check if the request was successful (outside the try/except block)
    if response is not None and response.error_code == 0:
        return response.data[0]  # Return the first line's data

    # Handle error case
    logger.error(f"Error getting indicator values: {response.error_message if response else 'No response'}")
    return None


def wait_for_connection(indicators: Indicators, max_attempts: int = 10) -> bool:
    """Wait for the indicator connector to establish a connection.

    Args:
        indicators: The Indicators connector instance
        max_attempts: Maximum number of connection attempts

    Returns:
        True if connection was established, False otherwise
    """
    for attempt in range(max_attempts):
        if indicators.is_connected():
            logger.info("Indicator connector successfully connected")
            return True

        logger.info(f"Waiting for indicator connector to connect... Attempt {attempt + 1}/{max_attempts}")
        time.sleep(1)

    logger.error("Failed to connect to indicator connector after maximum attempts")
    return False


def analyze_moving_averages(fast_ma: list[float], slow_ma: list[float]) -> tuple[bool, bool]:
    """Analyze moving averages to generate trading signals.

    Args:
        fast_ma: Fast moving average values
        slow_ma: Slow moving average values

    Returns:
        Tuple of (buy_signal, sell_signal)
    """
    if len(fast_ma) < 2 or len(slow_ma) < 2:
        return False, False

    # Current values
    current_fast = fast_ma[-1]
    current_slow = slow_ma[-1]

    # Previous values
    previous_fast = fast_ma[-2]
    previous_slow = slow_ma[-2]

    # Generate signals based on crossover
    buy_signal = previous_fast <= previous_slow and current_fast > current_slow
    sell_signal = previous_fast >= previous_slow and current_fast < current_slow

    return buy_signal, sell_signal


def main() -> None:
    """Main execution function for the Indicator Connector strategy."""
    # Initialize the trading strategy
    trade = Trade(
        expert_name="Indicator Connector Strategy",
        version="1.0",
        symbol="EURUSD",
        magic_number=572,
        lot=0.1,
        stop_loss=30,
        emergency_stop_loss=90,
        take_profit=60,
        emergency_take_profit=180,
        start_time="9:15",
        finishing_time="17:30",
        ending_time="17:50",
        fee=0.5,
    )

    logger.info(f"Starting Indicator Connector strategy on {trade.symbol}")

    # Initialize the indicator connector
    indicators = Indicators()

    # Wait for connection to be established
    if not wait_for_connection(indicators):
        logger.error("Could not connect to indicator connector - exiting")
        return

    # Strategy parameters
    prev_tick_time = 0
    # We'll use Moving Average indicator with different periods
    fast_ma_period = 14
    slow_ma_period = 50

    try:
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch current tick data
            current_tick = Tick(trade.symbol)

            # Only process if we have a new tick
            if current_tick.time_msc != prev_tick_time:
                # Set up indicator arguments for fast MA
                fast_ma_args = {
                    "symbol": trade.symbol,
                    "timeframe": 1,  # 1-minute timeframe
                    "count": 10,  # Get 10 values
                    "lines": [0],  # The first line of the indicator
                    "args": [fast_ma_period, 0, 0],  # Period, shift, MA method
                }

                # Set up indicator arguments for slow MA
                slow_ma_args = {
                    "symbol": trade.symbol,
                    "timeframe": 1,  # 1-minute timeframe
                    "count": 10,  # Get 10 values
                    "lines": [0],  # The first line of the indicator
                    "args": [slow_ma_period, 0, 0],  # Period, shift, MA method
                }

                # Get indicator values
                fast_ma_values = get_indicator_values(indicators, "Moving Average", fast_ma_args)
                slow_ma_values = get_indicator_values(indicators, "Moving Average", slow_ma_args)

                # Check if we got valid data
                if fast_ma_values and slow_ma_values:
                    # Log the current indicator values
                    logger.info(f"Fast MA ({fast_ma_period}): {fast_ma_values[-1]:.5f}")
                    logger.info(f"Slow MA ({slow_ma_period}): {slow_ma_values[-1]:.5f}")

                    # Generate signals based on moving average crossovers
                    buy_signal, sell_signal = analyze_moving_averages(fast_ma_values, slow_ma_values)

                    # Log signals
                    if buy_signal:
                        logger.info("Buy signal: Fast MA crossed above Slow MA")
                    elif sell_signal:
                        logger.info("Sell signal: Fast MA crossed below Slow MA")

                    # Execute trading positions based on signals
                    if trade.trading_time():  # Only trade during allowed hours
                        trade.open_position(
                            should_buy=buy_signal, should_sell=sell_signal, comment="Indicator Connector Strategy"
                        )

                # Update trading statistics
                trade.statistics()

                prev_tick_time = current_tick.time_msc

            # Check if it's the end of the trading day
            if trade.days_end():
                trade.close_position("End of the trading day reached.")
                break

            # Add a short delay to avoid excessive CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info("Strategy execution interrupted by user.")
        trade.close_position("User interrupted the strategy.")
    except Exception:
        logger.exception("Error in strategy execution")
    finally:
        logger.info("Finishing the program.")
        # Make sure to disconnect from the indicator connector
        indicators.disconnect()


if __name__ == "__main__":
    main()
