"""Test fixtures and configuration shared across test modules."""

from __future__ import annotations

import ctypes
import logging
import time
from typing import TYPE_CHECKING, Generator

import pytest

if TYPE_CHECKING:
    from mqpy.trade import Trade

VK_CONTROL = 0x11
VK_E = 0x45

logger = logging.getLogger(__name__)


def send_ctrl_e() -> None:
    """Send CTRL+E to MetaTrader 5 to enable Expert Advisors."""
    user32 = ctypes.windll.user32
    # Press CTRL
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    # Press E
    user32.keybd_event(VK_E, 0, 0, 0)
    # Release E
    user32.keybd_event(VK_E, 0, 2, 0)
    # Release CTRL
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(1)


@pytest.fixture
def test_symbols() -> dict[str, str]:
    """Provides common test symbols that can be used across tests."""
    return {"forex": "EURUSD", "indices": "US500", "commodities": "XAUUSD", "crypto": "BTCUSD", "invalid": "INVALID"}


@pytest.fixture
def configure_logging() -> Generator[None, None, None]:
    """Sets up logging configuration for tests."""
    root = logging.getLogger()
    for handler in root.handlers[:]:
        root.removeHandler(handler)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    root.addHandler(handler)

    root.setLevel(logging.INFO)

    yield

    for handler in root.handlers[:]:
        root.removeHandler(handler)


@pytest.fixture
def enable_autotrade(trade: Trade) -> Trade:
    """Enables autotrade for testing purposes."""
    send_ctrl_e()

    trade.start_time_hour = "0"
    trade.start_time_minutes = "00"
    trade.finishing_time_hour = "23"
    trade.finishing_time_minutes = "59"

    return trade
