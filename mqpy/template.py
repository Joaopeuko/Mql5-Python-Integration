"""Module for creating template files for MetaTrader 5 integration.

Provides functions for generating template files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import MetaTrader5 as Mt5


def get_arguments() -> dict[str, Any]:
    """Get the arguments for the template.

    Returns:
        dict[str, Any]: The arguments for the template.
    """
    return {
        "symbol": "EURUSD",
        "time_frame": Mt5.TIMEFRAME_M1,
        "start_position": 0,
        "count": 100,
    }


def create_template(file_name: str) -> None:
    """Create a template file for the expert advisor.

    Args:
        file_name (str): The name of the file to create.

    Returns:
        None
    """
    symbol = get_arguments()["symbol"]

    with Path(f"{file_name}.py").open("w") as file:
        file.write(
            f"""from mqpy.rates import Rates
from mqpy.tick import Tick
from mqpy.book import Book
from mqpy.trade import Trade
from mqpy.utilities import Utilities

def main():
    # Initialize the expert advisor
    expert = Trade(
        expert_name="{file_name}",
        version="1.0",
        symbol="{symbol}",
        magic_number=123456,
        lot=0.1,
        stop_loss=100,
        emergency_stop_loss=200,
        take_profit=100,
        emergency_take_profit=200,
    )

    # Initialize utilities
    utilities = Utilities()

    while True:
        # Get the current tick
        tick = Tick("{symbol}")

        # Get the current market book
        book = Book("{symbol}")

        # Get the current rates
        rates = Rates("{symbol}", Mt5.TIMEFRAME_M1, 0, 100)

        # Check if trading is allowed
        if utilities.check_trade_availability("{symbol}", 5):
            # Open a position
            expert.open_position(
                should_buy=True,
                should_sell=False,
                comment="Buy position opened by {file_name}",
            )

        # Close the market book
        book.release()

if __name__ == "__main__":
    main()
"""
        )
