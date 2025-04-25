"""Test MetaTrader5 initialization in headless environments like GitHub CI."""

import os
import sys
import time
import subprocess
import MetaTrader5 as mt5

def setup_headless_environment() -> bool:
    """Prepare the environment for headless MT5 operation."""
    # Create required directories that might be expected by MT5
    base_path = os.path.expanduser("~")
    mt5_data_path = os.path.join(base_path, "AppData", "Roaming", "MetaQuotes", "Terminal")
    
    os.makedirs(mt5_data_path, exist_ok=True)
    print(f"Created MT5 data directory: {mt5_data_path}")
    
    # Set environment variables that might help with headless operation
    os.environ["MT5_HEADLESS"] = "1"
    return True

def test_headless_initialize():
    """Test MT5 initialization in a headless environment."""
    print(f"MetaTrader5 package version: {mt5.__version__}")
    
    # Setup headless environment
    setup_headless_environment()
    
    # Start MT5 terminal process with headless-friendly options
    mt_path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    if not os.path.exists(mt_path):
        print(f"ERROR: MetaTrader5 executable not found at {mt_path}")
        return False
    
    print(f"Found MetaTrader5 at: {mt_path}")
    
    # Kill any existing MT5 processes
    try:
        subprocess.run(["taskkill", "/F", "/IM", "terminal64.exe"], 
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Killed any existing MetaTrader 5 processes")
        time.sleep(2)
    except Exception as e:
        print(f"Note: No existing processes to kill: {e}")
    
    # Launch with multiple flags for headless operation
    try:
        print("Starting MetaTrader 5 terminal with headless-friendly options...")
        process = subprocess.Popen([
            mt_path, 
            "/portable",          # Use portable mode to avoid requiring login
            "/skipupdate",        # Skip checking for updates
            "/config:headless",    # Use a specific config name
            "/nogui"              # No GUI needed (might not be supported but worth trying)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"Started MetaTrader 5 with PID: {process.pid}")
        time.sleep(15)  # Give it time to initialize backend services
    except Exception as e:
        print(f"Error starting MetaTrader 5: {e}")
        return False
    
    # Try initialization methods in sequence
    print("\nAttempting MT5 initialization...")
    
    # Method 1: With path parameter and longer timeout
    print("Method 1: With explicit path and timeout")
    try:
        result = mt5.initialize(path=mt_path, timeout=60000)  # 60-second timeout
        error = mt5.last_error()
        print(f"Result: {result}, Error: {error}")
        if result:
            print("Method 1 SUCCESS!")
            terminal_info = mt5.terminal_info()
            if terminal_info:
                print(f"Terminal info - Path: {terminal_info.path}, Connected: {getattr(terminal_info, 'connected', 'N/A')}")
            mt5.shutdown()
            return True
    except Exception as e:
        print(f"Exception in method 1: {e}")
    
    # Method 2: With server parameter (try to avoid login)
    print("\nMethod 2: With server parameter")
    try:
        result = mt5.initialize(
            path=mt_path,
            server="Demo",  # Use demo server
            login=0,        # No login
            timeout=60000   # 60-second timeout
        )
        error = mt5.last_error()
        print(f"Result: {result}, Error: {error}")
        if result:
            print("Method 2 SUCCESS!")
            mt5.shutdown()
            return True
    except Exception as e:
        print(f"Exception in method 2: {e}")
        
    # Method 3: Basic initialization with longer wait after process start
    print("\nMethod 3: After additional delay")
    try:
        print("Waiting 30 more seconds for MT5 to fully initialize...")
        time.sleep(30)
        result = mt5.initialize()
        error = mt5.last_error()
        print(f"Result: {result}, Error: {error}")
        if result:
            print("Method 3 SUCCESS!")
            mt5.shutdown()
            return True
    except Exception as e:
        print(f"Exception in method 3: {e}")
    
    # If we got here, all methods failed
    print("\nAll initialization attempts failed in headless mode")
    return False

if __name__ == "__main__":
    success = test_headless_initialize()
    if success:
        print("\nHEADLESS TEST PASSED: Successfully initialized MT5")
        sys.exit(0)
    else:
        print("\nHEADLESS TEST FAILED: Could not initialize MT5")
        sys.exit(1)