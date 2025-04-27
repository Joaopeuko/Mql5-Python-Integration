"""Tests for the Rates class that retrieves historical price data from MetaTrader 5."""

from __future__ import annotations

import logging
import time
from typing import Generator

import MetaTrader5 as Mt5
import pytest

from mqpy.rates import Rates


@pytest.fixture(scope="module", autouse=True)
def setup_teardown() -> Generator[None, None, None]:
    """Set up and tear down MetaTrader5 connection for the test module."""
    if not Mt5.initialize():
        pytest.skip("MetaTrader5 could not be initialized")

    time.sleep(5)

    yield

    Mt5.shutdown()


@pytest.fixture
def symbol() -> str:
    """Provides a valid trading symbol for testing."""
    time.sleep(1)

    symbols = Mt5.symbols_get()
    if not symbols:
        pytest.skip("No symbols available for testing")

    for symbol in symbols:
        if symbol.name == "EURUSD":
            return "EURUSD"

    return symbols[0].name


@pytest.fixture
def timeframe() -> int:
    """Provides a valid timeframe for testing."""
    return Mt5.TIMEFRAME_H1


def test_rates_initialization(symbol: str, timeframe: int) -> None:
    """Test initialization of Rates with a real symbol."""
    rates = Rates(symbol, timeframe, 0, 10)

    assert len(rates.time) == 10
    assert len(rates.open) == 10
    assert len(rates.high) == 10
    assert len(rates.low) == 10
    assert len(rates.close) == 10
    assert len(rates.tick_volume) == 10
    assert len(rates.spread) == 10
    assert len(rates.real_volume) == 10


def test_rates_data_types(symbol: str, timeframe: int) -> None:
    """Test data types of all Rates properties."""
    rates = Rates(symbol, timeframe, 0, 5)

    assert rates.time[0] is not None
    assert isinstance(rates.open[0], float)
    assert isinstance(rates.high[0], float)
    assert isinstance(rates.low[0], float)
    assert isinstance(rates.close[0], float)

    assert rates.tick_volume[0] >= 0
    assert rates.spread[0] >= 0
    assert rates.real_volume[0] >= 0

    logging.info(f"Type of tick_volume: {type(rates.tick_volume[0])}")
    logging.info(f"Type of spread: {type(rates.spread[0])}")
    logging.info(f"Type of real_volume: {type(rates.real_volume[0])}")


def test_rates_data_relationships(symbol: str, timeframe: int) -> None:
    """Test relationships between rate data points."""
    rates = Rates(symbol, timeframe, 0, 10)

    for i in range(len(rates.high)):
        assert rates.high[i] >= rates.open[i]
        assert rates.high[i] >= rates.close[i]
        assert rates.high[i] >= rates.low[i]

        assert rates.low[i] <= rates.open[i]
        assert rates.low[i] <= rates.close[i]
        assert rates.low[i] <= rates.high[i]

        assert rates.spread[i] >= 0
        assert rates.tick_volume[i] >= 0
        assert rates.real_volume[i] >= 0


def test_different_timeframes(symbol: str) -> None:
    """Test retrieving rates with different timeframes."""
    timeframes = [Mt5.TIMEFRAME_M1, Mt5.TIMEFRAME_M5, Mt5.TIMEFRAME_H1, Mt5.TIMEFRAME_D1]

    for tf in timeframes:
        rates = Rates(symbol, tf, 0, 5)

        assert len(rates.time) == 5
        assert len(rates.open) == 5
        assert len(rates.close) == 5

        logging.info(f"Successfully retrieved rates for {symbol} with timeframe {tf}")


def test_different_counts(symbol: str, timeframe: int) -> None:
    """Test retrieving different number of rates."""
    counts = [1, 10, 50]

    for count in counts:
        rates = Rates(symbol, timeframe, 0, count)

        assert len(rates.time) == count
        assert len(rates.open) == count
        assert len(rates.close) == count

        logging.info(f"Successfully retrieved {count} rates for {symbol}")


def test_different_start_positions(symbol: str, timeframe: int) -> None:
    """Test retrieving rates from different start positions."""
    start_positions = [0, 10, 50]

    for pos in start_positions:
        rates = Rates(symbol, timeframe, pos, 5)

        assert len(rates.time) == 5
        assert len(rates.open) == 5
        assert len(rates.close) == 5

        logging.info(f"Successfully retrieved rates for {symbol} from position {pos}")


def test_invalid_symbol() -> None:
    """Test behavior with an invalid symbol."""
    invalid_symbol = "INVALID_SYMBOL_THAT_DOESNT_EXIST"

    with pytest.raises(ValueError, match="Failed to create Rates object"):
        Rates(invalid_symbol, Mt5.TIMEFRAME_H1, 0, 10)


def test_invalid_parameters(symbol: str) -> None:
    """Test behavior with invalid parameter values."""
    with pytest.raises(ValueError, match="Failed to create Rates object"):
        Rates(symbol, Mt5.TIMEFRAME_H1, 0, -1)

    with pytest.raises(ValueError, match="Failed to create Rates object"):
        Rates(symbol, 9999, 0, 10)
