#!/usr/bin/env python3
"""Basic Moving Average Crossover Strategy Example.

This example demonstrates a simple moving average crossover strategy using the mqpy framework.
When a shorter-period moving average crosses above a longer-period moving average,
the strategy generates a buy signal. Conversely, when the shorter-period moving average
crosses below the longer-period moving average, the strategy generates a sell signal.
"""

from __future__ import annotations

import logging

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def calculate_sma(prices: list[float], period: int) -> float | None:
    """Calculate Simple Moving Average.

    Args:
        prices: A list of price values
        period: The period for the moving average calculation

    Returns:
        The simple moving average value or None if insufficient data
    """
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period


def main() -> None:
    """Main execution function for the Moving Average Crossover strategy."""
    # Initialize the trading strategy
    trade = Trade(
        expert_name="Moving Average Crossover",
        version="1.0",
        symbol="EURUSD",
        magic_number=567,
        lot=0.1,
        stop_loss=25,
        emergency_stop_loss=300,
        take_profit=25,
        emergency_take_profit=300,
        start_time="9:15",
        finishing_time="17:30",
        ending_time="17:50",
        fee=0.5,
    )

    logger.info(f"Starting Moving Average Crossover strategy on {trade.symbol}")

    # Strategy parameters
    prev_tick_time = 0
    short_period = 5
    long_period = 20

    # Variables to track previous state for crossover detection
    prev_short_ma = None
    prev_long_ma = None

    try:
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch tick and rates data
            current_tick = Tick(trade.symbol)
            historical_rates = Rates(trade.symbol, long_period + 10, 0, 1)  # Get extra data for reliability

            # Only process if we have a new tick and enough historical data
            has_new_tick = current_tick.time_msc != prev_tick_time
            has_enough_data = len(historical_rates.close) >= long_period

            if has_new_tick and has_enough_data:
                # Calculate moving averages
                short_ma = calculate_sma(historical_rates.close, short_period)
                long_ma = calculate_sma(historical_rates.close, long_period)

                # Check if we have enough data for comparison
                has_short_ma = short_ma is not None
                has_long_ma = long_ma is not None
                has_prev_short_ma = prev_short_ma is not None
                has_prev_long_ma = prev_long_ma is not None
                has_valid_ma_values = has_short_ma and has_long_ma and has_prev_short_ma and has_prev_long_ma

                if has_valid_ma_values:
                    # Check short MA and long MA relationship for current and previous values
                    is_above_now = short_ma > long_ma
                    is_above_prev = prev_short_ma > prev_long_ma

                    # Detect crossover (short MA crosses above long MA)
                    cross_above = is_above_now and not is_above_prev

                    # Detect crossunder (short MA crosses below long MA)
                    cross_below = not is_above_now and is_above_prev

                    # Log crossover events
                    if cross_above:
                        logger.info(
                            f"Bullish crossover detected: Short MA ({short_ma:.5f}) "
                            f"crossed above Long MA ({long_ma:.5f})"
                        )
                    elif cross_below:
                        logger.info(
                            f"Bearish crossover detected: Short MA ({short_ma:.5f}) "
                            f"crossed below Long MA ({long_ma:.5f})"
                        )

                    # Execute trading positions based on signals
                    if trade.trading_time():  # Only trade during allowed hours
                        trade.open_position(
                            should_buy=cross_above, should_sell=cross_below, comment="Moving Average Crossover Strategy"
                        )

                # Update previous MA values for next comparison
                prev_short_ma = short_ma
                prev_long_ma = long_ma

                # Update trading statistics periodically
                trade.statistics()

                prev_tick_time = current_tick.time_msc

            # Check if it's the end of the trading day
            if trade.days_end():
                trade.close_position("End of the trading day reached.")
                break

    except KeyboardInterrupt:
        logger.info("Strategy execution interrupted by user.")
        trade.close_position("User interrupted the strategy.")
    except Exception:
        logger.exception("Error in strategy execution")
    finally:
        logger.info("Finishing the program.")


if __name__ == "__main__":
    main()
