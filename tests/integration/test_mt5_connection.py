import os
import sys
import MetaTrader5 as mt5

def test_mt5_connection():
    """Test basic connection to MetaTrader 5 terminal."""
    
    print(f"MetaTrader5 package version: {mt5.__version__}")
    
    # Initialize MetaTrader 5
    if not mt5.initialize():
        print(f"initialize() failed, error code = {mt5.last_error()}")
        sys.exit(1)
    
    print(mt5.terminal_info())
    print(f"MetaTrader5 terminal copyright: {mt5.terminal_info().copyright}")
    print(f"MetaTrader5 terminal name: {mt5.terminal_info().name}")
    print(f"MetaTrader5 terminal path: {mt5.terminal_info().path}")
    
    authorized = mt5.login()
    if authorized:
        print(f"Connected to account: {mt5.account_info().login}")
        print(f"Balance: {mt5.account_info().balance}")

    mt5.shutdown()
    
    print("Test completed successfully")
    return True

if __name__ == "__main__":
    test_mt5_connection()
