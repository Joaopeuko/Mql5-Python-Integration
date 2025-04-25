"""Utility module for MetaTrader 5 integration.

Provides helper functions and classes for trading operations.
"""

import logging
from datetime import datetime, timezone

import MetaTrader5 as Mt5

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with formatting
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Utilities:
    """A utility class for handling trading-related functionalities."""

    def __init__(self) -> None:
        """Initialize the Utilities class."""
        # Variables for minutes_counter
        self.__minutes_counter: int = 0
        self.__counter_flag: bool = True
        self.__allowed_to_trade: bool = True
        self.__allow_to_count: bool = False
        self.__recent_trade: bool = False

    def check_trade_availability(self, symbol: str, count_until: int) -> bool:
        """Check if trading is allowed based on specified conditions.

        Args:
            symbol (str): The financial instrument symbol.
            count_until (int): The number of minutes until trading is allowed.

        Returns:
            bool: True if trading is allowed, False otherwise.
        """
        if len(Mt5.positions_get(symbol=symbol)) == 1:
            self.__recent_trade = True

        if len(Mt5.positions_get(symbol=symbol)) != 1 and self.__recent_trade and not self.__allow_to_count:
            self.__allow_to_count = True
            self.__allowed_to_trade = False

        if datetime.now(timezone.utc).second == 0 and self.__counter_flag and self.__allow_to_count:
            logger.info(f"Trading will be allowed in {count_until - self.__minutes_counter} minutes.")
            self.__minutes_counter += 1
            self.__counter_flag = False

        if datetime.now(timezone.utc).second == 59:
            self.__counter_flag = True

        if self.__minutes_counter == count_until:
            logger.info("Trading is allowed.\n")
            self.__reset_counters()

        return self.__allowed_to_trade

    def __reset_counters(self) -> None:
        """Reset counters after trading is allowed."""
        self.__minutes_counter = 0
        self.__counter_flag = True
        self.__allow_to_count = False
        self.__allowed_to_trade = True
