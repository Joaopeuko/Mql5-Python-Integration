import sys
import os
import time
import MetaTrader5 as mt5

def test_mt5_initialization():
    """Test MetaTrader5 initialization in various ways until one succeeds."""
    print(f'MT5 version: {mt5.__version__}')
    print('MT5_HEADLESS:', os.environ.get('MT5_HEADLESS'))
    print('MT5_PORTABLE_PATH:', os.environ.get('MT5_PORTABLE_PATH'))
    print('Initializing...')

    # Set environment variable directly in Python to ensure it's available
    os.environ['MT5_HEADLESS'] = '1'

    result = mt5.initialize()
    print(f'Initial result: {result}, Error code: {mt5.last_error()}')

    # If the initial attempt fails, try additional methods
    if not result:
        print('Initial attempt failed. Trying with standard path...')
        
        # Attempt 2: initialize with standard path
        result = mt5.initialize(
            path="C:\Program Files\MetaTrader 5\terminal64.exe",
            login=0,
            password="",
            server="",
            timeout=60000
        )

        print(f'Result with standard path: {result}, Error code: {mt5.last_error()}')

        # If first attempt fails, try alternative approach
        if not result:
            print('Second attempt failed. Trying with increased timeout...')
            mt5.shutdown()
            time.sleep(2)
            
            # Attempt 3: default init with longer timeout
            result = mt5.initialize(timeout=120000)
            print(f'Result with increased timeout: {result}, Error code: {mt5.last_error()}')
                
            if not result:
                print('All initialization attempts failed')
                return False

    # Check if initialization was successful
    if result:
        print('MT5 initialized successfully')
        
        # Try to get account info as test
        account_info = mt5.account_info()
        if account_info is not None:
            print(f'Account info: {account_info}')
        else:
            print('No account info available (demo mode)')
        
        # Try to get symbol info as test
        symbol_info = mt5.symbol_info('EURUSD')
        if symbol_info is not None:
            print(f'Symbol info available: {symbol_info.name}')
        else:
            print('Symbol info not available')
        
        # Clean shutdown
        mt5.shutdown()
        return True
    
    return False

if __name__ == "__main__":
    success = test_mt5_initialization()
    sys.exit(0 if success else 1)
