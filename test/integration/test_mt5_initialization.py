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

    # Try initialization using portable path and headless mode
    portable_path = os.environ.get('MT5_PORTABLE_PATH')
    if portable_path:
        mt5_path = os.path.join(portable_path, 'terminal64.exe')
    else:
        mt5_path = None

    print('Starting MT5 initialization...')

    # Set environment variable directly in Python to ensure it's available
    os.environ['MT5_HEADLESS'] = '1'

    result = mt5.initialize()
    print(f'Initial result: {result}, Error code: {mt5.last_error()}')

    # If the initial attempt fails, try additional methods
    if not result and mt5_path:
        print('Initial attempt failed. Trying with portable path...')
        result = mt5.initialize(
            path=mt5_path,
            login=0,
            password='',
            server='',
            timeout=60000
        )

        print(f'Result with portable path: {result}, Error code: {mt5.last_error()}')

        # If first attempt fails, try alternative approach
        if not result:
            print('First attempt failed. Trying default initialization...')
            mt5.shutdown()
            time.sleep(2)
            
            # Attempt 2: default init with timeout
            result = mt5.initialize(timeout=60000)
            print(f'Result with default init: {result}, Error code: {mt5.last_error()}')
            
            # Attempt 3: standard path
            if not result:
                print('Second attempt failed. Trying with standard path...')
                mt5.shutdown()
                time.sleep(2)
                result = mt5.initialize(
                    path='C:\\Program Files\\MetaTrader 5\\terminal64.exe',
                    timeout=60000
                )
                print(f'Result with standard path: {result}, Error code: {mt5.last_error()}')
                
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
    print('Running MT5 initialization test...')
    result = mt5.initialize()
    print(f'Initial result: {result}, Error code: {mt5.last_error()}')
    success = test_mt5_initialization()
    sys.exit(0 if success else 1)
