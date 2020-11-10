from typing import List, Union

import MetaTrader5 as Mt5


class Rates:
    """Represents historical rates data for a financial instrument."""

    def __init__(self, symbol: str, time_frame: int, start_pos: int, period: int) -> None:
        """
        Initializes a Rates object.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame of the rates data.
            start_pos (int): The starting position for data retrieval.
            period (int): The number of rates to retrieve.

        Returns:
            None
        """
        self._symbol = symbol
        try:
            rates_data = Mt5.copy_rates_from_pos(self._symbol, time_frame, start_pos, period)

            self._time = rates_data["time"]
            self._open = rates_data["open"]
            self._high = rates_data["high"]
            self._low = rates_data["low"]
            self._close = rates_data["close"]
            self._tick_volume = rates_data["tick_volume"]
            self._spread = rates_data["spread"]
            self._real_volume = rates_data["real_volume"]

            # Optionally, you can print statements here for debugging
            # print(f"Rates object created for symbol: {self._symbol}")
        except Exception as e:
            # Optionally, you can print statements here for debugging
            # print(f"Failed to create Rates object for symbol {self._symbol}. Error: {e}")
            raise

    @property
    def time(self) -> List[Union[int, float]]:
        """List of timestamps."""
        return self._time

    @property
    def open(self) -> List[float]:
        """List of open prices."""
        return self._open

    @property
    def high(self) -> List[float]:
        """List of high prices."""
        return self._high

    @property
    def low(self) -> List[float]:
        """List of low prices."""
        return self._low

    @property
    def close(self) -> List[float]:
        """List of close prices."""
        return self._close

    @property
    def tick_volume(self) -> List[int]:
        """List of tick volumes."""
        return self._tick_volume

    @property
    def spread(self) -> List[int]:
        """List of spreads."""
        return self._spread

    @property
    def real_volume(self) -> List[int]:
        """List of real volumes."""
        return self._real_volume
