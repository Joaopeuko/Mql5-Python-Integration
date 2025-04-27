"""Tests for the Book class that manages market depth information from MetaTrader 5."""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, Generator

import MetaTrader5 as Mt5
import pytest

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture

from mqpy.book import Book


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


def test_book_initialization(symbol: str, caplog: LogCaptureFixture) -> None:
    """Test initialization of Book with a real symbol."""
    caplog.set_level(logging.INFO)
    # Create book instance (used to trigger log message)
    Book(symbol)

    assert f"The symbol {symbol} was successfully added to the market book" in caplog.text


def test_book_get(symbol: str) -> None:
    """Test getting real market book data."""
    book = Book(symbol)

    time.sleep(1)

    market_data = book.get()

    assert market_data is not None

    if market_data:
        assert isinstance(market_data, list)

        # Loop separately to check for bids and asks
        has_bids = False
        has_asks = False

        for item in market_data:
            if item.type == Mt5.BOOK_TYPE_SELL:
                has_bids = True
            if item.type == Mt5.BOOK_TYPE_BUY:
                has_asks = True

        if not (has_bids or has_asks):
            logging.warning(f"No bids or asks found in market book for {symbol}")

    book.release()


def test_book_release(symbol: str) -> None:
    """Test releasing the market book."""
    book = Book(symbol)

    result = book.release()

    assert result is True


def test_full_workflow(symbol: str) -> None:
    """Test a complete workflow with the real market book."""
    book = Book(symbol)

    time.sleep(1)

    market_data = book.get()

    assert market_data is not None

    release_result = book.release()
    assert release_result is True

    time.sleep(1)
    data_after_release = book.get()

    if data_after_release is not None and len(data_after_release) > 0:
        logging.info("Market book data still available after release")


def test_multiple_symbols() -> None:
    """Test using Book with multiple symbols simultaneously."""
    symbols = Mt5.symbols_get()
    if len(symbols) < 2:
        pytest.skip("Need at least 2 symbols for this test")

    symbol1 = symbols[0].name
    symbol2 = symbols[1].name

    book1 = Book(symbol1)
    book2 = Book(symbol2)

    time.sleep(1)

    data1 = book1.get()
    data2 = book2.get()

    assert data1 is not None
    assert data2 is not None

    book1.release()
    book2.release()


def test_unavailable_symbol(caplog: LogCaptureFixture) -> None:
    """Test behavior with an unavailable symbol."""
    caplog.set_level(logging.ERROR)

    invalid_symbol = "INVALID_SYMBOL_THAT_DOESNT_EXIST"

    book = Book(invalid_symbol)

    assert "Error adding INVALID_SYMBOL_THAT_DOESNT_EXIST to the market book" in caplog.text

    release_result = book.release()
    assert release_result is False
