from datetime import datetime

import MetaTrader5 as Mt5


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
        """
        Check if trading is allowed based on specified conditions.

        Args:
            symbol (str): The financial instrument symbol.
            count_until (int): The number of minutes until trading is allowed.

        Returns:
            bool: True if trading is allowed, False otherwise.
        """
        if len(Mt5.positions_get(symbol=symbol)) == 1:
            self.__recent_trade = True

        if len(Mt5.positions_get(symbol=symbol)) != 1 and self.__recent_trade:
            if not self.__allow_to_count:
                self.__allow_to_count = True
                self.__allowed_to_trade = False
                self.__recent_trade = False

        if datetime.now().second == 0 and self.__counter_flag and self.__allow_to_count:
            print(f"Trading will be allowed in {count_until - self.__minutes_counter} minutes.")
            self.__minutes_counter += 1
            self.__counter_flag = False

        if datetime.now().second == 59:
            self.__counter_flag = True

        if self.__minutes_counter == count_until:
            print("Trading is allowed.\n")
            self.__reset_counters()

        return self.__allowed_to_trade

    def __reset_counters(self) -> None:
        """Reset counters after trading is allowed."""
        self.__minutes_counter = 0
        self.__counter_flag = True
        self.__allow_to_count = False
        self.__allowed_to_trade = True
