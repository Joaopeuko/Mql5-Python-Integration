"""Module for retrieving and managing historical price data from MetaTrader 5.

Provides the Rates class for accessing historical price information.
"""

from __future__ import annotations

import MetaTrader5 as Mt5


class Rates:
    """Represents historical price data for a financial instrument."""

    def __init__(self, symbol: str, time_frame: int, start_position: int, count: int) -> None:
        """Initializes a Rates object.

        Args:
            symbol (str): The financial instrument symbol.
            time_frame (int): The time frame for the rates.
            start_position (int): The starting position for the rates.
            count (int): The number of rates to retrieve.

        Returns:
            None
        """

        def _raise_value_error(msg: str) -> None:
            raise ValueError(msg)

        try:
            rates = Mt5.copy_rates_from_pos(symbol, time_frame, start_position, count)
            if rates is None:
                _raise_value_error(f"Failed to retrieve rates for {symbol}")

            self._time = [rate[0] for rate in rates]
            self._open = [rate[1] for rate in rates]
            self._high = [rate[2] for rate in rates]
            self._low = [rate[3] for rate in rates]
            self._close = [rate[4] for rate in rates]
            self._tick_volume = [rate[5] for rate in rates]
            self._spread = [rate[6] for rate in rates]
            self._real_volume = [rate[7] for rate in rates]
        except Mt5.Error as e:
            raise ValueError(f"Failed to create Rates object for symbol {symbol}") from e

    @property
    def time(self) -> list[int | float]:
        """List of timestamps."""
        return self._time

    @property
    def open(self) -> list[float]:
        """List of open prices."""
        return self._open

    @property
    def high(self) -> list[float]:
        """List of high prices."""
        return self._high

    @property
    def low(self) -> list[float]:
        """List of low prices."""
        return self._low

    @property
    def close(self) -> list[float]:
        """List of close prices."""
        return self._close

    @property
    def tick_volume(self) -> list[int]:
        """List of tick volumes."""
        return self._tick_volume

    @property
    def spread(self) -> list[int]:
        """List of spreads."""
        return self._spread

    @property
    def real_volume(self) -> list[int]:
        """List of real volumes."""
        return self._real_volume
