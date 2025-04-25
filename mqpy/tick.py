from typing import Optional

import MetaTrader5 as Mt5


class Tick:
    """Represents real-time tick data for a financial instrument."""

    def __init__(self, symbol: str) -> None:
        """Initializes a Tick object.

        Args:
            symbol (str): The financial instrument symbol.

        Returns:
            None
        """
        tick_info = Mt5.symbol_info_tick(symbol)

        self._symbol = symbol
        self._time = tick_info.time
        self._bid = tick_info.bid
        self._ask = tick_info.ask
        self._last = tick_info.last
        self._volume = tick_info.volume
        self._time_msc = tick_info.time_msc
        self._flags = tick_info.flags
        self._volume_real = tick_info.volume_real

    @property
    def symbol(self) -> str:
        """The financial instrument symbol."""
        return self._symbol

    @property
    def time(self) -> int:
        """Timestamp of the tick data."""
        return self._time

    @property
    def bid(self) -> float:
        """Current bid price."""
        return self._bid

    @property
    def ask(self) -> float:
        """Current ask price."""
        return self._ask

    @property
    def last(self) -> float:
        """Last traded price."""
        return self._last

    @property
    def volume(self) -> int:
        """Tick volume."""
        return self._volume

    @property
    def time_msc(self) -> int:
        """Timestamp in milliseconds."""
        return self._time_msc

    @property
    def flags(self) -> int:
        """Flags indicating tick data attributes."""
        return self._flags

    @property
    def volume_real(self) -> Optional[float]:
        """Real volume (if available)."""
        return self._volume_real
