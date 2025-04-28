#!/usr/bin/env python3
"""Script to setup and configure MetaTrader 5 for automated trading."""

import os
import sys
import time
from pathlib import Path
import logging

try:
    import MetaTrader5 as Mt5
except ImportError:
    print("MetaTrader5 package not installed. Install it with: pip install MetaTrader5")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def find_mt5_terminal():
    """Find MetaTrader 5 terminal executable."""
    common_paths = [
        "C:\\Program Files\\MetaTrader 5\\terminal64.exe",
        "C:\\Program Files (x86)\\MetaTrader 5\\terminal.exe",
        os.path.expandvars("%APPDATA%\\MetaTrader 5\\terminal64.exe"),
        os.path.expandvars("%PROGRAMFILES%\\MetaTrader 5\\terminal64.exe"),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None

def check_trading_allowed():
    """Check if trading is allowed and print current settings."""
    terminal_info = Mt5.terminal_info()
    logger.info("Current MetaTrader 5 settings:")
    logger.info(f"Connected: {terminal_info.connected}")
    logger.info(f"Trade allowed: {terminal_info.trade_allowed}")
    logger.info(f"DLLs allowed: {terminal_info.dlls_allowed}")
    
    return terminal_info.trade_allowed and terminal_info.dlls_allowed

def main():
    """Main function to setup MetaTrader 5."""
    logger.info("Looking for MetaTrader 5 terminal...")
    terminal_path = find_mt5_terminal()
    
    if not terminal_path:
        logger.error("Could not find MetaTrader 5 terminal. Please install it first.")
        sys.exit(1)
    
    logger.info(f"Found MetaTrader 5 terminal at: {terminal_path}")
    
    # Try to initialize MT5
    if not Mt5.initialize(path=terminal_path):
        logger.error(f"MetaTrader 5 initialization failed. Error code: {Mt5.last_error()}")
        sys.exit(1)
    
    try:
        if check_trading_allowed():
            logger.info("Trading is already enabled!")
        else:
            logger.warning("\nTrading is not fully enabled. For CI environments, you need to:")
            logger.warning("1. Create a pre-configured terminal with these settings:")
            logger.warning("   - Tools -> Options -> Expert Advisors:")
            logger.warning("   - Enable 'Allow automated trading'")
            logger.warning("   - Enable 'Allow DLL imports'")
            logger.warning("   - Enable 'Allow WebRequest for listed URL'")
            logger.warning("\n2. Package the pre-configured terminal with your CI pipeline")
            logger.warning("3. Use the pre-configured terminal path in your tests")
            logger.warning("\nNote: These settings cannot be enabled programmatically")
            sys.exit(1)
            
        # Test symbol selection
        symbol = "EURUSD"
        logger.info(f"\nTesting symbol selection with {symbol}...")
        if not Mt5.symbol_select(symbol, True):
            logger.error(f"Failed to select symbol {symbol}")
            sys.exit(1)
        
        symbol_info = Mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Failed to get symbol info for {symbol}")
            sys.exit(1)
            
        logger.info(f"Symbol {symbol} info:")
        logger.info(f"Trade mode: {symbol_info.trade_mode}")
        logger.info(f"Visible: {symbol_info.visible}")
        logger.info(f"Bid: {symbol_info.bid}")
        logger.info(f"Ask: {symbol_info.ask}")
        
    finally:
        Mt5.shutdown()

if __name__ == "__main__":
    main() 