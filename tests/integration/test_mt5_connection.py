"""Integration tests for MetaTrader 5 connection functionality."""

import sys
import os
import time
import MetaTrader5 as mt5


def test_mt5_connection() -> bool:
    """Test basic connection to MetaTrader 5 terminal.

    Returns:
        bool: True if the connection test was successful.
    """
    print(f"MetaTrader5 package version: {mt5.__version__}")

    # Define path to the MetaTrader terminal executable
    path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    print(f"MetaTrader5 path: {path}")

    # Try to initialize with explicit path parameter
    if not mt5.initialize(path=path):
        error = mt5.last_error()
        print(f"initialize() with path failed, error code = {error}")

        # Try the second method: initialize with just a delay 
        time.sleep(3)  # Give some time before retry
        print("Retrying initialization...")
        if not mt5.initialize():
            error = mt5.last_error()
            print(f"initialize() without path failed, error code = {error}")
            sys.exit(1)

    # Connection successful
    print("MetaTrader5 initialized successfully")

    # Get account info
    account_info = mt5.account_info()
    if account_info is not None:
        print(f"Account info: server={account_info.server}, balance={account_info.balance}")
    else:
        print("Failed to get account info - this is normal without login credentials")

    # Get terminal info
    terminal_info = mt5.terminal_info()
    if terminal_info is not None:
        print(f"Terminal info: connected={terminal_info.connected}, path={terminal_info.path}")
    else:
        print("Failed to get terminal info")

    # Shutdown the connection
    print("Shutting down MetaTrader5 connection...")
    mt5.shutdown()
    print("Done")

    print("Test completed successfully")
    return True


if __name__ == "__main__":
    test_mt5_connection()
