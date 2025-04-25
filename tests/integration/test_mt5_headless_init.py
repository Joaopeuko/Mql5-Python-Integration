"""MetaTrader5 headless initialization test with advanced configurations."""

import os
import sys
import time
import shutil
import subprocess
import MetaTrader5 as mt5

def prepare_mt5_environment():
    """Prepare necessary files and environment for headless MT5 operation."""
    print(f"MetaTrader5 package version: {mt5.__version__}")
    
    # Constants
    mt5_install_dir = "C:\\Program Files\\MetaTrader 5"
    mt5_exe = os.path.join(mt5_install_dir, "terminal64.exe")
    
    if not os.path.exists(mt5_exe):
        print(f"ERROR: MetaTrader5 not found at {mt5_exe}")
        return False
        
    # Create data directories that MT5 expects
    user_dir = os.path.expanduser("~")
    mt5_data_dir = os.path.join(user_dir, "AppData", "Roaming", "MetaQuotes", "Terminal", "Headless")
    mt5_config_dir = os.path.join(mt5_data_dir, "config")
    
    # Create directories
    os.makedirs(mt5_config_dir, exist_ok=True)
    print(f"Created MT5 config directory: {mt5_config_dir}")
    
    # Create minimal config files needed
    with open(os.path.join(mt5_config_dir, "startup.ini"), "w") as f:
        f.write("""[Common]
Login=0
EnableNews=0
EnablePush=0
AutoUpdate=0
DisableOpenGL=1
""")
    
    print("Created minimal startup.ini configuration file")
    
    # Copy potential config files from installation directory if they exist
    install_config = os.path.join(mt5_install_dir, "Config")
    if os.path.exists(install_config):
        for file in ["servers.dat", "groups.ini"]:
            src = os.path.join(install_config, file)
            dst = os.path.join(mt5_config_dir, file)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"Copied {file} to config directory")
    
    return mt5_data_dir

def test_mt5_initialization():
    """Test MetaTrader5 initialization with special headless handling."""
    
    # Set up environment
    config_dir = prepare_mt5_environment()
    if not config_dir:
        return False
    
    # Kill any existing MT5 processes
    try:
        subprocess.run(["taskkill", "/F", "/IM", "terminal64.exe"], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Killed any existing MetaTrader 5 processes")
        time.sleep(5)
    except Exception:
        pass  # Ignore if no processes found
    
    # Start MT5 with the prepared config directory
    mt_path = "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    
    try:
        cmd = [
            mt_path,
            f"/config:{os.path.basename(config_dir)}",  # Use our headless config
            "/portable",          # Portable mode to avoid login
            "/skipupdate",        # Skip updates
            "/autoclose"          # Allow auto-closing (may help with headless operation)
        ]
        print(f"Starting MT5 with command: {' '.join(cmd)}")
        
        process = subprocess.Popen(cmd, 
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        print(f"Started MetaTrader 5 with PID: {process.pid}")
    except Exception as e:
        print(f"Error starting MetaTrader 5: {e}")
        return False
    
    # Give extra time for initialization in CI
    print("Waiting for MT5 process to initialize (30 seconds)...")
    time.sleep(30)
    
    # Verify if process is still running
    try:
        if process.poll() is not None:
            print(f"WARNING: MetaTrader 5 process exited prematurely with code {process.poll()}")
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout.decode('utf-8', errors='ignore')}")
            print(f"STDERR: {stderr.decode('utf-8', errors='ignore')}")
    except Exception:
        pass
    
    # Try various initialization approaches
    print("\nAttempting MT5 initialization with various methods...")
    
    # Define all methods to try (path with increasing timeouts)
    methods = [
        {"name": "Default config path", "params": {"path": mt_path, "timeout": 30000}},
        {"name": "With longer timeout", "params": {"path": mt_path, "timeout": 60000}},
        {"name": "With login=0", "params": {"path": mt_path, "login": 0, "timeout": 30000}},
        {"name": "With config path", "params": {"path": mt_path, "config": config_dir, "timeout": 30000}}
    ]
    
    # Try each method in sequence
    for method in methods:
        print(f"\nTrying method: {method['name']}")
        try:
            # Ensure we're not already initialized
            mt5.shutdown()
            time.sleep(2)
            
            # Try initialization with this method's params
            result = mt5.initialize(**method['params'])
            error = mt5.last_error()
            print(f"Result: {result}, Error: {error}")
            
            if result:
                print(f"SUCCESS with method: {method['name']}")
                
                # Print terminal info
                try:
                    terminal_info = mt5.terminal_info()
                    if terminal_info:
                        print(f"Terminal path: {terminal_info.path}")
                        print(f"Connection: {getattr(terminal_info, 'connected', 'N/A')}")
                        print(f"Community: {getattr(terminal_info, 'community_account', 'N/A')}")
                except Exception as e:
                    print(f"Error getting terminal info: {e}")
                
                mt5.shutdown()
                return True
        except Exception as e:
            print(f"Exception: {e}")
    
    # If we get here, all methods failed
    print("\nAll initialization methods failed")
    return False

if __name__ == "__main__":
    success = test_mt5_initialization()
    print(f"\nTest {'PASSED' if success else 'FAILED'}: MetaTrader5 initialization")
    sys.exit(0 if success else 1)