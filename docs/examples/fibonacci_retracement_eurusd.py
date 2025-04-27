#!/usr/bin/env python3
"""Fibonacci Retracement Trading Strategy Example.

This example demonstrates a Fibonacci retracement-based trading strategy
using the mqpy framework. The strategy identifies swing highs and lows,
calculates Fibonacci retracement levels, and generates trading signals
when price interacts with key retracement levels.

Strategy Logic:
--------------
1. Swing Point Detection:
   - Analyzes price action to identify significant swing highs and lows
   - Uses a configurable window parameter to determine the significance of swing points

2. Fibonacci Level Calculation:
   - Applies standard Fibonacci ratios (0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0)
   - Calculates retracement levels between the most recent significant swing points
   - Adapts to both uptrends (retracements from low to high) and downtrends (retracements from high to low)

3. Signal Generation:
   - Monitors price proximity to Fibonacci levels using a configurable tolerance
   - Generates buy signals when price touches key retracement levels during uptrends
   - Generates sell signals when price touches key retracement levels during downtrends
   - Focuses on the most reliable retracement levels (0.382, 0.5, 0.618)

4. Visualization:
   - Creates candlestick charts with marked swing points
   - Displays horizontal lines at each Fibonacci retracement level
   - Provides visual confirmation of the strategy logic

Trading Assumptions:
-------------------
- Markets tend to retrace by predictable percentages during trends
- Key Fibonacci levels often act as support/resistance
- The 38.2%, 50%, and 61.8% retracement levels are considered the most reliable for trading signals
- Proper risk management using stop-loss and take-profit levels is essential

This strategy should be further enhanced with additional filters (volume, other indicators)
for improved reliability in live trading environments.
"""

from __future__ import annotations

import logging

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick_ohlc

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Fibonacci retracement levels (standard)
FIBONACCI_LEVELS = [0.0, 0.236, 0.382, 0.5, 0.618, 0.786, 1.0]


def find_swing_points(prices: list[float], window: int = 5) -> tuple[list[int], list[int]]:
    """Find swing high and swing low points in price data.

    Args:
        prices: List of price values
        window: Window size for determining swing points

    Returns:
        Tuple containing lists of swing high and swing low indices
    """
    highs: list[int] = []
    lows: list[int] = []

    if len(prices) < 2 * window + 1:
        return highs, lows

    for i in range(window, len(prices) - window):
        # Check for swing high
        if all(prices[i] > prices[i - j] for j in range(1, window + 1)) and all(
            prices[i] > prices[i + j] for j in range(1, window + 1)
        ):
            highs.append(i)

        # Check for swing low
        if all(prices[i] < prices[i - j] for j in range(1, window + 1)) and all(
            prices[i] < prices[i + j] for j in range(1, window + 1)
        ):
            lows.append(i)

    return highs, lows


def calculate_fibonacci_levels(start_price: float, end_price: float) -> dict[float, float]:
    """Calculate Fibonacci retracement price levels.

    Args:
        start_price: Starting price for retracement (swing high/low)
        end_price: Ending price for retracement (swing low/high)

    Returns:
        Dictionary mapping Fibonacci ratios to price levels
    """
    diff = end_price - start_price
    levels = {}

    for ratio in FIBONACCI_LEVELS:
        levels[ratio] = start_price + diff * ratio

    return levels


def plot_fibonacci_levels(
    rates: Rates, swing_highs: list[int], swing_lows: list[int], retracement_levels: dict[float, float] | None = None
) -> None:
    """Plot price chart with swing points and Fibonacci retracement levels.

    Args:
        rates: Rate data containing OHLC prices and times
        swing_highs: Indices of swing high points
        swing_lows: Indices of swing low points
        retracement_levels: Dictionary of Fibonacci levels to plot
    """
    try:
        # Convert rates data to pandas DataFrame
        data = []
        for i in range(len(rates.time)):
            # Convert to matplotlib date format
            date = mdates.date2num(pd.to_datetime(rates.time[i], unit="s"))
            data.append([date, rates.open[i], rates.high[i], rates.low[i], rates.close[i]])

        price_data = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close"])

        # Create plot
        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot candlestick chart
        candlestick_ohlc(ax, price_data.values, width=0.001, colorup="green", colordown="red", alpha=0.8)

        # Format date axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
        plt.xticks(rotation=45)

        # Mark swing highs and lows
        for idx in swing_highs:
            ax.plot(mdates.date2num(pd.to_datetime(rates.time[idx], unit="s")), rates.high[idx], "ro", markersize=8)

        for idx in swing_lows:
            ax.plot(mdates.date2num(pd.to_datetime(rates.time[idx], unit="s")), rates.low[idx], "go", markersize=8)

        # Plot Fibonacci retracement levels if provided
        if retracement_levels:
            colors = ["b", "g", "r", "c", "m", "y", "k"]
            for i, (ratio, price) in enumerate(retracement_levels.items()):
                ax.axhline(
                    y=price, color=colors[i % len(colors)], linestyle="--", label=f"Fib {ratio:.3f}: {price:.5f}"
                )

        plt.title("EURUSD with Fibonacci Retracement Levels")
        plt.ylabel("Price")
        plt.legend()
        plt.tight_layout()

        # Save the chart
        plt.savefig("fibonacci_retracement.png")
        logger.info("Chart saved as 'fibonacci_retracement.png'")

        # Show the plot
        plt.show()

    except Exception:
        logger.exception("Error creating Fibonacci retracement chart")


def analyze_retracement_signals(
    current_price: float, fib_levels: dict[float, float], tolerance: float = 0.0001
) -> tuple[bool, bool, float | None]:
    """Analyze price position relative to Fibonacci levels and generate signals.

    Args:
        current_price: Current market price
        fib_levels: Dictionary of Fibonacci retracement levels
        tolerance: Price tolerance for level testing

    Returns:
        Tuple containing (buy_signal, sell_signal, level_tested)
    """
    buy_signal = False
    sell_signal = False
    level_tested = None

    # Determine trend direction from Fibonacci levels
    uptrend = fib_levels[0.0] < fib_levels[1.0]

    for ratio, level in fib_levels.items():
        # Check if price is near a Fibonacci level
        if abs(current_price - level) < tolerance:
            level_tested = ratio

            # In uptrend, bounces off retracement levels can be buy signals
            # Focus on the most reliable levels: 0.382, 0.5, 0.618
            if uptrend and ratio in [0.382, 0.5, 0.618]:
                buy_signal = True

            # In downtrend, bounces off retracement levels can be sell signals
            elif not uptrend and ratio in [0.382, 0.5, 0.618]:
                sell_signal = True

            break

    return buy_signal, sell_signal, level_tested


def main() -> None:
    """Main execution function for the Fibonacci retracement strategy."""
    # Initialize the trading strategy
    trade = Trade(
        expert_name="Fibonacci Retracement Strategy",
        version="1.0",
        symbol="EURUSD",
        magic_number=571,
        lot=0.1,
        stop_loss=35,
        emergency_stop_loss=100,
        take_profit=70,
        emergency_take_profit=200,
        start_time="9:15",
        finishing_time="17:30",
        ending_time="17:50",
        fee=0.5,
    )

    logger.info(f"Starting Fibonacci Retracement strategy on {trade.symbol}")

    # Strategy parameters
    prev_tick_time = 0
    lookback_period = 100  # Number of candles to analyze
    swing_window = 5  # Window for swing high/low detection
    price_tolerance = 0.0001  # Tolerance for testing price at Fibonacci levels

    # Variables to track state
    current_fib_levels = None
    last_swing_check_time = 0
    swing_recalculation_interval = 10 * 60  # Recalculate swings every 10 minutes

    try:
        while True:
            # Prepare the symbol for trading
            trade.prepare_symbol()

            # Fetch tick and rates data (H1 timeframe for identifying swings)
            current_tick = Tick(trade.symbol)
            historical_rates = Rates(trade.symbol, lookback_period, 0, 60)  # H1 timeframe

            current_time = current_tick.time

            # Only recalculate swing points and Fibonacci levels periodically
            if (current_time - last_swing_check_time) > swing_recalculation_interval:
                # Find swing highs and lows
                swing_highs, swing_lows = find_swing_points(historical_rates.close, window=swing_window)

                # Calculate Fibonacci levels if we have swing points
                if len(swing_highs) > 0 and len(swing_lows) > 0:
                    # Use the most recent swing high and swing low
                    recent_high_idx = swing_highs[-1]
                    recent_low_idx = swing_lows[-1]

                    # Determine which one is more recent
                    if recent_high_idx > recent_low_idx:
                        # Downtrend: from high to low
                        start_price = historical_rates.high[recent_high_idx]
                        end_price = historical_rates.low[recent_low_idx]
                        logger.info(f"Detected downtrend from {start_price:.5f} to {end_price:.5f}")
                    else:
                        # Uptrend: from low to high
                        start_price = historical_rates.low[recent_low_idx]
                        end_price = historical_rates.high[recent_high_idx]
                        logger.info(f"Detected uptrend from {start_price:.5f} to {end_price:.5f}")

                    # Calculate Fibonacci retracement levels
                    current_fib_levels = calculate_fibonacci_levels(start_price, end_price)

                    # Log Fibonacci levels
                    logger.info("Fibonacci retracement levels:")
                    for ratio, price in current_fib_levels.items():
                        logger.info(f"  {ratio:.3f}: {price:.5f}")

                    # Create and save Fibonacci retracement chart
                    plot_fibonacci_levels(historical_rates, swing_highs, swing_lows, current_fib_levels)

                    last_swing_check_time = current_time

            # Only process trading logic if we have new tick data and Fibonacci levels
            if current_tick.time_msc != prev_tick_time and current_fib_levels:
                # Current price
                current_price = current_tick.ask  # Use ask price for analysis

                # Analyze price relative to Fibonacci levels
                buy_signal, sell_signal, level_tested = analyze_retracement_signals(
                    current_price, current_fib_levels, tolerance=price_tolerance
                )

                # Log signals
                if level_tested is not None:
                    logger.info(f"Price {current_price:.5f} testing Fibonacci level {level_tested:.3f}")

                    if buy_signal:
                        logger.info(f"Buy signal generated at Fibonacci level {level_tested:.3f}")
                    elif sell_signal:
                        logger.info(f"Sell signal generated at Fibonacci level {level_tested:.3f}")

                # Execute trading based on signals
                if trade.trading_time():  # Only trade during allowed hours
                    trade.open_position(
                        should_buy=buy_signal,
                        should_sell=sell_signal,
                        comment=f"Fibonacci {level_tested:.3f} Strategy"
                        if level_tested is not None
                        else "Fibonacci Strategy",
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
