"""Tests for the Tick class that retrieves real-time tick data from MetaTrader 5."""

from __future__ import annotations

import logging
import time
from typing import Generator

import MetaTrader5 as Mt5
import pytest

from mqpy.tick import Tick


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


def test_tick_initialization(symbol: str) -> None:
    """Test initialization of Tick with a real symbol."""
    tick = Tick(symbol)

    assert tick.symbol == symbol

    assert isinstance(tick.time, int)
    assert isinstance(tick.bid, float)
    assert isinstance(tick.ask, float)
    assert tick.ask >= 0
    assert tick.bid >= 0
    assert tick.ask >= tick.bid


def test_tick_properties(symbol: str) -> None:
    """Test all Tick properties with a real symbol."""
    tick = Tick(symbol)

    assert isinstance(tick.symbol, str)
    assert isinstance(tick.time, int)
    assert isinstance(tick.bid, float)
    assert isinstance(tick.ask, float)
    assert isinstance(tick.time_msc, int)
    assert isinstance(tick.flags, int)

    # Check last property
    if tick.last is not None:
        assert isinstance(tick.last, float)

    # Check volume property
    if tick.volume is not None:
        assert isinstance(tick.volume, int)

    if tick.volume_real is not None:
        assert isinstance(tick.volume_real, float)


def test_updated_tick_data(symbol: str) -> None:
    """Test getting updated tick data after waiting."""
    first_tick = Tick(symbol)
    first_time = first_tick.time

    time.sleep(2)

    second_tick = Tick(symbol)
    second_time = second_tick.time

    if first_time == second_time:
        # Log instead of print
        logging.info(f"No tick update for {symbol} after 2 seconds")


def test_multiple_symbols() -> None:
    """Test Tick with multiple symbols simultaneously."""
    symbols = Mt5.symbols_get()
    if len(symbols) < 2:
        pytest.skip("Need at least 2 symbols for this test")

    symbol1 = symbols[0].name
    symbol2 = symbols[1].name

    tick1 = Tick(symbol1)
    tick2 = Tick(symbol2)

    assert tick1.symbol == symbol1
    assert tick2.symbol == symbol2

    assert isinstance(tick1.bid, float)
    assert isinstance(tick1.ask, float)
    assert isinstance(tick2.bid, float)
    assert isinstance(tick2.ask, float)


def test_invalid_symbol() -> None:
    """Test behavior with an invalid symbol."""
    invalid_symbol = "INVALID_SYMBOL_THAT_DOESNT_EXIST"

    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'time'"):
        Tick(invalid_symbol)


def test_spread_calculation(symbol: str) -> None:
    """Test spread calculation from bid/ask values."""
    tick = Tick(symbol)

    spread = tick.ask - tick.bid

    assert spread >= 0

    logging.info(f"Spread for {symbol}: {spread}")
