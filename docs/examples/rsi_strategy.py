#!/usr/bin/env python3
"""RSI (Relative Strength Index) Strategy Example.

This example demonstrates an RSI-based trading strategy using the mqpy framework.
The strategy enters long positions when RSI is below the oversold threshold and
enters short positions when RSI is above the overbought threshold.
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


def calculate_rsi(prices: list[float], period: int = 14) -> float | None:
    """Calculate the Relative Strength Index.

    Args:
        prices: A list of closing prices
        period: The RSI period (default: 14)

    Returns:
        The RSI value (0-100) or None if insufficient data
    """
    if len(prices) < period + 1:
        return None

    # Calculate price changes
    deltas = np.diff(prices)

    # Separate gains and losses
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    # Calculate initial average gain and loss
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    # Avoid division by zero
    if avg_loss == 0:
        return 100

    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def main() -> None:
    """Main execution function for the RSI strategy."""
    # Initialize the trading strategy
    trade = Trade(
        expert_name="RSI Strategy",
        version="1.0",
        symbol="EURUSD",
        magic_number=568,
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

    logger.info(f"Starting RSI strategy on {trade.symbol}")

    # Strategy parameters
    prev_tick_time = 0
    rsi_period = 14
    overbought_threshold = 70
    oversold_threshold = 30

    try:
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch tick and rates data
            current_tick = Tick(trade.symbol)
            historical_rates = Rates(trade.symbol, rsi_period + 20, 0, 1)  # Get extra data for reliability

            # Only process if we have a new tick and enough data for RSI calculation
            if current_tick.time_msc != prev_tick_time and len(historical_rates.close) >= rsi_period + 1:
                # Calculate RSI
                rsi_value = calculate_rsi(historical_rates.close, rsi_period)

                if rsi_value is not None:
                    # Generate signals based on RSI thresholds
                    is_buy_signal = rsi_value < oversold_threshold
                    is_sell_signal = rsi_value > overbought_threshold

                    # Log RSI values and signals
                    if is_buy_signal:
                        logger.info(f"Oversold condition: RSI = {rsi_value:.2f} (< {oversold_threshold})")
                    elif is_sell_signal:
                        logger.info(f"Overbought condition: RSI = {rsi_value:.2f} (> {overbought_threshold})")
                    else:
                        logger.debug(f"Current RSI: {rsi_value:.2f}")

                    # Execute trading positions based on signals during allowed trading hours
                    if trade.trading_time():
                        trade.open_position(
                            should_buy=is_buy_signal,
                            should_sell=is_sell_signal,
                            comment=f"RSI Strategy: {rsi_value:.2f}",
                        )

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
