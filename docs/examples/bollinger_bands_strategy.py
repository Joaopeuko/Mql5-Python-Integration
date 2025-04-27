#!/usr/bin/env python3
"""Bollinger Bands Strategy Example.

This example demonstrates a Bollinger Bands trading strategy using the mqpy framework.
The strategy enters long positions when price breaks below the lower band and enters
short positions when price breaks above the upper band. The strategy is designed to
trade price reversals from extreme movements.
"""

from __future__ import annotations

import logging

import numpy as np

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def calculate_bollinger_bands(
    prices: list[float], period: int = 20, num_std_dev: float = 2.0
) -> tuple[float, float, float] | None:
    """Calculate Bollinger Bands (middle, upper, lower).

    Args:
        prices: A list of closing prices
        period: The period for SMA calculation, default is 20
        num_std_dev: Number of standard deviations for bands, default is 2.0

    Returns:
        A tuple of (middle_band, upper_band, lower_band) or None if not enough data
    """
    if len(prices) < period:
        return None

    # Convert to numpy array for vectorized calculations
    price_array = np.array(prices[-period:])

    # Calculate SMA (middle band)
    sma = np.mean(price_array)

    # Calculate standard deviation
    std_dev = np.std(price_array)

    # Calculate upper and lower bands
    upper_band = sma + (num_std_dev * std_dev)
    lower_band = sma - (num_std_dev * std_dev)

    return (sma, upper_band, lower_band)


def main() -> None:
    """Main execution function for the Bollinger Bands strategy."""
    # Initialize the trading strategy
    trade = Trade(
        expert_name="Bollinger Bands Strategy",
        version="1.0",
        symbol="EURUSD",
        magic_number=569,
        lot=0.1,
        stop_loss=50,
        emergency_stop_loss=150,
        take_profit=100,
        emergency_take_profit=300,
        start_time="9:15",
        finishing_time="17:30",
        ending_time="17:50",
        fee=0.5,
    )

    logger.info(f"Starting Bollinger Bands strategy on {trade.symbol}")

    # Strategy parameters
    prev_tick_time = 0
    bb_period = 20
    bb_std_dev = 2.0

    try:
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch tick and rates data
            current_tick = Tick(trade.symbol)
            historical_rates = Rates(trade.symbol, bb_period + 10, 0, 1)  # Get extra data for reliability

            # Only process if we have a new tick
            if current_tick.time_msc != prev_tick_time and len(historical_rates.close) >= bb_period:
                # Calculate Bollinger Bands
                bb_result = calculate_bollinger_bands(historical_rates.close, period=bb_period, num_std_dev=bb_std_dev)

                if bb_result:
                    middle_band, upper_band, lower_band = bb_result
                    current_price = current_tick.last

                    # Generate signals based on price position relative to bands
                    # Buy when price crosses below lower band (potential bounce)
                    is_buy_signal = current_price < lower_band

                    # Sell when price crosses above upper band (potential reversal)
                    is_sell_signal = current_price > upper_band

                    # Log band data and signals
                    logger.info(f"Current price: {current_price:.5f}")
                    logger.info(
                        f"Bollinger Bands - Middle: {middle_band:.5f}, Upper: {upper_band:.5f}, Lower: {lower_band:.5f}"
                    )

                    if is_buy_signal:
                        logger.info(f"Buy signal: Price ({current_price:.5f}) below lower band ({lower_band:.5f})")
                    elif is_sell_signal:
                        logger.info(f"Sell signal: Price ({current_price:.5f}) above upper band ({upper_band:.5f})")

                    # Execute trading positions based on signals
                    if trade.trading_time():  # Only trade during allowed hours
                        trade.open_position(
                            should_buy=is_buy_signal, should_sell=is_sell_signal, comment="Bollinger Bands Strategy"
                        )

                # Update trading statistics
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
