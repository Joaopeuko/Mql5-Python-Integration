"""Module for generating MT5 expert advisor template files.

Provides functionality to create template files for trading strategies.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Callable

from mqpy.logger import get_logger

# Configure logging
logger = get_logger(__name__)


def get_arguments() -> dict[str, Any]:
    """Parse command line arguments.

    Returns:
        dict[str, Any]: Dictionary containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate MetaTrader 5 expert advisor templates using the mqpy framework.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--file_name", type=str, default="demo", help="Name of the output Python file (without .py extension)"
    )

    parser.add_argument("--symbol", type=str, default="EURUSD", help="Trading symbol to use in the template")

    parser.add_argument(
        "--strategy",
        type=str,
        choices=["moving_average", "rsi", "macd", "bollinger"],
        default="moving_average",
        help="Trading strategy template to generate",
    )

    parser.add_argument("--magic_number", type=int, default=567, help="Magic number for the trading strategy")

    parser.add_argument("--lot", type=float, default=1.0, help="Lot size for trading")

    parser.add_argument("--stop_loss", type=float, default=25.0, help="Stop loss in points")

    parser.add_argument("--take_profit", type=float, default=25.0, help="Take profit in points")

    parser.add_argument("--directory", type=str, default=".", help="Directory to save the generated file")

    return vars(parser.parse_args())


def generate_moving_average_template(args: dict[str, Any]) -> str:
    """Generate a moving average crossover strategy template.

    Args:
        args: Dictionary with template parameters

    Returns:
        str: The template code as a string
    """
    return f"""#!/usr/bin/env python3
'''
Moving Average Crossover Strategy for MetaTrader 5
Generated with mqpy template generator

This strategy trades based on crossovers between short and long moving averages.
'''

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="Moving Average Crossover",
    version="1.0",
    symbol="{args['symbol']}",
    magic_number={args['magic_number']},
    lot={args['lot']},
    stop_loss={args['stop_loss']},
    emergency_stop_loss={args['stop_loss'] * 12},
    take_profit={args['take_profit']},
    emergency_take_profit={args['take_profit'] * 12},
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Strategy parameters
prev_tick_time = 0
short_window_size = 5
long_window_size = 20  # Adjust the window size as needed

def main():
    '''Main execution function'''
    global prev_tick_time

    print(f"Starting Moving Average Crossover strategy on {{trade.symbol}}")

    while True:
        # Prepare the symbol for trading
        trade.prepare_symbol()

        # Fetch tick and rates data
        current_tick = Tick(trade.symbol)
        historical_rates = Rates(trade.symbol, long_window_size, 0, 1)

        # Trading logic - only execute on new tick
        if current_tick.time_msc != prev_tick_time:
            # Calculate moving averages
            if len(historical_rates.close) >= long_window_size:
                short_ma = sum(historical_rates.close[-short_window_size:]) / short_window_size
                long_ma = sum(historical_rates.close[-long_window_size:]) / long_window_size

                # Generate signals based on moving average crossover
                is_cross_above = short_ma > long_ma and current_tick.last > short_ma
                is_cross_below = short_ma < long_ma and current_tick.last < short_ma

                # Execute trading positions based on signals
                if trade.trading_time():  # Only trade during trading hours
                    trade.open_position(is_cross_above, is_cross_below, "Moving Average Crossover")

            # Update statistics periodically
            trade.statistics()

        prev_tick_time = current_tick.time_msc

        # Check if it's the end of the trading day
        if trade.days_end():
            trade.close_position("End of the trading day reached.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nStrategy execution interrupted by user.")
    except Exception as e:
        print(f"Error in strategy execution: {{e}}")
    finally:
        print("Finishing the program.")
"""


def generate_rsi_template(args: dict[str, Any]) -> str:
    """Generate an RSI strategy template.

    Args:
        args: Dictionary with template parameters

    Returns:
        str: The template code as a string
    """
    return f"""#!/usr/bin/env python3
'''
RSI (Relative Strength Index) Strategy for MetaTrader 5
Generated with mqpy template generator

This strategy trades based on overbought and oversold conditions using RSI.
'''

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="RSI Strategy",
    version="1.0",
    symbol="{args['symbol']}",
    magic_number={args['magic_number']},
    lot={args['lot']},
    stop_loss={args['stop_loss']},
    emergency_stop_loss={args['stop_loss'] * 12},
    take_profit={args['take_profit']},
    emergency_take_profit={args['take_profit'] * 12},
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Strategy parameters
prev_tick_time = 0
rsi_period = 14
oversold_threshold = 30
overbought_threshold = 70

def calculate_rsi(prices, period=14):
    '''Calculate the Relative Strength Index'''
    if len(prices) < period + 1:
        return 50  # Default to neutral when not enough data

    # Calculate price changes
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]

    # Separate gains and losses
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]

    # Calculate initial average gain and loss
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    # Use smoothed averages for the rest of the data
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    # Calculate RS and RSI
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def main():
    '''Main execution function'''
    global prev_tick_time

    print(f"Starting RSI strategy on {{trade.symbol}}")

    while True:
        # Prepare the symbol for trading
        trade.prepare_symbol()

        # Fetch tick and rates data
        current_tick = Tick(trade.symbol)
        historical_rates = Rates(trade.symbol, rsi_period + 10, 0, 1)

        # Trading logic - only execute on new tick
        if current_tick.time_msc != prev_tick_time:
            # Calculate RSI
            if len(historical_rates.close) > rsi_period + 1:
                rsi_value = calculate_rsi(historical_rates.close, rsi_period)

                # Generate signals based on RSI
                is_buy_signal = rsi_value < oversold_threshold  # Buy when oversold
                is_sell_signal = rsi_value > overbought_threshold  # Sell when overbought

                # Execute trading positions based on signals
                if trade.trading_time():  # Only trade during trading hours
                    trade.open_position(is_buy_signal, is_sell_signal, f"RSI Strategy: {{rsi_value:.2f}}")

            # Update statistics periodically
            trade.statistics()

        prev_tick_time = current_tick.time_msc

        # Check if it's the end of the trading day
        if trade.days_end():
            trade.close_position("End of the trading day reached.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nStrategy execution interrupted by user.")
    except Exception as e:
        print(f"Error in strategy execution: {{e}}")
    finally:
        print("Finishing the program.")
"""


def generate_macd_template(args: dict[str, Any]) -> str:
    """Generate a MACD strategy template.

    Args:
        args: Dictionary with template parameters

    Returns:
        str: The template code as a string
    """
    return f"""#!/usr/bin/env python3
'''
MACD (Moving Average Convergence Divergence) Strategy for MetaTrader 5
Generated with mqpy template generator

This strategy trades based on MACD crossovers and signal line.
'''

from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="MACD Strategy",
    version="1.0",
    symbol="{args['symbol']}",
    magic_number={args['magic_number']},
    lot={args['lot']},
    stop_loss={args['stop_loss']},
    emergency_stop_loss={args['stop_loss'] * 12},
    take_profit={args['take_profit']},
    emergency_take_profit={args['take_profit'] * 12},
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Strategy parameters
prev_tick_time = 0
fast_period = 12
slow_period = 26
signal_period = 9

def calculate_ema(prices, period):
    '''Calculate the Exponential Moving Average'''
    if len(prices) < period:
        return sum(prices) / len(prices)

    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period

    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema

    return ema

def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    '''Calculate MACD, Signal line, and Histogram'''
    if len(prices) < slow_period:
        return 0, 0, 0

    # Calculate EMA values
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)

    # MACD line
    macd_line = fast_ema - slow_ema

    # Signal line (EMA of MACD)
    # For simplicity, we're approximating the signal line here
    signal_line = (macd_line + sum(prices[-signal_period:]) / signal_period) / 2

    # MACD histogram
    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram

def main():
    '''Main execution function'''
    global prev_tick_time

    print(f"Starting MACD strategy on {{trade.symbol}}")

    while True:
        # Prepare the symbol for trading
        trade.prepare_symbol()

        # Fetch tick and rates data
        current_tick = Tick(trade.symbol)
        historical_rates = Rates(trade.symbol, slow_period + signal_period + 10, 0, 1)

        # Trading logic - only execute on new tick
        if current_tick.time_msc != prev_tick_time:
            # Calculate MACD
            if len(historical_rates.close) > slow_period + signal_period:
                macd_line, signal_line, histogram = calculate_macd(
                    historical_rates.close, fast_period, slow_period, signal_period
                )

                # Generate signals based on MACD
                is_buy_signal = macd_line > signal_line and histogram > 0
                is_sell_signal = macd_line < signal_line and histogram < 0

                # Execute trading positions based on signals
                if trade.trading_time():  # Only trade during trading hours
                    trade.open_position(is_buy_signal, is_sell_signal, "MACD Crossover")

            # Update statistics periodically
            trade.statistics()

        prev_tick_time = current_tick.time_msc

        # Check if it's the end of the trading day
        if trade.days_end():
            trade.close_position("End of the trading day reached.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nStrategy execution interrupted by user.")
    except Exception as e:
        print(f"Error in strategy execution: {{e}}")
    finally:
        print("Finishing the program.")
"""


def generate_bollinger_template(args: dict[str, Any]) -> str:
    """Generate a Bollinger Bands strategy template.

    Args:
        args: Dictionary with template parameters

    Returns:
        str: The template code as a string
    """
    return f"""#!/usr/bin/env python3
'''
Bollinger Bands Strategy for MetaTrader 5
Generated with mqpy template generator

This strategy trades based on price movements outside Bollinger Bands.
'''

from math import sqrt
from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.trade import Trade

# Initialize the trading strategy
trade = Trade(
    expert_name="Bollinger Bands Strategy",
    version="1.0",
    symbol="{args['symbol']}",
    magic_number={args['magic_number']},
    lot={args['lot']},
    stop_loss={args['stop_loss']},
    emergency_stop_loss={args['stop_loss'] * 12},
    take_profit={args['take_profit']},
    emergency_take_profit={args['take_profit'] * 12},
    start_time="9:15",
    finishing_time="17:30",
    ending_time="17:50",
    fee=0.5,
)

# Strategy parameters
prev_tick_time = 0
bb_period = 20
std_dev_multiplier = 2.0

def calculate_bollinger_bands(prices, period=20, multiplier=2):
    '''Calculate Bollinger Bands (middle, upper, lower)'''
    if len(prices) < period:
        return prices[-1], prices[-1], prices[-1]

    # Calculate SMA (middle band)
    sma = sum(prices[-period:]) / period

    # Calculate standard deviation
    squared_diff = [(price - sma) ** 2 for price in prices[-period:]]
    std_dev = sqrt(sum(squared_diff) / period)

    # Calculate upper and lower bands
    upper_band = sma + (multiplier * std_dev)
    lower_band = sma - (multiplier * std_dev)

    return sma, upper_band, lower_band

def main():
    '''Main execution function'''
    global prev_tick_time

    print(f"Starting Bollinger Bands strategy on {{trade.symbol}}")

    while True:
        # Prepare the symbol for trading
        trade.prepare_symbol()

        # Fetch tick and rates data
        current_tick = Tick(trade.symbol)
        historical_rates = Rates(trade.symbol, bb_period + 10, 0, 1)

        # Trading logic - only execute on new tick
        if current_tick.time_msc != prev_tick_time:
            # Calculate Bollinger Bands
            if len(historical_rates.close) >= bb_period:
                middle_band, upper_band, lower_band = calculate_bollinger_bands(
                    historical_rates.close, bb_period, std_dev_multiplier
                )

                # Generate signals based on Bollinger Bands
                current_price = current_tick.last
                is_buy_signal = current_price < lower_band  # Buy when price crosses below lower band
                is_sell_signal = current_price > upper_band  # Sell when price crosses above upper band

                # Execute trading positions based on signals
                if trade.trading_time():  # Only trade during trading hours
                    trade.open_position(is_buy_signal, is_sell_signal, "Bollinger Bands Signal")

            # Update statistics periodically
            trade.statistics()

        prev_tick_time = current_tick.time_msc

        # Check if it's the end of the trading day
        if trade.days_end():
            trade.close_position("End of the trading day reached.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nStrategy execution interrupted by user.")
    except Exception as e:
        print(f"Error in strategy execution: {{e}}")
    finally:
        print("Finishing the program.")
"""


def main() -> None:
    """Generate a template file for a trading strategy based on user arguments."""
    args = get_arguments()

    # Create directory if it doesn't exist
    output_dir = Path(args["directory"])
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # Select the appropriate template generator based on strategy
    template_generators: dict[str, Callable[[dict[str, Any]], str]] = {
        "moving_average": generate_moving_average_template,
        "rsi": generate_rsi_template,
        "macd": generate_macd_template,
        "bollinger": generate_bollinger_template,
    }

    generator = template_generators.get(args["strategy"], generate_moving_average_template)
    template_content = generator(args)

    # Generate the file
    output_file = output_dir / f"{args['file_name']}.py"
    with output_file.open("w", encoding="utf-8") as file:
        file.write(template_content)

    logger.info(f"Strategy template generated: {output_file.absolute()}")
    logger.info(f"Strategy type: {args['strategy']}")
    logger.info(f"Trading symbol: {args['symbol']}")


if __name__ == "__main__":
    main()
