"""Tests for the Utilities class that provides helper functions for trading operations."""

from __future__ import annotations

import time
from typing import Generator

import MetaTrader5 as Mt5
import pytest

from mqpy.utilities import Utilities


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
def utilities() -> Utilities:
    """Provides a Utilities instance for testing."""
    return Utilities()


def test_utilities_initialization() -> None:
    """Test initialization of Utilities class."""
    utilities = Utilities()
    assert isinstance(utilities, Utilities)
    symbol = "EURUSD"
    assert utilities.check_trade_availability(symbol, 5) is True


def test_multiple_utilities_instances() -> None:
    """Test that multiple Utilities instances work independently."""
    utilities1 = Utilities()
    utilities2 = Utilities()
    assert utilities1.check_trade_availability("EURUSD", 5) is True
    assert utilities2.check_trade_availability("EURUSD", 5) is True
    assert utilities1 is not utilities2


def test_utilities_attributes(utilities: Utilities) -> None:
    """Test that the Utilities class has the expected attributes."""
    assert hasattr(utilities, "_test_get_minutes_counter")
    assert hasattr(utilities, "_test_get_counter_flag")
    assert hasattr(utilities, "_test_get_allowed_to_trade")
    assert hasattr(utilities, "_test_get_allow_to_count")
    assert hasattr(utilities, "_test_get_recent_trade")

    assert utilities._test_get_minutes_counter() == 0
    assert utilities._test_get_counter_flag() is True
    assert utilities._test_get_allowed_to_trade() is True
    assert utilities._test_get_allow_to_count() is False
    assert utilities._test_get_recent_trade() is False

    assert hasattr(utilities, "check_trade_availability")
    assert callable(utilities.check_trade_availability)


def test_reset_counters_functionality(utilities: Utilities) -> None:
    """Test the reset_counters functionality directly."""
    utilities._test_set_minutes_counter(5)
    utilities._test_set_counter_flag(False)
    utilities._test_set_allowed_to_trade(False)
    utilities._test_set_allow_to_count(True)

    utilities._test_reset_counters()

    assert utilities._test_get_minutes_counter() == 0
    assert utilities._test_get_counter_flag() is True
    assert utilities._test_get_allowed_to_trade() is True
    assert utilities._test_get_allow_to_count() is False
