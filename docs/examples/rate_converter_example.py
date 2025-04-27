#!/usr/bin/env python3
"""Rate Converter Example.

This example demonstrates how to use the MQPy rate converter to convert between different
timeframes in MetaTrader 5, which is essential for multi-timeframe analysis strategies.
"""

import logging

import matplotlib.pyplot as plt
import MetaTrader5 as Mt5
import numpy as np
import pandas as pd

from mqpy.rate_converter import RateConverter
from mqpy.rates import Rates

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def print_rates_info(rates: Rates, timeframe_name: str) -> None:
    """Print information about the rates data.

    Args:
        rates: The rates data object
        timeframe_name: Name of the timeframe for display
    """
    logger.info(f"{timeframe_name} Timeframe Data:")
    logger.info(f"  Number of candles: {len(rates.time)}")

    if len(rates.time) > 0:
        # Convert first timestamp to readable format
        first_time = pd.to_datetime(rates.time[0], unit="s")
        last_time = pd.to_datetime(rates.time[-1], unit="s")

        logger.info(f"  Time range: {first_time} to {last_time}")
        logger.info(
            f"  First candle: Open={rates.open[0]}, High={rates.high[0]}, Low={rates.low[0]}, Close={rates.close[0]}"
        )
        logger.info(
            f"  Last candle: Open={rates.open[-1]}, High={rates.high[-1]}, Low={rates.low[-1]}, Close={rates.close[-1]}"
        )


def plot_multi_timeframe_data(m1_rates: Rates, m5_rates: Rates, h1_rates: Rates) -> None:
    """Create a simple visualization of multi-timeframe data.

    Args:
        m1_rates: 1-minute timeframe rates
        m5_rates: 5-minute timeframe rates
        h1_rates: 1-hour timeframe rates
    """
    try:
        # Create figure with 3 subplots
        fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=False)

        # Convert timestamps to datetime for better x-axis labels
        m1_times = pd.to_datetime(m1_rates.time, unit="s")
        m5_times = pd.to_datetime(m5_rates.time, unit="s")
        h1_times = pd.to_datetime(h1_rates.time, unit="s")

        # Plot M1 data
        axes[0].plot(m1_times, m1_rates.close)
        axes[0].set_title("1-Minute Timeframe")
        axes[0].set_ylabel("Price")
        axes[0].grid(visible=True)

        # Plot M5 data
        axes[1].plot(m5_times, m5_rates.close)
        axes[1].set_title("5-Minute Timeframe")
        axes[1].set_ylabel("Price")
        axes[1].grid(visible=True)

        # Plot H1 data
        axes[2].plot(h1_times, h1_rates.close)
        axes[2].set_title("1-Hour Timeframe")
        axes[2].set_ylabel("Price")
        axes[2].set_xlabel("Time")
        axes[2].grid(visible=True)

        # Adjust layout
        plt.tight_layout()

        # Save the plot
        plt.savefig("multi_timeframe_analysis.png")
        logger.info("Saved visualization to 'multi_timeframe_analysis.png'")

        # Show the plot if in interactive mode
        plt.show()

    except Exception:
        logger.exception("Error creating visualization")


def main() -> None:
    """Main execution function for the Rate Converter example."""
    # Define the symbol to analyze
    symbol = "EURUSD"
    logger.info(f"Starting Rate Converter example for {symbol}")

    # Step 1: Get 1-minute timeframe data (100 candles)
    m1_rates = Rates(symbol, 100, 0, Mt5.TIMEFRAME_M1)
    print_rates_info(m1_rates, "M1")

    # Step 2: Use RateConverter to convert M1 to M5 timeframe
    logger.info("Converting M1 to M5 timeframe...")
    rate_converter = RateConverter()

    # Convert M1 data to M5 timeframe
    m5_rates = rate_converter.convert_rates(rates=m1_rates, new_timeframe=Mt5.TIMEFRAME_M5, price_type="close")
    print_rates_info(m5_rates, "M5 (converted from M1)")

    # Step 3: Use RateConverter to convert M1 to H1 timeframe
    logger.info("Converting M1 to H1 timeframe...")
    h1_rates = rate_converter.convert_rates(rates=m1_rates, new_timeframe=Mt5.TIMEFRAME_H1, price_type="close")
    print_rates_info(h1_rates, "H1 (converted from M1)")

    # Step 4: Demonstrate a simple multi-timeframe analysis
    logger.info("Performing multi-timeframe analysis...")

    # Calculate simple moving averages for different timeframes
    # For M1 data, calculate a 20-period SMA
    m1_sma = np.mean(m1_rates.close[-20:]) if len(m1_rates.close) >= 20 else None

    # For M5 data, calculate a 10-period SMA
    m5_sma = np.mean(m5_rates.close[-10:]) if len(m5_rates.close) >= 10 else None

    # For H1 data, calculate a 5-period SMA
    h1_sma = np.mean(h1_rates.close[-5:]) if len(h1_rates.close) >= 5 else None

    logger.info("Moving Average Results:")
    logger.info(f"  M1 20-period SMA: {m1_sma:.5f}" if m1_sma is not None else "  M1 SMA: Not enough data")
    logger.info(f"  M5 10-period SMA: {m5_sma:.5f}" if m5_sma is not None else "  M5 SMA: Not enough data")
    logger.info(f"  H1 5-period SMA: {h1_sma:.5f}" if h1_sma is not None else "  H1 SMA: Not enough data")

    # Step 5: Create a simple visualization
    logger.info("Creating visualization of multi-timeframe data...")
    plot_multi_timeframe_data(m1_rates, m5_rates, h1_rates)

    logger.info("Rate Converter example completed")


if __name__ == "__main__":
    main()
