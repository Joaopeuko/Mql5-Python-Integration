from typing import Any, Dict, Optional

import MetaTrader5 as Mt5


class Book:
    """Represents a market book for a financial instrument."""

    def __init__(self, symbol: str) -> None:
        """Initialize the Book object.

        Args:
            symbol (str): The financial instrument symbol.

        Returns:
            None
        """
        self.symbol: str = symbol
        if Mt5.market_book_add(self.symbol):
            print(f"The symbol {self.symbol} was successfully added to the market book.")
        else:
            print(f"Error adding {self.symbol} to the market book. Error: {Mt5.last_error()}")

    def get(self) -> Optional[Dict[str, Any]]:
        """Get the market book for the financial instrument.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the market book, or None if unsuccessful.
        """
        return Mt5.market_book_get(self.symbol)

    def release(self) -> bool:
        """Release the market book for the financial instrument.

        Returns:
            bool: True if successful, False otherwise.
        """
        return Mt5.market_book_release(self.symbol)
