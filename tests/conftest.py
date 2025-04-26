import pytest

@pytest.fixture
def test_symbols():
    """Provides common test symbols that can be used across tests."""
    return {
        "forex": "EURUSD",
        "indices": "US500",
        "commodities": "XAUUSD",
        "crypto": "BTCUSD",
        "invalid": "INVALID"
    }

@pytest.fixture
def configure_logging():
    """Sets up logging configuration for tests."""
    import logging
    
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