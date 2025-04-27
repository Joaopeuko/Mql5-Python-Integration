"""Test fixtures and configuration shared across test modules."""

from __future__ import annotations

import logging
from typing import Generator

import pytest


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
