"""Tests for the Trade class that manages trading operations with MetaTrader 5."""

from __future__ import annotations

import contextlib
import logging
import os
import time
from pathlib import Path
from typing import Generator

import MetaTrader5 as Mt5
import pytest

from mqpy.trade import Trade

logger = logging.getLogger(__name__)

# Constants for test values
TEST_LOT_SIZE = 0.01
TEST_STOP_LOSS = 50.0
TEST_EMERGENCY_STOP_LOSS = 100.0
TEST_TAKE_PROFIT = 100.0
TEST_EMERGENCY_TAKE_PROFIT = 200.0
TEST_MAGIC_NUMBER = 12345
TEST_FEE = 1.5


def is_headless() -> bool:
    """Check if running in headless mode."""
    return os.environ.get("HEADLESS_MODE", "false").lower() == "true"


@pytest.fixture(scope="module", autouse=True)
def setup_teardown() -> Generator[None, None, None]:  # noqa: C901 - Test setup needs to handle many cases
    """Set up and tear down MetaTrader5 connection for the test module."""
    if is_headless():
        logger.info("Running in headless mode - skipping MT5 initialization")
        yield
        return

    init_result = Mt5.initialize()

    if not init_result:
        common_paths = [
            "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
            "C:\\Program Files (x86)\\MetaTrader 5\\terminal.exe",
        ]

        for path in common_paths:
            if Path(path).exists():
                init_result = Mt5.initialize(path=path)
                if init_result:
                    logger.info(f"Successfully initialized MT5 with path: {path}")
                    break

    if not init_result:
        pytest.skip(f"MetaTrader5 could not be initialized. Error: {Mt5.last_error()}")

    time.sleep(5)

    symbols = Mt5.symbols_get()
    if not symbols:
        logger.warning("No symbols loaded. Attempting to fix...")
        Mt5.symbols_total()  # Sometimes this helps refresh the symbols list
        time.sleep(3)

        symbols = Mt5.symbols_get()
        if not symbols:
            logger.error("Still no symbols available after retry.")

    yield

    try:
        positions = Mt5.positions_get()
        if positions:
            for position in positions:
                if position.symbol == "EURUSD":
                    if position.type == 0:  # Buy position
                        Mt5.order_send(
                            {
                                "action": Mt5.TRADE_ACTION_DEAL,
                                "symbol": "EURUSD",
                                "volume": position.volume,
                                "type": Mt5.ORDER_TYPE_SELL,
                                "position": position.ticket,
                                "price": Mt5.symbol_info_tick("EURUSD").bid,
                                "deviation": 20,
                                "magic": 12345,
                                "comment": "Close test position",
                                "type_time": Mt5.ORDER_TIME_GTC,
                                "type_filling": Mt5.ORDER_FILLING_FOK,
                            }
                        )
                    else:  # Sell position
                        Mt5.order_send(
                            {
                                "action": Mt5.TRADE_ACTION_DEAL,
                                "symbol": "EURUSD",
                                "volume": position.volume,
                                "type": Mt5.ORDER_TYPE_BUY,
                                "position": position.ticket,
                                "price": Mt5.symbol_info_tick("EURUSD").ask,
                                "deviation": 20,
                                "magic": 12345,
                                "comment": "Close test position",
                                "type_time": Mt5.ORDER_TIME_GTC,
                                "type_filling": Mt5.ORDER_FILLING_FOK,
                            }
                        )
    except Exception:
        logger.exception("Error cleaning up positions")

    Mt5.shutdown()


@pytest.fixture
def symbol() -> str:
    """Provides a valid trading symbol for testing."""
    time.sleep(1)

    symbols = Mt5.symbols_get()
    if not symbols:
        logger.warning("No symbols returned from MT5, defaulting to EURUSD")
        return "EURUSD"

    for symbol in symbols:
        if symbol.name == "EURUSD":
            return "EURUSD"

    logger.warning("EURUSD not found, defaulting to first available symbol")
    return symbols[0].name


@pytest.fixture(autouse=True)
def cleanup_positions(symbol: str) -> None:
    """Close any open positions after each test."""
    yield
    # Clean up after the test
    Mt5.initialize()
    positions = Mt5.positions_get(symbol=symbol)
    if positions and len(positions) > 0:
        try:
            for position in positions:
                if position.symbol == symbol:
                    # Close the position
                    request = {
                        "action": Mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": position.volume,
                        "type": Mt5.ORDER_TYPE_BUY if position.type == 1 else Mt5.ORDER_TYPE_SELL,
                        "position": position.ticket,
                        "price": Mt5.symbol_info_tick(symbol).ask
                        if position.type == 1
                        else Mt5.symbol_info_tick(symbol).bid,
                        "deviation": 20,
                        "magic": 12345,
                        "comment": "Close position",
                        "type_time": Mt5.ORDER_TIME_GTC,
                        "type_filling": Mt5.ORDER_FILLING_RETURN,
                    }
                    Mt5.order_send(request)
        except Exception:
            logger.exception("Error cleaning up positions")

    Mt5.shutdown()


@pytest.fixture
def trade(symbol: str) -> Trade:
    """Create a Trade instance for testing."""
    trade = Trade(
        expert_name="TestExpert",
        version="1.0",
        symbol=symbol,
        magic_number=TEST_MAGIC_NUMBER,
        lot=TEST_LOT_SIZE,
        stop_loss=TEST_STOP_LOSS,
        emergency_stop_loss=TEST_EMERGENCY_STOP_LOSS,
        take_profit=TEST_TAKE_PROFIT,
        emergency_take_profit=TEST_EMERGENCY_TAKE_PROFIT,
    )

    positions = Mt5.positions_get(symbol=symbol)
    if positions:
        for position in positions:
            if position.magic == TEST_MAGIC_NUMBER:
                trade.close_position("Cleaning up for tests")

    return trade


def test_trade_initialization(symbol: str) -> None:
    """Test the initialization of the Trade class."""
    trade = Trade(
        expert_name="TestExpert",
        version="1.0",
        symbol=symbol,
        magic_number=TEST_MAGIC_NUMBER,
        lot=TEST_LOT_SIZE,
        stop_loss=TEST_STOP_LOSS,
        emergency_stop_loss=TEST_EMERGENCY_STOP_LOSS,
        take_profit=TEST_TAKE_PROFIT,
        emergency_take_profit=TEST_EMERGENCY_TAKE_PROFIT,
    )

    assert trade.expert_name == "TestExpert"
    assert trade.version == "1.0"
    assert trade.symbol == symbol
    assert trade.magic_number == TEST_MAGIC_NUMBER
    assert trade.lot == TEST_LOT_SIZE
    assert trade.stop_loss == TEST_STOP_LOSS
    assert trade.emergency_stop_loss == TEST_EMERGENCY_STOP_LOSS
    assert trade.take_profit == TEST_TAKE_PROFIT
    assert trade.emergency_take_profit == TEST_EMERGENCY_TAKE_PROFIT

    assert trade.start_time_hour == "9"
    assert trade.start_time_minutes == "15"
    assert trade.finishing_time_hour == "17"
    assert trade.finishing_time_minutes == "30"
    assert trade.ending_time_hour == "17"
    assert trade.ending_time_minutes == "50"
    assert trade.fee == 0.0

    assert trade.loss_deals == 0
    assert trade.profit_deals == 0
    assert trade.total_deals == 0
    assert trade.balance == 0.0
    assert trade.ticket == 0

    assert Mt5.symbol_info(symbol) is not None


def test_trade_with_custom_times(symbol: str) -> None:
    """Test the initialization of the Trade class with custom times."""
    trade = Trade(
        expert_name="TestExpert",
        version="1.0",
        symbol=symbol,
        magic_number=TEST_MAGIC_NUMBER,
        lot=TEST_LOT_SIZE,
        stop_loss=TEST_STOP_LOSS,
        emergency_stop_loss=TEST_EMERGENCY_STOP_LOSS,
        take_profit=TEST_TAKE_PROFIT,
        emergency_take_profit=TEST_EMERGENCY_TAKE_PROFIT,
        start_time="10:30",
        finishing_time="16:45",
        ending_time="17:00",
        fee=TEST_FEE,
    )

    assert trade.start_time_hour == "10"
    assert trade.start_time_minutes == "30"
    assert trade.finishing_time_hour == "16"
    assert trade.finishing_time_minutes == "45"
    assert trade.ending_time_hour == "17"
    assert trade.ending_time_minutes == "00"
    assert trade.fee == TEST_FEE


def test_symbol_selection(trade: Trade) -> None:
    """Test that a symbol can be selected."""
    with contextlib.suppress(Exception):
        Mt5.symbol_select(trade.symbol, False)

    trade.select_symbol()

    symbol_info = Mt5.symbol_info(trade.symbol)
    assert symbol_info is not None
    assert symbol_info.visible is True


def test_prepare_symbol(trade: Trade) -> None:
    """Test preparing a symbol for trading."""
    trade.prepare_symbol()

    symbol_info = Mt5.symbol_info(trade.symbol)
    assert symbol_info is not None
    assert symbol_info.visible is True


def test_trading_time_calculation() -> None:
    """Test the trading time calculation logic."""
    trade = Trade(
        expert_name="TestExpert",
        version="1.0",
        symbol="EURUSD",
        magic_number=TEST_MAGIC_NUMBER,
        lot=TEST_LOT_SIZE,
        stop_loss=TEST_STOP_LOSS,
        emergency_stop_loss=TEST_EMERGENCY_STOP_LOSS,
        take_profit=TEST_TAKE_PROFIT,
        emergency_take_profit=TEST_EMERGENCY_TAKE_PROFIT,
        start_time="0:00",
        finishing_time="23:59",
    )

    result = trade.trading_time()
    assert isinstance(result, bool)


def test_days_end_calculation() -> None:
    """Test the days_end calculation logic."""
    trade = Trade(
        expert_name="TestExpert",
        version="1.0",
        symbol="EURUSD",
        magic_number=TEST_MAGIC_NUMBER,
        lot=TEST_LOT_SIZE,
        stop_loss=TEST_STOP_LOSS,
        emergency_stop_loss=TEST_EMERGENCY_STOP_LOSS,
        take_profit=TEST_TAKE_PROFIT,
        emergency_take_profit=TEST_EMERGENCY_TAKE_PROFIT,
        ending_time="23:59",
    )

    result = trade.days_end()
    assert isinstance(result, bool)


def test_statistics_with_zero_deals(trade: Trade) -> None:
    """Test the statistics method with zero deals."""
    trade.statistics()


def test_statistics_with_deals(trade: Trade) -> None:
    """Test the statistics method with some deals."""
    trade.profit_deals = 3
    trade.loss_deals = 2
    trade.total_deals = 5
    trade.balance = 150.0

    trade.statistics()


def _check_position(magic_number: int, expected_type: int) -> bool:
    """Helper to check if a position of the expected type exists.

    Args:
        magic_number: The magic number to filter positions by
        expected_type: The expected position type (Buy or Sell)

    Returns:
        True if a position of the expected type exists, False otherwise
    """
    positions = Mt5.positions_get()
    if not positions:
        return False

    return any(position.magic == magic_number and position.type == expected_type for position in positions)


@pytest.mark.real_trading
def test_open_position_with_conditions(trade: Trade) -> None:
    """Test the open_position method with buy/sell conditions."""
    # Cleanup any existing positions
    positions = Mt5.positions_get(symbol=trade.symbol)
    if positions:
        for position in positions:
            if position.magic == TEST_MAGIC_NUMBER:
                trade.close_position("Cleaning up for test")

    # Configure trade time settings for 24/7 trading
    trade.start_time_hour = "0"
    trade.start_time_minutes = "00"
    trade.finishing_time_hour = "23"
    trade.finishing_time_minutes = "59"

    # Test buy condition
    trade.open_position(should_buy=True, should_sell=False, comment="Test Buy Condition")
    time.sleep(2)

    assert _check_position(TEST_MAGIC_NUMBER, Mt5.ORDER_TYPE_BUY)
    trade.close_position("Cleaning up after Buy test")
    time.sleep(2)

    # Test sell condition
    trade.open_position(should_buy=False, should_sell=True, comment="Test Sell Condition")
    time.sleep(2)

    assert _check_position(TEST_MAGIC_NUMBER, Mt5.ORDER_TYPE_SELL)
    trade.close_position("Cleaning up after Sell test")
    time.sleep(2)


@pytest.mark.real_trading
def test_open_buy_position(trade: Trade) -> None:
    """Test opening a Buy position with real trades."""
    positions = Mt5.positions_get(symbol=trade.symbol)
    initial_positions_count = len(positions) if positions else 0

    trade.open_buy_position("Test Buy Position")

    time.sleep(2)

    positions = Mt5.positions_get(symbol=trade.symbol)
    if positions is not None:
        assert len(positions) >= initial_positions_count

        latest_position = None
        for position in positions:
            if position.magic == TEST_MAGIC_NUMBER:
                latest_position = position
                break

        if latest_position is not None:
            assert latest_position.type == Mt5.ORDER_TYPE_BUY


@pytest.mark.real_trading
def test_open_sell_position(trade: Trade) -> None:
    """Test opening a Sell position with real trades."""
    positions = Mt5.positions_get(symbol=trade.symbol)
    if positions:
        for position in positions:
            if position.magic == TEST_MAGIC_NUMBER:
                trade.close_position("Cleaning up for test_open_sell_position")

    trade.open_sell_position("Test Sell Position")

    time.sleep(2)

    positions = Mt5.positions_get(symbol=trade.symbol)
    assert positions is not None

    has_sell_position = False
    for position in positions:
        if position.magic == TEST_MAGIC_NUMBER and position.type == Mt5.ORDER_TYPE_SELL:
            has_sell_position = True
            break

    assert has_sell_position


@pytest.mark.real_trading
def test_close_position(trade: Trade) -> None:  # noqa: C901 - Test needs to handle many edge cases
    """Test closing a position with real trades."""
    # First, ensure we can get symbol info
    symbol_info = Mt5.symbol_info(trade.symbol)
    if not symbol_info:
        pytest.skip(f"Could not get symbol info for {trade.symbol}")

    logger.info(f"Symbol {trade.symbol} trade mode: {symbol_info.trade_mode}")

    # Check if we have any existing positions to close
    positions = Mt5.positions_get(symbol=trade.symbol)
    has_existing_position = False
    if positions:
        for position in positions:
            if position.magic == TEST_MAGIC_NUMBER:
                has_existing_position = True
                logger.info(f"Found existing position with ticket {position.ticket}")
                break

    if not has_existing_position:
        # Try to open a new position
        try:
            logger.info(f"Attempting to open a new position for {trade.symbol}")
            trade.open_buy_position("Test Position to Close")
            time.sleep(2)  # Wait for position to open

            # Verify position was opened
            positions = Mt5.positions_get(symbol=trade.symbol)
            assert positions is not None, "Failed to get positions after opening"

            has_position = False
            for position in positions:
                if position.magic == TEST_MAGIC_NUMBER:
                    has_position = True
                    logger.info(f"Successfully opened position with ticket {position.ticket}")
                    break

            assert has_position, "Failed to find opened position"

        except Exception:
            logger.exception("Error opening position")
            raise

    # Now try to close the position
    try:
        logger.info("Attempting to close position")
        trade.close_position("Test Closing Position")
        time.sleep(2)  # Wait for position to close

        # Verify position was closed
        positions = Mt5.positions_get(symbol=trade.symbol)
        has_position = False
        if positions:
            for position in positions:
                if position.magic == TEST_MAGIC_NUMBER:
                    has_position = True
                    logger.warning(f"Position still exists with ticket {position.ticket}")
                    break

        assert not has_position, "Position was not closed successfully"
        logger.info("Position closed successfully")

    except Exception:
        logger.exception("Error during position test")
        raise


@pytest.fixture(autouse=True)
def skip_real_trading_in_headless(request: pytest.FixtureRequest) -> None:
    """Skip real trading tests in headless mode."""
    if is_headless() and request.node.get_closest_marker("real_trading"):
        pytest.skip("Skipping real trading test in headless mode")
