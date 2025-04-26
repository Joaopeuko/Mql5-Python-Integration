import sys
import os
import time
import MetaTrader5 as mt5

def test_mt5_initialization():
    """Test MetaTrader5 initialization in various ways until one succeeds."""
    print(f'MT5 version: {mt5.__version__}')
    
    # Start MetaTrader 5 process first before initialization
    import subprocess
    import time
    
    # Set environment variables
    os.environ['MT5_HEADLESS'] = '1'
    print('MT5_HEADLESS:', os.environ.get('MT5_HEADLESS'))
    print('MT5_PORTABLE_PATH:', os.environ.get('MT5_PORTABLE_PATH'))
    print('Initializing...')
    
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
        return False
    
    # First start the MetaTrader terminal process with specific parameters
    mt5_path = existing_paths[0]  # Use the first found path
    print(f"Starting MetaTrader 5 process from: {mt5_path}")
    
    try:
        # Kill any running MT5 processes first
        if sys.platform == 'win32':
            subprocess.call('taskkill /F /IM terminal64.exe', shell=True, stderr=subprocess.DEVNULL)
            time.sleep(3)
        
        # Start MT5 with the /portable parameter which helps in CI environments
        mt5_process = subprocess.Popen([mt5_path, '/portable'], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0)
        
        print(f"Started MetaTrader 5 process with PID: {mt5_process.pid}")
        # Wait for MT5 to start up
        time.sleep(15)
        
        # Now try connecting multiple times with different parameters
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            print(f"\nAttempt {attempt}/{max_attempts} to initialize MT5...")
            
            # Cleanup any previous connection
            if attempt > 1:
                try:
                    mt5.shutdown()
                except:
                    pass
                time.sleep(3)
            
            # Using longer timeouts and specifying path directly
            result = mt5.initialize(
                path=mt5_path,
                login=0,
                password="",
                server="",
                timeout=120000  # 2 minutes timeout
            )
            
            error_code = mt5.last_error()
            print(f'Initialization result: {result}, Error: {error_code}')
            
            if result:
                print('MT5 initialized successfully!')
                break
                
            # If we're getting timeout errors, wait longer between attempts
            if error_code[0] == -10005:  # IPC timeout
                print("IPC timeout encountered, waiting longer before next attempt...")
                time.sleep(10)
        
        if not result:
            print("All initialization attempts failed")
            return False
            
        # Successfully connected, try accessing some basic data
        print('MT5 initialized successfully')
        
        # Try to get terminal information as test
        terminal_info = mt5.terminal_info()
        if terminal_info is not None:
            print(f'Terminal info: {terminal_info._asdict()}')
        else:
            print('Terminal info not available')
        
        # Clean shutdown
        mt5.shutdown()
        return True
        
    except Exception as e:
        print(f"Error during MetaTrader 5 initialization: {e}")
        return False
    finally:
        # Make sure to terminate the MT5 process when done
        try:
            if 'mt5_process' in locals() and mt5_process:
                mt5_process.terminate()
                print("Terminated MetaTrader 5 process")
        except:
            pass

if __name__ == "__main__":
    success = test_mt5_initialization()
    sys.exit(0 if success else 1)
