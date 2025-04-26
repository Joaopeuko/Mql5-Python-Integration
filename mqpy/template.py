"""Module for generating MT5 expert advisor template files.

Provides functionality to create template files for trading strategies.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any


def get_arguments() -> dict[str, Any]:
    """Parse command line arguments.

    Returns:
        dict[str, Any]: Dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", type=str, action="store", default="demo")
    parser.add_argument("--symbol", type=str, action="store", default="EURUSD")
    return vars(parser.parse_args())


def main() -> None:
    """Generate a template file for a trading strategy."""
    file_name = get_arguments()["file_name"]
    symbol = get_arguments()["symbol"]

    with Path(f"{file_name}.py").open("w") as file:
        file.write(
            f"""from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="Moving Average Crossover",
    version="1.0",
    symbol="{symbol}",
    magic_number=567,
    lot=1.0,
    stop_loss=25,
    emergency_stop_loss=300,
    take_profit=25,
    emergency_take_profit=300,
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Main trading loop
prev_tick_time = 0
short_window_size = 5
long_window_size = 20  # Adjust the window size as needed

while True:
    # Fetch tick and rates data
    current_tick = Tick(trade.symbol)
    historical_rates = Rates(trade.symbol, long_window_size, 0, 1)

    # Check for new tick
    if current_tick.time_msc != prev_tick_time:
        # Calculate moving averages
        short_ma = sum(historical_rates.close[-short_window_size:]) / short_window_size
        long_ma = sum(historical_rates.close[-long_window_size:]) / long_window_size

        # Generate signals based on moving average crossover
        is_cross_above = short_ma > long_ma and current_tick.last > short_ma
        is_cross_below = short_ma < long_ma and current_tick.last < short_ma

        # Execute trading positions based on signals
        trade.open_position(is_cross_above, is_cross_below, "Moving Average Crossover Strategy")

    prev_tick_time = current_tick.time_msc

    # Check if it's the end of the trading day
    if trade.days_end():
        trade.close_position("End of the trading day reached.")
        break

print("Finishing the program.")
print("Program finished.")
"""
        )


if __name__ == "__main__":
    main()
