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
    
    # Find MetaTrader 5 installation paths
    possible_paths = [
        r"C:\Program Files\MetaTrader 5\terminal64.exe",
        r"C:/Program Files/MetaTrader 5/terminal64.exe",
        r"C:\Program Files (x86)\MetaTrader 5\terminal64.exe",
        os.path.join(os.environ.get('APPDATA', ''), 'MetaTrader 5', 'terminal64.exe'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'MetaTrader 5', 'terminal64.exe'),
    ]
    
    # Add portable path if available
    portable_path = os.environ.get('MT5_PORTABLE_PATH')
    if portable_path:
        possible_paths.insert(0, os.path.join(portable_path, 'terminal64.exe'))
    
    # Check which paths exist
    existing_paths = []
    for path in possible_paths:
        if os.path.exists(path):
            existing_paths.append(path)
            print(f"Found MetaTrader 5 at: {path}")
    
    if not existing_paths:
        print("WARNING: No MetaTrader 5 installation found in common locations!")
        
    # Attempt 1: Initialize with minimal parameters
    result = mt5.initialize()
    print(f'Initial result: {result}, Error code: {mt5.last_error()}')

    # Try each found path if initial attempt fails
    if not result and existing_paths:
        for idx, path in enumerate(existing_paths, 1):
            print(f'Attempt {idx+1}: Trying with path: {path}')
            
            # Ensure previous attempt is cleaned up
            if idx > 1:
                mt5.shutdown()
                time.sleep(2)
                
            # Try with this path
            result = mt5.initialize(
                path=path,
                login=0,
                password="",
                server="",
                timeout=60000
            )
            
            print(f'Result with path {path}: {result}, Error code: {mt5.last_error()}')
            
            if result:
                print(f'Successfully initialized with path: {path}')
                break
        
        # If all path attempts fail, try with increased timeout
        if not result:
            print('All path attempts failed. Trying with increased timeout...')
            mt5.shutdown()
            time.sleep(2)
            
            # Final attempt: default init with longer timeout
            result = mt5.initialize(timeout=120000)
            print(f'Result with increased timeout: {result}, Error code: {mt5.last_error()}')

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
