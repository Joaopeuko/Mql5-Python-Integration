"""Module for managing a market book for a financial instrument.

Provides the Book class for accessing market depth information.
"""

from __future__ import annotations

from typing import Any

import MetaTrader5 as Mt5

from mqpy.logger import get_logger

# Configure logging
logger = get_logger(__name__)


class Book:
    """Represents a market book for a financial instrument."""

    def __init__(self, symbol: str) -> None:
        """Initialize a Book object.

        Args:
            symbol (str): The financial instrument symbol.

        Returns:
            None
        """
        self.symbol: str = symbol
        if Mt5.market_book_add(self.symbol):
            logger.info(f"The symbol {self.symbol} was successfully added to the market book.")
        else:
            logger.error(f"Error adding {self.symbol} to the market book. Error: {Mt5.last_error()}")

    def get(self) -> list[Any] | None:
        """Get the market book for the financial instrument.

        Returns:
            list[Any] | None: The market book data if successful, None otherwise.
        """
        return Mt5.market_book_get(self.symbol)

    def release(self) -> bool:
        """Release the market book for the financial instrument.

        Returns:
            bool: True if successful, False otherwise.
        """
        result = Mt5.market_book_release(self.symbol)
        return False if result is None else result
